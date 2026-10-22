# Full-scope implications assembled during this audit

These derivations were assembled on2026-10-17. They are not claims that the cited authors printed these corollaries or assigned historical priority to them.

## Direct modular Fourier sum using Gilmer–Kopparty

Let T be the ordinary triangle count in fixed-p G(n,p), μ=ET, σ=sqrt Var(T)=Θ_p(n²), Z=(T−μ)/σ and ψ_n(t)=E exp(itZ). The imported statements are Gilmer–Kopparty's author manuscript dated6December2014, PDFp6: Lemma4 gives |ψ_n(t)|≤D|t|^(−1−δ0) for0<|t|≤n^.55, and Lemma5 gives |ψ_n(t)|≤D|t|^(−50) for n^.55≤|t|≤πσ. Their text immediately combines these into an envelope. Choose δ=min(δ0,1)>0; after increasing D, the common envelope D|t|^(−1−δ) applies throughout1≤|t|≤πσ. Only these theorem interfaces are imported, not a fresh proof of the source's conditioning machinery.

For integer q≥2, the roots-of-unity filter gives, for every residue a,

 q P(T≡a mod q)−1 = Σ_{j=1}^{q−1} exp(−2πija/q) E exp(2πijT/q).

Set j*=min(j,q−j). Since T is integer, frequencies aboveπ may be reduced modulo2π. Centering changes only the phase, so

 |E exp(2πijT/q)| = |ψ_n(2πσj*/q)|.

If q=o(σ), then d=2πσ/q→∞. Eventually every nonzero reduced grid point lies in[1,πσ], exactly the imported envelope's range. Each positive j* occurs at most twice, including the even-q endpoint. Therefore, uniformly in a,

 |q P(T≡a mod q)−1|
 ≤ 2D Σ_{j≥1}(2πσj/q)^(−1−δ)
 ≤ [2D(1+1/δ)/(2π)^(1+δ)](q/σ)^(1+δ) →0.

For q=1 the discrepancy is identically zero. This proves sufficiency for every sequence q=o(n²), including composites, bounded/oscillating values and arbitrary slow approach to the threshold. It uses the **earlier characteristic-function lemmas**, not merely the earlier qualitative LLT conclusion. Source definitions and the true standard deviation agree with the triangle count. The root proof's independent binomial-projection CLT supplies necessity; the standard-deviation obstruction is already explicitly described in Scott–Tateno2009. Thus the full equivalence is an implication of old ingredients, with no new mechanism needed.

The finite Fourier identity, pairing endpoint and convergent p-series are elementary and checked here. This is not a computational certification of the imported analytic envelope.

## Quantitative local theorem route

The operative Sah–Sawhney pointwise theorem supplies normalized error δ_n=O(n^(−1/2+ε)), ε<1/2. The root proof's bounded-differences tail and central-window count produce δ_n O(sqrt log n)+O(q/σ)+negligible tails. Hence the sharp sufficiency follows for every q=o(σ). Berkowitz's earlier quantitative triangle and clique results supply comparable polynomial-rate inputs, with correct means and standard deviations. I did not reprove their deep estimates.

## General mechanism comparison with Weber

Weber's2022 preprint explicitly truncates a residue sum to a finite window, applies a pointwise LLT on that window, controls tails and compares a Gaussian progression sum through Poisson summation. The theorem is stated for independent sums; one may not simply identify T with such a sum. The comparison is of mechanisms only. The candidate's own finite-window argument keeps the possible extra endpoint term, so no printed source constants are needed. A full transfer implication for triangles from this source alone is **not** asserted.

## Claims deliberately not made

No earlier exact sharp modular statement is asserted without a primary passage. No theorem proven today is backdated as an earlier explicit theorem. No new LLT, new Fourier method, current openness, exhaustive worldwide firstness, or independent discovery lineage is claimed. The ordinary2K2 counterexample remains Sah–Sawhney's known result.
