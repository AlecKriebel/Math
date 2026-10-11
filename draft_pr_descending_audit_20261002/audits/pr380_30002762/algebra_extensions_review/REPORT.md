# PR380: algebra and extension audit, Turns 1–3

**Scoped outcome: no mandatory mathematical repair found.** The frozen metabelian bound, virtually metabelian ambient-norm argument, and split abelian-extension inheritance statements are valid under their stated finite ordinary generation and abelian-kernel hypotheses. This report certifies neither novelty nor a solution of the original finitely presented counterexample question, and gives no full-PR merge-readiness or service disposition claim.

The audited object is Git commit `9946a67cf8a1f7e3130d2a12de902db05875283a`. `EXACT_BINDINGS.json` verifies every one of the 44 frozen snapshot paths (43 target files and the queue) against `git show` of that exact object and against the supplied SHA-256 manifest. `SCOPED_REPLAY_BINDINGS.json` rechecks all 44 files in the public snapshot and the private replay copy against the exact Git object after replay. Nothing in the candidate, queue, Git index, refs, or remote service was changed by this family.

## Source, independence and hypotheses

I fetched the [EMS primary OWR3/2015 PDF](https://ems.press/content/serial-article-files/46555), read Kędra's complete contribution on printed pp.199–200, and visually checked p.199. It requests a finitely presented counterexample to either the bounded-or-undistorted cyclic-power dichotomy or bounded-or-detected by a homogeneous real quasimorphism dichotomy. The norm comes from finitely many conjugacy classes. `PRIMARY_RECEIPT.json` records the independently fetched PDF SHA-256 `a2bd67ed20de1290e2cf5d2846d643438684d17a7ef0fff848f58fe8047ed0e5` and byte length 438,780.

The first candidate-content exposure was the `SOURCE_GATE.md` source index. It also exposed the source-question summary and literature-scope cautions; that exposure is candidly recorded. No TURN, FINAL, old review, sibling or root verdict was read before the independent reconstruction and controls were sealed at 2026-10-03T03:34:52.354934+00:00. The `PRECOMPARISON_SEAL.json` SHA-256 is `0aea01e44ff44ab3bb1c3846e18ed61f4829f6c34b72a79ca0543c8ff13c1772`. Its eight file bindings were subsequently rechecked unchanged. The candidate's Turns 1–3 and every replay script were then read fully; the old review and final summaries were read only afterward. This ordering avoids treating the earlier PASS as independent mathematical evidence.

Conventions used throughout:

- S consists of d finite representatives; inverses and all conjugates are allowed as unit letters. d counts representatives before symmetric closure. Ordinary generation, G=<S>, is stronger than normal generation.
- For [x,y]=xyx^{-1}y^{-1}, the fixed-side bound is ||[x,y]||<=2||y|| (and symmetrically 2||x||). A bound on arbitrary commutator length alone supplies no uniform normal norm bound.
- Bounded cyclic powers mean a single bound for every signed power. Undistorted powers mean a positive stable norm, hence a positive linear lower bound. Zero stable norm alone would not imply bounded powers outside the proved classes.
- An ordinary homogeneous real quasimorphism has one finite defect on the entire group and exact signed homogeneity. All detectors and pullbacks here have that meaning. No partial-quasimorphism defect is substituted.

## Turn 1: metabelian groups with arbitrary abelian derived subgroup

The candidate's ordinary-generation hypothesis is explicit. For an abelian normal subgroup M, its right-factor operator identity UV-1=(U-1)V+(V-1), together with the inverse identity, proves [G,M]=sum_i(T_i-1)M even for noncommuting actions. The terms can be grouped only because M is abelian. Each resulting factor is a commutator with a fixed ordinary generator, giving a uniform bound on the whole subgroup.

For M=G', the quotient by [G,M] has central derived image. The finitely many basic commutators generate that image; arbitrary integer exponents lift as [x_i^{n_ij},x_j]. The residual lies in [G,M]. This gives 2 binomial(d,2)+2d=d(d+1), with no finite-generation assumption on M. The candidate does not presume that every derived element is a single commutator. Its lifting proof establishes the additive norm comparison with the specified abelianization word norm, and the torsion-versus-real-character alternatives follow. The additional argument that every ordinary homogeneous quasimorphism descends to abelianization is also sound: bounded derived elements have zero value; the fixed defect applied to g^n h^{-n} makes equal cosets have equal homogeneous values.

The independent precomparison mechanism uses normal generation of the derived subgroup by the basic commutators as a module, augmentation compression, and class-two lifting. The fresh rank-four class-two control executes the entire group law, verifies six fixed-side commutator certificates for arbitrary central coordinates, and exhibits c_12 c_34 with Pfaffian 1, whereas a single commutator's Pfaffian is zero. This is a concrete boundary against an invalid single-commutator shortcut.

The Laurent-lamp subgroup Z[t,t^{-1}] semidirect Z gives an actual two-generator metabelian group whose derived subgroup (t-1)Z[t,t^{-1}] is not finitely generated as an abelian group. Independence of the Laurent translates follows from the absence of zero divisors in the Laurent ring; the finite controls execute the full semidirect group law and bounded certificates, not a stand-alone matrix identity.

A further negative boundary uses countably many dyadic-rational coordinates with t acting by doubling. The resulting group is normally generated by t because [a,t]=-a, yet no finite ordinary generating set covers all coordinates. Thus ordinary-generation module arguments cannot silently be attached to merely normal generators. This does not falsify the candidate: its theorem and proof specify ordinary generation. It also does not assert a new theorem or historical priority for the broader normal-generation case.

## Turn 2: virtually metabelian groups

The finite-index core is normal, metabelian and finitely generated. The candidate applies the metabelian bound to the restriction of the ambient norm using the actual finite ambient norms of the core generators. This supplies an upper bound on the core's derived subgroup without asserting any intrinsic-to-ambient lower bound.

After quotienting by that bounded normal subgroup, the remaining group is virtually abelian. Compressing its commutator with the abelian finite-index subgroup leaves a central finite-index quotient. The finite-generation and transfer proof of finiteness of its derived subgroup is valid: finitely many transversal conjugates normally generate the derived subgroup; its central intersection is finitely generated by Schreier; transfer restricts to the index power map and kills the derived subgroup. The central intersection has finite exponent and is finite. Bounded-kernel lifting then proves boundedness of the original derived subgroup and the additive comparison with abelianization. No group-independent numerical bound for finite extensions is asserted.

The independent precomparison proof uses a different final mechanism: compress [G,N] in the ambient norm using a finite quotient transversal, then separate torsion and nontorsion elements of N/[G,N] by invariant real characters and extend them by explicit transfer. It reconstructs both cyclic dichotomies without assuming an ambient lower comparison to an intrinsic norm. The candidate's stronger whole-derived-subgroup conclusion was separately checked through its elementary central finite-index proof.

The fresh Laurent-lamp semidirect D_infinity control has an index-two metabelian subgroup with infinitely generated abelian derived subgroup. Every zero-sum lamp element has a fixed-side commutator certificate; even translations have a reflection commutator certificate. The entire derived subgroup in this actual example has ambient norm at most 4, and every zero-mass element and all its signed powers have certificates at most 6. Meanwhile intrinsic translation powers in the metabelian index-two subgroup have norm at least |n| through its Z quotient. In particular t^102 has an ambient two-letter commutator certificate and intrinsic norm at least 102. This decisively rejects the invalid finite-index metric-equivalence shortcut while supporting the candidate's ambient treatment.

## Turn 3: split abelian extensions and ordinary detectors

The candidate applies its compression lemma to a finite ordinary generating set of the total group, so its bound is 2d with d equal to that generating-set size. It correctly identifies the quotient as M_Q x Q using the given splitting, and deduces finite generation of M_Q from the quotient rather than from finite generation of M. The exact additive bound concerns the induced quotient norm; passage to a product generating norm uses legitimate finite-normal-generator comparisons.

The product normal norm is exactly the sum of the factor norms for product generators. Torsion in the finitely generated abelian factor has bounded powers, nontorsion is detected by a real character, and either quotient dichotomy passes through projection and the bounded kernel. A homogeneous quasimorphism pulled back from Q retains its original global defect and domain. The candidate makes no nonsplit assertion and its Heisenberg warning is correct.

The fresh infinite control is Z^2 semidirect the free group on two generators, with action matrices P=((1,2),(0,1)) and U=((1,0),(2,1)). These matrices do not commute. The action preserves vectors modulo 2, and its coinvariant kernel is exactly 2Z^2: the two generator differences supply 2e_1 and 2e_2. Every kernel vector is represented by two fixed-side commutators, giving a four-letter certificate in the actual semidirect multiplication law. Projection to (Z/2)^2 x F_2 is checked as a homomorphism, including arbitrary-word coboundaries.

A homogeneous Brooks-type real quasimorphism is constructed explicitly by signed cyclic adjacent-pair counting on the free group. The written cancellation argument in the reconstruction proves a fixed global defect at most 12; controls observed maximum 2. It detects the free commutator despite zero exponent characters, remains homogeneous on signed powers in the actual semidirect product, and is unaffected by kernel perturbations. This gives a genuine ordinary non-homomorphism detector control, rather than a partial function or a defect inferred merely from samples. The nonsplit Heisenberg multiplication cocycle independently falsifies the would-be central-coordinate homomorphism; its central powers remain bounded by fixed-side commutators.

## Exact executions and their limits

`new_exact_controls.py`, written without candidate imports before comparison, passed **71,921** exact assertions using only integer and rational arithmetic. `NEW_CONTROLS_FULL_RESULTS.json` supplies every family count; `NEW_CONTROLS_RECEIPT.json` supplies actual execution times and full-output hashes. The code SHA-256 is `9d13d38f984b3127fb2cf9a6f66a6b9229be10a8caff3a4f6300e7fbd5dc5558`. The finite controls falsify boundary assumptions and check exact identities; the universal proofs do not rest on enumeration.

All candidate execution took place in an ignored private copy. `PORTABLE_REPLAY_FULL_RESULTS.json` preserves the complete stdout, stderr, exit status, command, times and SHA-256 hashes for all three complete portable executions:

| Execution | Actual complete result |
|---|---|
| REPLAY_ALL.py | 345,888 assertions; 62 manifest entries; all receipt bytes exact; 0 optional source bindings |
| review/independent_check.py | PASS; 47,964 assertions |
| verify_publication.py | PASS; 345,888 author and 47,964 earlier-review assertions; source omission explicitly reported |

The scoped checkers were also run separately with byte-exact stored stdout: Turn 1 gave 7,418 assertions; Turn 2 gave 149,704; Turn 3 gave 12,002. Their complete outputs and bindings are in `SCOPED_REPLAY_BINDINGS.json`. All stderr was empty and all successful executions exited zero.

The first replay attempt failed before any execution because the shell could not create its temporary here-document while the shared disk was full. The successful capture script avoided that shell path after space became available. This transient failure is preserved in the checkpoint log; no partial run was reported as successful.

The earlier private review describes eight optional raw-source bindings. The present portable packet contains no `sources/` directory, so the actual public replay verifies zero such bindings, exactly as its documentation and wrapper report. Its frozen script/receipt/manifests were still checked byte-exact. The separately fetched primary EMS PDF is independently bound by this family's receipt, and is not falsely counted as one of the candidate's optional eight source checks. No primary literature theorem is needed to establish the three elementary algebraic proofs audited here.

## Mandatory minimal repairs or clean list

**Mandatory mathematical repairs for Turns 1–3: none.** The following clean items were explicitly verified:

1. finite ordinary generation is stated; symmetric finite normal norm conventions are compatible;
2. noncommuting operator telescoping is correct; abelian image grouping is justified;
3. arbitrary, non-finitely-generated derived subgroups are allowed; no single-commutator assumption is used;
4. every commutator norm bound controls a fixed side uniformly;
5. finite-index comparison is ambient and one-sided where required;
6. core, normality, Schreier and central-transfer hypotheses are present;
7. bounded kernels preserve the specified quotient norm up to the claimed additive error;
8. split coinvariants give the actual direct product, and the abelian quotient factor is finitely generated;
9. detectors are ordinary homogeneous real quasimorphisms on the stated domain;
10. the nonsplit boundary and finite-presentation target remain explicit.

The strongest verified scoped result is precisely the three stated obstructions and norm comparisons. The original existence problem remains unresolved in this packet. Assessments of Turns 4–5, whole-PR source/queue consistency, other PRs, novelty and any acceptance action belong to the root's separate reconciliation; this family performs none of those actions. Completion estimate for this assigned family: 100% of the scoped audit, not 100% of the original discovery problem.
