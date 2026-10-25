# Independent adversarial review — Zenodo 22089551, version 1.2.4

## Verdict and exact scope

**PASS: no substantive mathematical defect or unresolved proof gap found in the reviewed main manuscript and supplementary note.**

The strongest reviewed result is Theorem 2.1 and Corollary 2.3 with their full quantifiers: for every finite weakly reversible stochastic mass-action network with one linkage class and every complex of molecularity at most two, every fixed positive rate vector and every initial population give a closed communicating reachability class. On each nonabsorbing class the minimal population CTMC is nonexplosive and positive recurrent, hence has a unique stationary probability distribution. An absorbing singleton has its point-mass stationary law. The argument also proves positive recurrence of the genuine-jump embedded chain and of its reachable target augmentation on an infinite class.

Separately, Lemma 2.2 correctly establishes symmetric reachability and closedness for arbitrary weakly reversible reaction networks, including multiple linkage classes and higher molecularity. This combinatorial statement is already in the cited literature and is not itself probabilistic recurrence.

This verdict is an independent mathematical and computational review, not a formal proof certification or external human peer review. No source repair was made. No publication action was taken.

## Reviewed identity and independence

- Main PDF: `paper-v1.2.4.pdf`, 16 pages, SHA-256 `1df7ec1e4596680e229c0316fad20d46b276fead4cf642ac40e47182e14cd7f4`.
- Supplementary PDF: `supplementary-note-v1.2.4.pdf`, 2 pages, SHA-256 `8838eefbb4233f0cbaba988544c060efd483b94f6ab69781b2f7023134733d98`.
- Source ZIP: `bimolecular-positive-recurrence-v1.2.4.zip`, SHA-256 `1f5983ebe6251a87fa5b1657d1934e2d7d6e13b1fad7bb5e53201c1a9ceecbbb`.
- Both published PDFs were read completely. The decisive top-complex page and supplementary return/physical-time page were additionally rendered and visually inspected. The corresponding mathematical source and executable support were inspected; actual archived tests were freshly executed in an isolated temporary directory under this review folder.
- No archived reviewer opinions, revision-audit verdicts, or current parallel-review conclusions were read. New controls import none of the archived mathematical implementation.
- Work is confined to `reviews/adversarial`. No website, spreadsheet, Git, Zenodo, external communication, or outreach changes.

## Adversarial examination of the proof

### 1. Closed classes, boundary states, and genuine channels

For an enabled channel (y\to y'), the representation (x=\rho+y) has \(\rho\ge0\). A directed return path from (y') to (y) lifts exactly to populations \(\rho+z_j\); each source is present and the original population is recovered. Weak reversibility is enough for this argument. It remains valid on coordinate faces, in parity-restricted classes, and with the zero complex. Consequently the reachability set is a communicating class and is closed. No assumption that a state first enters a closed class is hidden in the theorem.

The treatment of self-channels is necessary and correct. A self-channel contributes nothing to the population generator and is discarded before defining jump counts or total genuine rates. If the complex graph has more than one vertex and is strongly connected, deletion of self-channels leaves every vertex with a genuine outgoing edge and preserves the paths used in the proof. The one-vertex case is handled as absorbing. Exact parallel channels may be aggregated by summing their positive rates; equal displacement alone is not enough to aggregate channels for the marked proof. The manuscript and supplement preserve that distinction.

Finite nonabsorbing classes require no infinite-state Lyapunov argument. All genuine rates are finite at each finite population, and finite irreducibility gives finite positive return times. If no genuine channel is enabled, weak-reversibility closure forces an absorbing singleton. No excluded boundary state is silently treated as an interior state.

### 2. The marked chain and residual factorial potential

The target of the preceding actual channel is present at the post-jump population: (x\ge t\). Thus the residual \(\rho=x-t\) is always nonnegative. Given the next actual channel (s\to u\), the new residual is exactly (x-s\), independent of (u\). The ratio of residual factorial products therefore gives

\[
\Delta V=\log\frac{(x)_t}{(x)_s}.
\]

Following a channel whose source equals the carried target has exactly zero reward. This is an algebraic identity, not an asymptotic cancellation, and it does not require a positive lower bound on any population coordinate.

The proof that the reachable augmentation is irreducible is sound: a target witness supplies a genuine predecessor for the desired marked state; population irreducibility reaches that predecessor, then the witnessing channel produces the desired mark. Every population in a nonabsorbing class has such an incoming witness, using an outgoing jump and a return path if needed. The projection law depends only on population, so later projection arguments are legitimate.

