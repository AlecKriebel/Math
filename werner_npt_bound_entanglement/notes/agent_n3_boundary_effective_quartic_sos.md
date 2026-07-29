# Exact effective-quartic stability at the canonical nonnormal zero

## The local theorem

Let
\[
C_0=|000\rangle\langle110|+|001\rangle\langle111|
\]
in \((\mathbb C^3)^{\otimes3}\), and parameterize nearby rank-two
partial isometries by independent polar Stiefel charts for their left
and right two-frames.  The real tangent chart has dimension \(204\).

**Theorem.**  The Hessian of \(Q_3\) at \(C_0\) is positive
semidefinite, of rank \(149\) and nullity \(55\).  After exact
Lyapunov--Schmidt elimination of all \(149\) positive directions, the
degree-four reduced form on the \(55\)-dimensional kernel is a rational
sum of squares.  In particular it is nonnegative.  Its real zero set is
the union of four rational linear spaces of dimensions
\[
37,\ 37,\ 27,\ 27.
\]

This is a local theorem.  It neither proves unrestricted three-copy
positivity nor excludes a sign change at order six or above on three
of the four equality components.

## Lyapunov--Schmidt calculation

Choose one pivot \(p_j\) in each positive rank-one Hessian block.  The
quadratic term is
\[
q_2(p)=\sum_{j=1}^{149}h_jp_j^2,\qquad h_j>0.
\]
The cubic restricted to the \(55\)-dimensional kernel vanishes
identically.  Define the mixed quadratic forms
\[
\ell_j(k)=Dq_3(k)[p_j].
\]
For
\[
z(t)=tk+t^2p+O(t^3),
\]
the order-four coefficient is
\[
q_{4,\mathrm{raw}}(k)
+\sum_j\bigl(h_jp_j^2+\ell_j(k)p_j\bigr).
\]
Completing each square gives the reduced quartic
\[
q_{4,\mathrm{eff}}(k)
=q_{4,\mathrm{raw}}(k)
-\sum_{j=1}^{149}\frac{\ell_j(k)^2}{4h_j}.
\]
Thus it is essential to certify the effective form, not merely the raw
restriction to the Hessian kernel.

## Exact Gram certificate

The effective quartic has \(1448\) nonzero monomial coefficients and a
\(30\)-dimensional group of coordinate-sign symmetries.  Its
degree-two Gram monomials split into \(158\) character blocks, with
largest block size \(24\).  Exact face reconstruction leaves \(505\)
monomials and total Gram rank \(300\).

On the reconstructed rational face, coefficient matching is an exact
system of \(1759\) equations in \(670\) reduced symmetric-Gram entries.
Its rational rank is \(555\).  Fixing the \(115\) free entries at
rational values obtained from a numerical relative-interior point and
solving every pivot exactly gives positive-definite reduced Gram
matrices.  Exact \(LDL^T\) factorization verifies every pivot is
positive.  Direct expansion matches all \(1759\) coefficients.

The discovery stage was used only to locate the rational face and a
convenient interior point.  The verification stage is exact.

## Independent chart audit

The verifier does not trust stored Taylor data.
`verification/derive_n3_boundary_effective_quartic.py` uses only
Gaussian-rational arithmetic and begins with
\[
Q_3(C)=\sum_{S\subseteq\{1,2,3\}}
\left(-\frac12\right)^{|S|}
\|\operatorname{Tr}_S C\|_2^2.
\]
It reconstructs:

1. all \(204^2\) Hessian entries;
2. the \(149\) positive rank-one blocks and a \(55\)-element rational
   kernel basis;
3. all \(2446\) raw quartic terms;
4. all \(149\) mixed-cubic forms, containing \(544\) terms in total;
5. the \(1448\)-term effective quartic.

`verification/verify_n3_boundary_effective_quartic_sos.py` compares
those independently derived objects with the certificate, recomputes
the Hessian-inverse subtraction, checks positive exact \(LDL^T\)
pivots, and expands the Gram representation.  Both programs use only
the Python standard library.

## Equality decomposition

Because every reduced Gram is positive definite, equality is
equivalent to the vanishing of \(300\) explicit rational quadrics.
Exactly \(278\) split as products of linear forms.  Only \(36\)
independent linear factors occur.  The graph of forbidden simultaneous
nonzero factors has \(64\) maximal independent sets:
\[
2\times18,\qquad6\times10,\qquad56\times6.
\]

Restricting the remaining \(22\) quadrics to these branches makes them
factor recursively.  Exact branching visits \(486\) rational linear
states and ends in \(148\) linear leaves.  After containment removal,
four maximal components remain, with dimensions \(37,37,27,27\).
There is no nonlinear residual component.

The \(299\)-kilobyte finite branching certificate is
`verification/certificates/n3_boundary_effective_zero_decomposition.json`.
The standard-library verifier
`verification/verify_n3_boundary_effective_zero_decomposition.py`
independently reconstructs the \(300\) Gram-zero quadrics, checks all
\(278\) ambient product factorizations, re-enumerates the \(64\)
initial branches, checks every split in the \(486\)-node DAG, checks
all \(148\) leaves, and verifies both containments in the asserted
four-component union.

One \(37\)-dimensional component is the tangent space to
\[
C=|a\rangle\langle b|_{12}\otimes P_W,
\qquad \operatorname{rank}P_W=2.
\]
This manifold consists of exact zeros since
\[
Q_3(C)=Q_2(|a\rangle\langle b|)\,Q_1(P_W)=0.
\]
The other \(37\)-dimensional component and the two
\(27\)-dimensional components are the complete residual local
frontier.  Exact test paths have positive sixth-order coefficients,
but a uniform secondary Lyapunov--Schmidt certificate has not yet been
proved.

## Reproduction

Run:

```text
/usr/bin/python3 -S verification/verify_n3_boundary_flat_quartic_sos.py
/usr/bin/python3 -S verification/verify_n3_boundary_effective_quartic_sos.py
/usr/bin/python3 -S verification/verify_n3_boundary_effective_zero_decomposition.py
/usr/bin/python3 discovery/decompose_n3_boundary_effective_zero_ideal.py
```

The first two are independent exact certificate checks.  The third
performs the exact equality-ideal decomposition.
