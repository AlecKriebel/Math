# Source-scope and prior-art adjudication: crossing-number certificates

Target: OWR-822-007 / 30000215, queue rank 1782. Date: 14 October 2026.

## Decision

**The accepted uniform certificate for the specified four-ray drawings of K(3,n) and K(4,n), for every n >= 3, answers the original existential question affirmatively at exactly that family-specific scope.** A complete classification and unrestricted K(m,n) are not acceptance requirements in the primary source.

This does **not** establish a first historical affirmative answer. Published theory already supplies nonplanar positive cases. Nor does this review establish novelty of the family formulas, proof mechanism, or exposition. The appropriate description is a direct, independently checked theoretical verification for two explicit infinite families, with prior ingredients credited.

This document adjudicates source scope and attribution. It is not an additional mathematical proof or a replacement for the separately pinned proof audit. That audit accepts the final proof, SHA-256 `6ec0d8fbf2e583e02fd775e24be762144d09ae3e8de9a835a80856e27527746e` (15940 bytes), with no outstanding acceptance issue.

## 1. Primary-source coverage

Székely's original question is: “Are there graphs for which such a criterion can be verified with more theoretical tools?” It occurs in §2, printed p. 983 / PDF p. 59 of *Discrete Geometry*, OWR 17/2005. A Zarankiewicz drawing is suggested as a candidate. The question does not say “all complete bipartite graphs,” require an exhaustive classification, or prescribe a complexity class. [Official source](https://ems.press/content/serial-article-files/45990?nt=1), [publisher record](https://ems.press/journals/owr/articles/822).

The submitted result supplies a structured nonplanar family, a specified drawing for every parameter, and a uniform argument for all simultaneous assignments of the vertex sets A_e. Its crossing counts increase without bound. Those are substantive affirmative examples of the kind requested, rather than vacuous planar instances or a renamed exhaustive search. This assessment concerns the original existential wording. Broader ambitions suggested by a “which graphs” formulation remain separate.

The claimed result is confined to the explicit nice four-ray drawings of K(3,n) and K(4,n), n >= 3. It does not certify every drawing of either graph, establish the criterion for unrestricted K(m,n), classify every graph admitting a certificate, or supply a general efficient decision algorithm.

## 2. Exact invariant and proof coverage map

Székely's published 2008 Theorem 1, printed p. 33, equates the universal set-system inequality with independent-odd optimality for normal drawings; niceness additionally gives ordinary-crossing optimality. Definitions occur on pp. 32–33 and the motivation for structural verification on p. 34. The comparison class for independent-odd crossing number permits adjacent crossings and repeated crossings. An ordinary- or pair-crossing optimum alone is not the required lower bound. [Published paper](https://amc-journal.eu/index.php/amc/article/download/43/30), [DOI](https://doi.org/10.26493/1855-3974.43.506).

The proof under review addresses the stronger, exact condition directly. Its sections have the following acceptance roles; this is a coverage index, not a new derivation:

- Section 2: unordered independent edge pairs, unrestricted simultaneous A_e assignments, and the equivalence of the requested inequality with wt(c xor p) >= wt(c).
- Section 3: integer coordinates, exact crossing pairs and counts, no adjacent or repeated pair crossings, and no triple interior intersections for m = 3,4.
- Section 4: baseline K(3,3) parity and a coefficient identity in all permitted incidence variables simultaneously.
- Section 5: the K(3,n) bound via a triangle-free complement and the included proof of Mantel's bound.
- Section 6: restriction of assignments and exact multiplicity two in the four K(3,n) subgraphs of K(4,n).
- Section 8: the source criterion and iocr/cr consequences, in that logical order.
- Section 9: attribution and limitations.

The accepted formulas are iocr(K(3,n)) = cr(K(3,n)) = q(n) and iocr(K(4,n)) = cr(K(4,n)) = 2q(n), where q(n) = floor(n/2) floor((n-1)/2). They are consequences of the all-assignment certificate, not premises substituted for it.

## 3. Established positive cases must remain visible

Pelsmajer, Schaefer and Štefankovič's *Removing Even Crossings*, Theorem 1.2 and Remark 1, explicitly records the strong Hanani–Tutte theorem and credits Székely for iocr(K(3,3)) = iocr(K(5)) = 1. Together with nice one-crossing drawings and the published equivalence, these already give positive nonplanar instances. [Author manuscript dated 4 October 2006, PDF pp. 3–4](https://ovid.cs.depaul.edu/documents/tutte.pdf), [final article DOI](https://doi.org/10.1016/j.jctb.2006.08.001).