Although (\log(0!)=\log(1!)=0\), this does not invalidate properness or the global-minimum argument. There are only finitely many coordinates and target complexes; bounding the sum of log-factorials bounds every residual coordinate. Hence every potential sublevel in the reachable augmentation is finite.

The source-probability rewrite has the correct sign on both rate terms. Disabled sources are omitted, the carried target has strictly positive probability, and the entropy term is bounded by \(\log|\mathcal C|\). The result \(\delta\le\log p_x(t)+C_0\) is uniform in population for each fixed positive rate vector. The constant is allowed to depend on that vector.

### 3. Episodes and arbitrarily separated reaction-rate scales

Strong connectivity supplies a fixed simple path for every ordered target-terminal pair. The episode stops after the first channel that differs from the designated channel, or after one ordinary jump from the terminal. This is a stopping time for the labelled-channel filtration and takes between one and \(|\mathcal C|\) genuine jumps. Even a different channel with zero immediate reward is allowed to terminate the episode; the recursion remains valid.

At each continuing phase the population is \(\rho+y_k\), the residual stays \(\rho\), and the continuation probability is exactly (q_kp_k\). No generator coefficient is changed. The recursion

\[
J_k=\delta_k+q_kp_kJ_{k+1}
\]

counts both continuing and stopping branches correctly because the designated edge's immediate reward is zero.

The scalar supremum is correct on both branches. Its critical point is (p=(-qM)^{-1}\) when (M<-1/q\); otherwise the maximum is at (p=1\). It is nondecreasing in (M\) and tends to \(-\infty\) as (M\to-\infty\). Thus terminal rarity propagates backward through any fixed finite path even when intermediate source probabilities tend to zero at unrelated rates. In particular, the argument does not assume a uniform positive probability of successfully following the whole path. This addresses the principal potential fast/slow gap.

### 4. Compactification and the bimolecular top-complex alternative

The subsequence extraction is valid on the countable lattice: with a fixed carried target, each residual coordinate can be made constant or divergent, and at least one must diverge. Dividing its coordinate logarithms by their sum gives nonnegative weights of total one. A coordinate can diverge while receiving zero limiting weight; it remains in the divergent set (I\). The proof keeps this distinction throughout.

For enabled complexes, the stated falling-factorial logarithmic asymptotic is correct for both unit and double stoichiometric entries. Fixed bounded coordinates contribute finite constants only after enabledness has been checked, so logarithms of zero are never used. A strict height gap therefore forces a diverging ratio despite any unresolved equal-height slower scales.

I checked all three branches of Lemma 5.3:

1. If every complex has the same height, (w\cdot X\) is an exact nonnegative invariant. Since some positive-weight coordinate diverges, it cannot stay constant in the fixed communicating class.
2. If a top complex has two particles on divergent coordinates, bimolecularity leaves no bounded reactant. Its source is eventually enabled over every terminal complex, including a doubled species requiring two copies.
3. Otherwise each top complex has precisely one divergent particle. That particle has weight (h_*\), so the represented set (J\) characterizes top complexes by exactly one (J\)-particle. A top unary complex is automatically enabled. If all top complexes are mixed, each has exactly one bounded companion. A lower complex containing a companion supplies it at the terminal lift. If no lower complex does so, the signed functional \(\sum_{i\in J}x_i-\sum_{D\in\mathcal D}x_D\) is zero on every complex. Its positive part diverges and its negative coordinates are fixed, yielding the exact invariant contradiction.

This last signed invariant is not assumed nonnegative on the state space; only its behavior along the extracted subsequence is needed. Counting each distinct companion once is correct because binary top complexes contain exactly one companion particle. An absent species is itself invariant, so it cannot create an unhandled divergent direction. No additional pure-unary or pure-double complex hypothesis appears in this proof.

The exhaustive branch proof applies to real weights, not only the rational weights used in the finite controls. The controls are separately labelled below and do not establish this universal step by sampling.

### 5. From subsequences to a finite drift-exception set

Every invariant conclusion contradicts the fixed class, while every availability conclusion supplies one fixed terminal complex with source probability tending to zero. The target can be fixed by passing to a subsequence because the target set is finite. The corresponding path is fixed in advance. Propagation then gives one episode drift tending to \(-\infty\).

If the exceptional set (K=\{\min_cD_c>-1\}\) were infinite, properness permits a sequence in it with potential tending to infinity. Applying the preceding extraction contradicts its defining inequality. This is a valid compactness contradiction, without requiring explicit enumeration or an effective radius for (K\).

