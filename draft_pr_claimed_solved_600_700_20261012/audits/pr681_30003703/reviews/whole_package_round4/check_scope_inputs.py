#!/usr/bin/env python3
"""Read-only source/native/real-staged evidence reconciliation; writes own report."""
from pathlib import Path
import hashlib,html,json,os,stat,subprocess,sys,zipfile,datetime
R=Path(__file__).absolute().parent;A=R.parent.parent;REPO=A.parents[2]
def need(v,l):
 if not v:raise RuntimeError(l)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
freeze=json.loads((A/'WHOLE_PACKAGE_REVIEW_INPUTS.normalization_repair.json').read_bytes())
rows={}
for key,base in [('publication_files',A/'publication'),('helper_sha256',A),('gate_bindings',A)]:
 for n,p in freeze[key].items():
  actual=pin(base/n);need(actual['sha256']==(p if isinstance(p,str)else p['sha256']),'input binding '+n)
  if isinstance(p,dict):need(actual==p,'size '+n)
  rows[str((base/n).relative_to(A))]=actual
snapshot=json.loads((A/'SCOPE_AND_SNAPSHOT.json').read_bytes());need(snapshot['original_head']==freeze['original_head']and snapshot['status']=='claimed_solved','native scope')
cells=snapshot['queue_row'].split('|');need(cells[2].strip()=='30003703 / OWR-15987-013' and cells[8].strip()=='claimed_solved'and cells[9].strip()=='1/5','historical queue')
env={k:v for k,v in os.environ.items()if not k.startswith('GIT_')};env['GIT_OPTIONAL_LOCKS']='0'
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO,env=env)
N='unsolved_math_prioritization/attempts/30003703/';ls={}
for row in git('ls-tree','-r','-z',freeze['original_head'],'--',N).split(b'\0'):
 if row:
  d,n=row.split(b'\t');mode,kind,oid=d.decode().split();ls[n.decode()]={'git_mode':mode,'kind':kind,'git_blob':oid}
need(set(ls)==set(snapshot['original_blobs'])and len(ls)==23,'native Git inventory')
for n,p in snapshot['original_blobs'].items():
 b=(A/'native'/n).read_bytes();need(len(b)==p['size']and sha(b)==p['sha256'],'native bytes')
 need(stat.S_IMODE((A/'native'/n).lstat().st_mode)==0o644,'native mode')
 need(ls[n]=={'git_mode':'100644','kind':'blob','git_blob':p['git_blob']},'native Git mode/blob')
 need(sha(git('show',freeze['original_head']+':'+n))==p['sha256'],'native original Git bytes')
with zipfile.ZipFile(A/'publication/satoh_filtration_verification.zip')as z:
 infos=z.infolist();need(len(infos)==107 and z.namelist()==sorted(z.namelist()),'archive inventory/order')
 for i in infos:need(i.date_time==(2026,10,15,0,0,0)and i.external_attr>>16==0o100644 and i.compress_type==zipfile.ZIP_DEFLATED and not i.is_dir(),'archive structural metadata')
 need(all(i.filename.endswith(('.py','.md','.json','.txt','.tex','.pdf')) or i.filename.endswith('/.gitignore')for i in infos),'no raw fulltext inventory')
 need((R/'tmp/satoh_filtration_verification.zip').read_bytes()==(A/'publication/satoh_filtration_verification.zip').read_bytes(),'deterministic rebuild bytes')
