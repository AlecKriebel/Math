#!/usr/bin/env python3
"""Fail-closed offline package verification, not a mathematical proof checker."""
import ast,contextlib,hashlib,io,json,os,stat,sys,tempfile
from pathlib import Path
EXPECTED = {'ACCEPTANCE.json': {'bytes': 527, 'sha256': 'e606b5410a5fd63f708a58fd57bafb16ec6978ec0076309245ea1d6f8bd16c96'}, 'INDEPENDENT_MATHEMATICAL_REVIEW.md': {'bytes': 7446, 'sha256': '26dc10fa1b8b502e8f1c8a2275c40c6ba13b7cc9c4107cc531d77a63b9069b1b'}, 'MATHEMATICAL_AUDIT.md': {'bytes': 14930, 'sha256': '5a5c99dc1ad2b6c4af563c8a43631480d1ce75bc6ce283dfa2962bcac37b132f'}, 'PDF_METADATA.json': {'bytes': 945, 'sha256': '80f608b0b81e1c22b92f9d339eae4cabf7e2f27be66cc4e5b5343429cd61da95'}, 'PUBLIC_METADATA.json': {'bytes': 665, 'sha256': '59afd5ae030379f67aae534ae73644515314a75ffe8f863eebc399ddf2c05455'}, 'PUBLIC_PROJECTION.md': {'bytes': 1361, 'sha256': '091ecb04ee653b82ce5cc6720dab88516b675ee869f4368f1e162415225ef632'}, 'README.md': {'bytes': 1301, 'sha256': '11292d6aac51b43dfc23e2b933e873c0c121008e2db095c77486746891bae52a'}, 'REVIEW_INPUT_BINDINGS.json': {'bytes': 512, 'sha256': 'bd96868359f0289e52d5267a0666f2ab475e916bb6df2208820364410a5583ef'}, 'SOURCE_GATE.md': {'bytes': 4748, 'sha256': 'f33ec78d52712d8ab4ebe150ffb8afc5d714d8c9f9ac632de2e8dd47cb87c89a'}, 'generated_CHECK_RESULTS.json': {'bytes': 15334, 'sha256': '8dc95c57ae85e2e0f1cb89fff0785a8566125cde8319ed0590a9c6196bffa16b'}, 'generated_INDEPENDENT_CHECK_RESULTS.json': {'bytes': 1244, 'sha256': 'd93b2aa069984325b3ef1855351e23ea781e48a3808135c6430dc0953e87072a'}, 'generated_MANIFEST.json': {'bytes': 392, 'sha256': 'f0c3f277307bd9c9c975f646fd9121ba41dac2c5e3db72a0f6f747c9b815cd25'}, 'independent_review_checks.py': {'bytes': 3278, 'sha256': '9748381dda5e8f92b1eb6929118eaba53b36824f9fc7777443d889e9c05df47d'}, 'independent_review_checks.py.original.txt': {'bytes': 2211, 'sha256': 'ac04cf40d79eb9eeb7ef0dcc5e7fefc1749a57b187a6429c026c90c29722b722'}, 'independent_review_checks.py.stdout.json': {'bytes': 1244, 'sha256': 'd93b2aa069984325b3ef1855351e23ea781e48a3808135c6430dc0953e87072a'}, 'verify.py': {'bytes': 5660, 'sha256': '110102a0464843c1f143234da316477fc099538757f201db9e31bf98d0cb3d9a'}, 'verify.py.original.txt': {'bytes': 5660, 'sha256': '110102a0464843c1f143234da316477fc099538757f201db9e31bf98d0cb3d9a'}, 'verify.py.stdout.json': {'bytes': 473, 'sha256': '4c39777dc5eef63ceace7e7c9def1cebe65ccb18912d33823e97dfa84c339a41'}}
MANIFEST_HASH = '0fce72d07619656fd6a527fef0be127da19a9d568132fae9e614dcae4aa5ebbf'
ALLOWED=set(EXPECTED)|{'MANIFEST.json','validate.py'}
sys.dont_write_bytecode=True
def no_sockets(event,args):
 if event.startswith('socket.'): raise PermissionError('socket events denied')
