# Quadratic positive loci: exact reduction and residual program

## Status

This folder does **not** resolve the five-dimensional kissing problem.  It
isolates and verifies a materially smaller version of the weighted
two-design gap:

> If a 41-point kissing code has no nonnegative weights making its first
> moment zero and its second moment isotropic, then all 41 points lie in the
> strict positive locus of a normalized quadratic
> \[
> q(x)=b\mathbin{\cdot}x+x^{\mathsf T}Ax,\qquad
> \operatorname{tr}A=0,\quad \lambda_{\max}(A)=1.
> \]
> After rotation and coordinate reflections, the remaining separator
> parameters lie in an explicit compact eight-dimensional semialgebraic
> set.  Moreover, a new exact enlarged-cap certificate eliminates every
> separator with \(\lVert b\rVert\geq50\).

Thus the unresolved statement is no longer over an unnormalized, noncompact
space of quadratics.  It is the following exact compact occupancy problem:

\[
\tag{QPL}
\begin{split}
&-4\leq\lambda_1\leq\cdots\leq\lambda_4\leq\lambda_5=1,\qquad
  \sum_i\lambda_i=0,\\
&b_i\geq0,\qquad \sum_i b_i^2\leq50^2,\\
&q_{\lambda,b}(x)=\sum_i\lambda_i x_i^2+\sum_i b_i x_i.
\end{split}
\]

Prove uniformly that a kissing code contained in
\(\{x\in S^4:q_{\lambda,b}(x)\geq0\}\) has at most 40 points.  The closed
inequality deliberately includes every boundary point.

The exact reduction is `PROVED`, conditional only on the separately
computer-certified enlarged-cap theorem already checked into this
repository.  The uniform bound (QPL) is `CONJECTURAL`.

## 1. Why failure of weighted isotropy produces a quadratic

Put
\[
\Phi(x)=\left(x,xx^{\mathsf T}-\frac15I\right)
\in\mathbb R^5\oplus\operatorname{Sym}_0(5).
\]
Weights \(p_x\geq0\), \(\sum p_x=1\), satisfy
\[
\sum p_x x=0,\qquad \sum p_x\,x x^{\mathsf T}=\frac15I
\]
exactly when \(0\in\operatorname{conv}\{\Phi(x):x\in C\}\).
If no such weights exist, strict separation from this finite compact convex
hull gives \(b\in\mathbb R^5\) and \(A\in\operatorname{Sym}_0(5)\) such that
\[
b\mathbin{\cdot}x+\langle A,xx^{\mathsf T}-I/5\rangle
=b\mathbin{\cdot}x+x^{\mathsf T}Ax>0
\quad(x\in C).
\]
This equivalence uses neither symmetry, rigidity, antipodality, nor a finite
inner-product alphabet.

## 2. Canonical compact normalization

If \(A=0\), then \(q(x)>0\) is an open hemisphere.  The exact robust-cap
theorem gives occupancy at most 34, so this cannot contain 41 kissing
points.

Otherwise \(\operatorname{tr}A=0\) implies
\(\lambda_{\max}(A)>0\).  Multiplying \(q\) by a positive scalar, rotating,
ordering the eigenspaces, and reflecting coordinate axes gives
\[
A=\operatorname{diag}(\lambda_1,\ldots,\lambda_5),\qquad
\lambda_5=1,\quad \lambda_1\leq\cdots\leq\lambda_5,\quad b_i\geq0.
\]
Since the trace is zero and the four other eigenvalues are at most one,
\(\lambda_i\geq-4\).  There are three free eigenvalue parameters and five
linear parameters: eight dimensions in total.

Let \(B=\lVert b\rVert\) and \(u=b/B\).  Rayleigh's inequality gives
\[
q(x)\leq B\,u\mathbin{\cdot}x+1.
\]
If \(B\geq50\), positivity forces
\[
u\mathbin{\cdot}x>-1/B\geq-1/50.
\]
The new exact theorem in
[`proof_enlarged_cap_minus_1_over_50.md`](proof_enlarged_cap_minus_1_over_50.md)
says that this closed enlarged cap contains at most 39 kissing points.  Thus
a 41-point counterexample must have \(B<50\).  Replacing this by
\(B\leq50\) makes the residual parameter set compact without losing any
counterexample.

Run the exact arithmetic and dependency-hash audit with

```sh
python3 experiments/quadratic_positive_locus/verify_exact_reduction.py
python3 -m unittest \
  experiments.quadratic_positive_locus.test_exact_reduction -v
```

## 3. Complete axisymmetric split

Two opposite spectral endpoints reduce to one height \(t=x_5\).

For
\[
q_-(t)=1-5t^2+\beta t
\]
the roots are
\[
r_\pm=\frac{\beta\pm\sqrt{\beta^2+20}}{10}.
\]
For \(0\leq\beta<4\), the positive locus is a genuine belt
\(r_-<t<r_+\).  For \(\beta\geq4\), it is contained in the one-sided cap
\(t>r_-\).  Exact substitution shows
\[
r_-=-1/50\quad\Longleftrightarrow\quad
\beta=\frac{499}{10}.
\]
Consequently the new cap theorem proves occupancy at most 39 for every
\(\beta\geq499/10\).

