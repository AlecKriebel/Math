# A claim-neutral no-promotion selector inside the prospective 795

## 1. Scope

This note freezes a finite selector only.  It assumes prospectively that
the candidate 1,227-pair one-active branch is eventually certified, and it
then works inside the resulting exact 795-pair remainder.  It does **not**
assert that this prospective promotion has occurred.

The selector consists of the pairs \(P\) for which

1. the active-coordinate counts of the affine-feasible failed descriptors
   are exactly \(\{1,3\}\);
2. the whole-top support in every failed all-active descriptor is one fixed
   reversible two-node linkage; and
3. every failed all-active descriptor satisfies the curvature-cofactor
   premise of Proposition 5.2 of
   *three_active_shell_gluing_gate.md*.

There are exactly 26 such ordered support pairs.  All 26 are positive-
invariant pairs and none is signed.  Their pair fingerprint is

```text
393474671be0bf095868e66cbcbf3164d941b99191517f172a41f157e20b21af
```

The selector is frozen in `src/prospective_no_promotion_26.py`, with focused
tests in `tests/test_prospective_no_promotion_26.py`.  Every analytic,
pair-recurrence, and global flag remains false.

## 2. Exact incidence table

The 26 pairs have 124 affine-feasible failed incidences:

\[
 30\quad\hbox{one-active},\qquad
 0\quad\hbox{two-active},\qquad
 94\quad\hbox{all-active}.
\]

The frozen incidence hashes are

```text
all 124:    af666979be9e3b747375ce885d5feabbb01ed3053ccca786e27b12558a4e3f20
one-active: d5c045a19191ec841ec75a0c0014ab04b7f638451eec6eee514bfa910b6d7d8e
all-active: 8c99d1994817920d3226b797dced3d863fb4bd86953f0f1bcb02c277f346aab5
```

The one-active rows use only three structural proof shapes from the
arbitrary-orientation graph argument:

| structural route | incidences |
|---|---:|
| mixed linkage contains the physical active source | 20 |
| Family III, origin service of resistance zero | 8 |
| Family III, no historically reachable positive debt | 2 |

In particular, none of the 30 rows belongs to the generalized Family-II
single-cofactor/unbounded-base gate which occurs elsewhere in the 795.
The structural arguments apply verbatim, but the published graph theorem
was frozen on the different candidate-1,227 selector.  A scope-extension
audit is therefore still required before these 30 rows can be called
certified.

The fixed all-active top supports are

| top support | pairs | incidences |
|---|---:|---:|
| \(\{2A,B+C\}\) | 8 | 40 |
| \(\{A+C,B+C\}\) | 18 | 54 |

For each physical orientation and rate vector, detailed balance on this
reversible top selects one fixed correction \(\ell\) and hence

\[
 {\cal F}_{\ell}(x)
 =K+\sum_i\log(x_i!)+\ell\mathbin{\cdot}x,
 \qquad G=1+{\cal F}_{\ell},\qquad W=G^4.             \tag{2.1}
\]

The one-active fourth-power interface permits the same arbitrary fixed
\(\ell\).  Thus there is no base-potential correction conflict on these
26 pairs.

## 3. Why this is the maximal no-promotion target

Exactly 749 of the prospective 795 pairs have a feasible two-active
failure.  Every one of those 749 has at least one two-active promotion
failure.  Their common pair fingerprint is

```text
71de0de1b266a0e75f309495d31eb2ba0c7f4c39590054ccc2fd38597b695945
```

In particular, all 77 pairs with an audited closed rank-one two-active
episode also have another promotion failure.  The local rank-one episode
does not produce a larger no-promotion pair selector.

The other 46 pairs have no two-active failure.  They split disjointly into
the 26 pairs above and 20 pairs whose all-active theorem uses the exact
rank-two linear workload rather than a corrected factorial potential.  The
20-pair fingerprint is

```text
32e2d78e51f99d765eb76bbb8a2bcf490c4dfd0208f4b904a0475efea506b446
```