sys.addaudithook(no_sockets)
def require(ok,message):
 if not ok: raise ValueError(message)
def inventory(root):
 root=Path(os.path.abspath(root))
 for p in reversed([root,*root.parents]):
  require(stat.S_ISDIR(os.lstat(p).st_mode),'unsafe root or ancestor')
 found=set()
 for e in os.scandir(root):
  s=e.stat(follow_symlinks=False)
  require(stat.S_ISREG(s.st_mode),'nonregular entry: '+e.name)
  require(s.st_nlink==1,'hard link: '+e.name)
  require(e.name in ALLOWED,'unexpected entry: '+e.name)
  require(s.st_size<=1000000,'oversized entry: '+e.name)
  found.add(e.name)
 require(found==ALLOWED,'inventory differs')
 return root
CONTENT_READS=0
def read(root,name):
 global CONTENT_READS
 CONTENT_READS+=1
 fd=os.open(root/name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
 try:
  s=os.fstat(fd);require(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'unsafe file read')
  with os.fdopen(fd,'rb',closefd=False) as f:data=f.read(1000001)
  require(len(data)<=1000000,'oversized content')
  return data
 finally:os.close(fd)
class Harden(ast.NodeTransformer):
 def visit_Assert(self,n):
  return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=n.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='RuntimeError',ctx=ast.Load()),args=[ast.Constant('independent mathematical check failed: '+ast.unparse(n.test))],keywords=[]),cause=None)],orelse=[]),n)
def provenance(blobs):
 for name in ['verify.py','independent_review_checks.py']:
  tree=ast.parse(blobs[name]); original=ast.parse(blobs[name+'.original.txt'])
  if name=='independent_review_checks.py':original=ast.fix_missing_locations(Harden().visit(original))
  require(ast.dump(tree,include_attributes=False)==ast.dump(original,include_attributes=False),'whole-module AST mismatch: '+name)
  require(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),'removable assertion: '+name)
def replay(blobs,optimization):
 with tempfile.TemporaryDirectory(prefix='forcing-audit-') as tmp:
  root=Path(tmp)
  for name in ['MATHEMATICAL_AUDIT.md','verify.py','independent_review_checks.py']:(root/name).write_bytes(blobs[name])
  outputs={}
  for name in ['verify.py','independent_review_checks.py']:
   stream=io.StringIO()
   with contextlib.redirect_stdout(stream):exec(compile(ast.parse(blobs[name]),name,'exec',optimize=optimization),{'__name__':'__main__','__file__':str(root/name)})
   outputs[name+'.stdout.json']=stream.getvalue().encode()
  for name in ['CHECK_RESULTS.json','MANIFEST.json','INDEPENDENT_CHECK_RESULTS.json']:outputs['generated_'+name]=(root/name).read_bytes()
  return outputs
def main():
 root=inventory(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent)
 raw=read(root,'MANIFEST.json');require(hashlib.sha256(raw).hexdigest()==MANIFEST_HASH,'manifest hash mismatch')
 m=json.loads(raw);require(m=={'schema':1,'row':1901,'problem_id':'20002454','files':EXPECTED},'manifest mismatch')
 blobs={}
 for name,expected in EXPECTED.items():
  data=read(root,name);require(len(data)==expected['bytes'] and hashlib.sha256(data).hexdigest()==expected['sha256'],'payload mismatch: '+name);blobs[name]=data
 provenance(blobs)
 for mode in [0,1]:
  for name,data in replay(blobs,mode).items():require(data==blobs[name],'exact replay mismatch: '+name)
 print('PASS: row 1901 ID 20002454 exact inventory, hashes, whole-module AST provenance, normal/optimized outputs. Partial mathematics only.')
if __name__=='__main__':
 try:main()
 except Exception as exc:
  print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
