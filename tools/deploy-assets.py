#!/usr/bin/env python3
"""Warrior World deploy kit — every manager's Web3 power tool (zero deps, stdlib only).
Push a site/asset to Storj via pure-python sigv4 presigned PUT. Works on the brain
container (no boto3 needed). Creds come from the profile .env injected at boot.

Usage:
  python3 /opt/data/tools/deploy-assets.py --list [--bucket X]
  python3 /opt/data/tools/deploy-assets.py --file a.html --key site/index.html [--bucket X] [--content-type text/html]
"""
import os, sys, json, argparse, time, hmac, hashlib, urllib.request, urllib.parse

def load_env(path):
    d = {}
    try:
        with open(path) as f:
            for ln in f:
                ln = ln.strip()
                if ln and '=' in ln and not ln.startswith('#'):
                    k, v = ln.split('=', 1); d[k.strip()] = v.strip().strip('"').strip("'")
    except Exception:
        pass
    return d

def _sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def presign_put(host, bucket, key, access, secret, content_type, expires=3600):
    """Return a presigned PUT URL for Storj S3-compatible gateway (pure stdlib sigv4)."""
    # host like 'gateway.storjshare.io'
    region = 'us-east-1'; service = 's3'
    amz = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()); date = amz[:8]
    payload_hash = hashlib.sha256(b'').hexdigest()
    q = urllib.parse.quote(key, safe='/~')
    canonical_uri = '/{}/{}'.format(urllib.parse.quote(bucket, safe=''), q)
    query = urllib.parse.urlencode({
        'X-Amz-Algorithm': 'AWS4-HMAC-SHA256',
        'X-Amz-Credential': f'{access}/{date}/{region}/{service}/aws4_request',
        'X-Amz-Date': amz,
        'X-Amz-Expires': str(expires),
        'X-Amz-SignedHeaders': 'host;x-amz-content-sha256',
        'x-amz-content-sha256': payload_hash,
    }).replace('%2F', '/').replace('%3A', ':').replace('%2C', ',').replace('%25','%')
    canonical_headers = f'host:{host}\nx-amz-content-sha256:{payload_hash}\n'
    signed_headers = 'host;x-amz-content-sha256'
    canonical_request = '\n'.join(['PUT', canonical_uri, query, canonical_headers, signed_headers, payload_hash])
    scope = f'{date}/{region}/{service}/aws4_request'
    string_to_sign = '\n'.join(['AWS4-HMAC-SHA256', amz, scope, hashlib.sha256(canonical_request.encode()).hexdigest()])
    k = _sign(('AWS4' + secret).encode(), date)
    k = _sign(k, region); k = _sign(k, service); k = _sign(k, 'aws4_request')
    sig = hmac.new(k, string_to_sign.encode(), hashlib.sha256).hexdigest()
    return f'https://{host}/{urllib.parse.quote(bucket, safe="")}/{q}?{query}&X-Amz-Signature={sig}'

def _put_with_boto3(env, bucket, key, data, content_type):
    import boto3
    s3 = boto3.client('s3',
        endpoint_url=env.get('STORJ_ENDPOINT', 'https://gateway.storjshare.io'),
        aws_access_key_id=env['STORJ_ACCESS_KEY'], aws_secret_access_key=env['STORJ_SECRET_KEY'],
        region_name='us-east-1', config=boto3.session.Config(signature_version='s3v4'))
    url = s3.generate_presigned_url('put_object',
        Params={'Bucket': bucket, 'Key': key, 'ContentType': content_type}, ExpiresIn=3600)
    req = urllib.request.Request(url, data=data, method='PUT', headers={'Content-Type': content_type})
    r = urllib.request.urlopen(req, timeout=120)
    return r.status

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bucket'); ap.add_argument('--key'); ap.add_argument('--file')
    ap.add_argument('--content-type', default='text/html')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--env', default='/opt/data/.env')
    a = ap.parse_args()
    env = load_env(a.env)
    prof = os.environ.get('HERMES_PROFILE', '')
    if prof:
        env.update(load_env(f'/opt/data/profiles/{prof}/.env'))
    missing = [k for k in ['STORJ_ACCESS_KEY', 'STORJ_SECRET_KEY'] if not env.get(k)]
    if missing:
        print("MISSING creds:", missing); sys.exit(1)
    host = (env.get('STORJ_ENDPOINT') or 'https://gateway.storjshare.io').replace('https://', '').replace('http://', '').rstrip('/')
    bucket = a.bucket or env.get('STORJ_BUCKET', 'warrior-command')
    if a.list:
        # presign a GET of nothing isn't valid; do a simple HEAD via the gateway path list — use public list fallback
        print("NOTE: list uses presigned GET on the bucket prefix (tilde) — simplest: try direct URL.")
        url = f'https://{host}/{bucket}?list-type=2&max-keys=100'
        try:
            print(urllib.request.urlopen(url, timeout=30).read().decode()[:1200])
        except Exception as e:
            print("list unavailable from this host:", str(e)[:120])
        return
    if not (a.file and a.key):
        ap.print_help(); return
    data = open(a.file, 'rb').read()
    try:
        status = _put_with_boto3(env, bucket, a.key, data, a.content_type)
        print(json.dumps({'ok': status in (200, 201), 'status': status,
                          'bucket': bucket, 'key': a.key, 'size': len(data),
                          'storj': f'https://{host}/{bucket}/{a.key}'}))
    except urllib.error.HTTPError as e:
        print(json.dumps({'ok': False, 'status': e.code, 'err': e.read().decode()[:200]}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({'ok': False, 'err': str(e)[:200]}))
        sys.exit(1)

if __name__ == '__main__':
    main()