"""Fresh independent exact controls, written after initial seal, no supplied code imports.
Uses installed SymPy only. This is a selected new scientific check, not the default
custody verifier, and it never reads project/source/code/results or uses a network.
"""
import json
from fractions import Fraction
import sympy as s
I=s.I
checks=[]
def zero(label,x):
 r=s.factor(s.cancel(s.expand(x)))
 if r!=0:r=s.simplify(r)
 if r!=0:raise ValueError(label+': '+str(r))
 checks.append({'label':label,'exact_residual':str(r)})
def nonzero(label,x):
 r=s.factor(s.simplify(x))
 if r==0:raise ValueError(label)
 checks.append({'label':label,'exact_nonzero':str(r)})
def cross(a,b):return s.expand(a[0]*b[1]-a[1]*b[0])
def moments(points):
 area=sum(cross(p,q) for p,q in zip(points,points[1:]+points[:1]))/2
 moment=[sum(cross(p,q)*(p[j]+q[j]) for p,q in zip(points,points[1:]+points[:1])) for j in range(2)]
 return s.simplify(area),[s.simplify(x) for x in moment]
A,B,L=s.symbols('A B L',positive=True);H=(A+B)/2;e=(A-B)/2;d=1-L*(1/A+1/B);F=H*d+2*L
zero('support cosu coefficient F+ed',F+e*d-(A+L*(1-A/B)))
zero('support sinu coefficient F-ed',F-e*d-(B+L*(1-B/A)))
zero('F+ed lowerboundary difference',(F+e*d-B)-(A-B)*(B-L)/B)
zero('F-ed positive expansion',(F-e*d)-(B+L*(A-B)/A))
x,y,t,tb,h,k,D,H,e=s.symbols('x y t tb h k D H e',nonzero=True)
def conjugate(p):return s.expand(p.xreplace({x:1/x,y:1/y,t:tb,tb:t,I:-I}))
def det(p,q):return s.expand((conjugate(p)*q-p*conjugate(q))/(2*I))
Z=x*x;W=y*y;cd=(y/x+x/y)/2;cs=(x*y+1/(x*y))/2;c2x=(x*x+1/(x*x))/2;c2y=(y*y+1/(y*y))/2
hs=H+e*c2x;ks=H+e*c2y;hk=D*cd+e*cs
zero('support-square full Laurent identity',(D*cd+e*cs)**2-hs*ks-((D*D-e*e)*cd**2-H*H+e*e-e*(H-D)*(c2x+c2y)))
zero('unit cyclic edge identity',det(x,y)*(x+y)+I*(1+cd)*(y-x))
zero('doubled-normal endpoint identity',cs*(y/x-x/y)/(2*I)-(s.sin(0) if False else ((y*y-1/(y*y))-(x*x-1/(x*x)))/(4*I)))
# Own expansion of paired actual edge moments and independent Laurent reduction.
va=h*x-t*Z;vb=k*y-t*W;na=-h*x-t*Z;nb=-k*y-t*W
avg=s.expand((det(va,vb)*(va+vb)+det(na,nb)*(na+nb))/2)
poly=s.Poly(s.expand(2*I*avg),t,tb)
c=k*k*x*x-h*h*y*y+2*h*k*(x**3/y-y**3/x)
b=h*h*x*x/(y*y)-k*k*y*y/(x*x)+h*k*(x/y-y/x)
zero('paired edge linear t coefficient',poly.coeff_monomial(t)-c)
zero('paired edge linear bart coefficient',poly.coeff_monomial(tb)-b)
zero('paired edge pure w constant cancels',poly.coeff_monomial(1))
for term in [t*t,t*tb,tb*tb]:zero('paired quadratic coefficient '+str(term),poly.coeff_monomial(term))
zero('paired cubic term exact',avg-(c*t+b*tb)/(2*I)+t*t*tb*det(Z,W)*(Z+W))
r=Z/W-W/Z;q=Z*Z/W-W*W/Z
cspec=D*q+3*e*r/2+(D+H)*(Z-W)+e*(Z*Z-W*W)
bspec=(D/2+H)*r+e*q/2+e*(Z-W)/2+e*(1/W-1/Z)
replace=lambda p:s.expand(p).subs(h*h,hs).subs(k*k,ks).subs(h*k,hk)
zero('full c Laurent reduction',replace(c)-cspec)
zero('full b Laurent reduction',replace(b)-bspec)
zero('r and signed doubled area identity',r+2*I*det(Z,W))
zero('s moment endpoint telescope',q+2*I*det(Z,W)*(Z+W)-(W-Z))
nonzero('negativecontrol wrong3e coefficient',replace(c)-(D*q+e*r+(D+H)*(Z-W)+e*(Z*Z-W*W)))
# Projection is independent real coordinate algebra; conjugation is essential.
X,Y,nx,ny,hn=s.symbols('X Y nx ny hn',real=True);z=X+I*Y;n=nx+I*ny
Q=z+(hn-X*nx-Y*ny)*n;proposal=z/2+hn*n-s.conjugate(z)*n*n/2
zero('projection formula modulo unit-normal constraint',s.expand(Q-proposal).subs(ny*ny,1-nx*nx))
nonzero('negativecontrol omitconjugation',(Q-(z/2+hn*n-z*n*n/2)).subs({nx:1,ny:0,hn:2,X:1,Y:1}))
a,bv=s.symbols('a b',positive=True);rectangle=[(a,Y),(X,bv),(-a,Y),(X,-bv)]
ra,rt=moments(rectangle);zero('fourperiod rectangle area',ra-2*a*bv)
zero('fourperiod rectangle firstmoment x',rt[0]-4*a*bv*X);zero('fourperiod rectangle firstmoment y',rt[1]-4*a*bv*Y)
# General translation identity checked algebraically by the arbitrary quadrilateral
# control; derivation records the all-N telescoping proof separately.
uv=s.symbols('x0 y0 x1 y1 x2 y2 x3 y3 cx cy');points=[uv[i:i+2] for i in range(0,8,2)];cx,cy=uv[-2:];pa,pt=moments(points);ta,tt=moments([(p[0]+cx,p[1]+cy) for p in points])
zero('arbitraryquadrilateral translation area',ta-pa)
zero('arbitraryquadrilateral translation momentx',tt[0]-pt[0]-6*cx*pa);zero('arbitraryquadrilateral translation momenty',tt[1]-pt[1]-6*cy*pa)
# Exact native star construction, rebuilt directly from manuscript coordinates.
A=s.Rational(221,96);B=s.Rational(27625,20736);L=s.Rational(125,96);a=s.sqrt(A);b=s.sqrt(B)
R=s.Rational;norm=[(0,1),(-R(12,13),-R(5,13)),(1,0),(-R(12,13),R(5,13)),(0,-1),(R(12,13),R(5,13)),(-1,0),(R(12,13),-R(5,13))]
points=[s.Matrix([a*p,b*q]) for p,q in norm]
zero('star caustic first semiaxis',A-L-1);zero('star caustic second semiaxis',B-L-R(625,20736))
if len(set(norm))!=8:raise ValueError('distinctstarvertices')
checks.append({'label':'eight distinctstarvertices','exact_count':8})
pedals=[]
for j,p in enumerate(points):
 prev=points[j-1];nxt=points[(j+1)%8];edge=nxt-p;normal=s.Matrix([p[0]/A,p[1]/B]);ln=s.Matrix([edge[1],-edge[0]]);offset=s.simplify(ln.dot(p))
 zero('star boundary vertex '+str(j),p[0]*p[0]/A+p[1]*p[1]/B-1)
 zero('star chord caustic tangency '+str(j),offset*offset-(A-L)*ln[0]*ln[0]-(B-L)*ln[1]*ln[1])
 incoming=p-prev;outgoing=nxt-p;iu=incoming/s.sqrt(s.simplify(incoming.dot(incoming)));ou=outgoing/s.sqrt(s.simplify(outgoing.dot(outgoing)))
 reflected=iu-2*iu.dot(normal)/normal.dot(normal)*normal
 for coord in range(2):zero('star exact specularreflection '+str(j)+' coord'+str(coord),reflected[coord]-ou[coord])
 cp=s.simplify(cross(p,nxt))
 if cp.is_positive is not True:raise ValueError('positive oriented branch')
 checks.append({'label':'star consistent counterclockwisebranch '+str(j),'positive_cross':str(cp)})
 M=s.Matrix([X,Y]);foot=M+(1-normal.dot(M))/normal.dot(normal)*normal;pedals.append(tuple(s.simplify(v) for v in foot))
