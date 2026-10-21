#!/usr/bin/env python3
"""Independent byte custody and exact algebra diagnostics; not a proof/priority oracle.

Authenticate this file against an external SHA256 before execution. Optional
packet authentication also requires an external manifest SHA256. Controls write
only to a new explicitly supplied scratch directory, never the reviewed tree.
"""
import argparse, hashlib, importlib.util, io, json, os, shutil, stat, subprocess, sys, zipfile
from pathlib import Path, PurePosixPath
sys.dont_write_bytecode=True
SOURCE_PIN='5d7bccdc118a464da0e149804c4b512c88a9d28cbff2d8b3bc280d963dd4f348'
VERIFIER_PIN='700eaab42e6d98589fb2f1c6fa4a3077b4dd74cad4f336a00cb53bd6dfe47489'
HEAD='aa44dec3baf8c1cd179cf8b55f32be95c74ee81a'
SIX={
 'main.tex':(11910,'473336b7f4190447a80fa4145b867cef4403c612819ee01432d01892be5f0e5a'),
 'output/pdf/paper.pdf':(60080,'66d6d448245656cbedc8f219989833529723879561a2d5e6483b5289c6732c83'),
 'source-and-verification.zip':(338085,'c813b48f1ef1de36c90aff9870455adbe74cb4c79e8eafbe4d9f4f75cdfdd1cd'),
 'zenodo-deposit.json':(4834,'04b7462706fd8bee8f5df4d0a7ddbd6c93995958dca116c789259721cac32a70'),
 'zenodo-metadata.json':(4638,'56d88bc6e5f2971417280f834c50a284b5741c9bbf40bc1d13b88fca644142dc'),
 'zenodo-upload-kit.zip':(367714,'1a30de0ac8baa9aaa71c55de6f1b3200bb8b3cf2cb464dfe134e06a8a4abfe49')}
def need(x,msg):
 if not x: raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def strict(b):
 def pairs(ps):
  d={}
  for k,v in ps:need(k not in d,'duplicate JSON key');d[k]=v
  return d
 def bad(x):raise ValueError('nonfinite JSON')
 return json.loads(b,object_pairs_hook=pairs,parse_constant=bad)
def safe(n):
 need(isinstance(n,str) and n and '\\' not in n and not PurePosixPath(n).is_absolute() and all(p not in ('','.','..') for p in n.split('/')),'unsafe relative path')
 return n
def regular(p):
 need(stat.S_ISREG(p.lstat().st_mode),'nonregular file')
 return p.read_bytes()
def ident(b):return len(b),sha(b)
def inventory(p):
 need(p.is_dir() and not p.is_symlink(),'root directory')
 out={};dirs=set()
 for q in p.rglob('*'):
  need(not q.is_symlink(),'symlink')
  n=safe(q.relative_to(p).as_posix())
  if q.is_dir():dirs.add(n)
  else:out[n]=regular(q)
 expected={str(x) for n in out for x in PurePosixPath(n).parents if str(x)!='.'}
 need(dirs==expected,'extra empty directory')
 return out
