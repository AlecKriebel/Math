# Preliminary blind adversarial referee report

**Manuscript:** *Positive Recurrence for Single-Linkage Bimolecular Weakly Reversible Stochastic Reaction Networks*, Alec Kriebel, Version 1.2.4  
**Track:** adversarial mathematics, boundary cases, and citation/priority checks  
**Report timestamp:** 2026-08-21 22:31 PDT (2026-08-22 05:31 UTC)  
**Independence status:** preliminary and unmerged

## Blind-review protocol and scope

I first read and rendered the journal-facing PDF, then used only the manuscript TeX wrapper, `paper_content.tex`, and `references.bib` for exact notation and citations. Before reaching the judgment below, I did **not** read any author audit, preservation material, research or revision log, expert-audit note, reviewer checklist, validation output, committed expected/golden report, packet build log, implementation, test, or another referee track. I did not contact anyone. Public sources were consulted only to check citations, public announcements, novelty context, and release-tag availability.

This track is deliberately not a software or full artifact-consistency audit. Its affirmative conclusions concern the analytic theorem and the manuscript claims that can be assessed without crossing the information barrier. The other required tracks must independently assess code, replay, manifests, PDF/ZIP byte reproducibility, and author-generated records.

### Recorded inputs and environment

Packet root:

`/Users/alec/Documents/Math/bimolecular_positive_recurrence_ai_referee_packet_v1_2_4`

Files used:

| File | SHA-256 |
|---|---|
| `bimolecular_positive_recurrence_submission_v1_2_4/manuscript/main_jap.pdf` | `77b4f098a1f0655ed4e04423caccec79a051cf11297b17d5fa2d630d539e7c4d` |
| `bimolecular_positive_recurrence_submission_v1_2_4/manuscript/paper_content.tex` | `00c0d9f2b281d6f36a388ff45776d9f90f9d6388dce0e83d9eb7b6aa80a4deba` |
| `bimolecular_positive_recurrence_submission_v1_2_4/manuscript/main_jap.tex` | `e2c0603f0fa9922b90a2292e0da6f1d1d000579cb188493737b33005e3188a3e` |
| `bimolecular_positive_recurrence_submission_v1_2_4/manuscript/references.bib` | `00bd5723e1c518841e94e8bd02637c709b0295891f191ed65dffbcc10a034e61` |

Environment recorded before review:

- Hardware/OS: Apple arm64; Darwin 25.5.0; macOS 26.5.2, build 25F84.
- Python: 3.14.6.
- Tectonic: 0.16.9.
- PDF metadata: 16 US-letter pages, PDF 1.5, 156,340 bytes.
- The supplied packet is a copied directory, not a Git checkout (`.git` absent). Its bytes can be hashed, but those bytes alone cannot establish Git-tag provenance.
- At 2026-08-21 22:28 PDT the exact claimed v1.2.4 GitHub tree URL returned HTTP 404. A fresh `git ls-remote --tags` query returned the v1.2.3 tag but no v1.2.4 tag. This is a concrete availability discrepancy, detailed below.

All 16 PDF pages were rendered to images and visually inspected. I found no clipping, overlapping text, missing glyphs, or unreadable display equation.

### Checkpoint log

| Time (PDT) | Checkpoint | Best-guess completion |
|---|---|---:|
| 2026-08-21 22:15 | Blind inputs, hashes, environment, and exclusion boundary recorded | 10% |
| 2026-08-21 22:20 | PDF read and 16-page visual render inspection completed | 25% |
| 2026-08-21 22:27 | Load-bearing proof reconstructed; edge-case and finite-oracle attacks completed | 80% |
| 2026-08-21 22:30 | Primary-source and public-tag checks completed | 95% |
| 2026-08-21 22:31 | Preliminary report written; software/artifact tracks intentionally remain separate | 100% of this track |

## Provisional disposition

The analytic theorem survives my attempted falsification. I found no unresolved load-bearing mathematical gap and no counterexample. The one reproducible defect in this track is noncentral but real: the manuscript says that the v1.2.4 tagged repository directory and its release record are available, while the exact tag/tree was not publicly available when checked. The narrow repair is to publish and verify the stated tag, or revise the availability and preprint-status wording to describe the standalone packet accurately.

