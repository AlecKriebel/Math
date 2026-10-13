# Source-target coverage of the exact Jacobian decision construction

Date: 2026-10-13 UTC.

## Verdict

**The accepted theorems cover the literal mathematical question stated on Howe's 2006 IPAM slides, PDF pages 37–38.** A queue label of **claimed_solved**, explicitly qualified as a theoretical exact algorithmic resolution, is supported. Calling the result only a partial theorem because it lacks useful complexity bounds or an implementation would add requirements absent from that source.

This is a source-contract audit of already accepted theorems, not a new proof search or an independent reproof of their dependencies. It makes no novelty, priority, or broad historical-closure claim. The inspection was bounded. [Howe, *Low-genus curves over finite fields: Problems and variations*, pp.29–38](https://ewhowe.com/talks/IPAM.pdf)

## 1. What the source actually requires

The source distinguishes three questions in consecutive slides:

- Pages 29–30 ask whether a threefold isogeny class specified by its Weil polynomial contains a Jacobian.
- Pages 31–32 explain the finite-field descent obstruction; a geometric Jacobian or a Jacobian after arbitrary field extension does not answer the original-field question.
- Pages 33–34 ask how to recognize a supplied principally polarized threefold and raise the question of its representation. Pages 35–36 outline Meagher's modular-form approach and Ritzenthaler's geometric-quadric approach.
- Pages 37–38 specialize to ordinary, absolutely simple threefolds and ask whether **either** recognition approach can be connected to their polarized Deligne-module description to decide Jacobian existence in the isogeny class. The two pages repeat the same mathematical question.

There is no requirement on running time, certificate size, equation degree, numerical precision, practical implementation, or outputting an equation of the curve. There is no requirement to implement both recognition approaches. Nor does the source demand an individual ideal-to-model label, although that is a meaningful strengthening of a set-level connection. No odd-characteristic restriction is stated. [Howe 2006, pp.29–38](https://ewhowe.com/talks/IPAM.pdf)

## 2. Coverage by the aggregate theorem

The accepted manuscript *An exact counted-model connection from Deligne modules to Jacobian recognition* addresses each imposed obligation:

1. **Input and scope:** Section 1 takes an exact finite field and a promised realizable ordinary absolutely simple degree-six Weil polynomial. This is the source's given isogeny class, rather than an additional mathematical restriction. The theorem does not require maximal orders, invertible ideals, or odd characteristic.
2. **Actual use of Deligne modules:** Sections M2 and M6 use the complete polarized Deligne enumeration to compute the exact unweighted number of base-field polarized classes. That number certifies when the exact model enumeration is complete. Module information is essential to its stopping proof and is not merely attached to a separate curve search.
3. **Recognition input:** Sections M3–M5 construct and certify theta-equipped projective models, group laws, polarizations, their Weil polynomial, and polarized deduplication. Part II therefore receives exact algebraic data rather than an unverified period approximation or an assumed realization oracle.
4. **Either permitted recognition approach:** Sections G1–G5 implement the Beauville–Ritzenthaler geometric method. Its geometric hypotheses are established from the input or checked by the construction. This is an implementation of one of the source's permitted approaches at the level of exact computability.
5. **Original-field answer:** Section G6 restricts the quadratic descent character only along odd-degree extensions, preserving its value over the original finite field. The singular-theta branch also returns an original-field Jacobian answer.
6. **Both YES and NO:** Sections M6 and C1 prove finite complete coverage of every relevant principal-polarization orbit, including those on noninvertible ideals. If all models are rejected, a Jacobian elsewhere in the class is excluded. This is a decision algorithm, not only a positive semidecision procedure.
7. **All characteristics:** Section C2 records the characteristic-two and characteristic-three safeguards. The geometric criterion is Beauville–Ritzenthaler Proposition 2.1, Proposition 2.4, Proposition 3.1 and Theorem 3.4; the original-field descent is part of the argument, not inferred from principal polarizability alone. [Beauville–Ritzenthaler](https://arxiv.org/abs/1005.3683v1)

Thus the aggregate theorem already supplies the literal connection sought by the source. Its unlabeled model list is sufficient for the existential question.

## 3. What the marked inverse adds

The independently accepted manuscript *A certificate-search inverse for a marked polarized Deligne ideal* strengthens the connection: its theorem and Sections 5–7 realize a specified polarized ideal and attach the geometric recognition answer to that exact object. The two checked integral matrix identities match Frobenius and the polarization, rather than matching only a Weil polynomial or arbitrarily labeling the aggregate list.

Its full comparison convention is important but is not an unresolved oracle. Section 1 fixes an effective algebraic tower, compatible primes and residue embeddings, and a complex inclusion. These are computable choices defining the Deligne comparison; no candidate may choose a different convention simply to obtain a match. The dependence of a marked Deligne realization on a comparison choice is intrinsic to the equivalence. The existential isogeny-class answer from the aggregate theorem is convention-independent. Deligne's original Sections 3 and 8 are the cited comparison/descent inputs. [Deligne 1969](https://publications.ias.edu/sites/default/files/Number6.pdf)

Accordingly, this convention is neither an extra restriction on the source's Weil-polynomial inputs nor an unmet source obligation. The marked inverse removes even the stronger per-ideal interface concern, though the source did not explicitly demand it.

The separately accepted bounded good-point result replaces the unbounded odd-extension search with a prescribed odd extension degree at most seven. This strengthens one geometric stage. It is not needed for literal coverage, since the aggregate theorem already proves termination, and it supplies no bound on the entire certificate search.

## 4. Bounded primary-literature check

The following nearby results were inspected for an explicit statement of the same complete computability connection:

- **Marseglia**, *Computing square-free polarized abelian varieties over finite fields*, arXiv:1805.10223v3, abstract, Sections 3–6 and Section 8, especially PDF pp.16–17. The established output includes ideal classes, polarizations and canonical-lift period matrices. The inspected material does not state the complete exact model-certificate/recognition composition. These existing contributions must remain credited. [Paper](https://arxiv.org/abs/1805.10223v3)
- **Kirschmer–Narbonne–Ritzenthaler–Robert**, *Spanning the isogeny class of a power of an elliptic curve*, introduction and Algorithm 1, PDF pp.1–4. This explicitly connects lattice data to algebraic theta data and Serre's obstruction for classes isogenous to a power of an elliptic curve, subject to its stated restrictions. For dimension three, that input is outside absolute simplicity. Its discussion of heuristic lifting concerns historical practical methods, not a theorem that an exact exhaustive certificate search is impossible. [Author PDF](https://www.math.u-bordeaux.fr/~damienrobert/pro/publications/articles/algebraic_obstruction.pdf)
- **Howe**, *Deducing information about curves over finite fields from their Weil polynomials*, arXiv:2110.04221v3, PDF p.4. The discussion emphasizes the difficulty of genus-three existence and classification. It does not impose a complexity bound retroactively on the 2006 slide question, and it is not proof that the present no-complexity-bound connection was previously unknown. [Paper](https://arxiv.org/abs/2110.04221v3)
- **Costa–Dupuy–Marseglia–Roe–Vincent**, *Ordinary abelian varieties: isogeny graphs and polarizations*, arXiv:2601.20979v1, abstract and introduction, PDF pp.1–3. Its advertised algorithms concern bounded-degree isogenies and polarizations; no exact Jacobian-recognition composition was identified in that inspected scope. [Paper](https://arxiv.org/abs/2601.20979v1)
- **Rybakov**, *Twisted Deligne modules and abelian varieties over finite fields*, arXiv:2608.16668v4, abstract and introduction, with full HTML searches for Jacobian, algorithm and computation terminology. The result generalizes categorical descriptions. No Jacobian-recognition or exact marked-model algorithm was found in this check. The introduction explicitly recalls dependence of Deligne's functor on a comparison embedding. [Paper](https://arxiv.org/html/2608.16668v4)

Targeted web searches for Deligne-module Jacobian recognition, effective inverses, and certificate constructions located these and adjacent works but no explicit theorem identifying this exact all-characteristic synthesis. **This negative result is only a bounded search observation.** It does not establish novelty, worldwide openness before this work, or nonexistence of a prior computability argument. A finite exhaustive curve search already supplies a bare decidability baseline; the accepted contribution assessed here is the explicit Deligne-to-recognition connection.

## 5. Recommended queue wording

**Status:** `claimed_solved`

**Findings:** “Exact stated connection resolved at theoretical algorithmic scope: accepted all-characteristic Deligne-counted model enumeration plus Beauville–Ritzenthaler recognition decides original-field genus-3 Jacobian existence; accepted marked certificate-search inverse identifies each specified polarized ideal. No useful complexity bound or end-to-end implementation claimed; novelty and broad historical closure unverified.”

If the bounded good-point theorem is included in the same accepted edition, append: “Recognition can use an odd extension of degree at most 7.”

The turn count is unchanged by this audit. It should be set from the separately maintained substantive-pass evidence, not inferred from this report. Retaining `unsolved` would require a specific source-imposed mathematical obligation that remains unmet, or a substantive defect in the accepted arguments. None was identified here. A desire for a practical direct criterion can be recorded as further work without redefining the original source contract.

## Reviewed artifact identities and limits

- Aggregate proof: SHA-256 `920de11606684f8f642c731c81ebfeecf05bf0d4a6ea69128e96d1f854b7f6da`.
- Marked inverse proof: SHA-256 `6828c52bf1e49781a6e0c4fe5cc75699877dd76a3128bb5655650b1e7c6ed025`.

The aggregate manuscript, marked manuscript, their acceptance reports, and the relevant source context were read for scope coverage. Source pages 37–38 were visually inspected. The accepted proof status is used as an input to this audit; this report does not independently revalidate every proof step or cited theorem. No remote or queue write was performed. Only authored analysis and public bibliographic references appear in this report; copied source pages are excluded.
