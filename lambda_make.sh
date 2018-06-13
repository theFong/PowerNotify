cd ~/GoogleDrive/WorkStation/PowerNotify/
rm -rf lambda_zip/
mkdir lambda_zip/
cp -r env/lib/python3.6/site-packages/* lambda_zip/
cp -r .aws lambda_zip0/
cp app_lambda.py lambda_zip/app.py
cp email_creds.py lambda_zip/
cd lambda_zip0/