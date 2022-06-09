# gcloud beta functions deploy --timeout=500 twitter-crawling --entry-point=main --runtime python39 \
# --update-env-vars=GOOGLE_CLOUD_PROJECT=$PROJECT,BUCKET_NAME=$PROJECT,TWITTER_KEY=$TWITTER_KEY,TWITTER_SECRET=$TWITTER_SECRET,TWITTER_ACCESS_TOKEN=$TWITTER_ACCESS_TOKEN,TWITTER_ACCESS_TOKEN_SECRET=$TWITTER_ACCESS_TOKEN_SECRET,COUNT=50 \
# --region=asia-northeast1 \
# --gen2 \
# --trigger-http \
# $@
# --trigger-topic=twitter-crawling-scheduler $@
gcloud run deploy --source=. get-tweet --timeout=600 \
--region=asia-northeast1 \
--set-env-vars=GOOGLE_CLOUD_PROJECT=$PROJECT,BUCKET_NAME=$PROJECT,TWITTER_API_KEY=$TWITTER_API_KEY,TWITTER_API_SECRET_KEY=$TWITTER_API_SECRET_KEY,TWITTER_ACCESS_TOKEN=$TWITTER_ACCESS_TOKEN,TWITTER_ACCESS_TOKEN_SECRET=$TWITTER_ACCESS_TOKEN_SECRET,COUNT=50,TOPIC=tweets \
--service-account=tweets@$PROJECT.iam.gserviceaccount.com \
$@
