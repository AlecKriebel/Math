#!/usr/bin/env python3
"""Owned exact analytic controls; no submitted program imports or execution."""
from pathlib import Path
from itertools import permutations
import datetime,json
import sympy as s
O=Path(__file__).resolve().parent
checks=[]
def ck(name,test,detail=None):
 if not test:raise RuntimeError(name)
 row={'name':name,'verified':True}
 if detail is not None:row['detail']=detail
 checks.append(row)
def integral(poly,ts):
 value=s.expand(poly)
 for i in reversed(range(len(ts))):
  value=s.integrate(value,(ts[i],0,1-sum(ts[:i])))
 return s.factor(value)
def data(vertices):
 n=len(vertices[0]);ts=s.symbols('t0:'+str(n));base=s.Matrix(vertices[0])
 edges=s.Matrix.hstack(*(s.Matrix(v)-base for v in vertices[1:]))
 det=s.factor(edges.det())
 if not det:raise ValueError('Degenerate simplex excluded')
 coords=base+edges*s.Matrix(ts)
 vol=abs(det)*integral(1,ts)
 first=s.Matrix([abs(det)*integral(v,ts) for v in coords])
 second=abs(det)*integral(sum(v*v for v in coords),ts)
 return vol,first,second
def norm(v):return (s.Matrix(v).T*s.Matrix(v))[0]
def check_simplex(name,vertices,r2=None):
 n=len(vertices[0]);vol,first,second=data(vertices);c=first/vol
 q=sum(norm(v) for v in vertices)/s.Integer(n+1)
 ck(name+'_centroid',c==sum((s.Matrix(v) for v in vertices),s.zeros(n,1))/(n+1))
 ck(name+'_moment',s.factor(second/vol-(q+(n+1)*norm(c))/(n+2))==0)
 if r2 is not None:
  ck(name+'_vertex_bound',all(norm(v)>=r2 for v in vertices))
  ck(name+'_deficit',s.factor(second/vol-(r2+(n+1)*norm(c))/(n+2)-(q-r2)/(n+2))==0)
 return vol,first,second

# Repeated elementary polynomial integration, without the factorial moment formula.
for n in range(1,5):
 ts=s.symbols('t0:'+str(n));lambdas=[1-sum(ts),*ts];volume=integral(1,ts)
 ck('standard_volume_n'+str(n),volume==1/s.factorial(n))
 for i in range(n+1):
  ck('barycentric_first_n'+str(n)+'_'+str(i),integral(lambdas[i],ts)/volume==s.Rational(1,n+1))
  ck('barycentric_diagonal_n'+str(n)+'_'+str(i),integral(lambdas[i]**2,ts)/volume==s.Rational(2,(n+1)*(n+2)))
  if i:
   ck('barycentric_mixed_n'+str(n)+'_'+str(i),integral(lambdas[0]*lambdas[i],ts)/volume==s.Rational(1,(n+1)*(n+2)))

for n in range(1,5):
 vertices=[tuple([1]*n)]
 vertices += [tuple(-1 if j==i else 1 for j in range(n)) for i in range(n)]
 result=check_simplex('sphere_corner_n'+str(n),vertices,s.Integer(n))
 ck('sphere_corner_equality_n'+str(n),s.factor(result[2]/result[0]-(n+(n+1)*norm(result[1]/result[0]))/(n+2))==0)

triangle=[(1,0),(s.Rational(3,5),s.Rational(4,5)),(s.Rational(3,5),-s.Rational(4,5))]
vol,first,second=check_simplex('off_origin_nonregular_triangle',triangle,s.Integer(1))
ck('off_origin_triangle_value',first/vol==s.Matrix([s.Rational(11,15),0]) and second/vol==s.Rational(49,75))
ck('off_origin_triangle_excludes_origin',all(v[0]>=s.Rational(3,5) for v in triangle))
ck('off_origin_triangle_not_regular',len({norm(s.Matrix(a)-s.Matrix(b)) for i,a in enumerate(triangle) for b in triangle[i+1:]})>1)
check_simplex('strict_radius_triangle',[tuple(2*x for x in v) for v in triangle],s.Integer(1))
a,b=s.symbols('a b',positive=True);p,q,z=s.symbols('p q z',real=True)
ck('universal_two_term_completed_square',s.factor(a*(p-z)**2+b*(q-z)**2-a*b/(a+b)*(p-q)**2-(a+b)*((a*p+b*q)/(a+b)-z)**2)==0)

