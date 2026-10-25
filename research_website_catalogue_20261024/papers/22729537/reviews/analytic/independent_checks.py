"""Independent finite controls, not universal theorem certificates.

No imports from the paper's code and no reads of any archived reviewer outputs.
"""
from fractions import Fraction as F
from pathlib import Path
import datetime, hashlib, json, math
import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent

def det(a):
    a = [list(map(F, r)) for r in a]
    n, sign, value = len(a), 1, F(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            sign *= -1
        p = a[j][j]
        value *= p
        for i in range(j+1, n):
            c = a[i][j]/p
            for k in range(j+1, n):
                a[i][k] -= c*a[j][k]
    return value*sign

def solve(a, b):
    a = [list(map(F, r))+[F(x)] for r,x in zip(a,b)]
    n = len(a)
    for j in range(n):
        pivot = next(i for i in range(j,n) if a[i][j])
        a[j], a[pivot] = a[pivot], a[j]
        p = a[j][j]
        a[j] = [x/p for x in a[j]]
        for i in range(n):
            if i != j:
                c = a[i][j]
                a[i] = [x-c*y for x,y in zip(a[i],a[j])]
    return [row[-1] for row in a]

results = {}
results['utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
results['method_limit'] = 'Finite controls accompany the independently reconstructed analytic proofs; these controls do not prove arbitrary finite-size cases.'
results['pdf_sha256'] = {
    f: hashlib.sha256((ROOT/'sources'/f).read_bytes()).hexdigest()
    for f in ['NMSC_Paper_A_Main.pdf','NMSC_Paper_A_Supplement.pdf']
}

# Normalized four-state JC has beta=2/3 for a pair coalescing at age T.
# Set a_j=j*log(2)/beta, tau=log(2)/beta, lambda0=beta.
# Every Jacobian entry is then an exact rational number.
beta = F(2,3)
collisions = []
for L in range(1,8):
    m = L+1
    J = [[F(k,1)/(beta*(k+1)**2)*F(1,2)**k*F(1,2)**((k+1)*j)
          for j in range(1,m+1)] for k in range(1,m+1)]
    determinant = det(J)
    assert determinant != 0
    top = J[:-1]
    minors = [det([[row[j] for j in range(m) if j != omit] for row in top])
              for omit in range(m)]
    assert all(minors)
    kernel = [(-1)**j*minors[j] for j in range(m)]
    assert all(sum(row[j]*kernel[j] for j in range(m)) == 0 for row in top)
    next_moment_variation = sum(J[-1][j]*kernel[j] for j in range(m))
    assert next_moment_variation != 0
    collisions.append({'L': L, 'determinant': str(determinant),
                       'all_tangent_coordinates_nonzero': True,
                       'next_moment_variation_nonzero': True})
results['collision_jacobians'] = collisions

# Positive-atom decoder q=v^T H^{-1}v, with both separated and co-occupied mass.
decoder = []
for rates,weights in [([F(1),F(2),F(5)],[F(1,10),F(1,6),F(1,4)]),
                      ([F(3)],[F(7,13)]),
                      ([F(1,2),F(3,2)],[F(2,7),F(3,7)])]:
    r=len(rates)
    moment=lambda k:sum(w*l**k for w,l in zip(weights,rates))
    H=[[moment(i+j+2) for j in range(r)] for i in range(r)]
    v=[moment(i+1) for i in range(r)]
    q=sum(x*y for x,y in zip(v,solve(H,v)))
    assert q == sum(weights)
    assert all(det([row[:k] for row in H[:k]])>0 for k in range(1,r+1))
    Hnext=[[moment(i+j+2) for j in range(r+1)] for i in range(r+1)]
    assert det(Hnext)==0
    decoder.append({'rates':list(map(str,rates)), 'decoded_q':str(q),
                    'positive_minors_and_next_singular':True})
results['cooccupancy_decoder'] = decoder

# Reversible generator inversion from a realized conditional pair law.
# Include repeated eigenvalues and nonuniform stationary probabilities with zero conductances.
generator_checks=[]
for name,pi,w in [
    ('JC_repeated_eigenvalues', np.ones(4)/4, np.ones((4,4))-np.eye(4)),
    ('path_zero_conductances', np.array([.1,.2,.3,.4]),
     np.array([[0,1,0,0],[1,0,2,0],[0,2,0,3],[0,0,3,0]],dtype=float))]:
    Q=w/pi[:,None]
    np.fill_diagonal(Q,-Q.sum(axis=1))
    Q=Q/(-np.trace(Q))
    D=np.diag(np.sqrt(pi)); Di=np.diag(1/np.sqrt(pi))
    R=D@Q@Di
    lam,U=np.linalg.eigh(R)
    s=1.7
    E=Di@((U*np.exp(s*lam))@U.T)@D
    J=np.diag(pi)@E
    recovered_s=-np.linalg.slogdet(np.diag(1/pi)@J)[1]
    S=D@E@Di
    e,V=np.linalg.eigh(S)
    Qrec=Di@((V*np.log(e))@V.T)@D/recovered_s
    err=float(np.max(np.abs(Q-Qrec)))
    assert abs(recovered_s-s)<1e-12 and err<1e-12
    generator_checks.append({'case':name,'determinant_coordinate_error':abs(recovered_s-s),
                             'generator_max_error':err})
results['conditional_generator'] = generator_checks

# Independent balance collision: gamma=1/3, first rates 1 and 2, length log4.
g=F(1,3)
w1=g*g*F(1,4)
w2=(1-g)**2*F(1,16)
assert w1==w2==F(1,36)
results['posterior_balance']={'same_parent_weights':[str(w1),str(w2)],
                              'both_suffix_orders_have_identical_exponential_coefficients':True}

# Thue-Morse high-order breakpoint example, computed from bit parity.
A=[a for a in range(1,33) if (a-1).bit_count()%2==0]
B=[a for a in range(1,33) if (a-1).bit_count()%2==1]
diffs=[sum(a**k for a in A)-sum(b**k for b in B) for k in range(6)]
assert diffs==[0,0,0,0,0,-122880]
results['breakpoint_power_sums']=diffs

(OUT/'independent_checks.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'passed':True,'collision_orders':list(range(1,8)),
                  'decoder_cases':len(decoder),'generator_cases':generator_checks,
                  'posterior_balance':results['posterior_balance'],
                  'breakpoint_power_sums':diffs},indent=2))