Their later *Removing Independently Even Crossings*, Theorem 3.1, printed p. 384, proves iocr(G) <= 2 implies iocr(G) = cr(G). It follows that a known nice ordinary-optimal drawing with cr(G) <= 2 satisfies the exact criterion. The superficially similar “at most three” result for ocr must not be relabeled as an iocr theorem. [Author-hosted published-layout paper](https://www.cs.rochester.edu/~stefanko/Publications-new/J20.pdf), [DOI](https://doi.org/10.1137/090765729).

There is also a previously recorded four-crossing example, GP(12,4). The relevant primary paper is Fiorini and Gauci, *The crossing number of the generalized Petersen graph P[3k,k]*, *Mathematica Bohemica* 128 (2003), 337–347. The current source review does not audit or extend that paper's proof. It records the existing bibliographic lead; no general iocr claim for GP(3k,k) is made. [Primary article record](https://dml.cz/handle/10338.dmlcz/134001), [author-institution full text](https://www.um.edu.mt/library/oar/bitstream/123456789/120845/1/The%20crossing%20number%20of%20the%20generalized%20Petersen%20graph%20P%203k%20k%202003.pdf).

## 4. Classical provenance of the family argument

The four-ray drawing and its crossing counts are classical Zarankiewicz constructions. Eppstein's *The Effect of Planarization on Width*, Lemma 1, printed pp. 466–468, presents the K(3,n) **pair-crossing** formula and credits the argument to Zarankiewicz, in an adaptation from Kleitman. Its stated theorem is not an iocr formula. It is relevant precedent for both the drawing and the local-subgraph counting mechanism, and must not be presented as new infrastructure. [Primary paper](https://jgaa.info/index.php/jgaa/article/download/paper468/2483/2290), [DOI](https://doi.org/10.7155/jgaa.00468).

Norine's *Pfaffian graphs, T-joins and crossing numbers*, Theorem 4.2, explicitly attributes parity invariance of the total independent crossings of odd complete and odd-by-odd complete bipartite graphs to Kleitman. Theorem 4.3 states the strong Hanani–Tutte obstruction. These are on PDF pp. 8–9 of the author manuscript, whose drawing convention allows finitely many proper crossings rather than requiring nice drawings. [Author manuscript](https://www.math.mcgill.ca/snorin/papers/pfjoins.pdf), [publisher DOI](https://doi.org/10.1007/s00493-008-2150-2).

The submitted proof gives its K(3,3) parity identity directly for the all-A_e algebraic switches, so it does not need to assume these topological results. That self-contained presentation does not erase their historical relevance. Mantel's bound is likewise an established theorem, with its proof supplied in the submission.

Norine's dissertation §4.4, pp. 99–101, has an independent-odd hypergraph reduction (Lemma 4.4.5) and a further conjectured extremal estimate (Conjecture 4.4.6). It is not a proved unrestricted certificate. [Primary dissertation](https://harrell.math.gatech.edu/GP/Dissert/NorineS05.pdf).

## 5. Bounded search and current-status boundary

The recovered primary papers and targeted searches did not locate an explicit published all-A_e certificate or explicitly stated iocr formula for the full K(3,n)/K(4,n) families. The searches included variants of “independent odd crossing,” “K3,n,” “K4,n,” “K_{3,n},” “iocr,” and “CR-IODD,” as well as the identified parity and pair-crossing sources. This is a bounded search outcome only. It cannot establish that the formulas or argument are unpublished, unknown, or novel.

In particular, the readily available classical ingredients and the close pair-crossing proof make a priority claim inappropriate without substantially more historical research. No such research is required to accept a correct, honestly attributed family certificate.

The inspected September 2026 complete-bipartite manuscript claims an ordinary point-count crossing formula. It is not used as a proof input here and is not treated as establishing the independent-odd or all-A_e statement. This review performs no audit of that manuscript. [Public manuscript at a fixed repository revision](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/The-crossing-number-of-complete-bipartite-graphs-September-23-2026/paper.pdf).

Thus “general K(m,n) unresolved” in this packet means **not established by this submitted result or this review**, not a certified statement of global current openness.

## 6. Recommended queue disposition

Recommended status token: **claimed_solved**, with a qualified finding. This retains a distinction between an accepted internal mathematical review and an unqualified externally verified resolution. If the queue separately records source-history status, the literal existential should also be identified as having prior affirmative cases; the family submission must not be labeled the first solution.

Recommended Turns: **1/5**, subject to the authoritative attempt record. Source recovery, source-scope adjudication and a provenance-only amendment do not justify incrementing the mathematical-pass count.

Recommended Findings text:

> 2026-10-14: Verified affirmative family for the original existential question. Direct all-A_e certificates for the explicit nice four-ray Zarankiewicz drawings of K(3,n) and K(4,n), every n >= 3, give q(n) and 2q(n), q(n)=floor(n/2)floor((n-1)/2); full simultaneous quantifiers, geometry and counting independently audited. Existing nonplanar positive cases and classical ingredients credited; no novelty claim. No classification, arbitrary-drawing certificate, or unrestricted K(m,n) result; broader generality not established here.

Do not use “first affirmative answer,” “previously wholly unanswered,” “Zarankiewicz solved,” or an unqualified “all graphs classified.” Further mathematical passes are unnecessary for closing the accepted literal-existential target; a broader problem would need an explicitly stated broader objective.

## 7. Proof and acceptance pins

The final proof and audit byte hashes are recorded in `PROOF_PINS.json`. Only authored reports and verification metadata belong in this public packet. Source PDFs, extracted source text, dataset contents and private coordination records are excluded.
