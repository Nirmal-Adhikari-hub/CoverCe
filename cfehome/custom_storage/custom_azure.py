from storages.backends.azure_storage import AzureStorage
# from azure.storage.blob import BlobServiceClient
# from cfehome.settings import AZURE_CUSTOM_DOMAIN, AZURE_ACCOUNT_KEY, AZURE_CONTAINER

class AzureProtectedStorage(AzureStorage):
    location = 'protected'
    # container_name = AZURE_CONTAINER  # Update with your container name
    # account_url = AZURE_CUSTOM_DOMAIN  # Update with your storage account URL
    # account_key = AZURE_ACCOUNT_KEY  # Update with your storage account key

    # def _get_blob_client(self, name):
    #     blob_service_client = BlobServiceClient(account_url=self.account_url, credential=self.account_key)
    #     container_client = blob_service_client.get_container_client(self.container_name)
    #     blob_client = container_client.get_blob_client(self.location + '/' + name)
    #     return blob_client

class AzureStaticStorage(AzureStorage):
    location = 'static'