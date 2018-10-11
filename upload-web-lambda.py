import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):

    s3 = boto3.resource('s3')
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:255162520246:deployWebTopic')

    location : {
        "bucketName:": 'webbuild.damar.agency',
        "objectKey": 'webbuild.zip'
    }
    try:
        job = event.get('CodePipeline.job')

        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "WebPipeline":
                    location = artifact["location"]["s3Location"]

        print "Building web from " + str(location)
        damaragency_bucket = s3.Bucket('damar.agency')
        build_bucket = s3.Bucket(location["bucketName"])

        webbuild_zip = StringIO.StringIO()
        build_bucket.download_fileobj(location["objectKey"], webbuild_zip)

        with zipfile.ZipFile(webbuild_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                damaragency_bucket.upload_fileobj(obj,nm,
                ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                damaragency_bucket.Object(nm).Acl().put(ACL='public-read')

        print "Job Done!"
        topic.publish(Subject="Website deployed", Message="Website build deployed succesfully!")
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])

    except:
        topic.publish(Subject="Website NOT deployed", Message="Website build NOT deployed succesfully!")
        raise
    return 'Hello from Lambda'
