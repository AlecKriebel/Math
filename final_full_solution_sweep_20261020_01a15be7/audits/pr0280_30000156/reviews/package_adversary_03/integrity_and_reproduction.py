from pathlib import Path,PurePosixPath
import sys,hashlib,json,zipfile,stat,ast,subprocess,tempfile,shutil,os
R=Path(__file__).resolve().parent;A=R.parents[1];E=A.parents[1];P=E/'private/pr0280_package_adversary_03';Z=A/'preprint/publication'; AR=R/'archive/birational-cycle-verification'
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(v,m):
 if not v:raise RuntimeError(m)
def entries(root,items):
 for e in items:
  p=root/e['path']; b=p.read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'],'manifest '+str(p))
 return len(items)
res={}
release=json.loads((Z/'RELEASE_FILES.json').read_text());res['release_files']=entries(Z,release['files'])
snapshot=json.loads((A/'SOURCE_SNAPSHOT.json').read_text())
for e in snapshot['files']:
 b=(A/e['snapshot']).read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'],'original snapshot')
 require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob'],'original blob')
 require(b==(AR/e['snapshot']).read_bytes(),'archive original')
res['original17_identical']=len(snapshot['files'])
with zipfile.ZipFile(Z/'fixed-birational-cycle-nonlimit-verification.zip') as z:
 names=z.namelist();require(len(names)==len(set(names))==65,'members')
 for i in z.infolist():
  p=PurePosixPath(i.filename);require(not p.is_absolute() and '..' not in p.parts and not i.is_dir() and (i.external_attr>>16&0o170000)!=0o120000,'unsafe zip')
  b=z.read(i.filename);b.decode('utf-8')
 res['zip_members_safe_unique_crc_read']=len(names)
manifest=json.loads((AR/'MANIFEST.json').read_text());res['payloads']=entries(AR,manifest['files'])
require((AR/'paper/main.tex').read_bytes()==(Z/'fixed-birational-cycle-nonlimit.tex').read_bytes(),'inner outer TeX')
for p in AR.rglob('*'):
 if p.suffix=='.json':json.loads(p.read_text())
 if p.suffix=='.py':ast.parse(p.read_text())
res['all_archive_json_python_parse']=True
for name,base in [('ops_repair_20261021/MANIFEST.json',A),('publication_support/schema_integer_repair_20261021/REPAIR_OUTPUT_MANIFEST.json',A),('reviews/package_adversary_02/AUTHORED_FILE_MANIFEST.json',A/'reviews/package_adversary_02'),('publication_operations_preparation/MANIFEST.json',A/'publication_operations_preparation/prior_review_02_full')]:
 v=json.loads((A/name).read_text());res[name]={'sha256':sha((A/name).read_bytes()),'verified':entries(base,v['files'])}
# Main scientific old seal must be interpreted at its preserved snapshot.
v=json.loads((A/'preprint/prior_review_01_full/publication_support/PREPARATION_OUTPUT_MANIFEST.json').read_text());res['historical36_preparation']=entries(A/'preprint/prior_review_01_full',v['files'])
# Search human-readable public content for credential material. Pattern hits require manual interpretation.
import re
patterns=[r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',r'gh[pousr]_[A-Za-z0-9]{20,}',r'Bearer\s+[A-Za-z0-9._-]{20,}',r'ya29\.[A-Za-z0-9_-]{20,}',r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}']
res['exposure_pattern_hits']=[{'path':str(p.relative_to(AR)),'pattern':pt} for p in AR.rglob('*') if p.is_file() for pt in patterns if re.search(pt,p.read_text())]
runs=[]
for py in [sys.executable,str(E.parent/'.venv/bin/python')]:
 if not Path(py).exists():continue
 for flags in [[],['-O']]:
  run=subprocess.run([py,*flags,'-B',str(AR/'verify.py')],capture_output=True,text=True)
  require(run.returncode==0,run.stderr);runs.append({'python':py,'flags':flags,'stdout':json.loads(run.stdout),'exit':run.returncode})
res['current_verifier_replays']=runs
# Original legacy scripts print only; run normal mode, since their original assert guards are legacy.
legacy=[];py=str(E.parent/'.venv/bin/python')
for rel,expected in [('checks/verify.py','checks/output.json'),('independent_review/independent_check.py','independent_review/INDEPENDENT_CHECKS.json')]:
 run=subprocess.run([py,'-B',str(AR/'original'/rel)],capture_output=True,text=True)
 require(run.returncode==0,run.stderr);v=json.loads(run.stdout);baseline=json.loads((AR/'original'/expected).read_text())
 require(v==baseline,'legacy baseline differs');(P/('legacy_'+Path(rel).stem+'.stdout.json')).write_text(run.stdout)
 legacy.append({'script':rel,'assertions':v['assertions'],'matches_original_output_exactly':True,'exit':run.returncode})
res['legacy_replays']=legacy
res['legacy_runtime']=subprocess.check_output([py,'-c','import sys,sympy,json;print(json.dumps({"python":sys.version,"sympy":sympy.__version__}))'],text=True).strip()
(R/'INTEGRITY_REPRODUCTION.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
