# PR55 priority disposition adjudication — new SOURCE note

**Recommendation: `already_solved`, valid partial/priority finding, no paper under the user's process.** The original OWR request does not prescribe the candidate's algorithm. A published stronger algebraic/combinatorial formula, followed by the verified projection and elementary integration steps, already supplies the requested equality in the candidate's entire restored smooth regime. Requiring an earlier publication of the exact candidate mechanism would test a different, narrower claim of proof originality.

This recommendation supersedes the disposition caution in the frozen priority REPORT, without altering that historical packet or its READY. It is a SOURCE recommendation for ROOT; no native status change, merger, paper or publication is performed here.

## What the source actually asks

The complete Problem sentence on printed p.921 is:

> “Can we (re)-prove the coincidence between \(\mathbb W(\Delta_{X\times\mathbb P^{n-1}})\) and \(\mathbb W(\mathrm{Hu}_A)\) in a combinatorial way?”

[Official OWR PDF, printed p.921](https://ems.press/content/serial-article-files/51856). The notation above is a mathematical transcription of the extracted PDF text. The source's preceding discussion invokes the general GKZ framework. It does not demand a particular face algorithm, finite-difference identity, product-refinement construction, or reconstruction of GKZ foundations.

The candidate and prior-art comparison use the hypotheses recovered from the cited Sano theorem: smooth toric variety, complete very ample system, all lattice points of the Delzant polytope, degree≥2, n≥1, and massive boundary simplices. This adjudication covers that same restored regime. It does not settle an unrestricted sparse/singular reading of the report's introductory notation.

## What is published and what is our deduction

Esterov's [2010 paper](https://arxiv.org/html/0810.4996v3), [journal DOI10.1007/s00454-010-9242-7](https://link.springer.com/article/10.1007/s00454-010-9242-7), publishes the general mixed-fiber Newton-polytope theorem and its unmixed binomial face formula: global Theorem5.10 and Definition5.12. Its Cayley identification, signed Euler obstruction convention and normalization are also published ingredients.

The exact target specialization was written and checked during this audit. We do **not** assert that Esterov names the Hurwitz polytope, displays ξ_T=nη_{T,n}−η_{T,n−1}, or prints our argument verbatim. The independent mathematical comparison is preserved in [the frozen specialization note](../priority_adversary_family/ESTEROV_SPECIALIZATION.md).

Its steps have no remaining target-sized unsupported claim:

1. Universal coefficient blocks give the Cayley discriminant and satisfy the stated general-position requirement; all support/lattice-index assumptions are checked.
2. Coordinate-sum projection commutes with normalized fiber integrals and their polarization. The projected coefficient polytopes become identical.
3. Put l=n−1 in the published repeated-argument formula. Signed Delzant face coefficients and the binomial factors leave exactly nΣ_Q−Σ_facets.
4. The minimum of each fiber support is the lower envelope of the height. Integration of an affine function over a simplex equals its vertex average times volume, yielding η_{T,n} and massive η_{T,n−1} with the exact factorials.
5. Thus every generic height has support value 〈w,nη_{T,n}−η_{T,n−1}〉. Each regular height chamber gives that support gradient; all vertices are generically exposed. The convex hull is therefore precisely the requested model.

This is a full direct corollary of prior sufficient machinery, not merely the already-known geometric equality repeated, numerical evidence, a one-sided inclusion, or transfer of the missing reverse inclusion to an unproved assertion. Its proof may be recorded as this project's explicit derivation/application of prior work, with exact attribution.

## Strongest case for `already_solved`

The task asks whether a combinatorial proof exists, rather than whether this exact proof has been published. Esterov already provides an all-dimensional combinatorial Newton formula for a broader family. The remaining specialization uses standard linear functoriality and simplex integration, and now has a fully checkable proof under every candidate hypothesis. No proposed new mathematical principle is needed to bridge the formula to the target.

The candidate itself is accepted as combinatorial **within an established framework**: it invokes deep GKZ algebraic results. On that same convention, one cannot disqualify the prior Newton formula solely because its foundational proof uses algebraic geometry or Euler characteristics. The comparison from the formula to the requested characteristic-vector model uses finite combinatorial data. Both methods depend on proved general discriminant machinery and avoid Sano's K-energy route.

Under the user's process, an overlooked sufficient prior theorem is a priority issue even when a new author supplies a useful different derivation. A distinct proof organization may merit exposition elsewhere, but it does not justify treating the original request as an unsolved problem that this PR newly resolves decisively. Thus `already_solved` and a credited prior-art/partial record is the conservative and substantively supported disposition.

## Strongest case for retaining a new-proof claim

An implicit corollary and an explicitly published proof of a named theorem are not identical bibliographic events. The original author posed the reproof question in 2025. Our audit has not located a pre-existing publication spelling out the exact target specialization, and the candidate provides a different, transparent mechanism. A short new proof of a known result can have mathematical value and can be publishable without claiming a new equality.

There is also a meaningful possible proof-type distinction: someone could require all of the Newton-discriminant foundations to be proved by elementary combinatorics, or require the model comparison to proceed specifically from GKZ massive vectors rather than from a stronger mixed-discriminant formula. On such a newly tightened criterion, the Esterov corollary might not be the requested proof. However, the source does not state that criterion, and the current candidate does not rebuild its own GKZ foundations. Applying that restriction only to prior work would be inconsistent. If it were adopted symmetrically, it would weaken acceptance of the candidate as well.

These points support a qualified claim that the candidate is an alternative proof whose precise historical originality is unestablished. They do **not** override the user's requirement that a claimed_solved preprint decisively solve an originally unsolved task without a priority issue.

## Final narrow judgment

The earlier audit correctly separated the known equality from possible originality of a particular proof. Its caution against declaring `already_solved` merely because the equality was already known remains valid. The stronger prior theorem plus the verified full specialization is additional decisive evidence. Exact prior publication of the candidate algorithm is unnecessary for the native disposition requested by the user.

Recommend preserving the valid candidate, author/checker evidence and the new priority finding as attributed partial progress, setting `already_solved` with a reason explaining the prior theorem and our explicit specialization, and creating no paper/Zenodo/DOI package for this PR under this process. Do not say an exact 2010 Hurwitz proof was located, that all historical literature was searched, or that the candidate method has no novelty whatsoever. Those stronger historical statements are unsupported.
