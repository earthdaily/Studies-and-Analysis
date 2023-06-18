import os
import glob
import pandas as pd
import numpy as np
import boto3
from urllib.parse import urlparse
from sklearn.metrics import confusion_matrix
from rasterio.session import AWSSession
import rasterio
import matplotlib.pyplot as plt

def uri_scl_aws(row_df):
    """Identifies uri S3 from the information contained in the dataframe
    [tile, year, month, and day]

    Args:
        row_df (pandas.DataFrame): A DataFrame object containing the information required to construct the S3 URI, such as the tile, year, month, and day.

    Returns:
        str: The S3 URI constructed from the given information.
    """    
    tile = str(row_df['tile'])
    year = str(row_df['year'])
    month = str(row_df['month'])
    day = str(row_df['day'])
    uri_aws = f's3://sentinel-s2-l2a/tiles/{tile[1:3]}/{tile[3]}/{tile[4:6]}/{year}/{month}/{day}/0/R20m/SCL.jp2'
    return uri_aws

def list_available_data(bucket_name):
    """List availables data stored on the bucket

    Args:
        bucket_name (str): The name of the bucket to list the data from.

    Returns:
        df (pandas.DataFrame): A dataframe of the available data stored in the bucket.
    """    
    
    # connexion AWS
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=bucket_name, Delimiter='/')
    folder_list = []
    list_acm = []
    list_wqr = []
    
    for folder in response.get('CommonPrefixes', []): # list of folder in the bucket
        folder_name = folder.get('Prefix').rstrip('/')
        folder_list.append(folder_name)
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder.get('Prefix'))
        # search corresponding ACM and WQR mask
        for obj in response.get('Contents', []):
            nom_fichier = obj.get('Key')
            if nom_fichier.endswith('acm.tif'):
                list_acm.append('s3://ens-acm/' + nom_fichier)
            if nom_fichier.endswith('mask.tif'):
                list_wqr.append('s3://ens-acm/' + nom_fichier)
            '''if nom_fichier.endswith('GS2.tif'):
                list_gs2.append('s3://ens-acm/' + nom_fichier)'''

    df = pd.DataFrame({'dataset_name': folder_list, 'ACM': list_acm, 'WQR': list_wqr})
    
    df['tile'] = df['ACM'].apply(lambda x: os.path.splitext(os.path.split(x)[1])[0].split('_')[1])
    df['year'] = df['ACM'].apply(lambda x: os.path.splitext(os.path.split(x)[1])[0].split('_')[2][:4])
    df['month'] = df['ACM'].apply(lambda x: os.path.splitext(os.path.split(x)[1])[0].split('_')[2][4:6].lstrip('0'))
    df['day'] = df['ACM'].apply(lambda x: os.path.splitext(os.path.split(x)[1])[0].split('_')[2][6:].lstrip('0'))
    
    df['SCL'] = df.apply(uri_scl_aws, axis=1)   
    
    return df

def compute_accuracy_from_df(aws_session,df):
    """Compute a confusion matrix from multiple datasets contained in the dataframe and plot the results.

    Args:
        aws_session (boto3.Session): An AWS session object.
        df (pandas.DataFrame): A dataframe containing the dataset information.

    Returns:
        numpy.ndarray: The computed confusion matrix on :
        - ACM vs WQR
        - SCL vs WQR
        - SCL vs ACM
    """   
    mat_final_acm = np.array([[0, 0], [0, 0]])
    mat_final_scl = np.array([[0, 0], [0, 0]])
    mat_final = np.array([[0, 0], [0, 0]])
    with rasterio.Env(aws_session) as env:
        for idx, data in df.iterrows():
            with rasterio.open(data['SCL']) as src_scl, rasterio.open(data['ACM']) as src_acm, rasterio.open(data['WQR']) as src_wqr:
                # read mask on AWS
                mask_scl = np.repeat(np.repeat(src_scl.read(1), 2, axis=0), 2, axis=1)
                mask_acm = src_acm.read(1)
                mask_wqr = src_wqr.read(1)
                
                # Apply mask to ignore nodata
                masque = (mask_scl != src_scl.nodata) & (mask_acm != src_acm.nodata)

                final_scl = np.full(mask_scl.shape, fill_value=0, dtype=np.uint8)
                final_scl[np.isin(mask_scl, [3, 8, 9, 10, 11])] = 1

                final_acm = np.full(mask_acm.shape, fill_value=0, dtype=np.uint8)
                final_acm[mask_acm == 2] = 1

                final_wqr = np.full(mask_wqr.shape, fill_value=0, dtype=np.uint8)
                final_wqr[mask_wqr == 2] = 1

                final_scl = final_scl[masque]
                final_acm = final_acm[masque]

                # compute matrix confusion
                matrice_confusion = confusion_matrix(final_acm.flatten(), final_wqr.flatten())
                mat_final_acm = mat_final_acm + matrice_confusion
                matrice_confusion = confusion_matrix(final_scl.flatten(), final_wqr.flatten())
                mat_final_scl = mat_final_scl + matrice_confusion
                matrice_confusion = confusion_matrix(final_scl.flatten(), final_acm.flatten())
                mat_final = mat_final + matrice_confusion
    
    # convert to pourcentage
    sum_mat = np.sum(mat_final_acm)
    mat_final_acm_pourc = (mat_final_acm / sum_mat) * 100
    sum_mat = np.sum(mat_final_scl)
    mat_final_scl_pourc = (mat_final_scl / sum_mat) * 100
    sum_mat = np.sum(mat_final)
    mat_final_pourc = (mat_final / sum_mat) * 100

    plot_matrix_confusion(np.round(mat_final_acm_pourc),'ACM','WQR')
    plot_matrix_confusion(np.round(mat_final_scl_pourc),'SCL','WQR')
    plot_matrix_confusion(np.round(mat_final_pourc),'SCL','ACM')
    
    return np.round(mat_final_acm_pourc), np.round(mat_final_scl_pourc), np.round(mat_final_pourc)

