# A literal exact 334-dimensional defect minor

## Status

The numerical rank-334 defect in the constrained five-replica DTH lift has
now been converted to a **literal exact minor**.  The selected source
coordinates belong to the rational holomorphic charts

\[
 h_\lambda=E_\lambda A_\lambda E_\lambda^{\mathsf T}
\]

from `verification/agent_dth_exact_k_coordinates.py`.  Every selected target
row is a direct range-membership equation for the exact physical product
face from `verification/agent_dth_exact_face_coordinates.py`.

The resulting \(334\times334\) matrix has rank 334 over each of

\[
\mathbb F_{1000003},\qquad \mathbb F_{1000033}.
\]

Thus the rational defect map has rank **at least** 334.  This note does not
yet assert the matching rational upper bound; that will follow either from
the completed rational correction with a full exact face replay, or from an
explicit 3805-dimensional kernel certificate.

This is a statement about the first lifted pseudomoment relaxation.  It is
not a physical DTH counterexample and not a Werner-state witness.

## 1. Exact row convention

For one mixed block let \(F\in\mathbb Q^{n\times r}\) be the exact face
basis and let \(J\) be a set of \(r\) rows such that \(F_J\) is invertible.
For every \(q\notin J\), put

\[
 \ell_q^{\mathsf T}
 =e_q^{\mathsf T}-F_{q,:}F_J^{-1}e_J^{\mathsf T}.
\]

Then \(\ell_q^{\mathsf T}F=0\).  A symmetric mixed restriction matrix \(M\)
belongs to the face only if

\[
 \ell_q^{\mathsf T}M e_s=0
 \tag{1}
\]

for every column \(s\).  Each selected defect row is exactly one equation
(1); no floating complement or approximate null vector occurs in the exact
replay.

The final selected rows use only nine mixed type triples:

\[
122,\ 212,\ 221,\ 222,\ 224,\ 242,\ 422,\ 424,\ 442.
\]

Their multiplicities in the minor are respectively

\[
2,\ 2,\ 5,\ 176,\ 46,\ 51,\ 50,\ 1,\ 1.
\]

## 2. Exact source convention

The 334 columns are entries of the symmetric matrices \(A_\lambda\).  A
diagonal label \((\lambda,i,i)\) denotes

\[
 E_\lambda e_ie_i^{\mathsf T}E_\lambda^{\mathsf T},
\]

and an off-diagonal label \((\lambda,i,j)\), \(i<j\), denotes

\[
 E_\lambda(e_ie_j^{\mathsf T}+e_je_i^{\mathsf T})
 E_\lambda^{\mathsf T}.
\]

The raw rational crossing is rebuilt as

\[
 C=B A^{-1},
\]

where \(A,B\) are the exact 103-diagram restriction bridges.  Its reduced
common denominator is 14400 and its largest numerator has magnitude 115200.
The global crossing is \(C^{\otimes3}\).

## 3. Reproducibility

The discovery selector is

```text
discovery/agent_dth_select_exact_defect_minor.py
```

and the exact finite-field replay is

```text
verification/agent_dth_defect_minor_modular.py
```

The current label artifact is

```text
/tmp/dth_direct_defect_minor334.npz
```

with SHA-256

```text
4eba7035971142afc7eb2f4523abac63a04e56fc7e08575f67450e33c9e1a01b
```

The source-label and target-row-label checksums, using little-endian signed
64-bit serialization, are

```text
source: 524670289a7d4f1d56a90d8e21766a79748de9e1ed2444d393d28b4740ed73c2
target: d84ce96c6f4c64127d33ea33866083add6f557787cc59caee717f342fad37624
```

The floating selection minor has condition number

\[
2.5577148496824517\times10^5,
\]

while both exact modular replays have full rank.  Floating arithmetic is
therefore used only to choose labels, never to decide exact rank.

## 4. Integral correction chart

There is a useful simplification for the pending rational correction.  For
each source coordinate \(c\), choose \(d_c>0\) so that

\[
 H_c^{\rm int}=d_c H_c
\]

is integral.  On the selected coordinates one may take \(d_c\le576\).
Writing \(b_c=a_c/d_c\) gives

\[
 h=\sum_c b_c H_c^{\rm int}.
\]

For the selected target rows, clearing the row functional needs a
denominator at most 2.  After replacing the local crossing by its integer
numerator, the full pivot matrix and the residual of a globally rounded
candidate are therefore integer.  One integer linear solve supplies an
exact correction, with the common factors \(14400^3\) and the row scales
cancelling from the homogeneous equations.

