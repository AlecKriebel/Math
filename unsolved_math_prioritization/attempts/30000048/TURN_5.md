# Turn 5: unrestricted Hermitian-sum-of-squares rigidity for SU(3)

2026-10-02. Fifth and final substantive author turn for problem 30000048. **The original problem remains unresolved and the five-turn attempt is exhausted.** This turn proves a larger, unbounded partial theorem that permits non-diagonal Gram matrices. It also exhibits a precise obstruction to extending the argument from sums of squares to arbitrary pointwise nonnegative virtual characters. Independent review is pending; no historical novelty is claimed.

## 1. The theorem and its limit

Let R(SU(3)) be the integral representation ring, viewed as class functions, and let R_C=R(SU(3)) tensor_Z C. Elements of R_C are finite complex linear combinations of irreducible characters. They are not required to be ordinary characters or integral virtual characters.

**Theorem.** Suppose f belongs to R(SU(3)), its normalized Haar mean is one, and it has a finite Hermitian sum-of-squares representation

    f=sum_l |q_l|^2,   q_l in R_C.                       (1.1)

Then f=|chi_(a,b)|^2 for one irreducible SU(3) character. There is no bound on a,b, the number of summands, or the degrees of the q_l. The q_l may mix different irreducibles with arbitrary complex coefficients.

This is stronger than turn 4's diagonal convex-square theorem: cross products between distinct irreducibles are allowed in (1.1). It is still not the original classification. A virtual character may be pointwise nonnegative on SU(3) without being a Hermitian sum of character-polynomial squares. Section 6 gives an explicit such positive virtual character, of Haar mean 15. Whether the extra integral mean-one condition rules out this obstruction is not proved here.

## 2. Integral character polynomials and concentration at one height

Put u=chi_(1,0)=tr(g), v=chi_(0,1)=conjugate(u). The representation ring is Z[u,v], and for every a,b>=0,

    chi_(a,b)=u^a v^b + terms of total degree <a+b.         (2.1)

For clarity, the all-weight triangular assertion follows inductively from the defining-representation Pieri rule

    chi_(a,b)=u chi_(a-1,b)-chi_(a-2,b+1)-chi_(a-1,b-1),
    a>=1,

where negative indices mean zero, together with conjugation for a=0. Every character on the right has smaller height a+b. Monic triangular elimination proves integral spanning by these characters. Polynomial injectivity can also be seen from the SU(3) trace image containing an open neighborhood of zero in the complex plane: at eigenvalues (1,omega,omega^2), the real trace Jacobian has determinant 3sqrt(3)/2, as computed in turn 3. Thus identities of character polynomials are genuine identities in C[u,v].

Expand each q_l in irreducibles and write (1.1) as

    f=sum_(lambda,mu) M_(lambda,mu) chi_lambda conjugate(chi_mu),

where M is a finite positive semidefinite Hermitian matrix. Schur orthogonality gives

    tr M = integral f = 1.                              (2.2)

Every diagonal entry is nonnegative. Also

    |M_(lambda,mu)|^2<=M_(lambda,lambda)M_(mu,mu),

so zero diagonal entries have zero rows and columns.

Let N be the largest height a+b with a positive diagonal entry. The homogeneous part of f of degree 2N comes only from products of height-N characters. Index those characters by

    phi_a=chi_(a,N-a),   0<=a<=N.

By (2.1), the coefficient of u^N v^N in that highest homogeneous part is exactly the trace of the height-N diagonal block: a product phi_a conjugate(phi_c) has leading monomial

    u^(N+a-c) v^(N-a+c),

which is u^N v^N precisely when a=c. The trace of this block is positive and at most one. Since f belongs to Z[u,v], this coefficient is an integer and therefore equals one. Equation (2.2) forces all other diagonal blocks to be zero, and positive semidefiniteness then forces their rows and columns to be zero. We have proved that the entire Gram matrix is supported at the single height N.

Write the surviving matrix as M_(a,c), 0<=a,c<=N. Its trace is one. For each integer delta define the band sum

    B_delta=sum_(a-c=delta) M_(a,c).

The same leading-monomial formula shows B_delta is an integer, because it is the coefficient of u^(N+delta)v^(N-delta) in f. In particular B_0=1. Furthermore

    p(z)=sum_delta B_delta z^delta

is nonnegative on the unit circle: if M is represented by its Gram vectors, p is the sum of the squared moduli of their ordinary one-variable polynomial combinations. Equivalently it is the quadratic form of M on the vector (1,z,...,z^N), with an immaterial conjugation convention.

