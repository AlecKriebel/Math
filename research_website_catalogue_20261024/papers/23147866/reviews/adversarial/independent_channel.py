#!/usr/bin/env python3
"""Fresh control: start in A1,A2,B1,B2 computational order; no archived code imported."""
import json, hashlib, itertools, datetime
from pathlib import Path
import sympy as s
Q=s.Rational
out=Path(__file__).resolve().parent
checks=[]
def check(name, cond):
    if not cond: raise AssertionError(name)
    checks.append(name)
def mat_sum(ms):
    ms=list(ms)
    return sum(ms,s.zeros(*ms[0].shape))
def spectrum(a):
    ev=a.eigenvals()
    check('Hermitian spectrum '+str(len(checks)), all(x.is_real and x>=0 for x in ev))
    return sorted([v for v,m in ev.items() for _ in range(m)],reverse=True)
def pos_spec(a):return [v for v in spectrum(a) if v]
def block_spec(bs):return sorted(sum([pos_spec(b) for b in bs],[]),reverse=True)
def entropy(spec):return s.expand_log(-sum(v*s.log(v,2) for v in spec if v),force=True).expand().simplify()
def bits(k):return [(k>>j)&1 for j in [3,2,1,0]]
def idx(bs):return sum(b<<(3-j) for j,b in enumerate(bs))
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Z=s.diag(1,-1)
paulis=[I,X,Z,X*Z]
w=s.zeros(16,1)
for k in [8,4,2,1]:w[k]=Q(1,2)
check('literal W normalization',(w.T*w)[0]==1)
bells=[s.Matrix(x) for x in [(1,0,0,1),(1,0,0,-1),(0,1,1,0),(0,1,-1,0)]]
for j,b in enumerate(bells):
    check('Bell norm '+str(j),(b.T*b)[0]==2)
for j,k in itertools.product(range(4),repeat=2):
    check(f'Bell Gram {j},{k}',(bells[j].T*bells[k])[0]==(2 if j==k else 0))
channel={}; residuals={}
for x,y in itertools.product(range(4),repeat=2):
    U=s.kronecker_product(paulis[x],paulis[y],I,I)
    check(f'unitary {x},{y}',U.T*U==s.eye(16))
    v=U*w
    bs=[]
    for j,b in enumerate(bells):
        r=s.zeros(4,1)
        for k in range(16):
            a1,a2,b1,b2=bits(k)
            r[2*a2+b2]+=b[2*a1+b1]*v[k]
        B=r*r.T/2
        bs.append(B)
        check(f'block PSD {x},{y},{j}',all(t>=0 for t in B.eigenvals()))
        check(f'block rank {x},{y},{j}',B.rank()<=1)
    channel[x,y]=bs
    check(f'complete instrument trace {x},{y}',sum(b.trace() for b in bs)==1)
    check(f'conditional spectrum {x},{y}',block_spec(bs)==[Q(1,2),Q(1,4),Q(1,4)])
    residuals[str((x,y))]=[str(b.trace()) for b in bs]
barx={x:[mat_sum(channel[x,y][j] for y in range(4))/4 for j in range(4)] for x in range(4)}
bary={y:[mat_sum(channel[x,y][j] for x in range(4))/4 for j in range(4)] for y in range(4)}
bar=[mat_sum(channel[x,y][j] for x,y in itertools.product(range(4),repeat=2))/16 for j in range(4)]
for x in range(4):check(f'x fixed spectrum {x}',block_spec(barx[x])==[Q(1,4)]*2+[Q(1,16)]*8)
for y in range(4):check(f'y fixed spectrum {y}',block_spec(bary[y])==[Q(1,8)]*8)
check('full average spectrum',block_spec(bar)==[Q(3,32)]*8+[Q(1,32)]*8)
S0=entropy(block_spec(channel[0,0])); Sx=entropy(block_spec(barx[0])); Sy=entropy(block_spec(bary[0])); Sav=entropy(block_spec(bar))
h=entropy([Q(3,4),Q(1,4)])
check('conditional entropy',S0==Q(3,2));check('fixed x entropy',Sx==3);check('fixed y entropy',Sy==3)
check('joint entropy',s.simplify(Sav-3-h)==0)
check('X conditional Holevo',Sy-S0==Q(3,2));check('Y conditional Holevo',Sx-S0==Q(3,2));check('sum Holevo',s.simplify(Sav-S0-Q(3,2)-h)==0)
def marginal(v, keep):
    keep=tuple(keep);drop=tuple(k for k in range(4) if k not in keep)
    ans=s.zeros(2**len(keep))
    for i,j in itertools.product(range(16),repeat=2):
        bi,bj=bits(i),bits(j)
        if all(bi[k]==bj[k] for k in drop):
            ii=sum(bi[k]<<(len(keep)-1-l) for l,k in enumerate(keep)); jj=sum(bj[k]<<(len(keep)-1-l) for l,k in enumerate(keep))
            ans[ii,jj]+=v[i]*v[j]
    return ans
