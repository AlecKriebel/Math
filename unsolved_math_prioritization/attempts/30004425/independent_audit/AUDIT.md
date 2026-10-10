# Independent adversarial audit: 30004425

Date: 5 October 2026. Rank: 750. Source code: OWR-17473-001.

## Verdict

**REVISE_REQUIRED, narrowly for two publication corrections.** The mathematical controls and the qualified prior-results/source-curation finding pass. No substantive error was found in any retained example-specific proof. This is not a new solution, a new counterexample, or a complete general classification of semigroup wall crossing.

The untouched author archive has 17,849 bytes and SHA-256 `8297f9480c92cf9a736468cfeefc008b62a04b7e4674c8851b9e72fb6c99a446`. All eight ZIP members agree with the unpacked freeze. All seven manifest-covered files pass, and the author program's output agrees byte-for-byte with its saved results. The audit did not modify the freeze or perform a remote write.

Required publication corrections:

1. REPORT.md, setting bullet: replace “finite semigroups” with “finitely generated semigroups.” These semigroups are infinite: a degree-one generator has distinct positive multiples. This is a terminology error, not a failure of the subsequent proof.
2. SOURCE_VERIFICATION.json, repository.queue.verification and the final retrieval-history entry: do not describe the embedded queue header as a blob/size mismatch. The complete queue content independently measures 389,371 bytes and hashes to Git blob `483de6795be8c12bacc3d18e1ef04900eddedf04`, exactly matching its pinned tree. Its SHA-256 is `6b37d1112c4223ae1c39156a98a745389112a7b129080dcd3a6439c334ebf2c2`. The old sha/size on its first line is literal stale file content. There is no demonstrated transport-integrity failure and no queue repair is warranted. Preserve the earlier freeze; correct the publication copy and regenerate its manifest.

No other required mathematical revision was identified. The two replacements should receive a small delta audit before the revised publication package is labeled PASS.

## Disposition and credit

**Conservative queue recommendation: `unsolved`, 1/5, expressly qualified as a prior-results/source-curation correction.** This is a status recommendation for the still-broad dataset wording, not a finding that the known convex-body theorem remains open. Do not use `verified_solved` or claim novelty.

Why conservative: the exact row bundles maps and semigroups without specifying the desired structure or hypotheses. The general convex-body relation is established, but the particular natural semigroup bijection needs an extra common-Gröbner-cone condition; stronger compatibility assertions are false; a general characterization is not supplied here. A broad question of this kind does not give an unambiguous full-resolution criterion. The catalogue's claim that its checked primary literature supplies no general answer must nevertheless be corrected.

`already_solved`, 1/5 is defensible only if the queue explicitly uses it to retire this mis-extracted motivating question on the basis of the already-published, qualified answer. In that case the accompanying note must state the semigroup condition and counterexample, and must not imply that every stronger semigroup question has been resolved. No forced resolved label is warranted. If a genuine residual target is retained, formulate it separately, for example a characterization of when the standard-monomial bijection agrees with a geometric restriction. This audit does not establish that such a target is globally open as of this date, and does not silently substitute it for the dataset statement. Research-turn bookkeeping remains separate from the author's two mathematical passes and this independent verification.

## Primary-source reconciliation

