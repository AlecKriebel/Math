# Exact source and known-result boundaries

Audit date: 2026-09-30 UTC. The full original target remains unresolved by this work. No historical priority is asserted for the deductions or examples.

## Original definition

Niven Achenjang's contribution *On the Brauer Groups of Stacky Curves* appears in *Explicit Methods in Number Theory*, OWR 40/2024, printed pp.2336–2339, published in 2025. Question 1 is on p.2337. The complete report was retrieved; the question and its stated partial theorem on pp.2337–2338 were visually inspected. The source defines a stacky curve as a separated finite-type algebraic stack, pure of dimension one, with finite inertia, and defines its Brauer group as the torsion subgroup of H²_et(Gm).

Thus the target does not require a proper or smooth curve, Deligne–Mumford inertia, or trivial generic stabilizers. Tameness is the Abramovich–Olsson–Vistoli linearly-reductive-inertia condition. Connected diagonalizable group schemes in positive characteristic are allowed. The characteristic-not-two restriction in the motivating modular examples is not imposed on Question 1 itself.

The source already announces a restricted locally-Brauerless result. Its later setup additionally assumes a smooth coarse curve, an iterated root stack along points, and a gerbe banded by a finite commutative linearly reductive group. The generic band and its Cartier dual are explicit; they cannot be replaced by merely a list of isolated orbifold orders.

Original report: https://ems.press/content/serial-article-files/50042

## Current primary literature read

1. **Niven Achenjang, *On Brauer groups of tame stacks*, arXiv:2410.06217v3, 19 July 2025.** The complete current preprint was retrieved. Its conventions, local quotient statement (Corollary 2.16), classifying-stack calculation (Propositions 3.8–3.9), connected-inertia calculation (Proposition 4.3), exact local sequence (Proposition 4.4), and locally-Brauerless theorem (Theorem 4.14) were checked, including the relevant proofs. Theorem C and the Section 7 restrictions were checked for scope. Proposition 4.3's p-primary Picard group makes the connecting arrow in Proposition 4.4 vanish when mapping into the prime-to-p finite-group H² term; this yields the local calculation used in our generically schematic partial theorem. The original report's in-preparation reference now has this full preprint, but no claim of a complete arbitrary-stack classification is made. https://arxiv.org/pdf/2410.06217v3
2. **Martin Bishop, *Brauer groups of tame stacky curves and their μr-gerbes*, arXiv:2507.08780v2, 24 July 2025.** The complete current preprint was retrieved. Convention 1.3 explicitly uses tame separated Deligne–Mumford stacks and defines “stacky curve” with trivial generic stabilizer. Proposition 3.7 computes all H^j for j≥2 in that class, using finite-support Leray and Theorem 2.7's curve vanishing. The full proof of this proposition was checked. Theorem 4.9 adds μr-gerbes and gives an exact sequence with additional root-gerbe, inflation and splitting conditions; Corollary 4.11 covers the smooth base case. These results are substantial credited progress, but their conventions are narrower than the original question. We do not silently allow μp-gerbes in characteristic p under Bishop's tame DM convention. https://arxiv.org/pdf/2507.08780v2
3. **Bishop–Newman, *Tame nodal stacky curves*, arXiv:2509.20629v3, 15 June 2026.** The complete current preprint was retrieved. Section 1.2 assumes proper, geometrically connected tame Deligne–Mumford curves with trivial generic stabilizer and split nodes. Theorems stated as Propositions 4.13 and 5.10 compute nodal Brauer contributions. Those statements and the reference back to Bishop's Proposition 3.7 were checked for scope; the full nodal classification proof was not recertified. This does not handle arbitrary generic inertia or arbitrary singularities in the original class. https://arxiv.org/pdf/2509.20629v3
4. **Rose Lopez, *The Brauer group of BG and gerbe structures of moduli spaces*, arXiv:2601.05370v1, 8 January 2026.** The complete preprint was retrieved. Theorem 1.1 concerns a smooth connected semisimple linear algebraic group over an algebraically closed field; its later applications calculate specified moduli gerbes. The main statements were checked for scope. This is not an arbitrary finite-inertia curve theorem, and the full moduli computations were not audited. https://arxiv.org/pdf/2601.05370v1
5. **Stacks Project, Tag 0ADD.** A separated locally Noetherian algebraic space is a scheme at every point where its local dimension is at most one. The complete statement and proof were read. This supplies the schematic coarse curve used in the partial theorem. https://stacks.math.columbia.edu/tag/0ADD

These are precise use-and-scope checks. Except for the explicitly identified relevant proofs, they do not claim to recertify entire research papers. The Achenjang and Bishop versions used are preprints; their mathematical inputs are credited as such.

## What the partial formula computes

For a dense schematic open, the formula reduces to finitely many Schur multiplier groups H²(Q_i,k×), where Q_i is the étale quotient of the actual stabilizer group scheme. These are determined by finite-group multiplication tables, for example by the normalized bar resolution and integer Smith normal forms for the Schur multiplier. No unresolved geometric transgression remains in that restricted case. In the DM subclass the formula is already Bishop's degree-two computation.

By contrast, with generic inertia the higher direct images need not have finite support. The two proper μℓ²-gerbe examples in PARTIAL.md demonstrate that even fixing the coarse curve and every stabilizer isomorphism type does not fix the answer. Their global gerbe classes differ. The characteristic-p example A¹×Bμp lies within the broad original tame Artin definition and has a fully explicit infinite p-primary Brauer group. It is a direct use of Achenjang's Proposition 3.9 and the Artin–Schreier sequence, not a new general classification.

All computations use the source's cohomological Brauer convention. No global theorem identifying it with every Azumaya Brauer group is imported merely from terminology in another paper.

## Prior-attempt and duplicate gate

The dedicated branch started at remote main c6975ca76f9f667f1250ba403d0e6da2aafe14d0. The queue showed rank 156, queued 0/5. Searches of 134 all-state PRs, exact remote branch names, all fetched attempt-path history, state and related-target groups found no previous problem-specific attempt or publication. The full pinned dataset gave no second record with a Brauer-and-stacky-curve statement. The source-code-keyed upstream report is null; the local desk note only proposes Leray/stabilizer cohomology and asks whether later work already covers the exact target.

The UnsolvedMath landing page was unavailable through the web tool, so the authorized pinned record and its complete original source were used. All later source checks preserve the exact original scope.

Dataset attribution: *UnsolvedMath: A Curated Collection of Open Mathematics Problems*, UnsolvedMath Contributors (2026), https://huggingface.co/datasets/ulamai/UnsolvedMath, revision 37e53eabe540fb458758e198be61634bd02ee008. Curation and metadata: CC BY 4.0. Original sources retain their own licenses. Source PDFs and rendered pages are kept outside the public attempt package; hashes are in source_manifest.json.

## Remaining status

Three substantive approaches produced restricted formulas and scope diagnostics. No general computation of generic bands, transgressions and extension data was obtained. The bounded current-literature search found no verified full coverage of the original arbitrary class; this does not certify that no later answer exists. Recommended campaign status: unsolved, 3/5. Independent adversarial review is required before any PR.
