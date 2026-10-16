# Exact source and prior gate: 30004047 / OWR-16763-021

## Exact bundled question

Let x,y lie in (0,1]. Consider every finite simple graph with three disjoint nonempty parts A,B,C, retaining only A--B and B--C edges. Require only

- every a in A has at least x|B| neighbors in B;
- every b in B has at least y|C| neighbors in C.

For c in C, N_A^2(c) denotes the distinct A-vertices reached by a two-edge path through B; path multiplicity is not counted. Define

phi(x,y)=inf_G max_(c in C) |N_A^2(c)|/|A|,

where the infimum ranges over all finite admissible graphs. This is the largest universally guaranteed fraction; no attainment of the infimum is presumed. The imported short statement omits the universal-over-graphs clause, which the primary source explicitly supplies.

The two bundled assertions are:

1. Does phi(x,x)>=1/2 hold whenever x>1/3?
2. More generally, for every integer k>=1, do x+ky>1 and kx+y>=1 imply phi(x,y)>=1/k?

The second includes the first with k=2. Strict and weak inequalities are retained exactly. All real parameters in (0,1] are included. No lower degree from B to A or from C to B is assumed.

The complete primary contribution is Paul Seymour, joint with Chudnovsky, Scott and Spirkl, *Concatenating bipartite graphs*, OWR 1/2019, printed pp.46--47, PDF42--43. Both pages were visually inspected. Official PDF: https://ems.press/content/serial-article-files/46780 . Publisher record: https://ems.press/journals/owr/articles/16763 , DOI 10.4171/OWR/2019/1. The report volume/year is 16 (2019), pp.5--63; actual publication was 27 February 2020. Those dates are distinct and consistent with the imported citation.

## Later primary paper and credited results

The detailed publication is Chudnovsky, Hompe, Scott, Seymour and Spirkl, *Concatenating Bipartite Graphs*, Electronic Journal of Combinatorics 29(2) (2022), P2.47, DOI 10.37236/8451, published 3 June 2022. Published PDF: https://www.combinatorics.org/ojs/index.php/eljc/article/download/v29i2p47/pdf/ . Its finite-simple-graph definitions are on pp.2--4, the weighted version in Theorem 2.1, and the exact general assertion remains Conjecture 5.1 on p.21. The relevant definitions, theorem statements and proofs in Sections 2, 5 and the mono-constrained part of Section 6 were inspected.

Known inputs to credit:

- Theorem 2.3 proves phi(x,y)=phi(y,x); this is a proved fact about phi, not the previously attempted symmetry question for psi.
- Theorem 1.8 gives phi>=max(x,y); Theorem 1.9 gives the cyclic upper bounds. Reciprocal diagonal values and the jump bounds are known.
- Theorem 5.2 proves the k=1 case. Theorem 5.3 gives the stronger-than-3/7 lower bound just above the one-third diagonal.
- Theorem 5.5 uses a random k-vertex covering certificate. It is only a sufficient condition, not a characterization.
- Theorem 6.6 proves phi(x,y)>=1/2 if 2x^2y>=(1-x-y)^2. Together with symmetry this includes its transpose. In particular the paper records the diagonal threshold approximately 0.352202, which does not cover every x>1/3.
- Theorem 4.2 proves the full integer-k implication for the stronger biconstrained function psi. It cannot be used as a proof for phi after dropping two hypotheses.

The earlier arXiv1902.10878v3 is dated 7 December 2020; it is not a new post-2022 resolution. Patrick Hompe's separate arXiv1908.07453v3 was withdrawn on 23 June 2022, with the stated reason that the results were edited and incorporated into the joint paper. The current primary arXiv pages and Seymour's publication list were checked. Bounded current exact-title/conjecture searches located no verified complete resolution; this is not a novelty certificate or an exhaustive literature claim.

## Prior research and the neighboring symmetry target

The requested problem URL https://www.unsolvedmath.com/problems/30004047 returned an internal retrieval error. The authorized fallback is ulamai/UnsolvedMath, pinned revision 37e53eabe540fb458758e198be61634bd02ee008. Both complete cached JSON files were checked byte-for-byte by length and SHA-256 against the repository manifest. The exact record was read; its prior research report under OWR-16763-021 is null.

Live exact-ID PR and branch searches are empty. Live target-path commit history is empty; default-branch code search finds only assignment metadata. All-ref message/path searches across 487 mirrored refs found no exact target attempt. Catalog row 409 is eligible, queued 0/5, with no holds; the related-target-groups file contains no matching group. Repository AGENTS and queue-specific research instructions were read.

The adjacent completed target 30004048 asks whether the **biconstrained** function psi is symmetric. Its unique draft PR364, https://github.com/AlecKriebel/Math/pull/364 , was read at head 0d07b06537aded3e76f5a71908f3546df574a691, together with its full source scope and final result. It gives a reviewed negative psi-symmetry answer on a rational boundary, while retaining all four degree constraints. That theorem is not the one-direction threshold assertion here. Its rational-weight and finite-blow-up framework is related background, not a new author contribution to be recounted. No exact prior attempt of the present target was found, so a distinct five-turn budget applies.

Raw source PDFs, renders and imported JSON remain local-only. Research checkpoints contain only original exposition, controls and source bindings. Source review uses zero substantive author turns; fresh proof work is recorded separately.
