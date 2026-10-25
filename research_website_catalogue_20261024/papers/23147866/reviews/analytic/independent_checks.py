"""Independent density-operator/eigenspace/rate controls for Zenodo 23147866.

Does not import the published verifier. Constructs 16x16 density operators,
conjugates by Kronecker matrices, reorders tensor factors, and verifies spectra
through exact eigenspace nullities rather than the author's power-sum method.
Only standard-library Fraction arithmetic is used for algebra.
"""
from fractions import Fraction as F
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from math import log2
import json

checks = 0


def check(x):
    global checks
    assert x
    checks += 1


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    bt = transpose(b)
    return [[sum(x*y for x,y in zip(row,col)) for col in bt] for row in a]


def kron(a, b):
    return [[x*y for x in ra for y in rb] for ra in a for rb in b]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def rank(a):
    a = [row[:] for row in a]
    h = 0
    for j in range(len(a[0])):
        piv = next((i for i in range(h,len(a)) if a[i][j]),None)
        if piv is None:
            continue
        a[h], a[piv] = a[piv], a[h]
        t = a[h][j]
        a[h] = [v/t for v in a[h]]
        for i in range(len(a)):
            if i != h:
                t = a[i][j]
                a[i] = [v-t*w for v,w in zip(a[i],a[h])]
        h += 1
        if h == len(a):
            break
    return h


def avg(items):
    n = len(items)
    return [[[sum(x[j][r][s] for x in items)/n for s in range(4)]
             for r in range(4)] for j in range(4)]


def eigenspace_check(blocks, spectrum):
    check(all(m == transpose(m) for m in blocks))
    for val, multiplicity in Counter(spectrum).items():
        nullity = sum(4-rank([[m[i][j]-val*(i==j) for j in range(4)]
                              for i in range(4)]) for m in blocks)
        check(nullity == multiplicity)
    check(len(spectrum) == 16 and sum(spectrum) == 1 and min(spectrum) >= 0)


def majorizes(x,y):
    x,y=sorted(x,reverse=True),sorted(y,reverse=True)
    return sum(x)==sum(y) and all(sum(x[:k])>=sum(y[:k]) for k in range(1,len(x)))


def entropy(vals):
    return -sum(float(p)*log2(float(p)) for p in vals if p)


