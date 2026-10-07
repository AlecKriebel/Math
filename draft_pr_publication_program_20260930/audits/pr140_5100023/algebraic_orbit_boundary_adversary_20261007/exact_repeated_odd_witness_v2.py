#!/usr/bin/env python3
"""Exact algebraic repeated-triangle boundary witness, not a proof-search turn."""
import sympy as s
from pathlib import Path
from datetime import datetime,timezone
import os,sys,json,hashlib
start=datetime.now(timezone.utc).isoformat()
x,y=s.symbols('x y')
G=s.groebner([16*x*x-18*x-25,y*y+x*x-1],y,x,domain=s.QQ)
checks=[]
def dot(u,v):return u[0]*v[0]+u[1]*v[1]
def sub(u,v):return tuple(u[i]-v[i] for i in range(2))
def check(name,expression):
 num=s.together(expression).as_numer_denom()[0]
 r=G.reduce(s.expand(num))[1]
 if r!=0:raise ValueError(name+': '+str(r))
 checks.append(name)
P=[(s.Integer(5),s.Integer(0)),(5*x,3*y),(5*x,-3*y)]
lam=25*(1-x*x);d=y*(16*x-25)/(3*x)
V=[(5*(x-1)/d,3*y/d),(s.Integer(0),s.Integer(-1)),(5*(1-x)/d,3*y/d)]
Q=[]
for i,p in enumerate(P):
 check('ellipse_'+str(i),p[0]**2/25+p[1]**2/9-1)
 check('unit_velocity_'+str(i),dot(V[i],V[i])-1)
 n=(p[0]/25,p[1]/9);incoming=V[(i-1)%3];outgoing=V[i]
 factor=2*dot(incoming,n)/dot(n,n)
 for k in range(2):check('reflection_'+str(i)+'_'+str(k),outgoing[k]-incoming[k]+factor*n[k])
 B=P[(i+1)%3];edge=sub(B,p);normal=(edge[1],-edge[0]);r=dot(normal,p)
 check('confocal_tangency_'+str(i),r*r-(25-lam)*normal[0]**2-(9-lam)*normal[1]**2)
 determinant=p[0]*B[1]-p[1]*B[0]
 k=dot(p,p);l=dot(B,B)
 q=((k*B[1]-l*p[1])/determinant,(p[0]*l-B[0]*k)/determinant)
 for j,pt in enumerate([p,B]):check('origin_line_'+str(i)+'_'+str(j),dot(pt,q)-dot(pt,pt))
 Q.append(q)
Cx=sum(q[0] for q in Q)/3;Cy=sum(q[1] for q in Q)/3
expected=s.Rational(34,15)*(2+1/x)
check('origin_centroid_x',Cx-expected);check('origin_centroid_y',Cy)
# False controls through the same polynomial certificate, not a dummy assertion.
false=[]
for name,expr in [('zero_centroid',Cx),('changed_caustic',r*r-(25-(lam+1))*normal[0]**2-(9-(lam+1))*normal[1]**2),('corrupted_reflection',outgoing[0]+1-incoming[0]+factor*n[0])]:
 num=s.together(expr).as_numer_denom()[0]
 if G.reduce(s.expand(num))[1]==0:raise ValueError('false control accepted '+name)
 false.append(name)
xx=(9-s.sqrt(481))/16;yy=s.sqrt(1-xx*xx)
points=[[str(v),str(s.N(v.subs({x:xx,y:yy}),35))] for p in P for v in p]
r={'schema':'pr140-exact-repeated-odd-boundary-witness/v1','verdict':'PASS','actual_PID':os.getpid(),'UTC_start':start,'UTC_end':datetime.now(timezone.utc).isoformat(),'optimized':sys.flags.optimize>0,'sympy_version':s.__version__,'outer_ellipse':'X²/25+Y²/9=1','selected_root':'x=(9−sqrt(481))/16, y=sqrt(1−x²)>0','root_polynomial':'16x²−18x−25=0','strict_bounds':'−1<x<−4/5 follows from 109/5<sqrt(481)<25; hence 0<lambda=25(1−x²)<9','triangle_vertices':['(5,0)','(5x,3y)','(5x,−3y)'],'least_period':3,'repeated_traversal_count':6,'lambda_exact':str(s.simplify(lam.subs(x,xx))),'lambda_decimal':str(s.N(lam.subs(x,xx),35)),'origin_antipedal_vertices':[str(q) for q in Q],'origin_centroid_exact':'(34/15)(2+1/x), 0','origin_centroid_decimal':str(s.N(expected.subs(x,xx),35)),'nonzero_proof':'−1<x<−4/5 implies 3/4<2+1/x<1, so Cx>17/10>0. The centrally inverted triangle has the same confocal caustic and centroid −C; repeated six-point lists retain each centroid.','denominator_signs':'x<0, y>0, d=y(16x−25)/(3x)>0; distinct points and nonzero line determinants (±15y,−30xy). Clearing denominators is justified by these signs.','reflection_and_tangency_certificates':checks,'certificates_count':len(checks),'false_controls_rejected':false,'symbolic_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'independent_of_author_code':True,'other_family_read':False,'scope':'Refutes only an interpretation permitting repeated odd least-period orbits under an even traversal count. It does not refute the candidate even-least-period theorem.','new_central_proof_search_turns':0}
Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'verdict':r['verdict'],'PID':r['actual_PID'],'UTC':r['UTC_end'],'checks':len(checks),'lambda':r['lambda_decimal'],'Cx':r['origin_centroid_decimal'],'optimized':r['optimized']}))
