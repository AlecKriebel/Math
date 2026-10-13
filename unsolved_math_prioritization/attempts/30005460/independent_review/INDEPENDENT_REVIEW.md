# Independent review: 30005460

## Verdict

**PASS_COMPLETE_GENERAL_NONCONVEXITY_SOURCE_TARGET. No mandatory correction.**

The frozen second-turn candidate proves that the set of real nonnegative homogeneous sextics whose **cube** is SOS need not be convex. It gives one explicit finite ambient dimension, `n=3*10^62`, and a finite average of `10^62` members that is outside the set. This is a complete negative answer to the source's general convexity question. It is not a classification of all parameter triples or a resolution of the separately fixed ternary case. Closedness remains true.

The stronger existential statement for every odd exponent `q>=3` also passes. Its dimension depends on q and is not asserted to equal the explicit cubic bound. The first-turn circuit and formal-preordering partials pass with their stated limitations.

This is an uninvolved mathematical and source audit. I did not contribute to the author proof or construct its moment functional. No novelty, optimality, or practical small-dimensional bound is certified. The credited seed identity and classical separation/tensor methods must retain their attribution. Publication remains subject to the parent gate.

## Binding version

- Author `PROOF.md`: SHA256 `ca6f6d3c23ee412ad5f01ca0f8fd473516e35f76c778488ad045e10df6718be5`
- Author `FROZEN_MANIFEST.json`: SHA256 `27e51197de62357686c71775915d3ebae9d49dfed4d0d68dfd3fe2e1ef076eaf`, binding18 files
- Author `TENSOR_MOMENT_CERTIFICATE.json`: SHA256 `6fa52a986409a15d6c6daf0673c7221a3c02afb621e6351f7d5cf8e8c2b09b84`

All18 author files and all3 pinned full PDFs match. Both author checkers were run in a separate copy and replayed their saved receipts byte-for-byte. Frozen author mathematics was not edited.

## 1. Source correspondence

I read the original Reznick contribution in OWR14/2023, printed778–780, and visually checked the definition and question on779. The parameter n is unrestricted; the exponent is fixed before testing addition. Thus a single finite n and fixed q=3 counterexample suffices to reject the general assertion. Nothing requires the counterexample to be ternary or computationally small.

The final2026 Blekherman–Kozhasov–Reznick paper was checked directly, including its definitions, Theorems5.1–5.3 and §6. Its convex union over odd exponents is a different set. The seed cube identity on printed24 was visually compared term by term and re-expanded independently. The article still poses fixed-exponent convexity separately. The proof does not infer current worldwide priority from that fact or from a bounded literature search.

## 2. Complete local moment matrix

The functional is specified consistently on all monomials of total degree at most18. Moments with any odd coordinate vanish. The ten even degree-six indices exhaust that degree's possibilities; other even degrees use the stated Gaussian moments and scales. The constant is1. Hence every entry indexed by monomials of degree at most9 is a uniquely specified moment, including all cross-degree entries.

I independently reconstructed the entire220-dimensional polynomial moment matrix from the written table, using standard-library rational/integer arithmetic and a different monomial order. Multiplication by1024 makes it integral without changing positivity. Its eight coordinate-parity blocks have dimensions35 or20. A separately authored fraction-free Bareiss calculation verifies **every one of their220 leading principal minors is strictly positive**, with exact division at each elimination step. The actual positive integers are preserved in `INDEPENDENT_CERTIFICATE.json`. All cross-parity entries are independently zero. Sylvester's criterion proves positive definiteness of the full moment matrix, not merely its homogeneous degree-nine corner.

The author's alternative Schur trace proof is valid as well. At extension order r, each old/new cross entry has degree below2r; if its total degree is2r-1, coordinate parity forces it to vanish. Thus choosing the new scale changes only the new/new Gaussian block. Gaussian Gram matrices of distinct monomials are positive definite. Since `C=B^T A^-1 B` is positive semidefinite, the largest eigenvalue of `G^-1/2 C G^-1/2` is at most its trace, and the exact strict trace bound is sufficient. Every inverse identity and bound was replayed exactly. No arbitrary Hankel completion or numerical eigenvalue assertion is hidden here.

## 3. Seed and scalar moments

For `p=x^4y^2+x^2y^4+z^6-x^2y^2z^2`, AM–GM gives the sum of the first three terms at least `3x^2y^2z^2`, so p is nonnegative for all real coordinates. The displayed weighted cube identity has16 square summands, positive coefficients at the chosen parameter, and homogeneous degree-nine summands. Independent dictionary polynomial arithmetic checked all1330 monomials of degree at most18 against the cube. The source identity is correctly specialized.

The reconstructed functional gives exactly

`L(p)=-1`, `L(p^2)=11292*10^53`, `L(p^3)=35039520*10^116`.

Its negative value on p also certifies that p is not SOS. In particular this functional is not an ordinary probability distribution or a representing measure. Neither the author argument nor this verdict needs it to be one.

## 4. Arbitrary finite tensor power and degree restriction

