#!/usr/bin/env python3
"""Round-1 independent, offline mathematical/integrity/service-boundary checks.
Writes only the selected reviewer scratch folder. No live service or Git calls.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,copy,hashlib,importlib.util,json,math,os,shutil,subprocess,sys,tempfile,types,zipfile

def need(x,m):
 if not x:raise RuntimeError(m)
def load(p):
 s=importlib.util.spec_from_file_location('round1_'+p.stem+str(id(p)),p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(b):return hashlib.sha256(b).hexdigest()
def add(a,b):return [a[i] if i>=len(b) else b[i] if i>=len(a) else a[i]+b[i] for i in range(max(len(a),len(b)))]
def scale(a,c):return [x*c for x in a]
def mul(a,b):
 c=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
def power(a,k):
 o=[F(1)]
 for _ in range(k):o=mul(o,a)
 return o
def integ(a,k=0):return sum((x/F(i+k+1) for i,x in enumerate(a)),F(0))
def evalp(a,t):
 x=F(0)
 for c in reversed(a):x=x*t+c
 return x
def kernel(m):
 ts=[[F(1)],[F(1),F(-2)]]
 for j in range(1,m):ts.append(add(scale(mul(ts[-1],ts[1]),2),scale(ts[-2],-1)))
 ans=[F(1)]
 for t in ts[1:m+1]:ans=add(ans,scale(t,2))
 return scale(ans,F(1,2*m+1))
def legendre(j):
 # Rodrigues, expanded independently in x; no imported diagnostic code.
 a=[F(0)]*(2*j+1)
 for k in range(j+1):a[2*k]=F(math.comb(j,k)*(-1)**(j-k))
 for _ in range(j):a=[(i+1)*a[i+1] for i in range(len(a)-1)]
 return scale(a,F(1,2**j*math.factorial(j)))
def math_checks():
 leg=0
 for j in range(13):
  a=legendre(j);need(evalp(a,F(1))==1,'Legendre normalization')
  for k in range(j+1):
   p=mul(a,legendre(k));value=sum((2*c/F(i+1) for i,c in enumerate(p) if i%2==0),F(0))
   need(value==(F(2,2*j+1) if j==k else 0),'Rodrigues norm/orthogonality');leg+=1
  # Independent finite exact endpoint checks; the analytic modulus bound is separate.
  for i in range(65):need(abs(evalp(a,F(i,32)-1))<=1,'Legendre grid')
 witnesses=[]
 for m in range(1,6):
  a=kernel(m);need(len(a)==m+1 and a[0]==1,'kernel degree/core endpoint')
  q=power(a,10);den=integ(q,2);num=integ(q,3);need(den>0 and 0<num<den,'pyramid all-mass witness')
  witnesses.append({'m':m,'denominator':str(den),'objective':str(num/den),'density_degree':10*m,'hierarchy_order':5*m})
 degree=0
 for n in range(1,21):
  L=n+2
  for r in range(1,2001):
   if r>=2*L:
    m=r//(2*L);need(m>=1 and 4*m*L<=2*r,'global-square degree');need(F(1,(2*m+1)**2)<=F(4*L*L,r*r),'floor constant')
   else:need(4*L*L>r*r,'small-order constant')
   degree+=1
 # Direct order-one pyramid determinant in the basis (1,z,x,y).
 H=[[F(4,3),F(1)],[F(1),F(4,5)]];Z=[[F(1),F(4,5)],[F(4,5),F(2,3)]]
 det=add(mul([Z[0][0],-H[0][0]],[Z[1][1],-H[1][1]]),scale(mul([Z[0][1],-H[0][1]],[Z[1][0],-H[1][0]]),-1))
 need(det==[F(2,75),-F(4,45),F(1,15)],'pyramid exact characteristic quadratic')
 need(F(2,9)/F(4,15)==F(5,6),'pyramid odd modes')
 return {'Rodrigues_pair_checks':leg,'Legendre_exact_grid_points':13*65,'pyramid_witnesses':witnesses,'all_order_degree_finite_checks':degree,'pyramid_quadratic':[str(x) for x in det],'limits':'Finite exact consistency checks; the all-body/all-order proof was separately checked analytically.'}
def archive_checks(a,scratch):
 p=a/'publication';build=json.loads((p/'BUILD_RECEIPT.json').read_text());raw=(p/build['verification_zip']['path']).read_bytes();need(sha(raw)==build['verification_zip']['sha256'],'outside ZIP SHA')
 dest=scratch/'extracted';dest.mkdir()
 with zipfile.ZipFile(p/build['verification_zip']['path']) as z:
  names=z.namelist();need(len(names)==152 and len(set(names))==152,'152 unique members')
  for name in names:
   need(not name.startswith('/') and '..' not in Path(name).parts and '\\' not in name,'unsafe ZIP name');target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(name))
 runs=[];anchors=build['verification_anchors'];args=[x for k,v in anchors.items() for x in ['--expected-'+k+'-sha256',v]]
 for flags in [[],['-O'],['-OO']]:
  r=subprocess.run([sys.executable,'-B',*flags,str(dest/'verify.py'),*args],capture_output=True,text=True,timeout=180);need(r.returncode==0,r.stderr);d=json.loads(r.stdout);need(d['authenticated_members']==151,'member count');runs.append({'flags':flags,'result':d})
 # Recreate the actual build inputs from the frozen inventory only. There are
 # no post-build review receipts added to the archive or its context.
 cp=scratch/'rebuild/program/audits/pr1261_30003990';cp.mkdir(parents=True)
 freeze=json.loads((a/'reviews/package_round1/INPUT_FREEZE.json').read_text())
 for e in freeze['files']:
  dst=cp/e['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a/e['path'],dst)
 r=subprocess.run([sys.executable,'-B',str(cp/'publication/build_package.py')],capture_output=True,text=True,timeout=180);need(r.returncode==0,r.stderr)
 rebuilt=(cp/'publication'/build['verification_zip']['path']).read_bytes();need(rebuilt==raw,'exact original152 archive rebuild differs');need((cp/'publication'/build['pdf']['path']).read_bytes()==(p/build['pdf']['path']).read_bytes(),'copied PDF differs')
 return {'outside_zip_sha256':sha(raw),'archive_members':152,'verifier_runs':runs,'exact152_member_archive_rebuild':True,'post_build_records_added':False}
def kit_checks(a,scratch):
 kit=load(Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py'));coord=load(a.parents[1]/'publication_coordinators/pr1261.py');coord.install_exact_verifier(kit);kit.doi_status=lambda d:{'status':'not_checked_offline_review'}
 manifest=(a/'publication/zenodo-deposit.json').resolve();meta,files=kit.load_manifest(manifest);cases=[]
 for changed in [None,*meta]:
  state=scratch/('state-'+str(changed));kit.STATE_DIR=state;place=kit.state_path(manifest,'production');kit.save_state(place,{'manifest':str(manifest),'environment':'production','id':787})
  actual=copy.deepcopy(meta)
  if changed is not None:
   actual[changed]='CORRUPTED' if not isinstance(actual[changed],list) else []
  dep={'id':787,'submitted':False,'metadata':actual,'files':[{'filename':e['name'],'filesize':e['size'],'checksum':'md5:'+e['md5']} for e in files]};events=[]
  class Client:
   def get(self,i):need(i==787,'wrong ID');events.append('GET');return copy.deepcopy(dep)
   def publish(self,i):need(i==787,'wrong POST ID');events.append('POST publish');dep.update(submitted=True,doi='10.5281/zenodo.787')
  try:
   result=kit.run(types.SimpleNamespace(command='publish',manifest=manifest,sandbox=False,confirm_id=787,check_doi=False),client=Client())
   need(changed is None and result['state']=='published' and events.count('POST publish')==1,'changed supplied field published')
  except kit.DepositError:
   need(changed is not None and 'POST publish' not in events,'unexpected failure or POST before rejection')
  cases.append({'changed_supplied_field':changed,'events':events})
 # F01: an exact generic-kit normalization accepted by the original verifier
 # must still be rejected by the installed concrete strict wrapper.
 plain=copy.deepcopy(meta);plain['description']='Synthetic fixture A & B';remote=copy.deepcopy(plain);remote['description']='Synthetic fixture A &amp; B';dep={'metadata':remote,'files':[{'filename':e['name'],'filesize':e['size'],'checksum':'md5:'+e['md5']} for e in files]}
 try:kit.verify(dep,plain,files)
 except kit.DepositError:normalized_rejected=True
 else:raise RuntimeError('F01 normalized description accepted by strict actual verifier')
 return {'actual_shared_kit_run':True,'actual_current_metadata_11_fields':list(meta),'cases':cases,'strict_F01_entity_normalization_rejected':normalized_rejected,'no_live_clients':True}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--audit',type=Path,required=True);ap.add_argument('--scratch',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);q=ap.parse_args();q.audit=q.audit.resolve();q.scratch=q.scratch.resolve();q.scratch.mkdir(parents=True,exist_ok=True)
 d={'status':'PASS','mathematics':math_checks(),'archive':archive_checks(q.audit,q.scratch),'actual_kit':kit_checks(q.audit,q.scratch)};q.output.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({'status':d['status'],'output':str(q.output),'sha256':sha(q.output.read_bytes())}))
if __name__=='__main__':main()
