ARCHIVE_FILENAME="archive_temporary123455125214.zip" # guaranteed to be unique
AWS_LAMBDA_FUNCTION_NAME="functionv5"
DIRECTORY_WITH_CONTENT="./code" 
DIRECTORY_WITH_FILES_TO_BE_COPIED="./environment"
BUILD_DIR="./build"

mkdir $BUILD_DIR
cp -r $DIRECTORY_WITH_CONTENT/* $BUILD_DIR
cp -r $DIRECTORY_WITH_FILES_TO_BE_COPIED/* $BUILD_DIR


ditto -c -k --sequesterRsrc $BUILD_DIR $ARCHIVE_FILENAME
aws lambda update-function-code --function-name $AWS_LAMBDA_FUNCTION_NAME --zip-file fileb://$ARCHIVE_FILENAME
rm $ARCHIVE_FILENAME