def check_source(p):
 src=p/'source';fs=inventory(src);need(sha(fs['MANIFEST.json'])==SOURCE_PIN,'external source pin')
 need(sha(fs['verify_source.py'])==VERIFIER_PIN,'external verifier pin')
 mf=strict(fs['MANIFEST.json']);rows={}
 for r in mf['files']:
  n=safe(r['path']);need(n not in rows,'duplicate path');rows[n]=r
 need(len(fs)==151 and set(fs)==set(rows)|{'MANIFEST.json'},'151 closure')
 for n,r in rows.items():need(ident(fs[n])==(r['bytes'],r['sha256']),'source bytes '+n)
 for n,(size,h) in SIX.items():need(ident(regular(p/n))==(size,h),'six output '+n)
 pi=strict(regular(p/'PACKAGE_INVENTORY.json'))
 need(pi['source_manifest_sha256']==SOURCE_PIN and pi['source_files_including_manifest']==151,'inventory source binding')
 need({r['path']:(r['bytes'],r['sha256']) for r in pi['files']}==SIX,'inventory exact six')
 with zipfile.ZipFile(io.BytesIO(regular(p/'source-and-verification.zip'))) as z:
  need(len(z.infolist())==len(set(z.namelist()))==151,'source ZIP count')
  need({safe(i.filename):z.read(i) for i in z.infolist()}==fs,'source ZIP equality')
 identity=strict(fs['audit/intake/ROOT_SOURCE_IDENTITY.json']);need(identity['reviewed_head']==HEAD,'head')
 original={}
 for r in identity['original_files']:
  n=safe(r['path']);b=fs['audit/intake/original/'+n]
  need(n not in original,'duplicate original');original[n]=b
  need(ident(b)==(r['bytes'],r['sha256']),'original SHA')
  need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob'],'Git blob')
 need(len(original)==58,'58 originals')
 base='unsolved_math_prioritization/attempts/30001478/';count=0
 for n,b in original.items():
  if n.endswith('.zip'):
   family='author' if 'AUTHOR_SAFE' in n else 'first_audit' if 'INDEPENDENT_AUDIT' in n else 'second_review'
   with zipfile.ZipFile(io.BytesIO(b)) as z:
    need(len(z.namelist())==len(set(z.namelist())),'duplicate original ZIP')
    for i in z.infolist():need(original[base+family+'/'+safe(i.filename)]==z.read(i),'original ZIP member');count+=1
 need(count==44,'44 original ZIP members')
 selected=strict(fs['audit/intake/SELECTED_PUBLIC_RECORD.json'])
 need(sha(selected['problem']['statement'].encode())=='628ed4ce70b7b62857ead560403291f24b890137a8073ce34a17c50d857aa3a6','statement')
 need(sha(json.dumps([selected['problem'],selected['prior_research']],sort_keys=True).encode())=='cf0071b62b0e096c74205deac1c8f7cad50cbbf50b4f37d8400170a2d742848f','selected pair')
 return {'source_files':151,'original_git_blobs':58,'original_archive_members':44,'exact_distribution_files':6}
def algebra():
 # Independent integer-coefficient free polynomial model. Keys (alpha,beta,word).
 def add(*ps):
  q={}
  for p in ps:
   for m,c in p.items():q[m]=q.get(m,0)+c
  return {m:c for m,c in q.items() if c}
 def mul(p,q):
  r={}
  for (a,b,u),c in p.items():
   for (d,e,v),f in q.items():r[(a+d,b+e,u+v)]=r.get((a+d,b+e,u+v),0)+c*f
  return {m:c for m,c in r.items() if c}
 def neg(p):return {m:-c for m,c in p.items()}
 def sub(p,q):return add(p,neg(q))
 def atom(word='',a=0,b=0):return {(a,b,word):1}
 def evaluate(p,images,comm=False):
  r={}
  for (a,b,w),c in p.items():
   v={(a,b,''):c}
   for letter in w:v=mul(v,images[letter])
   if comm:
    v=add(*[{(aa,bb,''.join(sorted(ww))):cc} for (aa,bb,ww),cc in v.items()])
   r=add(r,v)
  return r
 x={i:atom(str(i)) for i in range(1,5)};a=atom(a=1);b=atom(b=1)
 rel=[]
 for left,right in [(1,1),(1,2),(2,1),(2,2)]:
  rel.append(add(mul(x[left],sub(mul(a,x[right]),x[right+2])),mul(x[left+2],sub(x[right],mul(a,x[right+2])))))
 rel.extend([add(mul(x[1],sub(mul(b,x[1]),x[2])),mul(x[4],sub(x[1],mul(b,x[2])))),add(mul(x[1],sub(mul(b,x[3]),x[4])),mul(x[4],sub(x[3],mul(b,x[4]))))])
 X,Y=atom('X'),atom('Y');Q=add(mul(b,mul(X,X)),neg(mul(X,Y)),mul(Y,X),neg(mul(b,mul(Y,Y))))
 images={'1':X,'2':Y,'3':X,'4':Y}
 need([evaluate(p,images) for p in rel]==[{},{},{},{},Q,Q],'six universal images')
 U,V=atom('U'),atom('V');basis=evaluate(Q,{'X':add(U,V),'Y':V})
 expected=add(mul(b,mul(U,U)),mul(sub(b,atom()),mul(U,V)),mul(add(b,atom()),mul(V,U)))
 need(basis==expected,'triangular identity')
 theta={'X':add(X,mul(b,Y)),'Y':add(mul(b,X),Y)}
 def qtwist(t):
  q={}
  for (aa,bb,w),c in Q.items():
   v=mul({(aa,bb,''):c},mul(atom(w[0]),t[w[1]]))
   q=add(q,*[{(a0,b0,''.join(sorted(w0))):c0} for (a0,b0,w0),c0 in v.items()])
  return q
 need(qtwist(theta)=={},'positive twist')
 need(qtwist({'X':X,'Y':Y})!={},'untwisted negative')
 inverse={'X':sub(X,mul(b,Y)),'Y':sub(Y,mul(b,X))}
 need(qtwist(inverse)=={(0,1,'XX'):2,(0,1,'YY'):-2},'inverse convention residual')
 detected=0
 for n,p in enumerate(rel):
  q=dict(p);m=next(iter(q));q[m]*=-1
  if evaluate(q,images)!=evaluate(p,images):detected+=1
 need(detected==6,'six sign perturbations')
 return {'six_relation_images':'0,0,0,0,Q,Q','triangular_identity':True,'positive_twist':True,'sign_perturbations_detected':detected,'untwisted_rejected':True,'inverse_residual':'2 beta(X²-Y²), zero in char2','scope':'Exact identities only; universal proof in INDEPENDENT_DERIVATION.md.'}