def main():
    I=eye(2); X=[[F(0),F(1)],[F(1),F(0)]]; Z=[[F(1),F(0)],[F(0),F(-1)]]
    paulis=[I,X,Z,mm(X,Z)]
    state=[F(int(i in [1,2,4,8]),2) for i in range(16)]
    rho=[[x*y for y in state] for x in state]
    check(trace(rho)==1 and mm(rho,rho)==rho)
    bells=[[F(1),F(0),F(0),F(1)],[F(1),F(0),F(0),F(-1)],
           [F(0),F(1),F(1),F(0)],[F(0),F(1),F(-1),F(0)]]
    # Original A1,A2,B1,B2 index -> A1,B1,A2,B2 index.
    def reorder(i):
        a1,a2,b1,b2=(i>>3)&1,(i>>2)&1,(i>>1)&1,i&1
        return 8*a1+4*b1+2*a2+b2
    inv=[reorder(i) for i in range(16)] # this permutation is its own inverse
    outputs={}
    for x,P in enumerate(paulis):
        for y,Q in enumerate(paulis):
            U=kron(kron(kron(P,Q),I),I)
            check(mm(U,transpose(U))==eye(16))
            encoded=mm(mm(U,rho),transpose(U))
            ordered=[[encoded[inv[i]][inv[j]] for j in range(16)] for i in range(16)]
            blocks=[]
            for v in bells:
                blocks.append([[sum(v[l]*v[k]*ordered[4*l+r][4*k+s]/2
                                    for l in range(4) for k in range(4))
                                for s in range(4)] for r in range(4)])
            outputs[x,y]=blocks
            check(sum(trace(m) for m in blocks)==1)
            check(sorted(trace(m) for m in blocks)==[F(0),F(1,4),F(1,4),F(1,2)])
    pair=[F(1,2),F(1,4),F(1,4)]+[F(0)]*13
    ex=[F(1,4)]*2+[F(1,16)]*8+[F(0)]*6
    ey=[F(1,8)]*8+[F(0)]*8
    grand=[F(3,32)]*8+[F(1,32)]*8
    for o in outputs.values():eigenspace_check(o,pair)
    for x in range(4):eigenspace_check(avg([outputs[x,y] for y in range(4)]),ex)
    for y in range(4):eigenspace_check(avg([outputs[x,y] for x in range(4)]),ey)
    eigenspace_check(avg(list(outputs.values())),grand)

    # Explicit no-signalling checks: R alone is independent of sender 1;
    # the Bell outcome J alone is independent of sender 2.
    def reduce_R(o):return [[sum(m[r][s] for m in o) for s in range(4)] for r in range(4)]
    for y in range(4):
        for x in range(4):check(reduce_R(outputs[x,y])==reduce_R(outputs[0,y]))
    for x in range(4):
        for y in range(4):check([trace(m) for m in outputs[x,y]]==[trace(m) for m in outputs[x,0]])

    # Mixing/measurement majorization. Equal entropy of ex,ey does not imply
    # either spectrum majorizes the other.
    maj={name:majorizes(a,b) for name,a,b in [
        ('pair_to_avg_x',pair,ex),('pair_to_avg_y',pair,ey),
        ('avg_x_to_grand',ex,grand),('avg_y_to_grand',ey,grand),
        ('avg_x_to_avg_y',ex,ey),('avg_y_to_avg_x',ey,ex)]}
    check(all(v for k,v in maj.items() if k not in ['avg_x_to_avg_y','avg_y_to_avg_x']))
    check(not maj['avg_x_to_avg_y'] and not maj['avg_y_to_avg_x'])
    comm=[]
    for a,b in zip(outputs[0,0],outputs[1,1]):
        ab,ba=mm(a,b),mm(b,a)
        comm.extend(ab[i][j]-ba[i][j] for i in range(4) for j in range(4))
    comm_norm=sum(x*x for x in comm)
    check(comm_norm>0)

    both=[]
    for o in outputs.values():
        probs=[sum(v[i]*m[i][j]*v[j]/2 for i in range(4) for j in range(4))
               for m in o for v in bells]
        check(sum(probs)==1)
        check(sorted(probs)==[F(0)]*12+[F(1,4)]*4)
        both.append(probs)
    avgprob=[sum(v[k] for v in both)/16 for k in range(16)]
    check(avgprob==[F(1,16)]*16)
    check(majorizes(pair,[F(1,4)]*4+[F(0)]*12))
    check(majorizes(grand,[F(1,16)]*16))

    # Analytical rate checks use exact inequalities where possible.
    h=2-F(3,4)*log2(3)
    total=F(3,2)+h
    check(27<32) # h_2(1/4)>3/4 and hence total>9/4.
    check(F(9,8)<F(3,2) and F(9,4)<total)
    check(total<1+2*h<3)
    check(F(3,2)+F(3,2)>total) # individual maxima cannot be summed.
    check(abs(entropy(pair)-1.5)<1e-14)
    check(abs(entropy(ex)-3)<1e-14 and abs(entropy(ey)-3)<1e-14)
    check(abs(entropy(grand)-(3+h))<1e-14)
    check(abs(entropy(avgprob)-sum(entropy(v) for v in both)/16-2)<1e-14)
    check(abs(2*h-1.6225562489182657)<1e-14)

    result={
        'utc':datetime.now(timezone.utc).isoformat(),
        'status':'PASS_INDEPENDENT_FINITE_ALGEBRA_AND_RATE_CONTROLS',
        'assertions':checks,'input_pairs':16,'instrument_blocks':64,
        'method':'Full density-operator tensor conjugation, partial Bell contraction, exact eigenspace dimensions, no-signalling and majorization; no published checker imports.',
        'spectra':{k:[str(x) for x in v] for k,v in dict(pair=pair,average_over_y=ex,average_over_x=ey,grand=grand).items()},
        'majorization':maj,'noncommuting_output_pair_commutator_squared_frobenius':str(comm_norm),
        'rates':{'h2_1_4':h,'conditional_each':1.5,'sum_lower_bound':total,'explicit_each':1.125,
                 'equal_rate_boundary':float(total)/2,'raw_LO_unitary_sum':2*h,
                 'classical_fallback':2,'source_LOCC_upper_bound':1+2*h,'global_upper_bound':3,
                 'both_Bell_uniform_mutual_information':2,
                 'retained_quantum_output_gain_over_both_Bell':float(total)-2},
        'negative_controls':['The two conditional individual maxima do not form an achievable sum pair under the sum constraint.','Both-Bell measurement reduces the information to exactly 2.','The retained output family is not commuting.','The two conditional averages have equal entropy but incomparable spectra.'],
        'scope_limit':'These finite checks do not replace Winter\'s asymptotic cq-MAC coding theorem or establish optimal unrestricted LOCC capacity, one-shot, zero-error, maximal-error or finite-blocklength guarantees.'}
    Path(__file__).with_name('independent-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='spectra'},indent=2))


if __name__=='__main__':main()
