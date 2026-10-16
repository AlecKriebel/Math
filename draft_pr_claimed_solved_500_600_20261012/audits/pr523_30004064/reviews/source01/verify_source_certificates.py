"""Independent exact checks of primary-source overlap and repair witnesses.

No external packages, solver runs, source-code execution, or publication.
The constructions are prior work, not claims of novelty by this review.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import json


def lines(n, diagonal=True):
    groups = [[(i,j) for j in range(n)] for i in range(n)]
    groups += [[(i,j) for i in range(n)] for j in range(n)]
    if diagonal:
        groups += [[(i,j) for i in range(n) for j in range(n) if j-i==d]
                   for d in range(1-n,n)]
    return groups


def matrix(n, groups):
    return [[int((i,j) in g) for i in range(n) for j in range(n)] for g in groups]


def mv(a,x):
    return [sum(Q(v)*Q(w) for v,w in zip(row,x)) for row in a]


def rank(a):
    a=[[Q(v) for v in row] for row in a]
    if not a: return 0
    r=0
    for j in range(len(a[0])):
        p=next((i for i in range(r,len(a)) if a[i][j]),None)
        if p is None: continue
        a[r],a[p]=a[p],a[r]
        a[r]=[v/a[r][j] for v in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][j]:
                v=a[i][j]; a[i]=[u-v*w for u,w in zip(a[i],a[r])]
        r+=1
        if r==len(a): break
    return r


def binary_solutions(n,a,x):
    y=mv(a,x)
    row_sums=[int(sum(x[i*n:(i+1)*n])) for i in range(n)]
    patterns=[]
    for k in row_sums:
        patterns.append([tuple(int(j in c) for j in range(n))
                         for c in combinations(range(n),k)])
    solutions=[]; count=0
    for rows in product(*patterns):
        candidate=sum(rows,())
        count+=1
        if mv(a,candidate)==y: solutions.append(candidate)
    return solutions,count


# Ferudun Theorem 4.2: 0/1 picture and a kernel vector in +/-1 coding.
x5=list(map(int,''.join(['00010','01000','10001','10000','00100'])))
c5=[1,0,0,-1,0, 0,-2,0,1,1, 0,0,1,0,-1, -1,1,0,0,0, 0,1,-1,0,0]
a5=matrix(5,lines(5))
s5=[2*v-1 for v in x5]
assert mv(a5,c5)==[0]*len(a5)
endpoint5=[Q(s)+Q(c) for s,c in zip(s5,c5)]
assert all(-1<=v<=1 for v in endpoint5)
assert mv(a5,endpoint5)==mv(a5,s5)
support5=[j for j,c in enumerate(c5) if c]
assert len(support5)==11
assert all(s5[j]*c5[j]<0 for j in support5)
solutions5,tested5=binary_solutions(5,a5,x5)
assert solutions5==[tuple(x5)]
# A source row-space potential forces every feasible perturbation off the
# eleven-pixel support to vanish, and the restricted kernel is one-dimensional.
rho=[1,0,-1,1,0]; gamma=[-1,0,1,0,1]; delta=[2,0,-1,2,0,2,0,-1,0]
f5=[rho[i]+gamma[j]+delta[j-i+4] for i in range(5) for j in range(5)]
assert all(s*f<=0 for s,f in zip(s5,f5))
assert [j for j,f in enumerate(f5) if f==0]==support5
assert rank([[row[j] for j in support5] for row in a5])==10
# At coordinate (1,1), s+t*c = 1-2*t forces t<=1; at (0,0), -1+t
# forces t>=0. Hence feasible set is exactly the segment s+t*c, 0<=t<=1.
assert s5[6]==1 and c5[6]==-2 and s5[0]==-1 and c5[0]==1
# A full binary sign output is impossible for EVERY multiplier: if
# sign(A^T*mu)=s5 then c5^T A^T*mu<0, but Ac5=0 makes it zero.

# Theorem 4.6's explicit intersection witness; no LP or count claim is imported.
x4=list(map(int,''.join(['1100','1001','0010','0100'])))
a4=matrix(4,lines(4))
q4=[Q(v) for v in [1,Q(1,2),Q(1,2),0,Q(1,2),Q(1,2),Q(1,2),Q(1,2),Q(1,2),Q(1,2),0,0,0,Q(1,2),0,Q(1,2)]]
assert mv(a4,q4)==mv(a4,x4)
solutions4,tested4=binary_solutions(4,a4,x4)
assert len(solutions4)==4
common4=[j for j in range(16) if len({s[j] for s in solutions4})==1]
assert common4==[3,6,9,12]
assert all(s[j]==0 for s in solutions4 for j in common4)
changed_common4=[j for j in common4 if q4[j]!=x4[j]]
assert changed_common4==[6,9]

# Candidate row/column witness: fixed/common agreement is compatible with
# a box polytope segment; it cannot disprove the intended fixed-pixel reading.
x3=list(map(int,''.join(['111','110','101'])))
x3b=list(map(int,''.join(['111','101','110'])))
a3=matrix(3,lines(3,False))
solutions3,tested3=binary_solutions(3,a3,x3)
assert set(solutions3)=={tuple(x3),tuple(x3b)}
common3=[j for j in range(9) if len({s[j] for s in solutions3})==1]
assert common3==[0,1,2,3,6]

# Audit-local reproduction of the universal identity with arbitrary signs,
# box-feasible fractional data and an arbitrary rectangular rational matrix.
count=0
A=[[Q(1),Q(-2),Q(1,3)],[Q(0),Q(3,2),Q(2)]]
for z in product([Q(-1),Q(-1,2),Q(0),Q(1,2),Q(1)],repeat=3):
    y=mv(A,z)
    for mu in product([Q(-2),Q(-1,3),Q(0),Q(2,3)],repeat=2):
        nu=mv(list(zip(*A)),mu)
        F=lambda v: sum((Q(w)-yi)**2 for w,yi in zip(v,y))/2 + sum(abs(w) for w in mv(list(zip(*A)),v))
        difference=F(mu)-F([0,0])
        rhs=sum(w*w for w in mu)/2+sum(abs(t)-s*t for s,t in zip(z,nu))
        assert difference==rhs and rhs>=sum(w*w for w in mu)/2
        count+=1

out={
 'purpose':'Independent exact confirmation of prior theorem overlap and original-scope repair witnesses; no novelty claim',
 'prior_5x5':{'matrix_shape':[len(a5),25],'matrix_rank':rank(a5),'binary_candidates_checked':tested5,'binary_solutions':len(solutions5),'kernel_support':len(support5),'restricted_kernel_dimension':1,'fixed_pixels':14,'full_sign_output_impossible_for_any_multiplier':True},
 'prior_4x4':{'matrix_shape':[len(a4),16],'matrix_rank':rank(a4),'binary_candidates_checked':tested4,'binary_solutions':len(solutions4),'common_pixels_zero_based':common4,'fractional_witness_moves_common_pixels':changed_common4,'solutions':['/'.join(''.join(map(str,s[i*4:(i+1)*4])) for i in range(4)) for s in solutions4]},
 'candidate_3x3':{'binary_candidates_checked':tested3,'binary_solutions':len(solutions3),'common_pixels_zero_based':common3,'box_relaxation_common_fixed_agreement':'follows from bipartite incidence total unimodularity'},
 'universal_identity_cases':count,
 'not_verified':['published all-image counts','all real-solver run claims','cited central-path rate claims','MATLAB/CVX authors stack execution'],
 'status':'PASS'
}
Path('certificate_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
