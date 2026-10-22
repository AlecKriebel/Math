"""Fresh complete mechanical/live end boundary, no fetch or service mutation."""
from pathlib import Path
import json,hashlib,subprocess,datetime,sys,stat,zipfile
R=Path(__file__).resolve().parent;A=R.parents[1];P=A.parents[1];D=A/'preprint';ROOT=P.parent
CORE='14ac4e7009a1f4973f81aed776d5c6afd344dea93ff369dd65175427e0492eec';IP='9650f0baf87ac6d83a5a7eb934d212cc66ea67dea4c8758813bec47f5a24cc05';FP='ab027971f0245481783e2afa106292543c41f06a93c3c83a0cf8dcea4cff9d77';label=sys.argv[1]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def need(c,m):
 if not c:raise RuntimeError(m)
def fingerprint(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
start=now();f=json.loads((D/'FREEZE.json').read_bytes());iv=json.loads((A/'publication/workflow/OPERATIONS_INVENTORY.json').read_bytes());need(fingerprint((P/'accept_pr952.py').read_bytes())['sha256']==CORE,'core pin');need(fingerprint((D/'FREEZE.json').read_bytes())['sha256']==FP,'freeze pin');need(fingerprint((A/'publication/workflow/OPERATIONS_INVENTORY.json').read_bytes())['sha256']==IP,'inventory pin')
maps={}
for group,record,base in [('candidate_files',f['files'],D),('evidence_files',f['evidence_files'],ROOT),('operations_dependencies',iv['files'],ROOT)]:
 observed={}
 for name,pin in record.items():q=base/name;actual=fingerprint(q.read_bytes());need(actual==pin,'boundary '+group+' '+name);observed[name]=actual
 maps[group]=observed
originals={};wanted=json.loads((A/'ORIGINAL_FILE_RECORDS.json').read_bytes())['files'];z=zipfile.ZipFile(D/'habiro-rank-interpolation-verification-v1.0.zip')
for name,pin in wanted.items():
 b=(A/'original'/name).read_bytes();g=subprocess.run(['git','show',f['original_pr_head']+':'+name],cwd=ROOT,capture_output=True);tree=subprocess.run(['git','ls-tree',f['original_pr_head'],'--',name],cwd=ROOT,capture_output=True);need(fingerprint(b)=={k:pin[k] for k in ('bytes','sha256')} and g.returncode==0 and g.stdout==b,'original disk/Git');need(format(stat.S_IMODE((A/'original'/name).stat().st_mode),'04o')==pin['disk_mode'],'original disk mode');need(tree.stdout.decode().split()[:3]==[pin['git_mode'],'blob',pin['git_blob']],'original Git mode/blob')
 zi=z.getinfo('original/'+name);need(z.read(zi)==b and zi.external_attr>>16==0o100644,'original ZIP mode/bytes');originals[name]={**pin,'archive_mode':'100644','disk_and_archive_match':True}
prior_base=A/'reviews/full_package_03';prior_raw=(prior_base/'MANIFEST.json').read_bytes();need(fingerprint(prior_raw)['sha256']=='40357e8317174e69e326ba59503927ba435cae56ead9300faeb89ad76565e912','extra-frozen prior03 external manifest');prior_doc=json.loads(prior_raw);prior_members={}
for name,pin in prior_doc['files'].items():
 actual=fingerprint((prior_base/name).read_bytes());need(actual==pin,'extra-frozen prior03 member');prior_members[name]=actual
maps['additional_prior_full03']={'manifest_sha256':fingerprint(prior_raw)['sha256'],'files':prior_members}
primary_actual=fingerprint((A/'private_primary/O.pdf').read_bytes());need(primary_actual['sha256']=='33d9c18c9ab8403a4d88b978b366451383edd12dd24760a77b9e25b666d9a8fd','neutral primary O unchanged');maps['neutral_primary_O']=primary_actual
obs=R/('observations_'+label);obs.mkdir();cmd=[sys.executable,'-I','-S','-B',str(P/'accept_pr952.py'),'--operations-sha256',IP,'--freeze',FP,'--preflight-only','--observation-dir',str(obs)];t0=now()
p=subprocess.run(cmd,cwd=ROOT,capture_output=True);t1=now();(R/'private'/('PREFLIGHT_'+label+'.stdout.raw')).write_bytes(p.stdout);(R/'private'/('PREFLIGHT_'+label+'.stderr.raw')).write_bytes(p.stderr)
launch={'mechanical_start':start,'preflight_start':t0,'preflight_end':t1,'argv':cmd,'returncode':p.returncode,'all213_877_7_and_original33_mechanical_pass':True,'private_raw_stdout_pin':fingerprint(p.stdout),'private_raw_stderr_pin':fingerprint(p.stderr),'raw_output_preserved_private':True};(R/('BOUNDARY_'+label+'.launch.json')).write_text(json.dumps(launch,indent=2)+'\n')
if p.returncode:print('BOUNDARY_FAILED',label,p.returncode);sys.exit(p.returncode)
pre=json.loads(p.stdout);gate=pre['gate'];need(pre['status']=='PASS_READONLY_PREFLIGHT','actual live preflight');auth={'status':'PASS','utc':pre['utc'],'original_pr_head':f['original_pr_head'],'freeze_sha256':FP,'package_manifest_sha256':f['package_manifest_sha256'],'future_helpers':f['future_helpers'],**maps,'originals':originals,'live_gates':gate,'observed_mechanical_start_utc':start,'preflight_raw_launch':'BOUNDARY_'+label+'.launch.json','boundary_label':label,'private_raw_output_retained':True}
(R/('AUTHENTICATION_'+label+'.json')).write_text(json.dumps(auth,indent=2)+'\n');(R/'AUTHENTICATION_END.json').write_text(json.dumps(auth,indent=2)+'\n');(R/('ACTUAL_'+label+'_SUMMARY.json')).write_text(json.dumps({'utc':pre['utc'],'status':pre['status'],'main':gate['parent'],'source':gate['source'],'native':gate['native'],'original_head':pre['original_pr_head'],'changed_paths':gate['paths']['count'],'pr':{k:gate['pr'][k] for k in ('state','isDraft','headRefOid','baseRefName','currentBaseRefOid')},'stable_authority':gate['bracket']['authority_equal'],'service_mutations':pre['service_mutations'],'Git_network_fetch_performed':pre['Git_network_fetch_performed']},indent=2)+'\n');print('BOUNDARY_PASS',label,pre['utc'],gate['parent'])
