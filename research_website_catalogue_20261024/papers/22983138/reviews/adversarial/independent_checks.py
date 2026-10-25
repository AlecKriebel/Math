"""Independent polynomial integration and 3D shell checks. No submitted imports."""
from pathlib import Path
import json,math
import sympy as s

def plain(q):return str(s.factor(q))
def integral_std(poly,t):
 out=s.expand(poly)
 for j in range(len(t)-1,-1,-1):
  out=s.integrate(out,(t[j],0,1-sum(t[:j])))
  out=s.expand(out)
 return s.factor(out)
def moments(vertices):
 n=len(vertices)-1
 if n<1 or any(len(x)!=n for x in vertices):raise ValueError('wrong dimension')
 vv=[s.Matrix(x) for x in vertices]
 A=s.Matrix.hstack(*[v-vv[0] for v in vv[1:]])
 det=s.factor(A.det())
 if det==0:raise ValueError('degenerate simplex has zero volume')
 t=s.symbols('t:'+str(n));xx=vv[0]+A*s.Matrix(t)
 mass=integral_std(1,t)
 center=s.Matrix([integral_std(c,t)/mass for c in xx])
 c2=integral_std(sum(c*c for c in xx),t)/mass
 q=sum(sum(c*c for c in v) for v in vv)/(n+1)
 expected=(q+(n+1)*center.dot(center))/(n+2)
 if s.factor(c2-expected)!=0:raise RuntimeError('simplex formula mismatch')
 return {'dimension':n,'volume':s.Abs(det)*mass,'centroid':center,'C2':s.factor(c2),'q':s.factor(q),'expected':s.factor(expected)}
def serial(M):return {k:[plain(v) for v in val] if isinstance(val,s.MatrixBase) else plain(val) for k,val in M.items()}
def deficit(M,r2):return s.factor(M['C2']-(r2+(M['dimension']+1)*M['centroid'].dot(M['centroid']))/(M['dimension']+2))
# Affine simplices with nonzero centroids in dimensions1..5, direct nested integration.
affine=[]
for n in range(1,6):
 v0=s.Matrix([s.Rational(j+1,j+2) for j in range(n)])
 A=s.Matrix(n,n,lambda i,j:(i+2 if i==j else (s.Rational(1,3) if j>i else 0)))
 V=[list(v0)]+[list(v0+A[:,j]) for j in range(n)]
 affine.append(serial(moments(V)))
# Nonregular centered tetrahedron on radius3 sphere.
V=[(1,2,2),(1,-2,-2),(-1,2,-2),(-1,-2,2)]
M=moments(V);edges=sorted({sum((a-b)**2 for a,b in zip(V[i],V[j])) for i in range(4) for j in range(i)})
assert M['centroid']==s.zeros(3,1) and M['q']==9 and deficit(M,9)==0 and len(edges)>1
centered={'moments':serial(M),'edge_squared_lengths':edges,'strengthened_deficit':plain(deficit(M,9)),'unstrengthened_deficit':plain(M['C2']-s.Rational(9,5))}
# Unit-circle triangle entirely in x>=3/5: origin is outside, centroid not zero.
V=[(1,0),(s.Rational(3,5),s.Rational(4,5)),(s.Rational(3,5),-s.Rational(4,5))]
M=moments(V)
assert M['q']==1 and deficit(M,1)==0 and M['centroid'][0]>0
outside={'moments':serial(M),'origin_outside':'all x>=3/5','strengthened_deficit':plain(deficit(M,1)),'unstrengthened_deficit':plain(M['C2']-s.Rational(1,4))}
# Paper's nonregular nonzero-centroid example, checked by direct integration.
M=moments([(1,0),(0,1),(-1,0)])
assert M['C2']==s.Rational(1,3) and deficit(M,1)==0
paper_example=serial(M)
# 1D endpoint controls and negative omitted-hypothesis example.
intervals=[]
for lo,hi,rr in [(-1,1,1),(-1,2,1),(2,3,1),(-s.Rational(1,10),s.Rational(1,10),1)]:
 M=moments([(lo,),(hi,)])
 intervals.append({'ends':[plain(lo),plain(hi)],'r':plain(rr),'moment':serial(M),'deficit':plain(deficit(M,rr*rr)),'hypothesis':bool(lo*lo>=rr*rr and hi*hi>=rr*rr)})