Those 20 pairs therefore retain a genuine potential-switch obligation.
The 26-pair family is the maximal exact subfamily which avoids both a
two-active promotion kernel and an already visible factorial/linear
potential switch.

## 4. The exact powered all-active obligation

Proposition 5.2 of *three_active_shell_gluing_gate.md* proves

\[
 {\cal L}{\cal F}_{\ell}(x_n)\longrightarrow-\infty  \tag{4.1}
\]

along each failed all-active sequence in this selector.  Equation (4.1)
does not by itself imply negative drift of the convex fourth power.  The
missing statement is the following network-local lift.

> **Open powered-all-active lemma.**  Fix one of the 26 pairs, an arbitrary
> physical orientation, and positive rates.  Let \(\ell\) be the
> detailed-balance correction selected by its fixed reversible top.  Along
> every affine-feasible failed all-active exact-tier sequence,
> \[
>   {\cal L}(1+{\cal F}_{\ell})^4(x_n)
>       \longrightarrow-\infty.                     \tag{4.2}
> \]
> The estimate must be uniform over the finite failed-cone menu of the
> fixed pair and strong enough to give a finite-exception physical-time
> generator bound.

Here is a precise sufficient estimate to audit.  Write \(T\) for the fixed
top linkage, \(R\) for the other linkage, \(\alpha_n\) for the top source
scale, \(\beta_n\) for the maximal \(R\)-source propensity, and

\[
 d_r={\cal F}_{\ell}(x+\zeta_r)-{\cal F}_{\ell}(x).
\]

Let \({\cal D}_{T,n}\ge0\) be the reversible top entropy-dissipation
term and let \(a_n\to\infty\) be the forced lower-tier logarithmic gap.
It is enough to prove, uniformly on every selected failed cone,

\[
\begin{aligned}
 {\cal L}{\cal F}_{\ell}
   &\le-c\{{\cal D}_{T,n}+\beta_na_n\},\\
 \sum_r\lambda_r d_r^2
   &\le C\{{\cal D}_{T,n}+\beta_n(1+\log^2 R_n)\},\\
 \sum_r\lambda_r|d_r|^k
   &\le C\{{\cal D}_{T,n}\log^{k-2}R_n
              +\beta_n(1+\log^kR_n)\},\qquad k=3,4, \tag{4.3}
\end{aligned}
\]

where \(R_n=1+\lVert x_n\rVert_1\).  The curvature-cofactor premise gives
\(\alpha_n/x_{n,i}=O(\beta_n)\) for every coordinate changed by the top
reaction.  This is the expected input for controlling the shifted
factorial remainder near top detailed balance; away from detailed balance,
\({\cal D}_{T,n}\) should absorb the top jump moments.

Substituting (4.3) into the exact identity

\[
\begin{split}
 {\cal L}G^4={}&4G^3{\cal L}{\cal F}_{\ell}
 +6G^2\sum_r\lambda_rd_r^2
 +4G\sum_r\lambda_rd_r^3
 +\sum_r\lambda_rd_r^4                         \tag{4.4}
\end{split}
\]

would prove (4.2), because \(G\asymp R_n\log R_n\) and

\[
 {\log^2R_n\over G a_n}\longrightarrow0.
\]

The unproved step is the uniform discrete bound (4.3), including the
shifted falling-factorial terms.  It must not be replaced by the invalid
inference that negative drift of \({\cal F}_{\ell}\) survives every convex
transform.

## 5. Conditional composition boundary

If, and only if,

1. the candidate one-active fourth-power theorem is certified;
2. its graph theorem is formally extended and audited on the 30 structural
   rows above; and
3. the powered all-active lemma (4.2) is proved and audited,

then the common potential \(W\) in (2.1) has the correct local rule on every
failed and passing descriptor of each selected pair.  The usual
finite-exception/common-potential physical-time gluing theorem would then
give a 26-pair recurrence theorem.  None of those conditional conclusions
is asserted by this note.
