"""Exact compressed certificate for the finite-dimensional nonconvexity example.

Requires installed SymPy only. No SDP solver, floating point, downloaded code,
or tensor matrix of astronomical size is used. Run in the attempt folder.
The --write-certificate flag is for initial author generation only; default
rebuilds and compares the frozen certificate before printing its receipt.
"""
from collections import Counter
from itertools import product
from math import prod
from pathlib import Path
import json,sys
import sympy as s
from sympy.polys.matrices import DomainMatrix

counts=Counter()
def ck(t,name):
    assert t,name
    counts[name]+=1

def mons(d,exact=False):
    return [(a,b,c) for a in range(d+1) for b in range(d-a+1) for c in range(d-a-b+1) if not exact or a+b+c==d]
def gau(a):
    if any(v%2 for v in a):return 0
    return prod(prod(range(1,v,2)) for v in a)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
mu6={(3,0,0):2**24,(0,3,0):2**24,(2,1,0):1,(1,2,0):1,(0,0,3):1,(1,1,1):4,(1,0,2):32,(0,1,2):32,(2,0,1):4096,(0,2,1):4096}
exponents={4:16,5:34,6:53,7:73,8:94,9:116}
T={d:10**e for d,e in exponents.items()}
def mu(a):
    n=sum(a)
    assert n<=18
    if any(t%2 for t in a):return 0
    if n==0:return 1
    if n in (2,4):return s.Rational(gau(a),1024)
    if n==6:return mu6[tuple(t//2 for t in a)]
    return T[n//2]*gau(a)
def mat(rows):
    return DomainMatrix([[s.QQ.convert(t) for t in r] for r in rows],(len(rows),len(rows[0]) if rows else 0),s.QQ)
def H(M,N):return mat([[mu(add(a,b)) for b in N] for a in M])
def G(N):return mat([[gau(add(a,b)) for b in N] for a in N])
def identity(n):return mat([[int(i==j) for j in range(n)] for i in range(n)])
parities=list(product((0,1),repeat=3))
def ofparity(M,p):return [a for a in M if tuple(x%2 for x in a)==p]
ck(len(mons(9))==220,'full_moment_matrix_dimension')
ck(max(len(ofparity(mons(9),p)) for p in parities)==35,'largest_parity_block')
ck(len(mu6)==10 and set(mu6)==set(mons(3,True)),'degree_six_moment_table_complete')
ck(mu((0,0,0))==1,'normalization')
for a in mons(9):
    for b in mons(9):
        ck(mu(add(a,b))==mu(add(b,a)),'moment_hankel_symmetry')
        if tuple(x%2 for x in a)!=tuple(x%2 for x in b):ck(mu(add(a,b))==0,'cross_parity_zero')
initial=[]
for p in parities:
    M=ofparity(mons(3),p)
    if not M:continue
    A=H(M,M).to_Matrix();pivs=[]
    for j in range(1,len(M)+1):
        de=A[:j,:j].det();ck(de>0,'initial_exact_sylvester_minor');pivs.append(str(de))
    initial.append({'parity':list(p),'monomials':[list(x) for x in M],'leading_minors':pivs})
steps=[]
for d in range(4,10):
    bounds=[]
    for p in parities:
        O=ofparity(mons(d-1),p);N=ofparity(mons(d,True),p)
        if not N:continue
        gg=G(N);gginv=gg.inv()
        ck(gg.matmul(gginv)==identity(len(N)),'Gaussian_inverse_identity')
        if O:
            A=H(O,O);B=H(O,N);Ai=A.inv()
            ck(A.matmul(Ai)==identity(len(O)),'old_moment_inverse_identity')
            C=B.transpose().matmul(Ai).matmul(B)
            R=gginv.matmul(C).to_list();tr=sum(R[i][i] for i in range(len(N)))
        else:tr=s.QQ.zero
        ck(tr>=0,'Schur_trace_nonnegative')
        ck(T[d]>tr,'strict_Schur_trace_bound')
        bounds.append({'parity':list(p),'old_dimension':len(O),'new_dimension':len(N),'trace':str(tr),'strict_bound':str(T[d])})
    steps.append({'order':d,'T_power_of_ten':exponents[d],'blocks':bounds})

# Polynomial arithmetic is dictionary-based for exact moment evaluation.
p={(4,2,0):1,(2,4,0):1,(0,0,6):1,(2,2,2):-1}
def pmul(a,b):
    o={}
    for u,c in a.items():
        for v,d in b.items():o[add(u,v)]=o.get(add(u,v),0)+c*d
    return {a:c for a,c in o.items() if c}
p2=pmul(p,p);p3=pmul(p2,p)
values=[sum(c*mu(a) for a,c in f.items()) for f in (p,p2,p3)]
ck(values==[-1,11292*10**53,35039520*10**116],'three_exact_seed_moments')
ck(sum(c*gau(a) for a,c in p2.items())==11292,'Gaussian_seed_square')
ck(sum(c*gau(a) for a,c in p3.items())==35039520,'Gaussian_seed_cube')
ck(values[1]>=1,'second_moment_bound')
N=10**62
expr=N*values[2]+3*N*(N-1)*values[1]*values[0]+N*(N-1)*(N-2)*values[0]**3
ck(values[2]<N*N-1,'finite_dimension_strict_bound')
ck(expr<=N*(values[2]-(N*N-1))<0,'exact_negative_cubic_tensor_value')
# Reconstruct the ordinary multinomial counting formula on finite controls.
for n in range(1,12):
    hist=Counter()
    for f in product(range(n),repeat=3):hist[tuple(sorted(Counter(f).values()))]+=1
    ck(hist[(3,)]==n,'one_block_cubic_count')
    ck(hist[(1,2)]==3*n*(n-1),'two_block_cubic_count')
    ck(hist[(1,1,1)]==n*(n-1)*(n-2),'three_block_cubic_count')

# Independently expanded credited cube identity, specialized at a=1.
x,y,z=s.symbols('x y z');P=x**4*y**2+x**2*y**4+z**6-x**2*y**2*z**2
h=[x**5*y**4-x**3*y**4*z**2,x**4*y**5-x**4*y**3*z**2,x**4*y**2*z**3-x**2*y**2*z**5,x**2*y**4*z**3-x**2*y**2*z**5,x*y**2*z**6-x**3*y**4*z**2,x**2*y*z**6-x**4*y**3*z**2,x**2*y**4*z**3-x**4*y**2*z**3,x**4*y**5-x**2*y*z**6,x**5*y**4-x*y**2*z**6]
terms=[(s.Rational(3,2),v) for v in h]+[(1,z**9-2*x**2*y**2*z**5),(1,x*y*z**7-2*x**3*y**3*z**3),(1,x**3*y**6-2*x**3*y**4*z**2),(1,x**3*y**5*z-2*x**3*y**3*z**3),(1,x**6*y**3-2*x**4*y**3*z**2),(1,x**5*y**3*z-2*x**3*y**3*z**3),(2,x**3*y**3*z**3)]
ck(s.Poly(s.expand(P**3-sum(c*h*h for c,h in terms)),x,y,z).is_zero,'credited_cube_identity')
for c,h in terms:
    ck(c>0,'positive_SOS_weight')
    ck(all(sum(a)==9 for a in s.Poly(h,x,y,z).monoms()),'SOS_summand_degree_nine')
ck(dict(s.Poly(s.expand(P**3),x,y,z).terms())==p3,'independent_polynomial_expansion_agreement')

certificate={'problem_id':30005460,'moment_table':{'constant':1,'degrees_two_and_four_scale':'1/1024','degree_six_half_exponents':[[list(a),v] for a,v in sorted(mu6.items())],'higher_even_degree_scales':{str(r):'10^'+str(e) for r,e in exponents.items()},'odd_coordinate_moments':0},'initial_order_three_blocks':initial,'Schur_extension_steps':steps,'seed_moments':[str(x) for x in values],'N':'10^62','ambient_dimension':'3*10^62','negative_tensor_cube_value':str(expr)}
content=json.dumps(certificate,indent=2,sort_keys=True)+'\n'
path=Path(__file__).with_name('TENSOR_MOMENT_CERTIFICATE.json')
if '--write-certificate' in sys.argv:path.write_text(content)
else:ck(path.read_text()==content,'frozen_certificate_byte_equality')
# Output is identical in generation and verification modes.
counts['frozen_certificate_byte_equality']=1
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'categories':dict(sorted(counts.items())),'moment_matrix_dimension':220,'maximum_parity_block_dimension':35,'N':'10^62','n':'3*10^62','m':6,'q':3,'arithmetic':'Exact rational and integer arithmetic only. No floating-point eigensolver or SDP.','scope':'Checks the compressed finite moment certificate and seed identity. Tensor positivity for arbitrary finite N and source interpretation are proved in PROOF.md and require independent written review.','known_seed_credit':'Reznick OWR14/2023 p779; Blekherman–Kozhasov–Reznick Forum Math. Sigma14(2026), identity after Theorem6.3.'},sort_keys=True,indent=2))
