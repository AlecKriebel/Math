#!/usr/bin/env python3
"""Reproducible finite controls. Floating-point spectra are exploratory, not certified."""
import argparse, itertools, json, math, platform
from fractions import Fraction as Q
import numpy as np
import scipy
from scipy.linalg import eigvalsh

def merge(intervals, tol=0.0):
    out=[]
    for a,b in sorted(intervals):
        if out and a <= out[-1][1]+tol: out[-1][1]=max(b,out[-1][1])
        else: out.append([a,b])
    return out

def score(intervals):
    """Largest-first bridge/gap score; intervals sorted and merged beforehand."""
    if len(intervals)<2:return math.inf
    gaps=[(intervals[i][1],intervals[i+1][0]) for i in range(len(intervals)-1)]
    result=math.inf
    for i,(a,b) in enumerate(gaps):
        g=b-a
        left=intervals[0][0]; right=intervals[-1][1]
        for j in range(i-1,-1,-1):
            if gaps[j][1]-gaps[j][0]>=g: left=gaps[j][1]; break
        for j in range(i+1,len(gaps)):
            if gaps[j][1]-gaps[j][0]>=g:right=gaps[j][0];break
        result=min(result,(a-left)/g,(right-b)/g)
    return result

def presentation_score(intervals, order):
    gaps=[(intervals[i][1],intervals[i+1][0]) for i in range(len(intervals)-1)]
    removed=[]; value=math.inf
    for i in order:
        a,b=gaps[i]
        left=max([intervals[0][0]]+[gaps[j][1] for j in removed if j<i])
        right=min([intervals[-1][1]]+[gaps[j][0] for j in removed if j>i])
        value=min(value,(a-left)/(b-a),(right-b)/(b-a)); removed.append(i)
    return value

F=[1,1]
for _ in range(14): F.append(sum(F[-2:]))

def bands(k,lam):
    q,p=F[k],F[k-1]
    if q<3: raise ValueError('This constructor requires q >= 3')
    n=np.arange(1,q+1,dtype=np.int64)
    potential=(((n+1)*p)//q-(n*p)//q).astype(float)*lam
    base=np.diag(potential)+np.diag(np.ones(q-1),1)+np.diag(np.ones(q-1),-1)
    endpoints=[]
    for sign in (1.,-1.):
        A=base.copy();A[0,-1]+=sign;A[-1,0]+=sign
        endpoints.extend(eigvalsh(A,driver='evr'))
    endpoints=np.sort(endpoints)
    return [[float(a),float(b)] for a,b in endpoints.reshape(-1,2)]

def trace_word_control():
    # Integer substitution words: 0,1,10,101,... match recurrence x_(j+1)=2x_j x_(j-1)-x_(j-2).
    words=['0','1']
    for _ in range(6):words.append(words[-1]+words[-2])
    count=0
    for E,lam in itertools.product([-2,-1,0,1,2],[Q(1,2),Q(1),Q(2)]):
        xs=[Q(1),Q(E,2),Q(E-lam,2)]
        for _ in range(6):xs.append(2*xs[-1]*xs[-2]-xs[-3])
        for k,w in enumerate(words):
            M=[[Q(1),Q(0)],[Q(0),Q(1)]]
            for c in w:
                v=E-lam*int(c)
                M=[[v*M[0][0]-M[1][0],v*M[0][1]-M[1][1]],[M[0][0],M[0][1]]]
            assert (M[0][0]+M[1][1])/2==xs[k+1]
            assert M[0][0]*M[1][1]-M[0][1]*M[1][0]==1
            count+=1
        for k in range(2,len(xs)):
            x,y,z=xs[k],xs[k-1],xs[k-2]
            assert x*x+y*y+z*z-2*x*y*z==1+lam*lam/4
    return count

def exact_controls():
    count=0
    # All 4^5=1024 alternating length patterns for 3 bands / 2 gaps.
    # Also all 2^9=512 patterns for 5 bands / 4 gaps (24 presentations each).
    for blocks,values in [(5,range(1,5)),(9,range(1,3))]:
        for lengths in itertools.product(values, repeat=blocks):
            edges=[Q(0)]
            for v in lengths:edges.append(edges[-1]+v)
            intervals=[[edges[i],edges[i+1]] for i in range(0,blocks,2)]
            best=max(presentation_score(intervals,p) for p in itertools.permutations(range(len(intervals)-1)))
            assert score(intervals)==best
            count+=1
    C=[[Q(0),Q(1)]]
    for _ in range(6):
        C=[[c,d] for a,b in C for c,d in [(a,a+(b-a)/3),(b-(b-a)/3,b)]]
        assert score(C)==1
    # Positive semidefinite endpoint motion can increase bridge/gap ratios.
    assert score([[Q(0),Q(1)],[Q(3),Q(5)]])==Q(1,2)
    assert score([[Q(0),Q(3,2)],[Q(3),Q(5)]])==1
    # Nested Cantor supersets can decrease thickness: C union (2+epsilon C).
    # First-level exterior gap alone bounds its thickness by epsilon.
    xs=[Q(1),Q(0),Q(-1,2)];ds=[Q(0),Q(0),Q(-1,2)]
    for _ in range(5):
        ds.append(2*(ds[-1]*xs[-2]+xs[-1]*ds[-2])-ds[-3])
        xs.append(2*xs[-1]*xs[-2]-xs[-3])
    return {'finite_presentation_exhaustions':count,'middle_third_levels':6,
            'exact_transfer_matrix_comparisons':trace_word_control(),
            'trace_derivatives_E0_lambda1':[str(x) for x in ds],
            'operator_order_countercontrol_scores':['1/2','1']}

def run():
    result={'warning':'Floating-point band scores are finite approximant diagnostics, not rigorous bounds for infinite-spectrum thickness.',
            'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
            'exact_controls':exact_controls()}
    # Periodic/antiperiodic constructor calibration at lambda=0.
    free=[]
    for k in range(3,12):
        I=merge(bands(k,0.),tol=1e-12)
        assert len(I)==1 and abs(I[0][0]+2)<1e-12 and abs(I[0][1]-2)<1e-12
        free.append(F[k])
    result['free_operator_periods']=free
    rows=[]
    lambdas=[.05,.1,.2,.5,1.,2.,4.,8.,16.]
    for k in [6,8,10,11]:
        for lam in lambdas:
            union=merge(bands(k,lam)+bands(k+1,lam),tol=1e-12)
            gaps=[union[i+1][0]-union[i][1] for i in range(len(union)-1)]
            widths=[b-a for a,b in union]
            s=score(union)
            rows.append({'k':k,'periods':[F[k],F[k+1]],'lambda':lam,'bands':len(union),
                         'score':s,'lambda_times_score':lam*s,
                         'smallest_gap':min(gaps) if gaps else None,'smallest_band':min(widths)})
    result['grid']=rows
    result['sampled_increases']=[{'k':k,'from':a['lambda'],'to':b['lambda'],'old':a['score'],'new':b['score']}
        for k in [6,8,10,11] for a,b in zip([r for r in rows if r['k']==k],[r for r in rows if r['k']==k][1:])
        if b['score']>a['score']+1e-8]
    return result
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='control_results.json');args=parser.parse_args()
    result=run();open(args.output,'w').write(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'exact_controls':result['exact_controls'],'sampled_increases':result['sampled_increases'],'rows':len(result['grid'])},indent=2))
