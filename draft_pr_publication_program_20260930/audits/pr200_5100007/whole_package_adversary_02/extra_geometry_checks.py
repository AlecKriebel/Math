from pathlib import Path
import json
import sympy as s
import mpmath as m

def require(c,label):
 if not c:raise RuntimeError(label)

sqrt=s.sqrt; a=s.Integer(3);b=s.Integer(1);c=sqrt(8);l=s.Rational(9,16)
fixtures=[[(3,0),(s.Rational(9,4),sqrt(7)/4),(-s.Rational(9,4),sqrt(7)/4)],[(0,1),(-3*sqrt(15)/4,s.Rational(1,4)),(-3*sqrt(15)/4,-s.Rational(1,4))]]
values=[]
for half,expected in zip(fixtures,[s.Rational(20736,343),s.Rational(6912,125)]):
 pts=[s.Matrix(p) for p in half]+[-s.Matrix(p) for p in half];outer=[]
 for j,P in enumerate(pts):
  prev=pts[(j-1)%6];Q=pts[(j+1)%6]
  require(s.simplify(P[0]**2/9+P[1]**2-1)==0,'boundary')
  vin=P-prev;vout=Q-P;vin=vin/sqrt(vin.dot(vin));vout=vout/sqrt(vout.dot(vout));normal=s.Matrix([P[0]/9,P[1]])
  require(all(s.simplify(x)==0 for x in vin-2*(vin.dot(normal))*normal/normal.dot(normal)-vout),'cyclic reflection including closure')
  line=s.Matrix([P[0],P[1],1]).cross(s.Matrix([Q[0],Q[1],1]));nx,ny,offset=line
  require(s.simplify((9-l)*nx*nx+(1-l)*ny*ny-offset*offset)==0,'same caustic tangency')
  point=s.Matrix([[P[0]/9,P[1]],[Q[0]/9,Q[1]]]).inv()*s.ones(2,1)
  outer.append(point)
 require(len(set(tuple(p) for p in pts))==6,'primitive vertices')
 square=s.Integer(1)
 for P in outer[:3]:
  x,y=P;square*=s.expand(((x-c)**2+y*y)*((x+c)**2+y*y))
 square=s.simplify(square);require(square==expected**2,'exact ordinary product square')
 values.append({'ordinary_positive_product':str(expected),'square':str(square),'all_six_cyclic_reflections':True,'outer_vertices':[[str(s.simplify(v)) for v in p] for p in outer]})
m.mp.dps=105;div=[]
for kt in ('0.4','0.9'):
 k=m.mpf(kt);par=k*k;K=m.ellipk(par);Kp=m.ellipk(1-par);p=m.j*Kp
 for N,tau in [(4,1),(5,1),(6,1),(8,1),(8,3),(10,3),(12,5)]:
  delta=4*K*tau/N
  sn=lambda u:m.ellipfun('sn',u,par)
  dn=lambda u:m.ellipfun('dn',u,par)
  cn=lambda u:m.ellipfun('cn',u,par)
  def H(u):return dn(u)**2*(dn(delta)**2-par*cn(delta)**2*sn(u)**2)
  eps=m.mpf('1e-12');pole_order=2 if N==4 else 4
  observed=-m.log(abs(H(p+2*eps)/H(p+eps)),2)
  require(abs(observed-pole_order)<m.mpf('1e-9'),'complex pole order')
  locations=[(p+K,2)] if N==4 else [(p+K,2),(p+K+delta,1),(p+K-delta,1)]
  zero_orders=[]
  for z,order in locations:
   measured=m.log(abs(H(z+2*eps)/H(z+eps)),2)
   require(abs(measured-order)<m.mpf('1e-9'),'complex zero multiplicity')
   zero_orders.append(m.nstr(measured,15))
  div.append({'k':kt,'N':N,'tau':tau,'pole_order':m.nstr(observed,15),'zero_orders':zero_orders})
result={'status':'PASS','exact_N6':values,'complex_divisor_cases':div,'numerics_are_diagnostics':True}
Path('EXTRA_GEOMETRY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','cyclic_reflection_fixtures':2,'complex_divisor_cases':len(div)}))