For
\[
q_+(t)=5t^2-1+\beta t
\]
the roots are
\[
s_\pm=\frac{-\beta\pm\sqrt{\beta^2+20}}{10}.
\]
For \(0\leq\beta<4\), the positive locus is the union
\([-1,s_-)\cup(s_+,1]\) of two caps.  At \(\beta=4\), \(s_-=-1\), and for
every \(\beta\geq4\) only the northern component remains; it lies in the
open hemisphere \(t>0\).  Hence its occupancy is at most 34.

These exact endpoint reductions leave the belt and two-cap regimes as
honest hard cases rather than silently assuming a single cap.

## 4. Construction attacks

`search_fixed_positive_locus.py` performs direct manifold optimization of
41 points in three fixed mean-zero quadratic positive loci:

- the pure belt \(1-5t^2>0\);
- the symmetric two-cap locus \(5t^2-1>0\);
- the shifted belt/cap \(1-5t^2+5t>0\).

It deliberately breaks symmetry and uses independent deterministic seeds.
Coordinates, active maximum inner products, frame spectra, and minimum
quadratic margins are recorded.  These are floating-point near misses only.
No failure of this optimizer is evidence of nonexistence.

In the recorded four-start, 5,000-iteration scan, the best feasible near
misses had maximum inner products
\[
0.5375770409\quad\text{(belt)},\qquad
0.5562907281\quad\text{(two caps)},\qquad
0.5574466962\quad\text{(shifted cap)}.
\]
All three remain decisively above \(1/2\).

Reproduce a modest scan with

```sh
.venv/bin/python \
  experiments/quadratic_positive_locus/search_fixed_positive_locus.py \
  --starts 4 --iterations 5000 \
  --output experiments/quadratic_positive_locus/construction_scan.json
```

Recompute every norm, quadratic margin, and pairwise maximum independently:

```sh
.venv/bin/python \
  experiments/quadratic_positive_locus/audit_construction_scan.py
```

## 5. Certified enlarged-cap theorem at \(-1/50\)

The degree-eight exact positive-kernel certificate proves
\[
\langle u,x\rangle\geq-1/50
\quad\Longrightarrow\quad |C|\leq39.
\]
This improves the general linear-dominance cutoff from \(300\) to \(50\)
and eliminates the axisymmetric \(q_-\) family from
\(\beta=1/(1/50)-5(1/50)=499/10\) onward.

The exact kernel satisfies \(F(x,x)\leq35\) and
\(F(x,y)\leq-9/10\) for distinct feasible pairs.  Hence
\[
|C|\leq1+\frac{35}{9/10}=\frac{359}{9}<40.
\]
Its integer Gram factors and 1,344-leaf exact Bernstein tree are checked by
`verify_enlarged_cap_minus_1_over_50.py`.  The sampled solver and approximate
matrices are retained only as discovery history.

## 6. Residual SOS program

[`residual_sos_formulation.md`](residual_sos_formulation.md) gives a direct
parameter-dependent positive-kernel/SOS formulation over the compact
eight-parameter set (QPL).  It contains:

- an exact kernel summation lemma;
- all parameter, sphere, contact, positive-locus, and boundary constraints;
- a matrix-SOS condition ensuring kernel positivity for each separator;
- exact polynomial identities whose objective below 41 would prove
  occupancy at most 40.

This is a concrete low-dimensional semialgebraic certificate format, not a
claim that a low-degree certificate exists.

## 7. Boundary and rigor audit

- Strict separation gives \(q(x)>0\), but the proposed upper bound is imposed
  on the larger closed locus \(q(x)\geq0\).
- The linear-dominance endpoint \(B=50\) is included: at
  \(u\cdot x=-1/50\), Rayleigh gives \(q(x)\leq0\).
- The cap theorem includes height exactly \(-1/50\), contacts
  \(x\cdot y=1/2\), and determinant-zero triples.
- Eigenvalue multiplicities cause no loss: after diagonalization,
  independent coordinate reflections preserve diagonal \(A\) and make
  every \(b_i\geq0\).
- Solver objectives, random audits, and approximate coordinates in this
  folder are never imported by the exact verifier.
- Proof verifiers use always-on exceptions rather than Python `assert`.
  Their tests run valid and deliberately tampered certificates under
  `python -O`, so optimized mode cannot silently discard certificate
  checks.
- This reduction does not assume that a maximum code is centered, jammed,
  antipodal, or a two-design.  It addresses precisely the alternative in
  which weighted centering and isotropy fail.

## 8. Precise unresolved gap

Prove (QPL), or produce 41 kissing points in one of its positive loci.  An
SOS solution must have an exact rational/algebraic PSD factorization and
full-domain nonnegativity audit.  A sampled SDP value below 41 is not enough.
