#!/usr/bin/env python3
"""Independently reconstruct the paper's seven rational bounds by term recurrence."""
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
import datetime
import json
import subprocess
import sys

def need(c,m):
    if not c:raise RuntimeError(m)
def exp_lo(x,n):
    term=total=Q(1)
    for k in range(1,n+1):
        term*=x/k;total+=term
    return total,term*x/(n+1)
def exp_hi(x,n):
    lo,first=exp_lo(x,n)
    need(0<=x<n+2,'positive tail range')
    return lo+first/(1-x/(n+2))
def root_hi(x):
    scale=10**8
    k=isqrt(x.numerator*scale**2//x.denominator)
    lo,hi=Q(k,scale),Q(k+1,scale)
    need(lo**2<=x<hi**2,'root lattice')
    return hi
def atan_pair(x):
    term=x;total=Q(0)
    for k in range(24):
        total+=term/(2*k+1);term*=-x*x
    return total,total+term/49
def fstr(x):return str(x.numerator)+'/'+str(x.denominator)
p,q=atan_pair(Q(1,3)),atan_pair(Q(1,7))
pi_low,pi_high=8*p[0]+4*q[0],8*p[1]+4*q[1]
tan_twice=2*Q(1,3)/(1-Q(1,3)**2)
need((tan_twice+Q(1,7))/(1-tan_twice/7)==1,'pi tangent identity')
need(Q(1772,1000)**2<pi_low<pi_high<Q(1773,1000)**2,'sqrt pi brackets')
need(exp_hi(Q(1),14)<Q(2719,1000),'e upper')
need(pi_high*exp_hi(Q(1),14)**3<128,'round attainment')
small=Q(1773,4000)*exp_hi(Q(7,20),14)
values=[small];regions=['(0,7/5]']
for k in range(14,20):
    a,b=Q(k,10),Q(k+1,10)
    A=b*root_hi(b)/exp_lo(3*b/4,50)[0]
    D=a*root_hi(a)*(4/exp_lo(15*a/4,50)[0]+18/exp_lo(35*a/4,50)[0])
    values.append(A+D);regions.append('['+str(a)+','+str(b)+']')
printed=[629002,631338,636143,639464,641172,641202,639541]
rows=[]
for region,value,p in zip(regions,values,printed):
    need(value<Q(p,10**6),'printed rational upper bound '+region)
    need(Q(p,10**6)<Q(321,500),'strict upper threshold')
    rows.append({'region':region,'independent_exact':fstr(value),
                 'printed_upper':fstr(Q(p,10**6)),'positive_margin':fstr(Q(p,10**6)-value)})
lower=Q(1772,2719)*Q(10000000-7092,10004000)
need(lower==Q(1106714561,1700054750),'displayed lower fraction')
need(lower-Q(13,20)==Q(3357947,3400109500),'displayed strict margin')
need(lower>Q(13,20)>Q(321,500)>Q(1773,4000),'threshold order')
Aroot=Path(__file__).resolve().parents[1]
fresh=subprocess.run([sys.executable,'-I','-B',str(Aroot/'trace_audit_01/check_trace_bounds.py')],
                     capture_output=True,text=True,cwd='/',timeout=30)
need(fresh.returncode==0 and not fresh.stderr,'fresh checker replay')
data=json.loads(fresh.stdout)
executable=[Q(data['small_time_bound_exact'])]+[Q(r['bound_exact']) for r in data['middle_intervals']]
need(executable==values,'independent/executable fractions differ')
need(json.loads((Aroot/'trace_audit_01/EXACT_RESULTS.json').read_bytes())==data,'stored result mismatch')
result={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS',
        'method':'term recurrences and integer isqrt, no candidate source imports; all acceptance rational',
        'seven_regions':rows,'cylinder_lower':fstr(lower),'margin_over_13_over_20':fstr(lower-Q(13,20)),
        'exact_fraction_identity_with_executable':True,'stored_receipt_identity':True,
        'round_attainment_128_gt_pi_e_cubed':True,'mathematical_analysis_proved_by_program':False}
(Aroot/'package_review_01/ARITHMETIC_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='seven_regions'},indent=2))
