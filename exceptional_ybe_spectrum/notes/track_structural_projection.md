# Track A/C: arbitrary-projection structure

**Checkpoint:** 2026-07-28 21:39 PDT
**Scope:** arbitrary orthogonal \(P\in\operatorname{End}(V\otimes V)\); no
Pauli, Clifford, sparsity, irreducibility, or faithful-localization ansatz.

## 1. Setup

Let \(\dim V=d\), let

\[
P=P^*=P^2,\qquad \operatorname{rank}P=\frac{d^2}{2},
\]

and on \(\mathcal H=V^{\otimes3}\) put

\[
p=P_{12}=P\otimes I,\qquad q_0=P_{23}=I\otimes P.
\]

To avoid confusing the projection \(q_0\) with the Hecke phase, write
\(c=1/3\).  The defining relation is

\[
p q_0 p-q_0p q_0=c(p-q_0). \tag{1}
\]

The letter \(q=e^{i\pi/3}\) is reserved below for the Hecke phase.

## 2. Complete abstract two-projection decomposition

### Proposition 2.1

Let \(p,q_0\) be any two orthogonal projections on a finite-dimensional
Hilbert space satisfying (1), with \(0<c<1\).  Then the space is an orthogonal
sum of:

1. common-one blocks, on which \(p=q_0=1\);
2. common-zero blocks, on which \(p=q_0=0\);
3. identical two-dimensional generic blocks

\[
p=\begin{pmatrix}1&0\\0&0\end{pmatrix},\qquad
q_0=\begin{pmatrix}
c&\sqrt{c(1-c)}\\
\sqrt{c(1-c)}&1-c
\end{pmatrix}. \tag{2}
\]

Thus every nontrivial principal angle has squared cosine \(c\).  In the
exceptional case it has squared cosine \(1/3\).

### Proof

Set

\[
z=pq_0p-cp=q_0pq_0-cq_0.
\]

The equality is (1).  Projection identities give

\[
pz=zp=z,\qquad q_0z=zq_0=z.
\]

Hence the range of the self-adjoint operator \(z\) is contained in
\(K=\operatorname{ran}p\cap\operatorname{ran}q_0\).  On \(K\), both
projections are the identity, so \(z=(1-c)I\).  Self-adjointness then gives

\[
z=(1-c)e, \tag{3}
\]

where \(e\) is the orthogonal projection onto \(K\).  Consequently

\[
pq_0p=cp+(1-c)e,\qquad
q_0pq_0=cq_0+(1-c)e. \tag{4}
\]

Remove \(K\).  On the remaining part of \(\operatorname{ran}p\),
\(pq_0p=cp\).  If \(u\) is a unit vector there, define

\[
w=\frac{q_0u-cu}{\sqrt{c(1-c)}}.
\]

Then \(w\in\ker p\), \(\|w\|=1\), and the matrices of \(p,q_0\) on
\(\operatorname{span}\{u,w\}\) are (2).  Choosing an orthonormal basis of
\(\operatorname{ran}p\ominus K\) gives mutually orthogonal copies of this
block.  Taking the ordinary trace of (1) first shows
\(c(\operatorname{rank}p-\operatorname{rank}q_0)=0\), so the two projections
have equal rank.  The constructed blocks therefore exhaust
\(\operatorname{ran}q_0\) as well.  What remains is orthogonal to both ranges
and is the common kernel.

The same result can also be read as the finite-dimensional Halmos
two-projection decomposition with the relation forcing the entire
principal-angle operator to equal \(cI\).  The argument above does not require
that theorem.

### Multiplicities at half rank

Write

\[
D=\dim\mathcal H,\quad
a=\dim(\operatorname{ran}p\cap\operatorname{ran}q_0),\quad
b=\dim(\ker p\cap\ker q_0),
\]

and let \(r\) be the number of generic two-dimensional blocks.  Then

\[
D=a+b+2r,\qquad \operatorname{rank}p=a+r.
\]

In the tensor-overlap problem \(D=d^3\) and
\(\operatorname{rank}p=D/2\), so

\[
b=a,\qquad r=\frac D2-a. \tag{5}
\]

At this purely abstract level \(a\) is not fixed.  In particular,

\[
\operatorname{Tr}(p q_0)
=a+cr
=\frac{cD}{2}+(1-c)a. \tag{6}
\]

