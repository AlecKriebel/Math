#!/usr/bin/env python3
"""Exact integer and free-word controls for AIM Conjecture 3.4.
Bounded experiments are not an atoroidality or quasi-isometry algorithm.
"""
import json
from itertools import permutations
from pathlib import Path
PHI={'a':'b','b':'c','c':'ab','d':'ea','e':'ed'}
PSI={'a':'cA','b':'a','c':'b','d':'cADe','e':'daC'}
def inv(w):return w.swapcase()[::-1]
def red(w):
 s=[]
 for a in w:
  if s and s[-1]==a.swapcase():s.pop()
  else:s.append(a)
 return ''.join(s)
def sub(w,m=PHI):return red(''.join(m[a] if a.islower() else inv(m[a.lower()]) for a in w))
def cyc(w):
 w=red(w)
 while len(w)>1 and w[0]==w[-1].swapcase():w=w[1:-1]
 return w

def conjugacy_key(w):
 w=cyc(w)
 return min(w[i:]+w[:i] for i in range(len(w))) if w else ''
def mat(m,letters):return [[m[a].count(b)-m[a].count(b.upper()) for a in letters] for b in letters]
def mul(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def identity(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mpow(a,n):
 b=identity(len(a))
 while n:
  if n&1:b=mul(b,a)
  a=mul(a,a);n//=2
 return b

def det(a):
 n=len(a);s=0
 for p in permutations(range(n)):
  sign=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n));v=sign
  for i in range(n):v*=a[i][p[i]]
  s+=v
 return s

def torsion(a,n):
 b=mpow(a,n);return abs(det([[b[i][j]-int(i==j) for j in range(len(a))] for i in range(len(a))]))

def verify_t1():
 a=mat(PHI,'abc');m=mat(PHI,'abcde');b=[[0,1],[1,1]]
 assert all(sub(sub(x,PSI),PHI)==x==sub(sub(x,PHI),PSI) for x in PHI)
 assert det(a)==1 and det(m)==-1
 rows=[]
 for n in range(1,21):
  t,u,v=torsion(a,n),torsion(m,n),torsion(b,n)
  assert t>0 and u==t*v and v>0
  rows.append({'n':n,'Gamma_torsion_order':t,'G_torsion_order':u,'ratio':v})
 # Polynomial evaluations at seven points certify the characteristic polynomials.
 for x in range(-3,4):
  char=lambda c:det([[int(i==j)*x-c[i][j] for j in range(len(c))] for i in range(len(c))])
  assert char(a)==x**3-x-1
  assert char(m)==(x**3-x-1)*(x**2-x-1)
 return {'matrices':{'lower':a,'full':m,'quotient':b},'cyclic_cover_torsion':rows}

# Degree-two noncommutative Magnus expansions use tuples of generator indices.
def magmul(p,q):
 r={}
 for a,x in p.items():
  for b,y in q.items():
   if len(a+b)<=2:r[a+b]=r.get(a+b,0)+x*y
 return {a:x for a,x in r.items() if x}
def maginv(p):
 h={a:x for a,x in p.items() if a};r={():1}
 for a,x in h.items():r[a]=r.get(a,0)-x
 for a,x in magmul(h,h).items():r[a]=r.get(a,0)+x
 return {a:x for a,x in r.items() if x}
def magword(w):
 p={():1}
 for a in w:
  g={():1,('abc'.index(a.lower()),):1};p=magmul(p,g if a.islower() else maginv(g))
 return p
ALPHA_MAG=[magword('b'),magword('c'),magword('ab')]
def magsub(p):
 r={}
 for a,x in p.items():
  v={():1}
  for i in a:v=magmul(v,{j:y for j,y in ALPHA_MAG[i].items() if j})
  for j,y in v.items():r[j]=r.get(j,0)+x*y
 return {a:x for a,x in r.items() if x}
