#!/usr/bin/env python3
"""Replay the pinned author's artifact and independent finite algebra checks.

This is integrity/diagnostic verification, never formal proof certification.
For full external input binding pass both --corpus-dir and --source-dir.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
AUTHOR = 'WEINSTEIN_TWO_HANDLEBODIES_2986_AUTHOR_SAFE_FREEZE.zip'
EXTERNAL = 'WEINSTEIN_TWO_HANDLEBODIES_2986_AUTHOR_EXTERNAL_MANIFEST.json'
AUTHOR_PIN = (15453, 'd322363aa52fb7f45110c3a66be3ed3381cba5cd23ce2dbe6ce20c283734b25b')
EXTERNAL_PIN = (2111, 'febab4c31b53b7d4a6f5844b22c808b1593f17e4006fa1c3260e5f0818a42cad')
CORPUS = [
 ('catalog.json',21735099,'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
 ('problems.json',68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
 ('research_results.json',80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b')]
SOURCE_NAMES = ['k3.pdf','bowden_v3.pdf','christian_menke_v4.pdf','splitting_v1.pdf','flexible_published.pdf','breen_christian_v3.pdf','hozoori.pdf']
CHECKS = 0


def need(test, message):
 global CHECKS
 if not test:
  raise ValueError(message)
 CHECKS += 1


def digest(b):
 return hashlib.sha256(b).hexdigest()


def pin_bytes(b,pin,label):
 need(len(b)==pin[0],label+': byte count mismatch')
 need(digest(b)==pin[1],label+': hash mismatch')


def matrix_sum(a,b):
 return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]


def matrix_mul(a,b):
 return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
 return [list(x) for x in zip(*a)]


def independent_algebra():
 # Coordinate order q1,q2,p1,p2. The Hessian is reconstructed directly
 # from f=-p1*q2+p2*q1-(p1*q1+p2*q2)/2, without author polynomial code.
 n=4
 identity=[[Q(int(i==j)) for j in range(n)] for i in range(n)]
 omega=[[Q(x) for x in row] for row in [[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]]]
 hessian=[[Q(x) for x in row] for row in [[0,0,Q(-1,2),1],[0,0,-1,Q(-1,2)],[Q(-1,2),-1,0,0],[1,Q(-1,2),0,0]]]
 need(hessian==transpose(hessian),'Hessian symmetry')
 half_identity=[[x/2 for x in row] for row in identity]
 A=matrix_sum(half_identity,matrix_mul(omega,hessian))
 want=[[Q(x) for x in row] for row in [[0,-1,0,0],[1,0,0,0],[0,0,1,-1],[0,0,1,1]]]
 need(A==want,'Independent Liouville matrix')
 # i_X omega has coefficient matrix -Omega*A, its d has matrix B^T-B.
 B=[[-x for x in row] for row in matrix_mul(omega,A)]
 need(matrix_sum(transpose(B),[[-x for x in row] for row in B])==omega,'Exterior derivative matrix')
 need(matrix_sum(matrix_mul(transpose(A),omega),matrix_mul(omega,A))==omega,'Liouville conformal symplectic identity')
 need(sum(A[i][i] for i in range(n))==2,'Divergence')
 need(all(A[i][j]==0 for i in [2,3] for j in [0,1]),'p=0 invariant')
 J=[row[:2] for row in A[:2]]
 need(matrix_mul(J,J)==[[-1,0],[0,-1]],'Rotation generator square')
 need(matrix_sum(J,transpose(J))==[[0,0],[0,0]],'Rotation preserves norm')
 need(Q(0)<Q(1,2)**2<Q(1,2)<Q(3,4)<1,'Orbit/cutoff separation')
 # Identities for all t follow coefficientwise, rather than time sampling.
 AH=matrix_mul(omega,hessian)
 need(matrix_sum(matrix_mul(transpose(AH),omega),matrix_mul(omega,AH))==[[0]*4 for _ in range(4)],'Hamiltonian perturbation preserves omega')
 need(matrix_sum(transpose(half_identity),half_identity)==identity,'Radial Lyapunov quadratic identity')
 return {'method':'independently reconstructed rational Hessian and 4x4 matrices','checks':11,'claim':'finite algebra identities only; smooth, ODE, and topology proofs are written arguments'}


def validate_archive():
 ab=(ROOT/AUTHOR).read_bytes(); eb=(ROOT/EXTERNAL).read_bytes()
 pin_bytes(ab,AUTHOR_PIN,'author archive');pin_bytes(eb,EXTERNAL_PIN,'author external manifest')
 ext=json.loads(eb)
 need(ext['archive']=={'name':AUTHOR,'bytes':AUTHOR_PIN[0],'sha256':AUTHOR_PIN[1]},'external archive declaration')
 with zipfile.ZipFile(ROOT/AUTHOR) as z:
  entries=z.infolist();names=[x.filename for x in entries]
  need(len(names)==len(set(names))==9,'ZIP duplicate/member count')
  wanted={r['path']:r for r in ext['members']}
  need(set(names)==set(wanted),'ZIP exact member set')
  for info in entries:
   need(not info.is_dir() and Path(info.filename).name==info.filename and not Path(info.filename).is_absolute(),'unsafe ZIP path')
   need(not stat.S_ISLNK(info.external_attr>>16),'ZIP symlink')
   e=wanted[info.filename];pin_bytes(z.read(info), (e['bytes'],e['sha256']),info.filename)
  source=json.loads(z.read('SOURCE_AUDIT.json'))
  baseline=json.loads(z.read('CHECK_RESULTS.json'))
  status=json.loads(z.read('STATUS.json'))
  need(status['rank']==922 and status['turns_used']==4 and status['turn_limit']==5,'campaign position')
  need(status['status']=='partial' and status['full_solution'] is False and status['target_example_constructed'] is False,'bounded scope')
  need(status['novelty_established'] is False,'novelty limit')
  outputs=[]
  for optimized in [False,True]:
   with tempfile.TemporaryDirectory(prefix='weinstein audited relocation ') as td:
    dest=Path(td)/'author package';dest.mkdir();z.extractall(dest)
    cmd=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(dest/'verify.py')]
    p=subprocess.run(cmd,cwd=td,capture_output=True,text=True,timeout=30)
    need(p.returncode==0,'author replay failed: '+p.stderr)
    need(not p.stderr,'unexpected author stderr')
    need(json.loads(p.stdout)==baseline,'author replay differs from baseline')
    outputs.append(p.stdout)
  need(outputs[0]==outputs[1],'normal and optimized outputs differ')
 return source,{'normal':'PASS','optimized':'PASS','isolated':True,'relocated':True,'byte_identical_stdout':True,'positive_checks_per_run':85,'internal_negative_controls_per_run':3,'stdout_sha256':digest(outputs[0].encode())}


def bind_inputs(corpus_dir, source_dir, source):
 result={'provided':bool(corpus_dir),'corpus':[],'sources':[]}
 if not corpus_dir:
  result['limitation']='External datasets and PDFs were not supplied for this replay.'
  return result
 croot=Path(corpus_dir);sroot=Path(source_dir)
 parsed={}
 for name,size,h in CORPUS:
  b=(croot/name).read_bytes();pin_bytes(b,(size,h),name);parsed[name]=json.loads(b)
  result['corpus'].append({'name':name,'bytes':size,'sha256':h,'match':True})
 cat=[r for r in parsed['catalog.json'] if str(r.get('id'))=='2986']
 rec=[r for r in parsed['problems.json'] if r.get('id')==2986]
 need(len(cat)==len(rec)==1,'exact-ID uniqueness')
 need(cat[0]['rank']==922 and cat[0]['problem_number']==rec[0]['problem_number']=='KP-4.110','record identity')
 report=parsed['research_results.json'].get('KP-4.110',{})
 need(report=={},'inherited report is not empty')
 sh=digest(rec[0]['statement'].encode());ph=digest(json.dumps([rec[0],report],sort_keys=True).encode())
 need(sh==source['statement_sha256']==cat[0]['statement_hash'],'statement binding')
 need(ph==source['record_report_pair_sha256']==cat[0]['review_hash'],'complete record/report binding')
 result['identity']={'exact_catalog_matches':1,'exact_problem_matches':1,'rank':922,'problem_id':2986,'problem_number':'KP-4.110','statement_sha256':sh,'complete_record_report_sha256':ph,'inherited_report_empty':True,'substantive_record_review':'See written audit; machine checks identity, not proof content.'}
 need(len(source['sources'])==len(SOURCE_NAMES),'source count')
 for name,e in zip(SOURCE_NAMES,source['sources']):
  b=(sroot/name).read_bytes();pin_bytes(b,(e['bytes'],e['sha256']),name);need(b.startswith(b'%PDF-'),'PDF magic: '+name)
  result['sources'].append({'title':e['title'],'public_url':e['public_url'],'bytes':len(b),'sha256':digest(b),'match':True})
 return result


def audit_manifest():
 manifest=json.loads((ROOT/'AUDIT_MANIFEST.json').read_text())
 need(manifest['schema']=='weinstein-independent-audit-members-v1','audit manifest schema')
 entries=manifest['files'];names=[e['path'] for e in entries]
 need(len(names)==len(set(names)),'audit manifest duplicates')
 need(set(names)=={p.name for p in ROOT.iterdir()}-{'AUDIT_MANIFEST.json'},'audit member set')
 for e in entries:
  need(set(e)=={'path','bytes','sha256'},'audit entry schema')
  p=ROOT/e['path'];need(p.name==e['path'] and p.is_file() and not p.is_symlink(),'unsafe audit member')
  pin_bytes(p.read_bytes(),(e['bytes'],e['sha256']),e['path'])


def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--corpus-dir');parser.add_argument('--source-dir')
 args=parser.parse_args()
 need(bool(args.corpus_dir)==bool(args.source_dir),'Supply both external input directories or neither')
 audit_manifest()
 source,replay=validate_archive()
 algebra=independent_algebra()
 inputs=bind_inputs(args.corpus_dir,args.source_dir,source)
 print(json.dumps({'result':'PASS','problem_id':2986,'scope':'accepted bounded partial, 4/5; KP-4.110 unresolved','formal_proof_certification':False,'author_replay':replay,'independent_algebra':algebra,'external_input_binding':inputs,'checks':CHECKS},indent=2,sort_keys=True))

if __name__=='__main__':
 try:main()
 except Exception as e:
  print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
