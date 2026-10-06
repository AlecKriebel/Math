# PR124 novelty distinction adversary

Audit date: 2026-10-06. Exact target: problem 10400231 / AMR-103-0231, literal Turaev Conjecture 12.26. This audit concerns historical inference and contribution scope; it accepts the passed mathematical/source gate and performs no new central proof search.

## Verdict

**The blanket label “already solved / no new contribution” would exceed the located evidence if it asserts an earlier explicit resolution of Conjecture 12.26 or proves that this application was previously recorded.** The evidence does establish that the complete obstruction and authenticated counterexample follow formally from older published machinery. A new universal obstruction, new square-presentation mechanism, or claimed escape from an unresolved mathematical obstruction is therefore unsupported. The narrower possible contribution is the explicit application to the literal prescribed-pair conjecture and the displayed witness family. Its novelty is unestablished.

For the project's requirement of a genuinely open, novel full resolution before publication, this distinction does **not** clear the present work. Maintain a failed novelty clearance while retaining the valid negative mathematical answer. Neither “no explicit old refutation located” nor the original problem-list/database label establishes current openness.

The recommended bounded description is: **valid counterexample; old formal consequence verified; explicit prior conjecture refutation not located; application priority unresolved.** This is a recommendation, not a native status change.

## Four historical propositions

| Proposition | Evidence and bounded finding |
|---|---|
| (i) Old mechanism | Verified. Turaev's 1986 proof of Theorem 1.6.1 supplies the integral Laurent square matrix and exact integral specialization needed here. The other families also locate the cut-surface mechanism in Alcaraz 2014. The present work cannot claim either mechanism as invented here. |
| (ii) Old full inequality / theorem consequence | Verified as a formal consequence of the 1986 integral interface and the elementary determinant rank-drop argument. The exact inequality need not have been printed for this implication to hold. Truman's 2006 dissertation explicitly states a related modular augmentation-ideal inclusion and explicitly extends it to rank one, strengthening the historical antecedent. |
| (iii) Original conjecture's negative answer expressly recorded | Not established. No inspected source or bounded query located an express refutation of Conjecture 12.26 or this exact prescribed pair. This finding is not evidence that no such record exists. |
| (iv) Defensible contribution of the present application | Possible, not certified. An explicit application exposing insufficiency of the published conjecture's conditions, with a compact witness and self-contained integral proof, can be useful even when its tools are old. Its previously unrecorded status and research significance remain to be established. Expository and reproducibility value alone do not meet the stated novel-discovery goal. |

## Exact historical interface and its limits

The target prescribes H = Z direct-sum T itself, including the isomorphism type of finite T, and the ordinary integral Alexander polynomial in Z[t,t^-1]. It does not prescribe only the torsion cardinality, use a refined polynomial retaining finite-group variables, or divide away integer content. The authenticated original head is d110ad761291aa6ac1d66d2a49e8b8212c18bed6. Its preserved counterexample uses T = (Z/2)^3 and Delta = t + 6 + t^-1; it already includes the all-prime family.