def magcorrect(w,c):
 p=magword(w)
 for (i,j),x in zip([(0,1),(0,2),(1,2)],c):p[(i,j)]=p.get((i,j),0)+x;p[(j,i)]=p.get((j,i),0)-x
 return {a:x for a,x in p.items() if x}
def verify_t2():
 from fractions import Fraction as Q
 u=[Q(-2,5),Q(6,5),Q(2,5)];v=[Q(-1,5),Q(-2,5),Q(1,5)]
 x=magcorrect('ABc',u);y=magcorrect('C',v)
 assert magsub(x)==magmul(y,magword('a'))
 assert magsub(y)==magmul(y,x)
 # Derive six independent affine equations by evaluating their Magnus coefficients.
 def residual(c):
  x=magcorrect('ABc',c[:3]);y=magcorrect('C',c[3:]);out=[]
  for l,r in [(magsub(x),magmul(y,magword('a'))),(magsub(y),magmul(y,x))]:
   out.extend(l.get(k,0)-r.get(k,0) for k in [(0,1),(0,2),(1,2)])
  return out
 c0=residual([0]*6);matrix=[]
 for j in range(6):
  c=[0]*6;c[j]=1;matrix.append([a-b for a,b in zip(residual(c),c0)])
 E=[list(row) for row in zip(*matrix)]
 assert all(sum(a*b for a,b in zip(row,u+v))==-z for row,z in zip(E,c0))
 assert abs(det(E))==5
 # Commutators give the stated integral basis, with our convention xyX Y.
 for (i,j) in [(0,1),(0,2),(1,2)]:
  w='abc'[i]+'abc'[j]+'ABC'[i]+'ABC'[j]
  assert magword(w)=={():1,(i,j):1,(j,i):-1}
 return {'linear_system_matrix':E,'constant':c0,'determinant':det(E),'unique_rational_u':list(map(str,u)),'unique_rational_v':list(map(str,v)),'integral_solution':False}

def verify_t3():
 theta={x:sub(sub(sub(x))) for x in PHI}
 assert theta=={'a':'ab','b':'bc','c':'cab','d':'edeac','e':'edeaedb'}
 assert min(map(len,theta.values()))==2 and max(map(len,theta.values()))==7
 P,S='ed','aedb';w='e';center=0;rows=[]
 for n in range(1,5):
  center=len(sub(w[:center],theta))+len(P);w=sub(w,theta)
  assert w[center]=='e';rows.append({'n':n,'length':len(w),'left':center,'right':len(w)-center-1})
 pp,ss=P,S
 for _ in range(3):pp=sub(pp,theta);ss=sub(ss,theta)
 assert rows[2]=={'n':3,'length':162,'left':73,'right':88}
 assert len(pp)==267 and len(ss)==288
 assert min(rows[2]['left'],rows[2]['right'],len(pp),len(ss))>35
 low='a';top='e'
 for _ in range(6):low=sub(low,theta)
 for _ in range(7):top=sub(top,theta)
 assert low in top
 lang={low[i:i+k] for k in range(1,13) for i in range(len(low)-k+1)}
 assert all(z in top for z in lang)
 a='a'
 for _ in range(5):a=sub(a)
 assert a=='cab'
 return {'theta':theta,'top_centered_cores':rows,'BCC_bound':35,'theta3_P_length':len(pp),'theta3_S_length':len(ss),'lower_seed_phi5_a':a,'finite_language_words_checked':len(lang),'all_finite_control_words_in_top':True}

def rank(a):
 from fractions import Fraction as Q
 a=[list(map(Q,row)) for row in a];r=0
 for j in range(len(a[0])):
  z=next((i for i in range(r,len(a)) if a[i][j]),None)
  if z is None:continue
  a[r],a[z]=a[z],a[r];q=a[r][j];a[r]=[v/q for v in a[r]]
  for i in range(len(a)):
   if i!=r:
    q=a[i][j];a[i]=[v-q*w for v,w in zip(a[i],a[r])]
  r+=1
 return r

