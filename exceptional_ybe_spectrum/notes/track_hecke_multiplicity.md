# Track A: Markov trace and Hecke-tower multiplicities

Date: 2026-07-28
Status: **PROVED** (source hypotheses audited; exact arithmetic replayed)

## Executive conclusion

Two structural facts hold for an *arbitrary* matrix-class solution, with no
extra standardness or faithfulness hypothesis.

1. Scalar partial traces are automatic:
   \[
   \operatorname{Tr}_1(P)=\operatorname{Tr}_2(P)=\frac d2 I_d.
   \]
2. The multiplicity of every simple \(H_n(3,6)\)-module in
   \(V^{\otimes n}\) is forced to be
   \[
   \boxed{m_{\lambda,n}=D_\lambda\left(\frac d2\right)^n},
   \]
   where \(D_\lambda\in\{1,2,3\}\) is the
   \(\mathcal C(\mathfrak{sl}_3,6)\) quantum dimension attached to
   \(\lambda\).

It follows that **all central-idempotent ranks, all simple-block
multiplicities, and all inclusion recurrences are integral for every even
\(d\)**.  Conversely, the two-strand rank already requires \(d\) to be
even.  Thus representation-multiplicity arithmetic imposes exactly
\(2\mid d\), not \(4\mid d\), at every strand.

In particular, \(d=6\) passes the complete Hecke-tower arithmetic test.  This
does not construct a local Yang--Baxter matrix in dimension six.  It proves
that no divisibility-by-four theorem can come solely from the Markov weights,
central-idempotent ranks, simple-module multiplicities, or their branching
recurrences.

## 1. Normalization and automatic Markov property

Let
\[
q=e^{i\pi/3},\qquad
R=qI-(1+q)P,
\]
where \(P\) is an orthogonal projection of rank \(d^2/2\), and suppose that
\(R\) satisfies the braid-form Yang--Baxter equation.

The following implications use exactly the hypotheses above.

- The spectrum is \(\{-1,q\}\), and it contains no opposite pair because
  \(q\ne\pm1\).
- Lechner, Proposition 2.4, therefore applies: the associated subfactor
  inclusion is irreducible and the tensor-space character is Markov.
- Equivalently, Lechner, Lemma 3.1, states directly that every
  \(R\in\mathcal R_q\), \(q\ne\pm1\), has a positive Markov trace on
  \(H_\infty(q)\).
- Its parameter is
  \[
  \eta=\tau(P)=\frac{\operatorname{rank}P}{d^2}=\frac12.
  \]
- Lechner's equation (3.2) gives
  \[
  \eta_{6,3}
  =
  \frac{\sin(2\pi/6)}
       {2\cos(\pi/6)\sin(3\pi/6)}
  =\frac12,
  \]
  identifying this trace with the trace defining \(H_n(3,6)\).

This argument is independent of scalar partial traces; indeed, it proves
them next.

## 2. Automatic scalar partial traces

Lechner, Proposition 2.3, states that the tensor-space character is Markov
if and only if the normalized first partial trace satisfies
\[
\varphi(R)=\tau(R)I_d,\qquad
\varphi=\frac1d(\operatorname{Tr}\otimes\operatorname{id}).
\]
Since
\[
\tau(R)=q-(1+q)\eta
\]
and \(R=qI-(1+q)P\), comparison gives
\[
qI-(1+q)\varphi(P)
=
\bigl(q-(1+q)\eta\bigr)I.
\]
Because \(q\ne-1\),
\[
\varphi(P)=\eta I=\frac12I.
\]
Hence
\[
(\operatorname{Tr}\otimes\operatorname{id})(P)=\frac d2I_d.
\]

The other partial trace is the same.  This is quoted in Lechner's footnote
to Proposition 2.3 from Conti--Lechner, Theorem 5.10.  It also follows by
applying the preceding argument to \(FRF\), where \(F\) is tensor flip:
global reversal of three tensor factors shows that \(FRF\) is again a
unitary braid-form Yang--Baxter matrix, and its first partial trace is the
second partial trace of \(R\).  Therefore
\[
\boxed{
\operatorname{Tr}_1(P)=\operatorname{Tr}_2(P)=\frac d2I_d.
}
\]

