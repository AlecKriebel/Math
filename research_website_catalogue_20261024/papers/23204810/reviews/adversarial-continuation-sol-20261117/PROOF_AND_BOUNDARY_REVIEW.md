# Exact consequence and adversarial algebraic reconstruction

The claim under review remains the original universal claim, including its
equality witness and all ideals. It is not replaced by a characteristic-zero
monomial case, finite list of degree sequences or conditional-only public page.
The imported Artinian EGH proof has been examined in PRIMARY_ANALYSIS.md.

Let k be ANY characteristic-zero field, n>=0, and f_1,...,f_n a homogeneous
regular sequence of positive degrees in S=k[x_1,...,x_n]. Let A=S/(f_i),
m=A_+, c=sum(d_i-1), h_j=dim_k A_j, and p the LAST maximal Hilbert degree.
I ranges over every ideal of A, including0,A and nonhomogeneous ideals.

## Full-length EGH and the field/degree interface

If r defining forms are linear, they are independent: otherwise fewer than n
equations would have height n. A linear change eliminates them. The remaining
restrictions cannot vanish, because that would leave too few equations for
an Artinian quotient; they retain their homogeneous degrees>=2. They form a
system of parameters in a polynomial ring, hence a regular sequence. The
graded isomorphism preserves all ideals, mu and Hilbert dimensions. All
eliminated Hilbert factors equal1. If no variables remain, A=k: mu(0)=0,
mu(A)=1, p=0, m^0=A and the empty product is1. This handles n=0/all-linear
without applying an upstream theorem outside n>=1,a_i>=2.

In the remaining full-length case, sort the degrees using permutability of a
homogeneous system of parameters in the Cohen-Macaulay polynomial ring.
The genuine pinned EGH Corollary1.2 supplies the full complex Hilbert-function
premise for EVERY homogeneous ideal containing the sequence, with ONE pure-
power monomial counterpart in ALL degrees. For a fixed ideal Q over k, choose
a finitely generated coefficient field k_0 over Q containing homogeneous Q
generators and all defining forms; explicitly include the forms among the
Q generators. Faithful flatness descends regularity to k_0. Embed k_0 into C,
apply the complex result, and use its same monomial exponents back over k_0
and k. Graded quotient dimensions commute with both extensions. k_0 may depend
on Q: the bound depends only on the fixed degree list, so this is the correct
'for every Q there exists k_0' quantifier. No embedding of all k into C and
no descent of arbitrary ideals from an extension field is assumed.

Successive regular-sequence Hilbert sequences give

    H_A(t)=product_i(1+t+...+t^(d_i-1)).

The Koszul canonical-module calculation gives graded Gorenstein duality:
A_c is one-dimensional, and A_j times A_(c-j) to A_c is perfect. Product-of-
chains symmetric decomposition proves that h is symmetric and unimodal.
In particular c-p<=p and h_j<=h_(j+1) for all j<p, including a long plateau.

## Matching without transferring generator counts

For B=k[z]/(z_i^a_i), symmetric-chain successors inject any rank-j monomial
subset into its upper shadow whenever h_j<=h_(j+1). Echelonizing a vector
subspace W in a multiplicative monomial order gives distinct surviving leading
monomials. Every surviving variable multiple remains a leading monomial of
the corresponding product, so

    dim W <= dim B_1 W.

For V subset A_j, let I=AV and apply the now checked EGH premise to its
homogeneous preimage Q in S. Obtain J in B with H_(A/I)=H_(B/J). Since A,B
already have the same Hilbert function and I is generated in degree j,

    dim J_j=dim V,
    dim J_(j+1)=dim A_1 V.

The ideal property, followed by monomial matching, gives

    dim V=dim J_j <= dim B_1 J_j <= dim J_(j+1)=dim A_1 V.

V=0 is immediate. This is a subspace expansion statement, not a statement
about one generic linear form. EGH does not preserve mu of transferred ideals.
The sealed INITIAL exhibits two homogeneous ideals of the SAME pure-power
algebra with the same quotient Hilbert function but mu3 and mu2, disproving
that tempting shortcut explicitly.

## Homogeneous ideals: exact truncation and annihilator bound