area,mom=moments(pedals)
expected_area=-s.sqrt(30)/134784*(20736*(X*X+Y*Y)-123539)
expected_mom=[-s.sqrt(30)*X/109512*(41472*(X*X+Y*Y)-272935),-s.sqrt(30)*Y/97344*(52992*(X*X+Y*Y)-347633)]
zero('unrestrictedCartesian stararea polynomial',area-expected_area)
zero('unrestrictedCartesian starmomentx polynomial',mom[0]-expected_mom[0]);zero('unrestrictedCartesian starmomenty polynomial',mom[1]-expected_mom[1])
H=(A+B)/2;e=(A-B)/2;d=1-L*(1/A+1/B);F=H*d+2*L;v=-4*e*L*d/(F*F-e*e*d*d)
for label,actual,expect in [('d',d,-R(120,221)),('F',F,R(2795,1728)),('v',v,R(7,13)),('radius2',-2*F/d,R(123539,20736))]:zero('star exact '+label,actual-expect)
S0=area.subs({X:0,Y:0});G=2*F+d*(X*X+Y*Y);zc=X+I*Y;zcbar=X-I*Y
zero('full star allM denominator-cleared centroid identity',mom[0]+I*mom[1]-3*zc*area+S0/F*(zc*(F+2*H*d+e*v*d)+zcbar*(2*F*v+3*e*d+v*d*(X*X+Y*Y)/2)))
diag={X:13*s.sqrt(731)/144,Y:0};zero('diagnostic zero signedarea',area.subs(diag));zero('diagnostic stated nonzero moment',mom[0].subs(diag)-221*s.sqrt(21930)/10368)
nonzero('diagnostic pole nonremovable',mom[0].subs(diag));zero('diagnostic y moment',mom[1].subs(diag))
# Winding of normalized coordinates survives positive diagonal scaling.
winding=0
for p,qv in zip(norm,norm[1:]+norm[:1]):
 cp=cross(p,qv)
 if p[1]<=0<qv[1] and cp>0:winding+=1
 elif qv[1]<=0<p[1] and cp<0:winding-=1
if winding!=3:raise ValueError('starwinding')
checks.append({'label':'exact positive-ray winding count','winding':winding})
# Without antipodal pairing, a direct pedal area has an uncancelled linear term.
tria=[s.Matrix([2,0]),s.Matrix([0,1]),s.Matrix([-2,0])];tp=[]
for p in tria:
 nn=s.Matrix([p[0]/4,p[1]]);M=s.Matrix([X,Y]);tp.append(tuple(M+(1-nn.dot(M))/nn.dot(nn)*nn))
ta,tm=moments(tp);nonzero('negativecontrol missingantipodalpairing lineararea',s.diff(ta,Y).subs({X:0,Y:0}))
print(json.dumps({'independent_exact_checks':len(checks),'sympy_version':s.__version__,'checks':checks,'star_S':str(area),'star_T':[str(v) for v in mom],'star_winding':winding,'universal_claim_proved_by_finite_samples':False,'supplied_source_or_project_code_imported_executed':False,'network_subprocesses_or_file_writes':False},ensure_ascii=False,indent=2))