Fix any finite number s of disjoint triples. The product functional is defined on monomials of blockwise degree at most18 by multiplying the one-block moments, and extended linearly. Distinct global monomials have unique block decompositions, so this is well-defined. Its bilinear matrix on the tensor product of the one-block degree-at-most-nine polynomial spaces is the s-fold Kronecker product of the local positive matrix. A Kronecker product of finitely many positive semidefinite matrices is positive semidefinite; this follows, for example, by taking a real Gram factor in each finite factor and tensoring those factors.

Every global monomial of **total** degree at most9 lies in that tensor-product basis, since its degree in each block is at most9. The total-degree matrix is a principal submatrix. For a polynomial H of total degree at most9, evaluation of H² by the product functional agrees with its quadratic form in this principal matrix: the degree in each block is at most18, and each cross product uses exactly the same moment. Therefore the functional is nonnegative on all such squares and their finite sums.

This is an argument for every finite s, including `10^62`; it does not require constructing a tensor of that size. As a supplementary index check, I independently built a genuine84-dimensional total-degree-at-most-three matrix in two blocks directly from six-variable monomial sums. Every leading minor is positive. This finite control does not substitute for the general tensor argument.

A polynomial SOS of total degree18 cannot involve a square of degree greater than18: the highest-degree homogeneous pieces of its square summands have nonnegative squares and cannot cancel identically. Thus the degree-nine square test excludes every possible SOS representation of the displayed cube, not just representations using a chosen sparse support.

## 5. Exact large-dimensional contradiction

The labeled-factor expansion of `(p_1+...+p_N)^3` has N same-block terms, `3N(N-1)` terms of multiplicity type(2,1), and `N(N-1)(N-2)` all-distinct terms. It yields the author's exact expression. Since `a1=-1` and `a2>=1`, subtracting that expression from its claimed upper bound gives exactly

`3N(N-1)(a2-1)>=0`.

For `N=10^62`, `a3=35039520*10^116 < 10^124-1=N^2-1`. The upper bound, and hence the actual tensor value, is strictly negative. These are integer inequalities, not floating estimates.

All p_i live in the same real homogeneous degree-six space in3N variables and have the same fixed cube certificate. Their average has positive scalar factor1/N, is nonnegative, and has a non-SOS cube. A convex set contains any finite convex combination of its elements, by induction, regardless of the finite number of terms. Thus this finite average genuinely disproves convexity. Alternatively, the least failing prefix supplies two members whose sum is outside, without assuming any untested later prefix is inside. No two-input explicit Gram certificate for an arbitrarily chosen prefix is claimed.

## 6. General odd exponent

For any odd q>=3, the seed has `p^q=p^3*(p^((q-3)/2))^2` SOS and remains non-SOS. In the finite-dimensional polynomial space through degree2d, `d=qm/2`, the SOS cone is closed: choose a monomial vector v and positive-definite Gaussian Gram matrix G. For a coefficient-convergent sequence `v^T Q_j v`, the integrals `tr(Q_j G)` are bounded. Positivity gives bounded traces and entries of Q_j, hence a convergent Gram subsequence. The highest-degree argument excludes p from this cone even when d exceeds its original half-degree.

Finite-dimensional separation therefore gives a functional negative on p and nonnegative on all required squares. Adding a sufficiently small positive Gaussian functional preserves the strict negative value and makes the moment matrix positive definite; its constant value is then positive and can be normalized to1. This uses only a finite truncated space for each q, not a compatible infinite sequence of moments.

The partition expansion in the number s of blocks has degree q. Only the all-singleton partition contributes to its leading coefficient, `L(p)^q<0`. It is consequently negative for some finite sufficiently large integer s. The tensor reasoning above then proves nonconvexity for that q. No uniform bound in q, or smallest possible dimension, follows or is claimed.

## 7. Historical turn1 partials

The fixed-circuit theorem passes. Equal positive total degree converts affine independence of the outer exponents into linear independence, justifying the logarithmic positive-diagonal normalization. Absorption by ordinary SOS and positive scaling give the normalized parameter interval; the sign symmetry when beta has an odd coordinate is valid. Exposing an outer vertex rules out a negative outer coefficient. Perturbing zero outer coefficients by positive monomial squares and then taking limits gives the boundary restrictions, whose surviving forms are ordinary SOS. Concavity/homogeneity of the weighted geometric mean supplies the stated convexity.

The formal-preordering exponent barrier also passes. On the positive quadrant all four monomial weights are positive. Thus highest and lowest homogeneous weighted-square pieces cannot cancel, forcing every surviving term to have the target degree. For odd target degree, only the singly weighted terms remain. The missing binomial monomial below q+t-1 gives the stated ideal obstruction. At and above that exponent, the credited even truncated-binomial SOS multipliers and an even power of u+v give membership. These claims concern the formal two-variable certificate class; the later tensor proof is what establishes actual nonconvexity.

## 8. Verification summary and retained limits

-18 author hashes and3 full PDF hashes match
- Both author receipts replay byte-identically
-210,525 separately authored exact assertions pass, including220 full local leading minors and84 coupled two-block leading minors
- No floating-point computation, numerical SDP inference, external executable, or astronomical matrix enumeration
- No mandatory correction to the frozen proof, source reading, or certificate

Preserve the enormous finite dimension, the fixed exponent, real polynomial SOS meaning, attribution, and all small-dimension/parameter limitations. The result does not contradict the convexity of the union over exponents and does not assert that the displayed sum is stubborn.
