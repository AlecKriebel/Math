#!/usr/bin/env python3
"""Independent reaction-derived audit; imports no project code/certificates.
Exact algebra and exhaustive finite regressions supplement the all-m human proof.
Checks use explicit exceptions and cannot disappear under python -O.
"""
import itertools as it
import json,time
from pathlib import Path
import sympy as s
START=time.time();COUNTS={};RECORDS=[]
def check(v,tag,detail=''):
 if not bool(v):raise RuntimeError(f'{tag}: {detail}')
 COUNTS[tag]=COUNTS.get(tag,0)+1
def record(label,**kw):
 row=dict(label=label,**kw);RECORDS.append(row);print(json.dumps(row),flush=True)
def model(m,a=s.Integer(1),b=s.Integer(1)):
 names=[f'X{i}' for i in range(1,m+1)]+['Z'];x=s.symbols(' '.join(names))
 rxns=[({}, {'X1':1})]
 rxns += [({'X1':1,f'X{i}':1},{'X1':1,f'X{i+1}':1}) for i in range(2,m-1)]
 rxns += [({'X1':1,f'X{m-1}':1},{f'X{m}':2}),({f'X{m}':2},{'X2':1}),({'Z':2},{'X1':1,f'X{m}':1}),({'X1':1,f'X{m}':1},{'Z':2})]
 Y=s.Matrix([[src.get(n,0) for src,dst in rxns] for n in names])
 G=s.Matrix([[dst.get(n,0)-src.get(n,0) for src,dst in rxns] for n in names])
 f=s.zeros(m+1,1);weights=[a]*m+[b,b]
 for j,(src,dst) in enumerate(rxns):
  check(sum(src.values())<=2 and sum(dst.values())<=2,'binary_complex')
  f+=G[:,j]*weights[j]*s.prod(x[i]**Y[i,j] for i in range(m+1))
 A=f.jacobian(x).subs(dict.fromkeys(x,s.Integer(1)))
 return G,Y,x,f,A
def minor(J,I):return s.Integer(1) if not I else s.factor((-1)**len(I)*J.extract(I,I).det(method='domain-ge'))
def hurwitz(M):
 cs=M.charpoly().all_coeffs();n=M.rows
 for k in range(1,n+1):
  H=s.Matrix(k,k,lambda i,j:cs[2*j-i+1] if 0<=2*j-i+1<=n else 0)
  if H.det(method='domain-ge')<=0:return False
 return True
def components(A,I):
 I=list(I);n=len(I)
 R=[sum(1<<j for j in range(n) if i==j or A[I[j],I[i]]!=0) for i in range(n)]
 for k in range(n):
  for i in range(n):
   if R[i]&(1<<k):R[i]|=R[k]
 left=set(range(n));out=[]
 while left:
  i=min(left);C={j for j in left if R[i]&(1<<j) and R[j]&(1<<i)}
  out.append(tuple(I[j] for j in sorted(C)));left-=C
 return out
