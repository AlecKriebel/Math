from pathlib import Path
import datetime as dt, hashlib, json, os, shutil, subprocess, sys, tempfile, urllib.request
sys.dont_write_bytecode=True
os.environ.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
Q=Path(__file__).resolve().parent;R=Q.parent.parent;REPO=R.parent;H=R/'audits/pr0672_6700060';A=H/'reviews/prior_application_recheck01'
PY=sys.executable
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,m):
 if not v:raise RuntimeError(m)
def save(rel,obj):
 p=Q/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
inputs=json.loads((Q/'INPUT_MANIFEST.json').read_text())
def capture(p):
 require(p.is_file() and not p.is_symlink(),'Not regular '+str(p));b=p.read_bytes();rel=Path('private/inputs')/p.relative_to(R);d=Q/rel;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(b)
 existing=[v for v in inputs['files'] if v['source']==str(p)]
 if existing:require(len(existing)==1 and existing[0]['sha256']==sha(b),'Repeated input drift')
 else:inputs['files'].append(dict(source=str(p),path=str(rel),bytes=len(b),sha256=sha(b),captured_at=now(),source_mtime_ns=p.stat().st_mtime_ns))
 return b
for p in sorted(A.rglob('*')):
 if p.is_file():capture(p)
for name in ['ROOT_ORIGINAL_REPLAY.json','ROOT_PRIMARY_CUSTODY.json','ROOT_BOUNDARY_COUNTERCONTROLS.json','ROOT_FINAL_RECHECK_ACCEPTANCE.json','ROOT_PRIOR_APPLICATION_RECHECK.md','DUPLICATE_ACCOUNT_CHECK.json','DUPLICATE_AND_PRIOR_WORK_RECONCILIATION.json','private/ORIGINAL_INPUTS.json','private/complete_authenticated_account.json','private/existing_comments.json']:
 capture(H/name)
for p in sorted((H/'private/root_review_replay01').iterdir()):
 if p.is_file():capture(p)
for n in [672,734]:
 name=f'PR{n:04d}_PUBLICATION_LEADS.json'
 if not any(v['source']==str(R/name) for v in inputs['files']):capture(R/name)
save('INPUT_MANIFEST.json',inputs)
seal=json.loads((A/'SEAL.json').read_text());manifest=json.loads((A/'SEALED_MANIFEST.json').read_text());accept=json.loads((H/'ROOT_FINAL_RECHECK_ACCEPTANCE.json').read_text())
require(sha((A/'SEAL.json').read_bytes())==accept['seal_sha256']=='e2266da1306431f045c8b6ee692d6d25f917b26641c11c0d0cbf69c6ea9a6b29','Seal identity')
require(sha((A/'SEALED_MANIFEST.json').read_bytes())==seal['manifest_sha256']==accept['manifest_sha256'],'Manifest identity')
require(len(manifest['files'])==seal['payload_files']==50,'Hold payload count')
for v in manifest['files']:
 b=(A/v['path']).read_bytes();require(len(b)==v['bytes'] and sha(b)==v['sha256'],'Hold payload '+v['path'])
require(set(str(x.relative_to(A)) for x in A.rglob('*') if x.is_file())=={'SEALED_MANIFEST.json','SEAL.json'}|{x['path'] for x in manifest['files']},'Hold positive membership')
require(sha((A/'REPORT.md').read_bytes())==seal['report_sha256']==accept['report_sha256'],'Report seal')
originals=json.loads((H/'private/ORIGINAL_INPUTS.json').read_text());blobs={v['path']:v for v in json.loads((Q/'GIT_BLOB_INPUT_MANIFEST.json').read_text())['files'] if v['pr']==672 and '/attempts/' in v['path']}
require(len(blobs)==len(originals['files'])==24,'Hold original count')
for v in originals['files']:
 b=(Q/blobs[v['path']]['captured_path']).read_bytes();require(len(b)==v['bytes'] and sha(b)==v['sha256'],'Hold original identity '+v['path'])
