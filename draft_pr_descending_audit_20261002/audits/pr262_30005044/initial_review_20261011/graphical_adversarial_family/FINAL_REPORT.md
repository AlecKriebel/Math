# PR262 / 30005044: graphical-process adversarial audit

**Scoped verdict: GO.** The frozen candidate's simultaneous-infection explosion theorem, explicit annealed lower bound, fitness monotonicity, and almost-sure quenched possibility for every positive infection rate withstand this audit. No blocking mathematical gap was found within the graphical-process family. This is a correctness and model-compatibility judgment, not a novelty judgment or publication authorization.

**Frozen identity:** original commit `c805fbb48db939b82c59609c0b8be6cdcedd40e7`; target tree `430f0d154546eaa33c0b7eeb0ad29718b62968c4`; 16 target leaves. `frozen_integrity_receipt.json` rebuilds all blob/tree hashes using pure hashing and matches this identity. No Git metadata was opened or mutated. No source file or remote was changed. Other reviewers' prose/results were not read; the original supplied checker code was read as code and replayed. Unreviewed frozen payloads were hashed as opaque bytes only.

## 1. Exact hypothesis, assumptions, and success criteria

The candidate defines an offspring law on finite positive integers by

\[
P(\xi=m)=m^{-1/4}-(m+1)^{-1/4},\qquad m\ge1.
\]

It starts the minimal finite-path graphical contact process from the root alone on the corresponding rooted Galton–Watson tree. Recovery marks have rate 1; each ordered adjacent pair has rate-\(\lambda\) arrows for \(F\equiv1\), with \(0<\lambda<\infty\). The quantitative claim is

\[
P\bigl(|X_{\tau}|=\infty\bigr)
\ge {7\over30}e^{-3/(2\lambda)},\qquad \tau={1\over2\lambda}.
\]

Its stronger qualitative claim is: for a probability-one set of trees, every real \(\lambda>0\) has strictly positive quenched probability of an infinite configuration at some finite time. Arbitrary finite fitness assignments bounded below by 1 preserve both claims under the corresponding independent Poisson graphical construction. The quantitative statement is annealed, not a uniform bound conditional on every tree.

Audit success required checkable deductions for all of these claims, not merely a fast first-passage ray or numerical survival evidence. Primary falsification targets were adaptive selection bias, recovery omission, interval/index errors, arrow reversal, infection from infinity, an unjustified infinite-volume limit, and extension of an almost-sure statement across an uncountable parameter set.

## 2. Narrow source/model verification

