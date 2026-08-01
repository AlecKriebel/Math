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

## 5. Completed rational correction and full-face replay

The integer correction solve has now produced an exact rational moment.  Its
compact holomorphic certificate is

```text
/tmp/dth_exact_obstruction_v2.json.gz
```

with SHA-256

```text
707e183995f1963aebe9eef732530396b2baa53421aaa9fcbf9f5cb31c36e9da
```

The full-face verifier does not infer the remaining equations from the
observed rank.  It rebuilds a primitive integer left kernel in every one of
the 216 mixed blocks and checks all

\[
826573
\]

literal scalar membership equations.  After clearing the certificate
denominators, the exact bounds are:

\[
\begin{array}{c|r}
\text{quantity}&\text{bit length}\\
\hline
\text{global coordinate denominator}&1595\\
\text{holomorphic numerator bound}&1617\\
\text{maximum primitive face }\ell^1\text{ norm}&7\\
\text{mixed-entry numerator bound}&1677\\
\text{face-residual numerator bound}&1683.
\end{array}
\]

Every equation vanishes modulo 85 deterministic primes.  Their product has
bit length 1695, hence is larger than twice the residual bound.  Therefore
every integer residual is exactly zero.  This proves, over
\(\mathbb Q\), that the corrected holomorphic moment crosses into the exact
2266-dimensional product face.

The bridge also passes the literal integer intertwining identity

\[
C\,T_{\rm hol}=T_{\rm mixed}\,C,
\]

where the two permutation matrices transpose every local multiplicity
block.  Thus the crossing sends a symmetric holomorphic restriction to an
exactly symmetric mixed restriction; symmetry is not inferred from its
pivot-principal reconstruction.

The same CRT run reconstructs the 64900 entries in the mixed pivot-principal
submatrices and hence all exact mixed face-coordinate matrices.  A direct
independent scaling audit on blocks 222, 224, 242, 422, and 444 agrees with
ordinary floating crossing to relative errors between \(1.4\cdot10^{-14}\)
and \(2.1\cdot10^{-14}\).  As one exact PSD spot check, fraction-free
Sylvester elimination proves the 42 by 42 block 224 positive definite; the
calculation takes about 48 seconds and its final determinant has 108888
bits.

The exact mixed positivity audit has also passed.  Its dyadic reference and
inverse-Cholesky certificate is

```text
verification/certificates/dth_mixed_pd_reference.json.gz
```

with SHA-256

```text
648186810cd9e9becc71eb6d319749c2a2c956d3f152f116ff17a1cdd1bcdf33
```

For each of the 198 nonzero blocks (total rank 2266, maximum dimension 53),
the verifier proves an exact rational reference positive definite by a
strictly diagonally dominant rational congruence, then transfers positivity
to the reconstructed exact block using a rigorously bounded Frobenius
perturbation.  The worst squared perturbation-to-gap ratio is approximately
$2.692\cdot10^{-41}$, in block 144, and is checked as a strict rational
inequality.  Consequently the corrected moment is a genuine exact feasible
pseudomoment with negative objective in the complete corrected first-level
DTH relaxation.  It is not a rank-one physical DTH vector.
