from flask import Flask, render_template, redirect, Response
import boto3


app = Flask(__name__)
#app.config.from_object('yourapplication.default_settings')
app.config.from_envvar('FLASK_SETTINGS')


@app.route('/')
def index():
    return render_template("index.html", path="/", items=app.config['ROOT_LIST'].keys())


@app.route('/<path:path>')
def get(path):
    client = boto3.client('s3')
    split_path = path.split('/', 1)
    bucket = app.config['ROOT_LIST'][split_path[0]]
    prefix = ""
    if len(split_path) > 1:
        prefix = split_path[1]
        if not prefix.endswith('/'): # return object
            if app.config['S3_REDIRECT']:
                response = client.generate_presigned_url("get_object", Params=dict(
                    Bucket=bucket, Key=prefix))
                return redirect(response)
            response = client.get_object(
                Bucket=bucket,
                Key=prefix
            )
            return Response(response['Body'], mimetype=response['ContentType'])
    folders = list()
    files = list()
    list_objects_args=dict(
        Bucket=bucket,
        Delimiter='/',
        Prefix=prefix,
    )
    while True:
        response = client.list_objects_v2(**list_objects_args)
        if 'CommonPrefixes' in response:
            folders.extend(map(lambda x: x['Prefix'][len(prefix):], response['CommonPrefixes']))
        if 'Contents' in response:
            files.extend(map(
                lambda x: dict(name=x['Key'][len(prefix):], last_modified=x['LastModified'], size=x['Size']), 
                response['Contents']
            ))
        if response['IsTruncated']:
            list_objects_args['ContinuationToken'] = response['NextContinuationToken']
        else:
            break
    return render_template("page.html", path='/'+path, folders=folders, files=files)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True) # Run Debug Server
