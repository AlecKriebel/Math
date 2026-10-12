#!/usr/bin/env python3
"""Read-only full-body Zenodo publication authentication after actual publication."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, importlib.util, json, os, sys, urllib.request, urllib.parse, zipfile

A=Path(__file__).resolve().parents[1]; D=A/'publication_ready_v1'
TOOL=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
TOOL_SHA='26f264df93b657137b343acc05ae87a3e8e60d46cbbb8b822bc327d77b89c277'
def require(ok,msg):
    if not ok: raise RuntimeError(msg)
def now():return datetime.now(timezone.utc).isoformat()
def pin(p):
    b=p.read_bytes();return {'path':p.name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,url):
        u=urllib.parse.urlsplit(url)
        require(u.scheme=='https' and u.hostname=='zenodo.org' and not u.username and u.port in (None,443),'Unsafe public download redirect')
        return super().redirect_request(req,fp,code,msg,headers,url)
def main():
    started=now(); rid=int(sys.argv[1]); require(rid>0,'Positive actual record id')
    require(pin(TOOL)['sha256']==TOOL_SHA,'Bound repository upload tool changed')
    spec=importlib.util.spec_from_file_location('math_zenodo_readonly',TOOL);z=importlib.util.module_from_spec(spec);spec.loader.exec_module(z)
    md,local=z.load_manifest(D/'zenodo-deposit.json')
    statepath,state=z.local_state((D/'zenodo-deposit.json').resolve(),'production')
    require(state and state['id']==rid,'Actual saved draft differs')
    out=A/'published_record_fullbody_verification_20261006';require(not out.exists(),'Unique full-body read-back output');out.mkdir()
    client=z.ZenodoClient('production',z.token_for('production'))
    st=now(); record=client.get(rid);z.validate_record(record,rid)
    require(record['submitted'] is True,'Remote record not published')
    normalizations=z.verify(record,md,local)
    doi=record.get('doi') or record.get('metadata',{}).get('doi');require(doi=='10.5281/zenodo.'+str(rid),'Assigned actual record DOI mismatch')
    write(out/'actual_deposition_get.json',record)
    remote=z.server_files(record);receipts=[]
    opener=urllib.request.build_opener(SafeRedirect())
    for entry in local:
        item=remote[entry['name']];url=item.get('links',{}).get('download') or item.get('links',{}).get('self')
        u=urllib.parse.urlsplit(url or '')
        require(u.scheme=='https' and u.hostname=='zenodo.org' and not u.username and u.port in (None,443),'Unsafe/absent returned download URL')
        start=now();request=urllib.request.Request(url,headers={'User-Agent':z.USER_AGENT,'Accept':'application/octet-stream'})
        with opener.open(request,timeout=60) as response:
            status=response.status;body=response.read(entry['size']+1);final_url=response.url
        require(status==200 and len(body)==entry['size'],'Returned complete download size/status')
        require(body==entry['path'].read_bytes(),'Remote full-body file differs')
        (out/entry['name']).write_bytes(body)
        receipts.append({'UTC_start':start,'UTC_end':now(),'method':'GET','request_url':url,'final_url':final_url,
          'HTTP_status':status,'file':pin(out/entry['name']),'local_file':pin(entry['path']),'full_bytes_equal':True,
          'md5':hashlib.md5(body).hexdigest(),'authentication_sent':False})
    zp=out/'focal_antipedal_sum_support.zip';members=[]
    with zipfile.ZipFile(zp) as archive:
        require(archive.testzip() is None,'Downloaded archive CRC')
        expected={p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file() and p.name!='focal_antipedal_sum_support.zip'}
        require(set(archive.namelist())==expected and len(archive.namelist())==len(expected),'Exact remote archive member scope')
        for name in archive.namelist():
            require(archive.read(name)==(D/name).read_bytes(),'Downloaded full archive member differs')
            members.append({'path':name,'bytes':len(archive.read(name)),'sha256':hashlib.sha256(archive.read(name)).hexdigest()})
    result={'schema':'pr110-actual-zenodo-fullbody-readback/v1','actual_root_PID':os.getpid(),'UTC_start':started,'UTC_end':now(),
      'environment':'production','record_id':rid,'submitted':True,'DOI':doi,'record_url':'https://zenodo.org/records/'+str(rid),
      'tool':pin(TOOL),'deposition_get':{'UTC_start':st,'output':pin(out/'actual_deposition_get.json'),'method':'GET'},
      'metadata_exact_or_narrow_kit_normalizations':True,'metadata_normalizations':normalizations,'downloads':receipts,
      'full_archive_members_checked':len(members),'archive_members':members,'no_mutating_service_request':True,
      'local_package_unchanged':True,'tracking_pending':True,'native_integration_pending':True}
    write(out/'RESULT.json',result);print(json.dumps({k:v for k,v in result.items() if k!='archive_members'},indent=2))
if __name__=='__main__':main()