replays=[]
with tempfile.TemporaryDirectory(prefix='hold672_replay_',dir=Q/'private') as td:
 temp=Path(td);shutil.copyfile(A/'exact_application_controls.py',temp/'exact_application_controls.py')
 for mode,flags in [('normal',[]),('optimized',['-O'])]:
  r=subprocess.run([PY,'-I','-B',*flags,str(temp/'exact_application_controls.py')],cwd=temp,capture_output=True)
  require(r.returncode==0 and not r.stderr,'Exact controls failed');require(sha(r.stdout)==accept['independent_private_replay']['byteidentical_output_sha256'],'Exact output differs')
  require(json.loads(r.stdout)['passed_checks']==358,'Exact check count');(Q/f'private/hold_controls_{mode}.json').write_bytes(r.stdout);replays.append(dict(mode=mode,passed=358,bytes=len(r.stdout),sha256=sha(r.stdout)))
account=json.loads((H/'private/complete_authenticated_account.json').read_text());receipt=json.loads((H/'DUPLICATE_ACCOUNT_CHECK.json').read_text());require(sha((H/'private/complete_authenticated_account.json').read_bytes())==receipt['sha256'],'Account capture custody')
require(len(account['records'])==len({v['id'] for v in account['records']})==account['total']==197,'Captured account count');require(any(v['id']==23174283 for v in account['records']),'Account positive control')
terms=['6700060','AMR-066-0060','2608.06320','mean convex','mean-convex','dihedral','convex polytope'];leads=[]
for v in account['records']:
 metadata=json.dumps(v.get('metadata',{}),ensure_ascii=False).casefold()
 if any(t.casefold() in metadata for t in terms):leads.append(dict(id=v['id'],metadata=v.get('metadata',{})))
require(leads==[],'Captured account target lead requires review');save('private/hold_account_independent_search.json',dict(terms=terms,leads=leads,records=197,fresh_authenticated_fetch_performed=False))
# Fresh exact primary-source downloads, used only for stated-theorem/category custody.
sources=[]
for name,url,prior in [('gromov2017.pdf','https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/101-problemsOct1-2017.pdf','gromov2017.pdf'),('bi2608.06320v1.pdf','https://arxiv.org/pdf/2608.06320v1','bi2608.06320v1.pdf'),('gromov2013.pdf','https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/Plateauhedra_modified_apr23.pdf','gromov2013.pdf')]:
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent-scope-custody-review/1.0'}),timeout=45) as r:
  b=r.read();http=dict(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),at=now())
 require(b==(A/'private'/prior).read_bytes(),'Fresh source bytes differ '+name);dest=Q/'private/fresh_primary'/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
 text=subprocess.run(['pdftotext','-layout',str(dest),'-'],capture_output=True,check=True).stdout;dest.with_suffix('.txt').write_bytes(text)
 sources.append(dict(name=name,url=url,bytes=len(b),sha256=sha(b),matches_sealed_prior_bytes=True,http=http,scope='Original question / exact stated prior theorem / ambient smooth convention only; not a fresh full analytic proof audit.'))
save('fresh_primary_source_receipts.json',sources)
save('hold_custody_checks.json',dict(at=now(),pr=672,head=originals['head'],seal_sha256=accept['seal_sha256'],manifest_sha256=seal['manifest_sha256'],report_sha256=seal['report_sha256'],sealed_payloads_verified=50,exact_originals_verified=24,exact_controls=replays,root_release_replay_custody_verified=True,account_captured_records=197,account_fresh_authenticated_fetch=False,account_target_leads=0,conditional_stated_Bi_theorem=True,ambient_smooth_category=True,broader_corner_singular_category_certified=False,fresh_full_analytic_PDE_certification=False,new_discovery_mechanism=False))
log=json.loads((Q/'RESEARCH_LOG.json').read_text());log.append(dict(at=now(),completion_estimate_percent=85,event='70 scopes and status bindings complete; public downloads/183 payloads/72 originals verified; 672 fifty-file seal,24 originals,358 controls both modes,three fresh primary byte identities pass;734 current explicit withdrawal bound.'));save('RESEARCH_LOG.json',log)
print(json.dumps(dict(status='PASS',sealed_payloads=50,originals=24,exact_controls_per_mode=358,fresh_primary_sources=len(sources),captured_account=197,input_captures=len(inputs['files']))))
