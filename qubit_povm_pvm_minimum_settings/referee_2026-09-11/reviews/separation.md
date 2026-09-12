# Independent referee report: separation and strengthened witness

Date: 2026-09-11 (America/Los_Angeles). Checkpoint completion estimate: **100% of this assigned separation audit**, not a percentage of the entire paper's formalization. This review reads the Lean proof sources and primary paper directly. The root referee separately runs Lean compilation/kernel checks. No production sources were modified. All cited line ranges were rechecked against the original `bell_lean/Bell/` and `paper/` sources after the initial review; they do not refer to audit working copies. `ProjectiveFiber.lean` belongs to the independently assigned incidence review.

## Verdict

**The separation theorem endpoints and Appendix B attained lower bound have faithful, unconditional proof sources.** In particular, the PVM bound quantifies over actual complex two-qubit states and actual PVMs; it does not assume the conclusion or an unsupported scalar feasibility model. An exact operator sum-of-squares certificate proves the stronger bound `289/10`, from which the paper's weaker `U` follows. I found no mathematical or semantic defect in this separation route.

**It would nevertheless be inaccurate to say this formalizes every mathematical assertion in §3 and Appendices A/B.** Several analytic intermediate assertions and some secondary conclusions are absent as Lean theorems. These omissions do not undermine the separation theorem, because the formal proof uses a materially different, stronger upper-bound mechanism.

## Endpoint and coefficient correspondence

| Primary paper claim | Actual Lean evidence | Assessment |
| --- | --- | --- |
| Bell functional, `paper/main.tex:413–433` | `Bell/Witness.lean:188–198`, especially `bellScore` | Exact match: Alice signs `(+,−,+)`, Bob signs `(+,−)`, four CHSH coefficients `10,10,10,−10`, auxiliary terms `3/5 p(0,0|2,0) + 3/5 p(1,1|2,0) + 4/5 p(2,0|2,1)`. Lean argument order is `p x y a b`. |
| Common-label `(3,3,3)`-by-`(2,2)` presentation, `main.tex:422–425` | `Witness.lean:141–154` | The witness has zero third effects on the first two Alice inputs; the upper bound covers all three-output PVMs on those inputs. Thus the formal domain is at least as broad as needed for the declared architecture. |
| Simple physical strategy, `main.tex:463–491` | `Witness.lean:19–128,147–186` | Matrix entries match exactly. Positivity is proved by explicit Gram factors, normalization separately, and nonprojectivity by `aux0 * aux0 ≠ aux0` at line 97. |
| Bell-state trace identity and attained value, `main.tex:493–508` | `Witness.lean:131–138,206–238` | Arbitrary complex local operators in the trace identity; three exact auxiliary probabilities `8/25`; four exact correlations; `witness_value` proves `bellScore witnessBehavior = lower`. |
| Exact radical bounds and paper gap, `main.tex:443–459` | `Scalars.lean:16–39`; `ProjectiveBound.lean:165–201` | `lower`, `upper`, exact gap `3(2−√2)/250`, strictness, physical PVM upper bound, convex-hull extension, and strict separation are all supplied. |
| Ideal discrimination POVM optimum `16/25`, `main.tex:511–531` | `Discrimination.lean:18–89` | Correct score matrices and dual matrix; all three dual slacks are PSD; complementarity; bound for every complex ternary POVM; attainment. |
| Appendix B attained value `(16+8√7813)/25`, `appendices.tex:90–158` | `StrengthenedWitness.lean:16–209`; `Scalars.lean:188–205` | Explicit physical strategy, normalized pure state, normalized positive effects, exact value. Strict comparison is proved through the stronger intermediate claim `lower < strengthenedLower`. |
| Family upper bound for `f(η)`, `appendices.tex:161–173` | `Scalars.lean:209–224` | Correct scalar inequality for every `0 ≤ η ≤ 1`, proved by a square certificate instead of differentiation. |

The relevant target interfaces are real propositions, not assumed axioms: `Targets.lean:47–48` defines the physical projective bound and `Targets.lean:66–67` defines strengthened attainment. Actual inhabitants appear at `ProjectiveBound.lean:185–187` and `StrengthenedWitness.lean:208–209`. Historical conditional assembly helpers in `Targets.lean` are not the final separation proof.

