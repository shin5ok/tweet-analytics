import os

class GCP_NL:
    def __init__(self):
        pass

    def __repr__(self):
        return "GCP_NL"

    def sentiment(self, text):
        from google.cloud import language_v1
        language = language_v1.LanguageServiceClient()
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        return language.analyze_sentiment(request={'document': document}).document_sentiment


class GCS:
    def __init__(self, project, bucket_name):
        from google.cloud import storage

        self.project = project
        self.bucket_name = bucket_name
        self.storage_client = storage.Client()

    def put(self, file_name):
        upload_file_name = os.path.basename(file_name)
        bucket = self.storage_client.bucket(self.bucket_name)
        try:
            blob = bucket.blob(upload_file_name)
            blob.upload_from_filename(file_name)
        except Exception as e:
            print(str(e))
        finally:
            os.unlink(file_name)
