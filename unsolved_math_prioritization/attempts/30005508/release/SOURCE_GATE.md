# Source, scope, and prior-attempt gate

## Exact source and scope

The problem landing page https://www.unsolvedmath.com/problems/30005508 was attempted first on 3 October 2026 and could not be accessed. The pinned catalogue record supplied the statement and original-report citation. The primary report was then inspected directly:

- *Representations of Finite Groups*, Oberwolfach Report 19/2023, DOI [10.4171/owr/2023/19](https://doi.org/10.4171/owr/2023/19), Benjamin Sambale's contribution, printed pages 1055–1056. Conjecture 4 is precisely the local restriction-multiplicity formula. The report's Theorem 3 concerns the different nilpotent-indicator Conjecture 2; it is not a theorem proving Conjecture 4.
- Official report PDF: https://ems.press/content/serial-article-files/47014?nt=1 . Author's contribution: https://benjaminsambale.github.io/pdfs/owr23.pdf .
- Benjamin Sambale, *Real characters in nilpotent blocks*, Vietnam Journal of Mathematics 52 (2024), 421–433, [DOI 10.1007/s10013-023-00623-5](https://doi.org/10.1007/s10013-023-00623-5); [arXiv:2301.13440](https://arxiv.org/abs/2301.13440). Conjecture C is an aggregate projective-indicator assertion. Theorems 13–14 explain its relation to subsection square counts and the nilpotent-indicator conjecture. Theorem E establishes its stated nilpotent solvable case, not the general orbit-by-orbit assertion.
- Benjamin Sambale, *Real blocks with dihedral defect groups revisited*, Bulletin of the Australian Mathematical Society 109 (2024), 327–341, [DOI 10.1017/S0004972723000436](https://doi.org/10.1017/S0004972723000436). Published Conjecture 3.2 is the orbit-by-orbit involution formula; Theorem 3.3 derives the scalar formula. Lemma 4.1 gives the square-root permutation-module interpretation and a vanishing criterion. Proposition 4.2 proves an aggregate local identity for nilpotent abelian local defect. The paragraph immediately after it raises the local orbit-by-orbit formula. In the author's March 2023 PDF, these are Conjecture 5, Theorem 6, Lemma 7, and Proposition 8. Numberings must not be mixed.

Primary publisher page: https://www.cambridge.org/core/journals/bulletin-of-the-australian-mathematical-society/article/real-blocks-with-dihedral-defect-groups-revisited/FF706EC9D2BBB0BA351DFD64B16C6276 . Author PDF: https://benjaminsambale.github.io/pdfs/FSdihedral.pdf .

The current author publication list at https://benjaminsambale.github.io/subpages/pub.html and targeted searches for the exact conjecture and projective/involution terminology were checked. No general resolution was found. This is a bounded search result, not proof that no resolution exists.

## Terminology and exclusions

A B-subsection uses a 2-element x. Therefore every square root y is a 2-element and C_G(y)≤C_G(x). The right-hand intersection is with the conjugacy class in C_G(x), not in the full group unless x=1. The local block b need not be real; the nonreal case has a known vanishing argument described in Approach 1. “One simple module” is not interchangeable with “nilpotent block”; Approach 5 deliberately tests a nonnilpotent example.

The pair (D,E) is an actual defect pair in the given group. Finding one model with the same abstract pair does not transfer restriction multiplicities to an arbitrary block. Likewise, equality of a sum of orbit multiplicities does not imply equality term by term.

## Genuine prior-attempt check

The live `main` queue was read on 3 October 2026. Rank 489 was `queued`, 0/5, with no chat or findings entry. Its then-current queue blob SHA was `c87c275c638939b8008fd58db80657491d14971e`.

Repository searches in AlecKriebel/Math for the exact problem ID, exact code, and projective/square-root terms returned no matching attempt. Exact-ID commit and pull-request searches also returned no matches. The pinned research-results cache had no record matching this ID or OWR code; the catalogue's embedded literature triage was available. These negative searches are qualified by search coverage and do not assert that every private or unindexed attempt was inspected.

No pre-existing proof budget was found to resume. The five substantive approaches recorded here are research attempts, not a claim that five separate external model sessions occurred. No queue-generation script was run and no remote write was made while preparing this packet.

## Attribution

The standard C₃⋊E realization of every defect pair is already in Sambale's discussion after Definition 7 in *Real characters in nilpotent blocks*, and in Proposition 2.2 of the published dihedral paper (Proposition 3 of its author PDF). The square-root permutation interpretation and zero criterion are explicitly attributed above. The order-864 construction is in the same general family as Sambale's nonnilpotent solvable one-simple-module example near the end of the nilpotent-block paper; no identification with its SmallGroup ID and no new-example priority are asserted here. The central-quotient argument and product calculation are supplied for verification without a novelty claim.
