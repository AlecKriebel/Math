# Root audit: trace propagation and the three-strand algebra

Status: proved at the abstract two-projection level; source-dependent Markov
step audited against Lechner, Proposition 2.4 and Lemma 3.1.

## 1. Markov agreement does not require scalar partial traces here

Let \(R\) be any unitary Yang--Baxter matrix with spectrum
\(\{-1,q\}\), \(q=e^{i\pi/3}\).  Lechner's Proposition 2.4 proves that a
unitary \(R\)-matrix with no pair of opposite eigenvalues has an irreducible
shift inclusion and hence its normalized tensor-space character is Markov.
Lemma 3.1 applies this directly to every non-involutive Hecke \(R\)-matrix
with \(q\ne\pm1\).

The exceptional spectrum has no opposite pair: \(-q\notin\{-1,q\}\) and
\(1\notin\{-1,q\}\).  Therefore the normalized matrix traces of every
arbitrary solution in the class form the unique Hecke Markov trace with

\[
\eta=\tau(P)=\frac{\operatorname{rank}P}{d^2}=\frac12.
\]

This is a trace-level conclusion.  It does **not** say that either
unnormalized partial trace of \(P\) is scalar.  Lechner's Proposition 2.3
does imply scalar normalized partial trace of \(R\) once the Markov property
is known, but that conclusion uses the operator-algebraic result that the
partial trace lies in the generated von Neumann algebra.  It must not be
replaced by the false general statement that an arbitrary representation
with the same scalar character has scalar partial trace.

For the matrix-class problem, the source argument appears to prove
standardness automatically.  A finite-dimensional proof and the precise
left/right convention remain to be written before upgrading the global
standardness claim.

## 2. Abstract two-projection theorem

Let \(p,q\) be orthogonal projections on a finite-dimensional Hilbert space
\(\mathcal K\), and let \(0<\lambda<1\).  Suppose

\[
pqp-qpq=\lambda(p-q).
\tag{1}
\]

Define

\[
C=pqp-\lambda p=qpq-\lambda q.
\]

Both displayed expressions show, without any commutation assumption, that

\[
pC=C=Cp,\qquad qC=C=Cq.
\]

Thus \(\operatorname{ran}C\) lies in
\(E\mathcal K=\operatorname{ran}p\cap\operatorname{ran}q\), where \(E\) is
the projection onto the common range.  Because \(C=C^*\), it vanishes on
\((E\mathcal K)^\perp\).  On \(E\mathcal K\), \(p=q=I\), so
\(C=(1-\lambda)I\).  Hence

\[
\boxed{C=(1-\lambda)E}
\]

and

\[
\boxed{pqp=\lambda p+(1-\lambda)E,\qquad
       qpq=\lambda q+(1-\lambda)E.}
\tag{2}
\]

On \(L=\operatorname{ran}p\ominus E\mathcal K\), equation (2) gives
\((qp)^*(qp)=\lambda I_L\).  Similarly,
\((qp)(qp)^*=\lambda I_{\operatorname{ran}q\ominus E\mathcal K}\).
Consequently \(\lambda^{-1/2}qp\) is a unitary between these two spaces.
Choosing an orthonormal basis one obtains two-dimensional blocks on which

\[
p=\begin{pmatrix}1&0\\0&0\end{pmatrix},\qquad
q=\begin{pmatrix}
\lambda&\sqrt{\lambda(1-\lambda)}\\
\sqrt{\lambda(1-\lambda)}&1-\lambda
\end{pmatrix}.
\tag{3}
\]

The remaining space is the common kernel.  Therefore (1) permits only:

- common-range one-dimensional blocks;
- common-kernel one-dimensional blocks;
- the generic block (3).

There are no unmatched \(p=1,q=0\) or \(p=0,q=1\) blocks.

For the exceptional relation, \(\lambda=1/3\).  Thus every nontrivial
principal angle has squared cosine \(1/3\).

## 3. Exact three-strand multiplicities

Now take \(\mathcal K=V^{\otimes3}\),
\(p=P_{12}\), \(q=P_{23}\), and \(D=d^3\).  Both projections have rank
\(D/2\).  If \(a,b,c\) denote the numbers of common-range,
common-kernel, and generic blocks, respectively, then

\[
D=a+b+2c,\qquad \frac D2=a+c,
\]

so \(a=b\).

The automatic Markov trace gives

\[
\frac1D\operatorname{Tr}(pq)=\eta^2=\frac14.
\]

On the canonical blocks,

\[
\operatorname{Tr}(pq)=a+\frac13c.
\]

Solving with \(c=D/2-a\) gives

\[
\boxed{a=b=\frac{D}{8}=\frac{d^3}{8},\qquad
       c=\frac{3D}{8}=\frac{3d^3}{8}.}
\]

At three strands, integrality therefore forces only \(2\mid d\), not
\(4\mid d\).  In particular, the abstract three-strand algebra has perfectly
integral multiplicities at \(d=6\):

\[
(a,b,c)=(27,27,81).
\]

Any obstruction at \(d=6\) must use higher strands or the local-overlap
realization by a single two-site projection, not merely the abstract
two-projection relation.

## 4. Verification

Run:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_two_projection_blocks.py
```

The script checks (3), (1), the central element on all canonical block types,
and the \(d=6\) arithmetic using exact algebraic numbers.
