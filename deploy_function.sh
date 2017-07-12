ditto -c -k --sequesterRsrc lambda_package archive.zip
aws lambda update-function-code --function-name functionv5 --zip-file fileb://archive.zip