Turaev, [Reidemeister torsion in knot theory](https://doi.org/10.1070/RM1986v041n01ABEH003204), Russian Mathematical Surveys 41:1 (1986), printed 133, proof of Theorem 1.6.1, handles connected compact rank-one three-manifolds with Euler characteristic zero. For a boundary manifold his primitive-circle-relative spine has square integral Laurent boundary matrix B, determinant the ordinary Delta, and B(1) the actual integral relative boundary. For closed orientable M he drills a primitive free homology generator, obtaining an exterior V with H1(V) isomorphic to H1(M) and Delta(V) identified with Delta(M). These statements were inspected on the full printed page; the ordinary Alexander convention was checked in printed 126–127 text. The theorem's *stated conclusion* is the augmentation formula, rather than the modular rank inequality.

The following implication is our formal reading of the published interface, not a quoted 1986 conclusion. The relative sequence identifies coker B(1) with (Z direct-sum T)/<(1,s)>, hence with T. Modulo any prime p its corank is r_p(T). Constant invertible row/column operations make that many rows vanish at t = 1, so each contributes a factor t - 1 to det B. This gives ord_1(Delta mod p) >= r_p(T), including zero reductions with infinite order. Units and reversing t do not change the order. The original family has t Delta_p = (t - 1)^2 + p^3 t and r_p(T) = 3; its order two violates the old formal consequence. This route covers p = 2 independently of the polynomial-part issue below.

The formal implication is substantively stronger priority evidence than merely pointing to familiar Alexander machinery: the integral interface contains the full torsion-group information, and the residual step is elementary. But it still does not show that Turaev or anyone else recorded the modular consequence or noticed its conflict with the later conjecture.

Truman's [UMD dissertation record](https://drum.lib.umd.edu/items/eb6edb82-8b0e-4566-bb69-72fca6e6eed2), *Turaev Torsion of 3-Manifolds with Boundary*, authenticates a 2006-04-24 deposit and handle 1903/3453. Printed 35 explicitly extends mod-r torsion and its theorem to b1 = 1 using Turaev's polynomial part; printed 45, Theorem 2.2, includes tau mod r in I^(b - 2), where H1(M;Z_r) is free of rank b >= 2. The ambient setting is compact connected oriented manifolds with nonempty boundary and Euler characteristic zero. It attributes the inclusion itself to Turaev 2002 II.4.4. The corresponding [arXiv article](https://arxiv.org/abs/math/0611210) was submitted in November 2006, but its current PDF has an internal 2018 date; the dissertation avoids reliance on that discrepant internal date.

Ye, [Constrained knots in lens spaces](https://doi.org/10.2140/agt.2023.23.1097), AGT 23 (2023), printed 1131, equation (4), states the rank-one polynomial-part normalization in a knot-exterior proof. Its factor is either a power of t or that power times (t + 1)/2. For odd p it is a unit locally at t = 1. Projecting finite variables to one kills the singular numerator whenever p divides |T|. Consequently, with the same polynomial-part convention, the augmentation inclusion yields the same ordinary-Delta p-rank bound. A p = 3 witness would suffice to refute the universal conjecture. This odd-prime translation is compelling corroboration; it is not certified here as an independent fully closed source route because the exact identification with Truman's cited polynomial part remains to be checked in Turaev's book. The half factor prevents an unqualified mod-2 translation by this route.

## Adversarial reading of both novelty claims

The strongest case against mathematical novelty is that no new topological invariant, stronger bound, new realization obstruction mechanism, or extra class of manifolds has been established beyond the old integral interface and determinant observation. The original proof's attention to finite cut-manifold torsion and exact specialization is essential for correctness, but these features have historical antecedents. Truman's explicit modular theorem further reduces any claim that the general finite-field obstruction itself is a newly discovered mechanism. Limiting discussion to p = 2 would not rescue the named conjecture's novelty: the original family already includes odd primes, and the 1986 implication covers every prime.

The strongest case against “no new contribution” is that mathematical contribution is not identical to membership in the logical closure of older results. A previously unrecorded short counterexample to a published conjecture can constitute a new observation or application. Here the 2002 collection records a sufficiency conjecture despite the 1986 matrix interface. That historical juxtaposition makes a correction conceivable; it does not prove novelty. The 1986 source states an augmentation result and its proof carries more structure than that conclusion. Extracting a different consequence and connecting it to a later prescribed-pair question is a distinct act that cannot be attributed to the earlier author without evidence.

Thus “the old result formally implies the negative answer” is justified; “the negative answer was already known/published as such” is not justified by these sources alone. Likewise “the application may be new” is justified only as an unresolved possibility; “we newly resolve a genuinely open conjecture” is not justified.

## Exact remaining gaps and stopping boundary

1. Direct full-text access to Turaev's *Torsions of 3-manifolds* (2002), chapters II/III: II.3, II.4.4, II.4.5 and III.4.3, including rank-one polynomial-part definitions and hypotheses. Root's recorded official full/chapter PDF endpoints yielded HTML access/cookie pages, not readable PDFs. These are real source gaps. This audit did not seek permission, contact anyone, or treat failed download pages as theorem evidence.
2. The possibility that the book, a later update to the problem list, a thesis, or another primary paper explicitly states the conjecture's negative answer or the exact family. The family audits retain additional inaccessible historical leads (Turaev 1976 and 1989) and an Alcaraz thesis gap. They remain unclosed; their contents are not asserted here.
3. Whether the exact ordinary-Delta inequality was previously printed, beyond its verified logical consequence from the 1986 interface and the explicitly printed refined modular statement.
4. Whether presenting the explicit application is sufficiently original and substantive for the research goal. No source absence, expert assessment, comprehensive citation census, or first-priority certification has been supplied. Outside scholarly input could help assess that gap; no outreach was prepared or initiated.

Ten fresh bounded search queries and the inspected primary records are recorded in SOURCE_QUERY_MANIFEST.json. Exact-number/refutation and exact-polynomial searches returned the original conjecture or unrelated material; those non-hits cannot establish absence. Search crawled/published labels on old PDFs were not used as publication dates.

## Independence, controls, and seal

EARLY_INDEPENDENT_CHECKPOINT.md was preserved at 2026-10-06T20:09:10Z before consulting current other-family reports or the root bridge. Subsequent cross-checks are identified in the research log and manifest. The source page images were actually inspected; a render receipt alone was not counted as reading.

All writes are confined to novel_contribution_adversary_20261006. Private web response evidence is ignored; no source PDF or extracted source text is included in the public members. No shared tracked file, branch, index, native status, PR, GitHub/Zenodo/Sheet state, or external person was changed/contacted. No commit, push, publication, or PR closure was performed.

Bounded audit completion: 100% when sealed. Historical novelty/first priority remains unestablished, and novel-discovery publication clearance remains false. SHA256SUMS.json lists every public member other than itself.