def verify_t4():
 from itertools import combinations
 from search_periodic import class2,PAIR,V
 m=mat(PHI,'abcde')
 w=[[m[i][k]*m[j][l]-m[i][l]*m[j][k] for k,l in PAIR] for i,j in PAIR]
 assert [sum(a*b for a,b in zip(row,V)) for row in w]==[-a for a in V]
 assert rank([[w[i][j]+int(i==j) for j in range(10)] for i in range(10)])==9
 assert rank([[w[i][j]-int(i==j) for j in range(10)] for i in range(10)])==10
 for k,(i,j) in enumerate(PAIR):
  comm='abcde'[i]+'abcde'[j]+'ABCDE'[i]+'ABCDE'[j]
  assert class2(sub(comm))==tuple(row[k] for row in w)
 q={'d':'e','e':'ed'}
 comm='deDE'
 assert conjugacy_key(sub(comm,q))==conjugacy_key(inv(comm))
 assert conjugacy_key(sub(comm)) not in {conjugacy_key(comm),conjugacy_key(inv(comm))}
 return {'exterior_square_matrix':w,'minus_one_eigenvector':list(V),'rank_W_plus_I':9,'rank_W_minus_I':10,'quotient_commutator_is_inverted_up_to_conjugacy':True,'full_first_image_not_periodic_or_inverse':True}

def run_summary(w):
 p=0
 for a in w:
  if a not in 'abc':break
  p+=1
 s=0
 for a in w[::-1]:
  if a not in 'abc':break
  s+=1
 z=m=0
 for a in w:
  z=z+1 if a in 'abc' else 0;m=max(m,z)
 return len(w),p,s,m

def summary_concat(a,b):
 n,p,s,m=a;nn,pp,ss,mm=b
 return n+nn,p+pp if p==n else p,ss+s if ss==nn else ss,max(m,mm,s+pp)

def verify_t5():
 import math
 summaries={x:run_summary(x) for x in PHI};counts={x:[int(x==y) for y in PHI] for x in PHI};words={x:x for x in PHI};rows=[]
 for n in range(1,101):
  new={};newcounts={}
  for x,path in PHI.items():
   s=(0,0,0,0);c=[0]*5
   for y in path:s=summary_concat(s,summaries[y]);c=[a+b for a,b in zip(c,counts[y])]
   new[x]=s;newcounts[x]=c
  summaries,counts=new,newcounts
  if n<=15:
   words={x:sub(w) for x,w in words.items()}
   assert all(summaries[x]==run_summary(words[x]) for x in PHI)
   assert all(counts[x]==[words[x].count(y) for y in PHI] for x in PHI)
  if n in [5,10,15,20,30,50,100]:
   w=summaries['e'];c=counts['e'];rows.append({'n':n,'total_length':w[0],'longest_lower_run':w[3],'letter_counts':c})
 tau=(1+math.sqrt(5))/2;lo,hi=1.,1.4
 for _ in range(60):
  mid=(lo+hi)/2
  if mid**3-mid-1>0:hi=mid
  else:lo=mid
 rho=(lo+hi)/2;v=[1,1,tau-1,1,tau];m=mat(PHI,'abcde')
 assert max(abs(sum(a*b for a,b in zip(r,v))-tau*x) for r,x in zip(m,v))<1e-12
 last=rows[-1];frequency=(last['letter_counts'][3]+last['letter_counts'][4])/last['total_length']
 assert abs(frequency-.5)<1e-8
 return {'rows':rows,'tau':tau,'rho':rho,'gap_exponent':math.log(rho)/math.log(tau),'top_letter_frequency_n100':frequency,'limit_top_frequency':.5,'explicit_word_crosscheck_through_n':15}

if __name__=='__main__':
 print(json.dumps({'turn1':verify_t1(),'turn2':verify_t2(),'turn3':verify_t3(),'turn4':verify_t4(),'turn5':verify_t5()},indent=2,sort_keys=True))
