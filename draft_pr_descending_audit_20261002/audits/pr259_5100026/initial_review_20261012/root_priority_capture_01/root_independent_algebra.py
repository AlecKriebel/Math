"""Root independently derives raw focal pair and curve identities; library only."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json
V=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr261_5100021/initial_review_20261012/reproduction_source_adversary/vendor');sys.path.insert(0,str(V))
import sympy as s
O=Path(__file__).resolve().parent;results={}
def zero(name,expr):
    z=s.factor(s.cancel(expr));assert z==0,(name,z);results[name]=str(z)
h,f,g,r,t,B,lam=s.symbols('h f g r t B lam',nonzero=True)
X=s.Matrix([h,r]);Y=s.Matrix([h,t]);F=s.Matrix([f,g])
def I(X,Y):
    q=X-F;v=Y-F;return s.Matrix([list(q),list(v)]).inv()*s.Matrix([q.dot(X),v.dot(Y)])
Q=I(X,Y);Qopp=I(-X,-Y)
zero('raw_pair_tangent',(Q+Qopp)[1]+2*g)
zero('raw_pair_normal',(Q+Qopp)[0]-(2*h*g*(r+t)-2*f*(r*t+g*g))/(h*h-f*f))
a2=B+f*f+g*g;alpha=(B-lam)/B**2;beta=(lam*(a2+B)-a2*B)/(a2**2*B**2);kap=alpha+lam/(a2*B);den=alpha+beta*g*g
sumrt=-2*h*beta*f*g/den;prodrt=(h*h*(alpha+beta*f*f)-1)/den
normal=(2*h*g*sumrt-2*f*(prodrt+g*g))/B
zero('outer_conic_pair_exact',s.expand(s.together(normal+2*f-2*kap*f/den)).subs(h*h,B+f*f))
zero('positive_axis_eigenvalue_identity',alpha+beta*(f*f+g*g)-(a2-lam)/a2**2)
Lx,Ly,c,u,v=s.symbols('Lx Ly c u v',nonzero=True)
n=s.Matrix([u/Lx,v/Ly]);focus=s.Matrix([c,0]);al=1/Ly**2;be=(1/Lx**2-al)/c**2
qden=al*n.dot(n)+be*(c*n[1])**2
weighted=focus.dot(n)*n/qden
zero('weighted_normal_x',weighted[0]-c*Ly**2*u*u/(u*u+v*v))
zero('weighted_normal_y',weighted[1]-c*Lx*Ly*u*v/(u*u+v*v))
z,w,d,e=s.symbols('z w d e',nonzero=True)
def curve(z,w):return d*z*z*w*w-z*z-w*w+2*e*z*w+d
nextw=-z-2*e*w/(d*w*w-1)
zero('nonbacktracking_curve_preservation',curve(w,nextw)-curve(z,w))
zero('root_exchange_involution',-nextw-2*e*w/(d*w*w-1)-z)
zero('curve_discriminant',s.discriminant(curve(z,w),w)/4-(d*z**4+(e*e-d*d-1)*z*z+d))
zero('grouped_pole_identity',z*(-2*e*z/(d*z*z-1))+2*e/(d-1/(z*z)))
U,V=s.symbols('U V')
zero('strict_discriminant_factor',((1+(U-V)**2-(U+V-1)**2)/2)**2-(U-V)**2-4*U*V*(1-U)*(1-V))
receipt={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','exact_identities':len(results),'results':results,'runtime':{'python':sys.version,'sympy':s.__version__},'scope':'Independent raw line solving, conic pair/weighted-normal reductions, global curve/Vieta/discriminant identities. Positivity/compactness/pole completeness/periodic-family extension independently checked by Root in mathematical notes; not a standalone novelty clearance or firstvisibility proof.','imports_other_checker_helpers':False,'provider_writes':0,'shared_git_mutations':0}
(O/'ROOT_INDEPENDENT_ALGEBRA.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