old=json.loads((A/'ZENODO_STAGED_NATIVE_READBACK.json').read_bytes());new=json.loads((A/'ZENODO_STAGED_NATIVE_READBACK.source_capture_fixed.json').read_bytes());stage=json.loads((A/'ZENODO_STAGE.stdout').read_bytes())
need({k:v for k,v in old.items()if k!='created_utc'}=={k:v for k,v in new.items()if k!='created_utc'},'fresh staged readback semantically identical')
need(new['id']==stage['id']==23387442 and new['published']is False and stage['state']=='ready_to_publish'and new['native_pids']=={},'unpublished stage only')
local=json.loads((A/'publication/zenodo-deposit.json').read_bytes())['metadata'];expected=dict(local);expected['description']=html.escape(local['description'],quote=False)
need(new['expected_local_metadata']==local and new['legacy_supplied_metadata_fields']==expected,'all eleven legacy fields')
NORM=[{'field':'description','kind':'plain_text_html_entities'}];need(stage['metadata_normalizations']==new['legacy_metadata_normalizations']==NORM,'exact observed normalization')
m=new['native_metadata'];actual={'title':m['title'],'upload_type':'publication'if m['resource_type']['id'].startswith('publication-')else None,'publication_type':m['resource_type']['id'].split('publication-',1)[1],'publication_date':m['publication_date'],'version':m['version'],'description':m['description'],'creators':[{'name':c['person_or_org']['name'],'affiliation':c['affiliations'][0]['name'],'orcid':next(i['identifier']for i in c['person_or_org']['identifiers']if i['scheme']=='orcid')}for c in m['creators']],'access_right':'open'if new['native_access']['record']==new['native_access']['files']=='public'else None,'license':m['rights'][0]['id'],'keywords':[s['subject']for s in m['subjects']],'related_identifiers':[{'identifier':x['identifier'],'scheme':x['scheme'],'relation':x['relation_type']['id']}for x in m['related_identifiers']]}
expected['related_identifiers']=[dict(i,relation=i['relation'].lower())for i in expected['related_identifiers']];need(actual==expected and len(actual)==11,'independent all eleven native fields')
downloads={}
for n,d in new['files'].items():
 b=(A/'publication'/n).read_bytes();matches=list((A/'tmp').glob('staged-*-'+n));need(matches and all(p.read_bytes()==b for p in matches),'stored actual downloads')
 need(d['sha256']==sha(b) and d['md5']==hashlib.md5(b).hexdigest()and d['bytes']==len(b)and d['HTTP_status']==200,'binary exact hashes')
 downloads[n]={'matching_download_count':len(matches),**d}
# Repaired sources and predecessor pin are independently checked, not trusted as conclusions.
previous=json.loads((A/'reviews/whole_package_round3/VERDICT.json').read_bytes());need(sha((A/'reviews/whole_package_round3/VERDICT.json').read_bytes())=='c9bfc114d5e7c122023666fa6e1cf05c009f5837605b9776ad5d5e44a3b7b5eb','predecessor verdict pin')
for n,p in previous['diagnostic_and_fresh_staged_readback_pins'].items():need(pin(A/n)==p,'diagnostic pin '+n)
need((A/'root_check_integration.py').read_bytes()==(A/'root_check_integration.py.before_turns_repair').read_bytes().replace(b"ac[9].strip()==b'5/5'",b"ac[9].strip()==b'1/5'"),'exact Turns repair')
head=git('rev-parse','HEAD').decode().strip();branch=git('symbolic-ref','-q','HEAD').decode().strip();index_path=Path(git('rev-parse','--git-path','index').decode().strip());index_path=index_path if index_path.is_absolute()else REPO/index_path
live_run=subprocess.run(['gh','pr','view','681','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName'],capture_output=True,text=True,timeout=60)
live=json.loads(live_run.stdout)if live_run.returncode==0 else{'read_error':live_run.stderr[:200]}
if live_run.returncode==0:need(live['headRefOid']==freeze['original_head']and live['state']=='OPEN'and live['isDraft']and live['baseRefName']=='main','live selected draft/head')
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','normalization_freeze_sha256':sha((A/'WHOLE_PACKAGE_REVIEW_INPUTS.normalization_repair.json').read_bytes()),'files':rows,'original23_git_bytes_modes_blobs_exact':True,'original_selected_status':'claimed_solved','original_selected_turns':'1/5','archive_members':107,'rebuild_byte_equal':True,'staged_record_id':23387442,'actual_published':False,'all11_native_metadata_fields_exact':True,'metadata_normalizations':NORM,'remote_description_sha256':sha(expected['description'].encode()),'stored_downloads':downloads,'diagnostic_pins':previous['diagnostic_and_fresh_staged_readback_pins'],'observed_shared_head':head,'observed_shared_branch':branch,'observed_index_sha256':sha(index_path.read_bytes()),'live_pr_read_only_snapshot':live,'future_fresh_live_gates_required':True,'no_external_mutations_in_this_check':True}
(R/'SCOPE_NATIVE_STAGE_CHECKS.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','head':head,'live_pr':live},indent=2))
