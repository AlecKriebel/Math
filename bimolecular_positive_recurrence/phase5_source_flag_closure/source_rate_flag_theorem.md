# Normalized-log compactification and the top availability theorem

The final proof does not need to name or patch every population tier.  A
single compact normalized-log direction contains the complete finite flag.

## 1. Subsequence compactification

Let \((x^{(n)},t^{(n)})\) be a divergent sequence of reachable augmented
states in one fixed closed communicating class.  After passing to a
subsequence, the finite carried target is constant, say \(t\).  Put
\(r^{(n)}=x^{(n)}-t\).

A diagonal subsequence makes every coordinate either:

- constant in \(n\); or
- divergent to infinity.

Let \(I\) be the set of divergent coordinates and \(J=I^c\).  Define

\[
R_n=\sum_{i\in I}\log(r_i^{(n)}+1)
\]

and pass to a further subsequence so that

\[
w_i=\lim_{n\to\infty}
\frac{\log(r_i^{(n)}+1)}{R_n}
\]

exists for every \(i\in I\); put \(w_i=0\) on \(J\).  Then

\[
w\ge0,\qquad \sum_iw_i=1.
\]

Species in \(I\) may have \(w_i=0\).  Such species represent every slower
subtier at once; none is replaced by a bounded defect.

For a complex \(y\), put \(h(y)=w\cdot y\), let

\[
a=\max_{y\in\mathcal C}h(y),
\qquad
T=\{y:h(y)=a\}.
\]

## 2. Top availability or exact conservation

Exactly one of the following gives a contradiction or a useful terminal
complex.

### All complexes are top

If \(T=\mathcal C\), then

\[
w\cdot(y'-y)=0
\]

for every reaction.  Hence \(w\cdot X\) is an exact nonnegative
conservation law.  At least one positive-weight coordinate diverges, so
\(w\cdot x^{(n)}\to\infty\), impossible in one communicating class.

### A top complex contains two divergent particles

If some \(s\in T\) has \(q_I(s)=2\), bimolecularity implies that \(s\) uses
only divergent coordinates.  It is therefore enabled at \(r^{(n)}+c\) for
every lower complex \(c\notin T\), for all sufficiently large \(n\).

### Every top complex contains one divergent particle

Assume no top complex has \(q_I=2\).  Every top complex has \(q_I=1\).  Let
\(K\) be the set of divergent species appearing in top complexes.  Every
\(i\in K\) has \(w_i=a\), no complex contains two \(K\)-particles, and

\[
y\in T\quad\Longleftrightarrow\quad q_K(y)=1.
\]

If every complex has \(q_K=1\), then \(M_K=\sum_{i\in K}X_i\) is exactly
conserved, contradicting divergence.

Otherwise choose a lower complex with \(q_K=0\).

- If a unary top complex \(K_i\) exists, it is enabled over every lower
  terminal complex.
- Otherwise every top complex is \(K_i+D\), where \(D\in J\) is a bounded
  service species.  If a lower complex \(c\) contains one such \(D\), then
  the associated source \(K_i+D\) is enabled at \(r^{(n)}+c\).
- If no lower complex contains any service species, then

  \[
  M_K-\sum_{D\text{ service}}X_D
  \]

  is constant on every complex and hence is an exact reaction-wise
  conservation law.  Its positive part diverges while every negative
  coordinate is fixed, again impossible in the fixed class.

Therefore every nonconservative divergent sequence supplies complexes
\(s,c\) such that

\[
h(s)>h(c)
\]

and \(s\) is enabled at \(r^{(n)}+c\) for all large \(n\).

## 3. Terminal source probability tends to zero

For every enabled fixed complex \(y\),

\[
\frac{1}{R_n}\log (r^{(n)}+c)_y\longrightarrow h(y).
\]

The bounded coordinates contribute only constants, and zero-weight
divergent coordinates contribute \(o(R_n)\).  Thus

\[
\frac{(r^{(n)}+c)_s}{(r^{(n)}+c)_c}
\longrightarrow\infty.
\]

With \(\bar\kappa_y\) the aggregate outgoing rate,

\[
p_{r^{(n)}+c}(c)
\le
\frac{\bar\kappa_c(r^{(n)}+c)_c}
     {\bar\kappa_s(r^{(n)}+c)_s}
\longrightarrow0.
\]

The complete-credit lemma then makes the expected drift of the
\(t\)-to-\(c\) episode tend to \(-\infty\).

## 4. Finiteness of flag types

The discrete data are finite: the carried target, the divergent-coordinate
set \(I\), the top complex set \(T\), and the applicable availability or
conservation alternative.  The vector \(w\) ranges over a compact simplex,
but no continuum of episode templates is introduced: the terminal episode
is indexed only by \(c\in\mathcal C\).  The compact vector is used solely in
a contradiction argument proving that the common finite family is uniform
outside a finite set.
