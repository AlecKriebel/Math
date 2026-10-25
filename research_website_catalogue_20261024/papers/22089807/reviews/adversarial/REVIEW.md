# Independent adversarial review: Zenodo 22089807

Completed 2026-10-25 UTC. Reviewer role: adversarial mathematical review, performed independently before consulting any current sibling-review opinions. Completion: **100% of the assigned review**, not a percentage proof of correctness. No current analytic/scope conclusions were read. No external individuals were contacted, no outreach was prepared, and no submitted source was edited.

## Verdict

**No substantive mathematical fault or unresolved central gap found in the stated theorem.** The literal claim is supported by the reviewed argument: one effectively specified, fitness-independent sequence of finite connected loopless undirected weighted graphs eventually beats the same-order complete graph under each of the two ordinary Moran update rules, for every *fixed* fitness in `(1,R_hyb)`. Here `R_hyb=1.5028569127905696…` is the specified sextic root. This is a lower bound on `R_sim`, not an unrestricted optimality theorem.

The strongest verified result is the paper's pointwise-in-fitness eventual simultaneous amplification theorem, with the rational specialization also supported. The finite certificates do not prove the population asymptotics: those were checked as analytic arguments. No endpoint amplification at `R_hyb`, uniform population cutoff all the way to `r=1`, nonvanishing asymptotic gain, or graph-uniform high-fitness upper bound follows. The exact unrestricted value of `R_sim` remains open, as the paper states.

**Suggested follow-up: null.** The assignment exposed no concrete research continuation that clears the requested high bar. Routine metadata cleanup is noted below and is not an authorization to change the published artifacts.

## Source binding and independence

`SOURCE_BINDING.json` binds the fresh Zenodo raw/normalized record, receipt, both archive objects, all 23 tar members, both 21-page PDFs, their extracted page-text hashes, and primary PDFs used for model/theorem interfaces. The standalone PDF is 214040 bytes, SHA-256 `1d6d1d31a782776b07b9240467f02d624b47dcde5c83f4740a192136c2dfb8e3`; the tarball is 6952578 bytes, SHA-256 `e5b61e79d065a9abec0908e28db7e79366b5fccedeb6efbf22eadd7af3cc57ae`. The embedded PDF is 214136 bytes, SHA-256 `1e73984abfd64a45797b8ad6dc8b473d82a8d5eb8061efe470a1e603c2d10ad9`.

The entire standalone mathematical text was read, against the full `main.tex` proof. Both actual PDF readers were independently extracted and diffed; their only text deltas are the date on page 1, figure-label line placement on page 4, and a blank line. All 21 standalone pages were also rendered and visually scanned in three contact sheets, with pages 12 and 15 and embedded page 4 inspected separately. No mathematical PDF discrepancy was found. `MANIFEST_CHECK.json` records 22 manifest entries with zero mismatches.

The independent standard-library rational program and results were sealed at **2026-10-25T04:35:39.829549+00:00**, before reading or executing the submitted certificates. The proof-first review and independent code did not import submitted solvers or read previous favorable audit reports. `INDEPENDENT_SEAL.json` records those bytes and the chronology. Subsequent documentation and certificates were treated as evidence to audit, not authority for the theorem.

## Literal target, assumptions, and falsifiers

The relevant quantifiers are

`exists {G_t}, for every fixed r in (1,R_hyb), exists t_0(r), for every t >= t_0(r)`.

Each graph must be finite, connected, loopless, undirected, and have nonnegative symmetric weights and positive degrees. Initialization is a uniformly selected **vertex**, not a degree-weighted vertex or a separately chosen favorable start. Bd selects the parent by fitness and then the target by outgoing normalized weight; dB selects the death vertex uniformly and then the parent by incoming weight times fitness. Comparison uses the same `n_t` and the matching update rule on the loopless complete graph.