def controls(p,scratch):
 scratch.mkdir(parents=True,exist_ok=False);src=p/'source';pdf=p/'output/pdf/paper.pdf';cases=[]
 def run(root,pin=SOURCE_PIN,extra=(),opt=False):
  return subprocess.run([sys.executable,'-I','-B']+(['-O'] if opt else [])+[str(root/'verify_source.py'),'--expected-manifest-sha256',pin,'--pdf',str(pdf),*extra],capture_output=True,text=True,cwd='/',timeout=90)
 clone=scratch/'relocated source with spaces';shutil.copytree(src,clone)
 for opt in (False,True):need(run(clone,opt=opt).returncode==0,'relocated baseline');cases.append({'case':'relocation_'+str(opt),'result':'PASS'})
 badpdf=scratch/'altered.pdf';raw=pdf.read_bytes();badpdf.write_bytes(raw[:-1]+bytes([raw[-1]^1]))
 for opt in (False,True):
  r=subprocess.run([sys.executable,'-I','-B']+(['-O'] if opt else [])+[str(clone/'verify_source.py'),'--expected-manifest-sha256',SOURCE_PIN,'--pdf',str(badpdf)],capture_output=True,text=True,timeout=30)
  need(r.returncode!=0,'changed PDF accepted')
 cases.append({'case':'altered_supplied_PDF','result':'REJECT_BOTH_MODES'})
 mutations=['bytes','extra','empty','missing','fifo','leaflink','directorylink','wrongpin','dupkey','nonfinite','duplicatepath','unsafe']
 for kind in mutations:
  q=scratch/kind;shutil.copytree(src,q);pin=SOURCE_PIN
  if kind=='bytes':(q/'README.md').write_text('changed')
  elif kind=='extra':(q/'extra').write_text('x')
  elif kind=='empty':(q/'empty').mkdir()
  elif kind=='missing':(q/'README.md').unlink()
  elif kind=='fifo':(q/'README.md').unlink();os.mkfifo(q/'README.md')
  elif kind=='leaflink':(q/'README.md').unlink();(q/'README.md').symlink_to(src/'README.md')
  elif kind=='directorylink':shutil.rmtree(q/'audit/math_source_geometry');(q/'audit/math_source_geometry').symlink_to(src/'audit/math_source_geometry',target_is_directory=True)
  elif kind=='wrongpin':pin='0'*64
  else:
   f=q/'MANIFEST.json';raw=f.read_text();j=strict(raw)
   if kind=='dupkey':raw=raw.replace('{','{"schema":"duplicate",',1)
   elif kind=='nonfinite':raw=raw.replace('"bytes": 291','"bytes": NaN',1);need('NaN' in raw,'nonfinite target')
   elif kind=='duplicatepath':j['files'].append(j['files'][0]);raw=json.dumps(j)
   else:j['files'][0]['path']='../escape';raw=json.dumps(j)
   f.write_text(raw);pin=sha(f.read_bytes())
  for opt in (False,True):need(run(q,pin,opt=opt).returncode!=0,'accepted '+kind)
  cases.append({'case':kind,'result':'REJECT_BOTH_MODES'})
 # Actual builder controls, including aliases. Only cloned inputs can acquire links.
 spec=importlib.util.spec_from_file_location('reviewed_builder',clone/'build_package.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
 for kind in ['inside_source','output_ancestor_link','output_leaf_link','output_hardlink']:
  out=scratch/('builder_'+kind)
  if kind=='inside_source':out=clone/'out'
  elif kind=='output_ancestor_link':out.symlink_to(scratch/'aliasdestination',target_is_directory=True)
  else:
   out.mkdir()
   if kind=='output_leaf_link':(out/'main.tex').symlink_to(clone/'main.tex')
   else:
    donor=scratch/'disposable_donor';donor.write_text('x');os.link(donor,out/'main.tex')
  try:b.build(clone,SOURCE_PIN,pdf,out)
  except (ValueError,OSError):cases.append({'case':kind,'result':'REJECT'})
  else:raise ValueError('builder accepted '+kind)
 # Full ancestry guard exercised by advertised replay, before the expensive jobs.
 alias=scratch/'source_ancestor_alias';alias.symlink_to(clone.parent,target_is_directory=True)
 need(run(alias/clone.name,extra=('--replay',)).returncode!=0,'ancestor alias accepted by replay')
 cases.append({'case':'source_replay_ancestor_alias','result':'REJECT'})
 # Preserve and reproduce the historical old-resolve caveat using owned clones.
 original=clone/'audit/intake/original/unsolved_math_prioritization/attempts/30001478/author'
 altered=scratch/'historical self alias';shutil.copytree(original,altered)
 (altered/'verify.py').unlink();(altered/'verify.py').symlink_to(original/'verify.py');(altered/'EXTRA').write_text('x')
 for opt in (False,True):
  r=subprocess.run([sys.executable,'-I','-B']+(['-O'] if opt else [])+[str(altered/'verify.py')],capture_output=True,text=True,timeout=20)
  need(r.returncode==0 and strict(r.stdout)['status']=='PASS','historical caveat changed')
 cases.append({'case':'old_resolving_verifier_self_alias','result':'EXPECTED_HISTORICAL_PASS_BOTH_MODES'})
 return {'result':'PASS','cases':cases,'count':len(cases),'scope':'Disposable custody, JSON, relocation, builder alias, ancestry and preserved old-path controls; not a universal proof.'}
def packet(root,pin,cp):
 me=Path(__file__).absolute();need(sha(regular(me))==cp,'external checker pin')
 need(me==root/'review_check.py','checker location')
 fs=inventory(root);need(sha(fs['MANIFEST.json'])==pin,'external review manifest')
 mf=strict(fs['MANIFEST.json']);need(mf['schema']=='whole-preprint-round02/v1','review schema')
 rows={r['path']:r for r in mf['files']};need(len(rows)==len(mf['files']),'duplicate review row')
 need(set(fs)==set(rows)|{'MANIFEST.json'} and all('/' not in n for n in fs),'flat review closure')
 for n,r in rows.items():need(ident(fs[n])==(r['bytes'],r['sha256']),'review bytes '+n)
 return len(fs)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preprint-root',type=Path,required=True);ap.add_argument('--scratch',type=Path);ap.add_argument('--packet-root',type=Path);ap.add_argument('--expected-manifest-sha256');ap.add_argument('--expected-checker-sha256');a=ap.parse_args()
 result={'result':'PASS','custody':check_source(a.preprint_root.absolute()),'algebra':algebra()}
 if a.scratch:result['controls']=controls(a.preprint_root.absolute(),a.scratch.absolute())
 if a.packet_root:result['review_files']=packet(a.packet_root.absolute(),a.expected_manifest_sha256,a.expected_checker_sha256)
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as e:print(json.dumps({'result':'FAIL','error':str(e)}));sys.exit(1)
