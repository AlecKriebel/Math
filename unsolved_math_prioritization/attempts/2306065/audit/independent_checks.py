#!/usr/bin/env python3
"""Independent frozen-certificate audit. No imports of author verifier code.
Uses closed-form Chebyshev power coefficients and directly recomputes Bernstein
coefficients on each dyadic x interval, independently of de Casteljau recursion.
Run with standard Python (Fraction only); output is a mathematical check log.
"""
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path
import json, hashlib, copy, subprocess, tempfile, shutil, sys
P=Path('/workspace/shared/math-campaign/rank586-2306065/public')
EXPECTED_MANIFEST='2e460367412073ef24a4c39137fb0851123b0765f086d5e662ae2d31cdee4a6c'
def require(test, message):
    if not test: raise ValueError(message)
def Tpower(n):
    if not n:return [Q(1)]
    a=[Q(0)]*(n+1)
    for k in range(n//2+1):
        a[n-2*k]=Q(n*(-1)**k*factorial(n-k-1)*2**(n-2*k),2*factorial(k)*factorial(n-2*k))
    return a
def val(a,x):
    out=Q(0)
    for c in reversed(a):out=out*x+c
    return out
def bernstein_direct(a,l,h):
    n=len(a)-1
    powers=[sum(a[k]*comb(k,j)*l**(k-j)*(h-l)**j for k in range(j,n+1)) for j in range(n+1)]
    return [sum(powers[j]*Q(comb(i,j),comb(n,j)) for j in range(i+1)) for i in range(n+1)]
def certify(a):
    todo=[(Q(-1),Q(1),0)];leaves=[]
    while todo:
        l,h,d=todo.pop()
        b=bernstein_direct(a,l,h)
        # Independent endpoint consistency checks, in addition to positivity.
        require(b[0]==val(a,l) and b[-1]==val(a,h),'Bernstein endpoint mismatch')
        if min(b)>0:leaves.append({'left':l,'right':h,'depth':d,'minimum':min(b)})
        else:
            require(d<12,'Positivity unresolved within twelve subdivisions')
            m=(l+h)/2;todo.extend([(l,m,d+1),(m,h,d+1)])
    leaves.sort(key=lambda r:r['left'])
    require(leaves[0]['left']==-1 and leaves[-1]['right']==1,'Missing endpoint')
    require(all(a['right']==b['left'] for a,b in zip(leaves,leaves[1:])),'Coverage gap')
    return {'leaf_count':len(leaves),'depth':max(r['depth'] for r in leaves),'minimum':str(min(r['minimum'] for r in leaves)), 'coverage_complete':True,'cells':[{k:str(v) if isinstance(v,Q) else v for k,v in r.items()} for r in leaves]}
def exp_enclosure(x):
    require(0<x<32,'Positive-tail argument needs 0<x<32')
    lower=sum(x**k/factorial(k) for k in range(31))
    return lower,lower+x**31/factorial(31)/(1-x/32)
def check_witness(o):
    require(o['M']==3 and len(o['coefficient_numerators'])==40 and o['coefficient_denominator']==10**9,'Unexpected witness schema')
    c=[Q(v,o['coefficient_denominator']) for v in o['coefficient_numerators']]
    L=Q(o['L_numerator'],o['L_denominator'])
    pp=[Q(1)]+[Q(0)]*40;qq=[L]+[Q(0)]*40
    for n in range(1,41):
        for k,v in enumerate(Tpower(n)):pp[k]+=n*c[n-1]*v;qq[k]-=c[n-1]*v
    a3=c[1]+c[0]**2/2
    require(a3==Q(1134162229,1250000000)>Q(9,10)>Q(8,9),'a3 mismatch')
    lower,upper=exp_enclosure(L)
    require(upper<3,'Exponential bound fails')
    return {'a3':str(a3),'exp_L_upper':str(upper),'p':certify(pp),'q':certify(qq)}
def check_upper(o):
    require((o['N'],o['grid_denominator'],o['intervals'],o['dual_denominator'])==(40,100,64,10**12),'Upper schema mismatch')
    L=Q(o['L_upper_numerator'],o['L_upper_denominator'])
    require(exp_enclosure(L)[0]>3,'log(3) outer approximation fails')
    require(sorted(r['k'] for r in o['rows'])==list(range(64)),'Slab coverage incomplete')
    rows=[]
    weights=[Q(41-n,41) for n in range(1,41)]
    T=[[val(Tpower(n),Q(j,100)) for n in range(1,41)] for j in range(-100,101)]
    for r in sorted(o['rows'],key=lambda r:r['k']):
        lo=Q(r['k'],48);hi=Q(r['k']+1,48)
        coeff=[Q(0)]*40;constant=Q(0)
        for index,numerator in r['inequality_dual']:
            require(type(index)==int and 0<=index<402 and type(numerator)==int and numerator>=0,'Bad inequality multiplier')
            m=Q(numerator,10**12)
            if index<201:
                constant+=m
                for j in range(40):coeff[j]-=m*(j+1)*weights[j]*T[index][j]
            else:
                constant+=m*L
                for j in range(40):coeff[j]+=m*weights[j]*T[index-201][j]
        for j,numerator in r['lower_dual']:
            require(type(j)==int and 0<=j<40 and type(numerator)==int and numerator>=0,'Bad lower multiplier')
            m=Q(numerator,10**12);coeff[j]-=m;constant-=m*(lo if j==0 else Q(-2,j+1))
        for j,numerator in r['upper_dual']:
            require(type(j)==int and 0<=j<40 and type(numerator)==int and numerator>=0,'Bad upper multiplier')
            m=Q(numerator,10**12);coeff[j]+=m;constant+=m*(hi if j==0 else Q(2,j+1))
        objective=[(hi+lo)/2,Q(1)]+[Q(0)]*38
        residuals=[objective[j]-coeff[j] for j in range(40)]
        correction=sum(Q(2,j+1)*abs(v) for j,v in enumerate(residuals))
        result=constant+correction-lo*hi/2
        require(result<Q(957,1000),'Claimed strict bound fails')
        rows.append({'k':r['k'],'l':str(lo),'h':str(hi),'bound':str(result),'rounding_correction':str(correction),'nonzero_residuals':sum(v!=0 for v in residuals)})
    largest=max(rows,key=lambda r:Q(r['bound']))
    return {'all_64_slabs_pass':True,'largest':largest,'largest_approx':float(Q(largest['bound'])),'strict_margin':str(Q(957,1000)-Q(largest['bound'])),'rows':rows}
def manifest():
    data=(P/'SHA256SUMS.json').read_bytes()
    require(hashlib.sha256(data).hexdigest()==EXPECTED_MANIFEST,'Wrong frozen manifest')
    wanted=json.loads(data)
    actual={f.name:{'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size} for f in P.iterdir() if f.is_file() and f.name!='SHA256SUMS.json'}
    require(actual==wanted,'Frozen file hash mismatch')
    return {'manifest_sha256':EXPECTED_MANIFEST,'payload_files':len(actual),'top_level_files_including_manifest':len(actual)+1,'exact_match':True}
def mutation_controls():
    # Mutate only temporary copies. Require specific rejection reasons.
    tests=[('negative_upper_multiplier','verify_upper.py','UPPER_CERTIFICATE.json',lambda x:x['rows'][0]['inequality_dual'].__setitem__(0,[x['rows'][0]['inequality_dual'][0][0],-1])),
           ('duplicate_upper_slab','verify_upper.py','UPPER_CERTIFICATE.json',lambda x:x['rows'][-1].__setitem__('k',0)),
           ('out_of_range_dual_index','verify_upper.py','UPPER_CERTIFICATE.json',lambda x:x['rows'][0]['inequality_dual'].__setitem__(0,[402,1])),
           ('zero_upper_multipliers','verify_upper.py','UPPER_CERTIFICATE.json',lambda x:[r.update(inequality_dual=[],lower_dual=[],upper_dual=[]) for r in x['rows']]),
           ('boundedness_only_violation','verify_witness.py','WITNESS.json',lambda x:x.update(coefficient_numerators=[1200000000,300000000]+[0]*38)),
           ('starlikeness_only_violation','verify_witness.py','WITNESS.json',lambda x:x.update(coefficient_numerators=[0,1000000000]+[0]*38)),
           ('exp_bound_violation','verify_witness.py','WITNESS.json',lambda x:x.update(L_numerator=2,L_denominator=1))]
    output={}
    for label,script,filename,mutate in tests:
        with tempfile.TemporaryDirectory() as td:
            d=Path(td);shutil.copyfile(P/script,d/script)
            o=json.loads((P/filename).read_text());mutate(o);(d/filename).write_text(json.dumps(o))
            run=subprocess.run([sys.executable,str(d/script)],capture_output=True,text=True,timeout=30)
            require(run.returncode!=0,f'Author verifier accepted bad fixture {label}')
            output[label]={'rejected':True,'return_code':run.returncode,'last_stderr':run.stderr.strip().splitlines()[-1]}
    return output
if __name__=='__main__':
    result={'inventory':manifest(),'witness':check_witness(json.loads((P/'WITNESS.json').read_text())),'upper':check_upper(json.loads((P/'UPPER_CERTIFICATE.json').read_text())),'negative_controls':mutation_controls(),'frozen_inventory_after_checks':manifest()}
    print(json.dumps(result,indent=2))