A nonnegative integral Laurent polynomial of constant coefficient one equals one. A short proof is to take its largest nonzero positive exponent m: averaging at mth roots of a suitable phase gives |B_m|<=B_0/2=1/2, contradicting nonzero integrality. In the present case all B_delta are real integers and B_-delta=B_delta, so the two phases 1 and -1 suffice, exactly as in turn 3. Consequently

    B_delta=0 for every delta!=0.                       (2.3)

This alone does not force M diagonal. Non-diagonal positive definite matrices can have cancelling band sums; the independent controls include an explicit example. The next step handles those cancellations.

## 3. The cross multiplicity on a stable strip

Let m_k(a,c) be the multiplicity of chi_(k,k) in phi_a conjugate(phi_c), with both phi characters at height N. Suppose

    1<=k<=floor(N/2),
    k-1<=a,c<=N-k+1.                                   (3.1)

Then

    m_k(a,a)=k+1-1_(min(a,N-a)=k-1),                     (3.2)

while for a!=c,

    m_k(a,c)=0                       if a-c is not divisible by 3,
    m_k(a,c)=max(0,k-2|h|+1)          if a-c=3h.          (3.3)

The essential fact is that every off-diagonal coefficient depends only on the difference a-c, not on the location inside the strip.

Equation (3.2) is the diagonal multiplicity proved in turn 4:

    m_k(a,a)=min(a,N-a,k,N-k)+1.

The central character of phi_a conjugate(phi_c) is omega^(2(a-c)), whereas chi_(k,k) has trivial central character. This gives the first zero in (3.3).

It remains to prove the second formula. Because chi_(k,k) is self-conjugate, interchanging a and c leaves the multiplicity unchanged. Assume therefore a-c=3h with h>=1. Put b=N-a, so c=a-3h. The GL(3) partitions for the two factors are

    lambda=(N,b,0),  mu=(N,c,0).

Their total degree is 3N-3h. The only polynomial GL(3) constituent restricting to chi_(k,k) is

    nu=(N+k-h,N-h,N-k-h).                               (3.4)

If h>k, nu does not contain lambda in its first row, so the LR coefficient is zero, consistent with (3.3). Assume 1<=h<=k. The strip condition implies c>=k-1 and b>=k-1, which also ensures the third part in (3.4) is nonnegative.

The skew shape nu/lambda has row lengths k-h, a-h, N-k-h. Content mu requires N 1s and c 2s. Row 1 is all 1s by the ballot condition. Let t be the number of 2s in row 2. Its 1s number a-h-t, and row 3 has

    b-k+2h+t 1s and c-t 2s.

Rows 1 and 2 have no column overlap, since row 2 ends at column N-h. Rows 2 and 3 overlap in exactly

    c+2h-k >= 2h-1 > 0

columns. Column strictness forces row 3's 1s to end at or before column b, hence t<=k-2h. This stronger bound also forces row 2's overlapping entries to be 1s. The ballot inequalities from rows 2 and 3 are t<=k-h and t<=k+h, both weaker.

If k<2h, there is no allowed t. If k>=2h, every integer

    0<=t<=k-2h

is allowed: c,b>=k-1 make all row counts nonnegative, the column inequalities hold, and the ballot inequalities hold. Each t fixes the tableau uniquely. The LR multiplicity is thus max(0,k-2h+1), proving (3.3). This is a full all-weight tableau argument; the finite computations below merely check it on examples.

## 4. Boundary-layer elimination of the Gram matrix

Initially M is supported on indices 0,...,N. Suppose inductively it is supported on

    k-1,...,N-k+1,

for some 1<=k<=floor(N/2). Let w be the sum of its diagonal entries on the two boundary indices k-1 and N-k+1. They are distinct in this range. Thus 0<=w<=1.

By (3.2), the diagonal contribution to the coefficient of chi_(k,k) in f is k+1-w. By (3.3), each off-diagonal contribution is a constant multiple of a band sum B_delta. All those sums are zero by (2.3). Therefore

    <f,chi_(k,k)>=k+1-w.                                (4.1)

The left side is an integer because f is a virtual character. Thus w is an integer in [0,1].

If w=0, both boundary diagonal entries vanish, so their rows and columns vanish. M is supported on k,...,N-k, establishing the next induction step.

If w=1, all other diagonal entries vanish, so M is supported on just the two boundary indices. Their off-diagonal entry is now the only possible entry in its nonzero-distance band, and hence is zero by (2.3). The two corresponding irreducibles are conjugates, so their square functions are equal. Their diagonal coefficients sum to one, and f is that square.

If the zero-boundary case continues through the last step, the remaining support is one middle index when N is even, or two conjugate middle indices when N is odd. The same band-sum argument kills the possible off-diagonal entry, and f is again one square. For N=0 or 1 the support already has this form before any induction. This completes the theorem.

