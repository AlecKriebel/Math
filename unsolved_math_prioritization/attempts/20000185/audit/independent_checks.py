#!/usr/bin/env python3
"""Independent exact adversarial controls. Does not import the author verifier.
Usage: python independent_checks.py [packet_directory]
Requires Python 3 and SymPy. Writes JSON to stdout; input bytes are read-only.
"""
from pathlib import Path
import hashlib, itertools, json, math, sys
import sympy as S

ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'submission'
EXPECTED_FREEZE='43286aeaa36c1e27b4ccfe7ef1a002f26e3dad3f56cce702c0b654a2eba05698'
EXPECTED_PROOF='488a29cd89d119140b23c7653933416d84935ab2a5201c90895f052316a89c36'
assertions=0

def ck(x,msg):
 global assertions
 assertions+=1
 if not x: raise AssertionError(msg)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def bind():
 freeze=ROOT.parent/'FREEZE_MANIFEST.json'
 ck(sha(freeze)==EXPECTED_FREEZE,'external freeze digest')
 ck(sha(ROOT/'PROOF.md')==EXPECTED_PROOF,'proof digest')
 m=json.loads(freeze.read_text())
 ck({p.name for p in ROOT.iterdir() if p.is_file()}=={e['path'] for e in m['files']},'exact eleven files')
 for e in m['files']:
  p=ROOT/e['path'];ck(p.stat().st_size==e['bytes'],e['path']+' bytes');ck(sha(p)==e['sha256'],e['path']+' hash')
 return {'freeze_sha256':sha(freeze),'proof_sha256':sha(ROOT/'PROOF.md'),'file_count':len(m['files'])}

a,b,s,t,u,v,w,z,k=S.symbols('a b s t u v w z k')

def order(poly,var):
 terms=S.Poly(poly,var).terms()
 ck(bool(terms) and poly!=0,'nonzero polynomial for valuation')
 return min(e[0][0] for e in terms)

def resultant_length(f,g):
 # Both polynomials have constant nonzero leading t coefficient. At s=0,
 # gcd must be a power of t, excluding remote common points on that fiber.
 K=S.QQ.frac_field(z)
 ff=S.Poly(f,t,domain=K.poly_ring(s));gg=S.Poly(g,t,domain=K.poly_ring(s))
 ck(not ff.LC().has(s) and not gg.LC().has(s),'projection finite at s=0')
 fiber_gcd=S.gcd(S.Poly(f.subs(s,0),t,domain=K),S.Poly(g.subs(s,0),t,domain=K)).monic()
 ck(len(fiber_gcd.terms())==1,'only common point over s=0 is origin')
 R=S.resultant(f,g,t)
 length=order(R,s)
 return length, str(S.factor(R))

def reported_lengths():
 out=[]
 for m,n,i,j,expected in [(2,2,0,0,2),(2,2,0,1,1),(3,3,1,0,5),(3,4,2,1,7),(4,5,1,3,14)]:
  f=s**i*t**(m-1-i)-s**m-t**m
  g=z*s**j*t**(n-1-j)-s**n-2*t**n
  length,R=resultant_length(f,g)
  ck(length==expected,'independent resultant length')
  out.append({'m':m,'n':n,'i':i,'j':j,'length':length,'resultant':R})
 return out

def local_orders():
 count=0
 for U,V in itertools.product(range(13),repeat=2):
  for x in ([0] if U else range(4)):
   for y in ([0] if V else range(4)):
    for os,ot in itertools.product(range(4),repeat=2):
     if min(os,ot):continue
     raw=[x+V,y+U,U+V+os,U+V+ot]
     cancelled=min(raw);world=[p-cancelled for p in raw]
     ck(cancelled==min(U,V),'raw four-section base order')
     ck(min(world[0],world[2],world[3])==max(V-U,0),'P fixed order')
     ck(min(world[1],world[2],world[3])==max(U-V,0),'Q fixed order')
     ck(min(world[2],world[3])==max(U,V),'baseline fixed order')
     count+=1
 return {'local_valuation_patterns':count,'coefficient_range':[0,12]}

