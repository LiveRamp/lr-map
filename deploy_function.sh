AWS_LAMBDA_MAIN_FUNCTION_NAME="***REMOVED***"
AWS_LAMBDA_ADD_TO_DB_FUNCTION_NAME="***REMOVED***-db-helper"
S3_STATIC_CONTENT_BUCKET_NAME="***REMOVED***"

DIRECTORY_WITH_CONTENT="./code" 
DIRECTORY_WITH_DB_HELPER="./db_helper_lambda"
DIRECTORY_WITH_FILES_TO_BE_COPIED="./environment"
BUILD_DIR="./build"

MAIN_ARCHIVE_FILENAME="archive_main_123455125214.zip" # guaranteed to be unique
DB_HELPER_ARCHIVE_FILENAME="archive_db_2222222222215.zip" # guaranteed to be unique

mkdir $BUILD_DIR
cp -r $DIRECTORY_WITH_CONTENT/* $BUILD_DIR
cp -r $DIRECTORY_WITH_FILES_TO_BE_COPIED/* $BUILD_DIR

AWS_PROFILE=${AWS_PROFILE:-"TEST"}
CLI_PROFILE_ARG=" --profile $AWS_PROFILE"

if [ "$AWS_PROFILE" = "TEST" ]; then
    S3_STATIC_CONTENT_BUCKET_NAME="$S3_STATIC_CONTENT_BUCKET_NAME-test" # nothing if on production
fi

ditto -c -k --sequesterRsrc $BUILD_DIR $MAIN_ARCHIVE_FILENAME
ditto -c -k --sequesterRsrc $DIRECTORY_WITH_DB_HELPER $DB_HELPER_ARCHIVE_FILENAME

aws lambda update-function-code --function-name $AWS_LAMBDA_MAIN_FUNCTION_NAME --zip-file fileb://$MAIN_ARCHIVE_FILENAME --profile $AWS_PROFILE
aws lambda update-function-code --function-name $AWS_LAMBDA_ADD_TO_DB_FUNCTION_NAME --zip-file fileb://$DB_HELPER_ARCHIVE_FILENAME --profile $AWS_PROFILE


aws s3 cp ./code/frontend/index.html s3://$S3_STATIC_CONTENT_BUCKET_NAME/index.html --profile $AWS_PROFILE
aws s3 cp ./code/frontend/index.js s3://$S3_STATIC_CONTENT_BUCKET_NAME/index.js --profile $AWS_PROFILE
aws s3 cp ./code/frontend/style.css s3://$S3_STATIC_CONTENT_BUCKET_NAME/style.css --profile $AWS_PROFILE
aws s3 cp ./code/frontend/img/16th.png s3://$S3_STATIC_CONTENT_BUCKET_NAME/img/16th.png --profile $AWS_PROFILE
aws s3 cp ./code/frontend/img/17th.png s3://$S3_STATIC_CONTENT_BUCKET_NAME/img/17th.png --profile $AWS_PROFILE
aws s3 cp ./code/frontend/img/pin.png s3://$S3_STATIC_CONTENT_BUCKET_NAME/img/pin.png --profile $AWS_PROFILE

rm -r $BUILD_DIR
rm $MAIN_ARCHIVE_FILENAME
rm $DB_HELPER_ARCHIVE_FILENAME