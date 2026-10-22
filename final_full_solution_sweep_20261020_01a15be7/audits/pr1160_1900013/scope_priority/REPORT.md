# PR1160 independent original-scope and bounded priority audit

Review date: 2026-10-22 UTC. Overall research-program estimate: 79%. Scope/priority review completion: 100%.

## Disposition

**The historical finiteness subquestion is fully answered, and the literal historical equivalence classes have a complete arithmetic parametrization in this PR. A blanket exclusion because the files say PARTIAL or do not edit QUEUE would miss those facts. However, the central arithmetic classification, multiplier-order discriminant, infinitude mechanism and finite-order reduction are already present in, or follow directly from, older mathematics. This audit does not support promotion as a novel full solution.**

No indispensable face-list, torus-list, particular algorithm, efficiency bound, or implemented class-group computation is stated in the literal fixed-field question. The source does support a broader interest in geometric descriptions. That distinction should be stated rather than turning neighboring problems into unstated requirements.

This is an independent internal AI scope/priority assessment, not human peer review. It does not independently reproduce all arithmetic calculations; another audit must address that. I found no new mathematical defect in the actual claims on this reading.

## Frozen object and actual claim

The inspected head is `6124be0d9baffbfb83d80d7273a2389146b3cf1d`, base `293f0c3d87e07532755d3202e535490ea07e2056`. I read the full PROOF, RESULT, README, AUDIT and ACCEPTANCE from immutable Git objects, plus the remaining five package files. All ten local PR_ copies are byte-identical to those objects; none was read from the dirty working-tree candidate. No Git/PR/Zenodo/Sheet mutation occurred.

Let C(K) be the GL(3,Z)-equivalence classes of complete eight-sail Klein unions arising from irreducible unimodular operators generating a fixed totally real cubic field K. The manuscript proves

    C(K) = {full Z-lattices I in K}/(I ~ a tau(I)),
           a in K×, tau in Aut_Q(K).

It proves surjectivity by positive SL(3,Z) realizations; its equivalence criterion is necessary and sufficient. For each exact multiplier order R, it gives a finite set of subgroups in conductor intervals c J_i <= I <= J_i and a finite unit/automorphism quotient. Orders can be enumerated as finite-index subrings of O_K. This is an exhaustive arithmetic classification, rather than merely a necessary invariant. The number of classes is exactly countably infinite, with an explicit separating family. There is no remaining realization or equivalence gap in that literal arithmetic statement, conditional on the proof's validity.

The discriminant alone is not complete: several classes may have the same multiplier order. The conductor enumeration and quotient, rather than the discriminant by itself, supply completeness. Fixed-order finiteness does not imply field-wide finiteness.

## Original-question reconciliation

