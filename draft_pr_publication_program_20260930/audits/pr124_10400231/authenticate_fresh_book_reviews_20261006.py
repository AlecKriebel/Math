"""Authenticate new independent book reviews and replay exact algebra without changing seals."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;C=A.parents[2]
D=A/'root_book_review_authentication_20261006';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14';GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(v,s):
 if not v:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def dump(p,v):p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(A)),'bytes':len(b),'sha256':sha(b)}
require(not D.exists(),'Actual authentication already exists')
D.mkdir();events=[]
F=A/'turaev_book_obstruction_adversary_20261006';G=A/'book_realization_priority_adversary_20261006'
fseal=load(F/'SEAL.json');require(fseal['sealed'] and fseal['payload_cardinality']==9,'Book seal')
fresh=[]
for name,digest in fseal['payload_sha256'].items():
 p=F/name;require(sha(p.read_bytes())==digest,'Book member changed '+name);fresh.append(pin(p))
require(sha((F/'PUBLIC_SHA256SUMS').read_bytes())==fseal['PUBLIC_SHA256SUMS_sha256'],'Book manifest changed')
fresh.extend([pin(F/'SEAL.json'),pin(F/'PUBLIC_SHA256SUMS')])
gman=load(G/'PUBLIC_MANIFEST.json')
for x in gman['files']:
 p=G/x['path'];b=p.read_bytes();require(len(b)==x['bytes'] and sha(b)==x['sha256'],'Realization member changed '+x['path']);fresh.append(pin(p))
fresh.append(pin(G/'PUBLIC_MANIFEST.json'))
require(len(fresh)==19,'Fresh member cardinality')
original=load(A/'original_head_authentication_20261006/ORIGINAL_AUTHENTICATION.json')
for x in original['original_files']:
 p=A/'original_head_authentication_20261006/original_attempt'/x['path'];b=p.read_bytes()
 require(len(b)==x['bytes'] and sha(b)==x['sha256'],'Original changed '+x['path'])
require(original['original_budget']=='2/5' and original['original_head']=='d110ad761291aa6ac1d66d2a49e8b8212c18bed6','Original scope')
require(sha((A/'MATHEMATICAL_SOURCE_GATE_20261006.json').read_bytes())=='4d820293c9c9fde1dad40c4a11fc81cb9f0a49f9b3715bdfadfb9418db160568','Math gate changed')
pages=[]
for num in [1,2,3]:
 rpath=A/'continued_public_access_20261006'/('ACTUAL_PREVIEW_PAGES_'+str(num).zfill(2)+'.json');r=load(rpath)
 for x in r['events']:
  p=Path(x.get('unmodified_local_path',x.get('private_local_path','')));b=p.read_bytes()
  require(len(b)==x['bytes'] and sha(b)==x['sha256'],'Primary pixels changed')
  page=x.get('printed_page',x.get('printed_page_requested')); valid=x.get('valid_primary_page_pixels',True)
  pages.append({'printed_page':page,'valid_primary_page':valid,'bytes':len(b),'sha256':sha(b),'actual_receipt':pin(rpath),'copyrighted_kept_private':True})
require(sum(x['valid_primary_page'] for x in pages)==10,'Usable source page count')
require([x['printed_page'] for x in pages if not x['valid_primary_page']]==[19],'Failed placeholder classification')
for x in load(F/'SOURCE_PROVENANCE.json')['inspected_primary_pages']:
 p=A/'continued_public_access_20261006/private_sources'/('turaev2002_PA'+str(x['printed_page'])+'.png')
 require(p.stat().st_size==x['bytes'] and sha(p.read_bytes())==x['sha256'],'Family1 source pin')
for x in load(G/'SOURCE_SEARCH_LEDGER.json')['source_records']:
 if 'path' in x and 'sha256_actual' in x:
  p=Path(x['path']);b=p.read_bytes();require(len(b)==x['bytes_actual'] and sha(b)==x['sha256_actual'],'Family2 source pin')
prior_immutable=[]
for name in ['integral_topology_adversary_20261006','integral_algebra_adversary_20261006','primary_scope_adversary_20261006','historical_alexander_priority_adversary_20261006','original_conjecture_priority_adversary_20261006','later_realization_priority_adversary_20261006','novel_contribution_adversary_20261006']:
 prefix=str((A/name).relative_to(C))
 child=subprocess.run([GIT,'ls-tree','-r','--name-only','5de48499b84f168099d0273a340f4976f841f691','--',prefix],cwd=C,capture_output=True)
 require(child.returncode==0,'Old tracked inventory')
 for rel in child.stdout.decode().splitlines():
  child2=subprocess.run([GIT,'show','5de48499b84f168099d0273a340f4976f841f691:'+rel],cwd=C,capture_output=True)
  require(child2.returncode==0 and child2.stdout==(C/rel).read_bytes(),'Earlier sealed member changed '+rel)
  prior_immutable.append(pin(C/rel))
src=(F/'verify_algebra.py').read_bytes();rep=D/'normal_replay';rep.mkdir();(rep/'verify_algebra.py').write_bytes(src)
env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
start=now();child=subprocess.Popen([PY,'-E','-S','-B','-P',str(rep/'verify_algebra.py')],cwd=rep,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate()
(rep/'stdout.json').write_bytes(out);(rep/'stderr.txt').write_bytes(err)
events.append({'PID':child.pid,'UTC_start':start,'UTC_end':now(),'argv':[PY,'-E','-S','-B','-P',str(rep/'verify_algebra.py')],'exit_code':child.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err),'assertions_physically_enabled':True})
require(child.returncode==0,'Exact normal algebra replay')
actual=load(rep/'ALGEBRA_CHECK.json');expected=load(F/'ALGEBRA_CHECK.json')
require({k:v for k,v in actual.items() if k!='UTC'}=={k:v for k,v in expected.items() if k!='UTC'},'Exact arithmetic result mismatch')
# Meaningful normal-mode corruption: a zero quotient must be rejected.
mut=D/'normal_zero_quotient_control';mut.mkdir();body=src.decode();needle='quotient={k:1}'
require(body.count(needle)==1,'Control source target')
(mut/'verify_algebra.py').write_text(body.replace(needle,'quotient={k:0}'))
start=now();child=subprocess.Popen([PY,'-E','-S','-B','-P',str(mut/'verify_algebra.py')],cwd=mut,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate()
(mut/'stdout.txt').write_bytes(out);(mut/'stderr.txt').write_bytes(err)
events.append({'PID':child.pid,'UTC_start':start,'UTC_end':now(),'argv':[PY,'-E','-S','-B','-P',str(mut/'verify_algebra.py')],'exit_code':child.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err),'assertions_physically_enabled':True,'expected_corruption_rejected':True})
require(child.returncode!=0 and b'AssertionError' in err,'False quotient was not rejected')
for x in fresh:
 p=A/x['path'];b=p.read_bytes();require(len(b)==x['bytes'] and sha(b)==x['sha256'],'New seal mutated by replay')
fr,gr=load(F/'RESULT.json'),load(G/'RESULT.json')
require(fr['source_bridge_complete'] and fr['old_theorem_direct_corollary_all_primes'] and fr['original_general_rank_obstruction_old_theorem_direct_corollary'],'Family1 source coverage')
require(gr['exact_old_source_family_refutation_verified'] and gr['general_original_necessary_condition_old_source_covered'] and not gr['new_mathematically_substantive_contribution_established'],'Family2 source coverage')
r={'schema':'pr124-root-fresh-book-review-authentication/v1','UTC':now(),'actual_operator_PID':os.getpid(),'fresh_public_member_count':len(fresh),'fresh_members':fresh,'original17_unchanged':True,'earlier_tracked_sealed_members_unchanged_count':len(prior_immutable),'earlier_members':prior_immutable,'usable_primary_pages_count':10,'source_pages':pages,'actual_child_events':events,'normal_algebra_replay_matches':True,'false_zero_quotient_rejected':True,'optimized_assertion_checks_not_claimed':True,'mathematical_validity_retained':True,'old_published_full_family_and_general_obstruction_verified':True,'express_historical_refutation_not_established':True,'substantive_novel_resolution_not_established':True,'fresh_disposition_review_pending':True,'new_central_proof_search_turns':0,'native_shared_PR_Zenodo_Sheet_mutations':False}
dump(A/'ROOT_FRESH_BOOK_REVIEW_AUTHENTICATION_20261006.json',r)
print(json.dumps({k:v for k,v in r.items() if k not in ['fresh_members','earlier_members','source_pages','actual_child_events']}))