## Full PVM coverage and independent certificate check

The physical chain is complete:

1. `ProjectionSupport.lean:17–62` proves a ternary qubit PVM has a zero effect. The proof uses entrywise Cayley–Hamilton, orthogonality, and normalization: three nonzero mutually orthogonal idempotents would each have trace one, contradicting trace two.
2. `ProjectionSupport.lean:65–94` constructs Hermitian involutions from arbitrary projections, including `0` and `I`. Hence deterministic observables and all scalar degeneracies are retained.
3. `ProjectiveBound.lean:22–79` derives the Bell operator from the actual Born behavior and actual signed effects, without assuming a scalar representation.
4. `ProjectiveBound.lean:108–150` proves three explicit operator identities for zero positions 1, 2, and 0 respectively. Zero position 0 uses a CHSH-preserving switch: Alice observables become `(-A1,−A0,A2)` and Bob becomes `(-B0,B1)`. Singleton supports have two zero positions and are automatically included.
5. `ProjectiveSOS.lean:58–75` proves `289/10 I − bell02 = gram Q words`; `SOSCertificate.lean:57–63` proves all rational pivots positive and the exact LDL coefficient factorization. `SOSAlgebra.lean:40–73` turns that into nonnegative expectations for every positive complex density matrix.
6. The remaining `{0,1}` pair has an explicit three-square decomposition plus positive `1/70 I` remainder at `ProjectiveSOS.lean:88–117`.
7. `ProjectiveBound.lean:153–163` applies the complete zero-position disjunction. Lines 189–192 extend the bound to the actual convex hull through linearity. Thus neither mixed states nor shared randomness are omitted.

I wrote a separate standard-library exact checker at `referee_2026-09-11/computations/separation_exact.py`. It parses the coefficient matrix, LDL factor, and pivots directly from the current Lean source, without reading the repository's JSON certificate or earlier receipts. It checks all 144 rational LDL entries and 12 strictly positive pivots. Separately, it expands the Gram expression in the free involution algebra on each party, keeping noncommutative word order within each party and commuting only Alice with Bob. It reproduces **exactly** the 10 nonzero coefficients of `289/10 I − 10 CHSH − (3/5)P⊗B0+ − (4/5)(I−P)⊗B1+`, independently specified from the paper's Bell functional. Perturbing one coefficient by `1/600` is rejected. Results are in `computations/separation_exact_result.json`.

This check is stronger than random numerical testing: the identity is verified symbolically in a universal algebra, and positivity is exact rational LDL positivity. It is independent supporting evidence, not a replacement for kernel checking.

The resulting numerical ordering is `289/10 < U < L0 < L1`. The exact formal margin theorem `ProjectiveBound.lean:203–209` proves the simple witness exceeds every convexified PVM value by more than `1/50`. Neither paper nor Lean claims the upper bound or either attained lower bound is the global optimum.

## Mathematical assertions not individually formalized

### 1. Physical derivation of the paper's analytic projective estimate

The physical Schmidt/CHSH reduction in `main.tex:537–591`, the steered-score trace-norm formula and physical discrimination reduction in `main.tex:594–642`, and the determinant/trace-norm derivation in `appendices.tex:7–34` are not proved as this analytic chain in the reviewed Lean sources. `Scalars.lean:149–155` explicitly assumes the scalar relations and upper bounds needed by `global_upper_from_deficits`; the file's own comment at lines 146–148 correctly says the end-to-end proof uses the separate SOS route. Searches find no use of `global_upper_from_deficits` or `robust_pair_bound` outside their definitions and axiom audit listing.

The scalar polynomial identities and robust box inequality **are** proved (`Scalars.lean:49–141`), and the completion-of-square endpoint **is** proved from stated scalar hypotheses (`Scalars.lean:143–185`). This is a formal-coverage omission in the paper's chosen derivation, not an unsupported premise of the actual theorem. Suggested description: “The main separation theorem is formalized using a stronger SOS upper bound; selected scalar algebra from the paper's analytic proof is also formalized.”