The original OWR contribution uses iid fitnesses in \([1,\infty)\), rate \(\lambda F_uF_v\), root infection, and unit recovery. Its p. 619 question explicitly removes the finite-mean assumption, and the immediately preceding explanation identifies nonexplosion with finiteness of the infected set at every time. The unbounded-support assumption on fitness belongs to a preceding survival result. Thus constant iid fitness is admissible for the explosion question, and an existential example suffices for its wording. [Official OWR report, printed pp. 618–619](https://ems.press/content/serial-article-files/46949).

The later full author manuscript Definition 2.1 explicitly recovers the classical contact process with \(F=1\). Section 3 constructs independent recovery/infection marks and gives graphical monotonicity; Theorem 3.2 assumes finite offspring mean for its nonexplosion conclusion. The candidate does not contradict that theorem. [Full author manuscript, Definition 2.1 and §3](https://arxiv.org/pdf/2110.14537v4).

Bartha–Komjáthy–Valesin Definition 3.1/equation (19), printed p. 17, defines infection by a finite arrow path with recovery-free vertical segments and explicitly permits finite-time explosion. The candidate adopts exactly this finite-witness convention. The proof below independently establishes its finite-ball equivalence; no survival theorem is being used as an explosion theorem. [Primary graphical-definition source](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0C2D174326F5BB7EFDC7DADE9E768D56/S2050509425101448a.pdf/degreepenalized_contact_processes.pdf).

No priority, novelty, or comprehensive literature audit was attempted. The original target's bibliographic/sign-misprint discussion is immaterial to the deductions checked here.

## 3. Offspring law and local finiteness

The probabilities are strictly positive because \(m^{-1/4}\) strictly decreases. For every integer \(M\ge1\), telescoping gives

\[
\sum_{m=1}^{M}P(\xi=m)=1-(M+1)^{-1/4}\longrightarrow1.
\]

Likewise, summing from \(m\) to \(M\) and taking \(M\to\infty\) gives the claimed tail \(P(\xi\ge m)=m^{-1/4}\). The limit of that tail is zero, so there is no infinite offspring atom. For \(M=16^L\),

\[
E\xi\ge M P(\xi\ge M)=8^L\longrightarrow\infty.
\]

This avoids any question about numerical integration or interchange of a signed series. The exact integer-tail threshold is important: \(P(\xi\ge D_{n+1})\), not \(P(\xi>D_{n+1})\), equals the value used in the proof.

An iid degree field can be indexed by the countable Ulam–Harris label set. Every field value is finite almost surely, simultaneously on that countable set. Induction on generations then shows each generation and each finite root ball is finite. Since \(\xi\ge1\) almost surely, extinction is impossible; and \(P(\xi\ge2)=2^{-1/4}>0\). Both facts are later used, rather than left as generic supercritical-tree assumptions.

## 4. Graphical semantics and finite-volume limit

Fix a locally finite countable tree and a realization of its locally finite Poisson marks. Extend the process on each finite root ball by zero outside that ball. If a ball is enlarged, every existing finite infection path remains available; therefore these infected sets increase at each fixed time. Conversely, any finite path visits finitely many vertices and is contained in some finite ball. Consequently

\[
X_t=\bigcup_{N\ge0}X_t^{B_N}
\]

is precisely the finite-path definition. This equality does not require a globally finite number of marks before \(t\), or a nonexplosive global jump enumeration. Each finite ball has finite total mark rate on a bounded time interval.

Each \(\{v\in X_t^{B_N}\}\) is a measurable finite-system event. The event of infinitely many simultaneous infections is, more explicitly,

\[
\{|X_t|=\infty\}
=\bigcap_{M\ge1}\bigcup_{N\ge0}\{|X_t^{B_N}|\ge M\}.
\]

All limits here are countable. The random tree causes no additional measurability problem: finite rooted labeled tree shapes are countable, and independent Poisson fields can be constructed on the countable universal label set and restricted to present vertices. Conditional probability kernels are therefore measurable functions of the tree. This substantiates the good-tree measurability used in §8 below.

No ball has an infected boundary source. If the initial infected set is empty, every finite-path set is empty; an infinite limiting arrow chain does not create a new initial infection. A path may leave a small ball and return, in which case a larger finite ball captures the full finite witness. The supplied construction needs no such excursions: the witness for \(v_n\) stays in \(B_n\).

Ordered downward arrows are the required arrows. Reverse arrows cannot carry root infection down the tree; adding upward arrows cannot invalidate a downward witness. Some informal source notation groups marks by undirected edges, but the finite-volume transition rates are those of the standard directed-arrow contact process. Moreover, the proof never needs independence between the two orientations of the same edge: it uses only the downward orientation and independence across different tested edges.

## 5. Adaptive ray: exactly what remains independent

The schedules are

\[
D_n=2^{4n+8},\quad \ell_n={2^{-n-2}\over\lambda},\quad
s_n={1-2^{-n}\over2\lambda},\quad \tau={1\over2\lambda}.
\]

At stage \(n\), \(v_n\)'s own degree is already known to be at least \(D_n\), and the first \(D_n\) children consequently exist. At earlier stages the exploration revealed degrees of vertices at levels at most \(n\), together with incoming arrows used to select the ray. It did not reveal degrees of those children's children or outgoing arrows from \(v_n\) to its children.

Condition on the exploration history, not on the entire eventual tree. Split over the countably many possible selected labels. On each such history the newly inspected degree/arrow coordinates are disjoint from the coordinates on which selection depended, so they retain their original product distribution. Conditioning on \(v_n\)'s large degree does not condition its children's iid degrees. Nonselected siblings' exposed degrees also do not change the selected child's descendants. There is no assertion that selected degrees remain unbiased iid variables.

For an inspected child, the actual conditional eligibility probability is

\[
p_n=2^{-n-3}(1-e^{-2^{-n-2}}).
\]

The half-open window has length \(\ell_n\), and \(\lambda\ell_n=2^{-n-2}\in(0,1/4]\). The lower bound \(1-e^{-x}\ge x/2\) on \([0,1]\) follows, for example, from \(f(x)=1-x+x^2/2-e^{-x}\): \(f(0)=f'(0)=0\) and \(f''(x)=1-e^{-x}\ge0\). Hence

\[
p_n\ge2^{-2n-6},\quad D_np_n\ge4^{n+1},\quad
P(\text{stage }n\text{ fails}\mid\text{history})
\le e^{-4^{n+1}}\le16^{-(n+1)}.
\]

The final comparison follows from \(4^{n+1}\ge4(n+1)\) and \(e>2\). The first inequality can be proved inductively: equality holds at \(n=0\), and multiplying the previous bound by four dominates the next linear bound.

Let the first-failure event at \(n\) include successful arrival at that stage. Its conditional probability given the root event is at most the displayed stage bound. These events are disjoint; their countable union is failure at some finite stage. No independence of different stage-success events is needed. Since the root event has probability \(1/4\),

\[
P(G)\ge\frac14\left(1-\sum_{n\ge0}16^{-(n+1)}\right)
=\frac7{30}.
\]

The continuing-success event \(G\) is a countable intersection, and every selected label is a measurable finite-stage function. The degrees of successive selected vertices are strongly biased, but this does not transfer the difficulty into an unsupported independent-ray claim.

## 6. Recovery conditioning and exact endpoints

Let \(\mathcal S\) be the sigma-field generated by the full tree and all arrow marks. On \(G\), the selected ray is fixed after conditioning on \(\mathcal S\). Its vertices are distinct, because every step moves to a child. The recovery fields were never inspected and are independent of \(\mathcal S\), so their conditional law at these distinct selected labels is a product of rate-1 Poisson laws.

For a finite prefix \(v_0,\ldots,v_N\), require no recovery in \([0,\tau]\) at \(v_0\), and in \([s_{n-1},\tau]\) at \(v_n\) for \(1\le n\le N\). The total length is exactly

\[
L_N=\tau+\sum_{n=1}^N\tau2^{-(n-1)}
=3\tau-2\tau2^{-N}.
\]

Thus the conditional finite-prefix probability is \(e^{-L_N}\). The prefix events decrease as \(N\) increases. Continuity from above gives

\[
P(R\mid\mathcal S)=e^{-3\tau}=e^{-3/(2\lambda)}\quad\text{on }G.
\]

This is an exact countable-product argument, not the inference that all individual probabilities being positive makes the infinite conjunction positive. Full-length guards at every vertex would instead have infinite total length and probability zero.

Choose the first eligible arrow time \(a_n\in[s_n,s_{n+1})\). It exists and is a measurable finite-interval Poisson selection on \(G\). The half-open convention gives

\[
a_n<s_{n+1}\le a_{n+1}<\tau,
\]

so all selected arrows are chronologically ordered. A child guard begins at \(s_n\), before or at its incoming arrow \(a_n\); a parent's guard persists through its outgoing arrow and until \(\tau\). Therefore all recovery-free vertical segments required for a finite path are included in the forbidden recovery windows.

Closed recovery windows also forbid recovery exactly at \(\tau\) or an incoming/outgoing endpoint. Poisson marks have no atom at any deterministic schedule endpoint; independent arrow/recovery processes have no coincident mark almost surely. These are countable null-set assertions over the edges/vertices/schedule. The proof's closed guard convention is already sufficient even without invoking those null sets for its witnesses.

## 7. Why the conclusion is simultaneous explosion

For a fixed \(n\), concatenate the \(n\) arrows at \(a_0,\ldots,a_{n-1}\) and their recovery-free vertical segments, ending with the vertical segment at \(v_n\) from \(a_{n-1}\) to \(\tau\). At the root use the segment from time zero to \(a_0\). This is a finite path contained in \(B_n\), with all marks validated by \(R\). It proves \(v_n\in X_\tau^{B_n}\).

On \(G\cap R\), every finite prefix is therefore simultaneously infected at the same deterministic time \(\tau\). Since the ray vertices are distinct, the union process has infinitely many infected vertices. No path with infinitely many jumps is used as a witness to any individual endpoint; no endpoint at infinity is introduced. Multiplying the conditional recovery probability by \(P(G)\) yields exactly the proposed annealed lower bound.

The strongest failed shortcut has an explicit deterministic counterexample. On a one-way ray take one arrow \(v_n\to v_{n+1}\) at \(a_n=1-2^{-(n+1)}\) and one recovery at \(v_n\) at \(r_n=(a_n+1)/2\). Each vertex infects its successor before its own recovery. Every vertex is infected at some time before 1, but every vertex has recovered by time 1 and there is no reinfection. Thus an accumulating transmission ray alone does not prove the candidate's conclusion. This fixture is a logical negative control, not a claimed positive-probability counterexample to the candidate. The candidate's shrinking no-recovery guards exclude it.

## 8. Quenched enhancement and its boundary assumptions

Fix \(\lambda>0\) and \(\tau=1/(2\lambda)\). Write \(p_m(T)\) for the quenched probability of infinite infection at \(\tau+m\), and call \(T\) good when some \(p_m(T)>0\). These are measurable functions by §4. Positive annealed probability at \(\tau\) implies the probability \(q\) of being good is positive: a nonnegative measurable function with positive integral cannot vanish almost surely.

For a fixed good child subtree, use the event consisting of no root/child recoveries during \([0,1]\) and a downward root-to-child arrow in \([0,1/2]\). Its probability is \(e^{-2}(1-e^{-\lambda/2})>0\). On that event there is a finite root-to-child path reaching time 1. Future marks in the subtree are independent of the whole event, including the incoming edge mark. If its \(p_m\) is positive for a particular integer \(m\), concatenate any finite post-1 subtree witness with that initial root-to-child path. All vertices of an infinite future configuration are then infected at \(\tau+(m+1)\) in the whole tree with positive probability. Additional initial infections/edges cannot hurt; no problematic process restart at infinity is required.

Thus a bad parent can have only bad child subtrees. The offspring count is finite, and conditionally on it the child subtrees are independent copies of the original law. With \(r=1-q\),

\[
r\le E[r^\xi].
\]

For \(0<r<1\), \(\xi\ge1\) gives \(r^\xi\le r\) almost surely, with strict inequality on the positive-probability event \(\xi\ge2\). Indeed, a quantitative strict gap is at least \(P(\xi\ge2)(r-r^2)>0\). Hence the displayed inequality is impossible. Since \(q>0\), \(r=1\) is also impossible, leaving \(q=1\).

The no-extinction assumption is essential to this particular unconditional enhancement. As a negative control, the supercritical law \(P(\xi=0)=1/4\), \(P(\xi=2)=3/4\) has a nonzero fixed point \(r=1/3\) of its generating function; it permits finite extinct trees on which explosion is impossible. A generic supercritical hypothesis alone would not justify \(q=1\). The candidate explicitly selects positive offspring and does not make that broadened claim.

Perform this argument for every positive rational rate and intersect the countably many full-probability tree sets. For any real \(\lambda>0\), pick a positive rational \(r<\lambda\). Graphical domination preserves infinite infection at the finite time furnished for rate \(r\). That time need not equal \(1/(2\lambda)\) plus an integer, which is why the final real-rate claim is correctly phrased as explosion at *some* finite time. An uncountable intersection or a uniform tree-dependent lower bound is unnecessary.

## 9. Fitness extension and limiting cases

For a fixed tree and fixed finite field \(F_v\ge1\), each directed edge rate is finite and decomposes as

\[
\lambda F_uF_v=\lambda+\lambda(F_uF_v-1).
\]

Use the same baseline arrows and recoveries and add independent arrows of the nonnegative extra rate. Every original finite witness persists. Countably many finite-rate edge processes are sufficient; their global sum need not be finite. This proves domination directly under the same finite-path convention. For random fields, condition on the tree/fitness first and then sample independent Poisson marks, as the model requires. The statement is not about fitness values chosen as functions of future graphical marks.

The iid constant field is allowed; an iid field \(1+\mathrm{Exp}(1)\) is finite almost surely and unbounded, and inherits the bound. No independence between degree and arbitrary fixed fitness values is required for the domination step. Zero, vanishing, or infinite fitness values are outside the asserted extension.

For very small positive \(\lambda\), the eligible-arrow probabilities remain the same because the windows scale as \(1/\lambda\), while the recovery factor tends to zero. It is still strictly positive for each fixed \(\lambda>0\); no positive lower bound uniform near zero is claimed. For large finite \(\lambda\), the horizon shrinks and the recovery factor approaches one, without contradicting the scaled arrow rates. Neither the degenerate rate \(\lambda=0\) nor an infinite arrow rate is asserted. Stage failure, recovery before a required transmission, and recoveries at the horizon genuinely obstruct the corresponding witness; they are excluded or bounded explicitly rather than ignored.

## 10. Evidence, mechanism status, and exact gaps

| Mechanism / adversarial question | Evidence | Status | Exact remaining gap |
|---|---|---|---|
| Tail normalization, finite degrees, infinite mean | Telescoping and divergent `M P(ξ≥M)` lower bounds | Verified | None for the stated law |
| Minimal finite-path versus finite-ball definition | Two-way inclusion of finite witnesses; countable count event | Verified | No uniqueness/Feller claim for every possible explosive extension is made |
| Adaptively selected outgoing tests | Coordinate-disjoint exploration history; exact observed-prefix cylinders | Verified | None; selected own degrees are correctly allowed to be biased |
| Positive-probability infinite ray | Conditional stage bounds and disjoint first failures | Verified | Infinite limit is analytic, not computationally certified |
| Recovery fields along selected ray | Selection measurable in tree/arrows; untouched independent recovery coordinates | Verified | None under the stipulated independent Poisson model |
| Exact schedule and guard indexing | `s_n`, half-open arrow windows, closed guards; `L_N=3τ−2τ2^(−N)` | Verified | None |
| Simultaneous infection versus cumulative-only infection | Explicit finite witness to every `v_n` at τ; negative fast-ray fixture | Verified | None |
| Arrow direction and no infection from infinity | Directed finite-path tests; empty-initial-state control | Verified | None |
| Arbitrary finite fitness ≥1 | Independent extra-arrow decomposition; preserved finite witnesses | Verified | Marks-dependent fitness and infinite fitness are outside scope |
| Hereditary good-tree property | Positive one-unit entrance event plus finite-path concatenation | Verified | None |
| A.s. quenched statement | Bad-tree inequality; strict positive-offspring contraction | Verified | Cannot extend unconditionally to offspring laws that can become extinct |
| Every real positive λ on one tree set | Rational intersection and monotonicity | Verified | No common deterministic horizon or uniform quenched bound is established or claimed |

The central difficulty is solved by the summable recovery guard construction; it is not transferred to an unproved survival-to-explosion principle. No route in this family remains blocked. Invalid broadenings were retained as negative controls, not repaired by unsupported assumptions.

## 11. Computation and reproducibility boundaries

All supplied checks were read completely before execution. Their saved replays report:

- `supplied_verify_replay.json`: PASS, 17,228 exact finite assertions.
- `supplied_independent_checker_replay.json`: PASS, 7,136 exact finite assertions, 69,904 enumerated toy cylinders.
- `graphical_controls_result.json`: PASS, 2,388 independent exact rational/cylinder assertions, 58 actually observed-prefix selection histories.

The independent controls exercise a finite temporal-path enumerator, left arrow endpoints, terminal recovery endpoints, pre-guard harmless recoveries, reversed arrows, empty initial infection, return paths in enlarged volumes, a cumulative-only fast ray, recovery-biased selection, fourth-power telescoping bins, and the extinction boundary of the quenched claim. Rational rates range from \(10^{-6}\) to \(10^6\); these are schedule controls, not empirical estimates of explosion probability.

These calculations check finite artifacts and catch specific implementation/indexing mistakes. They do **not** prove a countable conditional product, positive probability of an infinite ray, existence of infinitely many simultaneous infections, all real infection rates, or the hereditary probability-one theorem. Those are the explicit analytic deductions in §§3–9. No simulation of huge random trees was used, and no numerical sampling is presented as probability-theorem evidence.

To reproduce within this folder, run `python3 graphical_controls.py` and `python3 integrity_check.py`. Replay the two frozen checker paths listed by the output manifest with stdout redirected to new files in this folder. The source code is read-only input. `OUTPUT_MANIFEST.json` records audit files, sizes, hashes, scope, and checker-input hashes; it excludes itself to avoid a circular self-hash.

## 12. Final disposition

Strongest verified result: for the explicit a.s.-finite positive offspring law, the minimal graphical process has infinitely many simultaneous infections at \(1/(2\lambda)\) with the stated strictly positive annealed bound for every finite positive \(\lambda\); finite fitnesses ≥1 preserve this; almost every tree has positive quenched explosion probability at some finite time for every positive real rate.

**Blocking findings: none. Required mathematical repairs: none.** The qualifications about annealed versus quenched probabilities, some finite time versus a universal tree time, positive offspring, and constant fitness are already explicit in the frozen proof. The remaining parent-audit tasks may include distinct approach families and priority assessment; this scoped GO does not substitute for them.
