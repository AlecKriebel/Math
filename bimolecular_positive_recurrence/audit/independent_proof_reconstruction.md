# Independent proof reconstruction

**Version audited:** discovery manuscript preserved in `discovery_version/`  
**Audit date:** 6 August 2026  
**Scope:** binary/bimolecular, weakly reversible, one linkage class, arbitrary positive stochastic mass-action rates, each closed communicating class.

This reconstruction uses only the final marked-target argument. It does not use the speculative tier, fast-slow, cycle-pivot, or bounded-defect hierarchy developed during earlier phases.

## A1. Exact stochastic model

Let the finite species set be \(\mathcal S=\{S_1,\dots,S_d\}\). A complex is \(y\in\mathbb N_0^d\), with molecularity \(|y|=\sum_i y_i\). A reaction channel is a labelled directed edge \(r:y_r\to y_r'\) with \(\kappa_r>0\). Labels matter: channels with the same displacement but different sources or targets are distinct.

The network is binary/bimolecular when every complex has molecularity at most two. In a weakly reversible graph every complex lies on a directed cycle and is therefore a source, so this agrees with the usual second-order terminology in the cited literature.

For \(x\in\mathbb N_0^d\),
\[
 (x)_y=\begin{cases}
 \prod_i x_i!/(x_i-y_i)!,&x\ge y,\\
 0,&\text{otherwise}.
 \end{cases}
\]
Channel \(r\) has propensity \(\kappa_r(x)_{y_r}\). The binomial-coefficient convention differs only by a fixed source factorial and is absorbed into the positive rate constants.

A closed communicating class \(\Gamma\) is an irreducible class with no enabled transition leaving it. Positive recurrence means finite expected positive return time to one, hence every, state. Every finite closed communicating class is positive recurrent: its finite irreducible jump chain has a stationary probability distribution, all state rates are finite, and the corresponding finite-state CTMC is nonexplosive. Singleton absorbing classes are included in this reduction. If all complexes have equal molecularity, every reaction preserves total molecule count, and every communicating class is contained in a finite shell. The proof therefore fixes an infinite closed irreducible class and a strongly connected complex graph with at least two vertices.

Self channels have zero generator contribution and are removed. Exact parallel channels with the same source and target may be aggregated by adding rates. This does not merge channels with different marks.

## A2. Reaction-channel marking

Construct the discrete embedded chain first. At population state \(x\), select the actual enabled channel \(r\) with probability
\[
 \frac{\kappa_r(x)_{y_r}}{\Lambda(x)},\qquad
 \Lambda(x)=\sum_q\kappa_q(x)_{y_q}.
\]
After the channel fires, mark its actual target \(t=y_r'\). The augmented state is \((x,t)\), where \(x\) is the post-jump population. If the next marked channel is \(s\to u\), then
\[
 (x,t)\mapsto(x-s+u,u).
\]
The law is Markov because it depends on the current population and the selected actual channel; projection gives the ordinary population embedded chain.

Let \(\widetilde\Gamma\) be the reachable augmented states after genuine jumps. It is closed. It is also irreducible: for \((x,t),(x',t')\in\widetilde\Gamma\), reachability of the second state supplies a predecessor \(z=x'-t'+s'\in\Gamma\) and a channel \(s'\to t'\). Population irreducibility gives a marked path from \(x\) to \(z\); appending that actual channel reaches \((x',t')\).

The target cannot be inferred from displacement. Two channels may have equal displacement and different sources/targets; the verifier includes this adversarial case.

## A3. Proper residual factorial potential

If the preceding channel was \(s\to t\), then its post-jump state is \(x=z-s+t\ge t\). Thus the carried target is enabled and
\[
 r=x-t\in\mathbb N_0^d.
\]
Define
\[
 V(x,t)=\sum_i\log((x_i-t_i)!)=\sum_i\log(r_i!).
\]
Here \(\log(0!)=0\), so \(V\ge0\). Since \(\log(n!)\to\infty\), each residual coordinate is bounded on a sublevel set; the set of targets is finite. Every augmented sublevel is therefore finite.

If the next channel is \(s\to u\), the new residual is \(x-s\), and
\[
 \exp(\Delta V)
 =\prod_i\frac{(x_i-s_i)!}{(x_i-t_i)!}
 =\frac{(x)_t}{(x)_s}.
\]
Hence
\[
 V(x-s+u,u)-V(x,t)=\log\frac{(x)_t}{(x)_s}.
\]
When \(s=t\), the increment is exactly zero.

## A4. One-jump entropy bound

For every complex \(y\), let
\[
 \bar\kappa_y=\sum_{r:y_r=y}\kappa_r.
\]
After self channels are removed, strong connectivity with at least two vertices gives \(\bar\kappa_y>0\). Let \(\bar\kappa_-\) and \(\bar\kappa_+\) be the finite positive minimum and maximum.

For enabled source complexes,
\[
 p_x(y)=\frac{\bar\kappa_y(x)_y}{\Lambda(x)};
\]
set it to zero when disabled and use \(0\log0=0\) only in entropy expressions. The carried target is enabled, so \(p_x(t)>0\). The expected one-jump increment is
\[
 d(x,t)=\sum_{s:\,x\ge s} p_x(s)\log\frac{(x)_t}{(x)_s}.
\]
Because \((x)_s=p_x(s)\Lambda(x)/\bar\kappa_s\), exact substitution yields
\[
 d(x,t)=\log p_x(t)-\sum_{s:\,x\ge s}p_x(s)\log p_x(s)
 +\sum_{s:\,x\ge s}p_x(s)\log\bar\kappa_s-\log\bar\kappa_t.
\]
The entropy term is at most \(\log|\mathcal C|\); the rate term is at most \(\log(\bar\kappa_+/\bar\kappa_-)\). Therefore
\[
 d(x,t)\le\log p_x(t)+C_0,
 \qquad C_0=\log|\mathcal C|+\log(\bar\kappa_+/\bar\kappa_-).
\]
For the zero source, \((x)_0=1\), so there is no exceptional branch.

## A5. Honest target-following episodes

For every ordered pair \((t,c)\), strong connectivity supplies a simple path of actual marked channels
\[
 t=y_0\to y_1\to\cdots\to y_L=c,
 \qquad 0\le L\le|\mathcal C|-1.
\]
Starting from \((r+t,t)\), at phase \(y_k\) continue only if the exact designated channel \(y_k\to y_{k+1}\) fires. Stop immediately after any deviation. If \(c\) is reached, take one final ordinary jump and stop. When \(c=t\), the path has length zero and the episode is exactly that final jump.

This is a stopping time for the marked embedded filtration. Along designated edges,
\[
 r+y_0\to r+y_1\to\cdots\to r+c.
\]
The designated source is literally present at every step, the residual remains \(r\), and every state remains in the fixed closed class. The episode has between one and \(|\mathcal C|\) jumps and finitely many terminal branches.

Let
\[
 q_k=\kappa_{y_k\to y_{k+1}}/\bar\kappa_{y_k}>0,
 \qquad p_k=p_{r+y_k}(y_k).
\]
If \(J_k(r)\) is the expected remaining reward from phase \(k\), then
\[
 J_L=d(r+c,c),\qquad
 J_k=d(r+y_k,y_k)+q_kp_kJ_{k+1}.
\]
Continuation has exactly probability \(q_kp_k\), and the designated edge itself has zero immediate reward.

## A6. Full scalar envelope

For \(q>0\) and \(M\in\mathbb R\), set
\[
 F_q(M)=\sup_{0<p\le1}\{\log p+C_0+qpM\}.
\]
The objective is strictly concave, with derivative \(p^{-1}+qM\). Therefore
\[
 F_q(M)=\begin{cases}
 C_0+qM,&M\ge-1/q,\\
 C_0-1-\log(-qM),&M<-1/q.
 \end{cases}
\]
The first branch includes equality. In the second branch the unique maximizer is \((-qM)^{-1}\in(0,1)\). Both branches are exact calculus statements, not numerical checks. In particular, \(M_n\to-\infty\) implies \(F_q(M_n)\to-\infty\).

If the terminal source probability tends to zero, then \(J_L\le\log p_{r+c}(c)+C_0\to-\infty\). Applying the scalar envelope backward through the fixed finite path proves that the complete initial episode reward tends to \(-\infty\).

## A7. Logarithmic compactification

Take any divergent sequence in \(\widetilde\Gamma\). Pass to a subsequence with one carried target \(t\), and put \(r^{(n)}=x^{(n)}-t\). A diagonal extraction makes each residual coordinate either a fixed nonnegative integer or divergent. Let \(I\) be all divergent coordinates and
\[
 R_n=\sum_{i\in I}\log(r_i^{(n)}+1).
\]
After another subsequence,
\[
 w_i=\lim_n\frac{\log(r_i^{(n)}+1)}{R_n}
\]
exists for \(i\in I\), and set \(w_i=0\) outside \(I\). Then \(w\ge0\) and \(\sum_iw_i=1\). A slower divergent coordinate may have \(w_i=0\); it remains in \(I\) and is not treated as bounded.

For every fixed enabled binary complex \(y\) and fixed terminal \(c\),
\[
 \log(r^{(n)}+c)_y=R_n w\cdot y+o(R_n).
\]
For \(y_i=1\), this follows from \(\log(r_i+c_i)=\log(r_i+1)+o(R_n)\). For \(y_i=2\),
\[
 \log((r_i+c_i)(r_i+c_i-1))=2\log(r_i+1)+o(R_n).
\]
Fixed enabled coordinates contribute only \(O(1)\).

## A8. Exhaustive top-complex alternative

Let \(h(y)=w\cdot y\), \(a=\max_yh(y)\), and \(T=\{y:h(y)=a\}\).

### Case 1: every complex is top

Then \(w\cdot(y'-y)=0\) for every reaction. Thus \(w\cdot X\) is a nonnegative linear invariant. At least one positive-weight coordinate diverges, so its value tends to infinity along a sequence inside one class, impossible.

### Case 2: a top complex contains two particles from divergent coordinates

Bimolecularity leaves no bounded-coordinate particle in that complex. Its required particles are eventually present in the residual, including the case \(2S_i\). Hence it is enabled at \(r^{(n)}+c\) for every lower terminal complex \(c\), and has strictly greater weight.

### Case 3: every top complex contains exactly one divergent particle

Let \(K\) be the divergent species appearing in top complexes. For each \(i\in K\), the other possible particle is not divergent and has weight zero, so \(w_i=a\). No complex contains two \(K\)-particles, since that would have weight at least \(2a>a\). Moreover,
\[
 y\in T\iff q_K(y)=\sum_{i\in K}y_i=1.
\]

- **3a.** If every complex has \(q_K=1\), then \(M_K=\sum_{i\in K}X_i\) is a nonnegative invariant and diverges, impossible.
- **3b.** If a unary top complex \(S_i\) exists, it is enabled over every lower terminal.
- **3c.** Otherwise every top complex is \(S_i+D\) with a service species \(D\notin I\). If a lower complex contains one such \(D\), the corresponding top source is enabled over it.
- **3d.** If no lower complex contains a service species, let \(\mathcal D\) be the distinct service species. Then
  \[
  M_K-\sum_{D\in\mathcal D}X_D
  \]
  has the same value (zero) on every complex and is a signed linear stoichiometric invariant. Its positive part diverges, while the service coordinates are fixed along the extracted sequence. Its class value would tend to infinity, impossible.

The cases are exhaustive for molecularity at most two. The statement is “at least one alternative,” not logical exclusivity; overlaps do not affect the proof. The term “conservation law” is reserved for nonnegative invariants, while the last functional is explicitly signed.

A species absent from every complex has its own reaction-wise invariant coordinate and cannot diverge within a fixed class.

In every availability branch there are fixed complexes \(s,c\) with \(h(s)>h(c)\), and both are enabled at \(r^{(n)}+c\).

## A9. Terminal probability and uniformization

The strict weight gap and falling-factorial asymptotics give
\[
 \frac{(r^{(n)}+c)_s}{(r^{(n)}+c)_c}\to\infty.
\]
Therefore
\[
 p_{r^{(n)}+c}(c)
 \le\frac{\bar\kappa_c(r^{(n)}+c)_c}
 {\bar\kappa_s(r^{(n)}+c)_s}\to0.
\]

Let \(D_c(x,t)\) be the exact expected increment of the fixed \((t,c)\)-episode, and define
\[
 K=\{(x,t):\min_cD_c(x,t)>-1\}.
\]

If \(K\) were infinite, properness of \(V\) would give a divergent sequence in \(K\). The compactification either produces an invariant contradiction or a fixed terminal \(c\) whose episode drift tends to \(-\infty\), contradicting the definition. Thus \(K\) is finite.

It is also nonempty. Choose a global minimizer \(z_*\) of the proper nonnegative function \(V\). Every episode endpoint remains in the augmented class and has potential at least \(V(z_*)\). Hence every episode drift from \(z_*\) is nonnegative, so \(z_*\in K\).

Outside \(K\), choose the lexicographically first minimizer before the episode begins. The selector is deterministic and measurable on a countable state space and restarts under the strong Markov property. The selected episode has at most \(|\mathcal C|\) jumps and expected drift at most \(-1\).

## A10. Random-time Foster argument

Let \(Y_0=z\), and let \(Y_{n+1}\) be the selected episode endpoint. Put \(\sigma_K=\inf\{n:Y_n\in K\}\). For bounded \(N\), telescope only through \(N\wedge\sigma_K\):
\[
 \mathbb E_zV(Y_{N\wedge\sigma_K})+
 \mathbb E_z(N\wedge\sigma_K)\le V(z).
\]
Since \(V\ge0\), monotone convergence gives \(\mathbb E_z\sigma_K\le V(z)\). Each episode has at most \(|\mathcal C|\) original jumps, so the augmented embedded chain hits \(K\) in finite expected jump count.

## A11. Finite trace-chain closure

Let \(T_K^+=\inf\{n\ge1:Z_n\in K\}\). Starting from \(k\in K\), take one ordinary jump. There are finitely many channel successors, and each has finite mean hitting time of \(K\). Hence \(\mathbb E_kT_K^+<\infty\).

Successive visits to finite \(K\) form an irreducible trace chain. Fix \(k_*\in K\). From each trace state choose a finite positive-probability path to \(k_*\). Finiteness yields common \(m\) and \(\varepsilon>0\) such that \(k_*\) is hit within the next \(m\) trace steps with probability at least \(\varepsilon\), from every trace state. Starting at \(k_*\), first take one trace transition and then use geometric blocks. The positive trace return time has finite mean.

Let \(B=\max_{k\in K}\mathbb E_kT_K^+\). If \(M\) is the positive trace return count and \(L_j\) is the length of its \(j\)-th original-chain excursion, then \(\mathbb E[L_j\mid\mathcal F_j]\le B\). Tonelli gives
\[
 \mathbb E\sum_{j<M}L_j\le B\mathbb EM<\infty.
\]
Thus the augmented embedded chain has finite mean positive return to \(k_*\). Its population projection returns to the population coordinate no later.

## A12. Direct CTMC conversion and nonexplosion

At every augmented state the carried target is enabled, so
\[
 \Lambda(x)\ge\bar\kappa_t(x)_t\ge\bar\kappa_->0.
\]
Let \(N\) be the finite-mean embedded positive return count and \(H_j\) the holding times. Conditional on the embedded path, \(H_j\) has mean \(1/\Lambda(X_j)\). Hence
\[
 \mathbb E\sum_{j=0}^{N-1}H_j
 \le \frac{\mathbb EN}{\bar\kappa_-}<\infty.
\]

Nonexplosion is proved internally. Positive recurrence of the augmented embedded chain makes \(k_*=(x_*,t_*)\) recurrent, so it is visited infinitely often almost surely. The holding time following each visit is an independent exponential variable with the same finite rate \(\Lambda(x_*)\). Their infinite sum diverges almost surely. Total physical time dominates this subseries, so jumps cannot accumulate in finite time. The minimal CTMC is nonexplosive and has finite mean positive return.

## Mandatory adversarial examples

| Example | Result |
|---|---|
| Zero complex as source or target | \((x)_0=1\); target zero is enabled; all identities and episodes remain valid. |
| \(2A\) | The factor \(x_A(x_A-1)\) has normalized log weight \(2w_A\). |
| \(A+B\) | Mixed falling factorials add the two coordinate weights. |
| Permanent coordinate face | Every path is an actual enabled channel path inside the fixed class. |
| Divergent species with \(w_i=0\) | It remains in \(I\), preventing false bounded-defect reasoning. |
| Species absent from all complexes | Its count is reaction-wise invariant. |
| Shared service species | \(\mathcal D\) is a set, so each service coordinate is counted once. |
| Parallel channels | Exact source-target duplicates may be combined by rate addition. |
| Same displacement, different mark | Channels remain distinct and the actual target is recorded. |
| \(c=t\) | The designated path has length zero and the episode is one final jump. |
| Equal molecularity | Total count is conserved and each class is finite. |
| Absorbing singleton | Handled before augmentation. |
| Signed invariant | Named a signed linear stoichiometric invariant, not a nonnegative conservation law. |
| Parity/lattice restriction | All constructed transitions are actual transitions in the class. |
| \(0\to A+B\to B\to0\) | Boundary one-step growth is handled by complete target-following episode drift. |

## Audit conclusion

No substantive defect was found. Three interfaces were made explicit in Version 0.2: actual-channel marking, nonemptiness of the exceptional set, and direct embedded-chain-to-CTMC/nonexplosion conversion. The reconstructed proof supports the stated binary, one-linkage theorem and no broader claim.
