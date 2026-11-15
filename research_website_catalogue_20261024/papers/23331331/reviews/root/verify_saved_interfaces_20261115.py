"""Root offline whole-byte/type/order/namespace comparison; no science replay or writes."""
from pathlib import Path, PurePosixPath
import hashlib, json, os, stat
R=Path(__file__).resolve().parent
P=R.parent.parent
N=0
T=0
def need(x,label):
 global N
 N+=1
 if not x:raise RuntimeError(label)
def read(p):
 p=Path(p);need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary real input')
 return p.read_bytes()
def obj(p):return json.loads(read(p))
def sha(b):return hashlib.sha256(b).hexdigest()
def typed(a,b):
 global T
 T+=1
 need(type(a) is type(b),'exact scalar/container type')
 if isinstance(a,dict):
  need(list(a)==list(b),'whole key order')
  for k in a:typed(a[k],b[k])
 elif isinstance(a,list):
  need(len(a)==len(b),'whole list order/length')
  for x,y in zip(a,b):typed(x,y)
 else:need(a==b,'whole scalar value')
def extent(root):
 need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary real root')
 files=[];dirs=[]
 def walk(d):
  with os.scandir(d) as entries:
   for x in entries:
    q=Path(x.path);m=x.stat(follow_symlinks=False).st_mode;n=q.relative_to(root).as_posix()
    if stat.S_ISDIR(m):dirs.append(n);walk(q)
    else:need(stat.S_ISREG(m),'reject links and special entries');files.append(n)
 walk(root);return sorted(files),sorted(dirs)
def pin(p,d):
 b=read(p);need(len(b)==d['bytes'] and sha(b)==d['SHA256'],'complete byte identity');return b
def safe(n):
 q=PurePosixPath(n);need(q.parts and str(q)==n and not q.is_absolute() and '..' not in q.parts and '\\' not in n,'canonical relative input');return q
def main():
 contract=obj(R/'ROOT_NATIVE_CUSTODY_CONTRACT_20261115.json')
 for row in contract['namespaces']:
  root=Path(row['root']);files,dirs=extent(root)
  need(files==[x['path'] for x in row['files']] and dirs==row['directories'],'whole exact files AND directories, no future carveouts')
  for x in row['files']:pin(root/safe(x['path']),x)
 S=P/'sources';A=P/'reviews/adversarial';C=P/'reviews/scope'
 readyb=read(S/'SOURCE_READY.json');ready=json.loads(readyb)
 need(sha(readyb)=='28a9736d92beaadb1faa37c9146d56191be83fb217116f24b33162bea922e469','actual immutable READY')
 need(sha(read(S/'SOURCE_READY_SEAL.json'))=='c523e830e06555037254c26d9d85c82f4324c841cdd268f99d95664bf02e2150','actual immutable source seal')
 source_manifest=obj(S/'SOURCE_READY_MANIFEST.json')
 need(len(source_manifest['files'])==84 and len(contract['namespaces'][0]['files'])==87,'all84 plus3 exact source terminals')
 scope=obj(C/'VERDICT.json');adv=obj(A/'CUSTOM_VERDICT.json')
 typed(scope['whole_original_source_READY'],ready);typed(adv['whole_original_SOURCE_READY'],ready)
 protocol=obj(C/'SOURCE_PROTOCOL_BINDINGS.json');typed(protocol['SOURCE_READY_whole_literal'],ready)
 child=obj(C/'custody/WHOLE_LITERAL_NATIVE.json');typed(protocol,child)
 m=obj(C/'custody/INPUT_MANIFEST.json');need(len(m['files'])==87,'all87 source originals/raw copies')
 json_count=0
 for x in m['files']:
  original=Path(x['original']);copy=C/'custody'/x['copy'];a=read(original);b=read(copy)
  need(a==b,'every whole source/raw buffer equal')
  if original.suffix=='.json':typed(json.loads(a),json.loads(b));json_count+=1
 for d,value in zip(ready['whole_native_API_objects'],protocol['native_API_whole_literal']):typed(obj(d['path']),value)
 ap=obj(A/'NATIVE_PROTOCOL_IDENTITY.json')
 for x in ap['whole_API_objects']:typed(obj(x['original_binding']['path']),x['actual_parsed_whole_object'])
 need(ready['version']=='1.0' and ready['publication_date']=='2026-10-13' and ready['selected_actual_PDF']['pages']==5,'exact native edition')
 need(ready['printed_version'] is None and ready['printed_title_date_version_inspected'] is False,'historical source unread flags remain unchanged')
 typed(scope['printed_version'],'1.0');typed(adv['printed_version'],'1.0')
 baseline=P/'sources/published-source/asset-001/outer-pedal-centroid-verification/reproduction/REPRODUCTION_SUMMARY.json'
 actual=obj(A/'NATIVE_BASELINE_COMPARISON.json');typed(obj(baseline),actual['whole_original_native_baseline_object'])
 expected=next(x for x in obj(baseline)['replays'] if x['replay']=='AUTHOR_REPLAY')
 typed(expected,actual['selected_whole_baseline_entry'])
 need(expected['whole_output_byte_identical_to_submitted'] is False and expected['parsed_output_equal_to_submitted'] is False,'full historical negative comparison flags preserved')
 replay=obj(A/'NATIVE_REPLAY_RECEIPTS.json');buffers=[]
 for i,x in enumerate(replay['runs']):
  need(x['exit_code']==0 and x['timeout'] is False and x['assertions_enabled'] is (i==0),'ordinary-only scientific verification')
  b=pin(x['stdout_path'],{'bytes':x['stdout_bytes'],'SHA256':x['stdout_SHA256']});buffers.append(b)
  need(read(x['stderr_path'])==b'','whole empty stderr')
 need(buffers[0]==buffers[1] and len(buffers[0])==2369 and sha(buffers[0])==expected['output_sha256'],'complete actual normal/O and archived expected hash, no invented raw expected file')
 typed(json.loads(buffers[0]),actual['whole_actual_ordinary_output'])
 need(actual['archived_expected_raw_stdout_body_in_original_ZIP'] is False and actual['direct_raw_expected_body_comparison_claimed'] is False,'exact expected interface limits')
 native=P/'sources/published-source/asset-001/outer-pedal-centroid-verification/author/verify.py'
 need(sha(read(native))=='dca748ae931ba5276a16dedd00c502d474a5ac78957b30f87b4846e64c884bbb','unchanged selected native checker')
 for name in ['scope','adversarial']:
  value=obj(P/'reviews'/name/'FINAL_SEAL.json')
  need(value is not None,'actual full family terminal available')
 need(scope['substantive_mathematical_defect'] is None and adv['substantive_defect_found'] is False,'literal distinct scientific findings preserved')
 print(json.dumps({'status':'PASS_ROOT_COMPLETE_NATIVE_INTERFACES_AND_STRICT_NAMESPACES','checks':N,'typedNodes':T,'namespaces':[{'root':x['root'],'files':len(x['files']),'directories':len(x['directories'])} for x in contract['namespaces']],'wholeSourceJSONBuffersCompared':json_count,'wholeActualOutputBytes':2369,'onlyArchivedExpectedHashAvailable':True,'optimizedAssertionsNotScience':True,'sourceProgramsScientificCampaignsNetworkSubprocessOrWrites':False},sort_keys=True))
if __name__=='__main__':main()
