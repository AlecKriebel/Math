# Independent exact-byte audit of the both-available current-target theorem

**Audit date:** 2026-08-12 PDT.  
**Target:** `research_notes/proof_first_both_available_current_target_theorem.md`  
**Target SHA-256:**

```text
157e94cd035dec9a41947129dfcbbab0ebc6e72c01abde6bcf6626052954f1ed
```

The frozen target has 320 lines and 13,664 bytes.

## 1. Verdict and exact scope

**STRICT PASS** for the scoped theorem stated in target Theorem 5.1: on a
terminal two-active chart in which both linkages satisfy the
available-target alternative, the marked physical chain has an all-clock
negative-drift-or-structural-exit episode from every sufficiently large
state.  The proof retains arbitrary strong orientations, arbitrary fixed
positive labelled rates, actual endpoints, physical duration, and arbitrary
relative source rarity.

The pass includes the symbolic bridge from the inherited Q/U/C top
classifier to the available-target hypothesis.  That bridge is proved in
Section 3 below; a replay over the finite support universe was used only as a
regression check and is not the proof.

This verdict does **not** assert a generic theorem for one available and one
shielded linkage.  It does not replace any of the literal residual pair
theorems, and by itself it is not the global T3-2 theorem.  It closes exactly
the upstream both-available seam identified by the hostile audit of the
two-linkage composition.

## 2. Exact marked identity: pass

After a reaction \(y\to u\), the new population is \(x-y+u\) and the new
mark is its actual target \(u\).  Thus

\[
 F(x-y+u,u)-F(x,t)
 =\sum_i\log{(x_i-y_i)!\over(x_i-t_i)!}
 =\log{(x)_t\over(x)_y}.                              \tag{2.1}
\]

Because an actual target satisfies \(x\ge t\), \(t\) is an enabled source
of its strong linkage.  With \(p_y=K_y(x)_y/\Lambda(x)\), the pointwise
identity

\[
 \log{(x)_t\over(x)_y}
 =\log p_t-\log p_y-\log K_t+\log K_y              \tag{2.2}
\]

gives target (1.4) on averaging.  Shannon entropy on at most ten sources and
the finite fixed rate vector imply

\[
 D(x,t)\le\log p_t+C_K.                              \tag{2.3}
\]

Also, since \(\log p_t\le0\),

\[
 \left[\log{(x)_t\over(x)_y}\right]_+
 \le C+\log(1/p_y).
\]

The elementary bound
\(r(1+\log(1/r))^q\le C_q\) proves target (1.6) for every
fixed \(q\).  Parallel labels merely split one source probability by fixed
positive fractions.  No target label or clock is deleted.

## 3. Symbolic Q/U/C classifier bridge: pass

This is the point at which a pre-mark diagnostic can be misleading.  A
C-type top source may be disabled before some activation, but the theorem
does not start from that source.  It starts from the **actual carried target**
\(t\), which is necessarily enabled.  Strong connectivity then supplies a
path from \(t\) to a suitable rare terminal \(c\).

Let \(h=(h_A,h_B,0)\) scalarize a two-active source-order chart and let
\(T_h(L)\) be the top block of one nonflat linkage \(L\).  The inherited
classifier declares \(L\) available in exactly one of the following three
ways.

### Q: quadratic active top

Choose \(q\in T_h(L)\) with two active particles.  Binaryity gives \(q_C=0\).
Since the top is proper, choose any \(c\in L\setminus T_h(L)\).  Then

\[
                       q_C=0\le c_C,
 \qquad h\cdot q>h\cdot c.                            \tag{3.1}
\]

### U: unary top

After the quadratic and one-active-particle-flat alternatives have failed,
the classifier finds a unary \(q\in T_h(L)\).  Again \(q_C=0\).  Any lower
\(c\in L\setminus T_h(L)\) satisfies (3.1).

### C: bounded-cofactor carrier

The remaining available alternative has a top mixed complex \(q\) which
contains \(C\), and a lower complex \(c\) in the same linkage which also
contains \(C\).  Hence

