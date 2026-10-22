"""Read, classify and validate every member, source pin and original Git blob."""
import ast,hashlib,json,os,stat,subprocess
from pathlib import Path
R=Path(__file__).absolute().parent;A=R.parent.parent;repo=A.parents[2];P=R/'tmp/packet'
sha=lambda b:hashlib.sha256(b).hexdigest()
source=(P/'verify_package.py').read_bytes();n={'__file__':str(P/'verify_package.py'),'__name__':'trusted_content_inspection'};exec(compile(source,str(P/'verify_package.py'),'exec'),n)
report=n['verify'](P);rows=[]
for name in sorted(n['inventory'](P)):
 b=(P/name).read_bytes();row={'path':name,'bytes':len(b),'sha256':sha(b),'mode':oct(stat.S_IMODE((P/name).stat().st_mode))}
 if name.endswith('.pdf'):
  if name!='satoh_filtration_counterexamples.pdf' or not b.startswith(b'%PDF-'):raise RuntimeError(name)
  row['type']='authored_pdf'
 else:
  text=b.decode('utf-8');row['type']='utf8_text';row['lines']=len(text.splitlines())
  if name.endswith('.json'):
   x=n['json_data'](b);row['type']='strict_json';row['top_level_keys']=sorted(x)if isinstance(x,dict)else None
  if name.endswith('.py'):
   tree=ast.parse(text,filename=name);compile(text,name,'exec');row['type']='python_source'
   row['imports']=sorted({a.name for t in ast.walk(tree)if isinstance(t,ast.Import)for a in t.names}|{t.module for t in ast.walk(tree)if isinstance(t,ast.ImportFrom)and t.module})
   row['functions']=[t.name for t in ast.walk(tree)if isinstance(t,(ast.FunctionDef,ast.AsyncFunctionDef))]
 rows.append(row)
snapshot=json.loads((A/'SCOPE_AND_SNAPSHOT.json').read_bytes());env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
out=subprocess.check_output(['git','ls-tree','-r','-z',snapshot['original_head'],'--','unsolved_math_prioritization/attempts/30003703/'],cwd=repo,env=env)
actual={}
for entry in out.split(b'\0'):
 if not entry:continue
 details,name=entry.split(b'\t',1);mode,kind,oid=details.decode().split();actual[name.decode()]={'git_mode':mode,'git_blob':oid}
expected={name:{k:r[k]for k in('git_mode','git_blob')}for name,r in snapshot['original_blobs'].items()}
if actual!=expected:raise RuntimeError('original head Git tree differs')
for name,record in snapshot['original_blobs'].items():
 b=subprocess.check_output(['git','show',snapshot['original_head']+':'+name],cwd=repo,env=env)
 if b!=(A/'native'/name).read_bytes():raise RuntimeError('original blob bytes '+name)
summary={'schema':'pr681-round2-complete-content-inspection-v1','status':'PASS','members':len(rows),'strict_JSON_members':sum(x['type']=='strict_json'for x in rows),'python_sources':sum(x['type']=='python_source'for x in rows),'authored_PDFs':sum(x['type']=='authored_pdf'for x in rows),'root_and_family_pins':len(n['PINS']),'native_original_Git_blob_bytes_modes_verified':23,'raw_third_party_fulltexts_included':False,'all_member_bytes_read':True,'files':rows}
(R/'CONTENT_INSPECTION.json').write_text(json.dumps(summary,indent=2)+'\n')
bindings=[]
for rel,expected in [('tmp/primary/owr2018.pdf','91efb3f45550efd99cbae32c72001ea6b8d40fd0a9c1301c2f524398f9530de5'),('tmp/primary/satoh2017.pdf','b8d9d96f13bced6e70bde207e0f78b4edda0442f2f36cb36bb5dd4d14b132e64'),('reviews/classical_priority_01/tmp/burde_arxiv_v2.pdf','e5ff0279d05ec03c830f48110cd90906fd9402ba0578203de9625175076f769e'),('reviews/whole_package_round1/operations_controls.py','e3ca9d587a02216edd089044fd17cc2469cfef1f7f5891fa68fa34ae40bede73'),('reviews/whole_package_round1/VERDICT.json','4ad090e428a90fd531258bd8b5212d457fe880247feedd3f167097b80d9372c7')]:
 p=A/rel;b=p.read_bytes()
 if sha(b)!=expected:raise RuntimeError('source binding '+rel)
 bindings.append({'path':str(p),'bytes':len(b),'sha256':sha(b)})
(R/'SOURCE_BINDINGS.json').write_text(json.dumps({'schema':'pr681-round2-source-bindings-v1','sources':bindings,'raw_third_party_sources_copied_or_redistributed':False,'primary_inspection':'Complete OWR printed88-89 as cached full-page images/text; relevant Satoh2017v2 kernel definitions/Theorem6.3 and Burde2015v2 Eq4/Theorem4.14 in cached primary text; no final journal substitution; no new current-openness search certificate.'},indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items()if k!='files'}))
