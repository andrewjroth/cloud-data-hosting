from flask import Flask, render_template
import boto3


app = Flask(__name__)


@app.route('/')
def index():
    s3 = boto3.resource('s3')
    buckets = s3.buckets.all()
    return render_template("page.html", items=buckets)


@app.route('/<path:path>')
def get(path):
    split_path = path.split('/')
    bucket = split_path[0]
    prefix = ""
    if len(split_path) > 1:
        prefix = "/".join(split_path[1:])
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    objects = bucket.objects.filter(Prefix=prefix)
    return render_template("page.html", items=objects)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True) # Run Debug Server