### 2. Ideal discrimination PVM bound `3/5` and advantage `1/25`

The assertion at `main.tex:532–533` has no corresponding projective-discrimination theorem in `Discrimination.lean`, which ends after POVM attainment at line 89. The full Bell SOS upper bound does not directly imply the sharper ideal auxiliary bound `3/5`.

Independent mathematical verification: singleton scores are the traces `3/10,3/10,2/5`. For pair `{0,1}`, the score is at most `(3/5 + 3/5)/2 = 3/5`. For each pair involving label 2, the trace sum is `7/10` and the trace norm of the difference is `1/2`, giving `(7/10 + 1/2)/2 = 3/5`. The usual binary projector maximization follows by diagonalizing the Hermitian difference and choosing its positive eigenspace. These exact trace/determinant computations are independently checked in `separation_exact.py`. Thus the paper assertion is correct, but its formalization is missing. With POVM optimum `16/25`, the gap is exactly `1/25`.

### 3. Strengthened strategy's dual certificate

`appendices.tex:133–145` asserts a particular dual matrix dominates the three scores and annihilates the effect ranges. `StrengthenedWitness.lean:158–203` instead directly expands and evaluates the actual Born score; it does not define that dual matrix or prove its slack/complementarity assertions. This does not affect attained-value certification.

Independent direct verification: write the positive state coefficients as `a,b` and `k=3b/(5a)`. The scores are `K0=(3/10)(a,b)(a,b)^T`, `K1=(3/10)(a,−b)(a,−b)^T`, `K2=diag((4/5)a²,0)`. With `Γ=diag((4/5)a²,(12/25)b²)`, the slacks are

```
Γ−K0 = (1/50)(5a,−3b)(5a,−3b)^T,
Γ−K1 = (1/50)(5a, 3b)(5a, 3b)^T,
Γ−K2 = diag(0,(12/25)b²).
```

All are PSD; the first two annihilate the corresponding effect vectors `(k,1)` and `(k,−1)` because `5ak=3b`; the third annihilates the support of `M2`. This fills the paper's algebraic check in referee prose, but is not a new Lean proof.

### 4. Family derivatives, unique critical point, and equivalent radical coordinates

`Scalars.strengthened_family_bound` proves the family bound, not the derivative formulas or uniqueness assertion in `appendices.tex:168–171`, nor an explicit equality-at-`η=1/√7813` theorem for that scalar function. These are distinct from the separately proved attained physical value.

The family bound proof nevertheless contains a short independent route to uniqueness: its square deficit is `(4√(2−η²)−500η)²`; equality forces `√(2−η²)=125η`, hence `η²=1/7813`, and `η≥0` selects `η=1/√7813`. At that value the square vanishes. The derivative formulas are elementary and consistent.

The Lean witness uses `x=2qab/125` instead of `6√217/125`, and `k=3b/(5a)` instead of the paper's nested square root (`StrengthenedWitness.lean:16–21`). These are semantically identical: positivity and `q²(ab)²=1953` (`:64–68`) give `(2qab)²=7812=36·217`, so `2qab=6√217`; positivity and `b²/a²=(q−1)/(q+1)` give the asserted `k`. No explicit theorem names these two coordinate equalities, but the independently checked physical strategy and exact score suffice for the endpoint.

### 5. Minor descriptive matrix facts

The simple measurement's specific nonzero eigenvalues at `main.tex:490–491` are not individually stated as Lean spectral equalities; positive Gram factors, normalization, and failure of idempotence are proved instead. The eigenvalues follow directly from rank one plus traces `17/25,17/25,16/25`. Likewise Appendix B's explicit rank-one designation is stronger wording than the positivity/normalization needed and proved for the physical attainment construction.

## Recommended referee disposition for this portion

Accept the separation and strengthened-attainment **mathematical endpoint correspondence**, contingent only on the root referee's fresh successful kernel checks of these actual sources. Revise any blanket “all mathematical statements in the paper are formalized” claim to acknowledge the listed coverage omissions, or add those secondary theorem statements. No production repair is required to the separation endpoint proof based on this review.
