# Proof attempt 5: coupled value-and-derivative ideals

Date: 2026-10-20 UTC. ID 8800068 / AMR-087-0068.

## Outcome

This attempt replaces single modular evaluation by simultaneous value-and-derivative conditions. It constructs a genuinely different growing family whose additive quotient is noncyclic, proves coefficient ideal closure and determinant exactly, and proves an exact shortest-vector length sqrt(6). Its determinant scale avoids the basic Hermite obstruction to the sharp SVP exponent. Nevertheless, all 42 exact reductions of the tested inputs through dimension 17 return shortest first vectors. No poor stationary reduced-basis family is obtained. The original broad target remains unresolved after five distinct attempts.

This is not a cyclic or irreducible-ring construction: the chosen quotient polynomial has repeated factors, which are permitted by the broad general-monic-q formulation but not by several stronger interpretations of the historical question.

## 1. New algebraic construction

Let r>=1, n=2r+1, and let a>=8 be an integer divisible by r. Set

    h=X^r+1,
    m=a^r+1,
    q=X h^2.

The polynomial q is monic of degree n. Let A=(Z/m)[epsilon]/(epsilon^2). Define the ring map

    phi: Z[X]/(q) -> A,  X maps to a+epsilon.

For every polynomial f,

    f(a+epsilon)=f(a)+f'(a)epsilon in A.

Because h(a)=m, both q(a)=a m^2 and q'(a)=m^2+2a m r a^(r-1) vanish modulo m. Thus phi is well defined. It is surjective: 1 is in the image, and epsilon is the image of X-a.

Let I=ker(phi). Equivalently,

    I=(m,(X-a)^2) in Z[X]/(q).

