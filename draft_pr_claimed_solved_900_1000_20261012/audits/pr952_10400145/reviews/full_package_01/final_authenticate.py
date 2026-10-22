from pathlib import Path
import subprocess,json,datetime,hashlib,zipfile,stat
O=Path(__file__).resolve().parent;A=O.parents[1];P=A.parents[2];D=A/'preprint';now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def need(ok,label):
 if not ok:raise RuntimeError(label)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
cmd=['python3','-I','-S','-B',str(P/'draft_pr_claimed_solved_900_1000_20261012/accept_pr952.py'),'--operations-sha256','91d3af8e23beb49921713e41276a34e83d1d436e29503448a73e5950dde9c740','--freeze','84206451d82d4c93a7f0a8968558a7331d4a949331a5c99ba7c6cbab5db97107','--preflight-only','--observation-dir',str(O)]
start=now();r=subprocess.run(cmd,cwd=P,capture_output=True)
for suffix,b in [('stdout.json',r.stdout),('stderr.txt',r.stderr)]:(O/('PREFLIGHT_END02.'+suffix)).write_bytes(b)
(O/'PREFLIGHT_END02.launch.json').write_text(json.dumps({'started_utc':start,'completed_utc':now(),'argv':cmd,'returncode':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()},indent=2)+'\n')
need(r.returncode==0,'actual END02 source preflight failed: inspect private raw evidence')
need(pin(D/'FREEZE.json')['sha256']=='84206451d82d4c93a7f0a8968558a7331d4a949331a5c99ba7c6cbab5db97107','freeze');f=json.loads((D/'FREEZE.json').read_bytes());i=A/'publication/workflow/OPERATIONS_INVENTORY.json';need(pin(i)['sha256']=='91d3af8e23beb49921713e41276a34e83d1d436e29503448a73e5950dde9c740','inventory')
for n,v in json.loads(i.read_bytes())['files'].items():need(pin(P/n)==v,n)
for n,v in f['files'].items():need(pin(D/n)==v,n)
for n,v in f['evidence_files'].items():need(pin(P/n)==v,n)
records=json.loads((A/'ORIGINAL_FILE_RECORDS.json').read_bytes())['files'];orig={}
with zipfile.ZipFile(D/'habiro-rank-interpolation-verification-v1.0.zip') as z:
 for n,v in records.items():
  g=subprocess.run(['git','show','989a532ae1d50894190d010a0a02ba8c3d71ee05:'+n],cwd=P,capture_output=True,check=True).stdout;disk=(A/'original'/n).read_bytes();item=z.getinfo('original/'+n);b=z.read(item);need(g==disk==b,n);need(len(g)==v['bytes'] and hashlib.sha256(g).hexdigest()==v['sha256'],n);mode=format((item.external_attr>>16)&0o177777,'o');need(mode=='100644',n);tree=subprocess.run(['git','ls-tree','989a532ae1d50894190d010a0a02ba8c3d71ee05','--',n],cwd=P,capture_output=True,check=True).stdout.decode().split();need(tree[0]==v['git_mode'] and tree[2]==v['git_blob'],n);need(stat.S_IMODE((A/'original'/n).stat().st_mode)==0o644,n);orig[n]={**v,'archive_mode':mode,'disk_and_archive_match':True}
auth={'status':'PASS','utc':now(),'original_pr_head':'989a532ae1d50894190d010a0a02ba8c3d71ee05','freeze_sha256':'84206451d82d4c93a7f0a8968558a7331d4a949331a5c99ba7c6cbab5db97107','package_manifest_sha256':f['package_manifest_sha256'],'future_helpers':f['future_helpers'],'candidate_files':f['files'],'originals':orig,'actual_source_preflight_returncode':0,'evidence_pins_rechecked':37,'operations_rechecked':7,'earlier_END01_failure_retained':True}
(O/'AUTHENTICATION_END.json').write_text(json.dumps(auth,indent=2)+'\n')
observed=json.loads(r.stdout);summary={'utc':now(),'status':'PASS_ACTUAL_START_END02','START_raw_stdout_sha256':pin(O/'PREFLIGHT_START.stdout.json')['sha256'],'END02_raw_stdout_sha256':pin(O/'PREFLIGHT_END02.stdout.json')['sha256'],'END01_returncode':1,'END01_reason':'immutable actual-main fd1a54dad037057c498f5803e65c35c006f585be missing locally; read-only gate did not fetch; root cached exact object before a fresh run','END02_parent':observed['gate']['parent'],'END02_source':observed['gate']['source'],'END02_native':observed['gate']['native'],'service_mutations':0,'Git_network_fetch_performed_by_reviewer':False,'raw_PR_bodies_excluded_from_public_allowlist':True}
(O/'ACTUAL_PREFLIGHT_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({'status':'PASS','utc':auth['utc'],'actual_main':observed['gate']['parent'],'candidate_files':213,'evidence_pins':37,'operation_sources':7,'original_Git_disk_ZIP':33}))