**Provisional journal recommendation: minor revision.**

## Exact theorem audited

Let the species set be finite, let the reaction-channel set be finite, and let every channel \(r:y_r\to y'_r\) have a strictly positive rate constant. Populations lie in

\[
\mathbb N_0^d,
\]

and channel \(r\) has stochastic mass-action rate

\[
\lambda_r(x)=\kappa_r(x)_{y_r},
\qquad
(x)_y=\prod_i\frac{x_i!}{(x_i-y_i)!}
\]

when \(x\ge y\), and zero otherwise. The complex graph is assumed weakly reversible and to have exactly one linkage class; equivalently here, it is strongly connected. Every source or target complex is binary in the manuscript's sense,

\[
|y|=\sum_i y_i\le 2.
\]

For an arbitrary initial population \(x_0\), define

\[
\Gamma(x_0)=\{z\in\mathbb N_0^d:x_0\leadsto z\},
\]

where reachability uses finite sequences of enabled labelled channels and includes the empty path. The theorem claims:

1.  \(\Gamma(x_0)\) is exactly a closed communicating class.
2. If that class is nonabsorbing, the minimal population-valued CTMC on it is nonexplosive and positive recurrent for every positive rate vector.
3. If it is an absorbing singleton, its stationary law is the point mass.

For a nonabsorbing class, “positive recurrence” is explicitly physical-time positive recurrence: with \(\tau_1\) the first genuine jump time,

\[
T_x^+=\inf\{t\ge\tau_1:X(t)=x\},
\qquad \mathbb E_xT_x^+<\infty
\]

for one, hence every, state of the irreducible class. The corollary is uniqueness of the stationary probability on each reachable class. Self-channels are correctly removed because they contribute zero to the population generator; exact parallel source-target channels may be combined, while channels with equal displacement but different sources or targets remain labelled.

The exact theorem is at PDF p. 3 and `paper_content.tex` lines 240–247; the model and return-time definition are at PDF pp. 2–3 and lines 182–238.

## Proof-audit table

| # | Load-bearing obligation | Result | Concrete basis |
|---:|---|---|---|
| 1 | Lifted return paths and closure of every reachability class | **PASS** | If \(x=\rho+y\) fires \(y\to y'\), any directed complex return path \(y'\to\cdots\to y\) lifts to \(\rho+y'\to\cdots\to\rho+y=x\). Every lifted source is present because \(\rho\ge0\). Reversing each edge of a population path proves symmetric accessibility; reachability itself makes the class closed. PDF p. 4; lines 249–291. |
| 2 | Labelled-channel marked augmentation: Markov, irreducible, autonomous projection | **PASS** | The next labelled channel is selected from the current population only; the new mark is its target. Hence the pair is Markov and the population projection has the ordinary jump kernel. Projection is all of \(\Gamma\); irreducibility follows by reaching the predecessor \(z=x'-t'+s'\) of a witnessed target-marked state and appending \(s'\to t'\). PDF pp. 4–5; lines 332–378. |
| 3 | Proper shifted log-factorial potential and exact increment | **PASS** | The carried target is enabled, so \(\rho=x-t\ge0\). Finitely many targets plus divergence of \(\log(n!)\) makes every \(V=\sum_i\log(\rho_i!)\) sublevel finite. For next source \(s\), target \(u\), the new residual is \(x-s\), giving exactly \(\Delta V=\log((x)_t/(x)_s)\). PDF pp. 5–6; lines 369–378 and 453–470. |
| 4 | Target-following episode, deviations, zero-length paths, recursion | **PASS** | Every designated edge keeps residual \(\rho\) fixed and has zero reward. All non-designated first jumps stop but their immediate rewards are already included in \(\delta\). Continuation has exact probability \(q_kp_k\), yielding \(J_k=\delta_k+q_kp_kJ_{k+1}\). The episode has 1 through \(|\mathcal C|\) jumps, including path length zero. PDF p. 7; lines 520–566. |
| 5 | Scalar envelope, both branches, monotonicity, backward propagation | **PASS** | The objective \(\log p+C_0+qpM\) is strictly concave in \(p\). Its maximum is at \(p=1\) when \(M\ge-1/q\), otherwise at \(p=(-qM)^{-1}\); both displayed branches follow. Each envelope is nondecreasing in \(M\) and maps sequences tending to \(-\infty\) to sequences tending to \(-\infty\), so a finite backward composition preserves terminal negative divergence. PDF pp. 7–8; lines 571–617. |
| 6 | Normalized-log compactification, including zero-weight divergent coordinates | **PASS** | A diagonal subsequence makes every residual coordinate fixed or divergent. The denominator \(R_n\to\infty\), normalized nonnegative weights sum to one, and the set \(I\) retains all divergent coordinates even when \(w_i=0\). Direct expansion verifies \(\log(\rho^{(n)}+c)_y=R_nw\cdot y+o(R_n)\) for \(0,S_i,2S_i,S_i+S_j\), with enabled fixed-coordinate factors only \(O(1)\). PDF p. 8; lines 630–684. |
| 7 | Complete bimolecular top-complex trichotomy and every branch | **PASS** | I reconstructed cases A, B, and C independently, including the unary, bounded-companion availability, and signed-invariant subcases. Zero-weight divergent coordinates remain in \(I\), so they cannot be mistaken for bounded companions. The three cases exhaust molecularity at most two; the invariant contradictions are exact within a fixed communicating class. PDF p. 9; lines 694–787. |
| 8 | Finiteness and nonemptiness of exceptional Foster set \(K\) | **PASS** | If \(K\) were infinite, properness supplies a divergent sequence. The top lemma gives either an impossible invariant or a fixed terminal whose episode drift tends to \(-\infty\), contradicting membership in \(K\). A global minimizer of the proper nonnegative \(V\) exists, and every episode endpoint has at least that value, so all its expected episode increments are nonnegative and it belongs to \(K\). PDF p. 10; lines 814–840. |
| 9 | Stopped random-time Foster/supermartingale and integrability | **PASS** | \(W_n=V(Y_{n\wedge\sigma_K})+n\wedge\sigma_K\) is a nonnegative supermartingale. At each fixed \(n\), binary increments and bounded episode length deterministically bound all coordinates and hence \(V\), so no hidden integrability or unbounded optional-stopping step is used. The inequality is applied at deterministic \(N\); monotone convergence then gives \(\mathbb E\sigma_K\le V(z)\). PDF p. 11; lines 892–940. |
| 10 | Finite trace chain and projection to ordinary population jumps | **PASS** | One ordinary jump from finite \(K\), followed by the established finite expected hit, gives finite expected positive return to \(K\). The finite irreducible trace has geometrically bounded return count. Conditional excursion means are uniformly bounded over \(K\); Tonelli and the tail-sum identity give finite original-jump return. Projected population return occurs no later than return of the full marked state. PDF pp. 11–12; lines 946–1001. |
| 11 | CTMC nonexplosion, finite expected physical return, regenerative law | **PASS** | Embedded positive recurrence gives infinitely many visits to an anchor. The independent exponential holding times on that fixed-state subsequence have one finite positive rate and sum to infinity almost surely, excluding explosion. Every nonabsorbing state enables a genuine channel and every positive falling factorial is an integer at least one, so \(\inf_\Gamma\Lambda\ge\kappa_{\min}>0\); this converts finite expected jump return to finite expected physical return. The finite regenerative cycle occupation measure is normalized and stationary. PDF pp. 12–13; lines 1003–1073. |
| 12 | Uniqueness and absorbing singleton classes | **PASS** | Irreducibility plus positive recurrence/nonexplosion gives a unique stationary probability; the explicit occupation formula supplies existence. A population state with no genuine enabled channel has singleton reachability and the point mass; self-events do not alter the minimal population process. PDF pp. 3, 12–13; lines 229–246, 285–315, 1054–1073. |

## Detailed adversarial reconstruction

### 1. Reachability and the marked state space

The closure assertion does not rely on stochastic rates. Suppose \(y\to y'\) fires at \(x\), so \(x=\rho+y\) with \(\rho\in\mathbb N_0^d\). Weak reversibility supplies

\[
y'=z_0\to z_1\to\cdots\to z_m=y.
\]

At the \(j\)-th lifted population \(\rho+z_j\), the exact source \(z_j\) is present, so the return path is enabled. This remains true when \(y=0\), on a coordinate face, or when a repeated species \(2S_i\) occurs. It also preserves every lattice or parity restriction because it consists of actual reaction firings. Parallel labels and equal displacements do not affect it. A self-channel has zero increment and needs the empty return.

For the augmented state, a preceding labelled channel \(s\to t\) leaves population \(x=z-s+t\), so \(x-t=z-s\ge0\): the mark is always enabled. Given two reachable marked states \((x,t)\) and \((x',t')\), reachability of the latter has a final channel \(s'\to t'\) and predecessor \(z=x'-t'+s'\). Population irreducibility reaches \(z\) from \(x\), then the specified channel reaches \((x',t')\). This argument genuinely uses the labelled last channel and does not infer a mark from a possibly nonunique displacement.

### 2. Exact potential and source entropy

At \((x,t)\), after \(s\to u\) fires, the residual changes from \(x-t\) to \(x-s\). Therefore

\[
\exp(\Delta V)
=\prod_i\frac{(x_i-s_i)!}{(x_i-t_i)!}
=\frac{(x)_t}{(x)_s}.
\]

Both factorial denominators are defined because \(s\) and \(t\) are enabled. In particular \(s=t\) gives exact zero, not merely an asymptotic cancellation.

Aggregating only by source for the next-source probability,

\[
p_x(s)=\frac{\bar\kappa_s(x)_s}{\Lambda(x)},
\]

substitution of \((x)_s=p_x(s)\Lambda(x)/\bar\kappa_s\) into the expected increment gives

\[
\delta(x,t)=\log p_x(t)-\sum_s p_x(s)\log p_x(s)
+\sum_s p_x(s)\log\bar\kappa_s-\log\bar\kappa_t.
\]

The entropy term is at most \(\log|\mathcal C|\), and the rate term is at most \(\log(\bar\kappa_+/\bar\kappa_-)\). The zero complex causes no exception because \((x)_0=1\).

### 3. Episodes and arbitrarily separated rates

At phase \(y_k\), the probability of the designated labelled channel is

\[
p_k\frac{\kappa_{y_k\to y_{k+1}}}{\bar\kappa_{y_k}}=p_kq_k.
\]

Every alternative channel stops the episode immediately, but its reward contributes to the unconditional first-step mean \(\delta_k\). Conditional on the designated channel, the reward is zero and the next augmented state is exactly \((\rho+y_{k+1},y_{k+1})\). This establishes the recursion without discarding deviations.

The envelope calculation is also exact. If \(M<-1/q\), the maximizer \(p=(-qM)^{-1}\) may itself tend to zero, but

\[
F_q(M)=C_0-1-\log(-qM)\longrightarrow-\infty.
\]

Thus a tiny intermediate continuation probability cannot erase terminal negative drift; it only weakens its scale through a finite nested logarithm. Positivity, not quantitative separation, of every designated channel rate is what is needed.

### 4. Compactification and the decisive binary case split

For a divergent residual subsequence, at least one coordinate lies in \(I\), so \(R_n\to\infty\). A coordinate may diverge with normalized weight zero; retaining it in \(I\) is essential.

Let \(h(y)=w\cdot y\), \(h_*=\max h\), and \(\mathcal T=\{y:h(y)=h_*\}\). The proof's trichotomy is exhaustive:

- **A: all complexes are top.** Then \(w\cdot(y'-y)=0\) for every reaction, while \(w\cdot x^{(n)}\to\infty\). This contradicts constancy on the communicating class.
- **B: a top complex has two particles on coordinates in \(I\).** Molecularity at most two leaves no bounded-coordinate requirement. Its source is eventually enabled directly by the residual, including \(2S_i\), over any chosen lower terminal complex.
- **C: every top complex has exactly one \(I\)-particle.** Since its weight must be positive, every divergent species appearing in a top complex has weight \(h_*\); call this set \(\mathcal J\). No complex can contain two \(\mathcal J\)-particles. A complex is top exactly when it contains one \(\mathcal J\)-particle. If a unary \(S_i\) is top, it is available over every lower complex. Otherwise each top is \(S_i+D\) with \(D\notin I\). If a lower terminal contains one such companion, the corresponding top source is enabled. If no lower complex contains any companion, then

  \[
  \ell(x)=\sum_{i\in\mathcal J}x_i-\sum_{D\in\mathcal D}x_D
  \]

  is zero on every complex and hence invariant reaction by reaction. Its positive coordinates diverge and its negative coordinates are fixed because every \(D\notin I\), a contradiction.

The subtle zero-weight divergent case does not escape this split. If such a species occurs as an additional particle in a top complex, that complex has two \(I\)-particles and is in B; in C, every companion is outside \(I\), not merely of weight zero.

In the availability branch, fixed \(s,c\) have \(h(s)>h(c)\) and are both enabled at \(\rho^{(n)}+c\). Falling-factorial asymptotics then gives

\[
\frac{(\rho^{(n)}+c)_s}{(\rho^{(n)}+c)_c}\to\infty,
\]

so the terminal source probability for \(c\) tends to zero. Strong connectivity supplies a fixed target-following path from any carried target to that terminal, and the scalar recursion propagates its drift backward.

### 5. Foster, trace, and physical time

The Foster step does not apply optional stopping at an unbounded time. It applies the supermartingale inequality at deterministic \(N\), drops the nonnegative potential, and sends \(N\to\infty\) by monotone convergence. At fixed \(N\), at most \(|\mathcal C|N\) binary reactions have occurred, so all coordinates and log-factorials are deterministically bounded. This discharges integrability.

For the finite trace, a return in trace transitions alone would be insufficient: original-jump excursion lengths could in principle have infinite mean. The manuscript addresses exactly this interface. Each start in finite \(K\) has expected next-\(K\) time bounded by a finite common \(B\). If \(M\) is the finite-mean trace return count and \(E_j\) its original-jump excursion lengths, then

\[
\mathbb E\sum_{j<M}E_j
\le B\sum_{j\ge0}\mathbb P(j<M)
=B\,\mathbb EM<\infty.
\]

Projection loses information and can only make the first population return earlier than the marked return.

Finally, positive recurrence of an embedded chain does not by itself guarantee the manuscript's CTMC claim if rates can vanish at infinity. Here they cannot: in a nonabsorbing irreducible class at least one genuine channel is enabled at every state, and its positive falling factorial is an integer at least one. Thus \(\Lambda(x)\ge\kappa_{\min}>0\). Conversely, arbitrarily large rates cannot cause explosion because the recurrent embedded chain visits a fixed anchor infinitely often and the anchor's independent exponential holding-time subseries has divergent sum. These two one-sided rate arguments establish respectively finite expected physical return time and nonexplosion.

## Boundary and counterexample attacks

| Attempted failure mode | Test or construction | Why it does not defeat the theorem |
|---|---|---|
| Zero complex | Cycles containing (0\), including (0\rightleftarrows2A\) and the manuscript's delayed-restoration cycle | \((x)_0=1\); lifted paths use nonnegative residual; the marked identity and entropy formula remain defined. |
| Self channels | Added (y\to y\) at high rate | Such channels have zero generator increment and are removed from the minimal population CTMC. They cannot create a population jump or change recurrence. |
| Parallel channels | Duplicated a source-target channel and varied its two rates | Aggregation adds rates without changing the population generator. A designated labelled-channel fraction stays strictly positive. |
| Equal displacements, different complexes | Compared (A\to2A\) and (B\to A+B\), both displacement (+A\) | The augmentation samples the actual channel and retains its actual target; it never infers the mark from displacement. |
| Coordinate face | Used (0\to A+B\to B\to0\) from ((n,0)\) | The created target supplies exactly the missing boundary species. The fixed directed path is enabled in lifted form, and the terminal (B\)-marked drift is negative of logarithmic order. |
| Parity/lattice class | Used (0\rightleftarrows2A\) | Even and odd reachable sets stay separate but are individually closed communicating classes; the return-path lift respects parity. The death propensity grows quadratically and no escape counterexample results. |
| Repeated species | Tested sources (2S_i\) in the compactification | If (S_i\) diverges, both particles are eventually available. The factorial asymptotic contributes twice the normalized log weight. |
| Absent species | Added a coordinate never occurring in any complex | It is constant along every reaction path. It cannot diverge inside a fixed class, and it supplies an exact invariant if needed. |
| Divergent coordinate with (w_i=0\) | Allowed (\rho_i\to\infty\) slower than all positively weighted coordinates | It remains in (I\). In case B it counts toward source availability; in case C it cannot be misclassified as a bounded companion. |
| Zero-length target path | Chose terminal (c=t\) | The episode is one ordinary jump and (J_0=\delta(\rho+t,t)\); no empty stopping-time or missing reward occurs. |
| Arbitrarily separated positive rates | Sent one edge rate toward zero while keeping it positive | The finite envelope uses only fixed (q_k>0\). The exceptional set can move arbitrarily far, but terminal negative divergence still propagates for each fixed positive rate vector. |
| Absorbing state | Chose a boundary state enabling no genuine population-changing reaction | Weak reversibility does not force an unavailable channel to fire. Its reachable set is the singleton, correctly assigned the point mass. |
| Multiple linkage classes | Tried to make a useful terminal lie in another linkage class | This breaks the path library and is explicitly outside the recurrence theorem; the manuscript claims only the closure lemma in this regime. |
| Molecularity three | Tried a top complex with one divergent particle and two bounded companions | This creates an additional availability configuration not covered by the binary trichotomy. It is explicitly outside the theorem and identified as an open extension. |

No failed counterexample was rejected merely because a test implementation excluded it; the exclusions above follow from the stated theorem hypotheses or from exact population-state algebra.

## Re-derived examples and independent finite checks

### Delayed-restoration cycle

For

\[
0\xrightarrow{\kappa_0}A+B\xrightarrow{\kappa_1}B\xrightarrow{\kappa_2}0,
\]

starting from marked (((n,0),0)\), the first designated jump has zero increment. At ((n+1,1)\), the designated (A+B\to B\) probability is

\[
\frac{\kappa_1(n+1)}{\kappa_0+\kappa_2+\kappa_1(n+1)}.
\]

At the resulting (((n,1),B)\), direct use of the target/source identity gives

\[
-\frac{\kappa_1n}{\kappa_0+\kappa_2+\kappa_1n}\log n.
\]

The deviations one phase earlier have total probability (O(n^{-1})\) and (O(\log n)\) rewards, so they contribute (O(\log n/n)\). The episode is therefore \(-\log n+o(\log n)\), as claimed at PDF pp. 2–3, equations (4)–(5), TeX lines 130–158.

### Anderson--Cappelletti--Kim boundary example

For

\[
A\to A+B\to A+C\to C\to2B\to A,
\]

I recomputed each source propensity at the manuscript's states. The denominators (L_1,L_2,L_3\), continuation probabilities (p_0,p_1,p_2\), and branch rewards \(\delta_1,\delta_2,\delta_3\) in equation (10) agree. Multiplying the three limiting continuation factors yields

\[
\alpha=
\frac{\kappa_1}{\kappa_1+\kappa_2}
\frac{2\kappa_2}{\kappa_1+2\kappa_2}
\frac{\kappa_3}{\kappa_1+\kappa_2+\kappa_3}>0,
\]

and the complete episode is \(-\alpha\log n+O(1)\). This independently confirms PDF pp. 5–6 and TeX lines 401–450.

### Rate-dependence example

For (0\to A\to A+B\to0\), I re-derived (a_m,p_m,b_m,q_m,c_m\) from the three carried-target states and obtained

\[
D_0(m,A)=-\frac{\kappa_2}{\kappa_1+\kappa_2}\log m
+O\!\left(\frac{\log m}{m}\right).
\]

For fixed (m\), sending \(\kappa_2\downarrow0\) makes (q_mc_m\to0\), while the remaining expression tends to (a_m(1+p_m)>0\). Thus the example really shows that no rate-independent bound on the location or diameter of (K\) follows from the theorem. PDF pp. 10–11, equations (31)–(33), TeX lines 843–890.

### Independent scratch oracles

These checks were written and run independently and did not import a production helper or read the packet's code/tests:

1. **Exact factorial identity:** over all binary complexes in two species, populations with each coordinate (0,\ldots,5\), every enabled carried target and next source, and every binary next target, I compared factorial differences directly with the falling-factorial ratio. All 5,238 applicable cases agreed exactly.
2. **Top-case falsification enumeration:** for every nonempty subset of binary complexes in (d=2\) and (d=3\), bounded normalized integer weight patterns in \(\{0,1,2\}^d\), and choices allowing (I\) to strictly contain the positive-weight support, I independently classified A/B/C and tested each advertised availability or invariant branch. Results were:
   - (d=2\): 756 cases; A 124, B 506, C-unary 98, C-companion 24, C-signed 4; no failure.
   - (d=3\): 57,288 cases; A 2,548, B 47,706, C-unary 4,790, C-companion 2,028, C-signed 216; no failure.

   This is finite falsification evidence, not a proof for arbitrary real weights; the analytic case split above is the proof.
3. **Episode recursion:** direct enumeration of all terminal branches of a three-phase toy episode agreed with the nested recursion exactly. A separate rational branch table with designated probabilities (2/3,3/5\), deviation contributions (1/6,-1/10\), and terminal mean \(-1/2\) gave both direct and recursive expectation \(-1/10\).
4. **Scalar envelope:** direct maximization on a dense (p\)-grid on both sides of (M=-1/q\), followed by exact derivative checks, agreed with both branches and continuity at the boundary.

A larger (d=4\) exploratory enumeration did not complete within its 30-second scratch limit and produced no result; I do not count it as evidence.

## Citation, novelty, and prior-work checks

The cited literature is not bundled. I checked the material comparisons against public primary or official sources where available:

- Anderson and Kim's paper does formulate the weak-reversibility positive-recurrence program and sufficient conditions: [SIAM DOI 10.1137/17M1161427](https://doi.org/10.1137/17M1161427) and [author/arXiv HTML](https://arxiv.org/html/1710.11263).
- The 2020 Anderson--Cappelletti--Kim theorem has the binary, one-linkage, pure-species condition described in the manuscript. Their published Section 6.1 uses the (S_v/2S_v\) boundary branch in the way summarized here: [publisher DOI 10.1017/jpr.2020.28](https://doi.org/10.1017/jpr.2020.28) and [author-hosted paper PDF](https://people.math.wisc.edu/~dfanderson/papers/ACK2019.pdf).
- Paulevé--Craciun--Koeppl Lemmas 4.5--4.6 state the discrete return/reversibility criterion and weak-reversibility consequence matching the manuscript's terminology warning: [author-hosted final PDF](https://people.math.wisc.edu/~craciun/PAPERS_NEW/Pauleve_Craciun_Koeppl_JMB_2014_FINAL.pdf) and [DOI 10.1007/s00285-013-0686-2](https://doi.org/10.1007/s00285-013-0686-2).
- Xu's version 2 says every bimolecular weakly reversible stochastic mass-action system is nonexplosive and still describes bimolecular positive recurrence as open: [arXiv abstract/version record](https://arxiv.org/abs/2409.05340) and [v2 HTML](https://arxiv.org/html/2409.05340v2).
- The two-species result is publicly described as complete while its manuscript is listed as “in preparation” on the [official ConStRAINeD publications page](https://constrained.polito.it/publications/). The [University of Geneva 2022 program](https://www.unige.ch/jpe75conference/program.html) and the [official SIAM AG25 abstract book](https://www.siam.org/media/13rgukxr/ag25_abstracts.pdf) support the talk history and two-dimensional scope.
- The deterministic single-linkage permanence comparison matches the [SIAM primary article, DOI 10.1137/19M1248431](https://doi.org/10.1137/19M1248431).
- The standard Markov-chain and regenerative interfaces cited at the end are covered by the official book records and contents for [Norris, *Markov Chains*](https://www.cambridge.org/core/books/markov-chains/A3F966B10633A32C8F06F37158031739), [Meyn--Tweedie, *Markov Chains and Stochastic Stability*](https://www.cambridge.org/core/books/markov-chains-and-stochastic-stability/E2B82BFB409CD2F7D67AFC5390C565EC), and [Asmussen, *Applied Probability and Queues*](https://link.springer.com/book/10.1007/b97236). The manuscript also supplies the specialized Foster, trace, and CTMC arguments, so the main theorem is not resting on an unidentified black-box variant.

These checks found no material citation mismatch. Public exact-title and topic searches did not reveal a manuscript duplicating the present arbitrary-species, one-linkage binary result. That is evidence consistent with the novelty discussion, not an exhaustive proof of priority. In particular, absence of a publicly indexed manuscript cannot establish that no unpublished or newly posted result exists.

## Severity-ranked findings

### Blocker

None found in the analytic proof.

### Major

None found in the analytic proof.

### Minor

**M1. The stated v1.2.4 tagged repository directory was not publicly available at the time of review.**

- Location: PDF p. 14, “Code and supporting materials availability”; `paper_content.tex` lines 1139–1146. Related wording at lines 1148–1151 says Version 1.2.4 supersedes publicly available earlier versions.
- Manuscript claim: the verifier, tests, reports, sources, manifest, and supporting materials “are available” in the tagged Version 1.2.4 repository directory, and the release records the exact commit and hashes.
- Reproduction at 2026-08-21 22:28 PDT:
  - [exact claimed v1.2.4 tree URL](https://github.com/AlecKriebel/Math/tree/bimolecular-positive-recurrence-v1.2.4/bimolecular_positive_recurrence_submission_v1_2_4) returned 404;
  - the [public tag list](https://github.com/AlecKriebel/Math/tags) showed `bimolecular-positive-recurrence-v1.2.3` but not v1.2.4;
  - `git ls-remote --tags https://github.com/AlecKriebel/Math.git refs/tags/bimolecular-positive-recurrence-v1.2.4 refs/tags/bimolecular-positive-recurrence-v1.2.3` returned only v1.2.3 (`28217b5cb783d328ef404fefea66d1539a656487`).
- Consequence: the copied packet's content hashes can be recorded, but its asserted tagged provenance and public release record are not independently verifiable.
- Repair: publish the exact tag and verify that it resolves to the claimed durable tree/commit, or revise the availability statement and preprint status to say when and where v1.2.4 will be made public. This does not alter the theorem or proof.

### Notes

**N1. Novelty verification is necessarily time-bounded.** The public primary and official sources checked are consistent with the manuscript's comparison, including the still-in-preparation two-species work and Xu v2's open-problem statement. A journal should still run its normal literature/priority process.

**N2. The abstract's phrase “stationary law rather than escape to infinity” is informal, not a proof claim.** The introduction correctly states that positive recurrence does not mean paths remain bounded (PDF p. 2; TeX lines 55–62), so I do not regard this as a mathematical error.

## Residual uncertainty

1. I intentionally did not inspect code, tests, canonical reports, manifests, release archives, audit records, or other referee reports before writing this preliminary assessment. Nothing here certifies their correctness, independence, completeness, or byte reproducibility.
2. The exact Git commit intended for v1.2.4 cannot be inferred from a copied non-Git packet, and the public tag was absent when checked.
3. Several book chapters were verifiable only through official metadata/table-of-contents pages rather than unrestricted full text. The manuscript's relevant arguments are, however, explicitly reconstructed and sufficient at the interfaces where those books are cited.
4. Priority/novelty searching cannot rule out unpublished, unindexed, or just-posted work. I verified consistency with the identified primary and official public sources, not absolute priority.
5. Finite scratch enumerations are only counterexample searches. The positive mathematical conclusion rests on the analytic derivations above, especially the full binary top-complex argument and the trace/CTMC conversion.

## Final validity conclusion for this blind track

Every necessary analytic implication I could identify survives explicit reconstruction: lifted closure, marked irreducibility and projection, exact factorial algebra, treatment of all episode branches, scalar propagation, zero-weight compactification, the complete binary top trichotomy, the proper finite Foster set, bounded-time supermartingale reasoning, finite-trace conversion, nonexplosion, finite physical return, regeneration, uniqueness, and absorbing states. I found neither an exact counterexample nor an unresolved substantive proof obligation. The supporting computation remains for the separated software referee and cannot be used as the mathematical justification. The narrowest defect is the reproducible public-release availability discrepancy in M1.

**Final mathematical status: CORE RESULT SOUND, REVISION REQUIRED.**  
**Journal recommendation: minor revision.**