def toric_covers():
 # X=[v^m:u^m:u^(m-r)v^r], so f=a^r*s^(m-r)-t^m.
 # gcd(m,r)=1 makes this parametrization birational and f irreducible.
 out=[]
 pairs=[(3,2,4,3),(5,2,7,4),(5,3,7,3),(7,4,5,2),(4,3,5,2),(5,4,7,6)]
 for m,r,n,q in pairs:
  ck(math.gcd(m,r)==math.gcd(n,q)==1,'primitive image monomials')
  h=math.gcd(r,q);N=r*q//h;A=(m-r)*q//h;B=(n-q)*r//h
  f=s**(m-r)-t**m;g=z**q*s**(n-q)-t**n
  length,R=resultant_length(f,g)
  predicted=(m-r)*(n-q)+h*min(A,B)
  ck(length==predicted,'ramified overlap local length')
  delta=N+max(A,B)
  # World image monomial coordinate exponents on each normalized component.
  # Original common homogeneous degree N+A+B; cancellation min(A,B) at u=0.
  ds=N+A+B
  raw=[v**(m*q//h)*u**B,v**(n*r//h)*u**A,u**(A+B+N),u**(A+B)*v**N]
  common=S.gcd_list(raw);reduced=[S.cancel(p/common) for p in raw]
  ck(all(S.Poly(p,u,v).total_degree()==delta for p in reduced),'world homogeneous degree')
  exps=[S.Poly(p,u,v).monoms()[0][0] for p in reduced]
  exponent_gcd=math.gcd(*[abs(i-exps[0]) for i in exps[1:]])
  ck(exponent_gcd==1,'world monomial map birational')
  ck(h*delta+length==m*n,'ramified Bezout degrees')
  ck(delta-max(B-A,0)==m*q//h,'ramified first-center correction')
  ck(delta-max(A-B,0)==n*r//h,'ramified second-center correction')
  out.append({'m':m,'r':r,'n':n,'q':q,'components':h,'each_component_degree':delta,'baseline_length':length,'normalized_divisor_orders':[A,B],'resultant':R})
 return out

def multi_branch():
 E=(u-v)*(u+v)*(u-2*v);F=(u-v)**2*(u+v)*(u-3*v)
 X=u**4+v**4;Y=u**5+2*v**5
 ck(S.gcd(X,E)==S.gcd(Y,F)==1,'image triples basepoint free')
 raw=[X*F,Y*E,E*F*u,E*F*v]
 common=S.gcd_list(raw)
 ck(S.Poly(common,u,v).total_degree()==2,'overlap two distinct branches')
 reduced=[S.cancel(c/common) for c in raw]
 ck(all(S.Poly(c,u,v).total_degree()==6 for c in reduced),'multiple-branch degree six')
 f=E.subs({u:s,v:t})-X.subs({u:s,v:t});g=z*F.subs({u:s,v:t})-Y.subs({u:s,v:t})
 length,R=resultant_length(f,g)
 ck(length==14,'multiple-branch baseline length fourteen')
 return {'image_degrees':[4,5],'moving_degrees':[1,1],'overlap_degree':2,'world_degree':6,'baseline_length':length,'resultant':R}

def hilbert_degree(gens):
 G=S.groebner(gens,a,b,s,t,order='grevlex')
 lms=[p.LM(order=G.order).exponents for p in G.polys]
 # Hilbert numerator from exact inclusion-exclusion on leading monomial ideals.
 # The coefficient of (1-x)^2 equals the curve degree in four variables.
 P=0
 for mask in range(1<<len(lms)):
  chosen=[lms[i] for i in range(len(lms)) if mask>>i&1]
  d=sum(max(e[j] for e in chosen) for j in range(4)) if chosen else 0
  P+=(-1)**len(chosen)*k**d
 P=S.expand(P)
 ck(P.subs(k,1)==0 and S.diff(P,k).subs(k,1)==0,'curve Hilbert numerator has order at least two')
 D=S.diff(P,k,2).subs(k,1)/2
 ck(D>0,'curve Hilbert degree positive')
 return int(D),str(P)

def saturate_baseline(gens):
 c,d=S.symbols('c d')
 G=S.groebner([*gens,1-c*s-d*t],c,d,a,b,s,t,order='lex')
 return [p.as_expr() for p in G.polys if not p.as_expr().has(c,d)]

def ideals_equal(first,second):
 G1=S.groebner(first,a,b,s,t,order='lex');G2=S.groebner(second,a,b,s,t,order='lex')
 return all(G1.reduce(p)[1]==0 for p in second) and all(G2.reduce(p)[1]==0 for p in first)

def ideal_intersection(first,second):
 lam=S.Symbol('lam')
 G=S.groebner([lam*p for p in first]+[(1-lam)*p for p in second],lam,a,b,s,t,order='lex')
 return [p.as_expr() for p in G.polys if not p.as_expr().has(lam)]

def mixed_component_degrees():
 # A single irreducible rational quartic has two epipole branches and a
 # degree-two pencil. Its self fiber product has diagonal and antidiagonal.
 E=(u-v)*(u-2*v);X=u**4+u**3*v+v**4
 R=S.resultant(a*E.subs(v,1)-t*X.subs(v,1),s-t*u*u,u)
 coeff,factors=S.factor_list(R)
 candidates=[p for p,e in factors if p.has(a)]
 ck(len(candidates)==1,'one implicit image factor')
 f=candidates[0]
 ck(S.Poly(f,a,s,t).total_degree()==4,'implicit quartic degree')
 ck(S.expand(f.subs({a:X,s:E*u*u,t:E*v*v},simultaneous=True))==0,'quartic parametrization')
 ck(S.gcd_list([X,E*u*u,E*v*v])==1,'quartic basepoint freeness')
 # Distinguish u and -u generically: fixed field of u -> -u is k(u^2).
 ratio=X.subs(v,1)/E.subs(v,1)
 ck(S.cancel(ratio-ratio.subs(u,-u))!=0,'degree-two cover image parametrization birational')
 F=E.subs(u,-u);Y=X.subs(u,-u)
 raw=[X*F,Y*E,E*F*u*u,E*F*v*v]
 ck(S.Poly(S.gcd_list(raw),u,v).total_degree()==0,'antidiagonal no overlap')
 ck(all(S.Poly(p,u,v).total_degree()==6 for p in raw),'antidiagonal world degree six')
 # The world map has a degree-two pencil and is not invariant under u -> -u;
 # hence it is birational onto its image.
 ck(S.cancel(raw[0].subs(v,1)/raw[3].subs(v,1)-(raw[0]/raw[3]).subs({u:-u,v:1},simultaneous=True))!=0,'antidiagonal world map birational')
 sat=saturate_baseline([f,f.subs(a,b)])
 degree,numerator=hilbert_degree(sat)
 ck(degree==10,'saturated union degree ten')
 diagonal=[a-b,f]
 divided=S.cancel((f-f.subs(a,b))/(a-b))
 ghost=saturate_baseline([f,divided])
 diag_degree,diag_num=hilbert_degree(diagonal)
 ghost_degree,ghost_num=hilbert_degree(ghost)
 ck(diag_degree==4 and ghost_degree==6,'separate component Hilbert degrees')
 ck(ideals_equal(sat,ideal_intersection(diagonal,ghost)),'saturated ideal equals component intersection')
 for p in ghost:
  ck(S.expand(p.subs(dict(zip((a,b,s,t),raw)),simultaneous=True))==0,'ghost equations vanish on antidiagonal parametrization')
 # For this example the leading coefficients in t are constants even after
 # a=1,b=z; use the origin-fiber resultant to recover the baseline length.
 length,Rloc=resultant_length(f.subs(a,1),f.subs(a,z))
 ck(length==6,'quartic baseline length six')
 ck(degree+length==16,'quartic complete intersection degree sixteen')
 return {'implicit_image_equation':str(f),'image_degrees':[4,4],'moving_degrees':[2,2],'world_component_degrees':[4,6],'saturated_union_degree':degree,'component_intersection_verified':True,'separate_component_hilbert_degrees':[diag_degree,ghost_degree],'hilbert_numerator':numerator,'baseline_length':length,'saturated_generators':[str(p) for p in sat],'local_resultant':Rloc}

out={'binding':bind(),'reported_lengths_independently_by_resultants':reported_lengths(),'valuation_orders':local_orders(),'ramified_toric_covers':toric_covers(),'multiple_epipole_branches':multi_branch(),'mixed_component_degrees':mixed_component_degrees()}
out.update({'status':'PASS','assertions':assertions,'sympy':S.__version__,'scope':'Finite independent controls and hash binding; not a formal universal proof or novelty certification.'})
print(json.dumps(out,indent=2,sort_keys=True))
