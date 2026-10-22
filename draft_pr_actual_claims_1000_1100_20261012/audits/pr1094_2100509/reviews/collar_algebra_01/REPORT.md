# PR 1094 independent collar-algebra adversarial review

Reviewed target: problem 2100509 / AMR-020-0509. Submitted head: `954dd70b49458026e29b8dae63243391249008d8`. Workspace main during input capture: `fa24428a4fa6930fd3df9dc1b2feb0f7c72885c9`; this was not substituted for the submitted head. Review completed 2026-10-14 UTC.

Verdict: **PASS for the complete stated smooth classification. No P0, P1 or P2 defect and no required candidate correction found.** The constructive proof is universal, and the exact necessary obstruction is supported by the prior theorem and independently checked using its local holomorphic/splitting mechanism. Bibliographic priority and current-world openness remain unestablished, as the submission explicitly says.

## Independence and custody

The full MATHEMATICAL_REPORT was read before the old audit, README, source review, acceptance and status labels. INDEPENDENT_DERIVATION.md records the ensuing full derivation before companion-file inspection. No other mathematical family or review shard was read or contacted. New work was confined to this review folder. No candidate edit, branch change, Git mutation, service write or outside outreach was made.

All eight snapshots were byte-compared with actual locally available Git blobs at the submitted head and with their SUBMITTED_PINS SHA-256/length records. INPUT_CUSTODY.json includes the actual blob OIDs. The eight files were copied from those exact Git blobs to frozen/. The actual base-to-head diff is exactly the eight advertised additions. PACKAGE_INTERFACE_CHECKS.json verifies the manifest's seven member hashes, the acceptance proof/audit hashes, every captured PR-body pin including the independent manifest pin, and the captured head identity. The PR body was reviewed from LIVE_PR_CAPTURE.json, not represented as a fresh service fetch.

## Exact claim and criteria

For every n>=1 and every prescribed real Jordan matrix with entirely real numerical eigenvalues, there is a globally C-infinity compactly supported real Nijenhuis (1,1) tensor on R^n attaining that matrix in a commuting local frame on a nonempty open set. Conversely, no compactly supported such tensor can have nonreal spectrum at any point. Type and eigenvalues may change elsewhere. A fixed ambient Cartesian matrix, global constant rank/type, analytic compact support and global gl-regularity are outside the claim.

