# Source and status audit: KP-4.85

Checked 30 September 2026. Numeric ID **2961**, problem **KP-4.85**. The full target remains unresolved in this attempt. The note's useful claims are a correction to a background remark and explicit obstructions to two transfer routes, with no novelty claim.

## Exact source and duplicate

The upstream problem page could not be retrieved through the web tool. The complete pinned record is preserved in `source_record.json`; its research-results entry is null and its background contains a dated OPEN-TRIAGE report. These data came from the verified ulamai/UnsolvedMath cache at revision `37e53eabe540fb458758e198be61634bd02ee008`, with attribution under CC BY 4.0.

The pinned triage's AIM URL, `https://aimath.org/pastworkshops/kirbylistrep.pdf`, is a four-page workshop report and is not the complete K3 problem list. The complete [K3 author PDF](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf) was available in the shared source cache. Problem 4.85 and all its remarks on printed pp.259–260 were read and visually inspected. It asks for a closed orientable smooth four-manifold whose full smooth identity component is not uniformly perfect, and is attributed to Hokuto Konno. The PDF and page images are research inputs, not republication artifacts.

An exact duplicate was found in the full pinned dataset: **30004403 / OWR-17471-009**, preserved in `related_source_record.json`. Its original source was independently recovered in full: [Oberwolfach Report 8/2020](https://ems.press/content/serial-article-files/46844), Richard Webb's report *Quasimorphisms on homeomorphism groups*, pp.487–489, Question 3 on p.489. The workshop took place in February 2020; the dataset's title mentions 2021, but the report number and DOI are 2020/8. The two records ask the same mathematical question and must share the outcome and attempt budget.

## Scope that cannot be weakened

- The group is the identity component of **all smooth diffeomorphisms**, with no symplectic, volume-preserving, fiber-preserving or boundary condition imposed.
- The obstruction sought is unbounded **ordinary commutator length in that full group**. Positive stable commutator length or a nonzero homogeneous quasimorphism on it would suffice, but was not constructed here.
- A subgroup inclusion only decreases possible commutator length. A quasimorphism on a subgroup requires a justified extension, and a quasimorphism on a central covering group requires descent through the kernel.
- Unbounded fragmentation has the wrong inequality direction to imply unbounded commutator length by itself.
- Smooth means C-infinity. Results with the exceptional differentiability exponent r=dim(X)+1 do not create a counterexample in this problem.

## Primary literature actually inspected

1. **Burago–Ivanov–Polterovich**, [*Conjugation-invariant norms on groups of geometric origin*](https://arxiv.org/abs/0710.1412), published in Adv. Stud. Pure Math. 52 (2008), 221–250. A complete author manuscript was recovered. The group convention is stated near the beginning. Section 1.3, Definition 1.16, the product examples, Theorem 1.18, and the algebra and proof of Theorem 2.2(i) were inspected. Products of a closed manifold with Euclidean space are portable and their compactly supported smooth identity groups have commutator width at most two. `PARTIAL.md` reproduces the needed finite compression identity and product case, importing the classical perfectness theorem explicitly.
2. **Tsuboi**, [*On the uniform perfectness of the groups of diffeomorphisms of even-dimensional manifolds*](https://ems.press/content/serial-article-files/43279?nt=1), Comment. Math. Helv. 87 (2012), 141–185. The complete **published** PDF was recovered. Theorem 1.1(2), p.142, includes compact four-manifolds with a handle decomposition without 2-handles, with bound four. Its new general theorem, Theorem 1.2, assumes dimension at least six. The introduction also explains the role of disjoint Whitney disks and records corrections to earlier formulations of auxiliary general-position statements. The source audit therefore relies on the published theorem, not on the earlier 2009 preprint alone.
3. **Bowden–Hensel–Webb**, [*Quasi-morphisms on surface diffeomorphism groups*](https://www.math.lmu.de/~hensel/papers/dagger_arxiv.pdf), J. Amer. Math. Soc. 35 (2022), 211–231. A complete author manuscript was recovered. Theorem 1.2 and Corollary 1.3 establish non-uniform perfectness of the full identity component of a closed orientable surface of positive genus. Its introduction already recalls the no-middle-handle four-commutator theorem. Its fine curve graph construction uses actual curves rather than isotopy classes. No unproved four-dimensional analogue of that graph or its quasimorphisms is used here.
4. **Webb, OWR8/2020**, as above. The complete surrounding discussion on pp.487–489 gives the estimate cl ≤ 2 frag and explicitly lists four-manifolds without 2-handles among the understood cases, before posing the remaining four-dimensional question.

These sources show that the K3 remark asserting that only S4 is understood in dimension four is too broad as written. S1×S3 already has a handle decomposition with indices 0,1,3,4 and is covered by Tsuboi's theorem. The same applies to standard connected sums of such products. This observation credits existing literature and does not turn the original existence question into a solved problem.

The duplicate OWR record labels the linked Tsuboi paper as “Fukui and Rybicki.” The linked EMS publication is authored by Takashi Tsuboi; our citations use the publisher's correct attribution.

## Current-literature boundary

Searches covered the exact question, four-dimensional commutator length, uniform perfectness, product stabilization and quasimorphism extension, with current results through the search date. Later results encountered included nonorientable **surface** diffeomorphism groups, Hamiltonian-group perfectness and quasimorphisms, bounded cohomology of spheres and certain three-manifolds, and bundle or submanifold-preserving groups. Their objects or conclusions do not automatically answer this question. No claimed resolution for the required full smooth four-dimensional identity component was verified.

For example, [Edtmair's 2025 smooth-perfectness preprint](https://arxiv.org/abs/2509.16327) concerns Hamiltonian diffeomorphisms and locally bounded smooth commutator factorizations. It does not assert global uniform perfectness or non-uniform perfectness of the full Diff0 in dimension four. [Monod–Nariman](https://arxiv.org/abs/2111.04365) studies particular homeomorphism/diffeomorphism groups and bounded cohomology in specified degrees; its stated results do not supply the desired example. These abstract-level exclusions are not claimed to be complete audits of those papers.

The explicit K3 2026 question and this bounded literature search support retaining an unresolved status, but absence of a located resolution is not a guarantee about all unindexed literature. No current-best-bound or historical-priority claim is made for our partial consequences.

## Prior-attempt gate and research outcome

The queue row for 2961 was queued at 0/5. Numeric-ID, problem-code and descriptive searches of state, attempt histories, assessment histories, update/reset histories, related-target groups, all-ref attempt-path history, repository paths, and all-state PRs found no previous project attempt for 2961 or its exact duplicate 30004403. Exact branch and PR checks also found no pre-existing work on either assigned problem branch. Desk-review notes and external papers were treated as prior context, not as proof certificates.

Two substantive approaches were attempted and recorded locally. Surface-product transfer is blocked by an explicit ambient bound of four on f×id; direct cocycle averaging loses its bounded-defect proof when the measure is not invariant, and the full identity component preserves no probability measure. Neither obstruction settles the original existence question.

All 6,570 exact finite checks pass. They check the commutator-compression word in finite permutation groups, including noncommuting commutator controls; the pointwise factorization; and a singular derivative showing why a general point-dependent-time cutoff is invalid. They do not certify the imported perfectness theorem, an infinite-dimensional group conclusion on their own, or novelty.

The actual model was gpt-6-astra at xhigh reasoning. Separate adversarial review is pending; no PR will be opened before that review. Shared queue/state files were not regenerated or edited here.
