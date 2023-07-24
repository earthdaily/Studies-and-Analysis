import os
import pandas as pd
import numpy as np
import boto3
from urllib.parse import urlparse
from sklearn.metrics import confusion_matrix
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


def list_available_data(s3_client, bucket_name):
    """List available data stored on the bucket

    Args:
        s3_client: aws s3_client
        bucket_name (str): The name of the bucket to list the data from.

    Returns:
        df (pandas.DataFrame): A dataframe of the available data stored in the bucket.
    """

    response = s3_client.list_objects_v2(Bucket=bucket_name, Delimiter='/')
    folder_list = []
    list_acm = []
    list_wqr = []

    for folder in response.get('CommonPrefixes', []):  # list of folder in the bucket
        folder_name = folder.get('Prefix').rstrip('/')
        folder_list.append(folder_name)
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder.get('Prefix'))
        # search corresponding ACM and WQR mask
        for obj in response.get('Contents', []):
            file_name = obj.get('Key')
            if file_name.endswith('acm.tif'):
                list_acm.append(f's3://{bucket_name}/' + file_name)
            if file_name.endswith('mask.tif'):
                list_wqr.append(f's3://{bucket_name}/' + file_name)
            '''if file_name.endswith('GS2.tif'):
                list_gs2.append('s3://ens-acm/' + file_name)'''

    df = pd.DataFrame({'dataset_name': folder_list, 'ACM': list_acm, 'WQR': list_wqr})

    df['tile'] = df['ACM'].apply(lambda x: os.path.splitext(os.path.split(x)[1])[0].split('_')[1])
    df['year'] = df['ACM'].apply(lambda x: os.path.splitext(os.path.split(x)[1])[0].split('_')[2][:4])
    df['month'] = df['ACM'].apply(lambda x: os.path.splitext(os.path.split(x)[1])[0].split('_')[2][4:6].lstrip('0'))
    df['day'] = df['ACM'].apply(lambda x: os.path.splitext(os.path.split(x)[1])[0].split('_')[2][6:].lstrip('0'))

    df['SCL'] = df.apply(uri_scl_aws, axis=1)

    return df


def list_available_local_data():
    """List available data stored on local

    Args:

    Returns:
        df (pandas.DataFrame): A dataframe of the available data stored in the bucket.
    """

    path = os.getcwd()
    mask_folder = os.path.join(path, "masks")
    folder_list = []
    list_acm = []
    list_wqr = []
    list_scl = []

    for folder_name, directories, fichiers in os.walk(mask_folder):
        for directory in directories:
            dir_path = os.path.join(folder_name, directory)
            folder_list.append(folder_name)

            for sub_folder, dirs, files in os.walk(dir_path):
                for file in files:
                    if file.endswith('acm.tif'):
                        list_acm.append(os.path.join(dir_path, file))
                    if file.endswith('mask.tif'):
                        list_wqr.append(os.path.join(dir_path, file))
                    if file.endswith('SCL.jp2'):
                        list_scl.append(os.path.join(dir_path, file))

    df = pd.DataFrame({'dataset_name': folder_list, 'ACM': list_acm, 'WQR': list_wqr, 'SCL': list_scl})

    df['tile'] = df['ACM'].apply(lambda x: os.path.splitext(os.path.split(x)[1])[0].split('_')[1])
    df['year'] = df['ACM'].apply(lambda x: os.path.splitext(os.path.split(x)[1])[0].split('_')[2][:4])
    df['month'] = df['ACM'].apply(
        lambda x: os.path.splitext(os.path.split(x)[1])[0].split('_')[2][4:6].lstrip('0'))
    df['day'] = df['ACM'].apply(
        lambda x: os.path.splitext(os.path.split(x)[1])[0].split('_')[2][6:].lstrip('0'))

    return df


def compute_accuracy_from_df(df, aws_session=None):
    """

    Args:
        df: panda data frame
        aws_session:

    Returns:

    """
    mat_final_acm = np.array([[0, 0], [0, 0]])
    mat_final_scl = np.array([[0, 0], [0, 0]])
    mat_final = np.array([[0, 0], [0, 0]])

    if aws_session is not None:
        for idx, data in df.iterrows():
            with rasterio.Env(aws_session) as env:
                with rasterio.open(data['SCL']) as src_scl, rasterio.open(data['ACM']) as src_acm, rasterio.open(
                        data['WQR']) as src_wqr:
                    process_data(src_scl, src_acm, src_wqr, mat_final_acm, mat_final_scl, mat_final)
    else:
        for idx, data in df.iterrows():
            with rasterio.open(data['SCL']) as src_scl, rasterio.open(data['ACM']) as src_acm, rasterio.open(
                    data['WQR']) as src_wqr:
                process_data(src_scl, src_acm, src_wqr, mat_final_acm, mat_final_scl, mat_final)

    # Convert to percentage
    sum_mat = np.sum(mat_final_acm)
    mat_final_acm_pourc = (mat_final_acm / sum_mat) * 100
    sum_mat = np.sum(mat_final_scl)
    mat_final_scl_pourc = (mat_final_scl / sum_mat) * 100
    sum_mat = np.sum(mat_final)
    mat_final_pourc = (mat_final / sum_mat) * 100

    plot_matrix_confusion(np.round(mat_final_acm_pourc), 'ACM', 'WQR')
    plot_matrix_confusion(np.round(mat_final_scl_pourc), 'SCL', 'WQR')
    plot_matrix_confusion(np.round(mat_final_pourc), 'SCL', 'ACM')

    return np.round(mat_final_acm_pourc), np.round(mat_final_scl_pourc), np.round(mat_final_pourc)