Thus “standardness” in the scalar-partial-trace sense is automatic for the
entire exceptional matrix class.  No irreducibility of the finite-dimensional
matrix representation was assumed; the needed irreducibility is the
subfactor conclusion supplied by the no-opposite-eigenvalue theorem.

## 3. The quotient is represented faithfully for every solution

Let
\[
\rho_n:H_n(q)\longrightarrow\operatorname{End}(V^{\otimes n})
\]
be the tensor-space representation, and let
\(\tau_n=d^{-n}\operatorname{Tr}\).  Section 1 shows
\[
\tau_n\circ\rho_n=\mu_{1/2},
\]
the unique Markov trace with \(\mu_{1/2}(e_1)=1/2\).

Write
\[
\operatorname{Ann}_n
=
\{x:\mu_{1/2}(yx)=0\text{ for all }y\in H_n(q)\}.
\]
If \(x\in\operatorname{Ann}_n\), take \(y=x^*\):
\[
0=\mu_{1/2}(x^*x)
=\tau_n\!\left(\rho_n(x)^*\rho_n(x)\right).
\]
Faithfulness of ordinary matrix trace implies \(\rho_n(x)=0\).  The reverse
inclusion is immediate.  Hence
\[
\ker\rho_n=\operatorname{Ann}_n
\]
and every solution induces a faithful representation of
\[
H_n(3,6)=H_n(q)/\operatorname{Ann}_n.
\]

This proves the trace and faithfulness propagation at every level; it does
not infer it from two-strand trace agreement alone.

## 4. Simple modules and the admissible Young graph

Wenzl's description, recalled explicitly in Rowell's Section 2, labels the
simple \(H_n(3,6)\)-modules by partitions
\[
\lambda=(\lambda_1,\lambda_2,\lambda_3)\vdash n
\]
such that
\[
\lambda_1\ge\lambda_2\ge\lambda_3\ge0,
\qquad
\lambda_1-\lambda_3\le3.
\]
Branching is by adding one box while preserving admissibility.  If
\[
a=\lambda_1-\lambda_2,\qquad
b=\lambda_2-\lambda_3,
\]
then \((a,b)\) belongs to the ten-point alcove
\[
a,b\ge0,\qquad a+b\le3.
\]
The admissible successors are
\[
(a+1,b)\quad(a+b<3),\qquad
(a-1,b+1)\quad(a>0),\qquad
(a,b-1)\quad(b>0).
\]

The quantum dimensions are
\[
D_{a,b}
=
\frac{
\sin((a+1)\pi/6)\,
\sin((b+1)\pi/6)\,
\sin((a+b+2)\pi/6)}
{\sin(\pi/6)^2\sin(2\pi/6)}.
\]
They reduce exactly to
\[
\begin{array}{c|c}
D_{a,b}&(a,b)\\ \hline
1&(0,0),(3,0),(0,3)\\
3&(1,1)\\
2&(1,0),(0,1),(2,0),(0,2),(2,1),(1,2).
\end{array}
\]
Direct case checking on the ten-point graph gives the
Perron--Frobenius relation
\[
\sum_{\nu:\lambda\nearrow\nu}D_\nu=2D_\lambda.
\]

Let \(f_{\lambda,n}\) be the number of admissible paths from the empty
diagram to \(\lambda\); this is the dimension of the simple module
\(S_{\lambda,n}\).  The Wenzl trace formula, equivalently the categorical
trace under
\[
H_n(3,6)\cong
\operatorname{End}_{\mathcal C}(X^{\otimes n}),
\qquad \operatorname{FPdim}(X)=2,
\]
assigns a minimal projection in the \(\lambda\)-block the trace
\[
t_{\lambda,n}=\frac{D_\lambda}{2^n}.
\]
The formula is also verified intrinsically by the branching identity
\[
t_{\lambda,n}
=\sum_{\nu:\lambda\nearrow\nu}t_{\nu,n+1},
\]
which is exactly the preceding Perron--Frobenius relation divided by
\(2^{n+1}\).  Consequently, the central identity of that block has trace
\[
\mu_{1/2}(z_{\lambda,n})
=f_{\lambda,n}\frac{D_\lambda}{2^n}.
\]

