# Quadratic return-trace Foster bridge

## 1. Scope

This note records an abstract physical-time bridge for the remaining
one-active shell calculation.  It is deliberately independent of any
particular support pair.  It does **not** certify the fifteen critical pairs
or T3-2.  Its purpose is to isolate exactly what a support-specific return
calculation must prove.

The bridge avoids both invalid interfaces from the inherited manuscript:

1. no tight coordinate is replaced by a fixed finite phase; and
2. no count of fast embedded jumps is used.

Instead one traces the original CTMC at returns to a genuine population
cross-section and keeps the full physical duration of each excursion.

## 2. Return-trace theorem

Let \(X\) be a nonexplosive CTMC on a countable closed irreducible class
\(\Gamma\).  Let

\[
 \mathcal B=\{b_{n,e}:n\in\mathbb N_0,\ e\in E_n\}\subset\Gamma,
 \qquad \sup_n |E_n|<\infty,
\tag{2.1}
\]

be a population cross-section with finite level sets.  Write
\(\tau^+_{\mathcal B}\) for the first positive return to \(\mathcal B\),
and let \((N_1,E_1)\) be the level and mark at that return.

> **Theorem 2.1 (physical return-trace Foster criterion).**  Suppose:
>
> 1. from every state of \(\Gamma\), \(\mathcal B\) is hit in finite mean
>    physical time;
> 2. for every \(b_{n,e}\),
>    \(\mathbb E_{b_{n,e}}\tau^+_{\mathcal B}<\infty\), and in fact
>    \[
>      \sup_{n,e}\mathbb E_{b_{n,e}}\tau^+_{\mathcal B}<\infty;
>    \tag{2.2}
>    \]
> 3. the return kernel has integrable quadratic increments and, for some
>    \(n_0<\infty\) and \(\varepsilon>0\),
>    \[
>      \mathbb E_{b_{n,e}}[N_1^2-n^2]\le-\varepsilon,
>      \qquad n\ge n_0, e\in E_n.
>    \tag{2.3}
>    \]
>
> Then \(X\) is positive recurrent on \(\Gamma\).

### Proof

The successive returns to \(\mathcal B\) form a countable-state Markov
chain with proper Lyapunov function \(W(n,e)=n^2\): properness follows from
the uniform bound on \(|E_n|\).  Equation (2.3) and the ordinary discrete
Foster theorem make every closed class of the return chain positive
recurrent and give finite mean hit of the finite set
\(\{b_{n,e}:n<n_0\}\).  Assumption 1 and irreducibility of \(\Gamma\)
select the return class belonging to \(\Gamma\).

Let \(\widehat\pi\) be its invariant probability.  The standard cycle
occupation measure

\[
 \nu(A)=\sum_{b\in\mathcal B}\widehat\pi(b)
  \mathbb E_b\int_0^{\tau^+_{\mathcal B}}
  \mathbf 1_{\{X_t\in A\}}\,dt
\tag{2.4}
\]

is invariant for the original CTMC.  Its total mass is at most the uniform
bound in (2.2), and it is positive.  Normalizing \(\nu\) therefore gives an
invariant probability on \(\Gamma\).  Irreducibility and nonexplosion imply
positive recurrence.  \(\square\)

The uniform duration bound in (2.2) is stronger than strictly necessary,
but it is the clean condition delivered by the intended fast-shell return.
It also prevents the endpoint-only lexicographic failure recorded in the
release regressions.

There is a complementary version for reflected-debt episodes which obtain
almost-sure level descent but whose physical duration may grow with the
level.

> **Theorem 2.2 (shell-adapted return trace).**  Keep the cross-section
> (2.1), and suppose
> that from every \(b_{n,e}\) with \(n>n_0\) there is a physical stopping
> time \(\sigma_{n,e}\) ending in \(\mathcal B\) such that
> \[
>    N(X_{\sigma_{n,e}})\le n-1\quad\hbox{a.s.},
>    \qquad \mathbb E_{b_{n,e}}\sigma_{n,e}<\infty .
> \tag{2.5}
> \]
> Finite level sets make the nondecreasing numbers
> \[
>  c(n)=1+\max\!\left(
>    \{0\}\cup
>    \{\mathbb E_{b_{k,e}}\sigma_{k,e}:
>       n_0<k\le n,\ e\in E_k\}\right)
>  <\infty
> \tag{2.6}
> \]
> well defined, including when some \(E_k\) is empty.  Put
> \(U(n,e)=\sum_{j\le n}c(j)\).  Assume in addition that from every state
> \(x\in\Gamma\) there is a physical access stop \(\rho_x\) ending in
> \(\mathcal B\) such that
> \[
>  \mathbb E_x\!\left[
>    \rho_x+U(N(X_{\rho_x}),E(X_{\rho_x}))\right]<\infty.
> \tag{2.7}
> \]
> Then the original CTMC is positive recurrent.

