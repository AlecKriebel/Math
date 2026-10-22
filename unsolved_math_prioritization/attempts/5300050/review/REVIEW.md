# Independent review of the basin-boundary entropy partial

**Verdict: PASS_SCOPED_PARTIAL_RESULTS.** No mandatory correction was found. Recommend **unsolved, 1/5** for problem 5300050. The submitted work establishes the explicit harmonic-measure diagnostic and the continuous-extension sufficient case. It neither proves the missing general upper bound nor supplies a counterexample to the original equality.

Reviewed on 30 September 2026 by a separate GPT-6 Astra agent at xhigh effort. This is an independent AI mathematical review, not human peer review or a novelty certification. The immutable reviewed PARTIAL.md has SHA-256
**a9d74e2eb422b5406a9f328c6921effbc7c162243b262263ab1b3c5e7f75fed9**.

## Exact source and scope

I read the original contribution in [IMS 1992/7](https://www.math.stonybrook.edu/preprints/ims92-7.pdf), printed pp. 29–30, and visually checked p. 30. Problem 1.3 asks whether the boundary restriction has entropy equal to the logarithm of the degree on the attracting domain. The comment states: “The ≥ inequality is known and easy. The problem is with the opposite one.”

The preceding setup gives the proper holomorphic self-map of a simply connected spherical domain, degree at least two, with iterates converging to an interior constant. Problem 1.1 adds holomorphic extension across the spherical closure. There is no given continuous extension of the Riemann map. The package correctly uses the compact spherical boundary, local degree on the stated self-map, and ordinary compact-space topological entropy. It does not replace these by the global rational degree, entropy on a noncompact basin, or a pre-return map.

The boundary-invariance proof is correct. For a sequence in the domain tending to the boundary, continuity places its image limit in the closure, and properness excludes an interior limit. Conversely, surjectivity of a nonconstant proper self-map supplies interior preimages of any sequence approaching a prescribed boundary point. Compactness and continuity produce a boundary preimage. The attracting point is fixed by continuity of the iterates.

## Blaschke diagnostic

For $0<a<1$, the map $B_a(z)=z(z-a)/(1-az)$ is holomorphic near the closed disk, proper of degree two, and fixes zero with derivative $-a$. Its second factor has modulus strictly below one in the disk. On each smaller closed disk its modulus is uniformly below one, proving convergence of every interior orbit to zero. The reflection identity excludes exterior points from that basin, including the spherical interpretation at poles.

The angular derivative is positive and satisfies
\[
D_a(\theta)=\frac{2-2a\cos\theta}{1-2a\cos\theta+a^2},
\qquad
\frac{2}{1+a}\le D_a\le\frac{2}{1-a}.
\]
Thus every admitted parameter gives uniform expansion. The lift proof of conjugacy to doubling is valid: bounded one-step deviation from $2x$ implies uniform convergence of $2^{-n}F^n(x)$ and a uniformly bounded difference between $F^n(x)$ and $2^nH(x)$. A nontrivial interval collapsed by $H$ would contradict expansion of its iterated length. The resulting degree-one homeomorphism is a genuine conjugacy, giving topological entropy $\log 2$.

The harmonic mean-value argument proves invariance of normalized length without presupposing maximal entropy. The partition endpoints are correctly $1,-1$, since the equation $B_a(z)=1$ reduces to $z^2=1$. The two open semicircles map monotonically onto the circle cut at $1$. Every $n$-cylinder maps onto that cut circle and has diameter tending uniformly to zero, so this finite partition is generating modulo its countable, null endpoint set.

For precision, if $L$ is a Lipschitz constant for the logarithm of the angular derivative and $\lambda>1$ is its expansion lower bound, the oscillation of $\log D(B_a^n)$ on any $n$-cylinder is at most
\[
2\pi L\sum_{j=1}^n\lambda^{-j}
<\frac{2\pi L}{\lambda-1}.
\]
Applying the mean-value theorem on the full image interval then gives the stated uniform bounded error between $-\log m(I_n(x))$ and $\log D(B_a^n)(x)$. Integration, invariance, and the entropy theorem for a generating finite partition justify the metric-entropy formula. No numerical limit or unproved identification of the invariant measure enters.

The identity
\[
D_{3/5}(z)=\frac95\,
\frac{|1-z/3|^2}{|1-3z/5|^2}
\quad (|z|=1)
\]
is exact. Both logarithmic factors have mean zero because their zeros lie outside the closed disk. Hence $h_m(B_{3/5})=\log(9/5)$, strictly below $\log2$. The general factorization with $b=\sqrt{1-a^2}$ and $c=a/(1+b)$ yields $\log(1+b)$ as claimed. The limit as $a$ tends to one is valid through admitted parameters only. This proves that harmonic measure need not be a measure of maximal entropy, while leaving the original boundary-entropy equality intact in the example.

As an independent check of the invariant-measure mechanism, for any noncritical boundary point $z$, put $w=B_a(z)$. The other inverse root is $-w/z$. Exact rational controls verify that it is distinct, lies on the circle, and satisfies the transfer identity
\[
\frac{1}{D_a(z)}+\frac{1}{D_a(-w/z)}=1.
\]
These checks supplement rather than replace the mean-value proof.

## Continuous-extension sufficient case

The conjugated disk map is a finite Blaschke product fixing zero. Its circle derivative is a sum of $d$ Poisson kernels, including the constant kernel one. For $d\ge2$, the remaining positive continuous summands give a uniform expansion bound greater than one. The degree-$d$ version of the lift argument gives circle entropy $\log d$.

When the Riemann map extends continuously to the closed disk, its boundary map is a continuous surjection onto the spherical boundary. Boundary points cannot map into the interior because the interior inverse is continuous and maps compact interior sets to compact subsets of the disk. The interior conjugacy therefore extends to a continuous boundary factor map. Entropy monotonicity gives the upper bound; the lower bound is explicitly imported with credit from the original source. The separated-set justification has the correct direction and quantifiers. Local connectivity is used only as a sufficient hypothesis, not asserted for all original basins.

The proposed measurable replacement is also correctly conditional: if every positive-entropy ergodic boundary invariant measure is a factor of an invariant circle measure, entropy monotonicity and the variational principle give the missing upper bound. This property is not established in the package.

## Later-source limitations

I read the published [Przytycki accessibility paper](https://www.impan.pl/~feliksp/access.pdf), introduction through Remark 0.7, and visually inspected Corollary 0.1 on p. 263. Its measure-lifting conclusion explicitly retains the almost-everywhere side condition (0.3′), in addition to shrinking edges. The subsequent prose confirms both additional assumptions. Corollary 0.2 uses complete invariance of a rational basin. The submitted text correctly preserves this restriction rather than treating the abstract or a shortened “onto” statement as unconditional.

The published Roesch–Yin Theorem 1 concerns bounded polynomial Fatou components that are not eventually Siegel disks; the attracting cases used here are within its scope. Hawkins–Taylor concerns the mass of boundaries under a global rational-map maximal-entropy measure. Levin's Appendix A supplies a lower bound for completely invariant compact sets. I checked the respective statements and relevant hypotheses; this review does not independently reprove their analytic machinery. None of these inspected statements supplies the absent general upper bound in the submitted argument. The bounded search is not a proof that no later resolution exists.

## Reproducibility and publication scope

All **4,377** submitted rational assertions replay successfully and reproduce the submitted JSON receipt byte for byte. The independently written standard-library checker passes **1,701** exact assertions, covering inverse-root transfer normalization, inverse-contraction sums, coefficient-level entropy factorizations, and endpoint controls.

The algebraic checks do not prove entropy limits or boundary accessibility. Those claims were reviewed analytically above. The source qualifications and unresolved status are essential: publication may report the diagnostic and the sufficient case, with credited known lower bounds, but must not mark the original problem solved. No change to the author's mathematical file was made.

The exact publication file list and hashes are recorded in review_summary.json. The preserved author_replay/PARTIAL.md is required by the independent checker. Source PDFs and rendered source images are not part of that publication list.
