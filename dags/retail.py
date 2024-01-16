from airflow.decorators import dag, task
from datetime import datetime
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyTableOperator,BigQueryGetDataOperator
from astro import sql as aql
from astro.constants import FileType
from astro.sql.table import Table, Metadata
from astro.files import File
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from astro.files import File
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator,BigQueryExecuteQueryOperator
from datetime import datetime, timedelta
from airflow.operators.email import EmailOperator 
@dag(   
    start_date=datetime(2023, 12, 1),
    schedule_interval='05 07 * * *', 
    catchup=False,
    tags=['retail',],
)
def retail():
    upload_csv_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_csv_to_gcs',
        src='/usr/local/airflow/include/dataset/delta_load.csv',
        dst=f'ssrn_online_retail/online_retail_{{{{ ds_nodash }}}}.csv',
        bucket='ssrn_online_retail',
        gcp_conn_id='gcp',  
        mime_type='test/csv'
    )
    
    load_csv = GCSToBigQueryOperator(
    gcp_conn_id='gcp',
    task_id="load_csv",
    bucket='ssrn_online_retail',
    source_objects=['ssrn_online_retail/online_retail_{{ ds_nodash }}.csv'],
    destination_project_dataset_table='airflow-project-409205:retail.raw_invoices',
    schema_fields=[
        {"name": "InvoiceNo", "type": "STRING", "mode": "NULLABLE"},
        {"name": "StockCode", "type": "STRING", "mode": "NULLABLE"},
        {"name": "Description", "type": "STRING", "mode": "NULLABLE"},
        {"name": "Quantity", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "InvoiceDate", "type": "STRING", "mode": "NULLABLE"},
        {"name": "UnitPrice", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "CustomerID", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "Country", "type": "STRING", "mode": "NULLABLE"},
    ],
    write_disposition="WRITE_APPEND",
)
    
    execute_query_save = BigQueryInsertJobOperator(
    task_id="execute_query_save",
    gcp_conn_id='gcp',
    configuration={
        "query": {
            "query": "select CAST(CustomerID AS STRING) as CustomerID,Country, ROUND(SUM(UnitPrice), 3) AS TotalPurchases FROM retail.raw_invoices WHERE CustomerID IS NOT NULL AND UnitPrice IS NOT NULL GROUP BY CustomerID, Country;",
            "useLegacySql": False,
            "writeDisposition": "WRITE_TRUNCATE",
            'destinationTable': {
                'projectId': "airflow-project-409205",
                'datasetId': "retail",
                'tableId': "Sales_Data"
            },
        }
    },
)
    #Used for archiving.
    archive_files = GCSToGCSOperator(
    task_id="archive_files",
    source_bucket="ssrn_online_retail",
    source_object=f'ssrn_online_retail/online_retail_{{{{ ds_nodash }}}}.csv',
    destination_bucket="ssrn_online_retail",
    destination_object=f'ssrn_online_retail_archive/online_retail_{{{{ ds_nodash }}}}.csv',
    move_object=True,
    gcp_conn_id='gcp',
)
    
    upload_csv_to_gcs >> load_csv >> execute_query_save >> archive_files

# I used below code for initial push
def intial_kick():
    a = BigQueryCreateEmptyDatasetOperator(
        task_id='a',
        dataset_id='retail',
        gcp_conn_id='gcp',
        project_id='airflow-project-409205'
    )
   
    #Used for archiving.
    archive_filess = GCSToGCSOperator(
    task_id="archive_filess",
    source_bucket="ssrn_online_retail",
    source_object=f'ssrn_online_retail/online_retail.csv',
    destination_bucket="ssrn_online_retail",
    destination_object=f'ssrn_online_retail_archive/online_retail.csv',
    move_object=True,
    gcp_conn_id='gcp',
)
    # bucket_to_bigquery = aql.load_file(
    #     task_id="bucket_to_bigquery",
    #     input_file=File(
    #         'gs://ssrn_online_retail/ssrn_online_retail/online_retail.csv',conn_id='gcp',filetype=FileType.CSV),
    #     output_table=Table(
    #         name='raw_invoices',
    #         conn_id='gcp',
    #         metadata=Metadata(schema='retail')
    #     ),
    #     use_native_support=False
    # )

    create_test_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id='create_schema',
        dataset_id='retail',
        project_id='airflow-project-409205' ,
        gcp_conn_id='gcp'
    )

    
    PROJECT_ID='airflow-project-409205'
    DATASET_NAME='retail'
    create_view = BigQueryCreateEmptyTableOperator(
    task_id="create_view",
    dataset_id="retail",
    table_id="temp1",
    gcp_conn_id='gcp',
    view={
        "query": f"SELECT DISTINCT CustomerID FROM `{PROJECT_ID}.{DATASET_NAME}.raw_invoices`",
        "useLegacySql": False,
    },
    
)
    get_data = BigQueryGetDataOperator(
    task_id="get_data",
    gcp_conn_id='gcp',
    dataset_id="retail",
    table_id="raw_",
    max_results=10,
    project_id='airflow-project-409205',
    location='US',
)   
    #Make a new data table by choosing the data by SQL from existing table in bigquery.
   
    modify_constraint_query = """


    ALTER TABLE `airflow-project-409205.retail.DIM_Sales`
    DROP COLUMN NewCustomer_ID;


"""
    modify_constraint_task = BigQueryExecuteQueryOperator(
    task_id='modify_constraint',
    gcp_conn_id='gcp',
    sql=modify_constraint_query,
    use_legacy_sql=False,  # Set to True if you're using legacy SQL
    )
    location='US'
retail_dag = retail()

    
    