This is an important assumption check: the two-projection relation and
half-rank condition alone do **not** imply the Markov value
\(\operatorname{Tr}(pq_0)=D/4\).

The exact verifier `scripts/verify_two_projection_blocks.py` constructs
dimension-eight half-rank examples with \(a=0,1,2\).  All satisfy (1), but
their values of \(\operatorname{Tr}(pq_0)\) are respectively
\(4/3,2,8/3\).  Only \(a=1\) has the Markov value.  These are abstract pairs,
not claims that the first and second projections have the tensor-overlap
form \(P\otimes I,I\otimes P\).

## 3. A canonical three-strand Clifford sector

Let \(f\) be the common-kernel projection and \(g=I-e-f\) the generic
central projection.  On \(g\mathcal H\), define

\[
U=\frac{p-q_0}{\sqrt{1-c}},\qquad
W=\frac{p+q_0-I}{\sqrt c}.
\]

Then

\[
U=U^*,\quad W=W^*,\quad U^2=W^2=I,\quad UW=-WU. \tag{7}
\]

The anticommutator vanishes by direct expansion, independently of (1); (4)
gives the two square identities on the generic sector.  Thus every solution
has a canonical representation of the complex Clifford algebra
\(\mathrm{Cl}_2(\mathbb C)\) on its generic three-strand sector.

This does not by itself force \(4\mid d\): a complex
\(\mathrm{Cl}_2\)-module only has even dimension, already accounted for by
the two-dimensional blocks.  Any claimed local-space Clifford obstruction
needs an additional argument that transports this three-strand structure to
\(V\) itself.

For \(c=1/3\),

\[
U=\sqrt{\frac32}(p-q_0),\qquad
W=\sqrt3(p+q_0-I)
\]

on \(g\mathcal H\).  The verifier checks these identities exactly on (2).

## 4. Standardness is automatic

This is the highest-leverage conclusion of the structural audit.

### Theorem 4.1

Every orthogonal projection \(P\) in the exceptional class automatically
satisfies

\[
\operatorname{Tr}_1P=\operatorname{Tr}_2P=\frac d2 I_d. \tag{8}
\]

No irreducibility, faithfulness, or Pauli-form hypothesis is needed.

### Proof

Define

\[
R=-P+q(I-P)=qI-(1+q)P,\qquad q=e^{i\pi/3}.
\]

The projection relation (1) is exactly the Yang--Baxter equation for \(R\).
Because \(P\) is orthogonal and \(|q|=1\), \(R\) is unitary with spectrum
\(\{-1,q\}\).  This spectrum contains no opposite pair: the only way
\(-1\) and \(q\) could be opposites is \(q=1\).

Lechner, Proposition 2.4, proves that a unitary Yang--Baxter matrix with no
opposite eigenvalue pair has irreducible shifted braid subfactor and hence
Markov character.  Proposition 2.3 identifies the Markov property exactly
with scalar normalized partial trace:

\[
\varphi(R)=\tau(R)I,\qquad
\varphi=\frac1d(\operatorname{Tr}\otimes\operatorname{id}).
\]

These hypotheses are all automatic here; this is also stated for
non-involutive Hecke matrices in Lechner, Lemma 3.1.

Let \(\eta=d^{-2}\operatorname{rank}P=1/2\).  Since

\[
\varphi(R)=qI-(1+q)\varphi(P),\qquad
\tau(R)=q-(1+q)\eta,
\]

and \(1+q\ne0\), scalarity gives

\[
\varphi(P)=\eta I=\frac12I.
\]

Therefore \((\operatorname{Tr}\otimes\operatorname{id})(P)=dI/2\).

For the other leg, let \(F(x\otimes y)=y\otimes x\) and
\(R^{\mathrm{op}}=FRF\).  Reversal of the three tensor factors conjugates
the Yang--Baxter equation for \(R\) to that for \(R^{\mathrm{op}}\).
It has the same spectrum, so the preceding argument applies.  Its first
partial trace is the second partial trace of \(R\), proving the other
identity in (8).

### What this proof does and does not use

The proof uses the established operator-algebraic criterion in Lechner
Propositions 2.3--2.4.  It does not assume scalar partial traces.  If a fully
self-contained follow-up paper is desired, the short subfactor argument in
those propositions can be reproduced with its cited relative-commutant
lemma; omitting that lemma would leave a gap.

