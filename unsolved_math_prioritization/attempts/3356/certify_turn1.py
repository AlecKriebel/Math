"""Exhaustive exact certificate: no probable-prime test or external dependency.
For each prime q in range, certify p=16*q**4+1 composite, or certify
simultaneously p prime and 3 primitive by the complete-factorization Lucas test.
"""
from math import gcd, isqrt
from collections import Counter
from pathlib import Path
import argparse, hashlib, json, time

def primes(n):
    a=bytearray(b'\1')*(n+1)
    a[:2]=b'\0\0'
    for k in range(2,isqrt(n)+1):
        if a[k]:a[k*k:n+1:k]=b'\0'*(((n-k*k)//k)+1)
    return [k for k in range(5,n+1) if a[k]]

def certify(n):
    count=Counter(); rows=[]; unresolved=[]; prime_rows=[]
    for q in primes(n):
        p=16*q**4+1;N=p-1
        fermat=pow(3,N,p)
        if fermat!=1:
            row=[q,p,'fermat_composite',fermat]
        else:
            r2=pow(3,N//2,p);rq=pow(3,N//q,p)
            g2=gcd(r2-1,p);gq=gcd(rq-1,p)
            if g2==gq==1:
                row=[q,p,'lucas_prime_primitive',r2,rq];prime_rows.append(row)
            elif 1<g2<p:row=[q,p,'factor_composite',g2]
            elif 1<gq<p:row=[q,p,'factor_composite',gq]
            else:row=[q,p,'unresolved',fermat,r2,rq,g2,gq];unresolved.append(row)
        count[row[2]]+=1;rows.append(row)
    encoded=json.dumps(rows,separators=(',',':')).encode()
    out={'bound_q_inclusive':n,'q_primes_tested':len(rows),'outcomes':dict(count),'unresolved':unresolved,'certificate_rows_sha256':hashlib.sha256(encoded).hexdigest(),'first_20_prime_cases':prime_rows[:20],'last_prime_case':prime_rows[-1] if prime_rows else None,'largest_p_considered':rows[-1][1] if rows else None,'qualification':'Exact finite-range certificate only; no universal conclusion.'}
    assert not unresolved,unresolved
    return out,rows
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--bound',type=int,default=1000000);ap.add_argument('--output',type=Path);ap.add_argument('--rows',type=Path);a=ap.parse_args()
    out,rows=certify(a.bound)
    if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
    if a.rows:a.rows.write_text(json.dumps(rows,separators=(',',':'))+'\n')
    print(json.dumps(out,indent=2))
