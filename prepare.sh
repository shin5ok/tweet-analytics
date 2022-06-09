gcloud iam service-accounts create tweets
SA=$(gcloud iam service-accounts list --format=json | jq '.[].email|select(test("tweets"))' -r)
echo $SA
gcloud projects add-iam-policy-binding --member=serviceAccount:tweets@shingo-ar-twittertest.iam.gserviceaccount.com shingo-ar-twittertest --role=roles/pubsub.publisher

gcloud pubsub topics create tweets
gcloud pubsub subscriptions create tweets --topic=tweets

bq mk --data_location=US tweets
bq mk --schema=schema.json tweets.test