The conclusion is stronger than needed: for any non-involutive unitary
Hecke \(R\)-matrix, its spectral projection has scalar partial traces
\(d\eta I\).  Rank half merely sets \(\eta=1/2\).

Equivalently, for \(H=I-2P\),

\[
\operatorname{Tr}_1H=\operatorname{Tr}_2H=0. \tag{9}
\]

### Finite-level Markov propagation and the trace quotient

Equation (8), rather than mere agreement of traces at two strands, gives the
Markov property at every level directly.  Let
\(\rho_n:H_n(q)\to\operatorname{End}(V^{\otimes n})\) be the local Hecke
representation and let
\(\tau_n=d^{-n}\operatorname{Tr}_{V^{\otimes n}}\).  For every
\(x\in H_n(q)\),

\[
\begin{aligned}
\tau_{n+1}\!\left(\rho_{n+1}(x)P_n\right)
&=d^{-(n+1)}
  \operatorname{Tr}\!\left[
    \rho_n(x)\,
    \operatorname{Tr}_{n+1}(P_n)
  \right]\\
&=\frac12\,\tau_n(\rho_n(x)).
\end{aligned} \tag{10}
\]

This proves propagation, not just a two-strand numerical match.

Let \(\mu_{1/2}\) denote the unique Hecke Markov trace with
\(\mu_{1/2}(e_1)=1/2\), and let

\[
\mathcal I_n=\{x:\mu_{1/2}(x^*x)=0\}
\]

be its trace radical at level \(n\).  Uniqueness of the Markov trace and
(10) give \(\tau_n\circ\rho_n=\mu_{1/2}\).  Faithfulness of the ordinary
matrix trace then gives both implications

\[
\rho_n(x)=0
\quad\Longleftrightarrow\quad
\mu_{1/2}(x^*x)=0,
\]

and hence

\[
\ker\rho_n=\mathcal I_n. \tag{11}
\]

Therefore every exceptional class solution faithfully represents the
finite trace quotient \(H_n(q)/\mathcal I_n\).  Once this quotient is
identified, with matching generator convention, as the Jones--Wenzl
\(H_n(3,6)\) sequence, the distinction between class existence and faithful
ordinary localization collapses for this particular family.  That
identification is a normalization step and should be stated explicitly in
any manuscript; it is not silently built into the abstract projection
argument.

## 5. Consequences for the three-strand blocks

From (8),

\[
\operatorname{Tr}(p q_0)
=\operatorname{Tr}\!\left[
  (\operatorname{Tr}_1P)(\operatorname{Tr}_2P)
\right]
=\frac{d^3}{4}. \tag{12}
\]

Combining (6), \(c=1/3\), and \(D=d^3\) gives

\[
a=b=\frac{d^3}{8},\qquad r=\frac{3d^3}{8}. \tag{13}
\]

Thus the three-strand decomposition consists of:

- \(d^3/8\) common-one dimensions;
- \(d^3/8\) common-zero dimensions;
- \(3d^3/8\) generic two-dimensional blocks.

Its only immediate arithmetic consequence is \(2\mid d\).  In particular,
for \(d=6\) the multiplicities are \(27,27,81\), all integral.  The complete
abstract two-projection analysis therefore supplies no divisibility-by-four
obstruction.

There is a stronger operator-valued form.  From (4) and (8),

\[
\operatorname{Tr}_3 e=\frac d4P,\qquad
\operatorname{Tr}_1 e=\frac d4P. \tag{14}
\]

The complementary projections \(I-p,I-q_0\) satisfy the same relation.
Writing \(f\) for their common-one projection, equivalently the common
kernel of \(p,q_0\), gives

\[
\operatorname{Tr}_3 f=\frac d4(I-P),\qquad
\operatorname{Tr}_1 f=\frac d4(I-P). \tag{15}
\]

Consequently

\[
\operatorname{Tr}_3 g=\operatorname{Tr}_1g=\frac{3d}{4}I_{V\otimes V}.
\tag{16}
\]

Equations (14)--(16) may be useful for iterating central projections at
higher strand number.

## 6. Raw partial-trace identities

These identities are valid before inserting automatic scalarity and are a
safe starting point for an elementary proof attempt.

Put

