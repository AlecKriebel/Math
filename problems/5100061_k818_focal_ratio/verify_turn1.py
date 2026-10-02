#!/usr/bin/env python3
import sympy as s,json
A=s.Integer(2);B=s.Integer(1);rt=s.sqrt(5);v=list(map(s.Matrix,[(2,0),(s.Rational(4,3),rt/3),(-s.Rational(4,3),rt/3),(-2,0),(-s.Rational(4,3),-rt/3),(s.Rational(4,3),-rt/3)]))
n=0
def ck(x):
 global n
 assert s.simplify(x)==0,x;n+=1
def area(w):return s.simplify(sum(s.det(s.Matrix.hstack(a,w[(i+1)%len(w)])) for i,a in enumerate(w))/2)
for i,p in enumerate(v):
 ck(p[0]**2/4+p[1]**2-1)
 incoming=p-v[(i-1)%6];out=v[(i+1)%6]-p
 incoming=s.simplify(incoming/s.sqrt(incoming.dot(incoming)));out=s.simplify(out/s.sqrt(out.dot(out)))
 normal=s.Matrix([p[0]/4,p[1]]); reflected=s.simplify(incoming-2*incoming.dot(normal)/normal.dot(normal)*normal)
 for z in reflected-out:ck(z)
 # A line through the endpoints tangent to the caustic satisfies support²=n^T C n.
 d=v[(i+1)%6]-p;normal=s.Matrix([-d[1],d[0]]);support=normal.dot(p)
 ck(support**2-s.Rational(32,9)*normal[0]**2-s.Rational(5,9)*normal[1]**2)
for sign in [-1,1]:
 F=s.Matrix([sign*s.sqrt(3),0]);u=[];iv=[]
 for i,p in enumerate(v):
  q=v[(i+1)%6];M=s.Matrix.vstack((p-F).T,(q-F).T);assert s.simplify(M.det())!=0;n+=1
  z=s.simplify(M.inv()*s.Matrix([(p-F).dot(p),(q-F).dot(q)]));u.append(z)
  ck((p-F).dot(z-p));ck((q-F).dot(z-q));iv.append(s.simplify(F+(p-F)/(p-F).dot(p-F)))
 ck(area(u));ck(area(iv)-15*rt/8);ck(area(v)-20*rt/9)
print(json.dumps({'status':'PASS','exact_assertions':n,'source_recorded_case':'primitive simpleN6,a/b2','original_area':'20sqrt(5)/9','inverse_area':'15sqrt(5)/8','antipedal_area':'0','scope':'Exact exceptional-family geometry; general corollary uses credited full input proofs.'},indent=2))
