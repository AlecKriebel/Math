#!/usr/bin/env python3
"""Independent reconstruction audit; does not import any reconstructed lane code.
Rows use 3-adic exponent and bit positions use 2-adic exponent, transposing
finite_solver.py. A separate vertex include/exclude algorithm checks full
integer intervals without using smooth-component structure.
No assert statement is used, so checks remain active under -O and -OO.
"""
from functools import lru_cache
from math import gcd
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
class AuditFailure(RuntimeError): pass
def need(ok, why):
    if not ok: raise AuditFailure(why)

def smooth_below(x):
    out=[]
    p=1
    while p<=x:
        q=p
        while q<=x:
            out.append(q); q*=3
        p*=2
    return sorted(out)

def smooth_prefix(n):
    bound=1
    while len(smooth_below(bound))<n: bound*=2
    return smooth_below(bound)[:n]

def row_widths(x):
    out=[]; p=1
    while p<=x:
        out.append((x//p).bit_length()); p*=3
    return out

@lru_cache(None)
def transposed_min(x):
    widths=row_widths(x)
    # For every current row mask record optimum cardinality and multiplicity.
    costs=[m.bit_count() for m in range(1<<widths[0])]
    ways=[1]*len(costs)
    infinity=sum(widths)+1
    for h,k in zip(widths,widths[1:]+[0]):
        need(h>=k and h-k<=2, 'unexpected adjacent row-width drop')
        low=(1<<k)-1
        lower=[infinity]*(1<<k); totals=[0]*(1<<k)
        for row,cost,count in zip(range(1<<h),costs,ways):
            missing=low & ~(row | row>>1)
            if cost<lower[missing]:
                lower[missing]=cost; totals[missing]=count
            elif cost==lower[missing]: totals[missing]+=count
        # Sum/min over all demands contained in the chosen next row.
        for bit in range(k):
            f=1<<bit
            for mask in range(1<<k):
                if mask&f:
                    prev=mask^f
                    if lower[prev]<lower[mask]:
                        lower[mask]=lower[prev];totals[mask]=totals[prev]
                    elif lower[prev]==lower[mask]:totals[mask]+=totals[prev]
        costs=[c+m.bit_count() for m,c in enumerate(lower)]
        ways=totals
    return costs[0],ways[0]

def canonical(edges):
    distinct=sorted(set(edges),key=lambda e:(e.bit_count(),e))
    if distinct and distinct[0]==0: return (0,)
    out=[]
    for e in distinct:
        if not any((f&e)==f for f in out):out.append(e)
    return tuple(sorted(out))

@lru_cache(None)
def vertex_branch(edges):
    if not edges:return 0
    if edges[0]==0:return 10**9
    single=next((e for e in edges if e&(e-1)==0),None)
    if single is not None:
        return 1+vertex_branch(canonical(e for e in edges if not e&single))
    frequency={}
    for edge in edges:
        while edge:
            v=edge&-edge; edge-=v
            frequency[v]=frequency.get(v,0)+1
    v=max(frequency,key=frequency.get)
    include=1+vertex_branch(canonical(e for e in edges if not e&v))
    exclude=vertex_branch(canonical(e&~v for e in edges))
    return min(include,exclude)

def direct_integer_tau(n):
    edges=canonical(sum(1<<(v-1) for v in (m,2*m,3*m)) for m in range(1,n//3+1))
    return vertex_branch(edges)

def direct_smooth_tau(x):
    ss=smooth_below(x);index={v:i for i,v in enumerate(ss)}
    edges=canonical(sum(1<<index[v] for v in (m,2*m,3*m)) for m in ss if 3*m<=x)
    return vertex_branch(edges)

def q_data(x):
    counts=[0]*3;vs={};p=1;a=0
    while p<=x:
        q=p;b=0
        while q<=x:
            vs[q]=(a,b);q*=3;b+=1
        p*=2;a+=1
    active={v for m in vs if 3*m<=x for v in (m,2*m,3*m)}
    for v in active:
        a,b=vs[v]; counts[(a+2*b)%3]+=1
    corrected=counts[:]; m=0
    while 24*2**m<=x:
        if x<27*2**m:corrected[(m+2)%3]-=1
        m+=1
    return min(counts),min(corrected)

def run():
    values=smooth_prefix(77)
    exact=[]
    for k,x in enumerate(values,1):
        tau,count=transposed_min(x)
        if k<=45:
            need(direct_smooth_tau(x)==tau,f'vertex branching mismatch at {k}')
        q0,q1=q_data(x)
        exact.append({'index':k,'X':x,'tau':tau,'optimal_count':count,'q0_color_candidate':q0,'q1_terminal_candidate':q1})
    interval=[]
    for n in range(1,81):
        direct=direct_integer_tau(n)
        decomposed=sum(transposed_min(n//m)[0] for m in range(1,n+1) if gcd(m,6)==1)
        need(direct==decomposed,f'integer interval decomposition mismatch at {n}')
        interval.append({'N':n,'minimum_deletions':direct,'F':n-direct})
    numeric=json.loads((ROOT/'fixtures/exact/tau_through_X192.json').read_text())
    for entry in numeric:
        need(entry['X']<=192,'numeric cutoff file exceeded stated domain')
        expected=next((r for r in exact if r['index']==entry['index']),None)
        need(expected is not None and entry['X']==expected['X'] and entry['tau']==expected['tau'],'numeric cutoff certificate mismatch')
    negative={}
    for name,bad in [('wrong_tau',lambda:need(exact[23]['tau']==8,'incorrect tau rejected')),('wrong_count',lambda:need(exact[23]['optimal_count']==0,'incorrect count rejected')),('wrong_endpoint',lambda:need(smooth_below(3)==[1,2],'inclusive endpoint rejected')),('wrong_color_model',lambda:need(transposed_min(1536)[0]==q_data(1536)[0],'color class equality rejected'))]:
        try:bad()
        except AuditFailure:negative[name]='rejected'
        else:raise AuditFailure('negative control accepted: '+name)
    return {'status':'PASS','construction':'new independent audit reconstruction, not historical artifact restoration','smooth_transposed_range':[1,77],'smooth_vertex_branch_range':[1,45],'integer_interval_vertex_branch_range':[1,80],'finite_only':True,'all_scale_q1_theorem_inferred':False,'negative_controls':negative,'smooth':exact,'interval':interval}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