Nonemptiness follows from a global potential minimizer: every possible endpoint is in the same reachable augmentation and has at least the minimum potential. The minimizer exists by the finite-sublevel argument. Thus no theorem is applied to an empty target set. Outside (K\), a deterministic minimizing terminal can be selected measurably on the countable state space. Its stopping time has bounded length and expected drift at most \(-1\).

The correct quantifier is: for each fixed network, positive rate vector, and reachable class, a finite (K\) exists. There is no assertion of one (K\) uniform over rates or all classes. The paper's rate-degeneration and attenuation examples correctly illustrate this limit.

### 6. Hitting, positive return, and integrability

At episode endpoints, (V(Y_{n\wedge\sigma_K})+(n\wedge\sigma_K)\) is a nonnegative supermartingale. Integrability at every finite number of episodes follows from the deterministic coordinate overshoot bound and finite branching. Therefore bounded stopping followed by monotone convergence gives (E\sigma_K\le V(z)\). There is no unjustified optional-stopping passage to an unbounded time.

This gives finite expected hitting of (K\) in original jumps because each episode has at most \(|\mathcal C|\) jumps. From a state in (K\), taking one ordinary genuine jump before applying the hitting bound gives a positive return to (K\), not merely a zero-time hit. Its expectation is finite because each state has finitely many channel successors. Maximizing these expectations over finite (K\) gives a finite (B\).

The trace chain on (K\) is irreducible: any original augmented path gives a trace path after retaining its intermediate (K\)-visits. Finiteness yields a positive finite-block probability of reaching a selected trace state; hence its positive trace return count has finite mean. Expanding trace excursions is valid via Tonelli and conditional expectation on the sigma-field at each excursion's start. The event that the return count has not yet finished is measurable there. Independence of the excursion lengths is not assumed. This establishes finite expected positive return in the augmented chain. Projection gives a population return no later than that marked return, with the correct population-chain law.

### 7. Nonexplosion and physical return times

The embedded chain is constructed before physical time, so the argument is not circular. Recurrent visits to one population state (x_*\) produce an infinite subsequence of independent holding times with the same finite positive exponential rate. Their sum diverges almost surely, forcing the total physical jump time to diverge. Neither an upper bound on all rates nor an unjustified global bounded-rate assumption is needed.

For finite mean physical return, a distinct fact is used: every state in a nonabsorbing class enables a genuine channel, and every positive falling factorial is an integer at least one. Thus \(\Lambda(x)\ge\kappa_{\min}>0\) for the fixed finite positive rate vector. Tonelli gives (E T^+_{x_*}\le E N/\kappa_{\min}<\infty\). The roles of finite rate at the recurrent state and uniform lower rate across the class are correctly separated.

The occupation measure is normalized by a finite positive mean cycle length and is stationary under the usual regenerative construction. The supplement's entry/departure balance is consistent with that construction; it does not replace nonexplosion by a merely formal solution to the stationary equations. Irreducibility gives uniqueness within the fixed class. The finite and absorbing reductions cover all initial populations.

### 8. Restrictions that the proof does not remove

- Multiple linkage classes: the selected rare terminal can lie outside the carried target's linkage class; the needed directed path is then unavailable. Closure still holds, but this recurrence proof does not cover the extension.
- Higher molecularity: top complexes may contain additional bounded companions with multiplicities, invalidating the binary availability/invariant split as written.
- Zero rate constants: the fixed graph's positive-probability paths and uniform positive (\kappa_{\min}\) can fail. The theorem explicitly assumes positivity.
- Quantitative tails, mixing rates, exponential ergodicity, and moments of unbounded count observables are not established. Positive recurrence alone is not enough for those statements.
- No empirical biochemical prediction or claim that every biological network satisfies the graph hypotheses is inferred.

## Independent computations and archived reproduction

The unmodified archived reproducer passed **57 tests**, produced two byte-identical canonical reports, and matched the committed canonical report, SHA-256 `dc14127494eaa6ccf3b36a91f5d714ba6f79e76476f8d199760bd3b5faeed586`, under CPython 3.14.6. Its temporary directory was located under this review folder; source files were not changed.

New standard-library-only `fresh_controls.py`, which imports no archived code, checks:

- 18,360 exact rational target/source factorial identities, including disabled-source exclusions, zero coordinates, and double complexes;
- 486 actual lifted complex cycles at boundary populations;
- 77,748 combinations of three-species complex subsets, 43 rational normalized weights, and valid divergent sets. This includes 33,759 cases where a zero-weight coordinate remains divergent. The checker directly searches for a strict-height available source/terminal pair or an invariant witness, rather than repeating the manuscript's branch classifier;
- 3,000 deterministic additional cases in four through seven dimensions;
- direct terminal-branch episode sums in the missing-pure-(A\) boundary example, the fixed-population vanishing-rate example, and unit-rate double-species cycles with two through six species;
- exact stationary balance on the parity class \(\{(4,0),(2,2),(0,4)\}\) of (2A\rightleftarrows2B\) with rates 2 and 3, giving stationary weights \((9,36,4)/49\), alongside the absorbing state \((1,0)\).

The first version of my attenuation control imposed a relative tolerance at (N=10^8\) that was unjustified for the small coefficient at larger (d\). The manuscript states (O_d(\log N/N)\), not a dimension-uniform relative bound. Direct calculation gave relative error about (5.05\times10^{-5}\) at (d=6,N=10^8\), falling to (3.36\times10^{-9}\) at (N=10^{12}\). Raising the control's scale confirmed the stated asymptotic. The initial failed control log is retained; this was not a defect in the paper and no paper code or assertion was repaired.

These computations are falsification controls and reproduction evidence. They do not prove recurrence by finite sampling, enumerate the analytic set (K\), or bound its radius. The universal result rests on the analytic argument reviewed above.

## Primary-source verification

1. [Anderson–Cappelletti–Kim, author-hosted manuscript](https://people.math.wisc.edu/~dfanderson/papers/ACK2019.pdf): Theorem 4.1 explicitly assumes a pure unary/double complex for every species. Example 4.1 matches the network and unshifted entropy drift used in the reviewed manuscript. Theorem 3.1 gives the embedded-positive-recurrence and positive-lower-rate conversion used here; the new manuscript also supplies its own proof.
2. [Paulevé–Craciun–Koeppl, published paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC3835780/): Lemmas 4.5–4.6 establish reversibility of accessibility for weakly reversible discrete reaction networks. Their terminology is combinatorial and does not by itself imply stochastic positive recurrence. The manuscript distinguishes this correctly.
3. [Norris, *Markov Chains*, primary book text](https://cape.fcfm.buap.mx/jdzf/cursos/procesos/libros/norris.pdf): Theorem 2.7.1(iii), printed pp. 90–91, verifies nonexplosion from recurrence of the embedded chain. Theorems 3.5.3 and 3.5.5, pp. 118–121, give the positive-return/invariant-distribution and stationary-measure interfaces with the required irreducibility and nonexplosion. The hypotheses hold here. The chapter's warning about formal invariant distributions for explosive chains does not apply because nonexplosion is proved first.
4. [Xu, arXiv:2409.05340v2](https://arxiv.org/html/2409.05340v2): Theorem 4.6 includes nonexplosion for second-order weakly reversible systems; Theorem 4.13 relates recurrence to stationary-law existence. This is not a prior proof of the present single-linkage recurrence statement without the pure-species condition. The discussion records the broader bimolecular recurrence problem as open.
5. [ConStRAINeD project results page](https://constrained.polito.it/publications/), checked during this review: it announces a complete two-species proof while listing the five-author manuscript under “In preparation.” That is consistent with the reviewed paper's cautious distinction between two-species and arbitrarily-many-species results. No exhaustive global priority certification is claimed.

The crucial stochastic stopping, trace, and physical-time arguments are explicitly proved in the manuscript, so the conclusion does not depend on importing an unstated version of a general sampled-chain Foster theorem. The supplement clarifies the same interfaces and introduces no stronger unsupported recurrence claim.

## Artifacts and reproducibility boundaries

- `input_identity.json`: exact hashes of both reviewed PDFs.
- `fresh_controls.py`, `fresh_controls.json`, `fresh_controls.log`: independent controls and results.
- `archived_reproduction.log`: unmodified archived test/reproducer output.
- `initial_control_tolerance.log`: retained diagnostic for the review-only numerical tolerance issue.
- `reference_hashes.json`: exact local input and executable-source hashes plus primary-source URLs.
- `verdict.json`, `RESEARCH_LOG.md`: structured conclusion and timestamped completion checkpoints.

Run `python3 fresh_controls.py` from this directory to reproduce the new controls. The archived run used `bash ../../sources/published-source/bimolecular_positive_recurrence_submission_v1_2_4/code/reproduce.sh` with `TMPDIR` set to this review directory's `tmp/`. Generated images and temporary caches are ignored locally. No simulation is used as evidence of the universal theorem, and no external expert approval is asserted.
