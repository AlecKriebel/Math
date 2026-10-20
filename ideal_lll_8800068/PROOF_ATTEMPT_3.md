# Proof attempt 3: growing evaluation-kernel ideals

Date: 2026-10-20 UTC. ID 8800068 / AMR-087-0068.

## Result

A genuinely growing family of coefficient ideals with an exact planted shortest vector is constructed, with modulus and evaluation point chosen at the scales necessary to avoid two simple exponential-rate obstructions. The natural basis, HNF-style basis, and 96 randomly transformed bases were reduced exactly in dimensions through 16; all 112 reductions returned a shortest first vector. This fails to produce the desired bad reduced bases, but does not prove that none exist. A fixed-modulus extension of the quadratic example is ruled out analytically, and making the evaluation point excessively large is also proved counterproductive for this family.

The target remains the broad varying-monic-q, coefficient-Euclidean, classical LLL, existential reduced-input, first-vector/SVP exponent-1/2 target from attempt 1. No equivalence to cyclic or cyclotomic restrictions is assumed.

## 1. Why simply extending the quadratic example cannot work

For the evaluation kernel

    L(a,m,n)={v in Z^n : sum_(j=0)^(n-1) v_j a^j =0 mod m},

surjectivity through the constant coordinate gives det(L)=m. The classical Hermite estimate gives, for every reduced basis,

    ||b_1||/lambda_1(L) <= 2^((n-1)/4) m^(1/n)/lambda_1(L).

Since an integral lattice has lambda_1>=1, a family with log_2(m)=o(n^2) cannot have SVP exponent exceeding 1/4+o(1). In particular, keeping m=300 and a=18 from the quadratic example and merely increasing n cannot reach exponent 1/2.

Conversely any evaluation-kernel family attaining the target must satisfy

    log_2(m) >= (1/4-o(1))n^2 + n log_2(lambda_1(L)).

A second restriction comes from the n-1 independent relation vectors

    r_i=a e_i-e_(i+1),  0<=i<=n-2,

all of norm sqrt(a^2+1). The independent-short-vector bound proved in the accompanying cyclic analysis, applied to these vectors without requiring them to be shortest, gives

    ||b_1|| <= sqrt(a^2+1) 2^(n/4).

(The bound for d vectors of norm at most A is ||b_1||<=A 2^((2n-d-1)/4). Its proof depends only on an integral nonzero exterior minor and the LLL Gram-Schmidt inequalities.) Thus the target also requires

    sqrt(a^2+1)/lambda_1(L) >= 2^((1/4-o(1))n).

These restrictions are necessary, not sufficient. They are why a fixed evaluation point or a modest determinant should not be expected to supply the sharp target.

## 2. A family meeting the necessary scales

For n>=2 choose

    a_n=2^ceil(n/4),
    m_n=a_n^(n-1)+1,
    q_n=X^n+a_n.

Because q_n(a_n)=a_n m_n, evaluation at a_n modulo m_n is a well-defined surjection

    Z[X]/(q_n) -> Z/m_n.

Let I_n be its kernel, equivalently (m_n,X-a_n) in this quotient ring. Its coefficient lattice L_n is exactly L(a_n,m_n,n), is full rank, and has determinant m_n. No unproved ideal closure is used here. The q_n need not be irreducible, and this is not a cyclic-coordinate construction.

The vector

    v=e_0+e_(n-1)

evaluates to m_n and has norm sqrt(2). No unit coordinate vector lies in L_n, since 0<a_n^j<m_n for 0<=j<n. The only integral vectors of norm less than sqrt(2) are the unit coordinate vectors and zero. Hence

    lambda_1(L_n)=sqrt(2).

The family has log_2 m_n=(n-1)ceil(n/4)+o(1)=n^2/4+O(n) and log_2 a_n=n/4+O(1), so neither necessary scale restriction above excludes exponent 1/2. This does not establish attainability.

