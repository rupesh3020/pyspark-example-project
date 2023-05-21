from azure.storage.blob import BlobServiceClient

# Create a BlobServiceClient object
connection_string = "AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;DefaultEndpointsProtocol=http;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Retrieve a container client
container_name = "datasource"
container_client = blob_service_client.get_container_client(container_name)

# List blobs in the container
blobs = container_client.list_blobs()
for blob in blobs:
    print("Blob name:", blob.name)
    print("Blob size:", blob.size)
    print("Blob content type:", blob.content_settings.content_type)
    print()

# Download a blob
blob_name = "myblob.txt"
blob_client = container_client.get_blob_client(blob_name)
with open("downloaded_blob.txt", "wb") as f:
    data = blob_client.download_blob()
    data.readinto(f)

# Upload a blob
upload_blob_name = "uploaded_blob.txt"
with open("path/to/local/file.txt", "rb") as f:
    blob_client.upload_blob(upload_blob_name, f)

# Delete a blob
delete_blob_name = "blob_to_delete.txt"
blob_client.delete_blob(delete_blob_name)