"""Check the published Eq. (35) indexing, without importing submitted code.

This is a counterexample to an intermediate equality, NOT to the main theorem
or to the main text's weaker inequality A.31. No corrected proof is attempted.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import datetime,hashlib,json

def probe(N):
    ga={j:F(comb(N-2,j-1),2**(N-1)*(N+1)) for j in range(1,N)}
    q={k:F(comb(N-3,k-2),2**(N-2)*(N+1)) for k in range(2,N)}
    Y={k:F(2*(k+1),3*k*(k-1)) for k in range(2,N)}
    coefficient=lambda j:F(4*(j+2),3*(j+1)*(N-2))
    Yq=sum(Y[k]*q[k] for k in range(2,N))
    printed=sum(coefficient(j)*ga[j] for j in range(1,N-1))
    reindexed=sum(coefficient(j)*ga[j+1] for j in range(1,N-1))
    assert Yq==reindexed
    # Test the actual debt separately, so the false intermediate equality
    # is never represented as a counterexample to A.31 itself.
    d=[F(0)]*(N+1);c=F(2**N-1,N*2**(N-1))
    for k in range(1,N):d[k]=(2*N*(F(1,k)-c)+(k-1)*d[k-1])/(N-k)
    ks=list(range(2,N));size=N-2
    lo=[-F(N-k-1,2*N) if k>2 else F(0) for k in ks]
    diag=[1-F(N*(k-2)+k,2*k*N) for k in ks]
    hi=[-F(k*(k-1),2*(k+1)*N) if k<N-1 else F(0) for k in ks]
    rhs=[q[k] for k in ks]
    for i in range(1,size):
        factor=lo[i]/diag[i-1];diag[i]-=factor*hi[i-1];rhs[i]-=factor*rhs[i-1]
    W=[F(0)]*size
    for i in reversed(range(size)):
        W[i]=(rhs[i]-(hi[i]*W[i+1] if i<size-1 else 0))/diag[i]
    # Independently check the tridiagonal equation, including both boundaries.
    for i,k in enumerate(ks):
        value=(1-F(N*(k-2)+k,2*k*N))*W[i]
        if i:value-=F(N-k-1,2*N)*W[i-1]
        if i+1<size:value-=F(k*(k-1),2*(k+1)*N)*W[i+1]
        assert value==q[k]
    debt=sum(d[k-1]/(2*k)*W[i] for i,k in enumerate(ks))
    return {'N':N,'Yq':str(Yq),'printed_sum':str(printed),'reindexed_sum':str(reindexed),
            'Yq_minus_printed':str(Yq-printed),'published_equality_true':Yq==printed,
            'actual_debt_le_printed_sum':debt<=printed,'actual_debt_over_printed':str(debt/printed)}

values=[probe(N) for N in [3,4,10,24,40,80,288]]
forty=next(v for v in values if v['N']==40)
assert forty['Yq_minus_printed']=='549755813107/501063941451939840'
assert not forty['published_equality_true']
assert all(v['actual_debt_le_printed_sum'] for v in values)
out={'status':'INTERMEDIATE_EQUALITY_REFUTED_PROOF_DEPENDENCY_GAP',
     'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'target':'Support Eq. (35), connected to published PDF A.31/A.32/A.36',
     'main_theorem_counterexample':False,'A31_counterexample':False,'values':values,
     'limitation':'Finite exact debt probes do not prove A.31 at all orders. No repair has been constructed.'}
Path(__file__).with_name('debt_index_control_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status']);print('N=40 exact equality residual:',forty['Yq_minus_printed'])
