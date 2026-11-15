# A singleton-supported cycle correction to Byrnes's differential-poset bound

Alec Kriebel · 22 October 2026 · Version 1.0.0 · Unrefereed preprint

## Original abstract

For every ordinary unweighted r-differential poset and n ≥ 2, we subtract an explicit nonnegative term from Byrnes's cumulative upper bound for the nth rank size. The term is the cycle rank of the preceding incidence subgraph supported on elements with a singleton successor. Singleton witnesses transfer these cycles into the next incidence graph by replacing stars with trees having the same terminals. The correction can be positive and attained on standard reflected Young-prefix examples, and its coefficient one is sharp. A singleton-successor condition gives the conjectured local recurrence; two such successors give a conditional equality characterization. The result answers the printed request for an improvement of Byrnes's inequality in an incidence-dependent form. It does not prove the general local recurrence, improve the global Fibonacci envelope, or give a combinatorial proof of strict rank growth.

## What this means

A graded poset is arranged in ranks, with edges recording which elements cover those immediately below. Its rank sizes count the elements at each level. Differential posets satisfy a precise balance between the upward and downward edges.

Byrnes’s cumulative bound limits the size of the next rank using earlier rank sizes. This note subtracts a correction that can be read from the preceding incidence graph. Certain cycles are forced to survive into the next rank, leaving less room for new elements. The correction may be zero; classical examples show that it can also give a strict, attained improvement.

## The full bound

Fix any positive integer r and any ordinary unweighted r-differential poset P: it has one minimum, finite ranks, and the exact integer identity DU−UD = rI at every rank, including rank zero. Put pⱼ = |Pⱼ|. This is the standard ordinary category, allowing zero common covers; it is not an identity interpreted only modulo a characteristic.

For j ≥ 1, let Bⱼ be the bipartite cover graph on Pⱼ₋₁ ⊔ Pⱼ and let bⱼ = β(Bⱼ), where β(H) = |E(H)|−|V(H)|+c(H) and c(H) counts every component, including isolated vertices.

For n ≥ 2, let S consist of z ∈ Pₙ₋₂ having some a ∈ Pₙ₋₁ with the entire predecessor set pred(a) = {z}. Such an a is a singleton successor of z; this does not mean that z has only one successor. Let Hₛ retain S, every vertex of Pₙ₋₁, and the incident edges between them. Set qₙ = β(Hₛ).

The theorem holds for every such r, P and n: 0 ≤ qₙ ≤ bₙ₋₁ and bₙ ≥ qₙ. Thus, writing Uₙ = 1 + r Σ_{k=0}^{n−2} pₖ + (r−1)pₙ₋₁,

pₙ ≤ Uₙ−qₙ = r pₙ₋₁ + pₙ₋₂ + bₙ₋₁−qₙ.

The correction depends only on the two preceding incidence ranks, before Pₙ is constructed. No additional singleton-support hypothesis is needed for this bound.

## Why the cycles transfer

The full consecutive-rank incidence graphs are connected. Their edge counts give the exact slack identities pₙ = Uₙ−bₙ and bₙ−bₙ₋₁ = r pₙ₋₁+pₙ₋₂−pₙ.

Choose a singleton witness a_z for each supported z. The common-cover identity supplies upper vertices joining that witness to the other successors of z. Their complete stars form a tree with precisely those terminals. Different supported centers cannot share an internal upper vertex: that would give a common successor to witnesses whose predecessor sets are disjoint.

Consequently all these tree replacements coexist inside the next incidence graph. They preserve the terminal connections and change edge and vertex counts equally, including a one-terminal tree. Retaining all remaining terminal isolates preserves the component count too. Their union therefore has cycle rank qₙ, so the next full graph has at least that cycle rank. The argument works for arbitrary witness choices; finite checks supplement the written proof.

## When the local recurrence and equality follow

If every z ∈ Pₙ₋₂ has at least one singleton successor in Pₙ₋₁, then Hₛ is the whole preceding incidence graph and qₙ = bₙ₋₁. The theorem then gives pₙ ≤ r pₙ₋₁+pₙ₋₂ for every admissible next extension. In particular, the condition holds whenever rank n−1 was formed by reflection-extension; rank n need not itself be reflected.

For n ≥ 3, suppose every such z has at least two distinct singleton successors. Equality in the local bound holds if and only if the extension to rank n is reflection-extension, up to relabelling that new rank. The two-singleton and n ≥ 3 hypotheses belong to this equality statement; one witness alone is not asserted to characterize equality.

Gaetz–Venkataramana’s established rank-one two-singleton lemma supplies these hypotheses at rank three. Hence for every positive integer r, p₃ ≤ r p₂+r, with equality precisely when rank three is obtained by reflection from rank two. The lemma is credited, rather than presented as new.

## Two classical examples and the sharp coefficient

Wagner reflection adds one upper vertex over each previous neighborhood and r singleton successors over each current element. It preserves the ordinary differential-poset identities and can be repeated indefinitely. The following are classical reflected Young-prefix constructions, used here as witnesses rather than new poset families.

For r = 3, take the Y³ prefix with ranks (1,3,9), reflect to obtain rank size 30, and continue reflecting. Here q₃ = b₂ = b₃ = 1: Byrnes’s bound 31 is reduced to the attained bound 30.

For r = 1, take Young’s lattice through rank five, reflect twice, and continue reflecting. The ranks are (1,1,2,3,5,7,12,19), with q₇ = b₆ = b₇ = 1. Byrnes’s bound 20 is reduced to the attained bound 19. Both finite prefixes therefore belong to infinite differential posets.

In each example pₙ = Uₙ−qₙ with qₙ = 1. Replacing coefficient one by any real c > 1 would demand pₙ ≤ Uₙ−c qₙ < pₙ. Coefficient one is sharp; this does not claim optimality among all possible uses of preceding incidence data.

