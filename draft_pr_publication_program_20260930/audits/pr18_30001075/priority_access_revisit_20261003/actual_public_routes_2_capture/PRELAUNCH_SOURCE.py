"""Bounded ordinary public HTTP retrieval; no credentials, bypass or outreach."""
from pathlib import Path
import argparse, datetime as dt, hashlib, json, os, sys, urllib.request, urllib.error

P=Path(__file__).absolute().parent
def utc(): return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def put(p,b):
    with p.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
def main():
    a=argparse.ArgumentParser();a.add_argument('input');a.add_argument('output');v=a.parse_args()
    source=Path(__file__).read_bytes();task=json.loads((P/v.input).read_bytes())
    cache=P/'private_cache';cache.mkdir(exist_ok=True)
    out=dict(schema='pr18-public-access-revisit-actual-retrieval/v1',actual_pid=os.getpid(),actual_argv=sys.argv,started_utc=utc(),source_sha256=sha(source),external_individual_contact=False,credentials_supplied=False,access_control_bypass=False,routes=[])
    for row in task:
        z=dict(row,started_utc=utc(),complete_body_retrieved=False)
        try:
            req=urllib.request.Request(row['url'],headers={'User-Agent':'Mozilla/5.0 (public mathematical literature access check)','Accept':'*/*'})
            with urllib.request.urlopen(req,timeout=25) as response:
                body=response.read(8*1024*1024+1)
                if len(body)>8*1024*1024: raise ValueError('Bounded response limit exceeded; not complete')
                z.update(http_status=response.status,resolved_url=response.url,content_type=response.headers.get('Content-Type'),bytes=len(body),sha256=sha(body),pdf_magic=body.startswith(b'%PDF-'),complete_body_retrieved=True)
                filename=row['id']+'.raw';put(cache/filename,body);z['private_cache_filename']=filename
        except urllib.error.HTTPError as e:
            body=e.read(8*1024*1024+1);z.update(http_status=e.code,resolved_url=e.url,error_type=type(e).__name__,error=str(e),error_body_bytes=len(body),error_body_sha256=sha(body))
            if len(body)<=8*1024*1024:filename=row['id']+'.error.raw';put(cache/filename,body);z['private_cache_filename']=filename
        except Exception as e:z.update(error_type=type(e).__name__,error=str(e))
        z['finished_utc']=utc();out['routes'].append(z)
    out.update(finished_utc=utc(),source_unchanged=Path(__file__).read_bytes()==source)
    b=(json.dumps(out,indent=2,sort_keys=True)+'\n').encode();put(P/v.output,b)
    print(json.dumps(dict(actual_pid=os.getpid(),receipt=v.output,bytes=len(b),sha256=sha(b),routes=len(task),full_final_article_obtained_not_inferred=True)))
if __name__=='__main__':main()
