# Conditional classwise composition for one active linkage

**Proof-first composition, 2026-08-12 PDT.** This note joins the published
single-linkage and deficiency-zero theorems to the analytic small-support
and carrier theorems. It uses no orientation enumeration and no population
box search.

The separated input frozen during hostile audit at SHA-256
08c216dcf5926484e39edcab22df9ab119cd45f63f3f605154d6193a01c9f558.
That theorem failed at its asserted \(-\log A\) scale. The first proposed
log-gap repair in
*proof_first_single_linkage_08c_seam_audit_and_two_top_lemma.md* also
fails if it stops at the first cofactor-source entry: an entry of
probability \(e^{-h}\) can have raw endpoint cost \(\log A\), exceeding
\(h\) when \(h\) diverges slowly. The required input is a full all-clock
nested-carrier operator which pairs every new entry with its first exit
before charging a residual endpoint. A candidate of that exact form is
*proof_first_single_linkage_full_all_clock_nested_carrier.md*, frozen at
SHA-256
490f42487ec5045e17a7fa0dc1e69f61f836d17d0ee5ae3ce6af304fc7c230ac.
Every conclusion below is conditional on hostile validation of that
operator theorem. This note promotes no flag.

## 1. The theorem

> **Conditional Theorem 1.1.** Let every complex of a weakly reversible stochastic
> mass-action network have molecularity at most two. Fix a closed
> irreducible population class \(\Gamma\). Delete coordinates constant on
> \(\Gamma\), delete linkages with no enabled source there, and merge
> projected linkages sharing a projected complex. If the reduced network
> has at most three dynamic species and exactly one active linkage, then
> its CTMC is nonexplosive and positive recurrent on \(\Gamma\), for every
> strong orientation and every positive fixed rate vector, provided the
> nested-carrier and bounded-two-top stopped theorems cited above
> pass hostile replay on their final bytes.

An absorbing singleton is included. Constants may depend on the fixed
network, rates, and class.

## 2. Exact projection and nonexplosion

If \(X_i\equiv m_i\) on \(\Gamma\), closure forces every enabled reaction
to have zero \(i\)-increment. A directed return path in an active linkage
then shows that the coordinate is constant throughout that linkage; its
falling-factorial factor is absorbed into the rates. Projected linkages
sharing a complex have strongly connected union. Keeping parallel labelled
reactions reproduces the projected chain exactly.

A bimolecular-source reaction cannot increase total population. Therefore
the aggregate positive-jump rate satisfies

\[
                         q_+(x)\le C(1+|x|_1).                 \tag{2.1}
\]

Reaction vectors are bounded. A Yule comparison prevents population
explosion, and within a population sublevel finitely many states and
bounded rates prevent accumulation of population-neutral jumps.

## 3. Published branches

The Anderson--Cappelletti--Kim theorem applies literally when each dynamic
species \(S_i\) has \(S_i\) or \(2S_i\) in the one-linkage support. This
pure-multiple premise is not dropped.

A weakly reversible deficiency-zero network has the conditioned
product-Poisson invariant law on every closed class. Its normalizing
constant is finite, so an irreducible closed class is positive recurrent.

These branches require no stopped composition below.

## 4. Dimensions zero, one, and two

Zero dynamic species gives a singleton. With one dynamic species, every
nonconstant binary support contains its unary or binary pure complex, so
the published theorem applies.

For two dynamic species \(A,B\), suppose \(A,2A\) are absent. Since \(A\)
is dynamic,

\[
             {\cal C}=\{A+B\}\cup T,\qquad
             T\subseteq\{0,B,2B\}.                            \tag{4.1}
\]

At full rank, a support with at most three vertices has
\(\delta=m-1-2=0\). The unique residual support is

\[
                         \{0,B,2B,A+B\}.                       \tag{4.2}
\]

The all-clock theorem
*proof_first_single_linkage_2d_exception_service_theorem.md* gives, on its
missing-cofactor face,

\[
 \mathbb E_{(n,0)}
 [V(X_\tau)-V(n,0)+\tau]\le-\tfrac12\log n.                  \tag{4.3}
\]

Away from the face, the ordinary entropy generator descends. The theorem
has an independent mathematical PASS. This proves Theorem 1.1 in
dimensions at most two.

## 5. Enabled-top identity in dimension three

Let \(x_n\in\Gamma\) be a proper tier sequence, \(D^1\) its top
deterministic tier, and \(E\) its eventually enabled complexes. For enabled
\(y\),