## The remaining gap and boundary cases

The unremoved allowance is exactly bₙ₋₁−qₙ. In Young’s lattice at n = 6, b₅ = 1 and q₆ = 0: the refined bound is 13, the proposed local bound is 12, and the actual rank size is 11. This is not a counterexample to the local recurrence. The general recurrence would still require bₙ ≥ bₙ₋₁.

At n = 2, q₂ = 0 and p₂ ≤ r²+1. For r = 1 the replacement may be a single terminal with no internal vertex. Empty S leaves all Pₙ₋₁ vertices isolated and gives qₙ = 0; b₁ = 0 and no b₀ is assumed.

The result does not prove the general local recurrence, improve the global Fibonacci envelope, or provide a combinatorial strict-growth proof. The usual strict-growth statement also has the bottom exception r = 1 with p₀ = p₁ = 1. Weighted or multiple-edge graphs, merely modular commutation and isolated locally commuting layers without a valid bottom rank are outside the theorem.

Historical firstness, independence from unknown work and present worldwide openness are not established. The source comparisons are bounded, with version and access limits; a later proof, uninspected publisher edition or unpublished work is not ruled out.

## Context and credit

Majumder’s contribution in Oberwolfach Report 23/2018, printed pages 1452–1453, separately asks for an improvement of Byrnes’s cumulative inequality toward the local bound and for a combinatorial strict-growth proof. This note addresses the improvement request in an incidence-dependent form; the request imposes no rank-number-only restriction.

Stanley’s operator framework and Wagner reflection, Byrnes’s cumulative bound and earlier cycle arguments, and Stanley–Zanello’s incidence and hypergraph sums are established background. Cycle-space inclusion and terminal-preserving tree replacement are elementary graph facts. The assertion here is their simultaneous singleton-supported transfer in the ordinary differential-poset setting.

Singleton and crown methods also have Lewis and Miller–Reiner antecedents. Gaetz–Venkataramana’s Proposition 3.4 in the inspected v3 preprint is the exact rank-one lemma used above. Qing and Wright concern related upper-extremal scopes; Miller’s strict-growth work is a different direction. Versioned preprints and the published records are distinguished in the source dossier; no unread final-body identity or exhaustive literature coverage is inferred.

## Read the paper

Read the complete unchanged seven-page published paper below, or open and download the original PDF. The complete source-and-verification ZIP includes the editable manuscript, authored supporting history and optional exact finite checks. The universal theorem and infinite realization rest on the written proofs.

[Open or download the complete PDF](supported-cycle-bound.pdf) · [Complete original ZIP](supported-cycle-source-and-verification.zip) · [BibTeX](citation.bib)

## Collaboration

Independent verification of the transfer and equality arguments, a substantive primary-source comparison, or work toward a journal submission would be welcome. Any eventual authorship would reflect actual mathematical or writing contributions agreed together.

## AI assistance and review status

AI tools were used extensively in planning, mathematical exploration and proof development, exact computation and code, source research, writing, editing and adversarial checking. Alec Kriebel is the named human author. This is an unrefereed preprint, without conventional independent human peer review, journal acceptance or formal proof-assistant certification. Internal AI checks do not supply those certifications.

## Rights

Original authored prose and mathematical exposition are licensed CC BY 4.0. The companion code has its separate MIT license. The complete ZIP contains these different instruments; no single blanket license is assigned to that mixed archive. Cited third-party works retain their own rights.

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) · [MIT License](https://opensource.org/license/mit/)

## Related literature

- [Majumder: Rank sizes of Differential Posets](https://doi.org/10.4171/OWR/2018/23). Printed improvement request and separate strict-growth question, pages 1452–1453.
- [Byrnes: Structural Aspects of Differential Posets](https://conservancy.umn.edu/server/api/core/bitstreams/45a1bae8-402f-42a7-ad67-4caa7b55d104/content). Chapter 5: cumulative bound, global envelope and separate local conjecture.
- [Stanley: Differential posets](https://doi.org/10.1090/S0894-0347-1988-0941434-9). Ordinary category and classical Wagner reflection, Proposition 6.1.
- [Stanley–Zanello: On the rank function of a differential poset](https://doi.org/10.37236/2258). Remark 8 and the earlier incidence/dimension counts.
- [Gaetz–Venkataramana: Path counting and rank gaps in differential posets](https://arxiv.org/abs/1806.03509v3). Proposition 3.4 of the inspected v3 preprint: the credited rank-one two-singleton lemma.
- [Lewis: On Differential Posets](https://bpb-us-e1.wpmucdn.com/blogs.gwu.edu/dist/5/693/files/2018/04/JBLHarvardSeniorThesis-20drube.pdf). Section 3: earlier singleton and reflection context.
- [Miller–Reiner: Differential posets and Smith normal forms](https://arxiv.org/abs/0811.1983v1). Versioned preprint and earlier singleton techniques.
- [Qing: Differential Posets and Dual Graded Graphs](https://web.math.utk.edu/~yqing/MasterThesis.pdf). Related upper-extremal investigation, Chapters 2–3.
- [Wright: Maximal Extensions of Differential Posets](https://math.mit.edu/research/highschool/primes/materials/2019/conf/9-1-Wright.pdf). Related upper-extremal talk; not an assumed full later proof.
- [Miller: Differential posets have strict rank growth](https://arxiv.org/abs/1202.3006v1). Versioned preprint on the separate strict-growth direction.

## Citation

Alec Kriebel. A singleton-supported cycle correction to Byrnes's differential-poset bound. Version 1.0.0. Zenodo, 22 October 2026. doi:10.5281/zenodo.23578142.
