# Independent algebra audit: PR386 / Problem 2525

Completed UTC: 2026-10-03T01:34:15.953136+00:00. Exact frozen PR head: `76d804cffb0cdbd2c88416dad1ead6e2a89989d6`. Input bindings are in `INPUT_BINDINGS.json`; every one of the 51 frozen files matches the supplied snapshot manifest. This audit covers Turn1–4 algebra, controls, and the relevant replay machinery. Turn5 and broader source status are assigned to a distinct review family.

**Finding:** no invalid Turn1–4 theorem was found under its stated hypotheses. A source-grounded extension implication was omitted from the route summary and should be added before promotion. The original CB/non-MB existence question remains unsolved, 5/5. All acceptance and PR386 disposition remain pending PR387's disposition and any required revised-head audit. This is an independent AI audit, not external peer review.

## Primary normalization and independence

The exact manifest-bound Bergman arXiv PDF was independently retrieved from https://arxiv.org/pdf/math/0401304 and matched SHA256 `13bbd80925353a3f16683f10173979cfffe5512e40175695163973158de66fe0`. Pages 4–6 were read in text and as rendered pages before Turn1–4 reconstruction and before any prior review/verdict contents. `PRIMARY_RECONSTRUCTION.md` and `INDEPENDENT_DERIVATIONS.md` were written before previous-review comparison. The timestamped research log records that ordering. Only after reconstruction and independent controls were recorded were `final_review/REVIEW.md`, its checker, and wrapper status lines inspected.

CB is Bergman's condition (4): every group-generating subset admits a finite bound for words with inverse letters. MB quantifies over every subset genuinely generating the whole group by positive words. Bounds depend on the set; the empty word represents the identity. No topology or cardinality restriction is present. CB plus condition (3), no proper increasing countable subgroup exhaustion, implies MB. An arbitrary unbounded symmetric subadditive length refutes the conjunction, not CB alone. A group-generating proper monoid is not an applicable MB witness.

## Claim-by-claim reconstruction

| Claim | Independently checked mechanism | Hypotheses/boundary retained | Exact remaining gap |
|---|---|---|---|
| Turn1 inverse costs | Replace inverse letters in a symmetric word; `R≤D≤d max(1,R)` | S positively generates all G; d finite for this S; all-generating-set CB supplies it | No actual unbounded R in a verified CB group |
| Turn1 bounded orders | `s^{−1}=s^{ord(s)−1}` | Uniform order bound on S, not necessarily a common exponent; torsion alone is insufficient for this estimate | Unbounded orders/infinite-order generators remain possible |
| Turn1 cores | `A_n=B_n∩B_n^{−1}`, `H_n=<A_n>`; apply CB when a core generates G | CB applied to A_n, not to H_n; finite supplement fits inside later core; repeated terms harmless | Not every abstract proper exhaustion is realized by positive word balls |
| Turn2 positive Schreier | Short directed coset representatives; positive telescoping T generators | H may be nonnormal; finite index; inverse-representative cost c separately finite | Arbitrary infinite quotient lacks uniform inverse-representative costs |
| Turn2 quotients | Lift quotient letters and add all kernel elements | Same positive/group generation convention | No converse without extra kernel hypothesis |
| Turn2 strong normal kernel | Condition (3) and CB bound ambient length on N, then `l_Q≤l≤l_Q+C` | Ambient S∩N need not generate N; normality only for quotient; finite N included | MB alone has not been shown to bound arbitrary ambient lengths |
| Turn3 finite quotient comparison | Section normal form emits conjugate letters and factor-set constants; `l_T≤l_W≤(2+b)l_T` | H normal, finite quotient, genuine S; factor constants essential | Unbounded S alone need not survive finite saturation |
| Turn3 split iff | Actual finite Q-action; exact invariant-set metric equality; Schreier then Q-saturation | Finite semidirect product; action may be nonfaithful; both symmetric/positive metrics checked | No pair with CB_Q but not MB_Q produced |
| Turn3 dihedral example | Integer normal forms plus exhaustive two-letter type lower bound | Genuine positive generation; exact diameter 3; group itself fails CB | Witness destruction only, not separation |
| Turn4 finite normal generation | CB gives bounded symmetric conjugacy width; fixed positive costs bound its letters | Finite normally generating F and conjugation-invariant or uniformly controlled S | Neither arbitrary S nor finite normal generation of every CB group established |
| Turn4 inverse-producing relations | Uniform relation length and bounded finite-conjugator costs bound R | Fixed finite F, or another proved uniform positive cost; finite exceptions harmless | Variable unbounded conjugator costs/generalized torsion alone provide no uniform estimate |

The detailed, independently recorded deductions are in `INDEPENDENT_DERIVATIONS.md`. The strongest verified result is precisely this set of scoped necessary conditions, transports and equivalences. It does not imply the original separation or universal equivalence.

## Mandatory additive repair and terminology

**Required current-status clarification, without altering frozen Turn2 bytes:** Turn2 §4 says, “nor that their failure would yield the requested CB/non-MB separation.” This is a historical statement about what was established in that turn, not a false general theorem, but it misses a direct deduction from the exact primary source. Bergman, page 4 after Lemma 7, proves CB passes to arbitrary group extensions. Since MB implies CB, if N and Q are MB in `1→N→G→Q→1`, then G is CB. Therefore any such extension that fails MB is automatically a CB/non-MB separator. MB extension closure is still unproved here; no construction of its failure is supplied.

For checkability, reconstruct that credited deduction directly. Given a symmetric group-generating X of G, quotient CB gives a uniform quotient representative length d. Choose representatives r_q of length≤d with r_1=1. Schreier factors `r_q x r_{qπ(x)}^{−1}` have length≤2d+1 and group generate N. CB of N bounds their symmetric diameter by k, yielding global X diameter≤k(2d+1)+d. Thus no additional uncountable-cofinality hypothesis is required for CB extension closure.

