"""New package03 exact checks and unconditional wrapper fault injection."""
import sys
sys.dont_write_bytecode=True
from fractions import Fraction as Q
from pathlib import Path
import json,importlib.util,hashlib,math
HERE=Path(__file__).resolve().parent;KIT=HERE.parents[1]/'NEWpreprint_v1_0'
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def deriv(p):return [i*p[i] for i in range(1,len(p))]
def multiply(p,q):
    out=[Q(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):out[i+j]+=a*b
    return out
def integ(p):return sum((a/Q(i+1) for i,a in enumerate(p)),Q(0))
def value(p,x):
    out=Q(0)
    for a in reversed(p):out=out*x+a
    return out
def dot(a,b):return sum((x*y for x,y in zip(a,b)),Q(0))
def mm(A,B):return [[dot(row,col) for col in zip(*B)] for row in A]
def trans(A):return [list(x) for x in zip(*A)]
phi=list(map(Q,[0,0,0,0,1,-4,6,-4,1]));d=[phi]
for k in range(4):d.append(deriv(d[-1]))
a=integ(multiply(d[1],d[1]));b=integ(multiply(d[2],d[2]))
need(a==Q(4,45045),'area pairing mismatch')
need(all(value(d[k],Q(x))==0 for k in range(4) for x in [0,1]),'endpoint trace failure')
# Brownian dual representation is u_h proportional to i*h-prime Fourier.
# Parseval yields true diagonal witness norms int f-prime^2 and int g-prime^2;
# cell disjointness removes every off-diagonal entry, including n=1.
need(a/b>0 and a/b<Q(1,4),'Brownian witness inconsistent with optimum')
brownian=[]
for n in [1,3,6,17]:
    for r in [1,2,5,9]:
        m=n*r;err=Q(0)
        # Independent Gaussian fine increments. Project the mixed polygonal
        # kernel on both coarse block-sum spaces by exact block averaging.
        for j in range(m):
            for k in range(m):
                coeff=Q(1) if j<k else Q(1,2) if j==k else Q(0)
                block_j,block_k=j//r,k//r
                average=Q(1) if block_j<block_k else Q(1,2) if block_j==block_k else Q(0)
                err+=(coeff-average)**2/Q(m*m)
        formula=Q(r-1,4*n*r)
        need(err==formula,'Brownian conditional tensor projection mismatch')
        brownian.append({'n':n,'refinement_per_cell':r,'exact_projected_polygon_variance':str(err),'formula':str(formula),'limit_as_refinement_infinity':str(Q(1,4*n))})
# A noncommuting signed PSD trace example, constructed as rational Gram matrices.
S=[[Q(1),Q(-2),Q(0)],[Q(0),Q(1),Q(2)],[Q(1),Q(0),Q(1)]]
T=[[Q(2),Q(1),Q(0)],[Q(1),Q(-1),Q(1)],[Q(0),Q(1),Q(1)]]
A=mm(S,trans(S));C=mm(T,trans(T));AC=mm(A,C);CA=mm(C,A)
need(AC!=CA,'adverse PSD pair accidentally commutes')
tr=sum(AC[i][i] for i in range(3));Mf=sum(x*x for row in S for x in row);Mg=sum(x*x for row in T for x in row)
need(tr==sum(A[j][k]*C[j][k] for j in range(3) for k in range(3)) and tr<=3*Mf*Mg,'PSD trace inequality failed')
# Check correct exact Brownian tail comparison after removing pi powers.
partial=sum((Q(1,(2*k-1)**4) for k in range(1,501)),Q(0));need(partial<Q(7,6),'odd tail bound false')
sys.path.insert(0,str(KIT/'scripts'));import check
base=json.loads((KIT/'checks/original_expected.json').read_text());faults=[]
for key in base:
    if key=='utc':continue
    mutated=dict(base);mutated.pop(key)
    try:check.result_guard(mutated,base)
    except RuntimeError:faults.append({'missing_mathematical_field':key,'rejected':True})
    else:raise RuntimeError('Full-result guard accepted removed field '+key)
changed=dict(base);changed['utc']='different timestamp';check.result_guard(changed,base)
# Stronger counterexample to a tempting false lower increment coercivity:
# all-one unit increments telescope exactly. For rational 2H=1/2, compare n=16.
rough_telescope={'H':'1/4 (boundary demonstration only)','n':16,'variance_of_sum':'4','sum_of_unit_variances':'16','ratio':'1/4','general_ratio':'n^(2H-1) -> 0 for every H<1/2'}
out={'schema':'package03_independent_exact_checks_v1','exact_area_pairing':str(a),'int_phi_second_squared':str(b),'brownian_true_witness_constant_squared':str(a/b),'brownian_optimal_constant_squared':'1/4','brownian_tensor_projection_checks':brownian,'noncommuting_signed_PSD_trace':{'A':[[str(x) for x in row] for row in A],'C':[[str(x) for x in row] for row in C],'trace_AC':str(tr),'upper':str(3*Mf*Mg),'noncommuting':True},'odd_series_partial_500_less_than_7_over_6':True,'full_result_guard_each_field_faults':faults,'utc_only_difference_accepted':True,'rough_increment_coercivity_countermechanism':rough_telescope,'normalization':'Mixed independent Gaussian tensor isometry has factor1; unhalved antisymmetric residual has four times variance.','limits':'Exact finite rational checks and explicit algebra only; no interval-certified quadrature or universal numerical proof.'}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'exact_checks':'PASS','brownian_projections':len(brownian),'full_result_faults':len(faults),'mode_optimized':not __debug__}))
