#!/usr/bin/env python3
"""Read-only exact symbolic checks of an independent conformal/static route.
Handwritten derivations establish geometric/test/domain quantifiers. No sampling
or algebra-system output is substituted for those arguments. No source imports.
"""
from pathlib import Path
import hashlib,json,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE/'cache/deps'))
import sympy as S
rows=[];negatives=[]
def ck(name,expr):
 ok=bool(expr);rows.append({'name':name,'passed':ok})
 if not ok:raise RuntimeError(name)
def zero(name,x):ck(name,S.cancel(S.simplify(x))==0)
def nonzero(name,x):
 if S.cancel(S.simplify(x))==0:raise RuntimeError('False claim accepted: '+name)
 negatives.append({'name':name,'false_identity_rejected':True})
def main():
 ck('no arguments',len(sys.argv)==1)
 for name,d in {'sources/SOURCE_READY.json':'aeb11ade749cbe2c6147374642fc3fed6c5d88d323dbae59340b3fb8dfbe4535','sources/regular_zas_bianchi_defect.pdf':'015c034b3ef39044823ebe56291c043f5e96752ac5e0476fde5ac739bef9608a','sources/published-source/manuscript.tex':'fe6aed7b2dc17d3ba20985e184e17fe51b77545365503af7097a611a73608ed0','reviews/analytic/INITIAL_SEAL.json':'0ad8cffdbed41581b6575ea2247a36b1cecb544f15f49768915cd21a78960aab'}.items():ck('input hash '+name,hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==d)
 ck('pinned symbolic dependency',S.__version__=='1.14.0')
 a,rho=S.symbols('a rho',positive=True);A,B=S.symbols('A B',nonnegative=True);E=S.symbols('E',positive=True);gap=S.symbols('x',positive=True)
 phi=1-a/rho;q=(rho+a)/(rho-a);N=A+B*q;r=rho*phi**2
 zero('area coordinate derivative',S.diff(r,rho)-(1-a**2/rho**2))
 zero('lapse main member',(1+q)/2-1/phi)
 zero('area radius static f',q**2-(1+4*a/r))
 zero('flat harmonic definer',S.diff(phi,rho,2)+2*S.diff(phi,rho)/rho)
 zero('simple boundary derivative',S.diff(phi,rho).subs(rho,a)-1/a)
 # Independent conformal Ricci formula, rather than source areal Christoffels.
 pp=S.diff(phi,rho);ppp=S.diff(phi,rho,2)
 Rrad=S.cancel(phi**-4*(-2*ppp/phi+4*pp**2/phi**2))
 Rtan=S.cancel(phi**-4*(-2*pp/(rho*phi)-2*pp**2/phi**2))
 zero('conformal radial Ricci',Rrad-4*a/r**3);zero('conformal tangential Ricci',Rtan+2*a/r**3);zero('spatial scalar curvature',Rrad+2*Rtan)
 def Hess(u):return [phi**-4*(S.diff(u,rho,2)-2*pp*S.diff(u,rho)/phi),phi**-4*(S.diff(u,rho)/rho+2*pp*S.diff(u,rho)/phi)]
 Hq=Hess(q);HN=Hess(N)
 for i,v in enumerate([Rrad,Rtan]):zero('vacuum Hessian '+str(i),Hq[i]-q*v);zero('affine Hessian '+str(i),HN[i]-B*q*v)
 zero('vacuum lapse harmonic',Hq[0]+2*Hq[1]);zero('all affine lapses harmonic',HN[0]+2*HN[1])
 G=[S.cancel(Rrad-HN[0]/N),S.cancel(Rtan-HN[1]/N)]
 for i,v in enumerate([Rrad,Rtan]):zero('affine Einstein '+str(i),G[i]-A*v/N)
 D=[S.cancel(N*phi**6*v) for v in G]
 zero('radial weighted density',D[0]-4*A*a/rho**3);zero('tangential weighted density',D[1]+2*A*a/rho**3);zero('weighted trace',D[0]+2*D[1]);zero('weighted divergence',S.diff(D[0],rho)+2*(D[0]-D[1])/rho)
 # Full connection contraction vanishes in every direction, modulo n.n=1.
 n=S.symbols('n0:3',real=True);DD=S.Matrix(3,3,lambda i,j:A*a/rho**3*(6*n[i]*n[j]-2*int(i==j)))
 grad=[a*v/rho**2 for v in n]
 for k in range(3):
  T=sum(DD[i,j]*2/phi*(int(j==i)*grad[k]+int(j==k)*grad[i]-int(i==k)*grad[j]) for i in range(3) for j in range(3))
  num=S.together(T).as_numer_denom()[0]
  zero('generic Cartesian connection '+str(k),S.Poly(num,n[2]).rem(S.Poly(n[2]**2+n[0]**2+n[1]**2-1,n[2])).as_expr())
 main=[v.subs({A:S.Rational(1,2),B:S.Rational(1,2)}) for v in G]
 zero('main radial Einstein',main[0]-2*a/(rho**3*phi**5));zero('main tangential Einstein',main[1]+a/(rho**3*phi**5))
 inv=S.cancel(main[0]**2+2*main[1]**2);zero('Ricci invariant',inv-6*a**2/(rho**6*phi**10))
 zero('borderline Einstein coefficient',S.limit(gap**5*main[0].subs(rho,a+gap),gap,0,dir='+')-2*a**3)
 zero('curvature blowup coefficient',S.limit(gap**10*inv.subs(rho,a+gap),gap,0,dir='+')-6*a**6)
 zero('vacuum radial control',G[0].subs(A,0));zero('vacuum tangential control',G[1].subs(A,0))
 # An arbitrary symbolic radial coefficient, never a sampled bump.
 chi=S.Function('chi')(rho);radial=S.cancel(rho**2*(D[0]*S.diff(chi,rho)+2*D[1]*chi/rho))
 zero('full radial density as derivative',radial-4*A*a*S.diff(chi/rho,rho))
 flux=-4*A/a**2*4*S.pi*a**2
 zero('normalized family flux',flux+16*S.pi*A);zero('normalized main flux',flux.subs(A,S.Rational(1,2))+8*S.pi)
 mass=-S.Rational(1,4)*(4*a**S.Rational(2,3))**S.Rational(3,2)
 zero('regular ZAS mass',mass+2*a)
 c=S.symbols('c',positive=True);tilted=-S.Rational(1,4)*(4*a**S.Rational(2,3)*c**S.Rational(-2,3))**S.Rational(3,2)
 zero('uniform tilt mass',tilted+2*a/c)
 zero('radial null slope',-phi**-2*phi**6+phi**4)
 affine=(rho-a-a*S.log(rho/a))/E
 zero('null affine primitive',S.diff(affine,rho)-phi/E)
 zero('null affine leading coefficient',S.limit(affine.subs(rho,a+gap)/gap**2,gap,0,dir='+')-1/(2*a*E))
 zero('conformal radial distance coefficient',S.limit(phi.subs(rho,a+gap)**3/gap**3,gap,0,dir='+')-1/a**3)
 zero('boundary areal coordinate degenerates',S.limit(S.diff(r,rho),rho,a,dir='+'))
 # These deliberately wrong identities must have exact nonzero residuals.
 nonzero('wrong weak-flux sign',16*S.pi*A-flux)
 nonzero('vacuum claimed nonzero',S.Integer(1)-G[0].subs(A,0))
 nonzero('missing area factor',-4*A/a**2-flux)
 nonzero('wrong main lapse',q-1/phi)
 nonzero('wrong null slope phi squared',-phi**-2*phi**4+phi**4)
 nonzero('wrong radial Ricci sign',Rrad+4*a/r**3)
 nonzero('wrong main Einstein power',main[0]-2*a/(rho**3*phi**4))
 nonzero('areal boundary map claimed nonsingular',S.limit(S.diff(r,rho),rho,a,dir='+')-1)
 out={'assessment':'EXACT_INDEPENDENT_CONFORMAL_STATIC_IDENTITIES_SUPPORTED','symbolic_dependency':S.__version__,'exact_checks':len(rows),'false_identities_rejected':len(negatives),'checks':rows,'negative_controls':negatives,'scope':'Generic exact rational/symbolic identities; handwritten analytic proof and authenticated primary test/geometry interfaces are essential. No source program imported, no source or output file written.','optimized':not __debug__}
 print(json.dumps(out,sort_keys=True,indent=2))
if __name__=='__main__':main()
