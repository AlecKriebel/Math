#!/usr/bin/env python3
"""Independent finite controls and fail-closed package checks; not a target proof.

Default: independently generated combinatorics and small-monoid controls.
Optional --author-dir: validate and replay the exact frozen author packet.
Optional --catalog/--problems/--research: check full corpora and review identity.
Optional --source-dir: rehash privately supplied scholarly PDFs, never copy them.
Optional --manifest and --expected-manifest: validate an exact recursive file set.
Use Python 3.10+ and the standard library; no network or repository mutations.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
import math
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile

AUTHOR_MANIFEST = '64feb895b04279f97b88a9f624d5d75d9937b14d3b10981badf790e5dc2bb619'
AUTHOR_ZIP = '80e41bf9af68cbd1197495c188ba3ea956b541238ea33ab0ea4cbadfeabecb60'
CORPORA = {
 'catalog': (21735099, '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
 'problems': (68931837, '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
 'research': (80334822, '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b')}
STATEMENT = '9c4f90cf2e091ef4dc8f2336fcac77d255b9acf432b0c9ea645596fd62b5a33c'
REVIEW = '5576c84aff240284caeb8d3ea655c4be9c82ed64d9a7c4737888242b70cb9487'
COUNT = 0

def need(v, message):
 global COUNT
 COUNT += 1
 if not v:
  raise AssertionError(message)

def sha(b):
 return hashlib.sha256(b).hexdigest()

def blob(b):
 return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def boundary(c):
 result = Counter()
 for s,v in c.items():
  for i in range(len(s)):
   result[s[:i]+s[i+1:]] += (-1 if i%2 else 1)*v
 return {s:v for s,v in result.items() if v}

def rank_binary(columns):
 pivots = {}
 for column in columns:
  while column:
   top = column.bit_length()-1
   if top in pivots:
    column ^= pivots[top]
   else:
    pivots[top] = column
    break
 return len(pivots)

def topology():
 records = []
 for q in range(1,8):
  # Enumerate cross-polytope faces independently as ternary coordinate vectors.
  layers = [[] for _ in range(q)]
  for choices in itertools.product((-1,0,1), repeat=q):
   s=tuple((i,v) for i,v in enumerate(choices) if v)
   if s: layers[len(s)-1].append(s)
  counts=list(map(len,layers))
  need(counts==[math.comb(q,k)*2**k for k in range(1,q+1)],'cross-polytope f-vector')
  ranks=[0]
  for degree in range(1,q):
   indices={s:i for i,s in enumerate(layers[degree-1])}
   columns=[]
   for s in layers[degree]:
    b=boundary({s:1})
    need(not boundary(b),'integral differential squares to zero')
    columns.append(sum(1<<indices[t] for t in b))
   ranks.append(rank_binary(columns))
  ranks.append(0)
  betti=[counts[k]-ranks[k]-ranks[k+1] for k in range(q)]
  need(betti==[int(k==0)+int(k==q-1) for k in range(q)],'binary sphere homology')
  need(sum((-1)**k*c for k,c in enumerate(counts))==1+(-1)**(q-1),'Euler characteristic')
  top={s:math.prod(sign for _,sign in s) for s in layers[-1]}
  need(not boundary(top),'integral fundamental cycle')
  records.append({'levels':q,'f_vector':counts,'betti_F2':betti})
 a,b,c,d,e=(0,1),(0,-1),(1,1),(1,-1),(2,1)
 z={(a,c):1,(b,c):-1,(b,d):1,(a,d):-1}
 cone={s+(e,):v for s,v in z.items()}
 need(not boundary(z),'square cycle')
 need(boundary(cone)==z,'third level fills square integrally')
 return records

def enumerate_monoids(n):
 for tail in itertools.product(range(n),repeat=(n-1)**2):
  table=list(range(n))
  for a in range(1,n):table.extend([a]+list(tail[(a-1)*(n-1):a*(n-1)]))
  if all(table[table[a*n+b]*n+c]==table[a*n+table[b*n+c]]
         for a,b,c in itertools.product(range(n),repeat=3)):
   yield tuple(table)

def algebra():
 all_m={n:list(enumerate_monoids(n)) for n in range(1,5)}
 need([len(all_m[n]) for n in all_m]==[1,2,11,156],'identity-fixed labeled monoid counts')
 info=[]
 for n, tables in all_m.items():
  for t in tables:
   z=tuple(a for a in range(n) if all(t[a*n+b]==t[b*n+a] for b in range(n)))
   need(0 in z,'central unary unit')
   for x,y in itertools.product(z,repeat=2):
    need(t[x*n+y] in z and t[x*n+y]==t[y*n+x],'central composition and symmetry')
   # Com action: empty product, singleton, binary substitution and ternary symmetry.
   for x,y,w in itertools.product(z,repeat=3):
    lhs=t[t[x*n+y]*n+w]
    need(lhs==t[x*n+t[y*n+w]],'flattening operadic substitutions')
    need(all(t[t[u*n+v]*n+r]==lhs for u,v,r in itertools.permutations((x,y,w))),
         'permutation invariance')
   info.append((n,t,z))
 surjections=0
 for n,s,z in info:
  for m,t,zt in info:
   if m>min(n,3):continue
   for tail in itertools.product(range(m),repeat=n-1):
    f=(0,)+tail
    if len(set(f))!=m:continue
    if all(f[s[a*n+b]]==t[f[a]*m+f[b]] for a,b in itertools.product(range(n),repeat=2)):
     surjections+=1
     need(all(f[x] in zt for x in z),'surjective naturality')
 permutations=list(itertools.permutations(range(3)))
 comp=lambda p,q:tuple(p[q[i]] for i in range(3))
 identity=(0,1,2); x=(1,0,2);y=(0,2,1)
 zg=[p for p in permutations if all(comp(p,q)==comp(q,p) for q in permutations)]
 need(zg==[identity] and comp(x,y)!=comp(y,x),'C2 to S3 noncovariance')
 # Unary/nullary compatibility of an endomorphism operad forces each value fixed.
 for n in range(1,5):
  candidates=[z for z in itertools.product(range(n),repeat=n)
              if all(z[a]==a for a in range(n))]
  need(candidates==[tuple(range(n))],'all nullaries force identity')
 return {'identity_fixed_monoids':{str(n):len(t) for n,t in all_m.items()},
         'surjective_maps_to_orders_at_most_3':surjections,'S3_center_size':len(zg)}

def label_orbits():
 # Distinct labels give a trivial stabilizer, unlike a same-label binary sector.
 p=list(itertools.permutations(range(2)))
 permute=lambda x,s:tuple(x[s[i]] for i in range(len(x)))
 need(sum(permute(('a','b'),s)==('a','b') for s in p)==1,'mixed labels trivial stabilizer')
 need(sum(permute(('a','a'),s)==('a','a') for s in p)==2,'same labels nontrivial stabilizer')
 for x in [('a','b'),('b','a')]:
  need(sum(permute(x,s)==('a','b') for s in p)==1,'unique ordered mixed-label representative')
 return {'mixed_label_stabilizer':1,'same_label_stabilizer':2,
         'limitation':'Finite label check only; topological action obstruction is proved in the audit report.'}

def verify_manifest(path, expected):
 """Fail closed on every directory entry, using lstat before reading files."""
 path=Path(path).absolute()
 if not stat.S_ISREG(path.lstat().st_mode):raise ValueError('manifest must be a regular file')
 raw=path.read_bytes()
 if sha(raw)!=expected:raise ValueError('trusted manifest digest mismatch')
 data=json.loads(raw);root=path.parent;listed={}
 for rec in data['files']:
  rel=rec['path'];p=PurePosixPath(rel)
  if (not isinstance(rel,str) or p.is_absolute() or not p.parts or
      any(x in ('','..','.') for x in p.parts) or str(p)!=rel or '\\' in rel or
      rel in listed or rel==path.name):raise ValueError('unsafe or duplicate manifest path')
  listed[rel]=rec
 allowed_dirs={str(a) for rel in listed for a in PurePosixPath(rel).parents if str(a)!='.'}
 found=set();dirs=set()
 def walk(folder):
  for entry in folder.iterdir():
   rel=entry.relative_to(root).as_posix();mode=entry.lstat().st_mode
   if stat.S_ISDIR(mode):
    if rel not in allowed_dirs:raise ValueError('unlisted directory')
    dirs.add(rel);walk(entry)
   elif stat.S_ISREG(mode):
    if rel==path.name:continue
    if rel not in listed:raise ValueError('unlisted regular file')
    b=entry.read_bytes();rec=listed[rel]
    if len(b)!=rec['bytes'] or sha(b)!=rec['sha256']:raise ValueError('file identity mismatch')
    found.add(rel)
   else:raise ValueError('symbolic link or special entry')
 walk(root)
 if found!=set(listed) or dirs!=allowed_dirs:raise ValueError('missing entry')
 return {'files':len(found),'manifest_sha256':sha(raw),'all_entries_regular_or_declared_directories':True}

def manifest_regressions():
 cases=[]
 with tempfile.TemporaryDirectory() as td:
  root=Path(td);(root/'nested').mkdir();(root/'nested'/'item').write_bytes(b'audit')
  data={'files':[{'path':'nested/item','bytes':5,'sha256':sha(b'audit')}]}
  path=root/'MANIFEST.json';path.write_text(json.dumps(data));trusted=sha(path.read_bytes())
  need(verify_manifest(path,trusted)['files']==1,'strict recursive manifest positive control')
  tests=[('changed',lambda:(root/'nested'/'item').write_bytes(b'other'),lambda:(root/'nested'/'item').write_bytes(b'audit')),
         ('missing',lambda:(root/'nested'/'item').unlink(),lambda:(root/'nested'/'item').write_bytes(b'audit')),
         ('extra_file',lambda:(root/'extra').write_bytes(b'x'),lambda:(root/'extra').unlink()),
         ('extra_directory',lambda:(root/'extra').mkdir(),lambda:(root/'extra').rmdir()),
         ('dangling_symlink',lambda:(root/'extra').symlink_to('missing'),lambda:(root/'extra').unlink()),
         ('file_symlink',lambda:(root/'extra').symlink_to('nested/item'),lambda:(root/'extra').unlink()),
         ('directory_symlink',lambda:(root/'extra').symlink_to('nested'),lambda:(root/'extra').unlink()),
         ('fifo',lambda:os.mkfifo(root/'extra'),lambda:(root/'extra').unlink())]
  for name,setup,undo in tests:
   setup();rejected=False
   try:verify_manifest(path,trusted)
   except (ValueError,FileNotFoundError):rejected=True
   finally:undo()
   need(rejected,'reject '+name);cases.append({'case':name,'rejected':rejected})
  for name,d in [('wrong_digest','0'*64)]:
   try:verify_manifest(path,d);rejected=False
   except ValueError:rejected=True
   need(rejected,name);cases.append({'case':name,'rejected':rejected})
 return cases

def author_replay(root):
 root=Path(root).absolute();identity=verify_manifest(root/'MANIFEST.json',AUTHOR_MANIFEST)
 run=subprocess.run([sys.executable,'-B',str(root/'verify.py')],capture_output=True,check=True)
 need(run.stdout==(root/'RESULTS.json').read_bytes(),'default author output byte identity')
 counts=json.loads(run.stdout)['assertions_passed'];need(counts==900,'author finite assertion count')
 run=subprocess.run([sys.executable,'-B',str(root/'verify.py'),'--manifest',str(root/'MANIFEST.json'),
                     '--expected-manifest',AUTHOR_MANIFEST],capture_output=True,check=True)
 need(json.loads(run.stdout)['assertions_passed']==930,'author manifest assertion count')
 with tempfile.TemporaryDirectory() as td:
  copy=Path(td)/'author';shutil.copytree(root,copy);(copy/'extra_link').symlink_to('nonexistent')
  run=subprocess.run([sys.executable,'-B',str(copy/'verify.py'),'--manifest',str(copy/'MANIFEST.json'),
                      '--expected-manifest',AUTHOR_MANIFEST],capture_output=True)
  need(run.returncode==0,'reproduce author dangling-symlink defect')
  try:verify_manifest(copy/'MANIFEST.json',AUTHOR_MANIFEST);rejected=False
  except ValueError:rejected=True
  need(rejected,'audit guard rejects author missed entry')
 return {'identity':identity,'finite_assertions':counts,'manifest_assertions':930,
         'author_dangling_symlink_blind_spot_reproduced':True,'audit_guard_rejected_it':True}

def provenance(args):
 paths=[args.catalog,args.problems,args.research]
 if not all(paths):raise ValueError('supply all three complete corpora')
 content={};records={}
 for name,path in zip(CORPORA,paths):
  b=Path(path).read_bytes();n,h=CORPORA[name]
  need(len(b)==n and sha(b)==h,'complete corpus '+name)
  content[name]=json.loads(b);records[name]={'bytes':len(b),'sha256':sha(b),'records':len(content[name])}
  if name=='catalog':need(blob(b)=='bd5c23e4e6c7e1901717a7e596477a7f6dc72425','catalog pinned Git blob')
 c=[r for r in content['catalog'] if str(r['id'])=='30006031']
 p=[r for r in content['problems'] if str(r['id'])=='30006031']
 need(len(c)==len(p)==1,'unique selected identity')
 c,p=c[0],p[0];key='OWR-14298590-001'
 need(c['problem_number']==p['problem_number']==key and c['rank']==792,'rank and alias')
 need(c['source_url']==p['source_url']=='https://doi.org/10.4171/owr/2024/39','primary DOI')
 need(sha(p['statement'].encode())==c['statement_hash']==STATEMENT,'statement identity')
 need(sum(x['problem_number']==key for x in content['problems'])==1,'unique research join')
 need(key not in content['research'],'absent exact research key')
 r=content['research'].get(key,{})
 encode=lambda p,r:json.dumps([p,r],sort_keys=True).encode()
 need(sha(encode(p,r))==c['review_hash']==REVIEW,'full record review identity')
 changed=dict(p);changed['title']=changed.get('title','')+' audit mutation'
 negatives=[sha(encode(changed,r)),sha(encode(p,{'audit_mutation':True})),
            sha(p['statement'].encode()),sha(json.dumps([p,r],sort_keys=True,separators=(',',':')).encode())]
 need(all(h!=REVIEW for h in negatives),'review hash mutation controls')
 tokens=('30006031','owr-14298590-001','14298590','little three-disks actions on operadic homotopy centers')
 matches=[k for k,v in content['research'].items() if any(t in (k+' '+json.dumps(v)).lower() for t in tokens)]
 need(not matches,'bounded full research record scan')
 return {'corpora':records,'statement_sha256':STATEMENT,'review_sha256':REVIEW,
         'full_record_review_hash_recomputed':True,'review_negative_controls':4,
         'research_exact_key_present':False,'bounded_full_record_scan_matches':len(matches)}

def sources(root, metadata):
 names=['owr_ems.pdf','triple_delooping.pdf','condensation.pdf','centers.pdf','lattice_path.pdf',
        'additivity.pdf','swiss_cheese.pdf','polynomial_2monads.pdf']
 raw=Path(metadata).read_bytes()
 need(sha(raw)=='73ce2013442cbd5efcaea2795fddcd8094d0429776bbd48bcc8094e94ed44715','frozen source metadata digest')
 records=json.loads(raw)['sources'];result=[]
 need(len(records)==8,'exact scholarly source count')
 for name,rec in zip(names,records):
  b=(Path(root)/name).read_bytes()
  need(b.startswith(b'%PDF-'),'actual PDF '+name)
  need(len(b)==rec['bytes'] and sha(b)==rec['sha256'],'source hash '+name)
  result.append({'title':rec['title'],'url':rec['url'],'bytes':len(b),'sha256':sha(b)})
 need((Path(root)/'owr_ems.pdf').read_bytes()==(Path(root)/'owr2024_39.pdf').read_bytes(),
      'EMS and TIB private primary files identical')
 return result

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 for name in ['author-dir','catalog','problems','research','source-dir','source-metadata','manifest','expected-manifest']:
  ap.add_argument('--'+name)
 args=ap.parse_args()
 result={'problem_id':30006031,'target_status':'UNRESOLVED','poset_controls':topology(),
         'monoid_controls':algebra(),'label_orbit_controls':label_orbits(),
         'strict_manifest_regressions':manifest_regressions()}
 if args.author_dir:result['author_replay']=author_replay(args.author_dir)
 if any([args.catalog,args.problems,args.research]):result['provenance']=provenance(args)
 if args.source_dir:
  if not args.source_metadata:raise ValueError('source metadata required')
  result['source_hash_checks']=sources(args.source_dir,args.source_metadata)
 if args.manifest:
  if not args.expected_manifest:raise ValueError('trusted digest required')
  result['manifest']=verify_manifest(args.manifest,args.expected_manifest)
 result['assertions_passed']=COUNT
 result['result']='PASS_WITH_DOCUMENTED_AUTHOR_GUARD_CORRECTION'
 result['limits']='Finite controls, manual mathematical audit and byte checks are distinct; none resolves the target.'
 print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
