"""Independent package/inventory/AST/source-pin checks; stdlib only."""
from pathlib import Path,PurePosixPath
import ast,hashlib,json,zipfile,io,re,subprocess,sys,copy
from datetime import datetime,timezone
R=Path(__file__).resolve().parent
P=R.parent.parent/'publication'
fail=[]
def req(x,label):
 if not x:fail.append(label)
def sha(b):return hashlib.sha256(b).hexdigest()
m=json.loads((P/'PACKAGE_MANIFEST.json').read_text());records=m['files']; names=[x['path'] for x in records]
req(len(names)==len(set(names)),'duplicate inventory')
for x in records:
 q=P/x['path'];b=q.read_bytes();req(len(b)==x['bytes'] and sha(b)==x['sha256'],'inventory mismatch '+x['path'])
actual={q.relative_to(P).as_posix() for q in P.rglob('*') if q.is_file()}
excluded_local_build_artifacts=sorted(actual-(set(names)|{'PACKAGE_MANIFEST.json','zenodo-deposit.json','local_deformation_devissage_source_verification_v1.zip'}))
req(not (set(names)-actual),'manifested local file absent')
z=P/'local_deformation_devissage_source_verification_v1.zip';prefix='local_deformation_devissage_v1/'
req(sha(z.read_bytes())=='f41f904512ab3019da10069a6017fb45b6cb82fff7b49ab49ac4f8ea00dc95dc','ZIP input differs')
with zipfile.ZipFile(z) as f:
 zinfo=f.infolist();req(f.testzip() is None,'CRC error');zn=[x.filename for x in zinfo]
 req(len(zn)==len(set(zn)),'duplicate archive entry')
 req(set(zn)=={prefix+x for x in names+['PACKAGE_MANIFEST.json']},'ZIP inventory difference')
 for x in zinfo:
  rel=x.filename[len(prefix):];req(not PurePosixPath(x.filename).is_absolute() and '..' not in PurePosixPath(x.filename).parts,'unsafe archive path')
  req(f.read(x)==(P/rel).read_bytes(),'archive bytes mismatch '+rel)
  req(x.date_time==(2026,10,12,0,0,0) and x.create_system==3 and x.external_attr==0o100644<<16 and x.compress_type==zipfile.ZIP_DEFLATED,'archive deterministic metadata '+rel)
 req(zn==sorted(zn),'archive sort')
 buf=io.BytesIO()
 with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as out:
  for rel in sorted(names+['PACKAGE_MANIFEST.json']):
   info=zipfile.ZipInfo(prefix+rel,date_time=(2026,10,12,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED
   out.writestr(info,(P/rel).read_bytes())
 req(buf.getvalue()==z.read_bytes(),'archive recipe replay not exact')
pins=json.loads((P/'evidence/SUBMITTED_PINS.json').read_text());req(len(pins['files'])==27,'pin count');gitmatched=0;gitunavailable=[]
for x in pins['files']:
 b=(P/'evidence/submitted'/x['relative']).read_bytes();req(sha(b)==x['sha256'] and len(b)==x['size'],'submitted pin mismatch '+x['relative'])
 q=subprocess.run(['git','show',pins['head_commit']+':'+x['repository_path']],capture_output=True)
 if q.returncode==0:req(q.stdout==b,'git exact input mismatch '+x['relative']);gitmatched+=1
 else:gitunavailable.append(x['relative'])
for a,b in [('checks/check_corrected_case.py','evidence/submitted/check_corrected_case.py'),('checks/current/check_conjugacy.py','evidence/submitted/current/check_conjugacy.py'),('checks/current/verify_exact.py','evidence/submitted/current/verify_exact.py'),('expected/FINITE_CONTRACT.json','evidence/submitted/FINITE_CONTRACT.json')]:req((P/a).read_bytes()==(P/b).read_bytes(),'submitted portable source changed '+a)
old=ast.parse((P/'evidence/functor_review_01/verify_functor_identities.py').read_text());new=ast.parse((P/'checks/verify_functor_identities_explicit_guards.py').read_text());g=json.loads((P/'evidence/GUARD_ADAPTATION.json').read_text())
a=[x for x in ast.walk(old) if isinstance(x,ast.Assert)];b=[x for x in ast.walk(new) if isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name) and x.value.func.id=='require']
req(len(a)==len(b)==len(g['guards'])==11,'guard count')
for o,n,r in zip(a,b,g['guards']):req(ast.dump(o.test)==ast.dump(n.value.args[0])==r['test_ast'] and o.lineno==r['original_line'],'predicate correspondence line '+str(o.lineno))
class Restore(ast.NodeTransformer):
 def visit_FunctionDef(self,n):return None if n.name=='require' else self.generic_visit(n)
 def visit_Expr(self,n):
  if isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='require':return ast.Assert(test=n.value.args[0],msg=None)
  return self.generic_visit(n)
req(ast.dump(old)==ast.dump(Restore().visit(copy.deepcopy(new))),'entire arithmetic AST changed outside assertion conversion')
req(not any(isinstance(x,ast.Assert) for x in ast.walk(new)),'assert in guard adaptation')
req(sha((P/'evidence/functor_review_01/verify_functor_identities.py').read_bytes())==g['original_sha256'],'original guard pin');req(sha((P/'checks/verify_functor_identities_explicit_guards.py').read_bytes())==g['adapted_sha256'],'adapted guard pin')
meta=json.loads((P/'metadata.json').read_text());deposit=json.loads((P/'zenodo-deposit.json').read_text());req(meta==deposit['metadata'],'deposit metadata differs')
links=[]
for name in ['README.md','SUPPLEMENT.md','evidence/INDEX.md']:
 q=P/name
 for link in re.findall(r'\]\(([^\s)]+)\)',q.read_text()):
  if '://' not in link:
   req((q.parent/link.split('#')[0]).exists(),'broken local navigation '+name+' '+link);links.append({'source':name,'target':link})
receipt={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS' if not fail else 'FAIL','failures':fail,'inventory_count':len(names),'archive_entries':len(zinfo),'archive_sha256':sha(z.read_bytes()),'deterministic_recipe_byte_identical':not any('recipe' in x for x in fail),'original_pin_count':27,'git_object_exact_matches':gitmatched,'git_object_unavailable':gitunavailable,'guard_predicates':len(a),'entire_arithmetic_AST_restored_exactly':not any('AST' in x for x in fail),'local_navigation_links':links,'excluded_local_build_artifacts':excluded_local_build_artifacts,'metadata_exact':meta==deposit['metadata'],'archive_excludes_raw_third_party_sources':not any('/sources/' in x or '/raw/' in x for x in zn)}
(R/'receipts/INTEGRITY.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k!='local_navigation_links'},indent=2))
if fail:sys.exit(1)