[Karpenkov 2004, arXiv:math/0411054v1](https://arxiv.org/pdf/math/0411054v1), Definitions 1.1–1.2 and Statement 1.2, pp.3–4, specifies the complete sail union and integral linear equivalence for real irreducible unimodular operators. The fixed-field Problem 3 and its following finiteness remark are on p.16 after the common-field discussion on p.15. They impose no fixed polynomial or order. Geometric recognition and torus-decomposition questions are separately numbered Problems 1 and 2.

[Karpenkov 2017, arXiv:1712.01450v1](https://arxiv.org/pdf/1712.01450v1), pp.4–6, discusses multiple sail constructions. Problem 13, p.8, repeats the fixed cubic-field classification question. The p.9 remark says a corresponding classical periodic question still appears open. Section 3.3, p.7, explicitly values invariants that reveal combinatorics; Problems 9 and 11 separately request realizability algorithms and torus decompositions. This supports a broader geometric motivation, but does not unambiguously require those particular outputs inside Problem 13.

My inference: Theorem 4, Proposition 5 and Theorem 7 meet the literal historical arithmetic classification request; Theorem 6 completely settles the expressly mentioned finiteness issue. They do not characterize decorated tori or face data, and I cannot equate this arithmetic answer with every broader interpretation of the 2017 survey. The 2017 remark is historical evidence of the author's framing, not proof that familiar arithmetic parametrizations were unknown in 2017 or remain novel now. Nor does the presence of several sail definitions by itself establish that Problem 13 universally quantifies over every such model.

## Exact older route to the equivalence criterion and infinitude

The following is my deduction from older statements, not a claim that an older source writes out every line of the PR's exposition.

1. For full lattices I,J in K, choose infinite-order units in their multiplier orders. Squaring gives totally positive norm-one units. In cubic prime degree their squares generate K. Their multiplication matrices A_I,A_J are admissible positive SL(3,Z) operators.
2. By K04 Statement 1.2 (with the underlying proof in [Karpenkov's tori paper, Proposition 1.1, pp.2–3 of arXiv:0911.3025v1](https://arxiv.org/pdf/0911.3025v1)), equivalence of their continued fractions is equivalent to an integral conjugate of A_I commuting with A_J.
3. The rational centralizer of an irreducible cubic operator is Q[A_J]. This follows by identifying Q^3 with the rank-one Q[A_J]-module and evaluating a commuting map at 1. Consequently the integral conjugacy in step 2 identifies the two multiplication fields. Its induced map on K is T(x)=a tau(x): conjugation induces tau in Aut_Q(K), and a=T(1). Thus J=a tau(I). Conversely this semilinear lattice map permutes embedding hyperplanes, cones, and sails. This recovers the PR's exact arithmetic criterion without its missing-ray proof.
4. That criterion sends (I:I) to tau((I:I)), preserving its trace discriminant. For R_f=Z+f O_K, its multiplier ring is exactly R_f because it is a unital ring. Extend 1 to a basis 1,w2,w3 of O_K. Then R_f has basis 1,f w2,f w3; its index is f² and its discriminant is f⁴ disc(K). Different f yield inequivalent sails, all in the same K by step 1. Countability of finite lattice bases gives exact countable infinitude.

These are standard module/centralizer and order-discriminant deductions once the old geometric equivalence theorem is available. A different self-contained geometric proof may have expository merit; this audit does not establish new theorem priority for it.

## Direct older primary correspondence and finite classification

[ELMV, arXiv:math/0607815v1, 31 July 2006](https://arxiv.org/pdf/math/0607815v1), Definition 4.3 and Corollary 4.4, p.24, explicitly parametrizes all periodic diagonal-torus orbits by full lattices in totally real fields modulo field scalars, with embedding data. It identifies the multiplier order and its discriminant; pp.25–26 prove the matrix-field/lattice bridge. Taking the quotient by the finite permutation group of embedding coordinates removes embedding labels. For a fixed K, the resulting unlabelled arrangement classes are precisely full lattices modulo K× and genuine Aut(K). This last quotient/connection to the eight-sail equivalence is my deduction, using K04, not a quotation of ELMV.

Moreover ELMV's proof of Proposition 2.9, pp.15–16, obtains infinitely many rational translates of one fixed rational torus. Their underlying abstract field stays fixed; a further finite normalizer quotient cannot make this family finite. This is a second prior mechanism for the infinitude conclusion. ELMV's discriminant is normalization-dependent by a fixed factor, sufficient to separate differing order discriminants; I do not identify that normalization literally with the PR's definition.

[ELMV, Annals 173 (2011), §2.1 p.823 and §5.5 p.839](https://annals.math.princeton.edu/wp-content/uploads/annals-v173-n2-p05-p.pdf) restates the full-lattice parametrization, multiplier order, and distinction between order strata and local-homothety packets. In particular nonmaximal orders are not all represented by their invertible ideal class groups. These pages corroborate the correspondence, rather than supplying a new classification gap.

[Marseglia, arXiv:1805.09671v3, revised 17 August 2020](https://arxiv.org/pdf/1805.09671v3), Corollary 3.4 p.4 and Lemma 3.6 p.5 identify module isomorphism with scalar homothety and multiplier rings as invariants. Theorem 4.6 pp.7–8 and Proposition 5.1 pp.8–9 describe finite ideal-class-monoid strata including noninvertible ideals via finite conductor quotients and Picard groups. This already provides the finite order-level arithmetic machinery needed here. Theorem 8.1 p.16 gives the module/matrix correspondence, explicitly connected to Latimer–MacDuffee. I read this modern primary restatement; I did not inspect the original 1933 paper and make no priority claim based solely on its title.

My synthesis: enumerate orders R in O_K, compute the exact-R stratum of ICM(R), and quotient by field automorphisms. Combined with the old sail criterion, this gives the same arithmetic classification framework as the PR, with published stronger computational treatment of the noninvertible issue. The manuscript cannot acquire novel full-solution status by relabeling that framework.

## Boundaries and recommended handling

The strongest supported positive finding is a correct-looking, exhaustive arithmetic answer within the historical model, plus complete fixed-field infinitude. The strongest supported priority objection is an explicit deduction of its central conclusions from identified prior primary results, including a direct torus/lattice/order correspondence from 2006 and finite ideal-monoid algorithms by 2020. I did not find a source explicitly titled as a solution of Arnold's exact Problem 3; such a title is unnecessary for the deduction above, and its absence is not evidence of novelty.

Do not reject the candidate merely for PARTIAL wording, absent QUEUE changes, or absent face/torus lists. Do not promote it as a novel solution on the strength of historical openness language either. A fair disposition is **literal arithmetic classification and historical finiteness issue answered; central result derivative of prior theory; broader geometric classification unestablished; novelty not demonstrated**.

The bounded search included same-field infinitude, lattice/sail equivalence, multiplier orders, periodic torus orbits, ideal class monoids, and Latimer–MacDuffee variants. Search results for the 2026 Gauss–Kuzmin paper arXiv:2608.05853 were inspected at abstract level only; they concern statistics and were not used as a classification or novelty theorem. No global novelty certificate, exhaustive bibliography, or full claim about current geometric openness is supplied. No human or external chat was contacted.

Private full PDFs/text are excluded from publication membership. SOURCE_PINS.json records exact versions, retrieval times, hashes and inspection pages. The verifier checks closed authored membership and hashes, optional immutable Git matching and optional private-source matching; it does not prove mathematical truth.