## 5. Forced tensor-space multiplicities

Decompose the faithful semisimple representation as
\[
V^{\otimes n}
\cong
\bigoplus_{\lambda}
S_{\lambda,n}\otimes\mathbb C^{m_{\lambda,n}}.
\]
A minimal projection in
\(\operatorname{End}(S_{\lambda,n})\) has ordinary matrix rank
\(m_{\lambda,n}\).  Its normalized matrix trace is therefore
\[
\frac{m_{\lambda,n}}{d^n}.
\]
Equating this with \(t_{\lambda,n}=D_\lambda/2^n\) proves
\[
\boxed{
m_{\lambda,n}
=
D_\lambda\left(\frac d2\right)^n.
}
\]

The formula automatically obeys the restriction recurrence required by
\(V^{\otimes(n+1)}\cong V^{\otimes n}\otimes V\):
\[
\begin{aligned}
\sum_{\nu:\lambda\nearrow\nu}m_{\nu,n+1}
&=
\left(\frac d2\right)^{n+1}
\sum_{\nu:\lambda\nearrow\nu}D_\nu\\
&=
\left(\frac d2\right)^{n+1}2D_\lambda\\
&=d\,m_{\lambda,n}.
\end{aligned}
\]
Thus there is no hidden extra divisibility condition in the tower
inclusions.

If \(d\) is even, every \(m_{\lambda,n}\) is a nonnegative integer for every
\(n\).  If \(d\) is odd, already at \(n=2\),
\[
m_{\lambda,2}=2(d/2)^2=d^2/2
\]
is not an integer.  Therefore:
\[
\boxed{
\text{all Hecke-tower multiplicity and central-rank constraints}
\iff 2\mid d.
}
\]

## 6. Low-strand table

Here \(f_\lambda=\dim S_{\lambda,n}\).  The full replayable output continues
through arbitrary requested strand number.

| \(n\) | admissible \(\lambda\) | \(f_\lambda\) | \(D_\lambda\) | \(\mu(z_\lambda)\) | \(m_{\lambda,n}\) |
|---:|---|---:|---:|---:|---:|
| 1 | (1,0,0) | 1 | 2 | 1 | \(2(d/2)\) |
| 2 | (2,0,0) | 1 | 2 | 1/2 | \(2(d/2)^2\) |
| 2 | (1,1,0) | 1 | 2 | 1/2 | \(2(d/2)^2\) |
| 3 | (3,0,0) | 1 | 1 | 1/8 | \((d/2)^3\) |
| 3 | (2,1,0) | 2 | 3 | 3/4 | \(3(d/2)^3\) |
| 3 | (1,1,1) | 1 | 1 | 1/8 | \((d/2)^3\) |
| 4 | (3,1,0) | 3 | 2 | 3/8 | \(2(d/2)^4\) |
| 4 | (2,2,0) | 2 | 2 | 1/4 | \(2(d/2)^4\) |
| 4 | (2,1,1) | 3 | 2 | 3/8 | \(2(d/2)^4\) |
| 5 | (3,2,0) | 5 | 2 | 5/16 | \(2(d/2)^5\) |
| 5 | (3,1,1) | 6 | 2 | 3/8 | \(2(d/2)^5\) |
| 5 | (2,2,1) | 5 | 2 | 5/16 | \(2(d/2)^5\) |
| 6 | (4,1,1) | 6 | 1 | 3/32 | \((d/2)^6\) |
| 6 | (3,3,0) | 5 | 1 | 5/64 | \((d/2)^6\) |
| 6 | (3,2,1) | 16 | 3 | 3/4 | \(3(d/2)^6\) |
| 6 | (2,2,2) | 5 | 1 | 5/64 | \((d/2)^6\) |

For \(d=6\), these multiplicities are
\[
m_{\lambda,n}=D_\lambda\,3^n,
\]
which are positive integers at every level and satisfy every branching
recurrence exactly.

## 7. Strictification reformulation

Put \(d=2s\).  Define the canonical categorical module
\[
\mathcal M_n
=
\bigoplus_\lambda
S_{\lambda,n}\otimes\mathbb C^{D_\lambda}.
\]
Its dimension is
\[
\sum_\lambda f_{\lambda,n}D_\lambda=2^n.
\]
The forced multiplicity formula gives an abstract
\(H_n(3,6)\)-module equivalence
\[
V^{\otimes n}
\cong
\mathcal M_n\otimes\mathbb C^{s^n}.
\]