The core has `C=t^4` vertices, `q=t` heavy pairs and `m=floor(lambda_* t)` hub pendants. The gain scale is `eta=q/C=t^-3`. The key possible falsifiers are: a wrong local denominator; an unaccounted average over initial sites; a center error of order `eta`; a resident-center reversal probability not `o(eta)`; a nonuniform weak-cut limit smuggled across changing population size; an `r`-dependent choice of graph; or an unjustified claim at a zero leading correction. Each was tested below. None produced a central failure.

## Mechanism-by-mechanism attacks

### Ordinary process, normalization, and uniform starts

Equations (1)–(4), pages 2–3, agree with the labelled parent/target event definitions in the actual primary bodies of Svoboda et al. 2024 (model pages 4–5) and Tkadlec et al. 2020 (model pages 3–4 and SI model). In particular, a dead vertex has no self-contribution to its dB competition because the graph is loopless. Multiplying a state's entire changing generator by a positive statewise clock changes holding times but not harmonic fixation probabilities; the paper's suppressed Bd fitness clock is therefore legitimate.

Independent exact labelled-chain solutions on `K_4` reproduced both baselines at `r=1/2,1,3/2,3`. For example, at `r=3/2`, Bd gives `27/65` and dB `27/76`; at neutrality both give `1/4`. This specifically detects the erroneous substitution of the Bd benchmark for the dB benchmark. On the six-vertex hybrid fixture, uniformly averaged fixation is exactly `1/6` at neutrality under both rules, at each tested positive cut and in the separated trace. The paper's factor `(C+m)/N` times the isolated uniformly averaged center probability and `2q/N` times the pair probability accounts correctly for every initial vertex, including leaves.

### Lumping, the zero-cut trace, and event-rate orientation

Lemma 4, page 5, is a valid strong-lumping argument: its automorphism action is transitive on the fibres and preserves both labelled kernels. There is no need to assume independent lineages. At zero cut the fast classes are exactly the module-monomorphic states. The finite mixed-state block has spectral radius below one because each isolated finite connected module absorbs, even when several modules are initially mixed. Resolving a single first-order cross-cut excursion therefore gives the Schur generator in Proposition 5, pages 5–6.

For every **fixed finite** `C,m,q`, the fast resolvent and the interior restriction of the limiting scaled macro system are invertible, continuously in positive fitness on a compact interval. This is enough for compact-uniform weak-cut convergence. No inverse bound uniform in growing `C` is required or claimed by the diagonal construction. An unscaled full absorption-time inverse would diverge as the cut vanishes; the operative bounded inverse here is the scaled Schur boundary-value system.

An independent exact check constructs all 64 labelled states of a graph with `C=3,m=1,q=1,sigma=1/3`, obtains the zero-cut fast generator directly from Moran events, solves its 60-state mixed-module return system over `Fraction`, differentiates the cross-cut events exactly, and compares the resulting four macro transition coefficients against the paper table. It checks both rules at `r=1,3/2,3`. All six comparisons are exact identities at those rational inputs. It also checks all 36 orbit fibres at positive cut. This finite audit is evidence against a normalization/orientation error, not a universal numerical proof; the general rate derivation follows by summing identical pair contributions.

The general Bd table survives direct derivation: a mutant pair has parent-degree sum `I_P`, introduces into all `C` equally weighted core targets, and succeeds with the uniformly averaged core committor. This gives `A=Cr I_P u_core(r)`. Its reverse is `C'=C I_P u_core(1/r)`. Summing resident or mutant center parents into the two pair targets gives `D=2 I_H a_P(1/r)` and `B=2r I_H a_P(r)`. For dB the target-degree denominators move inside the portal functional: `A=2r J_H(r)`, `D=(C/r)J_P(1/r)`, `B=Cr J_P(r)`, `C'=(2/r)J_H(1/r)`. The reciprocal fitness factors in this row are essential and are correct.

### Center establishment and cleanup at the actual gain scale

