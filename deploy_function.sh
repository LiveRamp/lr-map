ARCHIVE_FILENAME="archive_temporary123455125214.zip" # guaranteed to be unique
AWS_LAMBDA_FUNCTION_NAME="functionv5"
DIRECTORY_WITH_CONTENT="./lambda_package"

ditto -c -k --sequesterRsrc $DIRECTORY_WITH_CONTENT $ARCHIVE_FILENAME
aws lambda update-function-code --function-name $AWS_LAMBDA_FUNCTION_NAME --zip-file fileb://$ARCHIVE_FILENAME
rm $ARCHIVE_FILENAME