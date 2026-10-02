"""Segmented exact counterexample search with polynomial compositeness sieve.
No probable-prime test. Every prime q gets a factor, Fermat, or complete Lucas certificate.
The per-q stream is hashed, not retained; --bound and --segment reproduce it exactly.
"""
from math import isqrt,gcd
from pathlib import Path
from collections import Counter
import argparse,json,hashlib,time

def small_primes(n):
 a=bytearray(b'\1')*(n+1);a[:2]=b'\0\0'
 for r in range(2,isqrt(n)+1):
  if a[r]:a[r*r:n+1:r]=b'\0'*(((n-r*r)//r)+1)
 return [r for r in range(2,n+1)if a[r]]

def scan(bound,segment):
 bases=small_primes(isqrt(bound));wheel=[]
 for r in small_primes(1000):
  if r%8==1:
   roots=[a for a in range(r)if(16*pow(a,4,r)+1)%r==0]
   assert len(roots)==4
   wheel.append((r,roots))
 counts=Counter();digest=hashlib.sha256();nq=0;first=[];last=[];unresolved=[];t0=time.time()
 for lo in range(5,bound+1,segment):
  hi=min(bound+1,lo+segment);sz=hi-lo;flags=bytearray(b'\1')*sz
  for r in bases:
   start=max(r*r,((lo+r-1)//r)*r)
   if start<hi:flags[start-lo:sz:r]=b'\0'*(((hi-1-start)//r)+1)
  factors=bytearray(sz)
  for idx,(r,roots)in enumerate(wheel,1):
   for a in roots:
    start=lo+(a-lo)%r
    if start<hi:factors[start-lo:sz:r]=bytes([idx])*(((hi-1-start)//r)+1)
  for i,prime in enumerate(flags):
   if not prime:continue
   q=lo+i;p=16*q**4+1;N=p-1;nq+=1
   if factors[i]:
    d=wheel[factors[i]-1][0];assert 1<d<p and p%d==0
    row=[q,p,'small_factor',d]
   else:
    a=pow(3,N,p)
    if a!=1:row=[q,p,'fermat_composite',a]
    else:
     a2=pow(3,N//2,p);aq=pow(3,N//q,p)
     g2=gcd(a2-1,p);gq=gcd(aq-1,p)
     if g2==gq==1:
      row=[q,p,'lucas_prime_primitive',a2,aq]
      if len(first)<10:first.append(row)
      last=(last+[row])[-10:]
     elif 1<g2<p:row=[q,p,'factor_composite',g2]
     elif 1<gq<p:row=[q,p,'factor_composite',gq]
     else:
      row=[q,p,'unresolved',a,a2,aq,g2,gq];unresolved.append(row)
      print('UNRESOLVED',row,flush=True)
   counts[row[2]]+=1;digest.update((json.dumps(row,separators=(',',':'))+'\n').encode())
  if (lo-5)//segment%20==19:print('progress',hi-1,nq,dict(counts),round(time.time()-t0,2),flush=True)
 out={'bound_q_inclusive':bound,'segment_size':segment,'q_primes_tested':nq,'counts':dict(counts),'polynomial_sieve_primes':[r for r,_ in wheel],'certificate_stream_sha256':digest.hexdigest(),'unresolved':unresolved,'first_prime_cases':first,'last_prime_cases':last,'qualification':'Exact finite-range result only; no per-q stream is retained, all data reproducible from this script.','elapsed_seconds':round(time.time()-t0,3)}
 assert not unresolved,unresolved
 return out
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--bound',type=int,default=100000000);a.add_argument('--segment',type=int,default=1000000);a.add_argument('--output',type=Path,required=True);args=a.parse_args()
 out=scan(args.bound,args.segment);args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
