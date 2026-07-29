# The Evans--Pugh \(D^{(6)}\) connection and the ordinary \(d=6\) problem

Date: 2026-07-28

Status: **PROVED at the stated direct-flattening scope** and
**EXACT_COMPUTATION** for the reconstructed connection.

## 1. Question and conclusion

The \(SU(3)_3\) nimrep graph \(\mathcal D^{(6)}\) has six vertices.  This
makes the Ocneanu-cell connection of Evans and Pugh look superficially like
a possible \(R\)-matrix on \(\mathbb C^6\otimes\mathbb C^6\).

It is not one.  The six labels are graph vertices (boundary or height
labels), not six freely tensorable local states.  The connection acts on
composable pairs of directed graph edges.  For \(\mathcal D^{(6)}\), there
are

\[
10\text{ directed edges with multiplicity},\qquad
20\text{ composable two-edge paths}.
\]

Thus its local face operator is \(20\times20\), not \(36\times36\).
Adjacent insertions act on the 48-dimensional space of composable
three-edge paths, not on \((\mathbb C^6)^{\otimes3}\), which has dimension
216.

After an explicit scalar normalization, the face operator nevertheless has
exactly the same exceptional Hecke spectrum:

\[
\operatorname{spec}(F)=
\{-1^{(10)},e^{i\pi/3\, (10)}\}.
\]

It therefore gives a highly relevant path-space realization of the same
Hecke parameter, but it does not answer the ordinary \(d=6\) matrix problem.

## 2. What Evans--Pugh actually construct

The primary source is:

> D. E. Evans and M. Pugh, *Ocneanu Cells and Boltzmann Weights for the
> \(SU(3)\) \(\mathcal{ADE}\) Graphs*, arXiv:0906.4307.

In their equations `Connection_using_weights_W` and `eqn:HeckeRep`, the
indices \(\rho_i\) are directed **edges** of the graph.  A nonzero connection
coefficient

\[
X^{\rho_1,\rho_2}_{\rho_3,\rho_4}
\]

has the square-boundary compatibility conditions

\[
s(\rho_1)=s(\rho_3),\quad
r(\rho_1)=s(\rho_2),\quad
r(\rho_3)=s(\rho_4),\quad
r(\rho_2)=r(\rho_4).
\]

Equivalently, for fixed endpoints \(x,y\), their matrix \(U^{(x,y)}\)
replaces the middle vertex/edge labels of a length-two path from \(x\) to
\(y\).  The paper says this explicitly immediately before its quantum-number
lemma:

\[
[U^{(s(\rho_1),r(\rho_2))}]_{r(\rho_1),r(\rho_3)}
=\mathcal U^{\rho_1,\rho_2}_{\rho_3,\rho_4}.
\]

The resulting Yang--Baxter identity is a face/connection identity with
compatibility-restricted sums.  The introduction likewise states that the
Hecke algebra is embedded in an AF **path algebra** of the graph.

These are not the index conventions of an ordinary vertex operator
\(R\in\operatorname{End}(V\otimes V)\), whose four indices each range freely
and whose adjacent copies act on the full tensor cube.

There is a useful reason the graph still resembles a dimension-two
localization.  Its adjacency matrix has the integer Perron--Frobenius vector

\[
\phi=(1,2,2,1,1,1)^T,\qquad A\phi=2\phi.
\]

Consequently appropriately boundary-weighted path spaces can have dimensions
proportional to \(2^n\).  This is a dimension count for a path/quasi-tensor
tower; it does not supply strict identifications with
\((\mathbb C^2)^{\otimes n}\), much less a two-site matrix on
\(\mathbb C^6\otimes\mathbb C^6\).

## 3. Exact reconstruction at \(\mathcal D^{(6)}\)

Use the graph labelling of Evans--Pugh Figure 17:

