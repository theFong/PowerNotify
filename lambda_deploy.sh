cd ~/GoogleDrive/WorkStation/PowerNotify/lambda_zip/
zip -r pn_lambda.zip .
aws lambda create-function  --region us-east-1  --function-name PowerNotify  --zip-file fileb://pn_lambda.zip  --role arn:aws:iam::138190232183:role/lambda_admin --handler app.lamda_event --runtime python3.6  --timeout 15  --memory-size 512
