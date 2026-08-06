# Uniform finite-family random-time Foster theorem

## 1. Augmented embedded chain

Discard zero-vector reactions, which do not produce jumps.  If the complex
graph has one vertex, or if a closed class is finite, positive recurrence is
immediate.  Otherwise every complex has at least one nontrivial outgoing
edge.

For an infinite closed irreducible population class \(\Gamma\), define the
reachable augmented state space

\[
\widetilde\Gamma=
\{(x,t):\text{the population }x\in\Gamma\text{ was reached by a reaction
whose target is }t\}.
\]

From \((x,t)\), a reaction \(s\to u\) gives

\[
(x,t)\longmapsto(x-s+u,u)
\]

with the ordinary embedded-jump probability.  The transition law depends on
\(x\), not on the historical label \(t\), so this is a Markov chain.

The augmented chain is irreducible.  Given two reachable pairs, choose a
predecessor population and final reaction realizing the second pair.
Population irreducibility reaches that predecessor; firing the final
reaction reaches the requested target label.

## 2. Common proper potential

Use

\[
V(x,t)=\sum_i\log((x_i-t_i)!).
\]

Since \(|t|\le2\) and \(\log n!\to\infty\), every sublevel set of \(V\) in
\(\widetilde\Gamma\) is finite.  Thus \(V\) is one common proper potential
for every episode template and every population hierarchy.

For each terminal complex \(c\), let \(D_c(x,t)\) be the expected change of
\(V\) over the finite \(t\)-to-\(c\) target-following episode described in
`complete_credit_elimination.md`.

## 3. Sequence-to-uniform lemma

Define

\[
K=\left\{(x,t)\in\widetilde\Gamma:
       \min_{c\in\mathcal C}D_c(x,t)>-1\right\}.
\]

### Lemma

\(K\) is finite.

### Proof

Suppose \(K\) were infinite.  Properness of \(V\) supplies a divergent
sequence in \(K\).  Pass to the coordinatewise constant-or-divergent and
normalized-log subsequence of `source_rate_flag_theorem.md`.

The top availability theorem gives either:

1. an exact species-linear conservation law whose value diverges along the
   fixed communicating class, a contradiction; or
2. a terminal complex \(c\) and an enabled source \(s\) with strictly larger
   normalized-log weight.

In the second case

\[
p_{r^{(n)}+c}(c)\to0.
\]

Complete-credit elimination then gives

\[
D_c(x^{(n)},t)\to-\infty,
\]

contradicting the definition of \(K\).  Therefore \(K\) is finite. \(\square\)

This is the exact sequence-to-uniform bridge.  The compact quantities are:

- the normalized logarithmic vector \(w\) in a simplex;
- the finite carried target;
- the finite divergent-coordinate set;
- the finite top-complex set.

The strict margin survives because the final statement is not merely a
limiting sign: terminal source probability tends to zero, and the finite
scalar elimination bound tends to minus infinity.

## 4. Deterministic episode selector

Outside \(K\), choose before the episode starts the lexicographically first
terminal complex minimizing \(D_c(x,t)\).  This is a deterministic measurable
function on the countable augmented state space.  It is not chosen according
to the realized outcome.

Let \(\tau(x,t)\) be the resulting episode length in embedded jumps.  Then

\[
1\le\tau(x,t)\le L:=|\mathcal C|
\]

and

\[
\mathbb E_{(x,t)}
  [V(Z_{\tau})-V(x,t)]\le-1,
\qquad (x,t)\notin K.
\]

Inside \(K\), define the next episode to be one ordinary jump.

## 5. Finite expected hitting time of K

Let \(Y_0=z\) and let \(Y_{n+1}\) be the endpoint of the episode selected at
\(Y_n\).  Put

\[
\sigma_K=\inf\{n\ge0:Y_n\in K\}.
\]

For every bounded stopping index \(N\), conditional expectation and the
episode drift give

\[
\mathbb E_z V(Y_{N\wedge\sigma_K})
 +\mathbb E_z(N\wedge\sigma_K)
 \le V(z).
\]

No unbounded optional-stopping theorem is used; this is obtained by summing
one-step conditional inequalities up to the bounded index.  Since \(V\ge0\),
monotone convergence yields

\[
\mathbb E_z\sigma_K\le V(z).
\]

The original augmented embedded chain reaches \(K\) in at most
\(L\sigma_K\) jumps.  Therefore

\[
\mathbb E_z T_K\le L V(z)<\infty.
\]

## 6. From a finite set to one recurrent state

The following steps avoid the common but incomplete assertion that a finite
set alone proves positive recurrence.

1. For \(k\in K\), take one ordinary jump.  There are finitely many possible
   successors, and each successor has finite expected hitting time of \(K\).
   Hence the next return time \(T_K^+\) has finite expectation from every
   \(k\in K\).

2. Record successive visits of the augmented embedded chain to \(K\).  This
   trace chain is irreducible: an augmented path between any two points of
   \(K\), with its intermediate \(K\)-visits recorded, gives a positive trace
   path.

3. Fix \(k_*\in K\).  Because the trace chain is finite and irreducible,
   there are integers \(m\) and \(\epsilon>0\) such that, from every trace
   state, \(k_*\) is reached within \(m\) trace transitions with probability
   at least \(\epsilon\).  Geometric blocking gives a finite expected number
   of trace transitions to \(k_*\), and also a finite expected trace-return
   time from \(k_*\).

4. Let
   \[
   B=\max_{k\in K}\mathbb E_k T_K^+<\infty.
   \]
   Strong Markov conditioning bounds the expected number of original jumps
   spent in any collection of trace excursions by \(B\) times the expected
   number of excursions.

5. Therefore the augmented embedded chain has finite expected return time to
   \(k_*\).

The projected population embedded chain returns to the population coordinate
of \(k_*\) no later than the augmented return, so it too has finite expected
return time.

## 7. Conversion to continuous physical time

Let

\[
\kappa_*=
\min\{\kappa_{y u}:y\ne u\}>0.
\]

At every state of an infinite irreducible class, at least one nontrivial
reaction is enabled.  Its falling-factorial factor is a positive integer and
therefore at least one.  Hence the total CTMC jump rate is at least
\(\kappa_*\), and the conditional mean holding time is at most
\(1/\kappa_*\).

If \(N\) is the embedded-jump return time to the selected population state,
Tonelli's theorem gives

\[
\mathbb E\left[\sum_{j=0}^{N-1}H_j\right]
 =\mathbb E\left[\sum_{j\ge0}
   \mathbf1_{\{j<N\}}\frac1{\Lambda(X_j)}\right]
 \le\frac{\mathbb E N}{\kappa_*}<\infty.
\]

The inherited nonexplosion theorem excludes accumulation of jump times.
Thus the original CTMC has finite expected return time to one—and hence
every—state of \(\Gamma\).  The class is positive recurrent.
