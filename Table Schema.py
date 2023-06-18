
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.core.credentials import AzureNamedKeyCredential
from azure.data.tables import TableServiceClient
from datetime import datetime
import os
from uuid import uuid4
from dotenv import find_dotenv, load_dotenv

credential = AzureNamedKeyCredential("my_account_name", "my_access_key")

service = TableServiceClient(endpoint="https://<my_account_name>.table.core.windows.net", credential=credential)
service = TableServiceClient(endpoint="https://<my_account_name>.table.core.windows.net/", credential=credential)
os.environ["PASSWORD"] = "Shaskruthi@29"
os.environ["SUBSCRIPTION_ID"] = "f92db8b9-56a2-4908-803e-00c3bcd33545"
os.environ["TABLES_PRIMARY_STORAGE_ACCOUNT_KEY"]="IlI2zn21931nVBR1/OLwVjX6ci0d4620qm8WZ6zFNDUoHfQgk3o2XeLc26MRI0XbC2K3qNV0Vnnv+ASt6P55zg=="
os.environ["TABLES_STORAGE_ENDPOINT_SUFFIX"]="core.cloudapi.de"
def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    PASSWORD = os.environ.get("PASSWORD", None)
    GROUP_NAME = "myResourceGroup1"
    DATABASE = "RED_FLAGS"
    SERVER = "mysqlserver239"

    #table_client = TableClient.from_connection_string(conn_str="<connection_string>", table_name="userdetails")

    # Create client
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    sql_client = SqlManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
credential = AzureNamedKeyCredential("redflags", "IlI2zn21931nVBR1/OLwVjX6ci0d4620qm8WZ6zFNDUoHfQgk3o2XeLc26MRI0XbC2K3qNV0Vnnv+ASt6P55zg==")

service = TableServiceClient(endpoint="https://f20212922@hyderabad.bits-pilani.ac.in.table.core.windows.net", credential=credential)
service = TableServiceClient(endpoint="https://f20212922@hyderabad.bits-pilani.ac.in.table.core.windows.net/", credential=credential)

table_service_client = TableServiceClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;AccountName=redflags;AccountKey=FV1rsC6jNn8q0v4Vg3JZ7YcrI7GjTP2fxfzP+blXm1PIpM3ZgoVes2mrBJNGZOlyXKLr6MAF8XEA+ASt9UjOoA==;EndpointSuffix=core.windows.net")
table_name = "Users"
#table_client = table_service_client.create_table(table_name=table_name)

class InsertDeleteEntity(object):
    def __init__(self):
        load_dotenv(find_dotenv())
        self.access_key = os.getenv("TABLES_PRIMARY_STORAGE_ACCOUNT_KEY")
        self.endpoint_suffix = os.getenv("TABLES_STORAGE_ENDPOINT_SUFFIX")
        self.account_name = os.getenv("TABLES_STORAGE_ACCOUNT_NAME")
        self.endpoint = "{}.table.{}".format(self.account_name, self.endpoint_suffix)
        self.connection_string = (
            "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix={}".format(
                self.account_name, self.access_key, self.endpoint_suffix
            )
        )

        self.table_name = "SampleInsertDelete"

        self.entity = {
            "PartitionKey": "User_id",
            "RowKey": "Name",
            "Symptoms": "Back_pain",
            "Diagnosis": "Back Pain",
            "Qustions_Answered": "Questions 1,2,3",
            "last_updated": datetime.today()
            
        }




    def create_entity(self):
        from azure.data.tables import TableClient
        from azure.core.exceptions import ResourceExistsError, HttpResponseError

        with TableClient.from_connection_string(self.connection_string, self.table_name) as table_client:

            # Create a table in case it does not already exist
            """try:
                table_client.create_table()
            except HttpResponseError:
                print("Table already exists")"""

            # [START create_entity]
            try:
                resp = table_client.create_entity(entity=self.entity)
                print(resp)
            except ResourceExistsError:
                print("Entity already exists")

    def delete_entity(self):
        from azure.data.tables import TableClient
        from azure.core.exceptions import ResourceExistsError
        from azure.core.credentials import AzureNamedKeyCredential

        credential = AzureNamedKeyCredential(self.account_name, self.access_key) # type: ignore[arg-type]
        with TableClient(endpoint=self.endpoint, table_name=self.table_name, credential=credential) as table_client:

            # Create entity to delete (to showcase etag)
            try:
                table_client.create_entity(entity=self.entity)
            except ResourceExistsError:
                print("Entity already exists!")

            # [START delete_entity]
            table_client.delete_entity(row_key=self.entity["RowKey"], partition_key=self.entity["PartitionKey"])
            print("Successfully deleted!")
            # [END delete_entity]



if __name__ == "__main__":
    ide = InsertDeleteEntity()
    ide.create_entity()
    ide.delete_entity()
   
