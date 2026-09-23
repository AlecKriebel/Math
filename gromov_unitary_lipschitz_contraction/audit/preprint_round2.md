# Independent adversarial preprint audit — round 2

**Completed:** 2026-09-23 13:45 UTC. **Completion estimate:** 100% of this bounded preprint-readiness audit, not a probability of correctness. **Reviewer:** independent AI-assisted internal reviewer; not external peer review.

| Audited artifact | SHA-256 |
|---|---|
| `paper/main.tex` (v1.1) | `954d45001560d29f3286383a40ff9c477a257d9359e02ada7477eac67a0cda4e` |
| `paper/main.pdf` (v1.1) | `3e8c052065110ec412a3e01e80f0c789f663ce6a9eb74c31aa8fdd99915fc02b` |
| Gromov's original PDF, independently retrieved | `1478b4025eb55e7237ab3f066e8924938a1de4cd407d74893b49f2b9007d9645` |

## Verdict

**Ready as a mathematically sound, accurately framed, unrefereed preprint. No actionable issue was found, at any severity. No further manuscript revision is required by this audit.** This is neither journal acceptance advice nor certification of first priority.

I read the revised source and complete PDF before earlier reviews. I independently audited the theorem through spectral functional calculus and tangent geometry, then examined the companions and the round-1 response. All four rendered manuscript pages were visually inspected: no clipping, missing mathematics, or unreadable references was found. No publication file was edited, and no person was contacted. Outputs other than this report are confined to `tmp/preprint_round2/`; no commit or push was made.

## Independent mathematical checks

**Spectral region and metrics.** If the principal eigenangles of a unitary are θj, its distance from I is `||θ||₂` for the unnormalized Hilbert–Schmidt metric and `||θ||∞` for the operator-norm length metric. The diagonal exponential path gives the upper bounds. For the lower bounds, follow an orthonormal eigenbasis along any connecting unitary path: each vector travels spherical distance at least `|θj|`. The maximum gives the operator bound; the integral triangle inequality applied to the vector of speeds gives the Hilbert–Schmidt bound. Thus normalization by Φ(p), diameter π, and `L≤1/2` put the entire image in the stated closed semicircle. The Hilbert–Schmidt admissible angle region is actually the smaller Euclidean ball; using the larger semicircle remains valid.

**Noncommutative differential.** Diagonalize W with eigenvalues `zj=e^(iθj)` and write a tangent vector as `E=iWK`, with K Hermitian. For `f(z)=(z+t)/(1+tz)`, the divided differences are

`f[zj,zk]=(1−t²)/((1+tzj)(1+tzk))`,

including repeated eigenvalues by continuity. Set `D=diag((1+tzj)⁻¹)`. Translating the output tangent back to the identity gives exactly

`−i F_t(W)* DF_t(W)[iWK]=(1−t²)D* K D`.

This diagonal congruence, rather than an entrywise bound alone, proves the operator-norm estimate as well as the Hilbert–Schmidt estimate. Since `|1+tzj|²=1+t²+2t cos θj≥1+t²`, both tangent norms contract by at most `q_t`. This independently confirms the manuscript's central noncommutative step, including repeated eigenvalues and the closed boundary.

**Intrinsic passage.** A minimizing source geodesic has an absolutely continuous image under Φ, with norm speed at most L almost everywhere. Every image point satisfies the spectral restriction. Integrating the preceding tangent estimate therefore bounds its transformed length by `q_t L` times the source length. Local principal-angle comparison identifies intrinsic speed with ambient matrix-norm speed. No target geodesic-convexity assumption, interchange of chordal and intrinsic distances, or differentiability of the operator norm is required.

**Endpoints, topology, and boundary cases.** The inverse stays nonsingular at `t=1` and eigenvalues ±i. The endpoints and fixed constants give the claimed strong retraction; it does not contract the copy of U(N) to a prescribed point. Normalization changes by at most twice the input sup distance, and the uniform inverse bound supplies joint time/input continuity. Direct substitution proves continuity for arbitrary topological parameter spaces and the stated frame equivariance. The strict sublevel, scalar target, antipodal source points, and zero Lipschitz constant are covered. For S⁰ with angular distance π, the displayed scalar angle derivative lies in `[0,q_t]`; integrating from zero contracts each angle and hence both distance norms. The separate S⁰ treatment is necessary and correct.

## Source alignment and package checks

I directly inspected text and rendered printed pp. 35–36 of [Gromov's original manuscript](https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/101-problemsOct1-2017.pdf). The literal question [?24](i) uses threshold 1/2 and continuous dependence on Φ. The preceding threshold-1 discussion and later sphere-fibration questions are distinct. The paper accurately defines its two metrics and does not infer arbitrary invariant metrics from one normalization. Its logarithm-chart observation and qualified classical-mechanism/priority wording are sound.

- The revised derivative wording, companion link, and embedded PDF title/author/subject address all three round-1 suggestions.
- Read the companion reviews, source record, log, README, scripts, builder, website HTML, citation record, and deposit metadata. No substantive inconsistency or inflated verification/priority claim was found.
- Replayed both diagnostics: **10/10 exact checks; 7,679 numerical checks, zero failures**. An additional 240-case spectral-functional-calculus differential diagnostic had maximum residual `1.38×10⁻⁹`; this is supplementary floating-point evidence only.
- Verified every embedded archive checksum, every archived file against its original, outer checksums, and all local published copies. **No mismatch.** Clean extraction and rebuild reproduced both ZIP archives byte for byte.

**Strongest verified result:** the full stated quantitative retraction, including the optional S⁰ extension. **Remaining gap for preprint readiness:** none identified. Exhaustive novelty certification, formal proof certification, external peer review, and deployment of the revision are outside this audit.
