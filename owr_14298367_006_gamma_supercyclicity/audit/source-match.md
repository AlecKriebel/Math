# Independent source and conjugacy audit

Audit timestamp: 2026-09-23 04:05 UTC. Scope: recover the original question and its standing hypotheses, then independently check the composition-to-sequence-space reduction. Completion estimate for this bounded audit: 100%. This is not a priority clearance or a formal proof certificate for the entire candidate.

## Primary source recovered

The supplied catalog URL, <https://www.unsolvedmath.com/problems/OWR-14298367-006>, returned HTTP 429 / Vercel challenge both through browser retrieval and a direct request. Its actual page contents and current status could not be inspected. The response and headers are preserved in `sources/source_catalog_response.html` and `sources/source_catalog_headers.txt`.

The underlying primary report was recovered independently:

- *Mini-Workshop: New Horizons in Linear Dynamics, Universality, and the Invariant Subspace Problem*, Oberwolfach Report 19/2024, workshop 7–12 April 2024, publisher DOI [10.4171/OWR/2024/19](https://doi.org/10.4171/OWR/2024/19).
- [MFO record](https://publications.mfo.de/handle/mfo/4214), repository DOI [10.14760/OWR-2024-19](https://doi.org/10.14760/OWR-2024-19).
- [Primary PDF](https://publications.mfo.de/bitstream/handle/mfo/4214/OWR_2024_19.pdf?isAllowed=y&sequence=1), preserved as `sources/source_OWR_2024_19.pdf` with extracted text alongside it. SHA-256: `620866807131964a6c0e4ceb53f6b1dfc08fe49911b836cf14cc913b82b37b6f`.
- The question is at printed page 1083, in Emma D'Aniello's report, *Preserved dynamics: a focus on hypercyclic and supercyclic behaviors*, joint work with Martina Maiuriello, pp. 1081–1084.

The printed question asks whether the stated equivalence of Γ-supercyclicity for the composition operator and its associated bilateral shift extends to every subset Γ of C. This matches the mathematical question in the user-supplied candidate. Mapping it to the supplied catalog identifier remains dependent on the user's attribution because the catalog itself was inaccessible.

## Standing hypotheses and boundary of the claim

The report's two relevant talks use separable Banach spaces (pp. 1078 and 1081). The measure setup (pp. 1079–1080) is σ-finite, with a bijective bimeasurable map f. Both f and its inverse satisfy a uniform upper measure bound, ensuring a bounded invertible composition operator on Lp, 1 ≤ p < ∞. Dissipativity means a disjoint partition by iterates of a wandering set W with finite positive measure. Bounded distortion is precisely the candidate's two-sided comparison, for all integers and all measurable subsets of W. Page 1080 defines the shift by (Bw a)j = wj+1 aj+1; page 1082 supplies the candidate's weight formula.

As corroboration, the report's reference [7], [D'Aniello–Maiuriello, arXiv:2404.04028](https://arxiv.org/abs/2404.04028), explicitly adopts separable Banach spaces in Section 2 and second-countable locally compact measure spaces from Section 3 onward. The retrieved PDF is v2 (6 February 2025), saved as `sources/source_DAniello_Maiuriello_2404_04028.pdf`; SHA-256: `70f4454d1d713937c8aefc3b4ff1af2fdebab1de645b6948cfe375828dff0dfd`.

**Required clarification for a standalone theorem:** explicitly assume that the complex Lp space is separable. The candidate's amplification lemma requires this, and σ-finiteness alone does not imply it. This is consistent with the report's standing context, not an extra restriction on Γ.

Separability is essential if one tries to generalize beyond that context. Let Ω carry an uncountable independent Bernoulli product probability measure, put X = Z × Ω, give layer j measure 2^(-|j|) times that probability, and let f(j,ω) = (j+1,ω). The system has distortion constant 1 and bounded invertible composition operator, but its Lp is nonseparable. No Γ-projective orbit can be dense there: it is contained in the separable closed span of a countable orbit. The scalar associated shift, by the candidate's elementary tail criterion for Γ = {1}, is hypercyclic. Thus a theorem stated for arbitrary σ-finite measure spaces without separability would be false. The standard Bernoulli coordinate indicators show nonseparability directly: any two differ with probability 1/2 and hence remain separated in Lp.

## Independent verification of the sequence-space reduction

Write mj = μ(fjW), c_j = mj/m0, and E = Lp(W). Let A and B be finite constants with μ(f^(-1)C) ≤ A μ(C) and μ(fC) ≤ B μ(C). Iteration gives finite positive mj for every integer j: upper bounds give finiteness, and pulling back/forward a zero layer would contradict m0 > 0. Moreover c_(j-1)/c_j ≤ A and c_(j+1)/c_j ≤ B. Thus bilateral translation on the scalar and E-valued weighted sequence spaces is bounded and invertible, with norms at most A^(1/p) and B^(1/p), respectively.

For a measurable C ⊆ W, define νj(C) = μ(fjC). Bimeasurability and injectivity make νj a measure. Distortion gives K^(-1)c_j μ ≤ νj ≤ Kc_j μ. Because μ restricted to W is finite, Radon–Nikodym applies without any hidden assumption about the global measure algebra. Its density hj satisfies the corresponding bounds almost everywhere.

The map Jφ = (φ ∘ fj restricted to W) is well-defined on Lp equivalence classes: all iterates preserve the measure class. Partitioning X into its disjoint layers and applying the pushforward integral identity yields

\[
K^{-1}\sum_j c_j\|(J\varphi)_j\|_E^p
\le \|\varphi\|_p^p
\le K\sum_j c_j\|(J\varphi)_j\|_E^p.
\]

Surjectivity follows by selecting measurable representatives uj on W and defining φ on fjW as uj ∘ f^(-j). Countably many layers ensure the glued function is measurable, and the displayed norm bounds ensure integrability. The same measure-class observation makes the construction independent of representatives. Direct substitution gives JTf = SEJ.

E is nonzero because 0 < μ(W) < ∞. It is separable because extension by zero embeds E as a closed subspace of the assumed separable Lp(X). This is the precise justification needed to apply the candidate's amplification lemma.

Finally D : ℓp(Z) → ℓp(Z,c), (Da)j = c_j^(-1/p)aj, is onto and isometric. Using the report's shift convention and wj+1 = (c_j/c_(j+1))^(1/p),

\[
(DB_wa)_j=c_j^{-1/p}w_{j+1}a_{j+1}
=c_{j+1}^{-1/p}a_{j+1}=(SDa)_j.
\]

Both conjugacies are bounded complex-linear bijections, so they preserve density of Γ-orbits for arbitrary Γ, including empty Γ, Γ = {0}, nonmeasurable Γ, and Γ with no algebraic closure properties.

**Verdict for this portion:** the reduction is correct in the source's separable setting. No contradiction with the original question or unproved measure-theoretic step was found. The standalone manuscript must make separability explicit and must not advertise the result for all σ-finite measure spaces without it.

## Priority lead found during source retrieval

The primary article [*Orbits of the backward shifts with limit points*](https://www.sciencedirect.com/science/article/abs/pii/S0022247X24002154) says that an arbitrary-Γ characterization for scalar bilateral shifts had already been obtained by its second author in its reference [3]. This needs a priority audit before calling the candidate's scalar two-tail criterion novel. This audit does not infer that the E-valued amplification or the composition equivalence is already published.