def compute_accuracy_from_path(aws_session, mask_acm, mask_scl, mask_wqr):
    """Compute a confusion matrix from S3 URIs for ACM, SCL, and WQR and plot the results.

    Args:
        aws_session (boto3.Session): An AWS session object.
        mask_acm (str): The S3 URI for ACM.
        mask_scl (str): The S3 URI for SCL.
        mask_wqr (str): The S3 URI for WQR.
        
    Returns:
        numpy.ndarray: The computed confusion matrix on :
        - ACM vs WQR
        - SCL vs WQR
        - SCL vs ACM
    """
    
    mat_final_acm = np.array([[0, 0], [0, 0]])
    mat_final_scl = np.array([[0, 0], [0, 0]])
    mat_final = np.array([[0, 0], [0, 0]])
    
    with rasterio.Env(aws_session) as env:
        with rasterio.open(mask_scl) as src_scl, rasterio.open(mask_acm) as src_acm, rasterio.open(mask_wqr) as src_wqr:
            # read mask on AWS
            mask_scl = np.repeat(np.repeat(src_scl.read(1), 2, axis=0), 2, axis=1)
            mask_acm = src_acm.read(1)
            mask_wqr = src_wqr.read(1)
            
            # Apply mask to ignore nodata
            masque = (mask_scl != src_scl.nodata) & (mask_acm != src_acm.nodata)

            final_scl = np.full(mask_scl.shape, fill_value=0, dtype=np.uint8)
            final_scl[np.isin(mask_scl, [3, 9, 10, 11])] = 1

            final_acm = np.full(mask_acm.shape, fill_value=0, dtype=np.uint8)
            final_acm[mask_acm == 2] = 1

            final_wqr = np.full(mask_wqr.shape, fill_value=0, dtype=np.uint8)
            final_wqr[mask_wqr == 2] = 1

            final_scl = final_scl[masque]
            final_acm = final_acm[masque]

            # compute matrix confusion
            matrice_confusion = confusion_matrix(final_acm.flatten(), final_wqr.flatten())
            mat_final_acm = mat_final_acm + matrice_confusion
            matrice_confusion = confusion_matrix(final_scl.flatten(), final_wqr.flatten())
            mat_final_scl = mat_final_scl + matrice_confusion
            matrice_confusion = confusion_matrix(final_scl.flatten(), final_acm.flatten())
            mat_final = mat_final + matrice_confusion

    # convert to pourcentage
    sum_mat = np.sum(mat_final_acm)
    mat_final_acm_pourc = (mat_final_acm / sum_mat) * 100
    sum_mat = np.sum(mat_final_scl)
    mat_final_scl_pourc = (mat_final_scl / sum_mat) * 100
    sum_mat = np.sum(mat_final)
    mat_final_pourc = (mat_final / sum_mat) * 100

    plot_matrix_confusion(np.round(mat_final_acm_pourc),'ACM','WQR')
    plot_matrix_confusion(np.round(mat_final_scl_pourc),'SCL','WQR')
    plot_matrix_confusion(np.round(mat_final_pourc),'SCL','ACM')
    
    return np.round(mat_final_acm_pourc), np.round(mat_final_scl_pourc), np.round(mat_final_pourc)

def plot_matrix_confusion(mat_confusion,pred,true_data):
    """Plot matrix confusion

    Args:
        mat_confusion (numpy.ndarray): The confusion matrix.
        pred (numpy.ndarray): The predicted labels.
        true_data (numpy.ndarray): The true labels.
    """    
    # Column and row names
    column_names = [ 'clear', 'cloud']
    row_names = [ 'clear', 'cloud']

    # Create dataframe
    df = pd.DataFrame(mat_confusion, index=row_names, columns=column_names)

    # Plot
    plt.figure(figsize=(4, 4))
    plt.axis('off')

    plt.text(0.5, 0.95, true_data, fontsize=12, fontweight='bold', ha='center', va='center')
    plt.text(-0.25, 0.25, pred, fontsize=12, fontweight='bold', ha='center', va='center')

    # Plot confusion matrix
    tableau = plt.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, cellLoc='center', loc='center',
                        cellColours=plt.cm.RdYlGn(df.values / np.max(df.values)), bbox=[0, 0, 1, 0.9])

    tableau.auto_set_font_size(False)
    tableau.set_fontsize(10)
    tableau.scale(1, 1.5)

    # compute accuracy, over/under cloud detection
    accuracy = mat_confusion[0,0] + mat_confusion[1,1]
    over_detection = mat_confusion[1,0]
    under_detection = mat_confusion[0,1]
    print("Analysis of {} vs {}: \naccuracy {}%, over cloud detection {}%, under cloud detection {}%".format(pred, true_data, accuracy, over_detection, under_detection))
    
    plt.show()
    
def download_s3_files(str_s3_path):
    """download files stored on aws S3 bucket

    Args:
        str_s3_path (str): URI S3 (aws)
    """    
    s3 = boto3.resource('s3')
    parsed_url = urlparse(str_s3_path)
    bucket_name = parsed_url.netloc
    directory_name = parsed_url.path.lstrip('/')
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=directory_name):
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        bucket.download_file(obj.key, obj.key)
    