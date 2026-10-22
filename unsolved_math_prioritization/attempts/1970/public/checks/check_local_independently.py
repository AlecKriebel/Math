#!/usr/bin/env python3
"""Independent local certificate check using closed-form binomial convolution.
No reconstructed lane code is imported. For bottom word z and defect (s,t):
x(a,b)=(1-(-2)^b)/3 + (-1)^b sum_j binom(b,j)z[a+j]
        + 1_(b>t) (-1)^(b-t-1) binom(b-t-1,s-a).
A binomial coefficient outside its range is zero. Widths decrease by at least
one, so every required ancestral vertex exists. This is a closed-form check of
the affine recurrence, independently evaluated for each coordinate.
"""
from itertools import product
from math import comb
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
def need(x,s):
    if not x:raise ValueError(s)
def widths(x):
    result=[];p=1
    while p<=x:result.append((x//p).bit_length()-1);p*=3
    return result

def evaluate(w,z,defect=None):
    answer=[]
    for b,width in enumerate(w):
        row=[]
        for a in range(width+1):
            value=(1-(-2)**b)//3+(-1)**b*sum(comb(b,j)*z[a+j] for j in range(b+1))
            if defect is not None:
                s,t=defect; h=b-t-1
                if h>=0 and 0<=s-a<=h:value+=(-1)**h*comb(h,s-a)
            if value not in (0,1):return None
            row.append(value)
        answer.append(row)
    return answer

def phase(w,r):return [[int((a+2*b)%3==r) for a in range(v+1)] for b,v in enumerate(w)]
def compare_suffix():
    cert=json.loads((ROOT/'fixtures/check_single_defect.json').read_text())
    result=[]
    expected_intervals=list(zip([2187,2304,2592,2916,3072,3456,3888,4096],[2304,2592,2916,3072,3456,3888,4096,4374]))
    for (lo,hi),r in product(expected_intervals,range(3)):
        w=widths(lo);base=phase(w,r);iso=w[0]-w[1]==2
        size=sum(map(sum,base))-(base[0][-1] if iso else 0)
        found=[]
        for s in range(4,w[0]):
            for t in range(3):
                if s>w[t+1]:continue
                for zz in product((0,1),repeat=w[0]-4):
                    z=base[0][:5]+list(zz)
                    if iso and z[-1]:continue
                    arr=evaluate(w,z,(s,t))
                    if arr is None:continue
                    need(all(arr[b][0]==base[b][0] for b in range(len(w))),'independent interface leakage')
                    delta=sum(map(sum,arr))-size
                    change=[[a,b,v-base[b][a]] for b,row in enumerate(arr) for a,v in enumerate(row) if v!=base[b][a]]
                    found.append({'defect':[s,t],'tail':list(zz),'size_difference':delta,'left_column_agrees':True,'changes_from_raw_phase':change})
        target=next(x for x in cert['suffix_cases'] if x['interval']==[lo,hi] and x['phase']==r)
        need(found==target['configurations'],'closed-form suffix mismatch')
        result.append({'interval':[lo,hi],'phase':r,'count':len(found),'minimum_difference':min(x['size_difference'] for x in found),'configuration_sha256':hashlib.sha256(json.dumps(found,sort_keys=True).encode()).hexdigest()})
    return result

def run():
    three=[''.join(map(str,z)) for z in product((0,1),repeat=4) if evaluate([3,2,1,0],z) is not None]
    need(three==['0010','0100','1001'],'exact stencil mismatch')
    seven=[]
    for t in range(3):
        count=sum(evaluate(list(range(7,-1,-1)),z,(3,t)) is not None for z in product((0,1),repeat=8))
        need(count==0,'interior defect survived')
        seven.append(count)
    six=[]
    for s,t in product(range(3),repeat=2):
        for z in product((0,1),repeat=7):
            arr=evaluate(list(range(6,-1,-1)),z,(s,t))
            if arr is not None:six.append({'defect':[s,t],'bottom':list(z)})
    cert=json.loads((ROOT/'fixtures/check_single_defect.json').read_text())
    expected=[{'defect':c['defect'],'bottom':v['bottom']} for c in cert['left_stencils'] for v in c['candidates']]
    need(six==expected and len(six)==6,'left stencil mismatch')
    suffix=compare_suffix()
    need(sum(x['count'] for x in suffix)==173,'unexpected suffix survivor total')
    return {'status':'PASS','method':'Independent closed-form integer binomial evaluation at every vertex; no lane code imported','T3_words':three,'T7_survivors':seven,'T6_survivors':six,'suffix_cases':suffix}
if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