\[
                     1=q_C\le c_C\in\{1,2\},
 \qquad h\cdot q>h\cdot c.                            \tag{3.2}
\]

Now begin from any marked state \((x_n,t)\) with \(t\in L\).  Choose a
simple directed path from \(t\) to \(c\).  On designated success the endpoint
population telescopes to

\[
                         z_n=x_n-t+c\ge c.             \tag{3.3}
\]

Every prescribed source is the preceding actual target and is therefore
physical.  If the bounded-coordinate phase, source support, or active chart
changes along the path, the causing reaction is the declared structural
exit.  Otherwise \(C\) remains in its fixed finite chart box.  In Q and U,
\(q\) uses no \(C\); in C, (3.2)--(3.3) enable \(q\).  Bounded shifts of the
two divergent active populations do not change their strict source order,
so

\[
 {\lambda_c(z_n)\over\lambda_q(z_n)}
 ={K_c(z_n)_c\over K_q(z_n)_q}\longrightarrow0.
                                                               \tag{3.4}
\]

Therefore \(p_c(z_n)\to0\).  This proves the available-target hypothesis
for every actual target \(t\), without waiting for or conditioning on a
future activation.

As a diagnostic, the exact bridge was replayed on all 163,612 raw
both-available support--workload incidences and returned zero failures.  The
replay is not used in (3.1)--(3.4).

The previously suspicious C--C witness illustrates the repair.  For

\[
 L_1=\{0,C,A+C\},\quad L_2=\{2A,2C,B+C\},
 \quad h=(1,3,0),\quad C=0,                           \tag{3.5}
\]

the possible carried sources at that face are \(0\) and \(2A\).  The paths

\[
 0\to C\to A+C,
 \qquad 2A\to B+C\to2C                              \tag{3.6}
\]

start from those enabled marks.  At their endpoints, respectively \(B+C\)
and \(2A\) are enabled faster sources, so \(A+C\) and \(2C\) are rare.  Thus
this witness defeats a pre-activation enabled-top word, but not the marked
current-target theorem.

## 4. Bellman recursion and coercivity: pass

Condition on having followed the first \(i\) designated labels.  The
population \(x_{i,n}\) and mark \(y_i\) are then deterministic functions of
the episode start.  Let \(a_{i,n}\) be the probability of the next designated
label and \(D_{i,n}\) the expectation of the next **ordinary all-clock**
jump.  If a competitor fires, its reward is already part of \(D_{i,n}\) and
the episode stops.  If the designated label fires, the same jump is part of
\(D_{i,n}\) and only the future reward \(J_{i+1,n}\) remains.  Hence, exactly,

\[
 J_{m,n}=D_{m,n},
 \qquad J_{i,n}=D_{i,n}+a_{i,n}J_{i+1,n}.             \tag{4.1}
\]

This is not a conditioned-activation reward.  It is the elementary first-step
recursion of the unconditioned episode.

Extract a subsequence on which the finitely many source probabilities at the
designated success states converge, and let \(j\) be their first zero limit.
Such a \(j\) exists because the terminal \(c\) is rare.  For \(i<j\),
\(p_{y_i}\) has positive limit, and

\[
 a_{i,n}={\kappa_{i}\over K_{y_i}}p_{y_i}(x_{i,n})
                         \ge b_i>0.                   \tag{4.2}
\]

At \(j\), (2.3) gives \(D_{j,n}\to-\infty\).  If \(j=m\), this is the
terminal ordinary jump and there is no tail.  If \(j<m\), then
\(a_{j,n}\le C p_{y_j}(x_{j,n})\to0\).  Since every
\(D_{r,n}\le C_0:=\max\{C_K,0\}\), backward induction in (4.1) bounds the
positive tail after \(j\) by a fixed multiple of \(a_{j,n}\).  Iterating
(4.1) therefore
gives

\[
 J_{0,n}
 \le C+\left(\prod_{i<j}a_{i,n}\right)D_{j,n}
       +C'a_{j,n}\longrightarrow-\infty.             \tag{4.3}
\]

