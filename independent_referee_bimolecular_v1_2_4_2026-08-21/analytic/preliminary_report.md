# Preliminary independent analytic-proof referee report

**Manuscript:** *Positive Recurrence for Single-Linkage Bimolecular Weakly Reversible Stochastic Reaction Networks*, Alec Kriebel  
**Pass:** separated analytic-proof review; no code or author-generated audit material consulted  
**Started:** 2026-08-21 22:16 PDT (2026-08-22 05:16 UTC)  
**Checkpoint/report time:** 2026-08-21 22:26 PDT (2026-08-22 05:26 UTC)  
**Completion estimate:** 100% of the preliminary analytic-proof track. This is not a merged referee conclusion; the separated software, adversarial, and artifact passes remain outside this report.

## 1. Information barrier and materials examined

I began with the journal-facing PDF and visually inspected all 16 rendered pages. Only afterward did I consult the journal wrapper, the exact mathematical source, and the bibliography:

- packet root: `/Users/alec/Documents/Math/bimolecular_positive_recurrence_ai_referee_packet_v1_2_4/`
- PDF: `bimolecular_positive_recurrence_submission_v1_2_4/manuscript/main_jap.pdf`
- exact source: `bimolecular_positive_recurrence_submission_v1_2_4/manuscript/paper_content.tex`
- journal wrapper: `bimolecular_positive_recurrence_submission_v1_2_4/manuscript/main_jap.tex`
- bibliography: `bimolecular_positive_recurrence_submission_v1_2_4/manuscript/references.bib`

SHA-256 values recorded before substantive review:

| File | SHA-256 |
|---|---|
| `main_jap.pdf` | `77b4f098a1f0655ed4e04423caccec79a051cf11297b17d5fa2d630d539e7c4d` |
| `paper_content.tex` | `00c0d9f2b281d6f36a388ff45776d9f90f9d6388dce0e83d9eb7b6aa80a4deba` |
| `main_jap.tex` | `e2c0603f0fa9922b90a2292e0da6f1d1d000579cb188493737b33005e3188a3e` |
| `references.bib` | `00bd5723e1c518841e94e8bd02637c709b0295891f191ed65dffbcc10a034e61` |

Environment recorded before review:

- macOS 26.5.2, build 25F84; Darwin 25.5.0, arm64
- Python 3.14.6
- Tectonic 0.16.9
- repository branch: `main`

The supplied packet is an untracked copied directory, not a checkout of the claimed release. The local repository had no `refs/tags/bimolecular-positive-recurrence-v1.2.4`, and `git ls-remote --tags origin refs/tags/bimolecular-positive-recurrence-v1.2.4` returned no matching remote reference at the checkpoint time. Thus the bytes listed above were reviewed as content, but Git-tag provenance was **not verified**.

I did **not** read any `audit/`, `preservation/`, validation report, expected/golden output, research log, revision log, expert-audit note, `supplement/reviewer_checklist.md`, packet build log, code file, test, or other referee track's report. No conclusion below relies on those materials.

## 2. Exact theorem audited