The [fresh v2 primary source](https://arxiv.org/abs/1804.03737v2), Problem 5.11 p29, asks precisely for compact support and prescribed unchanged Segre type in a domain. Its [v1 counterpart](https://arxiv.org/abs/1804.03737v1) is Problem 4.10 p37. The exact read-only local corpus row's statement hash matches the catalog identity; its full wording agrees and its 5.9 marker is correctly distinguished from these locators. Neither source requires varying numerical eigenvalues or a Cartesian frame.

## Independent full proof verification

For the globally commuting product frame E_i,T on T^(n-1) x I and L=[[A(t),b(t)],[0,lambda(t)]], the angular pairs have zero brackets. For a mixed pair,

    [LE_i,LT]=-lambda*A' E_i,
    [LE_i,T]=-A' E_i,
    [E_i,LT]=[E_i,T]=0.

The defining torsion is therefore `(A-lambda I)A' E_i`. There are no b', lambda' or angular components omitted; skew symmetry and tensoriality account for all pairs. In particular, the ordered product cannot be reversed and A need not commute with A'.

Designating the terminal vector of a Jordan chain as transverse leaves the shortened chain and all other blocks in A_0, retaining the full initial matrix via b_0. Holding A fixed makes b removal and arbitrary lambda alignment free. For an active block mu I+K, with lambda=mu and K=sum a_j E_(j,j+1), direct multiplication gives K K'=sum a_j a'_(j+1) E_(j,j+2). Removing a_1 first and then a_2, etc., annihilates the predecessor of each changing arrow; the first arrow has no predecessor. Once scalar, that block and lambda drift by exactly the same scalar function. The derivative is confined to the active block, where A-lambda I is zero. All other derivatives stay zero, including previously zero blocks. Finite repetition terminates at A=b=lambda=0 without division.

Singletons have no arrows, zero scalars need no movement, repeated eigenvalues cause no denominator, and the empty angular list permits lambda-only drift. Whole-block reorderings and constant frame permutations preserve commutation and restore any desired original block ordering. The initial b retains the terminal Jordan arrow on the central plateau. Thus no Jordan multiplicity is lost at realization.

Smooth switches with open endpoint plateaus make concatenation C-infinity. One explicit switch is H(v)/(H(v)+H(1-v)), where H(v)=exp(-1/v) for v>0 and zero otherwise, after rescaling to put plateaus near both ends of each stage. A smooth even collar map can be chosen as q(t)=S((t^2-1/16)/(1/2)), where S is this standard switch. It is zero for |t|<=1/4 and one for |t|>=3/4. Chain-rule reparametrization multiplies A' by q', preserving the constraint, including where traversal reverses. This is not an arbitrary matrix cutoff.

The circle base and boundary-of-normal-disk induction produce a smooth embedding T^d in R^(d+1) in every dimension. The oriented hypersurface has a global smooth normal; in one extra coordinate its normal bundle is explicitly rank-two trivial. A common sufficiently small disk radius exists by compactness and the tubular-neighborhood theorem. Its boundary is T^(d-1) x S^1, an embedded oriented hypersurface, hence two-sided. This yields the needed same-dimensional collar, not a higher-codimension product torus.

Pushing through the collar diffeomorphism preserves the commuting frame and torsion. The central collar is nonempty and open; a small connected coordinate box inside it works if desired. The compact set T^(n-1) x [-3/4,3/4] maps to a compact subset of the open collar. Exact zero on both end bands makes exterior zero extension smooth at all orders. Naturality and locality cover the extension boundary. No global exterior frame is needed. In dimension one, torsion is an alternating vector-valued two-form and vanishes automatically; a plateau bump times the identity realizes any scalar. The zero matrix also causes no exception.

## Primary rigidity and adversarial source check

The [prior rigidity source](https://arxiv.org/abs/1903.04603v2) has the quoted statement on p41; its full proof on pp42-43 and foundational splitting/holomorphic material were read. Theorem 6.1 assumes a closed connected smooth manifold, with no analyticity, constant type, gl-regularity or everywhere-nonreal premise. A compact-support tensor on R^n is exactly zero in the sphere chart near infinity, so its zero extension is smooth and Nijenhuis on closed connected S^n; persistence of a nonreal eigenvalue would contradict the zero point.

The p43 polynomial-reduction paragraph has a nonblocking literal imprecision about how many nonreal pairs its polynomial removes. SOURCE_DEPENDENCY_ADVERSARY.md provides a concrete spectral counterexample to that intermediate sentence and independently verifies the exact needed zero-point obstruction from the earlier maximum-principle phase. It isolates the maximal-imaginary-part cluster, uses a holomorphic trace maximum, and observes that shifting the roots onto the real axis makes all holomorphic polynomial coefficients constant. This avoids smooth-root assumptions and does not depend on the disputed induction sentence. It is not a counterexample to the cited theorem or a gap in the submitted classification. No full independent certification of the stronger prior constancy proof is claimed.

## New exact controls

exact_controls.py is new standard-library sparse-polynomial code. It is not a replay of an omitted historical program. CONTROL_RESULTS.json records PASS for:

- 85 scalar torsion components in arbitrary independent value/derivative jet families in dimensions 1-5, directly from the Lie-bracket definition.
- 452 full Jordan families and 4,416 stages: every ordered composition in dimensions 1-7 with every distinguished block, plus larger and mixed examples through dimension 20. Exact start/end continuity, the ordered product and final zero are checked. All-pair bracket torsion is also checked on the 172 stages in dimensions 1-4.
- Independent formal eigenvalue symbols, so every repeated/zero numerical specialization remains covered by the exact polynomial identities.
- Negative controls detecting reversed arrow deletion (`-E13`), one scalar cutoff (`u E13`), unmatched scalar drift (`mu^2 u`), and the reversed product rejecting a valid stage (`-E13`).
- A positive example with nonconstant b and lambda but constant A, whose torsion is zero; this refutes any added b'/lambda' restriction.

These finite controls strengthen indexing and schedule confidence. They do not establish arbitrary-dimensional existence by extrapolation; that follows from the universal argument above. They also do not authenticate the submitted historical test counts, which are explicitly identified as historical evidence.

## Eight-file consistency

| File | Result |
|---|---|
| MATHEMATICAL_REPORT.md | Full universal proof verified; exact local-frame and smooth scope retained. |
| MATHEMATICAL_AUDIT.md | Its derivations and boundary-case claims agree with fresh review; old finite counts remain historical. |
| README.md | Accurate statement, prior credit, eight-file inventory and review limits. |
| ACCEPTANCE.json | Proof/audit byte identities exact; accepted claim agrees with the proof; priority and external-review disclaimers clear. |
| STATUS.json | Accepted smooth scope consistent; no omitted executable treated as premise. |
| SOURCE_REVIEW.md | Exact locators and theorem hypotheses agree; later sources and negative searches remain bounded evidence. |
| SOURCE_METADATA.json | All four historical PDF identities matched fresh fetches; version dates and roles checked. |
| MANIFEST.json | Eight-member inventory exact; seven non-manifest hashes and lengths exact; manifest independently pinned by captured PR body. |

The [Geometry III primary PDF](https://arxiv.org/abs/2007.09506v1), full pp1-4, confirms local real-analytic gl-regular scope. Narrow checks of the identified [2024 survey](https://arxiv.org/html/2410.04276v1), [2026 three-dimensional paper](https://arxiv.org/html/2607.04913v1), and [2026 two-dimensional dictionary](https://arxiv.org/html/2609.05103v1) agree with their submitted contextual roles. No global priority search was undertaken. All four retrieved PDF lengths and hashes equal the submitted historical metadata. The exact pages of the two problem versions and full rigidity statement/proof were actually rendered and visually inspected; SOURCE_CUSTODY.json and RENDER_INVENTORY.json distinguish these fresh acts from recorded history.

## Severity and remaining gap

P0: none. P1: none. P2: none. P3 candidate defects: none. A nonblocking source-proof wording observation is separately preserved with a verified application-level repair; it requires no candidate change. No mathematical gap remains for the stated classification. The strongest verified result is the complete smooth classification, allowing every real block partition and every specified numerical real spectrum in a commuting local frame. Exhaustive novelty, current-world openness, human peer review and formal proof certification remain outside the evidence and outside the submitted claims.