This equivalence is only levelwise/tower-theoretic; it does not respect a
chosen strict tensor-factorization automatically.  It nevertheless isolates
the remaining problem sharply.  The known categorical quasi-localization
has local categorical dimension \(2\).  An ordinary solution of dimension
\(d=2s\) is a strict local realization after an \(s\)-dimensional ancilla at
each site.  The published \(d=4\) construction proves that \(s=2\) works,
whereas the first open case \(d=6\) asks whether \(s=3\) works.

Therefore, if a \(4\mid d\) theorem is true, its extra factor of two must
come from a coherence, associator, module-category, Brauer-class, or spatial
overlap obstruction to this strictification.  It cannot come from the
abstract semisimple tower.

## 8. Replay instructions

Run:

```text
python3 scripts/hecke_multiplicity_spectrum.py \
  --max-strand 18 --test-d-through 40
```

The program uses only Python integers and `fractions.Fraction`.  It:

1. enumerates every \((3,6)\)-admissible Young diagram through level 18;
2. computes every admissible path count;
3. verifies the quantum-dimension recursion;
4. verifies that central Markov weights sum to one;
5. verifies that represented block dimensions sum to \(d^n\) for
   \(d=2,4,6\);
6. checks all candidate \(d\le40\), finding integral multiplicities exactly
   for even \(d\).

An independent cross-check does not enumerate partitions or use add-a-box
logic.  It iterates an explicitly entered ten-vertex
\(\mathcal C(\mathfrak{sl}_3,6)\) fusion graph:

```text
python3 scripts/hecke_fusion_graph_crosscheck.py \
  --max-strand 60 --test-d-through 100
```

It independently verifies the Perron--Frobenius dimension vector, path
dimensions, Markov normalization, represented dimensions for
\(d=2,4,6\), and the exact evenness condition.

The finite run checks the implementation.  The displayed formula and
Perron--Frobenius proof establish the statement for all \(n\).

## 9. Sources and convention audit

- Gandalf Lechner, *The classification problem for unitary R-Matrices with
  two eigenvalues*, arXiv:2603.20158v1:
  Proposition 2.3, Proposition 2.4, Lemma 3.1, equation (3.2), and
  Theorem 3.4.
- Hans Wenzl, *Hecke algebras of type \(A_n\) and subfactors* (1988):
  semisimple quotients, admissible Young diagrams, and Markov trace.
- Eric C. Rowell, *A quaternionic braid representation (after Goldschmidt
  and Jones)*, arXiv:1006.4808:
  Section 2 explicitly recalls the \((k,\ell)\)-admissibility condition;
  Section 3 identifies \(\eta=1/2\) for \((3,6)\); Section 4 records the ten
  simple dimensions \(1,2,3\).
- César Galindo, Seung-Moon Hong, and Eric C. Rowell, *Generalized and
  quasi-localizations of braid group representations* (2012/2013):
  Section 5.6 and Theorem 5.28 identify the same \(H_n(3,6)\) trace quotient
  and its generalized localization.

Convention warning: GHR contains inconsistent printed powers of \(q\) in
nearby prose/formulas.  The audited normalization here is Lechner's:
\[
q=e^{i\pi/3},\qquad
R=-P+q(I-P),\qquad
\eta=\tau(P)=1/2.
\]

## 10. What this does and does not settle

Proved:

- scalar partial traces are automatic for every exceptional solution;
- every solution faithfully represents the \(H_n(3,6)\) quotient;
- all low- and high-strand representation multiplicities are fixed;
- their complete arithmetic obstruction is only evenness.

Not proved:

- existence at \(d=6\);
- existence in every even dimension;
- that an abstract compatible tower representation comes from a single
  local operator \(R\);
- nonexistence in dimensions \(d\equiv2\pmod4\).

The remaining obstruction, if there is one, must use the *spatial tensor
overlap/locality* of \(P_{12}\) and \(P_{23}\), not just the abstract
\(H_n(3,6)\)-module structure.