\[
A=\operatorname{Tr}_2P,\qquad B=\operatorname{Tr}_1P
\]

and define completely positive maps on \(\operatorname{End}(V)\) by

\[
\Phi_R(X)=\operatorname{Tr}_2\!\left[P(X\otimes I)P\right],
\qquad
\Phi_L(X)=\operatorname{Tr}_1\!\left[P(I\otimes X)P\right].
\]

Taking the third and first partial traces of (1), respectively, gives

\[
P(I\otimes A)P-(\operatorname{id}\otimes\Phi_R)(P)
=c(dP-I\otimes A), \tag{17}
\]

\[
(\Phi_L\otimes\operatorname{id})(P)-P(B\otimes I)P
=c(B\otimes I-dP). \tag{18}
\]

After (8), these reduce at \(c=1/3\) to

\[
(\operatorname{id}\otimes\Phi_R)(P)
=(\Phi_L\otimes\operatorname{id})(P)
=\frac d6(I+P). \tag{19}
\]

The normalized maps

\[
\mathcal E_R=\frac2d\Phi_R,\qquad
\mathcal E_L=\frac2d\Phi_L
\]

are bistochastic quantum channels: complete positivity is immediate,
\(\Phi_R(I)=A=dI/2\), \(\Phi_L(I)=B=dI/2\), and cyclicity of trace shows
that both scale the ordinary trace by \(d/2\).  Equation (19) becomes

\[
(\operatorname{id}\otimes\mathcal E_R)(P)
=(\mathcal E_L\otimes\operatorname{id})(P)
=\frac13(I+P). \tag{20}
\]

This channel eigen-relation is a potentially useful invariant formulation
of the overlap constraint.

## 7. Assumption ledger

| Statement | Inputs actually used |
|---|---|
| All generic principal angles have squared cosine \(1/3\) | Projection relation only |
| Common-one and common-zero multiplicities agree | Projection relation plus half rank |
| Scalar left and right partial traces | Tensor-overlap YBE, unitarity, non-opposite spectrum, Lechner Props. 2.3--2.4 |
| The common-one multiplicity is \(d^3/8\) | Previous row plus rank half |
| Canonical \(\mathrm{Cl}_2(\mathbb C)\) action on the generic three-strand sector | Projection relation only |
| Divisibility by four | **Not obtained** |
| Faithful representation of the trace quotient | Derived from standardness, Markov uniqueness, and faithful matrix trace; identification with the named Jones--Wenzl quotient requires the convention check |

## 8. Exact warning against a naive local direct sum

One tempting route to \(d=6\) is to decompose the local space as
\(V=V_4\oplus V_2\) and use the known \(d=4\) braiding on
\(V_4\otimes V_4\), with ordinary cross-braid maps between the two colors.
The most direct version of this cannot have the exceptional spectrum.

Indeed, if a unitary \(R\) exchanges the two mixed sectors

\[
V_4\otimes V_2\quad\text{and}\quad V_2\otimes V_4
\]

without diagonal components, its restriction to their sum has the form

\[
\begin{pmatrix}0&A\\B&0\end{pmatrix}.
\]

Conjugation by \(\operatorname{diag}(I,-I)\) negates this matrix, so its
spectrum is invariant under \(\lambda\mapsto-\lambda\).  A nonzero unitary
mixed sector therefore contains opposite eigenvalue pairs.  The target
spectrum \(\{-1,e^{i\pi/3}\}\) contains no opposite pair.

Thus an additive construction, if one exists, must use genuinely coupled
diagonal and off-diagonal mixed-sector terms; the usual purely exchanging
braided direct sum cannot work.  This does not rule out a sophisticated
local direct-sum construction.

## 9. Implications and next structural target

1. The program's standard/nonstandard dichotomy collapses: the nonstandard
   branch is empty for this exceptional unitary Hecke class.
2. Markov-trace and Jones--Wenzl representation data may therefore be used
   for every candidate, provided the propagation/factorization argument is
   stated rather than assumed.
3. Three-strand block integrality only recovers that \(d\) is even.  A
   \(4\mid d\) obstruction, if true, must first appear at four or more
   strands or use tensor locality more deeply than abstract principal angles.
4. The natural next calculation is the rank and partial trace of the
   four-strand central idempotents obtained by extending \(e,f,g\), followed
   by their exact multiplicity denominators as functions of \(d\).