for k in range(4):check(f'single marginal {k}',spectrum(marginal(w,[k]))==[Q(3,4),Q(1,4)])
for ks in itertools.combinations(range(4),2):check(f'pair marginal {ks}',spectrum(marginal(w,ks))==[Q(1,2),Q(1,2),0,0])
# Negative control 1: both receivers Bell-measure. This loses coherent-output benefit.
both={}
for x,y in itertools.product(range(4),repeat=2):
    ps=[(b.T*channel[x,y][j]*b)[0]/2 for j,b in itertools.product(range(4),bells)]
    check(f'both Bell normalization {x},{y}',sum(ps)==1)
    check(f'both Bell nonzero distribution {x},{y}',sorted(p for p in ps if p)==[Q(1,4)]*4)
    both[x,y]=ps
avps=[sum(both[x,y][k] for x,y in itertools.product(range(4),repeat=2))/16 for k in range(16)]
check('both Bell overall uniform',avps==[Q(1,16)]*16)
check('both Bell mutual information',entropy(avps)-sum(entropy(ps) for ps in both.values())/16==2)
# Negative control 2: erase classical report J. No receiver-2 signal about sender 1 remains.
noJ={xy:mat_sum(bs) for xy,bs in channel.items()}
for x,y in itertools.product(range(4),repeat=2):check(f'no J no X signal {x},{y}',noJ[x,y]==noJ[0,y])
check('no J joint Holevo',s.simplify(entropy(spectrum(mat_sum(noJ.values())/16))-entropy(spectrum(noJ[0,0]))-h)==0)
# Negative control 3: retaining a single branch is not a trace-preserving channel.
check('single branch trace is not one',channel[0,0][2].trace()==Q(1,2))
check('zero branch truly present',channel[0,0][3]==s.zeros(4))
# Exact control of pinching, including a POVM with off-diagonal J coherence.
u=s.Matrix(list(range(1,17))); D=u*u.T/(u.T*u)[0]
Dp=s.diag(*[D[4*j:4*j+4,4*j:4*j+4] for j in range(4)])
for x,y in itertools.product(range(4),repeat=2):
    omega=s.diag(*channel[x,y])
    check(f'pinched decoding probability {x},{y}',s.trace(D*omega)==s.trace(Dp*omega))
check('pinched POVM first effect PSD',all(v>=0 for v in Dp.eigenvals()))
check('pinched POVM second effect PSD',all(v>=0 for v in (s.eye(16)-Dp).eigenvals()))
# Exact threshold control, no floating point decision.
check('strict useful rational rate 9/8 individually',Q(9,8)<Q(3,2))
check('strict sum-rate margin equivalence',3**3<2**5)
check('classical threshold exceeded',2*Q(9,8)>2)
# Finite n=2 memoryless normalization; no asymptotic proof inferred from it.
for xy in [(0,0),(0,3),(2,1),(3,3)]:
    b2=[s.kronecker_product(a,b) for a,b in itertools.product(channel[xy],channel[xy])]
    check('two-copy trace '+str(xy),sum(a.trace() for a in b2)==1)
# Recover the Bell permutation directly from conjugation, then test Eq. (6) as matrices.
for x in range(4):
    left=s.kronecker_product(paulis[x],I)
    for j,b in enumerate(bells):
        proj=left.T*(b*b.T/2)*left
        matches=[k for k,c in enumerate(bells) if proj==c*c.T/2]
        check(f'Bell Pauli permutation {x},{j}',len(matches)==1)
        for y in range(4):
            right=s.kronecker_product(paulis[y],I)
            check(f'branch matrix formula {x},{y},{j}',channel[x,y][j]==right*channel[0,0][matches[0]]*right.T)
# Rational majorization sanity controls for mixing and the strict LO entropy comparison.
def majorizes(a,b):
    a=sorted(a,reverse=True);b=sorted(b,reverse=True);n=max(len(a),len(b));a+=[0]*(n-len(a));b+=[0]*(n-len(b))
    return sum(a)==sum(b) and all(sum(a[:k])>=sum(b[:k]) for k in range(1,n))
check('single qubit spectrum strictly away from uniform',[Q(3,4),Q(1,4)]!=[Q(1,2)]*2 and majorizes([Q(3,4),Q(1,4)],[Q(1,2)]*2))
check('joint twirl majorization',majorizes(block_spec(channel[0,0]),block_spec(bar)))
check('x partial twirl majorization',majorizes(block_spec(channel[0,0]),block_spec(barx[0])))
check('y partial twirl majorization',majorizes(block_spec(channel[0,0]),block_spec(bary[0])))
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Exact SymPy matrices independently generated from literal four-qubit computational-basis state. No published code imported.','checks_passed':len(checks),'checks':checks,'conditional_branch_weights':residuals,'entropies':{'S_output':str(S0),'S_x_fixed':str(Sx),'S_y_fixed':str(Sy),'S_mean':str(Sav),'h_quarter':str(h)},'rate_lower_bound_exact':'7/2 - (3/4)*log2(3)','rate_lower_bound_display':float(Q(3,2)+h),'negative_controls':{'both_Bell_mutual_information':'2','erase_J_sender1_information':'0','erase_J_sum_Holevo':str(h),'single_branch_trace':'1/2'},'scope':'Finite exact identities plus controls only; asymptotic conclusion uses separately reviewed Winter theorem and decoder argument.'}
(out/'independent-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['checks','conditional_branch_weights']},indent=2))
