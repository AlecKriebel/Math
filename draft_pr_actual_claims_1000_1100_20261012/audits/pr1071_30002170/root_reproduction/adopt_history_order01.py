import sys,os,json,hashlib,subprocess,datetime,zipfile,io,tempfile,shutil,collections
from pathlib import Path
sys.dont_write_bytecode=True
A=Path(__file__).resolve().parents[1];R=A/'repairs/history_order01';P=A/'NEWpreprint_v1_0';O=A/'root_reproduction/history_order01_20261016';O.mkdir(exist_ok=True)
def need(c,s):
 if not c:raise RuntimeError(s)
def load(p):return json.loads(p.read_text())
def identity(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def match(p,r):return identity(p)=={k:r[k] for k in ['bytes','sha256']}
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
seal=load(R/'SEAL.json');need(match(R/'OUTPUT_PINS.json',seal['output_pins']),'seal binding')
for r in load(R/'OUTPUT_PINS.json')['records']:need(match(R/r['path'],r),'repair output '+r['path'])
for r in load(R/'CURRENT_CANDIDATE_PINS.json')['records']:need(match(P/r['path'],r),'candidate pin '+r['path'])
baseline=load(R/'BASELINE_INPUT_PINS.json')['records'];before={r['original_path']:r for r in load(R/'BEFORE_PINS.json')['records']}
for r in baseline:need(match(A/(before[r['path']]['before_snapshot'] if r['path'] in before else r['path']),r),'baseline exact original')
need(len(baseline)==987 and len(before)==8,'baseline count')
q=load(P/'HISTORY_ORDER_QUALIFICATION.json');old=load(A/'repairs/case_alias01/HISTORICAL_STAGE_RESOLUTION.json');new=load(A/'repairs/portability01/HISTORICAL_STAGE_RESOLUTION.json')['records'];ks=['stage','captured_path','bytes','sha256'];proj=lambda r:{k:r[k] for k in ks};encode=lambda rows:json.dumps(rows,sort_keys=True,separators=(',',':')).encode()
before_rows=list(map(proj,old['additional_terminal_rows']));after_rows=list(map(proj,new[2788:]));need(q['before_projected_rows_sha256']==hashlib.sha256(encode(before_rows)).hexdigest() and q['after_projected_rows_sha256']==hashlib.sha256(encode(after_rows)).hexdigest(),'independent projection digest')
need(sum(a!=b for a,b in zip(before_rows,after_rows))==939 and collections.Counter(map(lambda r:encode(r),before_rows))==collections.Counter(map(lambda r:encode(r),after_rows)),'order versus multiset')
src=(R/'custody.py').read_text();src=src.replace("def write(n,o):(D/n).write_text", "O=Path("+repr(str(O))+")\ndef write(n,o):(O/n).write_text").replace("D=Path(__file__).resolve().parent;A=D.parents[1];", "D=Path("+repr(str(R))+");A=Path("+repr(str(A))+");")
(O/'custody_replay.py').write_text(src)
receipts=[]
def run(argv,ok=True):
 e=os.environ.copy();e['PYTHONDONTWRITEBYTECODE']='1';p=subprocess.run(argv,cwd=O,env=e,capture_output=True,text=True);receipts.append({'argv':argv,'cwd':str(O),'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'expected_success':ok});save(O/'ACTUAL_COMMANDS.json',receipts);need((p.returncode==0)==ok,'actual command failed');return p
py='/opt/homebrew/bin/python3.14';run([py,'-B',str(O/'custody_replay.py')]);x=load(O/'CUSTODY_SUMMARY.json');y=load(R/'CUSTODY_SUMMARY.json');x.pop('utc');y.pop('utc');need(x==y,'all custody summary fields')
def closed(root):
 m=load(root/'PACKAGE_MANIFEST.json')['members'];payload={r['path']:(root/r['path']).read_bytes() for r in m};payload['PACKAGE_MANIFEST.json']=(root/'PACKAGE_MANIFEST.json').read_bytes();buf=io.BytesIO()
 with zipfile.ZipFile(buf,'w',compression=0) as z:
  for n in sorted(payload):
   i=zipfile.ZipInfo(n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;z.writestr(i,payload[n])
 return buf.getvalue()
raw=(P/'PR1071_preprint_v1_0_support.zip').read_bytes();need(closed(P)==raw and len(load(P/'PACKAGE_MANIFEST.json')['members'])==198,'independent closed199')
tmp=Path(tempfile.mkdtemp(prefix='root1071-order-',dir='/private/tmp'));C=tmp/'clean';C.mkdir()
try:
 with zipfile.ZipFile(io.BytesIO(raw)) as z:z.extractall(C)
 for runtime in ['/opt/homebrew/bin/python3.11','/opt/homebrew/bin/python3.14']:
  for flags in [[],['-O']]:
   tag=Path(runtime).name+('-O' if flags else '-normal')
   run([runtime,'-B',*flags,str(P/'scripts/verify_package.py'),'--require-bindings'])
   run([runtime,'-B',*flags,str(C/'scripts/check.py'),'--out',str(tmp/(tag+'-math'))])
 run([py,'-B',str(C/'scripts/verify_package.py')])
 run([py,'-B',str(C/'scripts/build_archive.py'),'--out',str(tmp/'rebuilt.zip')]);need((tmp/'rebuilt.zip').read_bytes()==raw,'actual rebuild')
 # Coherent outer manifest rehash must still reject an untrue order claim.
 path=C/'HISTORY_ORDER_QUALIFICATION.json';man=C/'PACKAGE_MANIFEST.json';pb=path.read_bytes();mb=man.read_bytes();d=load(path);d['additional1558_global_order_preserved']=True;path.write_text(json.dumps(d));m=load(man)
 for r in m['members']:
  if r['path']=='HISTORY_ORDER_QUALIFICATION.json':r.update(identity(path))
 man.write_text(json.dumps(m))
 for flags in [[],['-O']]:
  p=run([py,'-B',*flags,str(C/'scripts/verify_package.py')],False);need('Global order versus multiset/per-stage qualification drift' in p.stderr,'semantic rather than stale binding failure')
 path.write_bytes(pb);man.write_bytes(mb)
 run([py,'-B',str(C/'scripts/verify_package.py')])
 run([py,'-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',str(A/'publication/zenodo-deposit.json')])
finally:
 save(O/'OWN_EXTERNAL_CLEANUP.json',{'entries':[{'path':str(p),**identity(p)} for p in sorted(tmp.rglob('*')) if p.is_file()],'scope':'Only new unsealed ROOT reproduction fixtures, exact identities before cleanup.'});shutil.rmtree(tmp)
for r in load(R/'OUTPUT_PINS.json')['records']:need(match(R/r['path'],r),'postrun repair output')
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ROOT_ADOPT_BOUNDED_HISTORY_ORDER_QUALIFICATION_REQUIRED_NEW_COMPLETE_WHOLE05','full_REPORT_current_qualification_status_notes_SUPPLEMENT_operative_verifier_diff_and_custody_source_read':True,'counts':{'repair_outputs':42,'baseline':987,'authorized_changes':8,'protected':979,'copy_pairs':153,'historical_rows':4346,'historical_locator_fields':11480,'earlier_later_pin_rows':3158,'newer_pin_rows':3637,'individual_omissions':74,'closed_archive_members':199},'complete_custody_replay':x,'actual_root_commands':receipts,'historical_global_order_claim_explicitly_false_and_superseded':True,'all_old_sealed_raw_records_preserved':True,'no_math_PDF_TeX_native_metadata_runtime_or_pathpolicy_change':True,'independent_closed_archive':identity(P/'PR1071_preprint_v1_0_support.zip'),'whole_reviews_completed':4,'minimum_whole_reviews':2,'new_complete_whole05_required':True,'root_terminal_adoption_required_after_clean_review':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,'actual_source_creation_ENOSPC_attempt_preserved_cause_deeper_than_observed_error_UNKNOWN':True,'no_Git_or_services_called':True}
save(A/'ROOT_HISTORY_ORDER_REPAIR_REVIEW_01.json',record);print(json.dumps({'status':'PASS_ROOT_ADOPTED_WHOLE05_REQUIRED','commands':len(receipts),'counts':record['counts']}))