An explicit integral basis is

    r_i=a_n e_i-e_(i+1),  0<=i<=n-2,
    v=e_0+e_(n-1).

All rows evaluate to zero modulo m_n. Its determinant has absolute value a_n^(n-1)+1=m_n, so these vectors generate the entire ideal lattice. The determinant identity follows, for example, by eliminating the first n-1 bidiagonal rows or by expansion in the last row.

## 3. Too large an evaluation point forces success instead

For this paragraph let a>=2, m=a^(n-1)+1, and L=L(a,m,n), with v=e_0+e_(n-1). Every lattice vector w satisfying

    ||w|| < (a-1)/2

is an integer multiple of v.

To prove this, write w(a)=k m, let c=w_(n-1), and set M=(a-1)/2. Since all coordinates have absolute value less than M,

    |k-c| = |sum_(i=0)^(n-2) w_i a^i-c|/m
      < M((a^(n-1)-1)/(a-1)+1)/m
      = (a^(n-1)+a-2)/(2m) < 1.

Therefore k=c. Reducing the identity sum_(i=0)^(n-2)w_i a^i=c modulo a gives w_0-c divisible by a. But |w_0-c|<a-1<a, so w_0=c. After subtracting and dividing by a, successive reductions modulo a force w_1=...=w_(n-2)=0, since each has absolute value less than a. Thus w=c v, as claimed.

The general LLL SVP estimate is ||b_1||<=2^((n-1)/2)sqrt(2)=2^(n/2). If

    a>2^(n/2+1)+1,

every reduced first vector therefore lies on Z v. A basis vector is primitive in its lattice, and v belongs to the lattice, so the first basis vector must be ±v. Thus in this large-a regime **every** reduced basis returns an exact shortest first vector.

This proves that inflating a without restraint is not a route to a sharp lower bound. The selected a_n near 2^(n/4) avoids this exclusion; the unresolved range is substantive, not empty.

## 4. Exact experiment

The script computation/check_attempt_3.py uses deterministic seed 880006803, dimensions n=2,3,4,6,8,10,12,16, and the parameters above. For each dimension it reduces:

1. A kernel HNF-style basis with first row (m,0,...,0) and subsequent rows (-a^i mod m)e_0+e_i (the code uses a negative least nonnegative power residue).
2. The explicit relation basis from section 2.
3. Twelve independently scrambled copies of the relation basis. Each scramble applies 5n elementary row additions with a uniformly selected distinct row pair and coefficient from {-3,-2,-1,1,2,3}.

SymPy's exact rational LLL is called at delta=3/4. Each output is independently checked in exact arithmetic for all size and Lovasz inequalities, membership in the evaluation kernel, and determinant magnitude m. These last two checks certify equality with the full ideal lattice, not only closure of a sublattice.

All 112 runs completed without errors. In every output the first-vector squared norm was 2, equal to the proved lambda_1^2. The per-dimension values and counts are saved in computation/ATTEMPT_3_RESULTS.txt.

This experiment demonstrates failure of these selected starts to expose a bad reduced basis. It does not enumerate reduced bases and does not exclude stationary adversarial inputs outside the tested set. No empirical probability or asymptotic success claim is made.

## 5. Remaining gap

This attempt supplies a fully verified growing ideal family and a precise parameter window, but no bad reduced basis. Obtaining a ratio of order 2^(n/2) would require finding a highly nonstandard reduced basis of this family or replacing the family. The planted vector has maximal possible polynomial degree n-1, so the simple no-wrap-shift multiplicity argument does not itself force many independent shortest vectors. The direct relation basis and tested HNF/random starts expose it immediately.

Direct sums of the two-dimensional example would not amplify its ratio, and tensor powers would change dimension exponentially and require a separate coefficient-ideal geometry proof. Neither is used as a shortcut here.

Attempt 3 outcome: **fixed-modulus extension refuted; exact growing kernel family constructed and analyzed; excessively large evaluation points proved easy for every reduced basis; concrete finite search unsuccessful; target unresolved.**
