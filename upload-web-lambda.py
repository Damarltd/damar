import boto3
import StringIO
import zipfile
import mimetypes

s3 = boto3.resource('s3')

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
