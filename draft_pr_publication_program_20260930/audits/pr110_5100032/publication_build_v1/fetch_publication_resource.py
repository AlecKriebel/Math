#!/usr/bin/env python3
"""One actual read-only HTTP GET per invocation, with a distinct raw response body."""
from pathlib import Path
from datetime import datetime, timezone
import argparse,hashlib,http.client,importlib.util,json,os,sys,urllib.parse,urllib.request
A=Path(__file__).resolve().parents[1];D=A/'published_record_fullbody_verification_20261006'
TOOL=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
EXPECTED='26f264df93b657137b343acc05ae87a3e8e60d46cbbb8b822bc327d77b89c277'
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def now():return datetime.now(timezone.utc).isoformat()
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def safeurl(url):
    u=urllib.parse.urlsplit(url);require(u.scheme=='https' and u.hostname=='zenodo.org' and not u.username and u.port in (None,443),'Unexpected transport origin');return u
class Redirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,url):
        safeurl(url);return super().redirect_request(req,fp,code,msg,headers,url)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('kind',choices=('deposition','metadata','file'));parser.add_argument('record_id',type=int)
    parser.add_argument('--name');parser.add_argument('--url');parser.add_argument('--bytes',type=int);args=parser.parse_args()
    require(args.record_id>0,'Positive actual record id');require(hashlib.sha256(TOOL.read_bytes()).hexdigest()==EXPECTED,'Bound repository upload tool changed')
    spec=importlib.util.spec_from_file_location('zenodo_bound_token_loader',TOOL);z=importlib.util.module_from_spec(spec);spec.loader.exec_module(z)
    D.mkdir(exist_ok=True);started=now();token=None
    if args.kind in ('deposition','metadata'):
        name='actual_deposition_get.json' if args.kind=='deposition' else 'actual_record_get.json'
        endpoint='/api/deposit/depositions/' if args.kind=='deposition' else '/api/records/'
        url='https://zenodo.org'+endpoint+str(args.record_id);token=z.token_for('production')
        u=safeurl(url);conn=http.client.HTTPSConnection(u.hostname,timeout=60)
        try:
            conn.request('GET',u.path,headers={'Authorization':'Bearer '+token,'Accept':'application/json','User-Agent':z.USER_AGENT})
            response=conn.getresponse();status=response.status;body=response.read(1048577);finalurl=url
        finally:conn.close()
        require(status==200 and len(body)<=1048576,'Metadata HTTP status or response bound failed')
        require(token.encode() not in body,'Secret echoed by server; refusing to retain or emit')
        value=json.loads(body);require(value.get('id')==args.record_id and (value.get('submitted') is True or value.get('is_published') is True),'Actual published record identity/state')
        require((value.get('doi') or value.get('metadata',{}).get('doi'))=='10.5281/zenodo.'+str(args.record_id),'Actual DOI identity')
    else:
        require(args.name in ('focal_antipedal_sum.pdf','focal_antipedal_sum_support.zip'),'Expected artifact name')
        require(args.bytes is not None and 0<args.bytes<1048576 and args.url,'Expected bounded download')
        name=args.name;url=args.url;safeurl(url)
        opener=urllib.request.build_opener(Redirect());request=urllib.request.Request(url,headers={'User-Agent':z.USER_AGENT})
        with opener.open(request,timeout=60) as response:
            status=response.status;body=response.read(args.bytes+1);finalurl=response.url
        require(status==200 and len(body)==args.bytes,'File HTTP status or response size failed')
        require(body==(A/'publication_ready_v1'/name).read_bytes(),'Full remote artifact differs from reviewed candidate')
    require(not (D/name).exists(),'Unique retained transport body');(D/name).write_bytes(body)
    envsha=hashlib.sha256(json.dumps(dict(os.environ),sort_keys=True,separators=(',',':')).encode()).hexdigest()
    receipt={'schema':'pr110-actual-http-get/v1','actual_process_PID':os.getpid(),'argv':[sys.executable]+sys.argv,'cwd':str(Path.cwd()),
      'environment_sha256':envsha,'UTC_start':started,'UTC_end':now(),'method':'GET','request_url':url,'final_url':finalurl,
      'HTTP_status':status,'record_id':args.record_id,'authentication_sent':args.kind in ('deposition','metadata'),
      'transport_body':{'path':name,**pin(body)},'stdout_interpretation':'exact raw HTTP JSON body' if args.kind in ('deposition','metadata') else 'JSON transport byte-count/SHA256 summary; artifact body stored separately'}
    (D/(name+'.HTTP_RECEIPT.json')).write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    if args.kind in ('deposition','metadata'):sys.stdout.buffer.write(body)
    else:print(json.dumps({'response_bytes':len(body),'response_sha256':hashlib.sha256(body).hexdigest()}))
if __name__=='__main__':main()
