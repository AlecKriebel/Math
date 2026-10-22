# Independent source and corollary review: PASS with explicit ranges

Problem2800404 / Bandeira Open Problem4.4(3). The source-derived proof passes for0<epsilon,delta<1 and real1<=s<=d<=m, with positive integer d,m. Recommended disposition: already_solved0/5, explicitly qualified to the stated standard regime and credited to Cai–Han–Zhang2022. This does not resolve the other OSNAP models or unrestricted parameter interpretations.

## Source matching

The full primary notes' pages76–77 were visually inspected, including the exact iid sparse-sign distribution and both requested parameter scales. Part2 gives the integer column-sparsity convention; part3 uses independent entries. The auxiliary normalization issue in part1 is real and is not imported into part3. The imported title does not authorize replacing the coordinate model by an arbitrary-subspace or fixed-count result.

The published Cai–Han–Zhang Lemmas5.4 and2.6 were checked in the local primary PDF/text. Relevant full proof passages on pages24–26 and18–19 were read; lemma statements and page26 were visually checked. The bounded-entry proof explicitly uses symmetry even though its statement omits that word. The target distribution has that symmetry. Its scalar factors are bounded in absolute value, so negative odd centered Bernoulli moments do not invalidate the termwise product comparison. Gaussian mixed moments are nonnegative pairing counts, with precisely the stated centered-first-moment zero case. The shape counting is the credited published argument. The rounded variance parameters in its proof may be written with a maximum with1: since both variances here are positive, their ceilings already have that property.

## Proof audit

For X=sqrt(s)Z transposed into d by m shape, the variance sums are ds/m and s, and the centered Gram is XX^T-sI. Even q permits norm-to-trace comparison. Retaining d/r in the comparison and using r Gaussian eigenvalues gives exactly d, with no m factor and no log(m). The first, operator-norm inequality in Lemma2.6 suffices; no accidental extra trace factor is introduced.

For d>=2, q=2ceil(log(2d/delta)) obeys q<=7log(d/delta): expanding the ceiling gives2L+2log2+2, bounded by7L for L>=log2. Consequently d/m and q/s are each at most10^(-4)epsilon squared under the proposed constants. The rounding inequalities r<=ds/m+q and t<=s+q imply the displayed B/s bound. Its four terms are bounded by(4+4sqrt2)(sqrt(a)+a)epsilon with a=10^(-4), hence less thanepsilon/3. The strict Markov estimate is valid for the target event including equality at epsilon.

The d=1 case genuinely needs separate treatment because log(1/delta) can approach zero. Under1<=s<=d it has s=1, and its exact binomial success probability exceeds1/3 while the assumed sparsity lower bound forces delta>2/3. The proof covers this edge case. For s=1/4 the standalone counterexample is also correct:4N cannot approach1 within1/2, while delta can be selected close enough to1 to meet any proposed sparsity constant. Thus the lower-range qualification must remain visible; it cannot be silently dropped from the status or PR description.

## Evidence and limits

All nine manifest-bound source-result files and six source hashes match. The author's2,652 exact controls replay byte-identically. A separate scalar mixed-moment and even-Gaussian-moment checker passes10,659 exact assertions. These controls supplement the general specialization proof; they are not a finite proof of concentration for all dimensions.

No mandatory correction was found. Preserve frozen bytes and add this review separately. The result is a credited consequence of existing lemmas, not a new Wishart concentration theorem or first-priority claim. Publication must explicitly retain the standard ranges and the fact that the broader parts1–2 are outside this target.
