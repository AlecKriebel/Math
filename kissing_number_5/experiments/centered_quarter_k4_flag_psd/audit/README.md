# Independent audit of the ordered-edge flag relaxation

## Result

The ordered-edge normalization in the parent experiment is correct.  More
importantly, the proposed obstruction does **not** survive all pointwise
identities coming from centering.  There is an exact positive rational
quarter-grid K2/K3/K4 pseudodistribution for \(N=41\) satisfying

- the K3-to-K2 and K4-to-K3 marginals;
- the centered vertex-flag moment matrix and both of its forced kernels;
- all ordered K2-to-K3 pointwise centering identities;
- all 609 ordered K3-to-K4 pointwise centering identities (116 distinct
  rows after exact relabeling deduplication);
- every ordered-edge covariance PSD block; and
- every forced ordered-edge Schur-block kernel.

The exact verifier proves positive definiteness after quotienting by the
forced kernels, using rational LDL decompositions.  Thus this is not merely
a solver-tolerance observation.

This is a barrier result, not a spherical code.  The witness is supported on
the seven-point quarter grid and is only locally consistent through K4.  It
does not give 41 vectors, global exchangeability, K5 consistency, or a value
of \(\tau(5)\).

## Normalizations from first principles

For a genuine centered \(N\)-point code, put

\[
 \alpha_q={1\over N}\#\{(i,j):i\ne j,\ \langle x_i,x_j\rangle=q\}.
\]

Thus \(\sum_q\alpha_q=N-1\).  Let \(\nu_T\) be the number of ordered
distinct triples, divided by \(N\), whose three sorted edge colors form
\(T\).  If \(\mu_H\) is the probability that a uniformly random unordered
four-set has K4 orbit \(H\), then

\[
 \operatorname{marg}_2(\nu)=(N-2)\alpha,\qquad
 \operatorname{marg}_3(\mu)={4\nu\over (N-1)(N-2)}.
\]

Fix an **ordered** base edge \((i,j)\) of color \(q\), and define

\[
 z_{ab}(i,j)=\#\{k\notin\{i,j\}:
    \langle x_i,x_k\rangle=a,\
    \langle x_j,x_k\rangle=b\}.
\]

Then

\[
 M_q={1\over N}\sum_{\substack{i\ne j\\q_{ij}=q}}
 \binom{z(i,j)}1\binom{z(i,j)}1^{\!T}\succeq0.
\]

Its lower-right entry is \(\alpha_q\), its off-diagonal vector is the
oriented K3 incidence, and its upper-left block is

\[
 \operatorname{diag}(\ell_q)
 +{\binom N4\over N}\sum_H\mu_H F_q(H).
\]

Here \(F_q(H)\) counts an ordered base edge and an ordered pair of distinct
extensions inside the unordered K4.  Each ordered quadruple is counted
exactly once, which explains the factor \(\binom N4/N\).

For an **unordered** base edge, the lower-right entry is instead
\(\alpha_q/2\), and the profile is the unordered pair \(\{a,b\}\).  Losing
the endpoint orientation also merges the two endpoint-centering identities.
Consequently the ordered block has three forced kernel vectors,

\[
 (\mathbf1,-(N-2)),\quad (a,1+q),\quad (b,1+q),
\]

while the unordered block has only

\[
 (\mathbf1,-(N-2)),\quad (a+b,2(1+q)).
\]

`normalization_audit.py` reconstructs both moment conventions two different
ways on the exact 40-point D5 code and obtains literal rational equality.
It also checks every one of the 59,280 ordered D5 triples against the
pointwise centering identity.

## Full pointwise-centering hierarchy

If \(d_a(i)\) is the number of neighbors of color \(a\) at vertex \(i\),
then centering gives

\[
 \sum_a d_a(i)=N-1,\qquad \sum_a a\,d_a(i)=-1.
\]

The corresponding vertex moment block therefore has the two kernels
\((\mathbf1,-(N-1))\) and \((a,1)\).

For every ordered base edge,

\[
 \sum_{a,b}z_{ab}=N-2,\quad
 \sum_{a,b}a z_{ab}=-1-q,\quad
 \sum_{a,b}b z_{ab}=-1-q.
\]

Multiplication by every component of \(z\) gives the full Schur-block kernel
equations.  Finally, for every ordered triple \((i,j,k)\),

\[
 \sum_{\ell\notin\{i,j,k\}}\langle x_i,x_\ell\rangle
 =-1-\langle x_i,x_j\rangle-\langle x_i,x_k\rangle,
\]

and likewise at \(j\) and \(k\).  These K3-to-K4 identities imply the top
rows of the edge-block kernel equations; the K2-to-K3 equations imply their
bottom rows.  The verifier nevertheless evaluates every kernel directly.

## Reproduction

From the repository root:

```text
PYTHONPATH=. .venv/bin/python experiments/centered_quarter_k4_flag_psd/audit/normalization_audit.py
PYTHONPATH=. .venv/bin/python experiments/centered_quarter_k4_flag_psd/audit/search_full_centering.py --level full --solver CLARABEL
PYTHONPATH=. .venv/bin/python experiments/centered_quarter_k4_flag_psd/audit/rationalize_full_witness.py
PYTHONPATH=. .venv/bin/python experiments/centered_quarter_k4_flag_psd/audit/verify_full_exact_witness.py
```

The numerical search used Python 3.14.6, NumPy 2.5.1, SciPy 1.18.0,
CVXPY 1.9.2, and Clarabel 0.11.1.  Rationalization used PARI/GP 2.17.4.
The last verifier uses exact `Fraction` arithmetic and does not trust the
solver status.

Expected SHA-256 digests:

```text
07e3908d94a43613391ca58867aa5bfd13c119414a94d333a3455d0292423448  results/d5_normalization_audit.json
66c8abca40f3f62937fd44220828f23617bc974f6dc295e45050063c9a5acf23  results/full_clarabel.json
30789a5ce7e4d5a9d4779cc0faac7cf05aeff5b90e525c8722e0f5356aa87198  results/full_exact_linear_witness.json
c820b8a84a203ef989b26bd60c90045a39fd4d42a491d96ba5b9200e309eabca  results/full_exact_verification.json
```