**Preserve the scope whenever summarizing the finite-action iff:** it belongs to finite semidirect products with an actual action. In a general finite extension, `alpha_q alpha_t=Inn(c(q,t)) alpha_{qt}`; section conjugations need not be an action or generate a finite automorphism group. The frozen detailed proof correctly separates the two cases. The summary phrase “finite-action criteria” is acceptable only with that explicit meaning; “finite semidirect-product criteria” is clearer. Retain factor constants and the additive Turn3 control clarification in every current wrapper. No promotion should imply that the general finite quotient comparison is an ordinary invariant-set characterization.

## Adversarial controls and gaps

`ADVERSARIAL_CONTROLS.md` supplies checkable constructions:

- Z with one symmetric-diameter-one but positive-unbounded set, exposing the all-generating-set CB quantifier.
- Index-two cyclic quotients with representative inverse costs tending to infinity, ruling out the shortcut c≤index−1.
- Nonsplit Z/2Z with section 5, where omission of the factor constant 10 breaks the lower length comparison.
- Q16 with index-two Q8 kernel, where a section conjugation squares to a nontrivial inner automorphism; and F(a,b) with an index-two kernel, where it has infinite order.
- The exact infinite dihedral diameter-three example, with CB explicitly false.
- A restricted direct sum of S_n with one-conjugate inverse relations and positive cycle-inverse costs≥ceil(n/2), proving that relation length alone does not bound conjugator costs. This group also fails CB, so it does not refute an unproved strengthened theorem retaining CB.
- Trivial groups, empty/identity generating sets, quotient 1, nonnormal finite-index H, nonfaithful actions, and bounded orders without a common exponent.

Blocked routes remain blocked at their exact cost or quantifier gaps: (i) strong kernel replaced by MB alone; (ii) saturation preserving an arbitrary positive witness; (iii) arbitrary conjugacy costs controlled by normal width; (iv) a proper exhaustion turned into a genuine positive witness. Reopening any requires a materially new mechanism or evidence. No finite test resolves those gaps.

## Checker audit and reproduction

Private replay of `verify_turn1.py` through `verify_turn4.py` exactly matches the frozen output bytes and hashes: **236,557 assertions**. The separate prior-review checker also exactly reproduces its **6,833 assertions**. These numbers are finite regression counts, not measures of proof strength or infinite CB evidence.

The new `independent_controls.py` imports no author code and passes **34,866 exact checks**. It independently constructs/validates groups, uses breadth-level distance expansion, and computes quotient distances directly on coset graphs rather than defining them as a minimum of already-known ambient distances. It includes nonnormal Schreier cases; symmetric and positive split comparisons; arbitrary-generator reverse saturation; nonsplit C4, C6, Q8 and Q16 factor-set comparisons; twisted-action/cocycle identities; normal/conjugacy bounds; and fixed-conjugator inverse formulas. Q16 supplies four normalized sections that are not actions. Integer normal-form windows and finite S_n controls supplement separate all-integer/support proofs; they do not establish their infinite conclusions by extrapolation.

| Checker | Actual scope and review finding |
|---|---|
| `finite_groups.py` | Exact table constructors and directed BFS; identity index 0 is valid for its enumerations; no infinite certification |
| `verify_turn1.py` | Exhaustive finite subsets and symmetric cores; Z windows check lower bound/attainment only |
| `verify_turn2.py` | Exhaustive finite subgroups, including nonnormal ones, positive Schreier generation/costs; normal quotient bounds |
| `verify_turn3.py` | Finite cyclic inversion saturation, positive comparisons and invariant equality; integer dihedral windows rather than the overstated extra finite scan |
| `verify_turn4.py` | Conjugacy-invariant permutation sets and normal widths, D8 conjugacy-cost bounds, local finite dihedral equality; no test of fixed-conjugator theorem until this independent audit |
| `final_review/independent_check.py` | Small finite dihedral subsets plus finite Cartesian controls; reproduced; Turn5 Cartesian scope left to the other family |
| `REPLAY_ALL.py` | Hash/byte bindings and five finite-control subprocesses; optional source hashes; not a proof checker |
| `verify_review.py` | Additional review-manifest binding and known-count assertions; its historical `PASS_SCOPED` output is not current PR acceptance |

`TURN_3_CONTROL_CLARIFICATION.md` is accurate: the extra Turn3 controls are integer normal-form windows; the finite subset scan controls inequalities. Turn4 adds local finite r^{−3} length checks for a specified finite set. Neither substitutes cyclic wrap-around for the infinite lower bound.

Prior `final_review/REVIEW.md` agrees with the independently reconstructed core algebra. Its broad “no further mandatory mathematical correction” does not remove the additive extension-route clarification above or current PR387-dependent disposition. No previous verdict was used as evidence for a theorem. This audit did not mutate candidate files, checkout/index/Git state, PRs, or published findings; no sixth author search or external communication occurred.

## Reproduce and interpret

Run `python3 independent_controls.py` from this review folder and compare its JSON stdout to `INDEPENDENT_CONTROLS.json`. `AUTHOR_REPLAY_SUMMARY.json` records the exact source replay outputs and frozen hashes. `INPUT_BINDINGS.json` binds all audited inputs; `RESEARCH_LOG.md` records checkpoints and audit-completion estimates.

A complete mathematical resolution still requires either a genuine monoid-generating S with unbounded positive/inverse costs in a group whose every group-generating set is bounded, or a universal proof excluding one. The frozen packet supplies neither. Audit completion: 100% of assigned Turn1–4 reconstruction/control review; discovery progress is not inferred from that percentage. Acceptance remains pending PR387 and any revised-head review.
