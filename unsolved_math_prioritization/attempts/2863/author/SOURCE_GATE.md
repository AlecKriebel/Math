# Source and scope gate

Checked 2026-10-03. Target: UnsolvedMath 2863 / KP-3.65, Kirby Problem 3.65.

## Identification and current scope

- Exact catalogue URL: https://www.unsolvedmath.com/problems/2863 . A direct request returned HTTP 403; the web reader also could not access it. This is not treated as fresh verification of the catalogue's full contents.
- The actual question was independently read in the author-posted 2026 K3 list, printed pp. 178–179: a closed, connected, oriented prime 3-manifold with generic rank-one Kauffman bracket skein module should be S^3 or S^1 x S^2. The tensor product is over Z[A,A^{-1}] with Q(A), not evaluation at a complex parameter and not finite generation over a Laurent polynomial ring.
- Source: https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf . The source's remarks retain the unrestricted question and describe extra-hypothesis results. The result here is therefore not classified as a full literature resolution.
- Numbering correction: K3 points to DKS Question 10.3. The 2025 journal version and arXiv v3 identify the rank-at-least-two question as Question 10.5. DKS 10.3 instead concerns finite generation for closed irreducible non-Haken manifolds. The rank-at-least-two question is stronger than excluding rank one alone, because rank zero is logically another possibility.
- Neither a counterexample nor a complete general proof was found in the bounded source search. This is a report of this search, not certification that no later or unindexed result exists.

## Primary proof reading

### Detcherry–Kalfagianni–Sikora

*Kauffman bracket skein modules of small 3-manifolds*, Advances in Mathematics 467 (2025), 110169; DOI https://doi.org/10.1016/j.aim.2025.110169 .

The local PDF is arXiv:2305.16188v3, dated 13 February 2025: https://arxiv.org/abs/2305.16188v3 . The author-hosted final journal PDF was readable through the web reader at https://users.math.msu.edu/users/kalfagia/skein.pdf ; a direct download at that address instead returned a short HTML challenge, not a usable PDF. The local arXiv PDF, rather than that HTML, is the detailed proof source.

Read completely for the used routes:

- Section 2, including the root-of-unity character bound, its irreducible/central/noncentral-abelian cases, and the finite-character separation argument.
- Section 3, including the specialization argument and the cyclic-decomposition/tameness assumptions.
- Theorems 4.2 and 4.3 with their proofs, including the corner-coefficient requirement and excluded Dehn-filling slopes.
- Section 9's evaluation-map statement, rational-homology-sphere nonvanishing input and proof of Theorem 1.7.
- Section 10's open-question statements and the conditional Floer comparison.

Important distinctions maintained in the proof package:

1. The root-of-unity lower bound is used at each specialization; it is not asserted directly for the generic module.
2. A character is a closed point of the character space, not an arbitrary representation up to conjugacy.
3. No reducedness assumption is needed for the lower bound used here.
4. The relevant torsion quantity is T/pT, not the total p-primary length. A cyclic module R/(p^e) has a one-dimensional residue fiber for every e>=1.
5. The argument here does not need the upper bound in DKS Theorem 3.1 or any asserted identity involving the total primary length.
6. At N=1 the character-ring description is used directly, avoiding low-order quantum-normalization issues.

The root-of-unity proof itself imports major results about surface skein algebras and non-semisimple quantum invariants. Those earlier external proofs are not independently re-proved or formally certified by this packet. The DKS result is an attributed theorem input.

### Zentner

*Integer homology 3-spheres admit irreducible representations in SL(2,C)*, Duke Mathematical Journal 167 (2018), 1643–1712; DOI https://doi.org/10.1215/00127094-2018-0004 . The complete author manuscript was retrieved from https://zentner.app.uni-regensburg.de/splicing.pdf .

Theorem 9.4 and the whole final Section 9 proof, including the degree-one domination reduction and the Seifert/hyperbolic cases, were read. The preceding splicing theorem and its gauge-theoretic foundations are imported results here; this is not a line-by-line verification of all 71 pages or all cited predecessors. The precise theorem used excludes S^3. No SU(2) theorem for all homology spheres is substituted for the published SL(2,C) theorem.

### Kitaeff

*The Gilmer-Masbaum map is not injective on the skein module*, New York Journal of Mathematics 32 (2026), 423–435: https://nyjm.albany.edu/j/2026/32-20.html and https://nyjm.albany.edu/j/2026/32-20p.pdf .

The statement and complete relevant proof of Theorem 1.10 were read through the displayed basis argument (Section 2) and the q-even evaluation calculation (Section 3). Its nonzero-skein assertion relies on Kinnear's imported dimension result; that paper is not independently recertified here. Only the proven failure of universal evaluation-map injectivity is used, not any claim that these mapping tori have rank one. The included checker tests the scalar cancellation in the formula, not topological nonvanishing of the element.

## Existing-repository work check

Before these attempts, the public AlecKriebel/Math queue recorded rank 531, ID 2863, KP-3.65 as queued, 0/5. That row alone was not treated as evidence that no work existed.

Additional read-only checks searched all-state PRs for 2863, 3.65, skein, Kauffman and rank-one; searched default-branch code for 2863 and KP-3.65; and checked the problem-specific attempt path. No exact prior attempt or resolving PR was found in those results. The skein search found PR 180, which concerns a different higher-genus torsion question, not rank-one recognition. Default-branch code search can be incomplete, and the recursive tree request failed twice with a transport error; the search is not a proof of historical nonexistence.

## Gate decision

**Proceed only as an unsolved, scoped partial-research packet, five substantive approaches.** The proof contains an elementary module lemma and conditional deductions from credited published theorems. No novelty, unrestricted solution, topological counterexample, exhaustive literature clearance, or formal verification of external topology is claimed.

The source PDFs, source screenshots, full extracted texts and raw search responses are not part of the public package. In particular the K3 author PDF is not reposted.
