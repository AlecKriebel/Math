# Independent audit of orbit closure incidence formulas

## Verdict and scope

**PASS for the stated partial results. Retain status UNSOLVED and the five documented approaches.** No blocking mathematical defect was found in the frozen packet. The local cancellation, incidence resolutions, smallness and semismallness criteria, relevant-path description, decomposition relation, worked example, and canonical-basis normalization withstand the checks below. They do not supply the all-orbits Catalan construction sought in the original report.

This audit is bound to problem 30006272, OWR-14299283-013, rank 554, and to the frozen manifest with SHA-256:

    76020afe8d46058f7f53756aa560521d9f4d8083f09df5b74e9e8de28573d1b7

All seven file lengths and hashes listed in that manifest were checked before review and again after the audit. The frozen packet was not edited. All three primary reading-copy PDF hashes match `SOURCE_HASHES.json`. The supplied checker was replayed, and a separate implementation independently reconstructed the finite dimension and path checks without importing candidate code.

The assessment concerns the mathematics and the accuracy of its stated scope. It does not establish novelty, exhaust the literature, independently repeat remote repository-history searches, or turn numerical agreement into a proof of intersection cohomology.

## Primary question and proof sources

The Reineke contribution, joint with Xin Fang, on printed pages 1315–1316 of [Oberwolfach Report 25/2025](https://ems.press/content/serial-article-files/51851) was read in full, with both pages visually inspected. The final question concerns the calligraphic canonical-basis elements indexed by complex orbits. It is neither an Ekedahl–Oort question nor a dual-canonical-basis question. No particular Catalan indexing set or weights are specified there. The packet correctly repairs the catalogue label and does not pretend that disproving one guessed formula disproves this question.

All nine pages of [Fang–Reineke, arXiv:2502.07688v1](https://arxiv.org/pdf/2502.07688v1) were inspected, including the full arguments of Theorems 4.1 and 5.1. The construction in 4.1 assumes sparse homology support, so adjacent positive homology dimensions are excluded. Theorem 5.1 has the same hypothesis and computes the irreducible components. Its proof uses the canonical/PBW comparison, the coefficient expansion, the endomorphism-dimension difference, and conversion of quantum binomials to ordinary Gaussian polynomials. Nothing in these proofs gives the stated all-orbits extension automatically.

The report's vertex-dimension display uses an inconsistent rank index. The packet's convention, d_i=h_i+r_{i-1}+r_i with r_0=r_n=0, is the correct one and agrees with preprint §2. It was used consistently throughout this audit.

The small and semismall inputs were checked against [de Cataldo–Migliorini, arXiv:0712.0349](https://arxiv.org/pdf/0712.0349), §4.2 through §4.2.1, printed preprint pages 55–59. In particular, the component-monodromy local systems and the nondegeneracy that ensures every relevant support occurs are genuine parts of the decomposition theorem, not additional conjectures in the packet.

## Orbit dimensions and transverse cancellation

For fixed dimensions d and ranks s, choose the usual complex normal form with incoming, homology, and outgoing blocks at every vertex. The independent checker calculates the dimension of the linear solution space

    f_i X_i = X_{i+1} f_i

for all endomorphism matrices X_i. In this normal form, each scalar equation identifies two variables or sets one variable to zero. Counting the resulting free classes gives dim End directly, without the interval-Hom formula used in the candidate. Subtraction from sum d_i^2 gives every orbit dimension. The results agree with equation (1) on all 18,525 tested drops.

The interval-Hom argument is also correct: with arrows oriented left to right, Hom(U_[a,b],U_[c,d]) has dimension one exactly for c<=a<=d<=b. In particular, reversing the inequality would produce an incorrect endomorphism count, but the packet has the correct orientation.

The Schur-complement cancellation is an actual algebraic local product. Write A=[[a,b],[c,d]] with a invertible, put S=d-ca^{-1}b, and use the packet's L and R so that LAR=diag(I,S). The adjacent maps must be changed to R^{-1}f_previous and f_next L^{-1}. Their affected rows and columns then vanish, and their remaining equations are exactly those of the residual complex. Reconstruction is algebraic from a,b,c,S and the residual maps, with only det(a) inverted. Thus the free factor is GL_s times an affine space, not a merely bijective parameterization.

This also survives a scheme-level challenge. After the basis changes, the composition equations eliminate the forced adjacent blocks, and the localized determinantal ideal for A becomes the lower-rank determinantal ideal for S. Multiplication by invertible matrices preserves adjacent determinantal ideals. At minimum, this proves the asserted product of reduced varieties, which is all that the IC claim needs. No claim that every naive global defining ideal is reduced is needed or inferred. Possible nilpotent structure would not change the underlying complex analytic IC calculation.

Pivots chosen from the normal form of the specified rank stratum can be canceled successively on open charts containing the point. The residual dimensions are h_i+k_{i-1}+k_i and the residual point is zero. Smooth-factor invariance with the degree-zero normalization therefore gives equation (2), with no extra cohomological shift.

## Incidence geometry and exact smallness

For the image incidence map, the Grassmannian base chooses U_i of dimension r_{i-1}. The fiber over that base is the vector space of maps V_i/U_i to U_{i+1}; hence its total space is smooth and irreducible. The incidence conditions define a closed subset of X times the projective base, so the forgetful morphism is projective. This argument does not require the total space itself to be projective.

At a rank drop k, an intermediate U_i exists because

    dim(Ker f_i / Im f_{i-1}) = h_i+k_{i-1}+k_i >= k_{i-1}.

The choices form Gr(k_{i-1},h_i+k_{i-1}+k_i), independently at the vertices. Over the open orbit, U_i is the actual image and varies algebraically, giving an isomorphism there. Thus surjectivity, birationality, and the claimed fiber dimensions are justified. Rank orbits are smooth homogeneous strata, and the equivariant fiber family is locally trivial over each orbit.

The numerical defect is correctly

    c_h(k)-2 f_im(k) = Q(k)-sum (h_{i+1}-h_i)k_i.

For nonzero k, Q(k)=one half of sum (k_i-k_{i-1})^2 is positive. Decreasing homology along every positive-rank edge therefore implies smallness. Conversely, a positive rise on an active edge gives k=e_i with defect 1-(h_{i+1}-h_i)<=0; its fiber has positive dimension. This proves necessity as well as sufficiency. Zero-rank edges impose no extraneous inequality. The dual kernel result has the reversed inequalities, as stated.

The small-resolution identification and proper base change consequently give equations (5) and (6). In two vertices one of the two chambers always applies, yielding equation (7). Isolated active edges genuinely separate into product factors, and the strict defects add. These are valid restricted formulas for all the indicated stalks.

The rank-one 2 by 2 determinantal cone has origin polynomial 1+q, while literal insertion of h=(1,1) into the sparse-support expression gives 1. This is a valid objection to that extrapolation. It has no force against an unspecified, different Catalan construction, as the packet already emphasizes.

## Semismallness and relevant supports

Taking k to be an active interval indicator proves the necessity of the rise bound in equation (8). Conversely, write k as the sum of all its superlevel-interval indicators. The linear rise term is the sum of interval rises, each at most one; the number of intervals is half the total variation of k. The inequality x^2>=|x| for integer x bounds that count by Q(k). This proves sufficiency with no assumption on the magnitude of r.

Equality forces both inequalities to be equalities. Thus every step has magnitude at most one and every superlevel interval has rise exactly one. There is no additional unaccounted equality case. Nonnegative, bounded, zero-endpoint paths with these step conditions are correctly described as restricted Motzkin paths. The packet does not equate this particular path family with the unspecified Catalan family of the primary question.

Every fiber is a product of Grassmannians and has exactly one top-dimensional irreducible component. The relevant local system is the permutation local system on those component classes. It is therefore constant of rank one. This argument does not require a claim that all rank orbits are simply connected. There is also no hidden orientation-sign local system: the semismall theorem uses the canonical complex component classes.

Because the map is projective with smooth source, nondegeneracy in the semismall decomposition theorem supplies one summand for every relevant orbit closure. Irreducibility of a fiber alone would not replace that theorem; here the theorem is expressly invoked and its hypotheses hold.

Let D=dim X and let Z be the closure of a relevant stratum of codimension c. In perverse normalization its summand is IC_Z^0[D-c]. Removing the source normalization [D] makes this IC_Z^0[-c]. Thus its stalk polynomial contributes q^(c/2), not q^(-c/2), and c is even by relevance. The support condition is t<=k, while the support's rank and homology labels are r-t and h[t]. These checks establish equation (9) with exactly the displayed shifts and no multiplicity factor.

Equation (9) is not a closed recurrence within the same semismall chamber. The exhibited r=(2,2,2), h=(0,1,0,1), t=(1,1,1) has a relevant support with h[t]=(1,3,2,2), which violates the first-edge rise bound. This warning is correct and necessary.

## Complete non-sparse example and canonical normalization

For r=(1,1), h=(1,2,1), the variety has dimension 9. The image map has precisely two relevant strata, t=(0,0) and t=(1,0). The latter has codimension 4, and its support Z has dimension 5 and labels r'=(0,1), h'=(2,3,1). It is the rank-at-most-one 2 by 4 matrix variety with the first map fixed to zero. There are no additional relevant point or one-edge supports.

The unshifted decomposition is therefore

    R pi_im,* Q = IC_X^0 direct_sum IC_Z^0[-4].

At the origin the total fiber polynomial is

    (1+q+q^2+q^3)(1+q) = 1+2q+2q^2+2q^3+q^4.

The supported IC contribution is q^2(1+q). Subtraction gives exactly

    1+2q+q^2+q^3+q^4.

At k=(1,0), the fiber polynomial 1+q+q^2 loses the contribution q^2; at k=(0,1), no Z contribution occurs and the fiber polynomial is 1+q. At the open orbit the polynomial is 1. The dual kernel resolution independently gives the same four results, exchanging the two one-edge supports. Lack of palindromicity at the origin is not an error: this is a local IC stalk, not the cohomology polynomial of a smooth projective variety.

Fang–Reineke §3, equation (1), identifies the coefficient as v^(-c_h(k)) times the stalk polynomial at q=v^2. Thus the three non-leading coefficients in this example are

    v^(-4)+v^(-2),
    v^(-4)+v^(-2),
    v^(-9)+2v^(-7)+v^(-5)+v^(-3)+v^(-1).

All have strictly negative powers, and the leading coefficient is one. Equation (11) has the correct sign, factor of two, PBW order convention, and canonical-basis interpretation. Strict negativity alone is not a proof of bar invariance, but here the geometric comparison provides the canonical element; the packet does not use negativity as a substitute for that comparison.

## Failed general extensions and remaining task

For h=(1,3,1), the image and kernel maps fail semismallness at opposite one-edge drops, with codimension 5 and fiber dimension 3. The full-flag fiber at k=(1,0) has dimension 4. Formula (12) follows from the flag dimensions a=k_{i-1}, b=h_i+k_{i-1}, N=h_i+k_{i-1}+k_i:

    dim Flag(a,b;N) = a(N-a)+(b-a)(N-b)
                   = h_i(k_{i-1}+k_i)+k_{i-1}k_i.

These failures are real but concern only the three named morphisms. They do not exclude a different resolution or a combinatorial formula. The packet's unsolved conclusion is therefore necessary.

The five approaches are substantive mathematical directions within one pass: determinantal/extrapolation tests, local cancellation, global small resolutions, semismall/path decomposition, and the full-flag repair plus canonical translation. They overlap technically, as disclosed, and are not five independent proofs of the conjecture. The progress count is reasonable under that stated meaning.

## Independent computation and reproducibility

`AUTHOR_REPLAY.json` reproduces the frozen checker's result exactly. `independent_verify.py` is a separate standard-library implementation, and `INDEPENDENT_RESULTS.json` records its output. Run the latter from this directory with:

    python3 independent_verify.py

Its orbit dimensions come from the explicit commuting-matrix equations; Gaussian coefficients come from enumeration of Schubert subset weights, rather than the candidate's Gaussian recursion. It covers:

- 2,460 profiles with n<=4 and rank/homology entries in {0,1,2};
- 18,525 rank-drop cases;
- 1,864 semismall profiles;
- 12,580 relevant-path comparisons;
- 5,665 small-chamber degree checks;
- 2,215 comparisons with the separately implemented sparse source formula in overlapping small chambers;
- the complete four-stratum non-sparse example using both image and kernel decompositions.

All passed. The supplied replay additionally reproduces its 55 partition/Gaussian checks and 180 determinantal cases. These totals count finite, overlapping assertion families. Neither checker is a general IC engine, and the general proofs above rest on algebraic geometry and the stated standard theorems, not the number of successful examples.

## Final disposition

There are no required corrections to the frozen partial-result packet. A later extension should continue to state the reduced-variety convention explicitly, preserve the normalization of IC, and distinguish exact decomposition identities from a proved closed Catalan rule. Those are scope safeguards, not defects requiring a new freeze.

The audit contains only authored mathematical analysis, verification code, result data, and hash metadata. It includes no source PDFs, extracted source corpora, private paths, or raw search responses. No remote write was performed.
