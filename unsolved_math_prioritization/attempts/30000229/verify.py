#!/usr/bin/env python3
import sympy as s
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import json
checks=0

def ck(x):
 global checks
 assert x
 checks+=1
x,y=s.symbols('x y',real=True)
l=[1-x-y,x,y]
def tri(f):return s.integrate(s.integrate(s.expand(f),(y,0,1-x)),(x,0,1))
energies=[]
for a,b,c in [(0,1,2),(0,2,1),(1,2,0)]:
 edge=4*l[a]*l[b];correction=20*l[a]*l[b]*l[c];psi=edge-correction
 ck(tri(edge)==s.Rational(1,6));ck(tri(correction)==s.Rational(1,6));ck(tri(psi)==0)
 energy=tri(s.diff(psi,x)**2+s.diff(psi,y)**2);ck(energy>0);energies.append(str(energy))
 # Restrict to the chosen edge in its unit barycentric parameter t.
 t=s.symbols('t');ck(s.integrate(4*t*(1-t),(t,0,1))==s.Rational(2,3))
 for z in (a,b):
  mapping={0:{y:1-x},1:{x:0},2:{y:0}}[z]
  ck(s.expand(psi.subs(mapping))==0)
# Center-hat gradients on the four unit-square base triangles.
grads=[(0,2),(-2,0),(0,-2),(2,0)]
ck(sum(F(g[0]**2+g[1]**2,4) for g in grads)==4)
for i in range(4):
 a,b=grads[i],grads[(i+1)%4]
 ck(sum((a[j]-b[j])**2 for j in range(2))==8)
for n in range(1,151):
 # Exact energy of levels1..n and exact infinite tail.
 partial=4*sum(F(1,4**j) for j in range(1,n+1))
 tail=F(4,3*4**n)
 ck(partial+tail==F(4,3))
 ck(sum(4*j+3*4**j for j in range(1,n+1))<=6*4**n)
 selected=sum(4**j*2*F(1,4**j) for j in range(1,n+1))
 ck(selected==2*n)
 ck(F(4*n*n,4**n)==(2*n)**2*F(1,4**n))
 for j in range(1,min(n,8)+1):
  h=F(1,4**j);amplitude=h
  jump2=8*(amplitude/h)**2;length2=h*h/2
  ck(jump2==8);ck(jump2*length2==4*h*h)
# Cauchy allocation inequality on disjoint selected segments.
allocation_cases=0
for n in range(1,5):
 lengths=[2*F(1,4**j) for j in range(1,n+1) for _ in range(4**j)]
 for seed in range(1,81):
  pieces=[1+(seed*(i+3)+i*i)%17 for i in range(len(lengths))]
  left=sum(a*a/m for a,m in zip(lengths,pieces))
  right=sum(lengths)**2/sum(pieces)
  ck(left>=right);allocation_cases+=1
# A selected segment split arbitrarily has sum(length_i²)>=length²/count.
for m in range(1,31):
 for seed in range(1,21):
  nums=[1+(seed*(i+1))%13 for i in range(m)];total=sum(nums)
  vals=[F(a,total) for a in nums]
  ck(sum(v*v for v in vals)>=F(1,m))
r={'status':'PASS','artifact_sha256':sha256(Path('COUNTEREXAMPLE.md').read_bytes()).hexdigest(),'exact_assertions':checks,'reference_bubble_energies':energies,'allocation_cases':allocation_cases,'limits':'Exact local polynomial and allocation controls; no finite mesh enumeration replaces the uniform H−1 and NVB overlay proof.'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