def structural():
 a,b=s.symbols('a b',positive=True)
 for m in range(3,10):
  G,Y,x,f,A=model(m,a,b);c=s.Matrix([0]+[4]*(m-2)+[2,1])
  E=s.Matrix.hstack(s.Matrix([1]*m+[0,0]),s.Matrix([0]*m+[1,1]))
  check(G.shape==(m+1,m+2),'reaction_count');check(G.rank()==m,'rank')
  check(c.T*G==s.zeros(1,m+2),'conservation');check(G*E==s.zeros(m+1,2) and E.rank()==2,'kernel_basis')
  check(G.extract([0]+list(range(2,m+1)),list(range(1,m+1))).det()==4*(-1)**m,'selected_rank_minor')
  B=s.zeros(m+1)
  entries={(0,0):-a-b,(0,m-2):-a,(0,m-1):-b,(0,m):2*b,(1,0):-a,(1,1):-a,(1,m-1):2*a,(m-1,0):2*a-b,(m-1,m-2):2*a,(m-1,m-1):-4*a-b,(m-1,m):2*b,(m,0):2*b,(m,m-1):2*b,(m,m):-4*b}
  for i in range(2,m-1):entries[(i,i-1)]=a;entries[(i,i)]=-a
  for ij,v in entries.items():B[ij]=v
  check(A==B,'displayed_jacobian');check(A*s.Matrix([2]+[-2]*(m-2)+[0,1])==s.zeros(m+1,1),'right_nullvector')
  for omit in range(m+1):
   I=[i for i in range(m+1) if i!=omit];want=0 if omit in (0,m-1) else (-2 if omit==m else 16)*a**(m-1)*b
   check(minor(A,I)==want,'symbolic_omission',(m,omit))
  if m<=6:
   hs=s.symbols('h0:'+str(m+1),positive=True);H=s.diag(*hs)
   fp=f.subs(dict(zip(x,[h*xi for h,xi in zip(hs,x)])),simultaneous=True);eq=dict(zip(x,[1/h for h in hs]))
   check(fp.subs(eq)==s.zeros(m+1,1),'arbitrary_equilibrium')
   check(s.simplify(fp.jacobian(x).subs(eq)-A*H)==s.zeros(m+1),'all_realizations')
  record('symbolic_structure',m=m)
 h1,hm,hz=s.symbols('h1 hm hz',positive=True)
 A=model(4,a,b)[4];T=A.extract([0,3,4],[0,3,4])*s.diag(h1,hm,hz);cs=T.charpoly().all_coeffs()
 check(s.expand(cs[1]-(a+b)*h1-(4*a+b)*hm-4*b*hz)==0,'triad_c1')
 check(s.expand(cs[2]-a*(4*a*h1*hm+7*b*h1*hm+4*b*h1*hz+16*b*hm*hz))==0,'triad_c2')
 check(s.expand(cs[3]-16*a*a*b*h1*hm*hz)==0,'triad_c3')
 gap=s.Poly(s.expand((cs[1]*cs[2]-cs[3])/a),a,b,h1,hm,hz)
 check(len(gap.terms())==14 and all(v>0 for _,v in gap.terms()),'triad_routh_positive')
 for I in it.combinations(range(3),2):
  M=T.extract(I,I)
  check(all(v>0 for _,v in s.Poly(-s.trace(M),a,b,h1,hm,hz).terms()),'triad_pair_trace')
  check(all(v>0 for _,v in s.Poly(M.det(),a,b,h1,hm,hz).terms()),'triad_pair_determinant')
 record('triad_certificate',positive_gap_terms=len(gap.terms()))
def exhaustive():
 for m in range(3,13):
  for b in (s.Integer(1),s.Integer(2),s.Integer(3)):
   A=model(m,s.Integer(1),b)[4];J=A*s.diag(*[s.Rational(2*i+3,i+2) for i in range(m+1)])
   allowed=[set(range(m-1)),set(range(1,m))];boundary={0,m-1,m};seen=set();sets=0
   for k in range(1,m):
    for I in it.combinations(range(m+1),k):
     sets+=1
     for comp in components(A,I):
      C=set(comp);check(len(C)==1 or C<=boundary or C in allowed,'scc_exhaustion',(m,b,I,comp))
      if comp not in seen:
       check(hurwitz(J.extract(comp,comp)),'exact_scc_hurwitz',(m,b,comp));seen.add(comp)
     if m<=6:check(hurwitz(J.extract(I,I)),'exact_entire_subsystem_hurwitz',(m,b,I))
   record('exhaustive_graph',m=m,b=str(b),principal_sets=sets,unique_blocks=len(seen))
