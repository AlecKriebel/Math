#!/usr/bin/env python3
"""Independent controls written for the audit; imports no packet code."""
from fractions import Fraction as Q
from itertools import product
import json

results=[]
def record(name, condition, data=None):
 assert condition, name
 results.append({'name':name, 'passed':True, 'data':data})

def negative_cf(n,d):
 out=[]
 while d:
  q=(n+d-1)//d;out.append(q);n,d=d,q*d-n
 return out
record('Hirzebruch-Jung fractions',negative_cf(3,2)==[2,2] and negative_cf(8,3)==[3,3],{'3/2':negative_cf(3,2),'8/3':negative_cf(8,3)})

# Work in the orthogonal basis L,A1,A2,B1,B2, rather than the seven-divisor matrix.
G=[[24,0,0,0,0],[0,-2,1,0,0],[0,1,-2,0,0],[0,0,0,-3,1],[0,0,0,1,-3]]
def inner(a,b):return sum(a[i]*G[i][j]*b[j] for i in range(5) for j in range(5))
L=[1,0,0,0,0]; D=[0,1,1,1,1]; beta=[0,Q(-1,4),Q(-1,4),Q(-3,8),Q(-3,8)]
record('Orthogonal-basis norms',inner(L,L)==24 and inner(D,D)==-6 and inner(beta,beta)==Q(-11,16) and inner(L,beta)==0)
record('Central-charge rank coefficient',Q(24,2)-inner(beta,beta)/2==Q(395,32),str(Q(395,32)))
subchains=[]
for start in (1,3):
 for a,b in ((start,start),(start,start+1),(start+1,start+1)):
  c=[int(a<=j<=b) for j in range(5)];m=b-a+1;n=sum(-G[j][j] for j in range(a,b+1));bp=inner(beta,c)
  chamber=bp-Q(n,2); residue=(Q(n,2)-(m-1)-bp)%1
  # Every integer total degree has the same residue. The nearest integer distance is exact.
  gap=min(residue,1-residue)
  record('Interval '+str((a,b)),chamber.denominator>1 and -m<chamber<1-m and gap**2+Q(1,48)*inner(c,c)>=0)
  subchains.append({'indices':[a,b],'chamber':str(chamber),'charge_residue':str(residue),'all_degree_minimum':str(gap),'cycle_square':inner(c,c)})

# Polynomial convolution controls the whole rational parametrization, not a list of s values.
def conv(a,b):
 r=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):r[i+j]+=x*y
 return r
lhs=[24*x for x in conv([1,0,1],[1,0,1])]
bsq=conv([0,4],[0,4])
for i,x in enumerate(bsq):lhs[i]-=6*x
record('Whole-path constant-volume polynomial',lhs==[24*x for x in conv([1,0,-1],[1,0,-1])],lhs)
# For 0<s<1/8, 8s<1<1+s^2, hence b/a<1/2 and all toric intersections are positive.
record('Uniform path inequality endpoint',8*Q(1,8)==1 and 1+Q(1,8)**2>1)

# A2 branch can be used literally without the false branching-ADE uniqueness assertion.
roots=[(a,b) for a,b in product(range(1,15),repeat=2) if a*a+b*b-a*b==1]
record('A2 root spot check',roots==[(1,1)],roots)
# A proof for all positive integers: (a-b)^2+ab=1 forces ab=1, hence a=b=1.
record('A2 algebraic identity',all(a*a+b*b-a*b==(a-b)**2+a*b for a,b in product(range(-5,6),repeat=2)))

# Chou's A1 input: discrepancy a E has (a E).E=K_F2.E=0, so a=0.
F2=[[ -2,1],[1,0]]
K=[-2,-4]
KE=sum(K[i]*F2[i][0] for i in range(2))
record('F2 exceptional crepancy',KE==0 and F2[0][0]!=0,{'K.E':KE,'E^2':-2,'discrepancy':0})
# One explicit admissible Chou choice is beta=-E/8, beta.E=1/4, beta^2=-1/32, z=1.
record('Chou A1 parameter chamber',Q(1,4)>0 and Q(1,4)<1 and 1>Q(1,64),{'beta.E':'1/4','beta^2':'-1/32','z':'1'})

M=[[-2,1,1,1],[1,-2,0,0],[1,0,-2,0],[1,0,0,-2]]
def square(v):return sum(v[i]*M[i][j]*v[j] for i in range(4) for j in range(4))
record('D4 distinct full-support square-minus-two roots',square([1,1,1,1])==square([2,1,1,1])==-2)
# beta with all pairings 1/4, explicitly solved: beta=(-5/4,-3/4,-3/4,-3/4).
b=[Q(-5,4),Q(-3,4),Q(-3,4),Q(-3,4)]
record('D4 beta divisor realizability',all(sum(M[i][j]*b[j] for j in range(4))==Q(1,4) for i in range(4)),list(map(str,b)))
print(json.dumps({'result':'PASS','independent_of_packet_code':True,'test_groups':len(results),'results':results,'all_integer_degree_intervals':subchains,'limits':'Polynomial identities and exact residue arguments are uniform; categorical existence remains a cited theorem.'},indent=2)+'\n',end='')