# A 3D retained shell with a nonsimplicial visible square facet.
base=(-1,-1,-1);cube=[]
for order in permutations(range(3)):
 v=list(base);vertices=[tuple(v)]
 for axis in order:v[axis]=1;vertices.append(tuple(v))
 cube.append(vertices)
apex=(2,0,0)
face1=[(1,-1,-1),(1,1,-1),(1,1,1)]
face2=[(1,-1,-1),(1,1,1),(1,-1,1)]
shell=[[apex,*face1],[apex,*face2]]
pieces=[check_simplex('cube_piece_'+str(i),v,s.Integer(3)) for i,v in enumerate(cube)]
pieces += [check_simplex('shell_piece_'+str(i),v,s.Integer(3)) for i,v in enumerate(shell)]
V=sum(v for v,_,_ in pieces);M=sum((m for _,m,_ in pieces),s.zeros(3,1));J=sum(j for _,_,j in pieces)
t=s.symbols('t',real=True)
pyramidV=s.integrate(4*(1-t)**2,(t,0,1))
pyramidM=s.integrate(4*(1-t)**2*(1+t),(t,0,1))
pyramidJ=s.integrate(4*(1-t)**2*((1+t)**2+s.Rational(2,3)*(1-t)**2),(t,0,1))
ck('3D_shell_volume_from_cross_sections',V==8+pyramidV==s.Rational(28,3))
ck('3D_shell_first_from_cross_sections',M==s.Matrix([pyramidM,0,0])==s.Matrix([s.Rational(5,3),0,0]))
ck('3D_shell_second_from_cross_sections',J==8+pyramidJ==s.Rational(32,3))
c=M/V;radial=0;variance=0
for vertices,(v,m,j) in zip(cube+shell,pieces):
 cell_c=m/v;cell_q=sum(norm(x) for x in vertices)/4
 radial += v/V*(cell_q-3)/5
 variance += s.Rational(4,5)*v/V*norm(cell_c-c)
deficit=s.factor(J/V-(3+4*norm(c))/5)
ck('3D_shell_deficit_split',s.factor(deficit-radial-variance)==0 and radial>=0 and variance>0)
S=data(cube[0]);T=data(shell[0]);aa,bb=S[0],T[0]
bound=s.factor(s.Rational(4,5)*aa*bb/(V*(aa+bb))*norm(S[1]/aa-T[1]/bb))
ck('retained_witness_strict_bound',0<bound<=deficit,{'bound':str(bound),'deficit':str(deficit)})
ck('retained_witness_vertex_difference',s.simplify(S[1]/aa-T[1]/bb)==s.Matrix(base)/4-s.Matrix(apex)/4)

# Singular/endpoint controls and an analytic nonpolytope family.
try:data([(0,0),(1,0),(2,0)])
except ValueError:ck('singular_simplex_rejected',True)
else:raise RuntimeError('Singular simplex accepted')
A,B,R=s.symbols('A B R',real=True)
mean=(A+B)/2;moment=(A*A+A*B+B*B)/3
ck('general_interval_deficit',s.factor(moment-(R*R+2*mean*mean)/3-(A*A+B*B-2*R*R)/6)==0)
for n in range(1,8):
 radial_moment=s.integrate(t**(n+1),(t,0,1))/s.integrate(t**(n-1),(t,0,1))
 ck('Euclidean_ball_analytic_n'+str(n),radial_moment==s.Rational(n,n+2) and radial_moment-s.Rational(1,n+2)==s.Rational(n-1,n+2))
result={'record_id':'22983138','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sympy':s.__version__,'checks':checks,'finite_checks_prove_universal_partition_or_equality':False,'source_programs_imported_or_run':False}
(O/'exact-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'all_verified':True,'sympy':s.__version__,'retained_3D_witness_bound':str(bound)}))