This proves the claimed coercivity no matter whether the rare probability
decays polynomially, logarithmically, or at an iterated-log scale.  The
negative term is \(\log p_{y_j}\); the proof never divides by \(p_{y_j}\).

If the deterministic designated prefix instead causes a structural exit,
then either an earlier source probability vanishes, giving (4.3), or every
label probability on the finite prefix has a positive lower bound.  In the
latter case the physical probability of the exit-causing prefix is bounded
below.  Thus the negative-reward/positive-exit dichotomy is exact.

Uniformity is a sequential-coercivity argument, not an unsupported compact
minimum.  If no finite exception and common margin existed in a fixed chart,
an escaping violating sequence would have a subsequence with fixed linkage,
mark, simple path, bounded-coordinate phase, and limiting finite source
probabilities.  Equations (4.2)--(4.3), or the exit-prefix alternative, give
a contradiction.  Finiteness of the target/path menu then makes the margin
uniform on the chart.

## 5. Moments, duration, and properness: pass

An episode contains at most ten ordinary jumps.  The positive part of its
total \(F\)-increment is bounded by the sum of the positive one-jump
increments.  Applying (1.6) at each success state therefore gives every
fixed positive endpoint-increment moment.

At every stage the current mark is an enabled source.  Its falling factorial
is a positive integer and at least one outgoing nonzero labelled rate is
positive.  Thus the total physical hazard is bounded below by one fixed
\(\kappa_*>0\).  Conditional exponential domination gives every fixed moment
of the sum of at most ten holding times.  No upper bound on a quadratic total
hazard is needed.

The endpoint differs from the start by at most ten bounded reaction vectors.
Moreover \(F\ge0\), the mark ranges over a finite binary set, and

\[
 |x|_1\to\infty\quad\Longrightarrow\quad
 \max_i(x_i-t_i)\to\infty\quad\Longrightarrow\quad F(x,t)\to\infty.
                                                               \tag{5.1}
\]

Hence \(W=1+F\) is nonnegative and proper on the marked state space.  From
\(\mathbb E\Delta W\le-2\) and
\(\sup\mathbb E\tau=C_\tau<\infty\), any
\(0<\eta\le C_\tau^{-1}\) gives target (4.4).  The positive endpoint
increment and duration are integrable.

## 6. Nonoverlap, trace mass, and the physical conclusion: pass

The deviation or final ordinary jump is the terminal jump of the current
episode.  Its actual target selects the next rule **after** that endpoint;
the jump is not counted again.  Thus every physical reaction belongs to
exactly one episode.  Since episode length lies between one and ten jumps,
reaction-count occupation and episode-start occupation are comparable up to
a fixed factor; a nonzero terminal Green trace cannot vanish under the
partition.

If both linkages are available, every actual target lies in one of them and
therefore starts a rule covered by Sections 3--5.  Positive exit-prefix mass
contradicts terminal-chart zero exit flux.  Otherwise the common proper
marked potential has the physical-time drift-cost estimate (4.4).  The
state-selected physical-time Foster lemma gives finite mean hitting of a
finite marked target when adjacent charts use this same \(W\).  Recording a
hit when it occurs, carrying the mark through one finite return cycle, and
projecting the finite cycle occupation measure yields an invariant
probability for the physical irreducible class.  The standard binary-network
linear-upward-rate argument supplies nonexplosion independently.

The conditional activation counterexample is inapplicable for an exact
reason: an activation/deviation jump is charged by (2.1) to the episode which
was already running from the preceding actual target.  Its resulting target
starts only the next episode.  No future reaction is conditioned upon.

## 7. Durable disposition

At SHA-256
`157e94cd035dec9a41947129dfcbbab0ebc6e72c01abde6bcf6626052954f1ed`,
the marked identity, Q/U/C availability bridge, unconditioned Bellman
recursion, rare-source coercivity, structural-exit alternative, uniform
finite menu, endpoint moments, physical duration, proper potential,
nonoverlap, and marked-to-physical conclusion all pass hostile replay.

**Final disposition: STRICT PASS for Theorem 5.1 at its stated scoped
both-available interface.**
