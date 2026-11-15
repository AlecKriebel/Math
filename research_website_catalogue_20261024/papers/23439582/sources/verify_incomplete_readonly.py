"""Pure offline custody of an incomplete acquisition, never a readiness verifier."""
from pathlib import Path
import hashlib,json,sys,zipfile
S=Path(__file__).resolve().parent
TERMINAL={'ACQUISITION_INCOMPLETE_MANIFEST.json','ACQUISITION_INCOMPLETE_CLOSURE.json','ACQUISITION_INCOMPLETE_SEAL.json'}
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def j(p):return json.loads(Path(p).read_text())
def main():
 count=0
 def ck(ok,msg):
  nonlocal count
  count+=1
  if not ok:raise ValueError(msg)
 m=j(S/'ACQUISITION_INCOMPLETE_MANIFEST.json')
 actual={str(p.relative_to(S)) for p in S.rglob('*') if p.is_file() and str(p.relative_to(S)) not in TERMINAL}
 ck(actual=={e['path'] for e in m['files']},'exact incomplete owned file set')
 for e in m['files']:
  p=S/e['path'];ck(p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(S),'regular confined file');ck(p.stat().st_size==e['bytes'] and h(p)==e['SHA256'],'whole-byte incomplete custody')
 ck(not (S/'SOURCE_READY.json').exists(),'never call failed acquisition SOURCE_READY')
 status=j(S/'ACQUISITION_STATUS.json')
 ck(status['status']=='INCOMPLETE_NATIVE_RECORD_HTTP403_NETWORK_TRAFFIC_RESTRICTION' and status['authenticated_native_record_obtained'] is False and status['source_ready'] is False,'literal incomplete status')
 receipts=sorted((S/'attempts').rglob('*.receipt.json'));ck(len(receipts)==3,'all three ordinary attempts retained')
 for p in receipts:
  r=j(p);body=Path(r['body_path']).read_bytes()
  ck(r['HTTP_status']==403 and r['request_URL']=='https://zenodo.org/api/records/23439582' and r['request_method']=='GET','exact original attempted transport')
  ck(isinstance(r['response_headers_in_order'],list) and hashlib.sha256(body).hexdigest()==r['SHA256'] and len(body)==r['bytes']==763,'whole error body/ordered headers')
  ck(b'unusual traffic from your network' in body,'actual network restriction evidence')
 c=j(S/'CACHE_CANDIDATE.json');p=Path(c['candidate_path'])
 ck(p.stat().st_size==c['bytes'] and h(p)==c['SHA256'],'actual historical candidate byte identity')
 ck(c['native_Zenodo_file_identity_not_yet_authenticated'] is True and c['not_copied_or_extracted'] is True,'cache not silently promoted to native source')
 with zipfile.ZipFile(p) as z:
  infos=z.infolist();ck(len(infos)==len(c['whole_central_directory'])==20,'whole candidate central-directory count')
  for f,e in zip(infos,c['whole_central_directory']):ck(f.filename==e['name'] and f.file_size==e['bytes'] and f.CRC==int(e['CRC32'],16) and f.compress_size==e['compressed_bytes'] and list(f.date_time)==e['date_time'] and f.external_attr==e['external_attr'] and f.flag_bits==e['flags'] and f.compress_type==e['compression'],'literal candidate directory order/metadata')
 sealed=False
 if (S/'ACQUISITION_INCOMPLETE_SEAL.json').exists():
  seal=j(S/'ACQUISITION_INCOMPLETE_SEAL.json')
  for name,key in [('ACQUISITION_INCOMPLETE_MANIFEST.json','MANIFEST_SHA256'),('ACQUISITION_INCOMPLETE_REPORT.md','REPORT_SHA256'),('ACQUISITION_STATUS.json','STATUS_SHA256'),('ACQUISITION_INCOMPLETE_CLOSURE.json','CLOSURE_SHA256')]:ck(h(S/name)==seal[key],'incomplete terminal seal '+name)
  sealed=True
 print(json.dumps({'status':'PASS_INCOMPLETE_CUSTODY_ONLY','source_ready':False,'read_only':True,'network_program_execution_or_writes':False,'checks':count,'owned_files':len(m['files']),'failed_native_transports':3,'final_incomplete_seal_checked':sealed},indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:print(json.dumps({'status':'FAIL','error':str(e)}));sys.exit(1)
