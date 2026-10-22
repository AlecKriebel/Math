# Turn 3: exact detection of all entangled Schmidt-correlated mixed states

**3/5 substantive author turns.** For the standard multipartite Schmidt-correlated family, both source fixed testers exactly detect every entangled state, with an explicit relation between their full complex projective norms for every number of parties, including odd numbers. The state family and its separability/partial-transpose properties are classical and credited to Zhao–Fei–Wang, *Entanglement of Multipartite Schmidt-correlated States* (2008). Their Proposition2 already gives the sum of absolute coefficients for a grouped realignment norm. The full m-factor calculation below recovers that known value and derives the corresponding SIC formula. We give the short required arguments as well. No novelty claim is made.

## 1. State family and theorem

Fix m>=2 and an integer r>=2. In each local Hilbert space choose an orthonormal family |1>_j,...,|r>_j. The local dimensions d_j may differ and may be larger than r. If A=(a_ik) is an r-by-r positive semidefinite matrix with trace1, define

    rho_A=sum_(i,k=1)^r a_ik
            |i>_1...|i>_m <k|_1...<k|_m,
    C(A)=sum_(i!=k) |a_ik|.                             (1)

This is a density matrix because the map |i> -> |i>_1...|i>_m is an isometry. Let r_m and s_m be the output complex Hilbert projective norms for the local realignment maps and for the local canonical SIC-Gram maps L_(d_j), respectively, as defined in turn2. In dimensions where actual rank-one SICs exist, s_m is exactly their tester value.

**Theorem.** For every such A and every m>=2,

    r_m(rho_A)=1+C(A),
    s_m(rho_A)=1+2^(-m/2) C(A).                         (2)

Thus rho_A is fully separable if and only if either tester value is1; otherwise both exceed1. For m>=3, within this family non-diagonal A even implies genuine multipartite entanglement, by the standard support argument in Section5. These are statements about this specific mixed family, not arbitrary states.

Local changes of the chosen orthonormal families do not affect (2). For realignment this is Hilbert–Schmidt unitary invariance. For the SIC-Gram map, the inner product formula (2) of turn2 is also unitarily invariant, so all the relevant image Gram matrices and projective norms are preserved.

## 2. The local image geometry

Write E_ik^(j)=|i>_j<k|. In the realignment output these form an orthonormal family. For the SIC-Gram output put

    v_i^(j)=L_(d_j)(E_ii^(j)),
    u_ik^(j)=sqrt(2)L_(d_j)(E_ik^(j)),  i!=k.

The Gram identity from turn2 gives

    <v_i^(j),v_k^(j)>=(1+delta_(i,k))/2,
    <u_ik^(j),u_ab^(j)>=delta_(i,a)delta_(k,b),
    <v_i^(j),u_ab^(j)>=0 for a!=b.                      (3)

In particular every v_i^(j) has norm1. These identities depend on r only through the number of vectors, and do not depend on the ambient dimensions d_j. The Gram matrix of the diagonal vectors is real and positive definite. Local isometries therefore identify their spans with one common real-coordinate configuration v_1,...,v_r in a complex Hilbert space D. Appending orthogonal output directions has no effect on a projective norm: inclusion is contractive and the orthogonal projection back is also contractive, so the two inequalities force equality.

Let v_bar=r^(-1)sum_i v_i. Then

    c²=||v_bar||²=(r+1)/(2r),
    e_0=v_bar/c,
    <e_0,v_i>=c,
    v_i=c e_0+w_i,  ||w_i||²=1−c².                     (4)

All these vectors have real coordinates in a common orthonormal basis, and w_i is orthogonal to e_0. Note that 1/2<c²<=3/4, so the parameter lies in the range used below.

The orthogonal-block lemma of turn2 separates the common diagonal span D from each one-dimensional off-diagonal span. It gives

    s_m(rho_A)=||sum_i a_ii v_i^tensor m||_pi
                +2^(-m/2)sum_(i!=k)|a_ik|.              (5)

All possible complex phases of a_ik are allowed; each off-diagonal component is a separate simple-tensor block. The only missing ingredient is that the diagonal norm in (5) is1, also for odd m.

## 3. An explicit complex trilinear certificate

We prove a norm-one certificate for any real unit vectors having the common coordinate c in (4). Put

    h=1/(2c),    lambda=(3c²−1)/(2c³).

For x=x_0 e_0+x_perp, and similarly y,z, let

    T_c(x,y,z)=lambda x_0 y_0 z_0
       +h[x_0 B(y_perp,z_perp)+y_0 B(x_perp,z_perp)
                                      +z_0 B(x_perp,y_perp)],                (6)

where B(u,v)=sum_l u_l v_l is the complex bilinear coordinate pairing in the fixed real orthonormal basis. This is a complex trilinear functional.

