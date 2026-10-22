from pathlib import Path
import hashlib,json,subprocess,datetime,ast,re
O=Path(__file__).resolve().parent;A=O.parent;P=A/'publication_package_v1';C=P/'verification';PY='/opt/homebrew/opt/python@3.14/bin/python3.14'
def require(ok,m):
 if not ok:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def run(label,argv):
 t=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(argv,cwd=O,capture_output=True);f=O/(label+'.stdout');g=O/(label+'.stderr');f.write_bytes(r.stdout);g.write_bytes(r.stderr);x={'UTC':t,'argv':argv,'cwd':str(O),'exit':r.returncode,'stdout':{'path':f.name,'bytes':len(r.stdout),'sha256':sha(r.stdout)},'stderr':{'path':g.name,'bytes':len(r.stderr),'sha256':sha(r.stderr)}};(O/(label+'.receipt.json')).write_text(json.dumps(x,indent=2));return x
runs=[]
for name in ['independent_exact.py','independent_face_word.py','independent_double_pentagon.py']:
 for opt in [False,True]:
  rr=run(name[:-3]+('_optimized' if opt else '_normal'),[PY,'-E','-S','-B','-P']+(['-O'] if opt else [])+[str(C/'independent'/name)]);require(rr['exit']==0,name);runs.append(rr)
for opt in [False,True]:
 rr=run('fresh_attack'+('_optimized' if opt else '_normal'),[PY,'-E','-S','-B','-P']+(['-O'] if opt else [])+[str(O/'independent_attack.py')]);require(rr['exit']==0,'fresh attack');runs.append(rr)
for label,old,new in [('wrong_halfturn_derivative','sub(one,p[j])==q[(1-j)%5]','add(one,p[j])==q[(1-j)%5]'),('wrong_coordinate_identity','scale(425,one)','scale(427,one)')]:
 s=(O/'independent_attack.py').read_text();require(s.count(old)==1,'mutation uniqueness');f=O/(label+'.py');f.write_text(s.replace(old,new))
 for opt in [False,True]:
  rr=run(label+('_optimized' if opt else '_normal'),[PY,'-E','-S','-B','-P']+(['-O'] if opt else [])+[str(f)]);require(rr['exit']!=0,'wrong science accepted');runs.append(rr)
# Exact original membership, including independent hashing of git blob objects.
m=json.loads((C/'provenance/ORIGINAL_FILE_MANIFEST.json').read_text());rows=[]
repo=A
while not (repo/'.git').exists() and repo!=repo.parent:repo=repo.parent
for x in m['files']:
 f=C/'historical_original'/x['path'];b=f.read_bytes();require(len(b)==x['bytes'] and sha(b)==x['sha256'],x['path']);require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\x00'+b).hexdigest()==x['git_blob'],'git blob sha1')
 r=subprocess.run(['git','-C',str(repo),'show',m['original_head']+':'+x['path']],capture_output=True);require(r.returncode==0 and r.stdout==b,'original Git object '+x['path']);rows.append({'path':x['path'],'sha256':sha(b),'git_blob':x['git_blob'],'git_show_exit':r.returncode})
# Guard replacement must preserve the exact expression AST of every original assertion.
guards=[]
for n in ['check_certificate.py','check_half_turn.py']:
 old=ast.parse((C/'historical_original/unsolved_math_prioritization/attempts/5000007'/n).read_text());new=ast.parse((C/'current'/n).read_text());a=[ast.dump(x.test) for x in ast.walk(old) if isinstance(x,ast.Assert)];b=[ast.dump(x.test.operand) for x in ast.walk(new) if isinstance(x,ast.If) and isinstance(x.test,ast.UnaryOp) and isinstance(x.test.op,ast.Not) and len(x.body)==1 and isinstance(x.body[0],ast.Raise)];require(a==b,'scientific guard AST '+n);guards.append({'file':n,'identical_original_assertion_tests':len(a)})
# Conservative privacy scan, content categories and actual hits retained (paths are provenance).
rx=re.compile(r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{24,}|Bearer [A-Za-z0-9._-]{20,}|(?:password|access_token|refresh_token)\s*[:=]\s*["\x27][^"\x27]{8,}',re.I);hits=[]
for f in C.rglob('*'):
 if f.is_file() and f.suffix.lower()!='.pdf':
  s=f.read_text(errors='replace')
  if rx.search(s):hits.append(f.relative_to(C).as_posix())
require(not hits,'possible secret requires inspection')
require(not any(f.suffix.lower() in ['.zip','.png'] for f in C.rglob('*') if f.is_file()),'unexpected media/archive in verification');require([f.relative_to(C).as_posix() for f in C.rglob('*.pdf')]==['manuscript/dodecahedron_endpoint.pdf'],'external pdf')
# Compile output page image equality checks do not assume byte-identical PDF timestamps.
runs.append(run('rebuilt_render',['/opt/homebrew/bin/pdftoppm','-scale-to','1300','-png',str(O/'dodecahedron_endpoint.pdf'),str(O/'rebuilt')]))
images=[]
for i in range(1,5):
 f=O/f'paper-{i}.png';g=O/f'rebuilt-{i}.png';images.append({'page':i,'packet_sha256':sha(f.read_bytes()),'rebuilt_sha256':sha(g.read_bytes()),'identical':f.read_bytes()==g.read_bytes()})
(O/'EXTRA_CHECK_RESULTS.json').write_text(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':runs,'original_git_blob_authentication':rows,'guard_expression_identity':guards,'privacy_secret_pattern_hits':hits,'external_primary_bodies_present':False,'packet_rebuilt_page_render_comparison':images,'secondary_script_O_limit':'independent_face_word and independent_double_pentagon retain assert guards; ordinary runs and the fresh explicit-guard attack supply verification. -O success alone is not counted as verification of those two scripts.'},indent=2));print({'runs':len(runs),'original_git_blobs':len(rows),'guard_tests':guards,'privacy':'PASS','rebuilt_images_identical':[x['identical'] for x in images]})
