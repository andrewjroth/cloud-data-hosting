# cloud-data-hosting

=== App Config Options ===

Settings can be configured in a file indicated by FLASK_SETTINGS.

* S3_REDIRECT - If True, will redirect object downloads to S3 instead of streaming the content back directly.
* ROOT_LIST - Dictionary (dict) of display names translated to bucket names for the homepage (root index).