Indeed, polynomial division by the monic (X-a)^2 leaves the remainder f(a)+f'(a)(X-a); the remainder vanishes in A exactly when both coefficients are divisible by m. Consequently the coefficient lattice is

    L={f in Z[X], deg(f)<n: f(a)=f'(a)=0 mod m},

and its determinant is m^2. Its additive quotient is (Z/m)^2, not Z/m^2; it therefore lies outside the single-evaluation/cyclic-additive-quotient class characterized in attempt 2.

An explicit integral coefficient basis consists of m, mX, and, for 2<=j<n,

    X^j+(j-1)a^j-j a^(j-1)X.

Each has zero value and derivative modulo m, and the triangular determinant is m^2, proving equality with the full kernel lattice.

## 2. Exact shortest-vector theorem

**Proposition.** Under the assumptions above, lambda_1(L)=sqrt(6), and its only shortest vectors are plus or minus h^2=1+2X^r+X^(2r).

**Proof.** First h^2 has coefficient norm sqrt(6) and belongs to I: its value is m^2 and its derivative is 2m r a^(r-1), both divisible by m.

Conversely, let a nonzero polynomial f=sum_(j=0)^(2r) f_j X^j belong to L and have coefficient norm at most sqrt(6). Each integer coefficient then has |f_j|<=2. Divide by h:

    f=h g+s,  deg(g)<=r, deg(s)<r.

The coefficients are explicitly

    g_r=f_(2r),
    g_0=f_r-f_(2r),
    g_j=f_(r+j) for 1<=j<=r-1,
    s_0=f_0-f_r+f_(2r),
    s_j=f_j-f_(r+j) for 1<=j<=r-1.

These formulas apply also to r=1, where the middle index ranges are empty. Hence |s_0|<=6 and |s_j|<=4 for j>=1. Since f(a)=0 modulo m and h(a)=m, s(a) is divisible by m. But

    |s(a)| <= 6+4 sum_(j=1)^(r-1) a^j < a^r+1=m.

For a>=8 the strict inequality follows explicitly from

    m-[6+4 sum_(j=1)^(r-1) a^j]
      = (a-5)(a^r-1)/(a-1) >0.

Thus s(a)=0. All coefficients of s have absolute value less than a, so repeated reduction modulo a of the integer equation s(a)=0 forces every coefficient to vanish. Therefore f=h g.

The derivative condition now gives

    0=f'(a)=r a^(r-1)g(a) mod m.

We have gcd(a,m)=1 and, because r divides a, gcd(r,m)=1. Therefore g(a)=0 modulo m.

Let c=g_r=f_(2r), and put t=g-c h. Its degree is less than r, its constant coefficient is f_r-2f_(2r) of absolute value at most 6, and its other coefficients have absolute value at most 2. Because g(a) and c h(a) are divisible by m, t(a) is divisible by m. The same bound just used, with 2<=4 for the nonconstant coefficients, shows |t(a)|<m, and then the same base-a coefficient argument gives t=0. Hence g=c h and f=c h^2.

The norm constraint and f nonzero force c=1 or -1. This proves both the exact minimum and uniqueness up to sign.

## 3. Growing parameters and why this is not immediately excluded

Choose

    a_n=r 2^max(3,ceil(n/4)),  n=2r+1.

Then a_n>=8, r divides a_n, and log_2(a_n)=n/4+O(log n). Since det(L_n)=m_n^2=(a_n^r+1)^2,

    log_2 det(L_n)=2r log_2(a_n)+o(1)=n^2/4+O(n log n).

Thus the determinant is large enough that the Hermite bound does not itself exclude a first-vector ratio 2^{(1/2-o(1))n}. The shortest norm remains the constant sqrt(6), rather than being inferred from determinant or experimental output.

The elementary relation (X-a)^2 has coefficient norm sqrt(a^4+4a^2+1) and supplies n-2 independent shifted vectors of that same norm. The independent-short-vector bound yields

    ||b_1|| <= sqrt(a^4+4a^2+1) 2^((n+1)/4),

which is too weak at the selected a_n to exclude the sharp target. It is not being presented as evidence that the target is attainable.

The unique shortest polynomial h^2 has maximal degree n-1 and is annihilated by multiplication by X in this quotient, since q=X h^2. Thus one cannot create n independent short vectors by rotating it; the orthogonal full-orbit obstruction does not apply. Multiplication by X is not an orthogonal cyclic shift here. These observations identify why the new family escapes earlier simple obstructions, without supplying a bad basis.

## 4. Exact computational attempt

The script computation/check_attempt_5.py uses dimensions 3,5,7,9,13,17 and the growing parameters above. For each dimension it starts with the explicit basis in section 1. It first reduces the first two coefficients of each higher row to centered residues modulo m by adding integer multiples of the rows m and mX. These are unimodular row operations and preserve the ideal exactly.

It then tests that basis and six scrambled versions of its initial exact LLL reduction. Each scramble applies 4n elementary row additions with distinct random row indices and coefficient from {-2,-1,1,2}, using deterministic seed 880006805. Every returned output is independently checked in exact arithmetic for size reduction, Lovasz inequalities, both modular membership conditions, and determinant magnitude m^2.

All 42 final tested reductions completed and had first-vector squared norm 6, exactly the proved lambda_1^2. The values and per-dimension counts are recorded in computation/ATTEMPT_5_RESULTS.txt. As in attempt 3, these are selected input runs, not enumeration of all reduced bases and not an asymptotic theorem about LLL.

One preliminary run using enormous unreduced representatives in dimension 17 triggered an internal SymPy LLL assertion before producing a verified output. The centered-residue basis transformation above resolved that computational issue. The final script is reproducible and validates its outputs independently; the failed preliminary call is not counted as a successful reduction or as mathematical evidence.

## 5. Remaining gap and final status of this attempt

The coupling through derivatives gives a noncyclic additive quotient and a rigorous new exact-shortest-vector family, not merely another presentation of the single-evaluation ideals. It does not solve the key basis-design problem: no already-reduced basis with exponentially bad first vector is constructed. The tested algorithmic inputs all reveal the short relation.

The failure of these particular starts does not establish a universal good-output result for the family. Likewise the repeated-factor quotient is not a substitute for cyclic, cyclotomic, irreducible, or HNF-start requirements. A genuine acceptance of the broad target would still require an unbounded family of verified reduced bases with the stated asymptotic ratio; none of the five attempts supplies one.

Attempt 5 outcome: **new coupled ideal family and exact SVP certificate established; finite reduction experiment unsuccessful; broad sharp-rate target unresolved.**
