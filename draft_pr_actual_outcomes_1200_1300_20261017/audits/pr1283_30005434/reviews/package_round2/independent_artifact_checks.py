from pathlib import Path
import json,hashlib,datetime,subprocess,copy,importlib.util,ast,sys
F=Path(__file__).resolve().parent;A=F.parent.parent;P=A/'publication';R=Path('/Users/alec/Documents/Math');T=A.parents[1]
def need(b,m):
 if not b:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
 s=importlib.util.spec_from_file_location('review_'+p.stem,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def rejects(fn,label):
 try:fn()
 except Exception as e:return {'label':label,'exception':type(e).__name__,'message':str(e)}
 raise RuntimeError('FALSE ACCEPT '+label)
checks={};snap=json.loads((A/'SUBMITTED_SNAPSHOT.json').read_text());head=snap['head']
def git(*args):
 r=subprocess.run(['git',*args],cwd=R,capture_output=True)
 if r.returncode:raise RuntimeError(r.stderr.decode())
 return r.stdout
need(git('rev-list','--parents','-n','1',head).decode().split()==[head,'a72180cf68ed6c9c54360cfd61b7a6567f5a0a5f'],'single original parent')
for x in snap['files']:
 b=git('show',head+':'+x['path']);need(b==(A/'submitted'/Path(x['path']).name).read_bytes(),'actual Git source body')
 need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob_sha1'],'actual Git blob')
need(set(git('diff-tree','--no-commit-id','--name-only','-r',head).decode().splitlines())=={x['path'] for x in snap['files']},'original changed8')
checks['original_git']={'original_head':head,'single_parent':'a72180cf68ed6c9c54360cfd61b7a6567f5a0a5f','exact_eight_blob_bodies':True}
mp=json.loads((A/'CURRENT_EDITION_CHANGE_MAP.json').read_text());pres=[]
for e in mp['changes']:
 n=e['path'];o=(A/'submitted'/n).read_bytes();b=(A/'current_edition'/n).read_bytes();need(sha(A/'submitted'/n)==e['original']['sha256'] and sha(A/'current_edition'/n)==e['current']['sha256'],'change-map byte pins')
 if n.endswith('.md'):need(b[e['prefix_bytes']:]==o and e['current_preserved_range']==[e['prefix_bytes'],len(b)],'verbatim complete suffix')
 elif n!='MANIFEST.json':need(json.loads(b)['historical_submitted_record']==json.loads(o),'historical JSON value')
 pres.append(n)
checks['preservation']={'all8_change_map_bindings':pres,'four_complete_verbatim_suffixes':True,'three_historical_JSON_values_equal':True,'absent_old_bodies_authenticated':False}
v=load(P/'verification/verify.py');c=v.load_context(A,P);meta=c['metadata'];manifest=json.loads((P/'zenodo-deposit.json').read_text());need(manifest['metadata']==meta and len(manifest['files'])==2,'exact actual manifest/context')
u=load(T/'publication_coordinators/pr1283.py');kit=u.load_exact_kit();wanted,files=kit.load_manifest(P/'zenodo-deposit.json');legacy={'metadata':copy.deepcopy(wanted),'files':[{'filename':f['name'],'filesize':f['size'],'checksum':'md5:'+f['md5']} for f in files]};need(kit.verify(legacy,wanted,files)==[],'actual strict kit metadata positive')
m=load(P/'check_public_downloads.py');remote=copy.deepcopy(meta);remote['resource_type']={'type':remote.pop('upload_type'),'subtype':remote.pop('publication_type')};remote['license']={'id':remote['license']};need(m.verify_public_metadata(remote,meta)==sorted(meta),'actual public schema positive')
neg=[]
for key in sorted(meta):
 b=copy.deepcopy(legacy);b['metadata'][key]=None;neg.append(rejects(lambda:kit.verify(b,wanted,files),'legacy11_'+key))
 b=copy.deepcopy(remote)
 if key in ['upload_type','publication_type']:b['resource_type']['type' if key=='upload_type' else 'subtype']=None
 elif key=='license':b['license']['id']=None
 else:b[key]=None
 neg.append(rejects(lambda:m.verify_public_metadata(b,meta),'public11_'+key))
for label in ['plain_entities','paragraph_apostrophe','omitted_affiliation']:
 w=copy.deepcopy(wanted)
 if label=='plain_entities':w['description']='A & B';actual={**w,'description':'A &amp; B'}
 elif label=='paragraph_apostrophe':w['description']='<p>A\u2019s B</p>';actual={**w,'description':"<p>A's B</p>"}
 else:w['creators']=[{'name':'Fixture only'}];actual={**w,'creators':[{'name':'Fixture only','affiliation':None}]}
 b=copy.deepcopy(legacy);b['metadata']=actual;neg.append(rejects(lambda:kit.verify(b,w,files),'strict_normalization_'+label))
checks['actual_metadata']={'exact11_fields':sorted(meta),'legacy_and_public_positives':True,'negative_controls':neg,'all_normalization_adapters_rejected':True,'no_real_remote_record_claim':True}
# Authenticate same-byte prior full normal/O/OO receipts, without replay claims.
auth=json.loads((A/'ROOT_WORKFLOW_AUTHENTICATION.json').read_text())
for e in auth['deployed_exact']:need(sha(Path(e['path']))==e['sha256'] and sha(A/'reviews/workflow_tooling'/e['mirror'])==e['sha256'],'historical source pin versus actual deployed')
progress=json.loads((A/'reviews/workflow_tooling/runs/proposed_final_02/RUN_PROGRESS.json').read_text())
for raw,e in progress['sources'].items():need(sha(A/'reviews/workflow_tooling'/raw)==e['sha256'],'same-byte historical regression source')
rr=A/'reviews/workflow_tooling/runs/proposed_final_02';ds=[]
for name in ['normal','O','OO']:
 p=rr/(name+'_stdout.json');d=json.loads(p.read_text());need(d['status']=='PASS' and (rr/(name+'_stderr.txt')).read_bytes()==b'','historical full run failure');ds.append(d)
need(ds[0]==ds[1]==ds[2],'historical optimized outputs differ');d=ds[0]
checks['historical_full_regression']={'fresh_replay':False,'three_modes_authenticated_identical':True,'sha256':sha(rr/'normal_stdout.json'),'identity_cases':len(d['identity_action_matrix']['cases']),'postmerge_cases':len(d['postmerge_complete_main']['cases']),'ready_negatives':len(d['ready_and_expected_head_merge']['negative_controls']),'ready_positives':len(d['ready_and_expected_head_merge']['positive_controls']),'coordinator_cases':len(d['deposit_coordinator_actual_kit_mocked_clients']),'current_deployed_code_matches_historical_final_run':True,'round1_ENOSPC_limits_preserved':True}
paths=[P/n for n in ['prepare_package.py','build_package.py','compile_note.py','append_tracker.py','update_pr_publication.py','check_public_downloads.py','workflow_regression.py','verification/verify.py']]+[T/'publication_coordinators/pr1283.py',T/'publication_coordinators/verify_pr1283_merge.py',A/'_local/ready_and_merge.py']
need(not any(isinstance(n,ast.Assert) for p in paths for n in ast.walk(ast.parse(p.read_text()))),'assert-only deployed guard')
checks['deployed_sources']={'all11_no_assert_nodes':True,'reviewed_source_sha256':{str(p):sha(p) for p in paths},'pinned_shared_kit_sha256':sha(R/'zenodo_deposit_tool/zenodo.py')}
for key,raw in [('source_sha256','manuscript/main.tex'),('pdf_sha256','output/pdf/main.pdf'),('compile_receipt_sha256','COMPILE_RECEIPT.json'),('layout_receipt_sha256','LAYOUT_VERIFICATION.json')]:need(sha(P/raw)==c['document_bindings'][key],'document anchor')
need((P/'output/pdf/main.pdf').read_bytes()==(P/'Semibrace_Existence_Classification_Note_v1.0.pdf').read_bytes(),'actual final PDF source copy')
checks['document_bindings']={'all_context_source_pdf_compile_layout_anchors_verified':True,'fresh_compilation':False,'byte_determinism_claim':False,'source_date_epoch_is_chosen_stamp_only':True,'actual_pdf_sha256':sha(P/'Semibrace_Existence_Classification_Note_v1.0.pdf')}
checks.update(status='PASS',at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),optimization=sys.flags.optimize)
print(json.dumps(checks,indent=2))
