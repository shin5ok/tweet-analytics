gcloud iam service-accounts create tweets
RUN_SA=$(gcloud iam service-accounts list --format=json | jq '.[].email|select(test("tweets"))' -r)
gcloud projects add-iam-policy-binding --member=serviceAccount:$RUN_SA $PROJECT --role=roles/pubsub.publisher

gcloud pubsub topics create tweets
gcloud pubsub subscriptions create tweets --topic=tweets

bq mk --data_location=US tweets
bq mk --schema=schema.json tweets.test