\[
 {\lambda_y(x_n)\over(x_n\vee1)^y}
   \longrightarrow c_y\in(0,\infty),                          \tag{5.1}
\]

whereas a disabled source has zero propensity. Hence

\[
 T^{S,1}\subseteq D^1
 \quad\Longleftrightarrow\quad D^1\cap E\ne\varnothing.       \tag{5.2}
\]

If (5.2) holds, strong connectivity supplies a first exit from the enabled
top block, and the Anderson--Kim source/D-tier estimate gives ordinary
descent.

If it fails, every top-D complex is disabled. A disabled binary complex
with divergent monomial must be mixed, with one coordinate zero and one
divergent. This yields the following exhaustive alternatives.

## 6. Structural alternatives

If all three coordinates diverge, every source is enabled.

If only \(A\) diverges and the sole top is \(A+C\), then

\[
 {\cal C}\subseteq\{0,B,2B,C,2C,B+C,A+C\},                   \tag{6.1}
\]

with \(B^2=o(A)\) when \(2B\) is present and \(B=o(A)\) when
\(B\) or \(B+C\) is present. This is the separated trace.

If both \(A+B\) and \(A+C\) are top, then \(B=C=0\). The level

\[
                              H=A-B-C                          \tag{6.2}
\]

vanishes on \(0,A+B,A+C\). The first nonzero lower target lowers \(H\);
the bounded carrier trace has a geometric directed-cut inverse and
\(O(A^{-1})\) paid-source error. Without such a target, (6.2) is invariant;
without \(0\), the face is frozen.

If \(A,B\to\infty\) and \(C=0\), then

\[
             \varnothing\ne D^1\subseteq\{A+C,B+C\}.          \tag{6.3}
\]

A singleton top reduces to (6.1). If both tops tie, pure active complexes
would be enabled tops and active-only quadratics would dominate, so

\[
 \{A+C,B+C\}\subseteq{\cal C}
 \subseteq\{0,C,2C,A+C,B+C\}.                                \tag{6.4}
\]

Every full-rank four-complex support in (6.4) is deficiency zero. In
particular, \(\{0,C,A+C,B+C\}\) has three independent differences from
zero and \(\delta=4-1-3=0\). The sole full-rank non-deficiency-zero
balanced support is the full five-complex set, covered by Theorem 5.1 of
*proof_first_single_linkage_structural_reduction_and_mesoscopic_gap.md*.

These cases exhaust zero, one, two, or three divergent coordinates.

## 7. Corrected separated carrier input

Put

\[
 {\cal Z}=\{0,B,2B,A+C\},\quad
 {\cal P}=\{C,2C,B+C\},\quad H=A-C.                           \tag{7.1}
\]

Every \({\cal Z}\)-to-\({\cal Z}\) reaction has zero \(H\)-reward. The
clean process retains all such clocks, including nested openings, and kills
on a \({\cal P}\)-target. The physical process also retains each
\({\cal P}\)-sourced clock; its first firing is stopped and included.

For maximal pure spectator degree \(d\), the clean potential

\[
                              J=B+dC                           \tag{7.2}
\]

has an orientation-free maximal-source order: a dominant macro kills or
decreases \(J\), a positive move is lower by \(O(B^{-1})\), and exact
returns have bounded directed-cut inverse. The killed Green kernel has
polynomial moments and an \(\exp\{-c k\log k\}\) upcrossing tail.

The paid complexes \(C,2C,B+C\) have spectator degree at most one. Their
sourcewise race against \(A+C\) at level \(k\) is

\[
                              O((1+k)/A),                      \tag{7.3}
\]

and is absorbed in Green order by a clean reaction-specific service gap or
\(-\log(k+e)\) spectator decrement. Put

\[
 m(B)=
 \begin{cases}
  1+B^2,&2B\in{\cal C},\\
  1+B,&2B\notin{\cal C},\
       {\cal C}\cap\{B,B+C\}\ne\varnothing,\\
  1,&B,2B,B+C\notin{\cal C},
 \end{cases}
 \qquad h(A,B)=\log{A\over m(B)}.                              \tag{7.4}
\]

The tier premise is \(h(A,B)\to\infty\). For

\[
 G_\ell=K_\ell+\sum_i\log(X_i!)+\ell\cdot X\ge1,\qquad
 W_\ell=G_\ell^4,                                             \tag{7.5}
\]

the candidate all-clock nested-carrier theorem gives, conditional on its
operator replay, an included physical
stopping time
with

