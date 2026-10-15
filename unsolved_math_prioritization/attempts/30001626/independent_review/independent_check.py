"""Independent finite controls for the Cartan/root centralizer audit.

Direct commutator nullities in several real/complex forms, rather than
importing the author checker. These do not prove Baire or cardinality claims.
"""
import sympy as s
from collections import Counter
import json
C=Counter()
def ck(value,label):
    assert value,label
    C[label]+=1
def E(n,i,j):
    A=s.zeros(n);A[i,j]=1;return A
def comm(A,B):return A*B-B*A
def zero(A,label):ck(all(s.simplify(x)==0 for x in A),label)
def column(A):return s.Matrix(list(A))
def nullity_on(H,basis):
    matrix=s.Matrix.hstack(*(column(comm(H,B)) for B in basis))
    return len(basis)-matrix.rank()

for n in range(2,8):
    basis=[E(n,i,j) for i in range(n) for j in range(n)]
    H=s.diag(*[s.Rational(1,3**j) for j in range(1,n+1)])
    ck(nullity_on(H,basis)==n,'complex_full_centralizer_nullity')
    Hbad=H.copy();Hbad[1,1]=Hbad[0,0]
    ck(nullity_on(Hbad,basis)==n+2,'collision_enlarges_centralizer')
    # Actual complex coefficients challenge the extraction signs.
    A=s.Matrix(n,n,lambda i,j:s.Rational(2*i+j+3,7)+s.I*s.Rational(i-3*j+1,11))
    for i in range(n):
      for j in range(n):
        if i==j:continue
        B=comm(E(n,i,i),comm(A,E(n,j,j)))
        zero((B+comm(E(n,i,i),B))/2-A[i,j]*E(n,i,j),'complex_ideal_extraction')
        zero(comm(E(n,i,j),E(n,j,i))-(E(n,i,i)-E(n,j,j)),'diagonal_difference_bracket')
    # Normal real Cartans can mix real eigenvalues and conjugate pairs.
    for pairs in range(n//2+1):
        singles=n-2*pairs;H=s.zeros(n)
        for j in range(singles):H[j,j]=10+j
        for j in range(pairs):
            k=singles+2*j;aa=s.Rational(j+1,3);bb=s.Rational(1,j+2)
            H[k,k]=H[k+1,k+1]=aa;H[k,k+1]=-bb;H[k+1,k]=bb
        zero(comm(H,H.T),'real_normal_model')
        ck(nullity_on(H,basis)==n,'mixed_real_cartan_nullity')
        zero(comm((H+H.T)/2,(H-H.T)/2),'real_star_parts_commute')

for n in range(3,10):
    basis=[E(n,i,j)-E(n,j,i) for i in range(n) for j in range(i+1,n)]
    H=s.zeros(n)
    for j in range(n//2):H[2*j,2*j+1]=s.Rational(1,3**j);H[2*j+1,2*j]=-s.Rational(1,3**j)
    ck(nullity_on(H,basis)==n//2,'compact_real_orthogonal_nullity')
    for B in basis:zero(comm(H,B)+comm(H,B).T,'compact_real_bracket_closed')

for r in range(1,5):
    n=2*r;signs=[1]*r+[-1]*r;J=s.diag(*signs)
    basis=[E(n,i,j)-signs[i]*signs[j]*E(n,j,i) for i in range(n) for j in range(i+1,n)]
    H=s.zeros(n)
    for j in range(r):H[j,r+j]=H[r+j,j]=s.Rational(1,3**j)
    zero(H.T*J+J*H,'split_real_model_in_form')
    ck(nullity_on(H,basis)==r,'split_real_orthogonal_nullity')
    for B in basis:
        zero(B.T*J+J*B,'split_basis_in_form')
        A=comm(H,B);zero(A.T*J+J*A,'split_bracket_closed')

for r in range(1,5):
    n=2*r;Omega=s.zeros(n)
    for i in range(r):Omega[i,r+i]=1;Omega[r+i,i]=-1
    basis=[]
    for i in range(r):
      for j in range(r):basis.append(E(n,i,j)-E(n,r+j,r+i))
    for i in range(r):
      for j in range(i,r):
        B=E(n,i,r+j);D=E(n,r+i,j)
        if i!=j:B+=E(n,j,r+i);D+=E(n,r+j,i)
        basis.extend([B,D])
    H=s.diag(*([s.Rational(1,3**j) for j in range(r)]+[-s.Rational(1,3**j) for j in range(r)]))
    ck(len(basis)==r*(2*r+1),'symplectic_dimension')
    ck(nullity_on(H,basis)==r,'symplectic_centralizer_nullity')
    for B in basis:zero(B.T*Omega+Omega*B,'symplectic_basis_in_form')

for n in range(2,6):
  for seed in range(1,9):
    A=s.Matrix(n,n,lambda i,j:s.Rational(i+2*j+seed,seed+2)+s.I*s.Rational(2*i-j-seed,seed+3))
    B=s.Matrix(n,n,lambda i,j:s.Rational(3*i-j+seed,seed+4)+s.I*s.Rational(i+j+1,seed+5))
    Z=s.Matrix(n,n,lambda i,j:s.Rational(i-j+2,seed+3)+s.I*s.Rational(i+2*j-seed,seed+6))
    zero(s.Matrix([s.trace(comm(A,B).conjugate().T*Z)-s.trace(B.conjugate().T*comm(A.conjugate().T,Z))]),'Hilbert_Schmidt_adjoint_identity')

for n in range(1,101):
    ck(n*s.Rational(1,n)**2==s.Rational(1,n),'trace_zero_approximation_squared_norm')
    lam=s.Rational(1,2**n);next_lam=s.Rational(1,2**(n+1))
    ck(0<lam-next_lam==next_lam,'small_nonzero_roots_no_inverse_bound')

print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(sorted(C.items())),'sympy_version':s.__version__,'scope':'Independent finite real/complex centralizer, adjoint and ideal controls. Completeness, Baire category, Hilbert root decomposition and nonseparable cardinality are reviewed analytically, not inferred from these tests.'},indent=2,sort_keys=True))
