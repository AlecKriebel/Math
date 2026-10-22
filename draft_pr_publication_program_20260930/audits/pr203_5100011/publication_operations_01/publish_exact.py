"""Guarded use of the repository Zenodo kit; each mutation is a separate command."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys,urllib.request,urllib.parse,os
if sys.flags.optimize:raise RuntimeError('Publication operations require ordinary Python; optimization removes assertions')
A=Path(__file__).resolve().parent.parent;D=A/'private_operations/zenodo';KIT=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def durable_json(path,value):
 with path.open('x') as out:
  json.dump(value,out,indent=2);out.write('\n');out.flush();os.fsync(out.fileno())
 fd=os.open(path.parent,os.O_RDONLY)
 try:os.fsync(fd)
 finally:os.close(fd)
def facts():
 gp=A/'ROOT_PUBLICATION_GATE_01.json';g=json.loads(gp.read_bytes());assert gp.stat().st_mode&0o777==0o444 and g['publication_ready_gate_accepted'] and g['whole_package_review_loop_complete'] and not g['historical_priority_established']
 assert len(g['whole_package_review_events'])>=2 and g['whole_package_review_events'][-1]['verdict']=='CLEANPASS' and g['whole_package_review_events'][-1]['reviewed_package_seal']==g['package_seal']
 for rel,x in g['package_safe_files'].items():assert pin(A/g['package']/rel)==x,rel
 rp=A/'ROOT_ACTUAL_READY_CHECKPOINT.json';r=json.loads(rp.read_bytes())
 assert r['PR']==203 and r['phase']=='ready' and rp.stat().st_mode&0o777==0o444
 ap=A/r['directory']/'ACCEPTANCE.json';ac=json.loads(ap.read_bytes())
 assert pin(ap)==r['acceptance_pin'] and ac['accepted'] and ac['every_selected_identity_checked_at_actual_observed_MAIN'] and ac['case_percent']==90 and ac['publication_ready'] and ac['checkpoint_commit']==r['checkpoint_commit']
 assert hashlib.sha256(KIT.read_bytes()).hexdigest()=='a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca'
 return gp,g,A/g['package']/'zenodo-deposit.json'
def invoke(mode):
 gp,g,manifest=facts();D.mkdir(parents=True,exist_ok=True);cmd=[sys.executable,'-E','-S','-B','-P',str(KIT)]
 if mode=='inspect-doi':cmd+=['inspect',str(manifest),'--check-doi']
 else:cmd+=[mode,str(manifest)]
 if mode=='publish':
  staged=json.loads((D/'stage.json').read_bytes());assert staged['state']=='ready_to_publish';cmd+=['--confirm-id',str(staged['id'])]
 elif mode not in ['stage','inspect','inspect-doi']:raise RuntimeError('unsupported mode')
 target=D/(mode+'.json')
 if target.exists() and mode in ['inspect','inspect-doi']:
  target=D/(mode+'-'+str(len(list(D.glob(mode+'*.json')))+1).zfill(2)+'.json')
 assert not target.exists(),'Existing outcome: inspect it rather than repeat a mutation'
 if mode in ['stage','publish']:
  marker=D/(mode.upper()+'_INFLIGHT.json')
  if marker.exists():raise RuntimeError('Mutation already attempted; inspect and reconcile read-only, never repeat an unconfirmed mutation')
  durable_json(marker,{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':mode,'manifest_pin':pin(manifest),'gate_pin':pin(gp),'intended_upload_files':g['intended_upload_files'],'mutation_not_yet_launched':True,'semantics':'Written and fsynced before child launch; existence prohibits any second mutation attempt even if later response or state receipt is absent. Reconcile read-only.'})
 p=subprocess.run(cmd,capture_output=True,text=True);target.with_suffix('.stdout.txt').write_text(p.stdout);target.with_suffix('.stderr.txt').write_text(p.stderr)
 if p.returncode:raise RuntimeError('Kit '+mode+' not confirmed; read saved output and reconcile before any retry')
 j=json.loads(p.stdout);assert j['title']==g['metadata']['title'] and j.get('metadata_normalizations',[])==[]
 durable_json(target,j);print(json.dumps(j))
def finalize():
 gp,g,manifest=facts();latest=max(D.glob('inspect-doi*.json'),key=lambda p:p.stat().st_mtime_ns);j=json.loads(latest.read_bytes());assert j['state']=='published' and j['doi']=='10.5281/zenodo.'+str(j['id']) and j['doi_resolution']['http_status']==200 and j['doi_resolution']['status']=='resolved' and not j['metadata_normalizations']
 assert {x['name']:{'bytes':x['size'],'sha256':x['sha256']} for x in j['files']}==g['intended_upload_files']
 checked=[]
 for x in j['files']:
  u='https://zenodo.org/api/records/'+str(j['id'])+'/files/'+urllib.parse.quote(x['name'])+'/content';req=urllib.request.Request(u,headers={'User-Agent':'Math-Zenodo-Public-File-Verification/1.0'})
  with urllib.request.urlopen(req,timeout=45) as response:
   assert response.status==200;z=response.read(x['size']+1)
  assert len(z)==x['size'] and hashlib.sha256(z).hexdigest()==x['sha256'];checked.append(x['name'])
 r={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':203,'actual_publication_verified':True,'metadata_exact_verified':True,'metadata_normalizations':[],'all_three_public_download_SHA256_verified':True,'verified_public_download_names':checked,'id':j['id'],'state':j['state'],'doi':j['doi'],'doi_url':j['doi_url'],'record_url':j['record_url'],'doi_resolution':j['doi_resolution'],'files':j['files'],'gate_sha256':pin(gp)['sha256'],'publication_gate':gp.name,'package':g['package'],'private_kit_receipts':'private_operations/zenodo/','historical_firstness_independence_established':False}
 f=A/'ROOT_PUBLICATION_RECEIPT.json'
 with f.open('x') as out:json.dump(r,out,indent=2);out.write('\n')
 f.chmod(0o444);print(json.dumps(r))
if __name__=='__main__':
 if sys.argv[1]=='finalize':finalize()
 else:invoke(sys.argv[1])
