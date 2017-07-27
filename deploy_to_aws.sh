ENV="TESTING"
AWS_PROFILE="PROD"

AWS_LAMBDA_APP_FUNCTION_NAME="***REMOVED***"
AWS_LAMBDA_DB_FUNCTION_NAME="***REMOVED***-db-helper"
S3_STATIC_CONTENT_BUCKET_NAME="***REMOVED***"

CODE_DIR="./src" 
LIB_DIR="./lib"
BUILD_DIR="./build"

APP_ARCHIVE_FILENAME="archive_app_123455125214.zip" # guaranteed to be unique
DB_ARCHIVE_FILENAME="archive_db_2222222222215.zip" # guaranteed to be unique

mkdir $BUILD_DIR
cp -r $CODE_DIR/* $BUILD_DIR
ditto -c -k --sequesterRsrc $BUILD_DIR $DB_ARCHIVE_FILENAME

cp -r $LIB_DIR/* $BUILD_DIR
ditto -c -k --sequesterRsrc $BUILD_DIR $APP_ARCHIVE_FILENAME

if [ "$ENV" = "TESTING" ]; then
  AWS_LAMBDA_APP_FUNCTION_NAME="$AWS_LAMBDA_APP_FUNCTION_NAME-staging"
  AWS_LAMBDA_DB_FUNCTION_NAME="$AWS_LAMBDA_DB_FUNCTION_NAME-staging"
  S3_STATIC_CONTENT_BUCKET_NAME="$S3_STATIC_CONTENT_BUCKET_NAME-staging"
fi

aws lambda update-function-code --function-name $AWS_LAMBDA_APP_FUNCTION_NAME --zip-file fileb://$APP_ARCHIVE_FILENAME --profile $AWS_PROFILE
aws lambda update-function-code --function-name $AWS_LAMBDA_DB_FUNCTION_NAME --zip-file fileb://$DB_ARCHIVE_FILENAME --profile $AWS_PROFILE

aws s3 cp ./src/frontend/ s3://$S3_STATIC_CONTENT_BUCKET_NAME/ --recursive --profile $AWS_PROFILE

rm -r $BUILD_DIR
rm $APP_ARCHIVE_FILENAME
rm $DB_ARCHIVE_FILENAME