Indeed, for every endpoint level \(m\le n-1\), monotonicity of \(c\) gives
\(U(m)-U(n)\le-c(n)\), while
\(\mathbb E\sigma_{n,e}\le c(n)-1\).  Thus
\(\mathbb E[\Delta U+\sigma_{n,e}]\le-1\) on the return trace.

On the return trace, \(U\) pays both one strict level descent and the
duration of the corresponding physical episode.  Telescoping gives a
finite mean hit of the finite trace set \(\{n\le n_0\}\); (2.7) pays for
the initial access and for every off-cross-section continuation.  The
ordinary finite-set trace argument in the original CTMC then proves
positive recurrence.  Notice
that properness is required only on the genuine return cross-section; an
unbounded artificial debt coordinate between returns is not silently
discarded.

## 3. The rare one-step shell corollary

The critical shell calculation naturally gives a level increment
\(\Delta_n=N_1-n\) rather than (2.3) directly.

> **Corollary 3.1 (quadratic amplification).**  Suppose, uniformly in the
> finite mark \(e\),
> \[
>   \mathbb E\Delta_n=-{a_e\over n}+O(n^{-2}),
>   \qquad
>   \mathbb E\Delta_n^2={b_e\over n}+O(n^{-2}),
> \tag{3.1}
> \]
> where \(\inf_e a_e>0\) and \(\sup_e b_e<\infty\), and suppose the
> contribution of jumps larger than a fixed constant is uniformly
> integrable at the same order.  Then
> \[
>   \mathbb E[(n+\Delta_n)^2-n^2]
>   =-2a_e+O(n^{-1}),
> \tag{3.2}
> \]
> so (2.3) holds for all sufficiently large \(n\).

Indeed, expand the square.  Notice that no comparison between \(a_e\) and
\(b_e/2\) is needed here because the physical return event itself has
probability of order \(n^{-1}\).  The variance term in (3.1) is therefore
only order \(n^{-1}\), whereas multiplication of the mean by \(2n\)
produces the nonzero constant in (3.2).

For the mixed shell \(\{0,A+C,B+C\}\), the proposed cross-section is

\[
 \mathcal B=\{(A,B,C)=(0,0,n):n\ge n_0\},
 \qquad Q=C-A-B=n.
\tag{3.3}
\]

A support-specific proof must establish, for the **full** two-linkage CTMC,

\[
 \mathbb E\Delta Q=-{a\over Q}+O(Q^{-2}),
 \qquad
 \mathbb E(\Delta Q)^2=O(Q^{-1}),
 \qquad a>0,
\tag{3.4}
\]

at the first physical return to (3.3), together with (2.2).  The exact
conditional product form on a fixed \(Q\)-shell identifies the coefficient
and sign, but stationary averaging alone is not enough: (3.4) must be
proved from the actual base state, with lower-reaction interruptions and
rare promotion excursions retained.

## 4. A sufficient tube-to-cross-section interface

The remaining global obligation can be checked without asserting that a
tight environment has finite support.  It is enough to produce a proper
function \(F\), a finite-width **generator-bad** tube \(\mathcal T\), and
stopping rules with the following properties:

1. \(\mathcal L F\le-1\) outside \(\mathcal T\) and a finite set;
2. from every point of \(\mathcal T\), the chain either hits
   \(\mathcal B\) or exits \(\mathcal T\) in uniformly integrable time;
3. after a tube exit, stopped Dynkin estimates for a sufficiently high
   power of \(1+F\) control the quadratic level cost on return;
4. from \(b_{n,e}\), the probability of reaching the tube boundary before
   the ordinary fast return is sufficiently small that the exceptional
   duration and quadratic endpoint costs are uniformly summable.

Here the tube is not obtained from tightness.  It is obtained by the
bad-sequence contradiction: if no finite width contained the states with
\(\mathcal L F>-1\), a divergent sequence with another unbounded coordinate
would realize a higher-dimensional descriptor, where the certified
generator theorem supplies strict descent.  Physical reactions are retained
on tube exit, and the exit is charged by items 3--4 rather than mislabeled as
an exact finite phase.

These four conditions imply assumptions 1--2 of Theorem 2.1 by alternating
localized \(F\)-descent outside the tube with the physical tube episode.
They are the precise endpoint seam that must accompany (3.4) before any
pair count is promoted.

## 5. Claim discipline

Theorem 2.1 is an abstract Markov-chain statement.  Equations (3.3)--(3.4)
and the four tube conditions are a proof checklist, not a certified CRN
theorem.  In particular, this note does not infer:

- a finite inactive phase from tightness;
- a killed-resolvent estimate from a stationary average;
- uniform return cost from a local drift sign; or
- recurrence from separate unglued Lyapunov functions.