For homogeneous I with initial degree alpha, standard grading gives
(mI)_d=A_1 I_(d-1). Let I'=direct sum_(d>=alpha+1) I_d. Only the alpha and
alpha+1 generator contributions change, so

    mu(I')-mu(I)=dim A_1 I_alpha-dim I_alpha >=0  if alpha<p.

Iterating gives mu(I)<=mu(I intersect m^p). Zero I is treated immediately,
and if p=0 there is no truncation. Hence it suffices to bound homogeneous
I contained in m^p. Set J=Ann(mI). The socle functional lambda gives a perfect
pairing on all A. For an ideal U, orthogonality to U implies orthogonality to
all multiples ub, hence actual annihilation of each u by nondegeneracy. Thus

    dim Ann(U)=dim A-dim U.

Since mJ subset Ann(I),

    mu(J)>=dim Ann(mI)-dim Ann(I)=dim I-dim mI=mu(I).

Perfect graded pairings also give Ann(m^u)=m^(c-u+1), including u=0,c+1.
For the reverse inclusion, pair any nonzero component of degree j<=c-u
against A_(c-j), a subspace of m^u, to get a nonzero socle projection. Now
mI subset m^(p+1), hence

    J contains Ann(m^(p+1))=m^(c-p), which contains m^p.

Apply truncation to J: J intersect m^p=m^p, so

    mu(I)<=mu(J)<=mu(m^p)=h_p.

This avoids any assumption that I or J maximizes mu before forming its
annihilator. The Gorenstein property is essential to the dimension identity.

## Every ideal and attainment

For arbitrary I, use intersection filtrations F^j I=I intersect m^j and
F^j(mI)=mI intersect m^j. As gr_m A=A, the lowest-degree initial parts make
J=gr_F I a homogeneous ideal. Products of initial parts give

    mJ subset gr_F(mI).

Finite associated grading preserves total k-dimensions, so

    mu(I)=dim J-dim gr_F(mI)
          <=dim J-dim mJ=mu(J)<=h_p.

The inclusion may be strict. In A=k[x,y]/(x^2,y^5), I=(x+y^2) is principal,
but J=(x,y^4) needs two generators. Here dim I=dim J=6, dim mI=5 and
dim mJ=4; the extra initial y^4 comes from y^2(x+y^2)-x(x+y^2). This explicit
same-class calculation confirms the inequality direction and rules out
silently replacing the inclusion by equality.

Finally m^p/m^(p+1)=A_p, so mu(m^p)=h_p. The upper bound and existing witness
prove the maximum over all ideals equals the largest Hilbert coefficient.
No compactness of an ideal parameter space, unique extremizer or genericity
of I is needed. Scalar extension preserves I/mI for a particular I by flatness;
this provides another valid descent route without extending the ideal quantifier.

## HWW actual proof and attribution interface

The explicit arXivv1 primary was read in full. Definition2 uses all ideals;
Proposition7 supplies monomial matching; Proposition8 combines matching,
Gorenstein duality and truncation; Theorem11 transfers the EGH Hilbert data
to matching. Its Proposition8 explicitly invokes Watanabe's graded-ideal
reduction, so the native all-ideal account is not a new implicit extension
of an exclusively homogeneous theorem. Its formulas use standard grading,
which the native hypotheses explicitly provide. The native proof's direct
annihilator inequalities and finite filtration also independently establish
the needed reduction, without depending on the Dilworth-lattice presentation.
The served PDF bears its own2018internal date despite the primary v1 identity
page's2016submission label; that distinction is retained in provenance.

## Remaining adversarial boundaries and ancillary source

The INITIAL rectangle-chain partition is checked pointwise, and its degrees
(2,5) example tests matching ABOVE the midpoint on a plateau. From rank4 to5,
dim A_4=2>dim A_1 A_4=1, refuting matching without its stated Hilbert-growth
condition. Using the first maximum would also break the needed c-p<=p step.
For n=1, every ideal of k[x]/(x^d) is a power ideal, with nonzero generator
count1 and the last layer as witness. Ideals0 and A, all-linear eliminations
and empty products have been checked separately. None is handled by an
unjustified invocation of the degree>=2 imported construction.

No positive-characteristic general theorem, nongraded quotient theorem,
WLP/SLP or new EGH mechanism follows. For example characteristic2 gives
(alpha x+beta y)^2=0 in k[x,y]/(x^2,y^2), despite its monomial Sperner property;
it is an explicit counterexample to a stronger Lefschetz shortcut, not to the
stated char0 conclusion. Arbitrary-cardinality char0 fields are allowed because
only finite coefficient fields are embedded, one containing ideal at a time.

Native hilbert_examples.py was read completely but NOT executed/imported.
Its convolution and bounded-exponent enumeration are exact integer algorithms
for the illustrative coefficients, including the empty Cartesian product.
The declared252small degree multisets count is independently the binomial
identity sum_(n=0)^5 binomial(n+4,4)=binomial(10,5)=252, not an execution receipt.
The displayed examples agree with hand polynomial multiplication; for eight
quadrics H=(1+t)^8 and mu(m^4)=binomial(8,4)=70. These checks are illustrations,
not the universal EGH/Sperner proof. No native reproduction or formal certificate
is claimed, and unused support audit bodies were not read.
