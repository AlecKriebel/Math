from pathlib import Path
import json,hashlib,subprocess,datetime,os
A=Path(__file__).resolve().parent;C=A.parents[2];D=A/'original_complete_custody_v2_20261006';D.mkdir(exist_ok=False);records=[]
head='3d159f0a00d0bd7ff8d558d6fbc75af5094f7a35';prefix='unsolved_math_prioritization/attempts/5100032/'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def need(x,m):
 if not x:raise RuntimeError(m)
def dump(p,x):p.write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def git(*args):
 start=now();p=subprocess.Popen(['/opt/homebrew/bin/git',*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate(timeout=30);i=len(records)
 for k,b in [('stdout',out),('stderr',err)]:(D/(str(i)+'.'+k+'.prefix.bin')).write_bytes(b[:4096])
 records.append({'argv':['/opt/homebrew/bin/git',*args],'actual_PID':p.pid,'UTC_start':start,'UTC_end':now(),'exit_code':p.returncode,'reaped':True,'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),'stderr_sha256':hashlib.sha256(err).hexdigest(),'stdout_prefix':str(i)+'.stdout.prefix.bin','stderr_prefix':str(i)+'.stderr.prefix.bin'})
 dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'records':records})
 need(p.returncode==0,'Git read failed');return out
meta=json.loads((A/'actual_operations/original_PR_metadata/stdout.bin').read_bytes());paths=sorted(x['path'] for x in meta['files'] if x['path'].startswith(prefix))
need(sorted(git('ls-tree','-r','--name-only',head,'--',prefix).decode().splitlines())==paths,'Complete incoming inventory')
need(git('symbolic-ref','--short','HEAD').strip()==b'main' and git('rev-parse','HEAD').strip()==b'735a11defdf906d1552912815810ff72779874a7' and not git('diff','--cached','--name-only','-z'),'Own main/index')
manifest=json.loads((A/'original_head_authentication_20261006/ORIGINAL_BLOB_MANIFEST.json').read_bytes())
for row in manifest['files']:
 body=git('show',head+':'+row['source_path']);saved=A/'original_head_authentication_20261006/original_attempt'/row['relative_path'];need(saved.read_bytes()==body,'Original copy changed');need(hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==row['git_blob_oid'],'Git SHA1 body');need(hashlib.sha256(body).hexdigest()==row['sha256'] and len(body)==row['bytes'],'Body pin')
O=A/'original_head_authentication_20261006/original_attempt';checksum_rows=[]
for l in (O/'SHA256SUMS').read_text().splitlines():
 expected,name=l.split(None,1);actual=hashlib.sha256((O/name.strip()).read_bytes()).hexdigest();checksum_rows.append({'name':name.strip(),'expected':expected,'actual':actual,'match':expected==actual})
bad=[r for r in checksum_rows if not r['match']];need(len(checksum_rows)==8 and len(bad)==1 and bad[0]['name']=='README.md','Unexpected checksum issue')
fix=A/'repaired_diagnostics_v1';fix.mkdir(exist_ok=False);fixed=''.join(r['actual']+'  '+r['name']+'\n' for r in checksum_rows);(fix/'SHA256SUMS').write_text(fixed)
dump(A/'ROOT_ORIGINAL_STALE_README_CHECKSUM_FINDING_20261006.json',{'UTC':now(),'actual_operator_PID':os.getpid(),'finding':'The original SHA256SUMS README pin is stale; seven other original entries match. No mathematical file or diagnostic changes.','bad_rows':bad,'original_SHA256SUMS_preserved_byte_exact':True,'effective_repair':str((fix/'SHA256SUMS').relative_to(C)),'effective_repair_sha256':hashlib.sha256(fixed.encode()).hexdigest(),'global_native_and_publication_propagation_pending':True,'mathematical_failure':False})
need((O/'PROOF.md').read_bytes()==(O/'independent_review/author_replay/PROOF.md').read_bytes(),'Original duplicated proof')
for n in ['verify.py','verification.json']:need((O/n).read_bytes()==(O/'independent_review/author_replay'/n).read_bytes(),'Original author replay pair')
sourcepair=json.loads((A/'original_head_authentication_20261006/SOURCEPAIR_AUTHENTICATION.json').read_bytes());need(sourcepair['submitted_source_equals_raw_and_SQL'] and sourcepair['submitted_prior_equals_raw_and_SQL'] and sourcepair['catalog_review_hash_verified'],'Full sourcepair')
root=Path('/Users/alec/Documents/Math/unsolved_math_prioritization');policy_pins=[]
for rel in ['README.md','review_v2/related_target_groups.json']:
 p=root/rel;b=p.read_bytes();dest=D/('READ_'+rel.replace('/','_'));dest.write_bytes(b);policy_pins.append({'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
 if rel.endswith('README.md'):print(b.decode())
 else:print('RELATED_TARGET_GROUPS_NUMERIC_OR_CODE_MATCH',('5100032' in b.decode() or 'AMR-050-0032' in b.decode()))
author=A/'reproduced_original_diagnostics_20261006/author/verification.json';ind=A/'reproduced_original_diagnostics_20261006/legacy_independent/independent_results.json'
need(author.read_bytes()==(O/'verification.json').read_bytes(),'Author normal receipt reproduction')
need(ind.read_bytes()==(O/'independent_review/independent_results.json').read_bytes(),'Independent normal receipt reproduction')
r={'schema':'pr110-root-complete-original-body-and-normal-diagnostic-custody/v2','UTC':now(),'actual_operator_PID':os.getpid(),'source_head':head,'native_inventory_count':len(paths),'complete_inventory_authenticated':True,'all_17_Git_blob_SHA1_and_SHA256_pins_verified':True,'submitted_checksum_members':8,'valid_submitted_checksum_members':7,'stale_README_checksum_repaired_in_separate_effective_artifact':True,'original_files_unchanged':True,'policy_read_pins':policy_pins,'raw_source_and_nonempty_prior_SQL_dataset_pair_verified':True,'review_hash':sourcepair['catalog_selected']['review_hash'],'statement_hash':sourcepair['catalog_selected']['statement_hash'],'revision':sourcepair['dataset_revision'],'author_normal_actual_PID':98919,'author_assertions':17364,'legacy_independent_normal_actual_PID':98918,'legacy_independent_assertions':1993,'both_normal_regenerated_receipts_byte_exact':True,'historical_checkers_use_asserts_and_not_claimed_effective_under_optimization':True,'original_effort':'2/5','new_central_proof_search_turns':0,'mathematical_clearance':False,'priority_clearance':False,'fresh_mathematical_review_families_active':3}
dump(D/'ROOT_AUTHENTICATION.json',r);print(json.dumps(r))