def process_data(src_scl, src_acm, src_wqr, mat_final_acm, mat_final_scl, mat_final):
    """
    processing data
    Args:
        src_scl(str): path of scl data
        src_acm(str): path of acm data
        src_wqr(str): path of wqr data
        mat_final_acm(np array)
        mat_final_scl(np array)
        mat_final(np array)
    """
    # Read mask from path (AWS or local)
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

    # Compute matrix confusion
    matrice_confusion_acm = confusion_matrix(final_acm.flatten(), final_wqr.flatten())
    matrice_confusion_scl = confusion_matrix(final_scl.flatten(), final_wqr.flatten())
    matrice_confusion_scl_acm = confusion_matrix(final_scl.flatten(), final_acm.flatten())

    mat_final_acm += matrice_confusion_acm
    mat_final_scl += matrice_confusion_scl
    mat_final += matrice_confusion_scl_acm

def compute_accuracy_from_path(mask_acm, mask_scl, mask_wqr, aws_session=None):
    """Compute a confusion matrix from URIs or local path for ACM, SCL, and WQR and plot the results.

    Args:
        mask_acm (str): The S3 URI for ACM.
        mask_scl (str): The S3 URI for SCL.
        mask_wqr (str): The S3 URI for WQR.
        aws_session (boto3.Session): An AWS session object.

    Returns:
        numpy.ndarray: The computed confusion matrix on :
        - ACM vs WQR
        - SCL vs WQR
        - SCL vs ACM
    """

    mat_final_acm = np.array([[0, 0], [0, 0]])
    mat_final_scl = np.array([[0, 0], [0, 0]])
    mat_final = np.array([[0, 0], [0, 0]])

    if aws_session is not None:
        with rasterio.Env(aws_session):
            with rasterio.open(mask_scl) as src_scl, rasterio.open(mask_acm) as src_acm, rasterio.open(
                    mask_wqr) as src_wqr:
                process_data(src_scl, src_acm, src_wqr, mat_final_acm, mat_final_scl, mat_final)
    else:
        with rasterio.open(mask_scl) as src_scl, rasterio.open(mask_acm) as src_acm, rasterio.open(mask_wqr) as src_wqr:
            process_data(src_scl, src_acm, src_wqr, mat_final_acm, mat_final_scl, mat_final)

    # Convert to percentage
    sum_mat = np.sum(mat_final_acm)
    mat_final_acm_pourc = (mat_final_acm / sum_mat) * 100
    sum_mat = np.sum(mat_final_scl)
    mat_final_scl_pourc = (mat_final_scl / sum_mat) * 100
    sum_mat = np.sum(mat_final)
    mat_final_pourc = (mat_final / sum_mat) * 100

    plot_matrix_confusion(np.round(mat_final_acm_pourc), 'ACM', 'WQR')
    plot_matrix_confusion(np.round(mat_final_scl_pourc), 'SCL', 'WQR')
    plot_matrix_confusion(np.round(mat_final_pourc), 'SCL', 'ACM')

    return np.round(mat_final_acm_pourc), np.round(mat_final_scl_pourc), np.round(mat_final_pourc)


def plot_matrix_confusion(mat_confusion, pred, true_data):
    """Plot matrix confusion

    Args:
        mat_confusion (numpy.ndarray): The confusion matrix.
        pred (numpy.ndarray): The predicted labels.
        true_data (numpy.ndarray): The true labels.
    """
    # Column and row names
    column_names = ['clear', 'cloud']
    row_names = ['clear', 'cloud']

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
    accuracy = mat_confusion[0, 0] + mat_confusion[1, 1]
    over_detection = mat_confusion[1, 0]
    under_detection = mat_confusion[0, 1]
    print("Analysis of {} vs {}: \naccuracy {}%, over cloud detection {}%, under cloud detection {}%".format(pred,
                                                                                                             true_data,
                                                                                                             accuracy,
                                                                                                             over_detection,
                                                                                                             under_detection))

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
    for obj in bucket.objects.filter(Prefix=directory_name, RequestPayer='requester'):
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        bucket.download_file(obj.key, obj.key, ExtraArgs={'RequestPayer': 'requester'})
