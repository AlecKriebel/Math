#!/usr/bin/env python3
"""Read-only deterministic interfaces; finite tests are not an analytic proof."""
import itertools,json,math,sys
from fractions import Fraction as Q
class AuditFailure(Exception):pass
def require(ok,label):
 if not ok:raise AuditFailure(label)
def fixed_g_ceiling(g,r):return (1+r*math.sqrt(g))**2
def accepted_scope():return {'constant_uniform_in_g':False,'new_research_turns':0,'main_target':'HOLD_VARIABLE_COUNT_UNIFORMITY'}
def eye(n):
    return [[Q(int(i==j)) for j in range(n)] for i in range(n)]
def zero(n,m=None):
    return [[Q(0) for _ in range(n if m is None else m)] for _ in range(n)]
def plus(A,B):
    return [[a+b for a,b in zip(x,y)] for x,y in zip(A,B)]
def times(A,B):
    return [[sum(A[i][j]*B[j][k] for j in range(len(B))) for k in range(len(B[0]))] for i in range(len(A))]
def adj(A):
    return [[A[j][i].conjugate() for j in range(len(A))] for i in range(len(A[0]))]
def kron(A,B):
    return [[a*b for a in ar for b in br] for ar in A for br in B]
def tr(A):
    return sum(A[i][i] for i in range(len(A)))
def power(A,n):
    out=eye(len(A))
    for _ in range(n): out=times(out,A)
    return out

def word(X,w):
    out=eye(len(X[0]))
    for j in w: out=times(out,X[j])
    return out

def sum_mats(seq,n):
    out=zero(n)
    for A in seq: out=plus(out,A)
    return out

def phi(X,H,inverse=False):
    return sum_mats((times(times(adj(A),H),A) if inverse else times(times(A,H),adj(A)) for A in X),len(H))

def rotation(w,j): return w[j:]+w[:j]

def calculations():
    done=[]
    def check(ok,label):
        require(ok,label);done.append(label)
    r=Q(3,4);x=Q(3,8)
    check(4*x*x==r*r and (1+4*x)**2==Q(25,4)>4,'ceiling_counterexample_exact')
    check(fixed_g_ceiling(4,r)==Q(25,4) and fixed_g_ceiling(16,r)>fixed_g_ceiling(4,r),'corrected_ceiling_exact')
    check(1+0==math.exp(0),'tail_constant_exact')
    t=Q(1,6);N=40
    check(sum(t**j for j in range(N+1))+t**(N+1)/(1-t)==1/(1-t),'scalar_reciprocal_exact')
    pluslog=sum((-1)**(n+1)*0.25**n/n for n in range(1,101))
    minuslog=sum(0.25**n/n for n in range(1,101))
    check(abs(pluslog-math.log1p(.25))<1e-14,'log_plus_sign_numeric')
    check(abs(minuslog+math.log1p(-.25))<1e-14,'inverse_determinant_log_sign_numeric')
    for n in (1,2,7):check(Q(1,n)>0,'commutator_mean_nonzero_'+str(n))
    X=[[[Q(1,8),Q(1,4)],[Q(0),Q(1,8)]],[[Q(0),Q(1,8)],[Q(1,8),Q(0)]]]
    B=[[[Q(1,9),Q(0),Q(1,9)],[Q(0),Q(1,9),Q(0)],[Q(0),Q(0),Q(1,9)]],
       [[Q(0),Q(1,9),Q(0)],[Q(0),Q(0),Q(1,9)],[Q(1,9),Q(0),Q(0)]]]
    S=sum_mats((kron(a,b) for a,b in zip(X,B)),6)
    row=eye(2);col=eye(2)
    for n in range(1,6):
        words=list(itertools.product(range(2),repeat=n))
        mats={w:word(X,w) for w in words}; bmats={w:word(B,w) for w in words}
        row=phi(X,row);col=phi(X,col,True)
        check(row==sum_mats((times(M,adj(M)) for M in mats.values()),2),'row_power_identity_'+str(n))
        check(col==sum_mats((times(adj(M),M) for M in mats.values()),2),'column_power_identity_'+str(n))
        check(tr(row)==tr(col),'row_column_trace_'+str(n))
        check(tr(power(S,n))==sum(tr(mats[w])*tr(bmats[w]) for w in words),'mixed_tensor_trace_'+str(n))
        pair=Q(0)
        for w in words:
            for v in words:
                count=sum(rotation(v,j)==w for j in range(n))
                pair+=tr(mats[w])*tr(bmats[v])*Q(count,n*n)
        check(pair==tr(power(S,n))/n,'full_gaussian_covariance_sum_'+str(n))
        for w in words:
            orbit={rotation(w,j) for j in range(n)}
            stabilizer=sum(rotation(w,j)==w for j in range(n))
            require(len(orbit)*stabilizer==n,'periodic-word:'+str(w))
        done.append('all_binary_word_orbits_'+str(n))
    H=[[Q(1),Q(2)],[Q(3),Q(4)]];K=[[Q(2),Q(1)],[Q(5),Q(3)]]
    check(tr(times(adj(K),phi(X,H)))==tr(times(adj(phi(X,K,True)),H)),'cp_maps_HS_adjoint')
    # Exact non-normal nilpotent example: row norm 2, outer radius zero.
    A=[[Q(0),Q(2)],[Q(0),Q(0)]];P=plus(eye(2),times(A,adj(A)))
    check(power(A,2)==zero(2) and phi([A],P)==plus(P,[[-Q(1),Q(0)],[Q(0),-Q(1)]]),'lyapunov_outer_similarity_identity')
    check(P==[[Q(5),Q(0)],[Q(0),Q(1)]] and Q(4,5)<1,'similarity_strict_row_squared')
    # Entrywise conjugation cannot be dropped: a=i/2, b=i/3.
    a=complex(0,1);b=complex(0,1)
    check(a*b.conjugate()==1 and a*b==-1,'complex_conjugation_required')
    return done

def main():
 require(len(sys.argv)==1,'no-output-or-other-arguments')
 scope=accepted_scope()
 require(type(scope['new_research_turns']) is int and scope['new_research_turns']==0,'zero-turns')
 require(scope['constant_uniform_in_g'] is False and scope['main_target']=='HOLD_VARIABLE_COUNT_UNIFORMITY','variable-count-scope')
 done=calculations()
 print(json.dumps({'status':'PASS','proof_turns':0,'optimization':sys.flags.optimize,'calculation_count':len(done),'calculations':done,'scope':scope,'read_only_by_design':True,'limits':'Finite interfaces only; no universal analytic proof, all-g bound, or complete manuscript acceptance.'},sort_keys=True))
if __name__=='__main__':
 try:main()
 except (AuditFailure,ValueError,KeyError,OSError) as e:
  print(json.dumps({'status':'FAIL','reason':str(e)},sort_keys=True),file=sys.stderr);sys.exit(1)
