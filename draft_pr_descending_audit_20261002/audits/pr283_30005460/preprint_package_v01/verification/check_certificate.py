"""Portable exact rational verification of the local certificate and cubic obstruction.
Python 3 standard library only; no floating point, downloads, or external code.
The written finite tensor and general odd-power proofs are in paper.tex.
"""
import collections, itertools, json, math, pathlib
from fractions import Fraction as F

D = pathlib.Path(__file__).resolve().parent
S = D
C = json.loads((S / 'TENSOR_MOMENT_CERTIFICATE.json').read_text())
counts = collections.Counter()
def check(condition, label):
    if not condition:
        raise AssertionError(label)
    counts[label] += 1
def basis(r):
    return [(a, b, t-a-b) for t in range(r+1) for a in range(t+1) for b in range(t-a+1)]
def add(u,v):
    return tuple(a+b for a,b in zip(u,v))
def gaussian(u):
    if any(v % 2 for v in u):
        return 0
    return math.prod(math.prod(range(1,v,2)) for v in u)
DEGREE6 = {(6,0,0):2**24,(0,6,0):2**24,(4,2,0):1,(2,4,0):1,
           (0,0,6):1,(2,2,2):4,(2,0,4):32,(0,2,4):32,(4,0,2):4096,(0,4,2):4096}
SCALES = {8:10**16,10:10**34,12:10**53,14:10**73,16:10**94,18:10**116}
def moment(u):
    t=sum(u)
    check(t <= 18,'moment_domain')
    if any(v % 2 for v in u):
        return F(0)
    if t == 0:
        return F(1)
    if t in (2,4):
        return F(gaussian(u),1024)
    if t == 6:
        return F(DEGREE6[u])
    return F(SCALES[t]*gaussian(u))
def matrix(rows,cols,fn=moment):
    return [[F(fn(add(a,b))) for b in cols] for a in rows]
def ldl(A):
    n=len(A); L=[[F(i==j) for j in range(n)] for i in range(n)]; p=[]
    for j in range(n):
        pivot=A[j][j]-sum(L[j][k]**2*p[k] for k in range(j))
        check(pivot>0,'positive_exact_LDL_pivot')
        p.append(pivot)
        for i in range(j+1,n):
            L[i][j]=(A[i][j]-sum(L[i][k]*L[j][k]*p[k] for k in range(j)))/pivot
    for i in range(n):
        for j in range(n):
            check(A[i][j]==sum(L[i][k]*p[k]*L[j][k] for k in range(min(i,j)+1)),
                  'exact_LDL_reconstruction')
    return L,p
def solve(dec,b):
    L,p=dec; n=len(p); y=[]
    for i in range(n):
        y.append(b[i]-sum(L[i][j]*y[j] for j in range(i)))
    z=[v/d for v,d in zip(y,p)]; x=[F(0)]*n
    for i in reversed(range(n)):
        x[i]=z[i]-sum(L[j][i]*x[j] for j in range(i+1,n))
    return x
def determinant(A):
    _,p=ldl(A)
    return math.prod(p)
def parity(u):
    return tuple(v % 2 for v in u)