The argument does not assert that the original Gram matrix must have rank one: distinct conjugate irreducibles can occur as two diagonal entries and still give the same square function. That harmless ambiguity is retained.

## 5. Exact controls, including genuine non-diagonal cancellation

Run `python3 verify_turn5.py` beside `verify_turn4.py`, or specify `--prior-dir` pointing to the directory containing that prior checker. It reruns turn 4's 2,265 controls, computes every ordered cross tensor product at each height 1,...,16, and compares the relevant diagonal coefficients with (3.2)-(3.3) wherever the strip hypotheses hold. It also verifies the boundary-mass matrix identity behind (4.1).

A separate control uses

    M = [ 1/3   1/10    0   ]
        [ 1/10  1/3   -1/10]
        [  0   -1/10   1/3 ]

on height two. Its Sylvester minors are positive, its trace is one, and its nonzero-distance band sums vanish. It is nevertheless not diagonal. Its resulting character has coefficient 4/3 at chi_(1,1), showing why the boundary integrality step is needed and why (2.3) alone is not enough.

The executable also verifies every displayed polynomial identity for the explicit non-SOS obstruction in the next section. These finite exact checks support, but do not replace, the unbounded Gram and LR proof.

## 6. A sharp obstruction to assuming sum-of-squares membership

Let x=uv, y=u^3+v^3, and define the SU(3) Weyl discriminant

    D(u,v)=27-18x+4y-x^2.

For actual eigenvalues z_1,z_2,z_3 of product one, its value is

    D=product_(i<j) |z_i-z_j|^2>=0.

The exact irreducible expansion is

    D=15-6 chi_(1,1)+3(chi_(3,0)+chi_(0,3))-chi_(2,2).

Thus D is a pointwise nonnegative integral virtual character, but its Haar mean is 15, not one. At the formal real trace value u=v=4, which is outside the SU(3) trace region,

    D(4,4)=-5.

Every Hermitian sum of squares of character polynomials is nonnegative at every formal pair (u,conjugate(u)) in the entire complex plane. Since polynomial identities on the SU(3) trace region extend to polynomial identities, D cannot have such a sum-of-squares representation. In real-trace notation the same obstruction is D(t,t)=(3-t)^3(t+1), negative for t>3.

This is not a counterexample to the source problem: the Haar normalization fails by a factor of 15, and dividing by 15 destroys integral virtual-character coefficients. It is a concrete warning that pointwise nonnegativity alone does not imply the SOS hypothesis. An argument replacing that missing step by a general multivariable Fejer–Riesz assertion, or allowing a nonconstant denominator without controlling the Haar normalization, would be invalid.

## 7. Final disposition and exact remaining gap

The complete original problem asks for every pointwise nonnegative integral virtual character of Haar mean one on every connected simply connected compact Lie group. It remains unresolved after the five allowed substantive author turns.

The strongest SU(3) reduction obtained here is: **any counterexample on SU(3) must lie outside the Hermitian polynomial sum-of-squares cone, even when the square roots may be arbitrary complex character combinations of unbounded degree.** A proof that the integral mean-one condition forces that cone membership would settle SU(3) by this theorem, but no such proof is supplied. The discriminant example shows that positivity without the normalization cannot provide it. Other higher-rank simple groups and mixed products also remain open in this attempt.

The preserved scoped outcomes are:

1. The all-r product classification for SU(2)^r, extending the credited rank-one mechanism.
2. The exact finite center-neutral SU(3) span classification.
3. The full SU(3) support a+b<=4 classification, without a center assumption.
4. The all-weight affine-single-irrep and integral convex-square classifications for SU(3).
5. The present all-weight Hermitian-SOS classification for SU(3), with non-diagonal Gram matrices allowed.

These claims are pending separate independent review. They are not a complete solution and do not establish historical novelty. No sixth substantive search turn is authorized by this five-turn attempt. A review may verify or correct the frozen results, but must not be relabeled as extra proof search on the unresolved original.

Final original status: **exhausted, unresolved, 5/5 substantive author turns**. Repository-required completion estimate remains 30%, subjective and uncalibrated, not a correctness probability.

## Sources

The exact target and original field/group hypotheses remain those in SOURCE_GATE.md and Serre's original/final papers. Serre's final Problem 4.6 is at https://ems.press/content/serial-article-files/50890. The integral Laurent extremality argument is credited to its section 5.

The Weyl and Littlewood–Richardson rules are classical. The LR tableau convention and primary references are given in TURN_4.md; a directly accessible proof exposition is Prasad, Theorems 19.2 and 19.5, https://arxiv.org/pdf/1802.06073. No claim that the specialized multiplicity formulas are historically new is made. The new assertion in this checkpoint is the precise scoped rigidity deduction and its explicit remaining positivity gap.