Proposition 6 and Lemmas 7–9, pages 6–13, supply an error smaller than `eta`, rather than merely `o(1)`. Before the initially resident hub first changes, the ordinary-count odds differ from the complete-core odds by `O(1/C)` for counts below `K=ceil(A_0 log C)`. The chance of a hub interruption over `O(K)` expected ordinary changes is `O(K/C)`. A fixed compact lower fitness bound permits `A_0` to make both geometric tails `o(C^-3/4)`; `K/C` is also `o(C^-3/4)`.

After establishment the ordinary count is not assumed Markov when hidden hub/leaf coordinates move. The pointwise intensity comparison yields a conditional embedded-step bias. Above the fixed boundary layer, the exponential supermartingale and the `O(C)` total jump intensity give exponentially small strip escapes over any fixed polynomial clock horizon. The Lyapunov calculation is only asserted above `R_0`; the paper correctly does not require negative deficit drift at `R=0` with a resident hub.

The Bd pendant synchronization stops at the target **or** upper-strip exit. Giving that exit favorable boundary value makes the committor comparison valid. The leaf trace has `O(m)` expected stopped outcomes and each costs at most `O(C)` expected clock time, hence `O(Cm)`. This avoids the false unstopped expectation that would result from rare eventual core extinction. In the final all-mutant-hub/all-mutant-leaf phase, integrated deficit bounds and Jensen give a fixed positive chance of reaching fixation without hub reversal. The explicit nested-strip strong-Markov blocks, pages 11–12, amplify this fixed success chance to failure `O(C^-B_0)` in polynomial time; no independence between blocks is assumed.

For dB the suppressed-deactivation attempt makes each resident leaf a pure death and the ordinary deficit decay exponentially. The choice `T=beta_0(B_0) log C`, with both coefficient inequalities displayed, gives the claimed coordinate-survival errors. Hub reversal costs `O((R_0+m)/C)=o(1)` per attempt, so only a fixed positive attempt success probability is needed before `O(log C)` regeneration. At a bounded-deficit visit, activation before the next ordinary jump has a positive compact-uniform probability (all these rates are bounded and activation is bounded below); this justifies using activated bounded-deficit attempts even though the deficit can move while the resident hub is waiting. No new asymptotic mechanism is needed for that short omitted detail.

The Bd single-leaf lower comparison uses an attractive graphical construction at `r>1`; deleting mutants and suppressing favorable births is adverse. Repeated hub activation creates a core establishment trial of probability at least constant over `m`, whereas loss of the protected initial pendant costs `O((1+K)/C)` per trial. Their ratio is `O(m(1+K)/C)=o(1)`. Under dB a leaf dies at rate one and its only useful initial hub activation has rate `O(1/C)`. Thus the opposite leaf responses used in the final average are justified.

### Reciprocal invasion and adverse global reversals

Lemma 10's killed ordinary process at fitness `s=1/r<1` has uniformly subcritical odds on a sufficiently small fixed-density interval. Its integrated particle mass is bounded and its high-count occupation tail decays exponentially. Weighting by the actual hub-change intensity gives `O(1/C)` first hub activation and an exponentially tight activated cloud, not merely an unweighted bound on arbitrary states.

Lemma 11, pages 14–15, then improves this coarse bound to the necessary little-oh. Under Bd, a mutant hub with finitely many ordinary mutants and no mutant leaves is lost at rate at least `m`, so its success probability tends to zero. Under dB, the subcritical process with immigration dominates the ordinary cloud until hub loss. Its finite-horizon exponential moment bounds its maximum; the paper splits the finite time horizon from the surviving-hub probability before letting the horizon grow. It does not incorrectly invoke an infinite-horizon maximum bound for a recurrent immigration process. After hub loss, pendant particle time is at most `m` and ordinary particle time is bounded, making reactivation `O((m+a_L)/C)=o(1)` for fixed truncations. The nested limits first fix the truncations as `C` grows and only then remove them. Combining this with the hazard-weighted first-activation tail gives `u_core^Bd(1/r)=o(1/C)` and `J_H(1/r)=o(1/C)`.