check(C['N']=='10^62' and C['ambient_dimension']=='3*10^62','certificate_parameter_metadata')
check(C['moment_table']=={
    'constant':1,'degrees_two_and_four_scale':'1/1024',
    'degree_six_half_exponents':[[[u//2 for u in a],v] for a,v in sorted(DEGREE6.items())],
    'higher_even_degree_scales':{str(r):'10^'+str(e) for r,e in [(4,16),(5,34),(6,53),(7,73),(8,94),(9,116)]},
    'odd_coordinate_moments':0},'certificate_moment_table')
check([z['order'] for z in C['Schur_extension_steps']]==list(range(4,10)),'all_six_extension_orders')
parities=list(itertools.product(range(2),repeat=3))
check([tuple(z['parity']) for z in C['initial_order_three_blocks']]==parities,'all_eight_initial_parities')
I9=basis(9)
check(len(I9)==220 and len(set(I9))==220,'full_order9_basis')
groups={p:[u for u in I9 if parity(u)==p] for p in parities}
check(max(map(len,groups.values()))==35,'largest_parity_block')
for i,u in enumerate(I9):
    for v in I9[:i]:
        if parity(u)!=parity(v):
            check(moment(add(u,v))==0,'off_parity_zero')
full=[]
for p, rows in groups.items():
    A=matrix(rows,rows)
    _,pivots=ldl(A)
    full.append({'parity':p,'monomials':rows,'rational_pivots':[str(v) for v in pivots]})

# Authenticate the author's compressed witnesses using our own Fraction LDL
# solves, rather than its symbolic DomainMatrix inverses or PSD flags.
for block in C['initial_order_three_blocks']:
    rows=[tuple(u) for u in block['monomials']]
    check(rows==sorted(u for u in basis(3) if parity(u)==tuple(block['parity'])),
          'initial_block_basis_complete')
    A=matrix(rows,rows)
    for k,target in enumerate(block['leading_minors'],1):
        check(determinant([row[:k] for row in A[:k]])==F(target),
              'author_initial_minor_authenticated')
traces=[]
for step in C['Schur_extension_steps']:
    r=step['order']
    check(SCALES[2*r]==10**step['T_power_of_ten'],'extension_scale')
    expected={p for p in parities if any(sum(u)==r and parity(u)==p for u in basis(r))}
    check({tuple(b['parity']) for b in step['blocks']}==expected,'all_extension_blocks_present')
    for block in step['blocks']:
        p=tuple(block['parity'])
        old=[u for u in basis(r-1) if parity(u)==p]
        new=[u for u in basis(r) if sum(u)==r and parity(u)==p]
        check((len(old),len(new))==(block['old_dimension'],block['new_dimension']),
              'extension_block_dimensions')
        A=matrix(old,old); B=matrix(old,new); G=matrix(new,new,gaussian)
        dA=ldl(A); dG=ldl(G)
        X=[solve(dA,[row[j] for row in B]) for j in range(len(new))]
        K=[[sum(B[t][i]*X[j][t] for t in range(len(old))) for j in range(len(new))]
           for i in range(len(new))]
        Y=[solve(dG,[row[j] for row in K]) for j in range(len(new))]
        trace=sum(Y[j][j] for j in range(len(new)))
        check(trace==F(block['trace']),'author_Schur_trace_authenticated')
        check(0<=trace<SCALES[2*r] and F(block['strict_bound'])==SCALES[2*r],
              'author_strict_trace_inequality')
        traces.append({'order':r,'parity':p,'trace':str(trace),'strict_bound':str(SCALES[2*r])})

# Sparse exact multiplication for the credited coefficient-1 seed cube.
def mul(a,b):
    out=collections.defaultdict(F)
    for u,c in a.items():
        for v,d in b.items():
            out[add(u,v)]+=c*d
    return {u:c for u,c in out.items() if c}
def power(a,q):
    result={(0,0,0):F(1)}
    for _ in range(q):
        result=mul(result,a)
    return result
def binomial(u,v,c=1):
    return {tuple(u):F(1),tuple(v):F(-c)}
seed={(4,2,0):F(1),(2,4,0):F(1),(0,0,6):F(1),(2,2,2):F(-1)}
polys=[power(seed,j) for j in (1,2,3)]
values=[sum(c*moment(u) for u,c in f.items()) for f in polys]
check(values==[-1,11292*10**53,35039520*10**116],'three_seed_moments')
check([str(v) for v in values]==C['seed_moments'],'recorded_seed_moments')
H=[((5,4,0),(3,4,2)),((4,5,0),(4,3,2)),
   ((4,2,3),(2,2,5)),((2,4,3),(2,2,5)),
   ((1,2,6),(3,4,2)),((2,1,6),(4,3,2)),
   ((2,4,3),(4,2,3)),((4,5,0),(2,1,6)),((5,4,0),(1,2,6))]
terms=[(F(3,2),binomial(u,v)) for u,v in H]
terms += [(F(1),binomial(u,v,2)) for u,v in
          [((0,0,9),(2,2,5)),((1,1,7),(3,3,3)),
           ((3,6,0),(3,4,2)),((3,5,1),(3,3,3)),
           ((6,3,0),(4,3,2)),((5,3,1),(3,3,3))]]
terms += [(F(2),{(3,3,3):F(1)})]
rhs=collections.defaultdict(F)
for coefficient,h in terms:
    check(coefficient>0,'cube_weight_positive')
    check(all(sum(u)==9 for u in h),'cube_square_degree9')
    for u,c in mul(h,h).items():
        rhs[u]+=coefficient*c
check(polys[2]=={u:c for u,c in rhs.items() if c},'credited_cube_identity')

# Derive the finite cubic expression by direct compositions for small N,
# then prove the exact integer inequality for the stated enormous N.
for n in (1,2,3,4,7):
    direct=F(0)
    for indices in itertools.product(range(n),repeat=3):
        direct+=math.prod(values[count-1] for count in collections.Counter(indices).values())
    formula=n*values[2]+3*n*(n-1)*values[1]*values[0]+n*(n-1)*(n-2)*values[0]**3
    check(direct==formula,'direct_tensor_cubic_count')
N=10**62
expr=N*values[2]+3*N*(N-1)*values[1]*values[0]+N*(N-1)*(N-2)*values[0]**3
bound=N*(values[2]-(N*N-1))
check(values[1]>=values[0]**2,'Cauchy_Schwarz_second_moment')
check(values[2]<N*N-1 and expr<=bound<0,'exact_finite_nonSOS_separation')
check(str(expr)==C['negative_tensor_cube_value'],'certificate_negative_value_authenticated')

# Deterministic output: finite certificate checks, not a global proof checker.
print(json.dumps({
    'status':'PASS_EXACT_RATIONAL_CERTIFICATE',
    'arithmetic':'Python standard-library integers and Fraction; no floating point',
    'local_moment_matrix_dimension':220,
    'positive_local_LDL_pivots':sum(len(b['rational_pivots']) for b in full),
    'initial_minors_authenticated':sum(len(b['leading_minors']) for b in C['initial_order_three_blocks']),
    'Schur_traces_authenticated':len(traces),
    'cube_square_terms':len(terms),
    'seed_moments':[str(v) for v in values],
    'N':str(N),'n':str(3*N),'m':6,'q':3,
    'negative_tensor_cube_value':str(expr),
    'negative_upper_bound':str(bound),
    'checks':dict(sorted(counts.items())),
    'scope':'Exact local moment positivity, compressed certificate, seed cube, moments, finite cubic sign and finite counting controls. Arbitrary finite product positivity and every-odd-q existence require the written proof.',
},sort_keys=True,indent=2))
