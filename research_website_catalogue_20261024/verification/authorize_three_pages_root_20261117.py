"""Create an explicit root action record; never import or execute a helper."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import hashlib,json,secrets,stat,sys

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
N=P/'verification/mink-riesz-k3-production-prepare-v2-sol-20261117'
OPS=P/'verification/mink-riesz-k3-root-execution-20261117'
AUDIT=P/'verification/mink-riesz-k3-production-static-v2-sol-20261117'
STAGE_AUDIT=P/'verification/mink-riesz-k3-stage-audit-html-fragments-sol-20261117'
STAGE_ADOPTION=P/'verification/root-mink-riesz-k3-stage-adoption-20261117.json'
pack=lambda x:(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)+'\n').encode()
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(f):
 assert f.is_file() and not f.is_symlink()
 raw=f.read_bytes()
 return {'path':str(f),'bytes':len(raw),'SHA256':sha(raw),'mode':f'{stat.S_IMODE(f.stat().st_mode):04o}'}
def snapshot(b):
 fs=[];ds=[]
 for f in sorted(b.rglob('*')):
  assert not f.is_symlink()
  if f.is_file():fs.append(dict(pin(f),path=f.relative_to(b).as_posix()))
  elif f.is_dir():ds.append({'path':f.relative_to(b).as_posix(),'mode':f'{stat.S_IMODE(f.stat().st_mode):04o}'})
  else:raise AssertionError(f)
 return {'root':str(b),'root_mode':f'{stat.S_IMODE(b.stat().st_mode):04o}','files':fs,'directories':ds,'regular_files':len(fs),'child_directories':len(ds)}

assert len(sys.argv)==2 and sys.argv[1] in {'preflight','install','verify-installed','publish'}
mode=sys.argv[1];p=json.loads((N/'PLAN.json').read_bytes())
assert pin(N/'release_three.py')['SHA256']=='83c48bca3761c9fbd49d8b29c42a113e10eebfa58b9793bad84c25644b48b3f9'
assert pin(N/'PLAN.json')['SHA256']=='a039e52df5a04d5e8a6c4dec4709bebb1858f4757efd11c09c9e35c1a67aaf24'
root_read=json.loads((P/'verification/root-mink-riesz-k3-v2-source-reading-20261117.json').read_bytes())
assert root_read['root_personally_read_complete_helper'] and root_read['helper_lines']==1279
adopted=json.loads((P/'verification/root-mink-riesz-k3-v2-helper-adoption-20261117.json').read_bytes())
assert adopted['status']=='ALL_STATIC_FINDINGS_RESOLVED_FOR_EXACT_ACTION'
assert adopted['helper_SHA256']==pin(N/'release_three.py')['SHA256']
assert adopted['PLAN_SHA256']==pin(N/'PLAN.json')['SHA256']
assert pin(AUDIT/'FINAL.json')['SHA256']==adopted['audit_FINAL_SHA256']
assert pin(STAGE_ADOPTION)['SHA256']=='4f23be687eecdd138350a880f8630e48f570281f68507aadbc8b1b9adaf34951'
b={'helper':pin(N/'release_three.py'),'PLAN':pin(N/'PLAN.json'),'controls':p['controls'],
   **{k:p[k] for k in ['record_ids','scope_paths','runtime_root','website_HEAD','website_tree','website_index','Math_native_main']},
   'stage_review_pending_during_preparation':True}
af=json.loads((AUDIT/'FINAL.json').read_bytes());sf=json.loads((STAGE_AUDIT/'FINAL.json').read_bytes())
helper_review={'audit_FINAL':pin(AUDIT/'FINAL.json'),
 **{'actual_'+k+'_present':k in af for k in ['schema','status']},
 **{'actual_'+k:af.get(k) for k in ['schema','status']},
 'root_personally_read_complete_helper_PLAN_and_audit':True,
 'root_adopts_all_findings_for_exact_current_helper_PLAN':True,
 'root_resolution':{'classification':'ALL_STATIC_FINDINGS_RESOLVED_FOR_EXACT_ACTION',
 'rationale':'Root read all1279 saved V2 lines, complete PLAN and actual independent V2 audit. Every opaque stdout is retained before return-code and caller validation; only relocation and PLAN pin otherwise change. Fixed stage and all native/public inputs remain exact.',
 'helper':b['helper'],'PLAN':b['PLAN']}}
stage_review={'root_adoption':pin(STAGE_ADOPTION),'root_adoption_semantics':json.loads(STAGE_ADOPTION.read_bytes()),
 'audit_FINAL':pin(STAGE_AUDIT/'FINAL.json'),'audit_manifest':pin(STAGE_AUDIT/'MANIFEST.json'),
 'audit_snapshot':snapshot(STAGE_AUDIT),
 **{'actual_'+k+'_present':k in sf for k in ['schema','status']},
 **{'actual_'+k:sf.get(k) for k in ['schema','status']},
 'root_resolution':{'classification':'ALL_ACTUAL_STAGE_FINDINGS_ACCEPTED_FOR_EXACT_STAGE',
 'rationale':'Root whole builder/article/HEAD/aggregate reading and fresh1715-file stage/audit custody support the actual third successful audit. Both earlier failed readers remain failures, with separate diagnoses; candidate unchanged.',
 'actual_criteria_summary':'Exact13A2M15paths6dirs;803files387dirs133articles134XML; whole accepted articles except8/7/7HEAD spans; all old HTML/JSON/XML prefixes and complete reversible edits; native assets, source/private/native/public guards exact; local/static only.',
 'all_criteria_accepted':True,'root_personally_read_complete_stage_and_audit':True,
 **{k:p['controls'][k] for k in ['stage_FINAL','stage_manifest','stage_builder']},
 'audit_FINAL':pin(STAGE_AUDIT/'FINAL.json'),'audit_manifest':pin(STAGE_AUDIT/'MANIFEST.json')}}
kind='readonly' if mode in {'preflight','verify-installed'} else mode
phase='installed' if mode in {'verify-installed','publish'} else 'before_install'
now=datetime.now(timezone.utc);nonce=secrets.token_hex(32)
a={'schema':p['authority_schema'],'action':{'readonly':'READONLY_EXACT15_PREFLIGHT','install':'INSTALL_EXACT15_FILESYSTEM','publish':'PUBLISH_EXACT15_GIT'}[kind],
 'phase':phase,'bindings':b,'concurrency':'ROOT_SERIALIZED_NO_OTHER_W_WRITER',
 'root_asserts_nonce_fresh':True,'root_asserts_no_other_W_writer':True,'deployment_authorized':False,
 'Sheet_authorized':False,'AA':None,'follow_up':None,'issued_UTC':now.isoformat(),
 'expires_UTC':(now+timedelta(minutes=45)).isoformat(),'nonce':nonce,'helper_review':helper_review,'stage_review':stage_review}
if kind=='readonly':a['request_fingerprint_SHA256']=sha(pack({'bindings':b,'phase':phase,'nonce':nonce}))
else:
 prior=json.loads((OPS/('PREFLIGHT.stdout.bin' if mode=='install' else 'VERIFY_INSTALLED.stdout.bin')).read_bytes())
 a['preflight_SHA256']=prior['preflight_SHA256']
if mode=='publish':
 installed=json.loads((OPS/'INSTALL.stdout.bin').read_bytes())
 a.update(installation_SUCCESS=pin(Path(installed['transaction'])/'SUCCESS.json'),author_name=p['author_name'],author_email=p['author_email'],commit_date=now.replace(microsecond=0).isoformat())
raw=pack(a);out=Path(p['authority_paths'][kind])
if out.exists():
 assert mode=='verify-installed'
 old=out.read_bytes();assert old==(OPS/'PREFLIGHT.authority.json').read_bytes()
 out.write_bytes(raw)
else:
 with out.open('xb') as f:f.write(raw)
out.chmod(0o644)
with (OPS/(mode.upper().replace('-','_')+'.authority.json')).open('xb') as f:f.write(raw)
print(json.dumps({'mode':mode,'authority':pin(out),'nonce':nonce,'expires_UTC':a['expires_UTC']}))