The [OWR report](https://ems.press/content/serial-article-files/46846), printed pp. 580–582, places the motivating question immediately before Theorem A, then discusses semigroup limitations and states Theorem B. Its broad motivating wording was extracted without the nearby answer. The brief report also has a transposed matrix-size typo; the author's corrected row convention agrees with the full paper.

The [Escobar–Harada paper](https://arxiv.org/abs/1912.04809v2) gives the convex-body theorem in 2.7, the conditional semigroup bijection in Section 4.2, the relevant counterexample in 4.5, and the conditional Grassmannian compatibility theorem in 5.15. These are credited prior results. The [publisher record](https://academic.oup.com/imrn/article-abstract/2022/7/5152/5901312) confirms online publication on 4 September 2020 and IMRN 2022(7), 5152–5203, DOI 10.1093/imrn/rnaa230. A 2019 preprint date and a 2022 issue date are both accurate but describe different events.

All four scholarly PDFs and the exact dataset-server row were independently retrieved anew. Their byte counts and SHA-256 values agree with every author pin. The live statement hash matches the pinned catalogue record. This does not bind the live dataset response to an immutable upstream corpus revision. The two full corpus hashes remain manifest declarations, not audit-rehashed files. Detailed public verification metadata is in SOURCE_RECHECK.json.

## Source-defined scope and normalization

The base ring is a standard graded complex domain generated in degree one, of dimension d+1. Its projective variety has dimension d. Each prime tropical cone has dimension d+1 and their common face has dimension d. No normality, smoothness, Fano, reflexivity, or rationality assumption on the original variety should be inserted.

Choose common integral rows inside the face, including the all-ones degree row. The full source chooses complementary rows in their respective cones so that their sums with the common rows lie in the relative interiors. It fixes the homogeneous valuation order with reversed degree comparison followed by lexicographic comparison of the remaining coordinates. It would improve the exposition to state these choices explicitly rather than merely saying “on the corresponding sides.” The matrices have d+1 rows and n columns.

Integral row choices give integral columns and lattice polytopes; rational choices give rational polytopes. This rationality statement concerns polyhedral coordinates, not rationality of the original projective variety. A degree-one convex hull does not record missing points of the value semigroup. Nor does “toric” here impose normality.

The common projection is justified by the compatible valuations. The fiber-length ratio is a positive global constant, not an unconditional equality in arbitrary ambient coordinates. The full source ties this constant to the vertical value lattices. With the author's convention L2 = kappa L1, the shift and flip formulas have the correct scale and orientation. Normalized vertical lengths agree. Replacing the last row of M2 by twice itself preserves the cone but doubles its unnormalized lengths; the independent verifier rejects the unqualified equality. Adding combinations of the common rows produces the expected fiberwise shear. Rational piecewise-linear maps need not be integral or additive.

The source theorem in 5.15 retains a common Gröbner chamber and its specified valuation construction. The author does not claim it for arbitrary chosen maps, valuations, or Grassmannian embeddings. The report correctly avoids promoting a map of polytopes to a morphism between the toric special fibers.

## Independent review of every retained example proof

1. **Domain and dimension.** Regarding the degree-11 trinomial as a polynomial in x2 over C[x1,x3,x4], the x4-adic order of its constant term is exactly one, while the leading coefficient is one. Eisenstein and Gauss apply. The quotient is a three-dimensional domain; its Proj is a surface. This proof passes.

2. **Prime adjacency and third cone.** The two exponent differences have rank two. Their common real nullspace is the two-dimensional span of (1,1,1,1) and (0,1,2,3). The three ray weight triples are (0,0,11), (0,11,0), and (0,-11,-11), in the minimum convention. The first two maximal cones therefore meet exactly in the common two-dimensional facet. Initial ideals of a principal ideal are generated by the initial polynomial because initial forms multiply. For the third cone the factorization into a monomial times x3^3+x1*x4^2 proves nonprimeness; the latter factor cannot divide a monomial, so the ideal contains no monomial. All conclusions pass.

3. **Primeness and value groups.** An independent signed-cofactor computation gives primitive integer kernels (-6,11,-4,-1) and (-7,11,-1,-3). In each case the gcd of maximal minors is one, so the column group is Z^3. Fibers of the Laurent monomial map differ by multiples of that primitive relation. Removing a common monomial reduces any binomial in its kernel to a difference of equal powers of the two relation monomials. Factoring that difference proves that the displayed binomial generates the entire kernel. The image is a domain. This is a complete primeness argument, not merely a determinant test.

4. **Common chamber and all-degree representatives.** The cone on which x2^11 is the minimum-weight initial monomial has the two prime cones as faces. Standard exponents have x2-exponent in [0,10]. Reducing each block of eleven with the appropriate nonnegative relation monomial proves existence in every degree. The primitive relation changes that exponent by eleven, proving uniqueness in every degree. The same standard index set parametrizes both semigroups; their first two coordinates agree. This establishes the bijection and inverse in all degrees. The finite verifier is supplementary.

5. **Nonadditivity and representative ambiguity.** The vector q=(1,1,0) is fixed, whereas its elevenfold multiple maps to (11,11,11). Thus the bijection is not additive. The exponents (0,11,0,0) and (6,0,4,1) have the same first-matrix image and different second-matrix images, so using arbitrary representatives would not define a function. Both failures are independently certified.

6. **Convex geometry and maps.** A separate convex-hull algorithm recovers the two triangles from the columns. Exact intersection of their edges with vertical lines gives breakpoints 0,2,3 and the endpoint formulas in EXACT_CONTROLS.md. The affine identities on each complete interval follow from the interval endpoints, not from numerical sampling. They imply kappa=1, shift(q)=(1,1,1/6), and flip(q)=(1,1,1). The general fiberwise inverse formulas remain valid at zero-length fibers. Homogeneous extension at the origin is valid because the degree-one slices are bounded and all generators have positive degree.

7. **Saturation holes and nonnormality.** The point h=(1,1,1) is absent in degree one in both semigroups, is in the full value groups, and has 11h in both semigroups. Consequently its Laurent monomial is integral over each semigroup ring but absent from it. This proves affine nonnormality. Independently, the projective line x1=x2=0 has codimension one in each integral surface and lies in its singular locus by the derivatives. The Jacobian criterion and the necessary R1 condition prove projective nonnormality. The unimodular linear flip still sends q to this hole. No illicit passage to saturation occurs.

8. **Hilbert function.** Removing degree-n monomials divisible by x2^11 gives binomial(n+3,3) minus binomial(n-8,3) for n at least eleven, and the first term alone below eleven. The standard-representative proof justifies using this count for both semigroups.

9. **Actual flat family.** Monic division in x2 over C[s,t,x1,x3,x4] makes the quotient free over that polynomial ring with basis 1,x2,...,x2^10. Hence it is free over C[s,t] on the stated standard monomials, with finite free homogeneous components. A graded localization remains flat over the base, and its degree-zero component is a direct summand; thus every standard Proj chart is flat. The three displayed specializations are correct. The two weight paths have exponents eleven, and their diagonal changes of projective coordinates are invertible away from zero even though some weights are negative. These facts establish genuine flat degenerations. They do not produce a direct map between the special fibers.

## Later literature

[Proost's thesis](https://arxiv.org/abs/2407.14515) is a master's thesis, latest v2 dated 15 September 2024. Its extension via re-embedding needs appropriate prime lifts and surviving adjacency; the discussion also warns that the underlying procedure need not always terminate. Its Gr(3,6) computation is a case study. It does not eliminate the general qualifications. The audit did not rerun that large computation.

[Escobar–Harada–Manon](https://arxiv.org/abs/2408.01785) is currently arXiv v3, submitted 28 September 2026; its PDF internal date is 30 September. Theorems 7.11, 7.21, and 7.22 assume finite integral polyptych data, a strict dual pair, a detropicalization with convex adapted basis, and the detailed polytope/facet conditions of 7.11. Integrality of the polytope is additional in 7.22. Its proof identifies the central semigroup with all lattice points in the cone. That construction cannot simply be declared to recover arbitrary prescribed nonsaturated semigroups such as the audited example. No theorem supplying those data for every adjacent prime pair was found in the inspected passages, and no journal-publication upgrade is asserted.

Ilten's mutation discussion uses additional choices and a dual polyhedral construction. The report correctly avoids identifying it with a single unrestricted ordinary lattice mutation.

## Code, negative controls, and limits

Run `python3 independent_verify.py`. It imports no author code and uses only exact standard-library arithmetic. It checks 36,190 values across both semigroups in degrees 0–24, using dynamic reachability and independent 2-by-2 linear solves for representatives. It reconstructs convex hulls, kernels, initial weights, the normality witness, and the relevant map values. Eight deliberately false strengthenings are rejected, including additivity, arbitrary representatives, integrality, preservation of the unsaturated semigroup, and unnormalized length equality after row rescaling.

Run `python3 verify_audit_manifest.py` to verify the frozen audit payload and deterministic arithmetic replay. These programs do not certify every imported theorem or replace mathematical proofs. The broad general results remain explicitly imported published mathematics. No exhaustive literature search or proof-assistant certification is claimed. Fresh repository checks bind the catalogue and queue to the pinned tree, confirm the target's absence from the complete 62-entry attempts tree, and find no exact-ID PR; they do not independently repeat every historical search in the author report.

Run `python3 mutation_verify.py /path/to/author/safe_freeze` for executable negative controls against the author code. Four isolated altered copies, changing a matrix sign, the standard reduction, the standard cutoff, and the flip orientation, all fail at mathematical assertions. The untouched author program still passes and matches its saved output. No author file is rewritten.

The audit package contains only authored analysis/code/results and public verification metadata. It excludes PDFs, source extracts, raw dataset contents, and private coordination files.
