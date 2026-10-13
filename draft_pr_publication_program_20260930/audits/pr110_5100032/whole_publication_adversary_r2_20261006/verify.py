#!/usr/bin/env python3
"""Fresh R2 custody and independent numerical falsification. Explicit guards survive -O.
Does not write or run in candidate. Immutable output sealing is a separate step.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,os,sys,zipfile,stat
R=Path(__file__).resolve().parent
A=R.parent
P=A/'publication_ready_v1'
N=0

def require(value,label):
 global N
 N+=1
 if not value: raise RuntimeError(label)

def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def close(x,y,tol=2e-8):
 return abs(x-y)<=tol*max(1,abs(x),abs(y))

def authenticate():
 s=A/'publication_ready_v1_SEAL.json';sp=pin(s)
 require(sp['bytes']==6538 and sp['sha256']=='691ae196a8a18472bac50df9202477fb1eb48428091b27258a371fecdfc946c7','external seal bytes')
 seal=json.loads(s.read_text());files=seal['files']
 require(len(files)==34,'34 sealed files')
 require({str(p.relative_to(P)) for p in P.rglob('*') if p.is_file()}=={x['path'] for x in files},'exact candidate file set')
 for f in files:
  p=P/f['path'];q=pin(p)
  require(not p.is_symlink(),'no symlink '+f['path'])
  require(all(q[k]==f[k] for k in ('bytes','sha256')),'sealed member '+f['path'])
 for name in ('PACKAGE_MANIFEST.json','source_payload_manifest.json'):
  j=json.loads((P/name).read_text())
  for f in j['files']:
   q=pin(P/f['path']);require(all(q[k]==f[k] for k in ('bytes','sha256')),'manifest '+f['path'])
 manifest=json.loads((P/'PACKAGE_MANIFEST.json').read_text())
 require({f['path'] for f in manifest['files']}=={f['path'] for f in files}-set(manifest['excluded']),'manifest exclusions exactly documented')
 sums={line.split('  ',1)[1]:line.split('  ',1)[0] for line in (P/'SHA256SUMS').read_text().splitlines()}
 require(set(sums)=={f['path'] for f in files}-{'SHA256SUMS','focal_antipedal_sum_support.zip'},'SHA256SUMS set')
 for name,h in sums.items():require(pin(P/name)['sha256']==h,'sum '+name)
 with zipfile.ZipFile(P/'focal_antipedal_sum_support.zip') as z:
  require(len(z.infolist())==33 and len(set(z.namelist()))==33,'33 unique zip members')
  require(set(z.namelist())=={f['path'] for f in files}-{'focal_antipedal_sum_support.zip'},'zip exact membership')
  require(z.testzip() is None,'ZIP CRC')
  for info in z.infolist():
   require(not info.is_dir() and not info.filename.startswith('/') and '..' not in Path(info.filename).parts,'zip safe relative files')
   require(not stat.S_ISLNK(info.external_attr>>16),'zip no symlinks')
   require(z.read(info.filename)==(P/info.filename).read_bytes(),'zip bytes '+info.filename)
 inputs=json.loads((P/'input_pins.json').read_text())['pins']
 require(len(inputs)==16,'16 research source pins')
 for f in inputs:
  q=pin(A/f['path_relative_to_audit_root']);require(all(q[k]==f[k] for k in ('bytes','sha256')),'input '+f['path_relative_to_audit_root'])
 binding=json.loads((P/'proof_binding.json').read_text());q=pin(P/binding['path'])
 require(all(q[k]==binding[k] for k in ('bytes','sha256')),'manuscript binding')
 sm=json.loads((P/'source_seal_receipt.json').read_text())
 q=pin(P/'source_payload_manifest.json');require(all(sm['source_manifest'][k]==q[k] for k in ('bytes','sha256')),'source receipt manifest binding')
 meta=json.loads((P/'intended_zenodo_metadata.json').read_text())['metadata']
 deposit=json.loads((P/'zenodo-deposit.json').read_text());require(meta==deposit['metadata'],'metadata identical')
 require(meta['title']=='A telescoping proof of the focal antipedal sum invariant','title')
 require(meta['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'creator')
 require(meta['publication_date']=='2026-10-06' and meta['version']=='1.0' and meta['license']=='cc-by-4.0','date/version/license')
 require(deposit['files']==[{'path':'focal_antipedal_sum.pdf'},{'path':'focal_antipedal_sum_support.zip'}],'deposit file plan')
 for stem in ('','root_reproduction/root_'):
  env=json.loads((P/(stem+'execution_envelope.json')).read_text())
  require(len(env['operations'])==10 and env['positive_runs']==2 and env['required_failed_subprocess_controls']==8,'source or root 10-run envelope')
  for op in env['operations']:
   require(op['child_PID']>0 and op['UTC_start']<=op['UTC_end'],'recorded real-process shape')
   if op['invalid_control'] is None:
    result=json.loads((P/(stem+'verification_optimized.json' if op['optimization'] else stem+'verification_normal.json')).read_text())
    require(result['actual_verifier_PID']==op['child_PID'] and op['exit_code']==0,'positive PID/exit')
    require(result['proof_sha256']==binding['sha256'],'executed manuscript')
    require(result['directed_chord_cases']==1456 and result['explicit_passing_guard_checks']==63346,'exact count')
    output=(P/(stem+'verification_optimized.json' if op['optimization'] else stem+'verification_normal.json')).read_bytes()
    require(len(output)==op['stdout']['bytes'] and hashlib.sha256(output).hexdigest()==op['stdout']['sha256'],'positive stream hash')
   else:
    r=op['verified_rejection'];raw=(json.dumps({'status':r['status'],'reason':r['reason'],'actual_verifier_PID':r['actual_verifier_PID'],'optimization_level':r['optimization_level']})+'\n').encode();require(len(raw)==op['stderr']['bytes'] and hashlib.sha256(raw).hexdigest()==op['stderr']['sha256'],'negative stream hash in original output order');require(op['exit_code']==2 and op['stdout']['bytes']==0 and r['actual_verifier_PID']==op['child_PID'] and r['status']=='rejected','negative genuine receipt consistency')
 review_inputs=json.loads((R/'INPUT_PINS.json').read_text())
 for item in review_inputs['primary_and_boundary_inputs']:
  q=pin(Path(item['path']));require(all(q[k]==item[k] for k in ('bytes','sha256')),'R2 primary/boundary input '+item['name'])
 book=json.loads((A/'priority_exact_invariant_history_20261006/IMPA_AUTHOR_SOURCE_CUSTODY.json').read_text())
 base=A/'priority_exact_invariant_history_20261006'/book['private_extraction_root']
 require(len(book['body_rows'])==145,'145 author source files')
 for row in book['body_rows']:
  body=(base/row['path']).read_bytes()
  require(len(body)==row['bytes'] and hashlib.sha256(body).hexdigest()==row['sha256'],'book author-source size/hash '+row['path'])
  require(hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==row['Git_blob_OID'],'book historical Git blob '+row['path'])
 return {'candidate_files':34,'zip_members':33,'input_pins':16,'external_seal':sp,'PDF':pin(P/'focal_antipedal_sum.pdf'),'ZIP':pin(P/'focal_antipedal_sum_support.zip')}

def ellipse_point(a,b,t):return (a*math.cos(t),b*math.sin(t))
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def antipodal_norm(A,B,f):
 U=(A[0]-f,A[1]);V=(B[0]-f,B[1]);d=det(U,V)
 require(abs(d)>1e-13,'noncollinear independent numerical rays')
 r=U[0]**2+U[1]**2;s=V[0]**2+V[1]**2
 Q=((r*V[1]-s*U[1])/d,(U[0]*s-V[0]*r)/d)
 return math.hypot(*Q)
def inspect_edge(a,b,lam,A,B,tol=2e-8):
 c=math.sqrt(a*a-b*b);dx=B[0]-A[0];dy=B[1]-A[1]
 w=det(A,B);orient=1 if w>0 else -1
 l=math.hypot(dx,dy);nx=orient*dy/l;ny=-orient*dx/l;rho=abs(w)/l
 require(rho-c*abs(nx)>0,'both positive heights')
 require(close(rho*rho,(a*a-lam)*nx*nx+(b*b-lam)*ny*ny,tol),'independent tangency')
 qplus=antipodal_norm(A,B,c);qminus=antipodal_norm(A,B,-c)
 gamma=c/(a*b*math.sqrt(lam))*(-a*a+b*b*lam/(b*b-lam))
 require(close(qplus-qminus,orient*gamma*dy,tol),'direct-solver coboundary')
 return qplus,qminus,orient,gamma

def independent_chords():
 worst=0;count=0;horizontal=0;signs=set()
 for a,b in ((math.sqrt(7),1.13),(5.0,3.0),(1.001,1.0),(8.21,0.19)):
  zero=a*a*b*b/(a*a+b*b)
  for lam in (b*b*1e-5,b*b*.2,zero,b*b*.91,b*b*(1-1e-5)):
   # Parameterize the actual caustic contact point, then solve outer intersection trig equation.
   ac=math.sqrt(a*a-lam);bc=math.sqrt(b*b-lam)
   for j in range(81):
    theta=2*math.pi*j/80
    nx=math.cos(theta)/ac;ny=math.sin(theta)/bc
    phase=math.atan2(b*ny,a*nx);delta=math.acos(1/math.hypot(a*nx,b*ny))
    A=ellipse_point(a,b,phase-delta);B=ellipse_point(a,b,phase+delta)
    qp,qm,o,g=inspect_edge(a,b,lam,A,B,3e-6)
    err=abs(qp-qm-o*g*(B[1]-A[1]))/max(1,qp,qm,abs(g*(B[1]-A[1])))
    worst=max(worst,err);signs.add(0 if abs(g)<1e-10 else (1 if g>0 else -1));horizontal+=abs(B[1]-A[1])<1e-10
    rqp,rqm,ro,rg=inspect_edge(a,b,lam,B,A,3e-6)
    require(close(qp,rqp) and close(qm,rqm) and ro==-o,'independent reversal')
    count+=2
 require(signs=={-1,0,1} and horizontal>0,'independent gamma/horizontal coverage')
 return {'directed_edges':count,'horizontal_unoriented':horizontal,'gamma_signs':sorted(signs),'max_relative_norm_difference_residual':worst,'mechanism':'caustic-contact normals, trigonometric outer intersections, direct 2x2 antipedal line solve; floating falsification only'}

def next_vertex(a,b,lam,t):
 A=ellipse_point(a,b,t);ac=math.sqrt(a*a-lam);bc=math.sqrt(b*b-lam)
 ph=math.atan2(A[1]/bc,A[0]/ac);delta=math.acos(1/math.hypot(A[0]/ac,A[1]/bc))
 candidates=[]
 for theta in (ph-delta,ph+delta):
  nx=math.cos(theta)/ac;ny=math.sin(theta)/bc
  dx,dy=-ny,nx
  z=-2*(A[0]*dx/(a*a)+A[1]*dy/(b*b))/(dx*dx/(a*a)+dy*dy/(b*b))
  B=(A[0]+z*dx,A[1]+z*dy)
  if det(A,B)>0:
   angle=math.atan2(B[1]/b,B[0]/a)
   step=(angle-t)%(2*math.pi)
   candidates.append((t+step,B))
 require(len(candidates)==1,'unique caustic-left outgoing edge')
 return candidates[0]

def travel(a,b,lam,N,start=.271):
 t=start;vertices=[ellipse_point(a,b,t)]
 for i in range(N):t,B=next_vertex(a,b,lam,t);vertices.append(B)
 return t-start,vertices

def odd_cycles():
 a,b=5.0,3.0;results=[]
 for n,k in ((3,1),(5,1),(5,2),(7,2),(9,2)):
  lo,hi=1e-7,b*b*(1-1e-8)
  for i in range(75):
   mid=(lo+hi)/2;theta,V=travel(a,b,mid,n)
   if theta<2*math.pi*k:lo=mid
   else:hi=mid
  lam=(lo+hi)/2;theta,V=travel(a,b,lam,n)
  require(abs(theta-2*math.pi*k)<2e-9,'odd/star closure angle')
  closure=math.dist(V[0],V[-1]);require(closure<2e-8,'odd/star closure point')
  plus=minus=0
  for i in range(n):
   qp,qm,o,g=inspect_edge(a,b,lam,V[i],V[i+1]);plus+=qp;minus+=qm
   require(o==1,'same-side propagation genuine cycle')
  err=abs(plus-minus)/max(plus,minus);require(err<2e-9,'odd/star positive norm sum')
  reverse=[V[0]]+list(reversed(V[1:-1]))+[V[0]]
  for i in range(n):inspect_edge(a,b,lam,reverse[i],reverse[i+1])
  results.append({'N':n,'winding':k,'lambda':lam,'closure_distance':closure,'sum_plus':plus,'sum_minus':minus,'relative_sum_residual':err,'star':k>1,'reversal_checked':True,'repeated_traversal_sum_error':3*abs(plus-minus)})
 return results

def invalid_average_transfer():
 # Circle rotation x -> x+2pi/5, g(x)=cos(5x) has zero spatial mean but orbit sum varies.
 values=[sum(math.cos(5*(phase+2*math.pi*j/5)) for j in range(5)) for phase in (0,math.pi/5)]
 require(close(values[0],5) and close(values[1],-5),'explicit rational-rotation average-transfer counterexample')
 return {'spatial_mean':0,'period':5,'two_phase_sums':values,'conclusion':'spatial averages alone do not determine every finite rational-period sum'}

def main():
 started=datetime.now(timezone.utc).isoformat();custody=authenticate();chords=independent_chords();cycles=odd_cycles();average=invalid_average_transfer()
 print(json.dumps({'schema':'pr110-fresh-r2-explicit-guards/v1','status':'passed','actual_PID':os.getpid(),'argv':[sys.executable]+sys.argv,'optimization':sys.flags.optimize,'UTC_start':started,'UTC_end':datetime.now(timezone.utc).isoformat(),'explicit_guards':N,'custody':custody,'independent_chords':chords,'independent_odd_star_cycles':cycles,'invalid_average_transfer_counterexample':average},indent=2))
if __name__=='__main__':main()
