import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):

    s3 = boto3.resource('s3')
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:255162520246:deployWebTopic')

    try:

        damaragency_bucket = s3.Bucket('damar.agency')
        build_bucket = s3.Bucket('webbuild.damar.agency')

        webbuild_zip = StringIO.StringIO()
        build_bucket.download_fileobj('webbuild.zip', webbuild_zip)

        with zipfile.ZipFile(webbuild_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                damaragency_bucket.upload_fileobj(obj,nm,
                ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                damaragency_bucket.Object(nm).Acl().put(ACL='public-read')

        print "Job Done!"
        topic.publish(Subject="Website deployed", Message="Website build deployed succesfully!")

    except:
        topic.publish(Subject="Website NOT deployed", Message="Website build NOT deployed succesfully!")
        raise
    return 'Hello from Lambda'
