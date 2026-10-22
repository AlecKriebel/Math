#!/usr/bin/env python3
"""New1268-specific offline controls. All fixture mains write only scratch."""
from pathlib import Path
import copy,hashlib,json,os,subprocess,sys,tempfile,types
ROOT=Path(__file__).resolve().parent
def load(p):
 import importlib.util
 spec=importlib.util.spec_from_file_location('edition_'+p.stem+str(id(p)),p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def reject(fn,label):
 try:fn()
 except (ValueError,RuntimeError,FileNotFoundError,KeyError):return label
 raise RuntimeError('Unexpected acceptance '+label)
def worker():
 w=load(ROOT/'workflow_regression.py');v=load(ROOT/'verification_verify.py');negative=[]
 with tempfile.TemporaryDirectory(prefix='new1268-edition-',dir=ROOT/'_local') as tmp:
  base=Path(tmp);f=w.fixture(base/'main');pub=f['pub'];audit=f['audit'];meta=copy.deepcopy(f['context']['metadata']);preserve=copy.deepcopy(f['context']);preserve.update(edition_mode='preserve_submitted',edition_text={},structured_records={});save(audit/'CURRENT_PR1268_CONTEXT.json',preserve);v.load_context(audit,pub)
  bad=copy.deepcopy(preserve);bad['edition_text']={'PROOF.md':'injected'};save(audit/'CURRENT_PR1268_CONTEXT.json',bad);negative.append(reject(lambda:v.load_context(audit,pub),'preserved_mode_cannot_invent_text'));save(audit/'CURRENT_PR1268_CONTEXT.json',preserve)
  run=subprocess.run([sys.executable,'-B',str(pub/'build_package.py')],env=f['env'],capture_output=True,text=True);need(run.returncode==0,run.stderr);build=json.loads((pub/'BUILD_RECEIPT.json').read_text());anchors=build['verification_anchors'];v.verify(pub/'verification',anchors['manifest'],anchors['context'],anchors['snapshot'])
  need(all((audit/'current_edition'/name).read_bytes()==(audit/'submitted'/name).read_bytes() for name in v.NAMES),'Preserve mode changed any original bytes');need(len(v.NAMES)==10,'Wrong ten originals');manifest=json.loads((audit/'current_edition/PUBLIC_MANIFEST.json').read_text());need(len(manifest['files'])==9 and 'PUBLIC_MANIFEST.json' not in {e['path'] for e in manifest['files']},'PUBLIC_MANIFEST self/count wrong')
  u=load(pub/'update_pr_publication.py');t=load(pub/'append_tracker.py');record={'environment':'production','state':'published','metadata_normalizations':[],'id':123,'doi':'10.5281/zenodo.123','doi_url':'https://doi.org/10.5281/zenodo.123','record_url':'https://zenodo.org/records/123','title':meta['title'],'files':[{'name':build[k]['path'],'size':build[k]['bytes'],'sha256':build[k]['sha256']} for k in ['pdf','verification_zip']]};tracker={'spreadsheetId':t.SID,'gid':t.GID,'updatedRange':"'Math Puzzles'!A2:D2",'readback_verified':True,'row':t.expected_row(record,meta['title'])};save(pub/'PUBLICATION_RECEIPT.json',record);files,publication,note=u.desired_files(build,record,tracker,f['snapshot']);need(len(files)==15 and len(publication)==5,'Not10+5 intended scope');need(all(files[v.BASE+'/'+n]==(audit/'submitted'/n).read_bytes() for n in v.NAMES),'Preserved finalPR originals changed')
  save(pub/'tracker/TRACKER_RECEIPT.json',tracker);save(pub/'PUBLIC_DOWNLOAD_VERIFICATION.json',{'synthetic':True});wanted=u.expected_identity(record,tracker,files,note);head='a'*40;changes=[v.BASE+'/publication_20261017/'+n for n in publication]
  def git(*args,data=None):
   if args[0]=='rev-list':return (head+' '+u.ORIGINAL+'\n').encode()
   if args[0]=='diff-tree':return ('\n'.join(changes)+'\n').encode()
   if args[0]=='show':return files[args[1].split(':',1)[1]]
   raise RuntimeError('Forbidden native Git fixture call')
  u.git=git;u.validate_saved({**wanted,'commit':head},wanted,files)
  # A rehashed outer/edition manifest cannot hide changed preserved originals.
  root=pub/'verification';proof=root/'current_edition/PROOF.md';proof.write_bytes(proof.read_bytes()+b'\nTAMPER');m=root/'current_edition/PUBLIC_MANIFEST.json';obj=json.loads(m.read_text())
  for e in obj['files']:
   if e['path']=='PROOF.md':e.update(bytes=proof.stat().st_size,sha256=sha(proof))
  save(m,obj);outer=root/'MANIFEST.json';obj=json.loads(outer.read_text())
  for e in obj['files']:
   if e['path'] in {'current_edition/PROOF.md','current_edition/PUBLIC_MANIFEST.json'}:q=root/e['path'];e.update(bytes=q.stat().st_size,sha256=sha(q))
  save(outer,obj);negative.append(reject(lambda:v.verify(root,sha(outer),anchors['context'],anchors['snapshot']),'coupled_outer_and_PUBLIC_manifest_rewrite_cannot_change_preserved_original'))
  paths=base/'paths';paths.mkdir();(paths/'Proof.md').write_text('CASE SENSITIVE');negative.append(reject(lambda:v.member(paths,'proof.md'),'case_mismatch'));(paths/'Dir').mkdir();negative.append(reject(lambda:v.member(paths,'dir/file.md'),'parent_case_mismatch'))
  for badpath in ['/absolute','../escape','a/../b','a//b','a/./b']:
   negative.append(reject(lambda raw=badpath:v.member(paths,raw),'unsafe_'+badpath))
  for desc in ['<p>n>=3</p>','<p>n<4</p>','<script>unsafe</script>','A > B','A < B']:
   changed=copy.deepcopy(meta);changed['description']=desc;negative.append(reject(lambda:v.metadata_contract(changed),'raw_angle_'+desc))
  for desc in ['No raw comparison signs.','<p>At least three vertices.</p>','<p>n&gt;=3 and n&lt;4.</p>']:
   changed=copy.deepcopy(meta);changed['description']=desc;v.metadata_contract(changed)
  for role in ['math','priority']:
   regs=copy.deepcopy(preserve['authored_freezes'])
   for reg in regs:
    if reg['role']==role:reg['role']='documentary'
   negative.append(reject(lambda:v.authenticate_nested_manifests(audit,regs),'missing_explicit_'+role+'_role'))
 return {'status':'PASS','preserve_all10_byte_exact_with_original_PUBLIC_manifest':True,'explicit_current_mode_exercised_in_base_fixture':True,'all15_desired_files_with_only5_actual_changed_paths_accepted':True,'automatic_replays_only_explicit_programs_no_repo_auth_assumptions':True,'stable_entity_or_words_descriptions_accepted':True,'relative_membership_and_explicit_roles_required':True,'new_negative_controls':negative,'scope':'Offline1268-specific fixture guards. No mathematical or priority acceptance, actual paper or service/Git mutation.'}
def main():
 if '--worker' in sys.argv:print(json.dumps(worker(),sort_keys=True));return
 runs=[]
 for flags in [[],['-O'],['-OO']]:
  r=subprocess.run([sys.executable,'-B',*flags,str(Path(__file__).resolve()),'--worker'],capture_output=True,text=True);need(r.returncode==0,r.stderr);runs.append({'flags':flags,'result':json.loads(r.stdout)})
 need(all(x['result']==runs[0]['result'] for x in runs),'Optimization dependent1268 edition guards');result={'status':'PASS','all3_modes_identical':True,'runs':runs};save(ROOT/'_local/EDITION_AND_PATH_RECEIPT.json',result);print(json.dumps({'status':'PASS','all3_modes_identical':True},indent=2))
if __name__=='__main__':main()
