"""Own finite enumeration. No external solution tables or executable code."""
from itertools import permutations,product
from collections import Counter
import json
from pathlib import Path

def comp(a,b):return tuple(a[x] for x in b)
def invert(a):return tuple(a.index(x) for x in range(len(a)))
def lift(p,m,i,n=3):
 o=[]
 for v in product(range(m),repeat=n):
  w=list(v);u=p[m*w[i]+w[i+1]];w[i],w[i+1]=divmod(u,m);y=0
  for z in w:y=m*y+z
  o.append(y)
 return tuple(o)
def powers(p):
 seen=set();q=tuple(range(len(p)));out=[]
 while q not in seen:seen.add(q);out.append(q);q=comp(p,q)
 return out

def enumerate_solutions(m):
 sols=[]
 for p in permutations(range(m*m)):
  if any(len({p[m*x+y]//m for y in range(m)})<m for x in range(m)):continue
  if any(len({p[m*x+y]%m for x in range(m)})<m for y in range(m)):continue
  a=lift(p,m,0);b=lift(p,m,1)
  if comp(a,comp(b,a))==comp(b,comp(a,b)):sols.append(p)
 return sols

def welded(r,s,m,kind=1):
 a,b=lift(r,m,0),lift(r,m,1);c,d=lift(s,m,0),lift(s,m,1)
 if comp(c,comp(b,c))!=comp(d,comp(a,d)):return False
 if kind==1:return comp(c,comp(b,a))==comp(b,comp(a,d))
 return comp(a,comp(b,c))==comp(d,comp(a,b))
def derived(r,m):
 lam=[[r[m*x+y]//m for y in range(m)] for x in range(m)]
 return tuple(m*y+lam[y][r[m*x+lam[x].index(y)]%m] for x in range(m) for y in range(m))
def guitar(r,m,n):
 lam=[[r[m*x+y]//m for y in range(m)] for x in range(m)];out=[]
 for v in product(range(m),repeat=n):
  w=[]
  for i in range(n):
   y=v[i]
   for j in reversed(range(i)):y=lam[v[j]][y]
   w.append(y)
  e=0
  for y in w:e=m*e+y
  out.append(e)
 return tuple(out)

def trace_word(gens,word):
 p=tuple(range(len(gens[0])))
 for j in reversed(word):p=comp(gens[j],p)
 return sum(i==x for i,x in enumerate(p))

def main():
 records=[]
 for m in [2,3]:
  sols=enumerate_solutions(m);invol=[x for x in sols if comp(x,x)==tuple(range(m*m))];C=Counter();examples=[]
  for r in sols:
   rp=derived(r,m);assert rp in sols
   J=guitar(r,m,3);assert len(set(J))==m**3;JI=invert(J)
   for i in [0,1]:assert comp(J,comp(lift(r,m,i),JI))==lift(rp,m,i)
   for ss in invol:
    for kind in [1,2]:
     if not welded(r,ss,m,kind):continue
     C[f'welded_kind_{kind}']+=1
     # A fixed J2 determines a candidate local q; test its compatibility at n3.
     J2=guitar(r,m,2);qq=comp(J2,comp(ss,invert(J2)))
     T=[comp(J,comp(lift(ss,m,i),JI)) for i in [0,1]]
     local=T==[lift(qq,m,i) for i in [0,1]]
     C[f'guitar_local_kind_{kind}']+=int(local)
     if not local and len([z for z in examples if z['kind']==kind])<2:
      examples.append({'kind':kind,'r':r,'s':ss,'rprime':rp,'J2_q':qq,'transported_s1':T[0],'transported_s2':T[1]})
     qs=[q for q in invol if welded(rp,q,m,kind)]
     if not qs:C[f'no_local_partner_kind_{kind}']+=1;examples.append({'kind':kind,'no_partner':True,'r':r,'s':ss,'rprime':rp})
  record={'size':m,'solutions':len(sols),'involutive_solutions':len(invol),'counts':dict(C),'examples':examples};records.append(record);print(m,len(sols),len(invol),dict(C),flush=True)
 Path(__file__).with_name('small_search.json').write_text(json.dumps(records,indent=2)+'\n')
if __name__=='__main__':main()