assert intervals[0]['deficit']=='0' and intervals[-1]['hypothesis'] is False and s.Rational(intervals[-1]['deficit'])<0
# Valid 3D coplanar-boundary shell: square-based pyramid, five genuine extreme points.
v0=(1,1,1);v1=(3,1,1);v2=(1,3,1);v3=(1,1,3);u=(3,3,1)
S=moments([v0,v1,v2,v3]);T=moments([u,v1,v2,v3])
x,y,z=s.symbols('x y z')
def Kint(poly):return s.factor(s.integrate(poly,(x,1,4-z),(y,1,4-z),(z,1,3)))
vol=Kint(1);g=s.Matrix([Kint(c)/vol for c in (x,y,z)]);c2=Kint(x*x+y*y+z*z)/vol
assert S['volume']+T['volume']==vol
assert all(s.factor(S['volume']*S['centroid'][i]+T['volume']*T['centroid'][i]-vol*g[i])==0 for i in range(3))
assert s.factor(S['volume']*S['C2']+T['volume']*T['C2']-vol*c2)==0
# The one strict visible plane is x+y+z=5. The base z=1 is tangent, not strict-visible.
assert sum(u)>5 and u[2]==1
# Every listed point has an explicit linear functional uniquely maximizing there.
verts=[v0,v1,v2,v3,u];directions=[(-1,-1,-1),(1,-1,-1),(-1,1,-1),(-1,-1,1),(1,1,0)]
for index,d in enumerate(directions):
 values=[sum(a*b for a,b in zip(d,v)) for v in verts]
 assert values[index]>max(values[:index]+values[index+1:])
# Coplanar lower face would yield determinant0 if incorrectly treated as positive-volume shell.
degen_detected=False
try:moments([u,v0,v1,v2])
except ValueError:degen_detected=True
assert degen_detected
r2=3;n=3
D=s.factor(c2-(r2+(n+1)*g.dot(g))/(n+2))
wS=S['volume']/vol;wT=T['volume']/vol
qterm=(wS*(S['q']-r2)+wT*(T['q']-r2))/(n+2)
varterm=(n+1)/(s.Rational(n+2))*(wS*(S['centroid']-g).dot(S['centroid']-g)+wT*(T['centroid']-g).dot(T['centroid']-g))
assert s.factor(D-qterm-varterm)==0
lb=s.factor(S['volume']*T['volume']*sum((a-b)**2 for a,b in zip(u,v0))/((n+1)*(n+2)*vol*(S['volume']+T['volume'])))
assert lb>0 and D>=lb and varterm==lb
shell={'old_simplex':serial(S),'new_simplex':serial(T),'direct_slice_integrals':{'volume':plain(vol),'centroid':list(map(plain,g)),'C2':plain(c2)},'strict_visible_plane':'x+y+z=5; u has value7','tangent_plane':'z=1; coplanar base is not strict visible','all_five_vertices_extreme':'explicit uniquely maximizing linear functionals checked','zero_volume_weak_visible_cone_rejected':degen_detected,'deficit':plain(D),'vertex_radius_part':plain(qterm),'centroid_variance_part':plain(varterm),'retained_pair_lower_bound':plain(lb)}
# Simplex moment matrix equality is algebraic in n via the two barycentric moments.
N=s.symbols('N',positive=True,integer=True)
assert s.factor(2/((N+1)*(N+2))-1/(N+1)**2-(N)/((N+1)**2*(N+2)))==0
out={'scope':'Exact finite controls and symbolic identity corroboration, not a proof of countable shell construction or worldwide novelty','direct_affine_simplex_integrations':affine,'centered_nonregular_tetrahedron':centered,'offcenter_origin_outside_equality_triangle':outside,'paper_triangle':paper_example,'intervals_and_omitted_hypothesis_negative_control':intervals,'three_dimensional_coplanar_shell':shell,'source_interface_trust_used_for_computations':False}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
