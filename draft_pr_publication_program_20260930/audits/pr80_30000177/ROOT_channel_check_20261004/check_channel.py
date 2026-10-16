"""Independent exact audit of PR80's specified instrument; standard library only.

Construct from original A1,A2,B1,B2 basis. No author checker imported.
This certifies finite channel algebra, not a capacity or coding theorem.
"""
from fractions import Fraction as F
import json
from math import log2

assert __debug__
letters = ('I', 'X', 'Z', 'XZ')
bell = ({0: 1, 3: 1}, {0: 1, 3: -1}, {1: 1, 2: 1}, {1: 1, 2: -1})
checks = 0

def check(value):
    global checks
    assert value
    checks += 1

def action(letter, bit):
    return bit ^ ('X' in letter), (-1 if 'Z' in letter and bit else 1)

def blocks(x, y):
    a = [[0] * 4 for _ in range(4)]
    for state in (8, 4, 2, 1):
        bits = [(state >> (3-k)) & 1 for k in range(4)]
        bits[0], sx = action(x, bits[0])
        bits[1], sy = action(y, bits[1])
        l = 2*bits[0]+bits[2]
        r = 2*bits[1]+bits[3]
        for j in range(4):
            a[j][r] += sx*sy*bell[j].get(l, 0)
    return [[[F(a[j][r]*a[j][s], 8) for s in range(4)] for r in range(4)] for j in range(4)]

def mean(states):
    return [[[sum(v[j][r][s] for v in states)/len(states) for s in range(4)] for r in range(4)] for j in range(4)]

def trace(m):
    return sum(m[k][k] for k in range(4))

def multiply(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]

def verify_spectrum(state, eigenvalues):
    # These four-by-four blocks form one sixteen-dimensional Hermitian matrix.
    # Power sums through dimension determine its characteristic polynomial.
    powers = state
    for k in range(1, 17):
        check(sum(trace(m) for m in powers) == sum(v**k for v in eigenvalues))
        if k != 16:
            powers = [multiply(powers[j], state[j]) for j in range(4)]

def entropy_symbolic(eigenvalues):
    # All verified positive eigenvalues have form 3^a / 2^b, a in {0,1}.
    constant = F(0)
    log3 = F(0)
    for p in eigenvalues:
        if not p:
            continue
        num, den = p.numerator, p.denominator
        check(num in (1, 3) and den > 0 and (den & (den-1)) == 0)
        constant += p*(den.bit_length()-1)
        log3 -= p*(num == 3)
    return constant, log3

allstates = {(x,y):blocks(x,y) for x in letters for y in letters}
eig_pair = [F(1,2),F(1,4),F(1,4)] + [F(0)]*13
eig_x = [F(1,4)]*2 + [F(1,16)]*8 + [F(0)]*6
eig_y = [F(1,8)]*8 + [F(0)]*8
eig_avg = [F(3,32)]*8 + [F(1,32)]*8
for state in allstates.values():
    check(sum(trace(m) for m in state)==1)
    verify_spectrum(state,eig_pair)
    for m in state:
        check(multiply(m,m)==[[trace(m)*v for v in row] for row in m])
for x in letters:
    verify_spectrum(mean([allstates[x,y] for y in letters]),eig_x)
for y in letters:
    verify_spectrum(mean([allstates[x,y] for x in letters]),eig_y)
avg=mean(list(allstates.values()))
verify_spectrum(avg,eig_avg)
for m in avg:
    check(m==[[F((3 if i%2==0 else 1),32) if i==j else F(0) for j in range(4)] for i in range(4)])
entropies=[entropy_symbolic(s) for s in (eig_pair,eig_x,eig_y,eig_avg)]
check(entropies==[(F(3,2),F(0)),(F(3),F(0)),(F(3),F(0)),(F(5),-F(3,4))])
check(3**3 < 2**5)
check(F(9,8)<F(3,2))

# Independent both-Bell measurement probabilities, from R block expectation.
bothbell=[]
for state in allstates.values():
    probs=[sum(F(u[r]*u[s],2)*m[r][s] for r in u for s in u) for m in state for u in bell]
    check(sorted(probs)==[F(0)]*12+[F(1,4)]*4)
    bothbell.append(probs)
check([sum(row[j] for row in bothbell)/16 for j in range(16)]==[F(1,16)]*16)

# Original marginals, using only the unencoded four-term W vector.
def marginal(keep):
    size=1<<len(keep); out=[[F(0) for _ in range(size)] for _ in range(size)]
    state=[[(v>>(3-k))&1 for k in range(4)] for v in (8,4,2,1)]
    discard=[k for k in range(4) if k not in keep]
    def index(bits):
        n=0
        for k in keep: n=2*n+bits[k]
        return n
    for u in state:
        for v in state:
            if all(u[k]==v[k] for k in discard): out[index(u)][index(v)]+=F(1,4)
    return out
for k in range(4): check(marginal([k])==[[F(3,4),F(0)],[F(0),F(1,4)]])
target=[[F(1,2),F(0),F(0),F(0)], [F(0),F(1,4),F(1,4),F(0)], [F(0),F(1,4),F(1,4),F(0)], [F(0)]*4]
for i in range(4):
    for j in range(i+1,4): check(marginal([i,j])==target)

result={'status':'PASS_EXACT_FINITE_CHANNEL_ALGEBRA','assertions':checks,'input_pairs':16,'conditional_blocks':64,'power_sum_orders':16,
    'entropy_pairs_constant_and_log2_3':[[str(x),str(y)] for x,y in entropies],
    'conditional_holevo_quantities':[1.5,1.5],'sum_holevo_quantity':3.5-0.75*log2(3),
    'both_bell_classical_mutual_information_bits':2,
    'independent_author_code_read_before_construction':False,
    'asymptotic_coding_or_priority_clearance':False}
print(json.dumps(result,indent=2))
