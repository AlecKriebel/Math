# Theoretical certification of crossing-number optimality: source-scope clarification

Date checked: 14 October 2026. Target: OWR-822-007 / 30000215.

This is a source and acceptance-scope analysis. It presents no new proof of a crossing-number formula and makes no novelty claim.

## 1. What the original question requires

The primary source is László A. Székely, “Variants of the Crossing Number Problem,” §2, in *Oberwolfach Report 17/2005*, printed page 983 (PDF page 59). The question is:

> Are there graphs for which such a criterion can be verified with more theoretical tools?

The next sentence proposes the Zarankiewicz drawing of a complete bipartite graph as a candidate. It does not require all complete bipartite graphs, a classification of all graphs, a polynomial-time algorithm, or a previously unknown graph family. The neighboring biplanar and outerplanar sections are separate questions. [Original report](https://ems.press/content/serial-article-files/45990?nt=1)

Accordingly, a rigorous theoretical verification for a specified nonplanar graph, or a nonplanar structured family, can answer the original existential wording. A proof for every member of the families K_{3,n} or K_{4,n}, with the actual universal set-system inequality established, would be within that wording. Such a result must be described at its proved scope. It would not establish the unrestricted Zarankiewicz claim, a complete classification, or novelty.

The curated formulation “For which graphs” invites a useful class description, but does not retroactively add a classification requirement to the primary source. The most ambitious direction explicitly suggested by the source is theoretical verification for Zarankiewicz drawings; it is a proposed example, not a mandatory acceptance condition.

## 2. Exact criterion and established reformulation

Let P(G) be the unordered pairs {e,f} of vertex-disjoint edges. For every edge e, choose an arbitrary A_e contained in V(G) minus its endpoints, and put

p_A(e,f) = (|e intersect A_f| + |f intersect A_e|) mod 2.

For a normal drawing D, let O_D comprise the pairs in P(G) crossing oddly. The full condition is

|{q in O_D : p_A(q)=1}| <= |{q in P(G) minus O_D : p_A(q)=1}|, for EVERY simultaneous assignment (A_e).

Székely's published *An Optimality Criterion for the Crossing Number*, Theorem 1, proves that this condition is equivalent to D minimizing the independent-odd crossing count. If D is nice, it also minimizes the ordinary crossing count. Here “nice” adds no adjacent-edge crossings and at most one crossing per edge pair to the usual finite, transverse, no-triple-crossing conventions. A nice D has O_D equal to its crossing-pair set. [Published paper, pp. 32–34](https://amc-journal.eu/index.php/amc/article/download/43/30), [DOI](https://doi.org/10.26493/1855-3974.43.506)

### Consequences for acceptance

These are interpretations of that published equivalence, not new crossing-number results:

- An ordinary-crossing optimum is not, by that fact alone, an exact certificate for this criterion. The missing requirement is independent-odd optimality.
- For a fixed nice drawing D with c crossings, a theorem proving iocr(G) >= c is enough to invoke the published equivalence and verify every A_e assignment. It is not necessary to reproduce Székely's proof, but the theorem and its hypotheses must be cited correctly.
- At graph level, existence of a nice drawing satisfying the criterion is equivalent to iocr(G)=cr(G). This is a useful reduction, not by itself a theoretical evaluation of either quantity.
- For a graph with iocr(G)<cr(G), no ordinary-crossing-optimal nice drawing can satisfy the universal criterion. This rules out a claim that every ordinary optimum automatically passes.
- A lower bound for odd crossing number, pair-crossing number, independent total crossing number, or ordinary crossing number does not automatically transfer to iocr. These quantities must not be interchanged.

The candidate drawing must be nice. Drawings compared in the definition of iocr need only be normal: repeated crossings and crossings of adjacent edges cannot simply be forbidden in the lower-bound argument. Adjacent pairs do not enter the iocr count, but their possible presence still matters to the class of permitted competing drawings.

## 3. Existing theoretical positive cases

### K_5 and K_{3,3}: legitimate, already known nonplanar examples

Pelsmajer, Schaefer and Štefankovič explicitly record iocr(K_5)=iocr(K_{3,3})=1 and credit Székely's earlier algebraic treatment. Their strong Hanani–Tutte theorem also gives the relevant independent-odd obstruction. Combining these established results with a nice one-crossing drawing and Székely's equivalence supplies exact nonplanar certificates. The application is a literature consequence, not a new solution or new proof.

[Removing Even Crossings, author manuscript dated 4 October 2006, Theorem 1.2 and Remark 1, PDF pp. 3–4](https://ovid.cs.depaul.edu/documents/tutte.pdf). The final article is *J. Combin. Theory Ser. B* 97 (2007), 489–500, [DOI](https://doi.org/10.1016/j.jctb.2006.08.001).

These examples are not excluded by the original wording. Nevertheless, reporting only them as a newly resolved research challenge would conceal the established prior theory and the source's interest in structured verification. A precise report should say that the literal existence question already has known affirmative examples.

### All graphs with at most two ordinary crossings

Pelsmajer, Schaefer and Štefankovič, *Removing Independently Even Crossings*, Theorem 3.1, prove that iocr(G)<=2 implies iocr(G)=cr(G). Thus, as a direct application, any known nice ordinary-optimal drawing of a graph with cr(G)<=2 satisfies the exact criterion. This includes nonplanar cases, not just planar drawings. The certificate still needs the claimed drawing and crossing minimum established. [Author-hosted published-layout paper, printed p. 384](https://www.cs.rochester.edu/~stefanko/Publications-new/J20.pdf), [SIAM J. Discrete Math. 24 (2010), 379–393](https://doi.org/10.1137/090765729)

The “at most three” theorem in *Removing Even Crossings* concerns ocr, not iocr; it must not be substituted for this result.

### A nontrivial four-crossing example already recorded in the literature

Schaefer's live survey records iocr(GP(12,4))=4. Its footnote explains that Fiorini and Gauci's work supplies a skewness lower bound of four and a four-crossing drawing. The same entry records sk(G)<=iocr(G), and hence equality with cr whenever a skewness lower bound matches a drawing. Applying Székely's equivalence supplies another exact-certificate route. This is established-literature application, not a novel certificate claimed here.

The survey warns that the larger family GP(3k,k) cannot simply be assigned the same conclusion: its cited inductive argument appears to depend essentially on ordinary crossing number. [Schaefer, *The Graph Crossing Number and its Variants: A Survey*, live 2026 edition, printed pp. 62–63, especially footnotes 110–111](https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS21/pdf). Its cited paper is Fiorini and Gauci, “The crossing number of the generalized Petersen graph P[3k,k],” *Math. Bohem.* 128(4) (2003), 337–347. The latter full proof was not independently audited in this source-scope review.

## 4. K_{3,n} and K_{4,n}: prior-art boundary

Targeted searches did not locate an explicit published all-A_e certificate, or an explicit iocr formula, for the full K_{3,n} or K_{4,n} families. This is a bounded negative search result, not evidence of novelty.

There is close prior proof infrastructure. Eppstein's *The Effect of Planarization on Width*, Lemma 1, establishes the pair-crossing formula for K_{3,n} by induction using K_{3,3} subgraphs. He credits the underlying argument to Zarankiewicz and an adaptation from Kleitman. It is relevant to the history of the proposed family argument, but its stated conclusion is pair-crossing number, not independent-odd crossing number. [JGAA 22(3) (2018), 461–481, Lemma 1 on pp. 466–468](https://jgaa.info/index.php/jgaa/article/download/paper468/2483/2290), [DOI](https://doi.org/10.7155/jgaa.00468)

A new exposition using parity, a graph-theoretic extremal bound, and an explicit Zarankiewicz drawing could be a genuine exact verification without being a novel numerical crossing-number theorem. Before acceptance, it must prove the independent-odd lower bound for arbitrary normal drawings, or prove the all-A_e inequality directly. The present review has not carried out that proof.

## 5. Norine's distinct route

Norine's 2005 dissertation §4.4, printed pp. 99–101, states a hypergraph reduction toward the independent-odd lower bound for K_{m,n}. Lemma 4.4.5 is proved there; the required universal extremal estimate is Conjecture 4.4.6. Therefore it is an existing reformulation and possible approach, not a proved unrestricted certificate. [Dissertation](https://harrell.math.gatech.edu/GP/Dissert/NorineS05.pdf)

The later article *Pfaffian Graphs, T-Joins and Crossing Numbers* supplies crossing-parity tools, including Kleitman's invariance theorem and Hanani–Tutte, but its recovered text does not include a proof of that conjectural extremal estimate. [Author manuscript](https://www.math.mcgill.ca/snorin/papers/pfjoins.pdf)

## 6. Bounded current-status conclusion

The 2026 complete-bipartite manuscript found during the source search claims an ordinary point-count crossing-number formula. The accompanying inspected scope document defines crossings as spatial points, counting repeated crossings of an edge pair separately; it does not state an independent-odd result. Its manuscript status and claim must be reported as such; an ordinary formula, even if subsequently validated, would not on its own verify the stronger all-A_e criterion. No mathematical audit of that manuscript was performed here. [Public manuscript](https://raw.githubusercontent.com/openai/math/main/preprints/The-crossing-number-of-complete-bipartite-graphs-September-23-2026/paper.pdf), [public scope document](https://github.com/openai/math/blob/main/lean/docs/165.md)

This review located established positive cases and the exact reformulation. It did not locate a verified unrestricted Zarankiewicz all-A_e certificate. That last sentence describes the bounded search outcome, not a declaration that no such result exists.

## 7. Acceptance gates

A proposed positive result should pass every applicable gate:

1. **Exact object.** State the graph or parameterized family, the full parameter range, and the particular drawing or class of drawings being certified.
2. **Drawing conventions.** Establish a simple graph, Jordan-arc edges, the required normality and niceness, and the exact crossing-pair count. Distinguish crossings per pair from distinct geometric intersection locations.
3. **Full quantifier.** Prove the inequality for all simultaneous A_e assignments. Checking singleton assignments, one edge at a time, small n, selected symmetries, or merely necessary parity constraints is insufficient unless a proved reduction covers all assignments.
4. **Correct invariant.** If using the published equivalence, prove the exact independent-odd lower bound in the full class of normal drawings. Do not infer it solely from an ordinary, pair, or odd crossing result.
5. **Theoretical verification.** Give a transparent theorem-level argument. Finite tests may corroborate it, but an exhaustive enumeration alone does not answer the requested methodological question.
6. **No circularity.** Do not assume the same iocr lower bound or all-A_e inequality under another name.
7. **Prior credit.** Separate published theorems, immediate applications of those theorems, and any genuinely new argument. Explicitly disclose known nonplanar existential positive cases.
8. **Scoped conclusion.** A verified nonplanar structured family answers the literal existential question. It is not necessary to prove unrestricted K_{m,n} or a classification. Conversely, do not describe a restricted result as establishing either broader claim.

## 8. Recommended status language

Before a new family proof is verified:

“Source scope clarified. The exact criterion is equivalent to independent-odd optimality. Known theoretical nonplanar examples already answer the bare existence wording; structured family certificates and their provenance require explicit checking. No new proof or unrestricted Zarankiewicz certification is established by this review.”

After a fully verified K_{3,n}/K_{4,n} certificate, an appropriate conclusion would identify those families and state that the original existential wording is affirmatively answered at that scope, while distinguishing established ingredients and avoiding an unsupported novelty or unrestricted-resolution claim.