def homogeneous_contrast():
 lam=s.symbols('lam');P=lam**4+12*lam**3+42*lam**2+47*lam+16;R=5*lam**2+33*lam+16
 for m in range(3,14):
  chi=model(m)[4].charpoly(lam).as_expr()
  check(s.expand(chi-(1+lam)**(m-3)*P+R)==0,'homogeneous_determinant')
  check(s.expand(chi).coeff(lam)==16*m-34,'homogeneous_simple_zero')
 x,y,z=s.symbols('x y z',real=True)
 def modulus(p):
  p=s.expand(p.subs(lam,x+s.I*y));return s.expand(p*s.conjugate(p))
 expr=s.Poly(s.expand(((1+x)**2+y*y)*modulus(P)-modulus(R)),x,y)
 check(all(i[1]%2==0 for i,c in expr.terms()),'homogeneous_even_y')
 cert=s.Poly(sum(c*x**i[0]*z**(i[1]//2) for i,c in expr.terms()),x,z)
 check(len(cert.terms())==35 and all(c>0 for i,c in cert.terms()),'homogeneous_positive_certificate')
 check(cert.coeff_monomial(x)>0 and cert.coeff_monomial(z)>0 and cert.coeff_monomial(1)==0,'homogeneous_equality_only_origin')
 record('homogeneous_certificate',positive_monomials=len(cert.terms()))
 for m in list(range(3,31))+[50,100,1000]:
  nu=m-2;K=lambda i:91*m-181-i
  unit=[s.Rational(23,63)]+[s.Rational(1,K(i)) for i in range(2,m)]+[s.Rational(1,7),s.Rational(16,45)]
  check(max(unit)/min(unit)==s.Rational(23,63)*(91*m-183),'unit_contrast')
  L0=1/s.sqrt(3) if nu==1 else s.sqrt(s.Rational(5,4*nu));L1=s.Rational(90*nu,90*nu+1)
  check(L0<L1,'tradeoff_interval')
  for L in (L0,(L0+L1)/2,L1):
   h=[s.Integer(1)]+[s.Rational(K(i),K(i-1))/L for i in range(2,m)]+[s.Integer(1),s.Integer(1)]
   d=[hi*di for hi,di in zip(h,unit)];cd=s.simplify(max(d)/min(d));ch=s.simplify(max(h)/min(h))
   check(s.simplify(cd-s.Rational(23,63)*91*nu*L)==0,'physical_diffusion_contrast')
   check(s.simplify(ch-(91*nu-1)/(91*nu*L))==0,'equilibrium_contrast')
   check(s.simplify(cd*ch-s.Rational(23,63)*(91*nu-1))==0,'contrast_product');check(cd>ch,'minimax_order')
 record('contrast_regressions',dimensions=31,max_m=1000)
def diffusion():
 z,lam=s.symbols('z lam',real=True);J=s.Matrix([[1,-2],[1,-2]])
 for dz in (1,2,3):
  D=s.diag(1,dz);p=s.expand((z*D-J).det());chi=s.expand((lam*s.eye(2)+z*D-J).det())
  check(s.expand(p-z*(2-dz+dz*z))==0,'abstract_n2_boundary')
  check(s.expand(s.diff(chi,lam)-2*lam-(1+dz)*z-1)==0,'abstract_n2_characteristic_derivative')
 record('abstract_n2',diffusivities_Z=[1,2,3],positive_threshold_for_Z_3='1/3')
 for m in range(3,7):
  A=model(m)[4]
  for hs in ([s.Integer(1)]*(m+1),[s.Rational(i+2,i+1) for i in range(m+1)]):
   J=A*s.diag(*hs)
   for eps in (-s.Rational(1,2),s.Integer(0),s.Rational(1,2)):
    ds=[s.Integer(1)]*(m+1);T=8*hs[-1]*sum(1/h for h in hs[1:m-1]);ds[-1]=T+eps
    p=s.Poly((z*s.diag(*ds)-J).det(method='domain-ge'),z);bs=[]
    for k in range(1,m+2):
     beta=sum(minor(J,I)*s.prod(ds[j] for j in range(m+1) if j not in I) for I in it.combinations(range(m+1),m+1-k));bs.append(s.factor(beta))
     check(s.simplify(beta-p.coeff_monomial(z**k))==0,'diffusion_minor_expansion')
    check(all(v>0 for v in bs[1:]),'diffusion_higher_coefficients')
    check(s.simplify(bs[0]+2*s.prod(hs[:m])*eps)==0,'diffusion_exact_boundary_sign')
    if m<=4:
     chi=(lam*s.eye(m+1)+z*s.diag(*ds)-J).det(method='domain-ge');der=s.Poly(s.diff(chi,lam),lam,z)
     check(all(v>0 for _,v in der.terms()),'characteristic_derivative_positive')
   record('exact_diffusion_boundary',m=m,H='unit' if all(h==1 for h in hs) else 'rational')
def main():
 structural();exhaustive();homogeneous_contrast();diffusion()
 out=dict(status='PASS',elapsed_seconds=time.time()-START,checks=COUNTS,records=RECORDS,sympy_version=s.__version__,no_project_imports=True)
 Path(__file__).with_name('independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k!='records'}),flush=True)
if __name__=='__main__':main()