\[
 \mathbb E_x[
 W_\ell(X_\tau)-W_\ell(x)+\tau]
       \le-cG_\ell(x)^3h(A,B).                                \tag{7.6}
\]

Moving localization is a terminal, already-paid endpoint. The global
router starts a fresh separated episode at a cofactor-free separated
endpoint, uses the ordinary generator chart at an open endpoint, and uses
the enabled-top or balanced chart only when that scale is actually reached.
The same \(W_\ell\) is used throughout.

The two-disabled-top case is not discharged by a paragraph: Theorem 3.1 of
the repair note supplies a geometric bounded-carrier kernel,
included \(O(A^{-1})\) competitors, duration moments, and
\(-cG_\ell^3\log A\) drift. Its invariant and frozen alternatives are
classwise exact.

## 8. Uniform chart cover

The balanced and separated episodes use the common potential (7.4). At an
ordinary enabled-top state, the factorial finite-difference expansion gives
along every divergent ordinary tier sequence

\[
                           {\cal L}W_\ell(x_n)\to-\infty.       \tag{8.1}
\]

The leading term is \(4G_\ell^3{\cal L}G_\ell\); bounded reaction jumps
make higher Taylor terms lower order on the dominant source scale.

Conditionally on the nested-carrier input and the bounded two-top
lemma, an exceptional sequence gives

\[
 \mathbb E_x[
 W_\ell(X_{\tau_x})-W_\ell(x)+\eta\tau_x]\le-\delta.          \tag{8.2}
\]

The causing reaction is included and the next chart is chosen only from
the actual endpoint, so reclassification has no toll.

If these regions failed to cover the complement of a finite subset of
\(\Gamma\), an uncovered divergent sequence would have a proper tier
subsequence with fixed availability and tier data. Sections 5--7 would put
it in an ordinary, balanced, separated, invariant, or frozen alternative,
a contradiction. Finitely many relabellings give common
\(\eta,\delta>0\) outside a finite target \(K\).

## 9. Fixed-class random-time Foster lemma

> **Lemma 9.1.** Let a nonexplosive irreducible countable-state CTMC have
> a proper \(W\ge1\). Suppose a finite set \(K\), a generator-good set,
> and finitely many episode sets cover its complement. Assume
> \({\cal L}W\le-\eta\) on the generator-good set. At every episode state
> assume an all-reaction stopping time \(\sigma>0\), with causing reaction
> included, satisfies
> \[
> \mathbb E_x[
> W(X_\sigma)-W(x)+\eta\sigma]\le-\delta,                     \tag{9.1}
> \]
> with endpoint and duration integrability sufficient to remove
> localization. Then \(\mathbb E_xT_K<\infty\) for every \(x\), and the
> chain is positive recurrent.

#### Proof

From a generator-good point, run until \(K\) or an episode set; stopped
Dynkin pays \(W\)-change plus \(\eta\) times physical duration. At an
episode point append (9.1). Choose the next rule after seeing the actual
endpoint. If \(K\) is visited inside an episode, record the hit and let the
episode finish only for drift accounting.

At completed macroepisode times \(S_r\), conditional expectation gives

\[
 \delta\,\mathbb E(r\wedge N_K)
 +\eta\,\mathbb E S_{r\wedge N_K}
       \le W(x)+\delta.                                      \tag{9.2}
\]

Nonexplosion excludes infinitely many positive-length episodes in finite
time. Monotone convergence yields \(\mathbb E_xT_K<\infty\).

If the class is not a singleton, take one ordinary jump from \(K\) and
apply the hitting bound to its successor. Finitely many states and reaction
successors give uniformly finite mean positive return to \(K\). The return
trace is finite; one recurrent trace state has finite mean physical return.
Irreducibility makes every state positive recurrent. \(\square\)

## 10. Conditional proof and strict status

Sections 2--4 prove nonexplosion and dimensions at most two. In dimension
three, Sections 5--7 exhaust every proper tier subsequence analytically.
Section 8 supplies the uniform finite chart cover, and Lemma 9.1 proves
positive recurrence. This proves Conditional Theorem 1.1 once the local
inputs pass. \(\square\)

This is a conditional composition theorem, not an audit certificate. The
two-species exception has a mathematical PASS and the balanced theorem has
independent replays recorded in its log. The frozen separated theorem
strictly fails at the wrong entropy scale, and the first stop-at-entry
log-gap repair also fails. The full all-clock nested-carrier candidate at
the SHA above and the expanded two-top lemma remain to be replayed. No certification flag is
changed and no finite computation is used.