Let the species set be finite, with population state space \(\mathbb N_0^d\). A finite set of labelled reaction channels \(r:y_r\to y'_r\) has fixed rates \(\kappa_r>0\), and at population \(x\) channel \(r\) has stochastic mass-action propensity

\[
\lambda_r(x)=\kappa_r(x)_{y_r},\qquad
(x)_y=\prod_i\frac{x_i!}{(x_i-y_i)!}
\]

when \(x\ge y\), and zero otherwise. Parallel channels are allowed. Every source and target complex has total molecularity at most two. The complex graph is weakly reversible and has exactly one linkage class; equivalently here, its full directed complex graph is strongly connected.

For an arbitrary initial population \(x_0\), let

\[
\Gamma(x_0)=\{z:x_0\leadsto z\},
\]

where \(\leadsto\) means reachability by a finite sequence of actually enabled channels. The claim is:

1. \(\Gamma(x_0)\) is exactly one closed communicating class.
2. If it is nonabsorbing, the minimal population-valued CTMC with the displayed propensities is nonexplosive and positive recurrent.
3. Here positive recurrence means that, after the first genuine population jump, the return time \(T_x^+\) to one (equivalently every) state of the irreducible class has finite expectation.
4. If the reachable class is an absorbing singleton, its unique stationary law is the point mass there.
5. Consequently every reachable class has a unique stationary probability distribution.

This is exactly Theorem 2.1 on PDF page 3 and `paper_content.tex` lines 240--247, together with Corollary 2.3 at lines 293--299. It makes no claim for multiple linkage classes or complexes of molecularity above two.

## 3. Proof audit table

| # | Load-bearing obligation | Status | Concrete basis |
|---:|---|---|---|
| 1 | Lifted state-return paths and closed reachability classes | **PASS** | If an enabled \(y\to y'\) fires from \(x=\rho+y\), any directed complex return path \(y'=z_0\to\cdots\to z_m=y\) lifts exactly to \(\rho+z_0\to\cdots\to\rho+z_m\). This reverses every enabled population edge and hence every reachability path. PDF p. 4; Lemma 2.2; lines 249--291. |
| 2 | Labelled-channel marked augmentation: Markov, irreducible, autonomous projection | **PASS** | The next-channel law depends only on population \(x\), not the carried target. Projection therefore has the ordinary jump kernel. Reachability of every marked state supplies a last-channel predecessor; population irreducibility followed by that last channel proves augmented irreducibility. PDF pp. 4--5; (8)--(9); lines 332--368. |
| 3 | Proper target-shifted log-factorial potential and exact increment | **PASS** | The carried target is enabled, so \(\rho=x-t\ge0\). Finite target set plus \(\log(n!)\to\infty\) makes sublevels finite. Direct factorial cancellation gives \(\Delta V=\log((x)_t/(x)_s)\), including \(0\), unary, and repeated-species sources. PDF pp. 5--6; (10), Lemma 3.2/(13); lines 369--378 and 453--470. |
| 4 | Target-following episode, deviations, recursion | **PASS** | Every designated edge is enabled along the lift \(\rho+y_k\), continuation occurs iff the exact designated channel fires, and every deviation terminates immediately. The recursion \(J_k=\delta+q_kp_kJ_{k+1}\) counts the first reward once; the continuation branch's immediate reward is exactly zero. Zero-length paths reduce to one final jump. PDF p. 7; (18)--(21); lines 520--566. |
| 5 | Scalar envelope, both branches, monotonicity, backward propagation | **PASS** | The objective is concave in \(p\). Its maximizer is \(p=1\) for \(M\ge-1/q\) and \((-qM)^{-1}\) otherwise. The supremum is nondecreasing in \(M\) and tends to \(-\infty\) with \(M\). Iterating through the finite path is valid even for arbitrarily separated fixed positive rates. PDF pp. 7--8; (22), Proposition 4.3; lines 571--621. |
| 6 | Normalized-log compactification, including zero-weight divergent coordinates | **PASS** | Integer-coordinate diagonal extraction yields coordinates that are fixed or tend to infinity. The normalizer diverges, the weights lie in the simplex, and a divergent coordinate may correctly retain weight zero. Falling-factorial asymptotics remain valid for such a coordinate because its log contribution is \(o(R_n)\), not because it is bounded. PDF p. 8; (23)--(25); lines 630--684. |
| 7 | Complete bimolecular top-complex trichotomy and availability/invariant branches | **PASS** | The A/B/C split is exhaustive. I checked every subcase: all-top gives the exact invariant \(w\cdot x\); two divergent particles make a top source eventually enabled; the one-divergent-particle case yields unary availability, bounded-companion availability, or the exact signed invariant \(\ell\). The argument includes \(2S_i\), zero-weight divergent coordinates, and absent species. PDF pp. 8--10; Lemmas 5.3--5.4, (26)--(29); lines 686--810. |
| 8 | Finiteness and nonemptiness of the exceptional Foster set | **PASS** | An infinite \(K\) supplies a proper-potential divergent sequence; the top alternative either contradicts a class invariant or gives a fixed terminal whose episode drift tends to \(-\infty\). A global minimizer of proper \(V\) lies in \(K\), since every episode endpoint remains in the augmented class. PDF p. 10; Proposition 6.1/(30); lines 814--841. |
| 9 | Stopped random-time Foster/supermartingale and integrability | **PASS** | Episodes last at most \(|\mathcal C|\) jumps and have drift at most \(-1\) outside \(K\). Per-coordinate overshoot is deterministically bounded. Thus each finite-horizon stopped potential is bounded by a deterministic finite factorial expression, providing integrability. Monotone convergence gives \(E\sigma_K\le V(z)\). PDF p. 11; (34)--(36); lines 892--940. |
| 10 | Finite trace chain and projection to population jumps | **PASS** | From every \(k\in K\), one jump followed by the Foster bound gives finite mean positive return to \(K\). The finite irreducible trace chain has finite mean return to a selected \(k_*\); Tonelli converts trace excursions to original jump counts. Population return occurs no later than marked return, and its kernel is autonomous. PDF pp. 11--12; Proposition 7.1; lines 946--1000. |
| 11 | CTMC nonexplosion, finite expected physical return, regenerative law | **PASS** | Positive recurrence of the jump chain forces infinitely many visits to \(x_*\); the i.i.d. exponential holding-time subseries at \(x_*\) diverges a.s., ruling out explosion. The uniform lower bound \(\Lambda(x)\ge\kappa_{\min}>0\) converts finite jump return count to finite physical return time. The regenerative cycle then has finite positive mean length and normalizes the occupation law. PDF pp. 12--13; Proposition 7.2, (37)--(38); lines 1003--1071. |
| 12 | Uniqueness and absorbing singleton classes | **PASS** | Irreducibility gives uniqueness of the regenerative stationary law in every nonabsorbing class; finite classes were reduced separately. With genuine self-channels removed, a singleton with no population-changing transition is absorbing and has the unique point mass. PDF pp. 3--4 and 13; lines 229--238, 301--320, 1071--1073. |

## 4. Independent derivations of the load-bearing identities

### 4.1 Return-path lifting

For an enabled channel \(y\to y'\), write \(x=\rho+y\) with \(\rho\ge0\). After it fires, \(x'=\rho+y'\). Weak reversibility gives a directed complex path from \(y'\) back to \(y\). At each lifted population \(\rho+z_j\), source \(z_j\) is present exactly, so the next edge is enabled. No interior positivity assumption is used. Reversing each edge of a population reachability path, in reverse order, proves symmetric reachability. Closure of \(\Gamma(x_0)\) then also follows directly from its definition: the endpoint of any enabled edge from a reachable state is reachable.

### 4.2 Exact marked increment

At marked state \((x,t)\), the old residual is \(x-t\). If source \(s\) fires to target \(u\), the new marked state is \((x-s+u,u)\), whose residual is \(x-s\). Therefore

\[
\exp(\Delta V)
=\prod_i\frac{(x_i-s_i)!}{(x_i-t_i)!}
=\frac{\prod_i x_i!/(x_i-t_i)!}{\prod_i x_i!/(x_i-s_i)!}
=\frac{(x)_t}{(x)_s}.
\]

No approximation occurs. If \(s=t\), the reward is zero. This also shows why the target rather than merely the population displacement must be retained.

### 4.3 Source entropy identity

For an enabled source \(s\), \((x)_s=p_x(s)\Lambda(x)/\bar\kappa_s\). Substitution in the preceding increment and averaging gives

\[
\delta(x,t)=\log p_x(t)-\sum_s p_x(s)\log p_x(s)
 +\sum_s p_x(s)\log\bar\kappa_s-\log\bar\kappa_t.
\]

The entropy term is at most \(\log|\mathcal C|\), and the rate term is at most \(\log(\bar\kappa_+/\bar\kappa_-)\). Hence \(\delta\le\log p_x(t)+C_0\). The zero source has \((x)_0=1\) and causes no division or logarithm failure.

### 4.4 Episode recursion and scalar envelope

At phase \(k\), the designated channel is chosen with probability

\[
\frac{\kappa_{y_k\to y_{k+1}}(x)_{y_k}}{\Lambda(x)}
=q_kp_k.
\]

The first-jump expectation \(\delta\) already includes the designated branch's zero immediate reward. Only its future reward remains to be added, giving

\[
J_k=\delta(\rho+y_k,y_k)+q_kp_kJ_{k+1}.
\]

For \(f(p)=\log p+C_0+qpM\), \(f''(p)=-p^{-2}<0\). If \(M\ge-1/q\), then \(f'(1)\ge0\) and the maximum over \((0,1]\) is at 1. Otherwise the maximum is at \(p=(-qM)^{-1}\). This reproduces both branches of (22). In particular, if a terminal \(J_m\to-\infty\), then recursively

\[
J_k\le F_{q_k}(J_{k+1})\to-\infty.
\]

The slow second branch may turn a large negative value into a negative logarithm, but a finite number of iterations still tends to \(-\infty\). No rate is sent to zero in this argument; every \(q_k\) is a fixed positive constant for the fixed rate vector.

### 4.5 Compactification and top alternative

After fixing the carried target on a subsequence, at least one residual coordinate diverges. With

\[
R_n=\sum_{i\in I}\log(\rho_i^{(n)}+1),\qquad
w_i=\lim\frac{\log(\rho_i^{(n)}+1)}{R_n},
\]

one has \(w\ge0\), \(\sum_iw_i=1\). For a fixed enabled binary complex \(y\), each unary factor contributes \(\log(\rho_i+1)+o(R_n)\), each repeated factor contributes twice that amount, and fixed coordinates contribute \(O(1)\). Thus

\[
\log(\rho^{(n)}+c)_y=R_nw\cdot y+o(R_n).
\]

The three top cases were checked as follows.

- If every complex is top, \(w\cdot y\) is constant on all complexes, hence on both ends of every channel. It is an exact invariant, but \(w\cdot x^{(n)}\to\infty\), impossible within one class.
- If a top complex contains two particles on divergent coordinates, bimolecularity leaves no bounded-coordinate requirement. The source is eventually enabled over any fixed lower terminal, including a repeated source \(2S_i\).
- Otherwise each top complex contains exactly one divergent particle. Species represented this way form \(\mathcal J\), and every such species has weight \(h_*\). A complex is top iff it contains exactly one \(\mathcal J\)-particle. A unary top source is automatically enabled; a mixed top source \(S_i+D\) is enabled whenever the lower terminal supplies its bounded companion \(D\). If no lower complex supplies any companion, every top complex has one \(\mathcal J\)-particle and one companion, while every lower complex has neither. Then
  \[
  \ell(x)=\sum_{i\in\mathcal J}x_i-\sum_{D\in\mathcal D}x_D
  \]
  is exactly zero on every complex and hence invariant on every reaction. Its positive coordinates diverge and its negative coordinates are fixed, again impossible within one class.

In the availability branches, the strict gap \(h(s)>h(c)\) makes the falling-factorial ratio grow exponentially on the \(R_n\) scale. Since both sources are enabled,

\[
p_{\rho^{(n)}+c}(c)
\le \frac{\bar\kappa_c(\rho^{(n)}+c)_c}
{\bar\kappa_s(\rho^{(n)}+c)_s}\to0.
\]

This is the terminal rarity required by the episode envelope.

### 4.6 Foster, trace, and physical time

Properness of \(V\) means any infinite exceptional set has a sequence escaping every finite set. The compactification contradicts that sequence, so \(K\) is finite. A global minimizer of \(V\) is in \(K\), so it is nonempty.

For the stopped endpoint chain, after \(N\) episodes every coordinate is at most its initial value plus \(2|\mathcal C|N\). Hence \(V(Y_{N\wedge\sigma_K})\) is bounded by a deterministic finite number; all finite-time optional-stopping quantities are integrable. The supermartingale inequality gives

\[
E[V(Y_{N\wedge\sigma_K})]+E[N\wedge\sigma_K]\le V(z),
\]

and monotone convergence gives \(E\sigma_K\le V(z)\).

The finite trace conversion does not assume uniform excursion independence. At the start of trace excursion \(j\), the strong Markov property gives \(E[E_j\mid\mathcal F_j]\le B\); since \(\{j<M\}\in\mathcal F_j\), Tonelli yields

\[
E\sum_{j=0}^{M-1}E_j
\le B\sum_{j\ge0}P(j<M)=BEM<\infty.
\]

Finally, the mass-action total rate satisfies \(\Lambda(x)\ge\kappa_{\min}\), because every state of a nonsingleton irreducible class enables a genuine channel and every positive falling factorial is an integer at least one. This lower bound controls expected physical return time. Nonexplosion follows separately from the divergent sum of holding times accumulated at recurrent visits to one fixed state.

## 5. Boundary and counterexample attempts

I attempted to break the interfaces rather than merely checking generic interior states.

1. **Zero complex and boundary faces.** For \(0\to A+B\to B\to0\), the lift works with residuals having zero coordinates, \((x)_0=1\), and the carried target remains enabled. At \(((n,0),0)\), the two designated rewards are zero. At \(((n,1),B)\), only the \(A+B\) source contributes a negative reward, giving exactly
   \[
   -\frac{\kappa_1n}{\kappa_0+\kappa_2+\kappa_1n}\log n.
   \]
   The preceding deviations have probability \(O(n^{-1})\) and reward \(O(\log n)\), so no positive boundary counterexample results.
2. **Repeated species \(2S_i\).** If a top source is \(2S_i\) with \(i\in I\), then \(\rho_i^{(n)}\to\infty\) supplies two copies eventually. The factorial asymptotic is \(2\log(\rho_i+1)+o(R_n)\). Thus the repeated-particle branch is genuinely covered.
3. **Zero normalized weight but divergence.** I tested the pattern in which one coordinate grows on the leading exponential scale and another diverges subexponentially, so the latter lies in \(I\) but has weight zero. If both occur in a top binary source, it falls into case B and is eventually enabled; it is not misclassified as bounded. If it is absent from top sources, it has zero coefficient in the case-C invariant and creates no false cancellation.
4. **Unary-absent mixed top complexes.** For top complexes of the form \(A+B\) with \(A\) divergent and \(B\) fixed, a lower terminal containing \(B\) enables the top source. If no lower complex contains any top companion, \(A-B\) (or its multi-species analogue (28)) is an exact invariant, so divergence inside one class is impossible. This rules out the apparent boundary-availability counterexample.
5. **Absent species.** If a species occurs in no complex, its coordinate never changes. A sequence in one class cannot diverge through that coordinate. In normalized-log language this is the all-top invariant branch.
6. **Parallel channels and equal displacements.** Exact parallels may be rate-aggregated. Channels with equal displacement but different sources remain distinguished; the actual target/source pair is recoverable from the labelled channel and the marked transition. The proof never infers it from displacement alone.
7. **Self channels.** A channel \(y\to y\) contributes zero to the population generator. Removing it is legitimate for the minimal population-valued CTMC. A system with no genuine enabled channel is an absorbing singleton, not a nonabsorbing recurrence counterexample.
8. **Parity and lattice restrictions.** The return-path and episode lifts use the same residual and only actual channels. They do not interpolate between lattice states, so parity-restricted classes remain closed throughout the construction.
9. **Zero-length target paths.** When \(c=t\), the episode is the terminal ordinary jump, \(J_0=\delta(\rho+t,t)\), and the envelope starts at the terminal bound. No missing continuation factor occurs.
10. **Arbitrarily separated rates.** Sending an important fixed rate ratio extremely close to zero can push \(K\) arbitrarily far out but does not defeat recurrence. Setting it exactly to zero would violate the theorem's positive-rate hypothesis. I independently rederived (31)--(33) for \(0\to A\to A+B\to0\): the leading terminal drift is \(-\kappa_2(\kappa_1+\kappa_2)^{-1}\log m\), while for each fixed \(m\), the drift becomes positive as \(\kappa_2\downarrow0\). This supports, rather than contradicts, the claimed rate-dependent exceptional set.
11. **Finite and absorbing classes.** Same-molecularity networks preserve total molecule count and therefore lie in finite shells. A one-complex graph has only self channels and hence population-absorbing classes. Neither case requires the infinite-class argument.
12. **Higher molecularity and multiple linkage classes.** The proof does not silently extend to either. A ternary top complex can contain one leading divergent species and two bounded companions, which is outside the A/B/C argument. With several linkage classes the fixed target need not reach the selected terminal. These are correctly excluded.

I also rederived the Anderson--Cappelletti--Kim worked episode on PDF pp. 5--6. At the successive marked populations, the total rates are exactly \(n(\kappa_1+2\kappa_2)+2\kappa_5\), \(n(\kappa_1+\kappa_2+\kappa_3)+\kappa_4\), and \((n-1)(\kappa_1+\kappa_2+\kappa_3)+\kappa_4\). The only leading negative term is the terminal \(-\log(n-1)\) reward multiplied by the three displayed positive continuation limits, reproducing the stated \(\alpha\).

## 6. Independent finite falsification checks

Without importing or reading any package code, I ran a separate in-memory Python oracle using only the standard library.

- It checked the exact factorial identity for every \(x\in\{0,\dots,5\}^3\), every enabled binary source \(s\), every enabled binary carried target \(t\), and every binary new target \(u\): **136,020 exact rational identities**, all equal.
- It exhaustively enumerated all subsets of the ten three-species complexes of molecularity at most two, all nonzero weight vectors with entries in \(\{0,1,2\}\), and all choices of zero-weight divergent coordinates. It checked the complete top-case classification for **56,728 configurations**. Counts were: all-top invariant 1,988; two-divergent-particle availability 47,706; unary-top availability 4,790; companion availability 2,028; signed-invariant fallback 216. No unclassified configuration or failed asserted invariant was found.

These finite checks are falsification evidence for the algebra and combinatorial split, not a proof of the universal theorem. The universal justification remains the derivation above.

## 7. External theorem and prior-work interfaces

I used network access only after the independent proof pass.

- The primary Anderson--Cappelletti--Kim preprint (`https://people.math.wisc.edu/~dfanderson/papers/ACK2019.pdf`, corresponding to DOI 10.1017/jpr.2020.28) states the binary, single-linkage theorem with the additional condition that each species has a pure multiple complex, which in the binary setting is \(S_i\) or \(2S_i\). Its Theorem 4.1 and Example 4.1 match the manuscript's comparison. This prior result is contextual, not used in the present proof.
- The primary Paulevé--Craciun--Koeppl article (`https://pmc.ncbi.nlm.nih.gov/articles/PMC3835780/`, DOI 10.1007/s00285-013-0686-2) has Lemmas 4.5--4.6 asserting their discrete-reaction-network notion of recurrence and that weak reversibility implies it. The manuscript accurately distinguishes that combinatorial term from stochastic positive recurrence. Its own lift proof is self-contained.
- The primary arXiv v2 PDF for Xu (`https://arxiv.org/pdf/2409.05340`) proves regularity/nonexplosion for bimolecular weakly reversible mass-action systems and states on p. 18 that the bimolecular positive-recurrence conjecture remained open. This matches the manuscript's contextual statement. It is not used in the proof.
- Norris is cited for standard irreducible-chain facts, Meyn--Tweedie for the sampled-chain Foster context, and Asmussen for the regenerative occupation theorem. The manuscript supplies the Foster, trace, nonexplosion, and mean-return arguments it needs. The remaining regenerative step uses the standard theorem under the correct interface: a nonexplosive strong Markov chain, regeneration at returns to one state, and finite positive mean cycle length. I did not independently inspect full primary book text or page-level theorem numbering.

I did not conduct an exhaustive novelty search across all 2026 manuscripts and unpublished work. Novelty beyond the specifically checked ACK and Xu comparisons is therefore not independently established in this analytic pass.

## 8. Findings by severity

### Blocker

None found in the mathematical argument.

### Major

None found in the mathematical argument.

### Minor

None required for the theorem or proof on this pass.

### Notes

1. **Release-tag provenance not verified.** The journal source says the package is available at tag `bimolecular-positive-recurrence-v1.2.4` (`paper_content.tex` lines 1139--1146; PDF p. 14), but neither the local tag nor a matching remote tag was visible at the checkpoint time. This does not affect the content-level proof audit, but it must be reconciled in the artifact/provenance review.
2. **Full novelty search incomplete.** The cited primary ACK and Xu comparisons checked out, but conference-announced or unpublished results were not exhaustively discoverable.
3. **Book pinpointing not checked.** The standard Markov/regenerative results have matching hypotheses, but the cited books were not independently checked for exact page/theorem pinpoints.

## 9. Provisional analytic conclusion

Every necessary analytic implication survived scrutiny. In particular, the proof does not infer a source from a displacement, does not require boundary interiority, does not discard zero-weight divergent coordinates, does not compare unrelated rate scales, and does not use a conclusion outside the one-linkage/bimolecular scope. I found no circular step and no counterexample.

**Provisional mathematical status for the analytic-proof track: VALID AS STATED.**

**Provisional journal recommendation on mathematical content alone: accept.**

This is deliberately not the final merged recommendation. Code behavior, canonical reports, artifact reproducibility, and comparison with the embargoed author-generated audit materials were not examined here and must be assessed independently before the overall referee report is issued.

## 10. Checkpoint log

- **2026-08-21 22:16 PDT — 5%:** recorded paths, hashes, environment, branch, and tag availability before reviewing content.
- **2026-08-21 22:18 PDT — 20%:** completed visual inspection of all 16 PDF pages; no rendering defect affected mathematical readability.
- **2026-08-21 22:22 PDT — 65%:** reconstructed Theorem 2.1 and checked the marked-chain, factorial, episode, compactification, and top-complex interfaces from exact TeX lines.
- **2026-08-21 22:24 PDT — 85%:** completed Foster/trace/CTMC checks and boundary counterexample attempts.
- **2026-08-21 22:25 PDT — 95%:** completed independent exact-identity and exhaustive finite top-split checks and limited primary-source verification.
- **2026-08-21 22:26 PDT — 100%:** completed this isolated preliminary analytic report.
