AWS_LAMBDA_MAIN_FUNCTION_NAME="functionv5"
AWS_LAMBDA_ADD_TO_DB_FUNCTION_NAME="addToMapDb"
S3_BUCKET_NAME="map42"

DIRECTORY_WITH_CONTENT="./code" 
DIRECTORY_WITH_DB_HELPER="./db_helper_lambda"
DIRECTORY_WITH_FILES_TO_BE_COPIED="./environment"
BUILD_DIR="./build"

MAIN_ARCHIVE_FILENAME="archive_temporary123455125214.zip" # guaranteed to be unique
DB_HELPER_ARCHIVE_FILENAME="archive_temporary2222222222215.zip" # guaranteed to be unique

mkdir $BUILD_DIR
cp -r $DIRECTORY_WITH_CONTENT/* $BUILD_DIR
cp -r $DIRECTORY_WITH_FILES_TO_BE_COPIED/* $BUILD_DIR



ditto -c -k --sequesterRsrc $BUILD_DIR $MAIN_ARCHIVE_FILENAME
ditto -c -k --sequesterRsrc $DIRECTORY_WITH_DB_HELPER $DB_HELPER_ARCHIVE_FILENAME

aws lambda update-function-code --function-name $AWS_LAMBDA_MAIN_FUNCTION_NAME --zip-file fileb://$MAIN_ARCHIVE_FILENAME
aws lambda update-function-code --function-name $AWS_LAMBDA_ADD_TO_DB_FUNCTION_NAME --zip-file fileb://$DB_HELPER_ARCHIVE_FILENAME

rm -r $BUILD_DIR
rm $MAIN_ARCHIVE_FILENAME
rm $DB_HELPER_ARCHIVE_FILENAME