\[
0\longrightarrow1
\mathrel{\substack{\gamma\\[-2pt]\longrightarrow\\[-2pt]\gamma'}}
2\longrightarrow0,
\qquad
2\longrightarrow3_r\longrightarrow1
\quad(r=0,1,2).
\]

Counting the double edge separately gives ten directed edges.  If

\[
K_m=\ell^2\{
(\rho_1,\ldots,\rho_m):
r(\rho_j)=s(\rho_{j+1})
\},
\]

then direct enumeration gives

\[
\dim K_2=20,\qquad \dim K_3=48.
\]

Specializing the printed \(\mathcal D^{(3k+3)}\) blocks to \(k=1\), with

\[
q_0=e^{i\pi/6},\qquad [2]_{q_0}=\sqrt3,
\]

produces nine endpoint blocks.  Their dimensions and ranks are

\[
\begin{array}{c|ccccccccc}
(x,y)&(0,2)&(1,0)&(1,3_0)&(3_0,2)&(1,3_1)&(3_1,2)&
(1,3_2)&(3_2,2)&(2,1)\\ \hline
\dim&2&2&2&2&2&2&2&2&4\\
\operatorname{rank}U^{(x,y)}&1&1&1&1&1&1&1&1&2 .
\end{array}
\]

Consequently the global face Hecke operator \(U\in\operatorname{End}(K_2)\)
satisfies, exactly,

\[
U=U^*,\qquad U^2=\sqrt3\,U,\qquad
\operatorname{rank}U=10.
\]

Put

\[
Q=e^{i\pi/3}=q_0^2,\qquad
P_{\rm face}=\frac{U}{\sqrt3},\qquad
F=QI_{K_2}-q_0U.
\]

Then

\[
P_{\rm face}=P_{\rm face}^*=P_{\rm face}^2,\qquad
\operatorname{rank}P_{\rm face}=10,
\]

\[
F^*F=I,\qquad
(F+I)(F-QI)=0.
\]

On \(K_3\), the two path-local insertions obey

\[
P_1P_2P_1-P_2P_1P_2=\frac13(P_1-P_2)
\]

and, equivalently,

\[
F_1F_2F_1=F_2F_1F_2.
\]

All of these claims are checked in exact SymPy arithmetic by
`scripts/audit_evans_pugh_d6_connection.py`.  A second verifier,
`verifiers/verify_evans_pugh_d6_from_cells.py`, independently reconstructs
the operator from the specialized cell values and equation `HeckeRep`,
without entering the printed \(U\)-blocks.

## 4. Why the obvious flattenings fail

### 4.1 Vertex-label flattening has the wrong state space

The connection coefficient needs a length-two path, hence three vertex
labels plus edge-multiplicity data.  In particular, the two parallel
\(\gamma,\gamma'\) edges cannot be recovered from a pair of vertex labels.
There is no map supplied by the cell system that turns its 20 path states
into the 36 free basis states of \(\mathbb C^6\otimes\mathbb C^6\).

This is a dimension and indexing mismatch, not merely a normalization issue.

### 4.2 Edge-label zero extension is singular

Let \(E=\ell^2(\{\text{directed edges}\})\cong\mathbb C^{10}\).  Then
\(K_2\) is the 20-dimensional composable-pair subspace of
\(E\otimes E\cong\mathbb C^{100}\).  Extending \(F\) by zero outside \(K_2\)
has rank 20 and an 80-dimensional kernel, so it is not unitary.

### 4.3 Even the two scalar Hecke completions fail the braid relation

One might instead let the noncomposable-pair sector carry one of the two
allowed scalar eigenvalues \(s\in\{-1,Q\}\).  This also fails.

The endpoint block \((0,2)\), on the two paths
\((a,\gamma)\) and \((a,\gamma')\), has both eigenvalues \(-1\) and \(Q\).
Append the edge \(a\).  The second adjacent pair is noncomposable.  On a
first-pair eigenvector with eigenvalue \(\lambda\), the two sides of the
ordinary braid relation become

\[
s\lambda^2
\quad\text{and}\quad
s^2\lambda.
\]

For \(s=-1,\lambda=Q\), their difference is \(-i\sqrt3\).  For
\(s=Q,\lambda=-1\), it is \(i\sqrt3\).  Hence neither scalar completion is
an ordinary Yang--Baxter operator.

This does not prove that every imaginable non-scalar completion is
impossible.  It proves that such a completion is additional mathematical
data not contained in the Evans--Pugh face connection.

## 5. What an actual vertex--face conversion would require

To produce an ordinary \(d=6\) witness, one would need a coherent family of
intertwiners, not a relabelling.  At minimum, it must:

1. replace compatibility-restricted path spaces by full tensor powers
   \(V^{\otimes n}\), \(\dim V=6\);
2. preserve both adjacent spatial insertions simultaneously;
3. account for the \(\gamma,\gamma'\) edge multiplicity;
4. intertwine the face generators with a single
   \(R\in\operatorname{End}(V\otimes V)\) for every strand number \(n\);
5. give the half-rank local spectral projection on \(V\otimes V\).

In tensor-network language this would be a genuine vertex--face
intertwiner/biunitary completion with compatible all-\(n\) blocking maps.
Evans--Pugh construct the face connection and path-algebra representation,
but no such ordinary tensor-power intertwiner is part of the cited
construction.

The \(D^{(6)}\) cells are therefore a promising source of structured data,
but using them to solve \(d=6\) remains a new construction problem.

## 6. Reproduction record

- Source archive:
  `tmp/literature/evans_pugh_0906.4307/source.tar`
- Source TeX:
  `tmp/literature/evans_pugh_0906.4307/cells_paper.tex`
- Exact audit:
  `scripts/audit_evans_pugh_d6_connection.py`
- Independent cell-level verifier:
  `verifiers/verify_evans_pugh_d6_from_cells.py`
- Raw output:
  `results/evans_pugh_d6_connection_audit.txt`
- Independent verifier output:
  `results/evans_pugh_d6_from_cells_verifier.txt`
- Command:
  `/Users/alec/Documents/Math/.venv/bin/python
  exceptional_ybe_spectrum/scripts/audit_evans_pugh_d6_connection.py`
- Independent command:
  `/Users/alec/Documents/Math/.venv/bin/python
  exceptional_ybe_spectrum/verifiers/verify_evans_pugh_d6_from_cells.py`
- Run completed:
  `2026-07-28 22:48 PDT`
- Platform:
  `macOS-26.5.2-arm64-arm-64bit`, Apple arm64
- Python:
  `3.9.6`
- SymPy:
  `1.14.0`
- Parent commit at start:
  `a6f5f29a76e49f9e80e3e98b068ef10bf5ad29b9`
- SHA-256, source TeX:
  `e3c956d1c4f89412e86595a877ea88d440a097e46919415a5a0a583da576fbc7`
- SHA-256, source archive:
  `7bb5c50fe9fcbd64b5dda710c3d978d4db0bda317ad6e7ef09953d385dcf7a29`
- SHA-256, exact audit script:
  `012fc8d203231ab392b8a196537874f5bcb26c267cb59f35a3e4c5d2c9c2dbad`
- SHA-256, independent cell-level verifier:
  `ddb5f7c7b684e054a29ab015f462245fd28a6eb4115f615df54ed5b6350f61e6`

No external communication was made.