For c in [1/sqrt(2),1], it has injective norm at most1. Here is a direct proof, avoiding a real-versus-complex symmetric-tensor theorem. For unit x,y,z use |B(u,v)|<=||u||||v||, put w=|z_0|, and note ||z_perp||=sqrt(1−w²). The absolute value of (6) is at most

    X^T M(w) Y,
    X=(|x_0|,||x_perp||),   Y=(|y_0|,||y_perp||),
    M(w)=[[lambda w, h sqrt(1−w²)],
          [h sqrt(1−w²), h w]].                         (7)

Both X and Y have Euclidean norm1. The constants satisfy 0<=lambda<=1 and 0<h<=1. The first claim follows from 3c²−1>=0 and

    1−lambda=(c−1)²(2c+1)/(2c³)>=0.

The two diagonal entries of I−M(w) are therefore nonnegative, and its determinant is exactly

    det(I−M(w))=(4c²−1)/(4c^4) · (w−c)² >=0.            (8)

Thus I−M(w) is positive semidefinite. The real symmetric matrix M(w) has nonnegative trace, so the absolute value of its smaller eigenvalue is no larger than its larger eigenvalue. Its operator norm is consequently at most1. Equations (7)-(8) prove |T_c(x,y,z)|<=1 for arbitrary complex unit vectors.

For every real unit v=c e_0+w with ||w||²=1−c²,

    T_c(v,v,v)=lambda c³+3hc(1−c²)
              =(3c²−1)/2+3(1−c²)/2=1.                (9)

Hence the certificate actually has norm1 and attains it simultaneously at all v_i in (4).

## 4. Completing the projective-norm calculation

Since a_ii>=0 and sum_i a_ii=1, the displayed decomposition of the diagonal tensor gives an upper bound1.

For even m, the paired bilinear certificate of turn2 has norm1 and evaluates every v_i^tensor m to1. For odd m>=3, use T_c on the first three factors and paired copies of B on the remaining even number of factors. The product is a complex m-linear functional of norm at most1, and (9) plus the reality and unit norm of v_i make its value1 on every v_i^tensor m. It therefore evaluates the diagonal tensor to1. In both cases its projective norm is exactly1.

Substituting in (5) proves the SIC-Gram formula in (2). The realignment formula follows even more directly: the vectors E_ik^(j) are orthonormal in each factor, so the same orthogonal-block argument yields sum_(i,k)|a_ik|=1+C(A).

No positivity or reality of off-diagonal a_ik was assumed. No optimization over a guessed real tensor decomposition was used. The lower bounds come from explicitly bounded complex multilinear functionals.

## 5. Separability and genuine multipartite entanglement in this family

If A is diagonal, (1) is a convex combination of pure product states. If a_ik!=0 for i!=k, partial transposition on the first party has on the span of

    |k>_1 |i>_2...|i>_m,   |i>_1 |k>_2...|k>_m

the block [[0,a_ik],[conjugate(a_ik),0]], up to the harmless ordering of the two basis vectors. It has eigenvalues plus/minus |a_ik|, so the partial transpose is not positive. The partial transpose of every separable state is positive, proving entanglement. The same argument works across every nontrivial bipartition.

The stronger genuine-entanglement conclusion for m>=3 uses support, rather than the invalid general implication that negativity across every cut alone implies genuine multipartite entanglement. Let V be the span of the r vectors |i>_1...|i>_m. Any pure vector occurring with positive weight in a convex decomposition of rho_A lies in V: taking the expectation of the projection onto V-perp gives a sum of nonnegative numbers equal to zero. A vector sum_i z_i |i>_1...|i>_m in V is a product across any fixed nontrivial bipartition only if at most one z_i is nonzero, since the displayed expansion is a Schmidt decomposition across that cut. Therefore every biseparable pure vector in V is a single correlated basis vector. A biseparable mixed state supported in V must be diagonal in those vectors. Consequently non-diagonal A in this family is genuinely multipartite entangled.

These standard Schmidt-correlated separability facts are credited to the earlier literature; they are included to keep the norm-to-entanglement implication self-contained. The additional fixed-test norm computation supplies an explicit complete detection result on this family.

## Scope after turn3

The central all-tester question has a reviewed negative answer. The two fixed tests are incomparable on general multipartite mixed states, while both are exact detectors on the Schmidt-correlated family with the quantitative relation (2). None of these statements classifies all mixed-state detection regions. General SIC-existence qualifications remain as in turn2; the canonical Gram-map identity itself holds in all finite dimensions. The new finite controls verify the trilinear determinant and coefficient identities and support/partial-transpose certificates, not the universal norm conclusion by sampling.
