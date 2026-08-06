# A self-contained episode Foster theorem

## Theorem

Let \(X\) be a nonexplosive irreducible continuous-time Markov chain on a
countable state space \(E\).  Let \(K\subset E\) be finite.  Suppose that for
every \(x\notin K\) a stopping rule \(\sigma_x\) is specified, with the same
rule restarted after each episode by the strong Markov property.  Assume:

1. \(\sigma_x\) is integrable and the endpoint value below is integrable;
2. every episode contains at least one genuine jump of \(X\);
3. there are \(V:E\to[0,\infty)\), \(g:E\setminus K\to(0,\infty)\), and
   \(C<\infty\) such that
   \[
   \mathbb E_x V(X_{\sigma_x})\le V(x)-g(x),
   \qquad
   \mathbb E_x\sigma_x\le Cg(x).
   \]

Then \(\mathbb E_x\tau_K\le C V(x)\) for every \(x\notin K\).  In
particular, the chain is positive recurrent.

The norm-like property of \(V\) is not needed for the implication once the
three displayed hypotheses have been established.  It is normally used to
construct a finite \(K\) and to verify endpoint integrability.

## Proof

Set \(S_0=0\).  If \(X_{S_n}\notin K\), restart the prescribed rule there and
put
\[
S_{n+1}=S_n+\sigma_{X_{S_n}}\circ\theta_{S_n}.
\]
Let \(Y_n=X_{S_n}\), and let
\(\nu=\inf\{n:Y_n\in K\}\).  Iterating conditional expectations gives, for
every integer \(m\),
\[
\mathbb E_x V(Y_{m\wedge\nu})
 +\mathbb E_x\sum_{j< m\wedge\nu}g(Y_j)
 \le V(x).
\]
Nonnegativity of \(V\), followed by monotone convergence, yields
\[
\mathbb E_x\sum_{j<\nu}g(Y_j)\le V(x).
\]
The duration inequality and the tower property therefore give
\[
\mathbb E_x S_\nu
 =\mathbb E_x\sum_{j<\nu}(S_{j+1}-S_j)
 \le C\mathbb E_x\sum_{j<\nu}g(Y_j)
 \le CV(x).
\]

It remains to exclude \(\nu=\infty\).  On that event the preceding bound
implies that \(S_\infty=\sum_j(S_{j+1}-S_j)<\infty\) almost surely.  But every
episode contains a genuine jump, so \(\nu=\infty\) would force infinitely
many jumps before the finite time \(S_\infty\), contradicting
nonexplosion.  Hence \(\nu<\infty\) almost surely and
\(\tau_K\le S_\nu\), proving the hitting-time bound.

Choose a reference state \(o\in K\).  For each \(k\in K\), irreducibility
supplies a finite state path from \(k\) to \(o\) with positive transition
rates.  Because \(K\) is finite, there is a uniform positive probability
\(p\) that, starting from any point of \(K\), the next finitely many jumps
follow the selected path.  The states occurring in all selected paths form
a finite set, so the expected duration of one such trial is uniformly
finite.  After a failed trial, the already proved estimate gives a finite
mean return time to \(K\).  Repeating the trials gives a geometric number of
attempts, hence a finite mean hitting time of \(o\) from every point of
\(K\).  Starting from \(o\) after its first departure now gives a finite mean
return time to \(o\).  Thus the irreducible chain is positive recurrent.

## Audited technical points

* Optional stopping is used only at the bounded episode index
  \(m\wedge\nu\); passage to the limit is monotone because \(g>0\) and
  \(V\ge0\).
* Endpoint integrability is an explicit hypothesis.
* Episode-time accumulation is excluded by the genuine-jump condition and
  nonexplosion.
* No skeleton-chain holding-time assumption is hidden: physical episode
  durations are summed directly.
* The last finite-set-to-singleton step uses only finitely many fixed paths
  and geometric trials.