Consequently `C'/B=o(1/C)` in each rule, uniformly on a fixed beneficial-fitness compact. Proposition 12's failure bound `q C'/(B+C')=o(q/C)` is valid: failure requires a first center reversal before all resident pairs have converted. There are at most `q` conversions before the first reversal, so repeated reversals need not be counted to obtain this upper bound. Starting from one mutant pair first competes at rates `A,D`, then starts the same controlled sweep. It yields the gates `Z_B=sigma(r^2-1)` and `Z_D=2r(r-1)/sigma` without replacing global fixation by a branching survival approximation.

### Responses, optimization, and fitness-independent coupling

The complete-graph Bd correction to `p=1-1/r` is exponentially small, and the dB correction is `O(1/C)`; both are negligible at `q/C`. The core, pendant, and pair weights in the uniform initial average therefore give equations (41)–(42), page 17. The independent rational code verifies the sextic root counts using its own polynomial remainder/Sturm implementation and the rational margins `232/17361` and `65/12123` at `r=3/2`. The subsequent symbolic certificates agree with the feasibility quadratic, its minimum `-P(r)/(4(r-1))`, the derivative signs, and the rational-family threshold.

At the algebraic tangency `0<sigma_*<1` and `lambda_*>0`. For fixed `sigma_*`, `L` increases and `U` decreases throughout the relevant interval, so choosing `lambda_*=L(R_hyb)=U(R_hyb)` gives strictly positive leading corrections at **every interior fixed** fitness. Positivity cannot be promoted to the zero-leading-correction endpoint. The response optimality proof only excludes an interval extending past the tangency within the displayed fixed-positive-parameter, first-order response model.

The dyadic choice in Lemma 2, page 4, is an effective definition, although computationally enormous. All finite harmonic systems have real-algebraic coefficients rational in fitness. Positivity of the transient determinants/event denominators permits exact interval inequalities. A finite interval's uniform weak-cut convergence guarantees termination of the least-integer search. The chosen interval depends only on `t` and the fixed algebraic threshold, and the same cut must pass both update rules over the whole interval. Thus no fitness is used after the graph has been fixed.

The proof correctly uses two separate limits: first weak-cut convergence for each finite population, then center/pair asymptotics in population size. The diagonal absorbs the lack of a population-uniform weak-cut rate. For any fixed interior `r`, eventually `r` belongs to `I_t`; its strictly positive scaled separated gain exceeds the cut approximation error `1/t`. This proves the stated quantifier order without interchanging limits.

## Boundary and interpretation checks

| Boundary or alternative | Outcome |
|---|---|
| `r=1` | Strict amplification is excluded; exact neutral uniform-average checks tie the benchmark. Response formulas containing `1/(r-1)` are not applied at neutrality. |
| Fixed `r` approaching 1 | Constants and `t_0(r)` may deteriorate. No uniform cutoff to the neutral endpoint is claimed. |
| `r=3/2` | It is interior to `R_hyb`; rational specialization has exact positive margins. |
| `r=R_hyb` | Both first-order corrections vanish; theorem intentionally excludes it. Higher-order terms are not controlled in sign here. |
| Large fixed fitness | The dB first-order response eventually becomes negative. No all-fitness amplification or unrestricted upper bound is asserted. Actual selected cuts are controlled only on the chosen expanding intervals. |
| Zero weak cut | Graph disconnects, so this is an auxiliary limiting trace, not a member of the claimed family. Every chosen dyadic cut is strictly positive. |
| Vanishing gain | Gain is only `Theta(t^-3)` for a fixed interior fitness. This is compatible with strict eventual inequalities and with limiting fixation equal to the well-mixed limit. |
| Degree-weighted initialization | Would change the claim. It is neither used in the paper nor in these comparisons. |
| Fixed-graph high-fitness obstruction | Has `for every G exists R_G`; it cannot refute `exists sequence for every fixed r exists t_0(r)`. |
| Floor in `m` | Changes the scaled coefficient by `O(1/t)` and need not give monotone finite-size behavior. |
| Rational-edge specialization | Internal weights, unit weights, and all selected dyadic cuts are rational; its algebraic endpoint does not make edge weights irrational. |

The primary interfaces were read from actual bodies: Svoboda et al.'s model and Theorem 3 (main and SI) concern the same pure update rules, uniform singleton initialization, and weighted undirected graphs. Tkadlec et al.'s model, Lemma 1 and transience theorem/proof allow weights but require missing support for their stated noncomplete case. The graph here has missing support, so that obstruction applies at each fixed `t`, with a population-dependent bound. The prior 21753405 theorem/corollary and complete-support proof were also read to check the broader background equality-class assertion. These are contextual consistency checks: none supplies the center asymptotics or the main positive theorem by citation.

## Submitted code audit and replay boundary

All authored Python and shell code in the 23-member archive was statically read. The three mathematical certifiers and `verify_paper_claims.py` have explicit checks, reject optimized Python, and have no network or write effects. `verify_paper_claims.py` also checks textual source markers; those checks are packaging guards and were not counted as proof. The lumping fixture has nine vertices, 512 labelled states, and 108 orbit fibres, at one parameter setting.

After the independent seal, only the four substantive certifiers were executed, from byte-identical quarantine. The supplied SymPy 1.14.0 and mpmath 1.3.0 wheel bytes were hash-checked and loaded by zipimport under Python 3.14.6; no installer or bootstrap was run. All four completed successfully; `SUBMITTED_REPLAY.json` preserves their actual output and timing. A separate reviewer-controlled launcher confirmed that all four reject `-O` without a PASS message (`OPTIMIZED_REJECTION.json`). No manuscript builder, archive builder, installer, release wrapper, deployment, or publication action was executed. The supplied full regression script was read but not executed because it invokes builder/bootstrap/release entry points.

The finite checks cannot certify compact-uniform establishment, cleanup, reciprocal invasion, the population limit, or the dyadic algorithm's practical runtime. The proof review above is the evidence for those mathematical steps. The independent finite computations have explicit rational outputs and are reproducible without third-party dependencies; their exact identities should not be confused with a sampled proof of an asymptotic theorem.

## Findings and remaining gap

There is **no substantive fault requiring notification or repair**. The only documentary discrepancy is stale pre-deposit language: page 20, the archive metadata/README, and the source still say no new persistent identifier has been assigned, while the fresh record is DOI `10.5281/zenodo.22089807`, version 2.0.4; the source link names v2.0.3. The standalone and embedded dates also differ as bound above. These should be preserved as provenance facts for this review and do not change the matched mathematical text. No repair was made.

The exact remaining mathematical gap is outside the verified claim: no result here determines the unrestricted simultaneous-amplification threshold, controls equality at `R_hyb`, establishes a useful finite `t_0(r)`, or proves the construction optimal among all graph families. Within the literal main theorem, no unresolved central proof gap was identified. This is an independent adversarial review with reproducible checks, not formal verification or a comprehensive priority certificate.

## Artifact index

- `READ_LEDGER.json`: actual readings, locators, evidence role, and exclusions.
- `SOURCE_BINDING.json`, `MANIFEST_CHECK.json`: immutable input and reader binding.
- `independent/check.py`, `independent/results.json`, `INDEPENDENT_SEAL.json`: pre-certificate exact checks and independence checkpoint.
- `STATIC_CODE_REVIEW.json`, `SUBMITTED_REPLAY.json`, `OPTIMIZED_REJECTION.json`: static audit, byte-identical selected replay, and negative execution checks.
- `RESEARCH_LOG.md`: timestamped checkpoints and completion estimates.
- `VERDICT.json`, `REVIEW_SEAL.json`: concise outcome and final artifact hashes.
