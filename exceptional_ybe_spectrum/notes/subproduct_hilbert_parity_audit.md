# Quadratic subproduct ranks do not force four-divisibility

**Date:** 2026-07-29
**Scope:** arbitrary exceptional projection for the universal statements;
exact non-Yang--Baxter projections for the limitation statements
**Status:** exact rank and Hilbert-series theorem, two exact limitation
models, and a sharp remaining locality gap

## 1. Conclusion

Let \(d=2s\), and for a two-site projection \(P\) define

\[
\mathcal E_n
=\bigcap_{i=1}^{n-1}\operatorname{ran}P_{i,i+1},
\qquad
\mathcal F_n
=\bigcap_{i=1}^{n-1}\ker P_{i,i+1}.
\tag{1}
\]

For every exceptional solution,

\[
\begin{array}{c|ccccc}
n&0&1&2&3&n\geq4\\ \hline
\dim\mathcal E_n&1&2s&2s^2&s^3&0\\
\dim\mathcal F_n&1&2s&2s^2&s^3&0.
\end{array}
\tag{2}
\]

The \(1/3\)-principal-angle half of the generic three-site sector has
dimension

\[
3s^3.
\tag{3}
\]

Both \(s^3\) and \(3s^3\) are divisible by the local dimension \(2s\)
exactly when \(s\) is even.  This makes divisibility of either space by
\(d\) look like a possible route to \(4\mid d\).  The present audit shows
that none of the following supplies that divisibility:

1. the dimensions in (2);
2. associativity of the corresponding quadratic algebra;
3. finite termination at degree four;
4. the ordinary Koszul or connected graded Frobenius conditions;
5. rank half, two scalar partial traces, and
   \(\mathcal E_4=0\), without the exceptional cubic.

There is an exact tensor-local quadratic subproduct system with precisely
the common-one Hilbert function in the first row of (2) for **every**
\(s\geq1\), including odd \(s\).  It has only one scalar two-site partial
trace and does not satisfy the exceptional cubic.  Its complementary
subproduct system is not asserted to have the second row of (2).

There is also an exact rank-half projection on
\(\mathbb C^4\otimes\mathbb C^4\) with **both** scalar partial traces,
\[
\dim\mathcal E_3=2\not\equiv0\pmod4,
\qquad
\mathcal E_4=0.
\tag{4}
\]
It too fails the exceptional cubic.  Thus even full standardness and
four-step nilpotence do not make an intersection rank a multiple of the
local dimension.

The surviving possibility is narrower:

> repeated tensor placement of one fully standard \(P\), together with
> the exact exceptional \(1/3\)-angle relation, might impose a
> divisibility theorem.

That statement is essentially the unresolved matrix problem.  It does
not follow from quadratic-Hilbert-space structure alone.

## 2. Forced exceptional subproduct data

Write

\[
p=P_{12},\qquad q=P_{23},\qquad r=P_{34}.
\]

Automatic standardness gives

\[
\operatorname{Tr}_1P
=\operatorname{Tr}_2P
=sI_{2s}.
\tag{5}
\]

The common-one and common-zero three-site projections are

\[
e
=\frac32pqp-\frac12p,
\tag{6}
\]

\[
f
=\frac32(1-p)(1-q)(1-p)-\frac12(1-p).
\tag{7}
\]

They project onto \(\mathcal E_3\) and \(\mathcal F_3\), respectively.
The two-projection calculation and normalized Markov trace give

\[
\operatorname{rank}e
=\operatorname{rank}f
=\frac{d^3}{8}
=s^3.
\tag{8}
\]

The four-site compression theorem gives

\[
ere=\frac12e.
\tag{9}
\]

If \(\xi\in\mathcal E_4\), then \(e\xi=\xi\) and \(r\xi=\xi\), so (9)
would give both

\[
ere\xi=\xi
\quad\text{and}\quad
ere\xi=\frac12\xi.
\]

Hence \(\xi=0\), proving \(\mathcal E_4=0\).  The complementary identity

\[
f(1-r)f=\frac12f
\]
proves \(\mathcal F_4=0\).  Every higher intersection is contained in
the corresponding four-site intersection, so it also vanishes.  This
proves (2).

### 2.1 Exact partial traces

The two-site projector has the partial traces (5).  The outer
contractions of \(e\) are

\[
\boxed{
\operatorname{Tr}_3e=\frac{s}{2}P_{12},
\qquad
\operatorname{Tr}_1e=\frac{s}{2}P_{23}.
}
\tag{10}
\]

Tracing any two tensor factors gives

\[
\boxed{
\operatorname{Tr}_{ij}e=\frac{s^2}{2}I_{2s}
}
\qquad(1\leq i<j\leq3).
\tag{11}
\]

For \(f\),

\[
\operatorname{Tr}_3f=\frac{s}{2}(I-P_{12}),
\qquad
\operatorname{Tr}_1f=\frac{s}{2}(I-P_{23}),
\tag{12}
\]
and its two-site contractions are again \(s^2I/2\).

The middle one-site removal

\[
K=\operatorname{Tr}_2e
\in\operatorname{End}(V_1\otimes V_3)
\tag{13}
\]
is not known to be scalar.  Universally,

\[
K\geq0,\qquad
\operatorname{Tr}K=s^3,\qquad
0\leq K\leq sI,
\tag{14}
\]

\[
\operatorname{Tr}_1K
=\operatorname{Tr}_3K
=\frac{s^2}{2}I_{2s}.
\tag{15}
\]

The same statements hold for \(\operatorname{Tr}_2f\).  In particular,
one must not replace the middle marginal by a scalar in a general
subproduct argument.

### 2.2 The \(1/3\)-angle multiplicity

Equation (6) rearranges to

\[
pqp=e+\frac13(p-e).
\tag{16}
\]

Thus the \(1/3\)-eigenspace of \(pqp\) inside \(\operatorname{ran}p\)
has projection

\[
a=p-e
\tag{17}
\]
and rank

\[
\operatorname{rank}a
=\frac{d^3}{2}-\frac{d^3}{8}
=3s^3.
\tag{18}
\]

For reference, two of its partial traces are

\[
\operatorname{Tr}_3a=\frac{3s}{2}P_{12},
\tag{19}
\]

\[
\operatorname{Tr}_1a
=sI_{23}-\frac{s}{2}P_{23}.
\tag{20}
\]

The shifted projection \(q-e\) has the same rank.  The abstract
two-projection algebra permits arbitrary multiplicity of its generic
\(2\times2\) block; in particular, the exact odd-multiplicity model in
the overlap/Kramers audit has multiplicity \(81\).  That model is not
tensor-local.  Therefore it closes an abstract block-divisibility
argument, but not a theorem using the common placement
\(p=P\otimes I,\ q=I\otimes P\).

## 3. Exact exceptional-shaped systems for every \(s\)

This section shows that associativity and either abstract Hilbert
function appearing in (2) do not see the parity of \(s\).

Let \(A=\mathbb C^2\), put

\[
u_0=|0\rangle,\qquad
u_1=|+\rangle
=\frac{|0\rangle+|1\rangle}{\sqrt2},
\]
and define

\[
W
=\operatorname{span}
\left\{
u_0\otimes|1\rangle,\,
u_1\otimes|0\rangle
\right\}
\subset A\otimes A.
\tag{21}
\]

Let \(Q\) be its orthogonal projection.  Its two spanning vectors are
orthonormal, so \(\operatorname{rank}Q=2\).  Direct contraction gives

\[
\operatorname{Tr}_1Q=I_2,
\tag{22}
\]

\[
\operatorname{Tr}_2Q
=
\begin{pmatrix}
3/2&1/2\\
1/2&1/2
\end{pmatrix}
\neq I_2.
\tag{23}
\]

Thus exactly one marginal is scalar.  We call this **one-sided
standard** only as shorthand for (22); it is not standard in the
exceptional sense, which requires both partial traces to be scalar.

The only product-vector lines in \(W\) are the two displayed in (21).
It follows immediately that

\[
(W\otimes A)\cap(A\otimes W)
=\mathbb C
\left(
|+\rangle\otimes|0\rangle\otimes|1\rangle
\right).
\tag{24}
\]

The last two factors of the vector in (24) can lie in \(W\), but its
third factor \(|1\rangle\) cannot be the first factor of either product
line in (21).  Consequently

\[
\mathcal E_1(Q)=A,\qquad
\dim\mathcal E_2(Q)=2,\qquad
\dim\mathcal E_3(Q)=1,\qquad
\mathcal E_4(Q)=0.
\tag{25}
\]

Now take any \(s\)-dimensional Hilbert space \(K\), set

\[
V=A\otimes K,
\]
and, after the sitewise tensor-coordinate shuffle, define

\[
P_s=Q\otimes I_{K\otimes K}.
\tag{26}
\]

On \(n\) sites the constraints regroup as

\[
(P_s)_i=Q_i\otimes I_{K^{\otimes n}}.
\]
Therefore

\[
\boxed{
\mathcal E_n(P_s)
=\mathcal E_n(Q)\otimes K^{\otimes n}.
}
\tag{27}
\]

Equations (25)--(27) give

\[
\dim\mathcal E_1=2s,\qquad
\dim\mathcal E_2=2s^2,\qquad
\dim\mathcal E_3=s^3,\qquad
\mathcal E_n=0\ (n\geq4)
\tag{28}
\]
for every positive integer \(s\).

The partial traces are

\[
\operatorname{Tr}_1P_s=sI_{2s},
\tag{29}
\]

\[
\operatorname{Tr}_2P_s
=s
\begin{pmatrix}
3/2&1/2\\
1/2&1/2
\end{pmatrix}
\otimes I_s.
\tag{30}
\]

So this construction deliberately misses full standardness.  It also
misses the exceptional cubic: at \(s=1\),

\[
\left\|
Q_{12}Q_{23}Q_{12}
-Q_{23}Q_{12}Q_{23}
-\frac13(Q_{12}-Q_{23})
\right\|_{\mathrm{HS}}^2
=\frac{13}{36}.
\tag{31}
\]

After spectator amplification, the squared residual is
\(13s^3/36\).  This is not an \(R\)-matrix construction.  Its exact
content is that the exceptional-shaped subproduct dimensions and their
associativity permit odd \(s\).

## 4. Full standardness still does not make intersection ranks divisible

We next impose both scalar partial traces, while continuing not to impose
the cubic.

Use the same \(W\subset A\otimes A\) as in (21), and introduce a
two-dimensional color space \(C\).  The local space is

\[
V=C\otimes A\cong\mathbb C^4.
\]

Let \(X,Y,Z\) be the Pauli matrices and put

\[
C_0=\frac{X+Z}{\sqrt2},
\tag{32}
\]

\[
K_0
=\frac1{\sqrt2}
\left(
Y+\frac{X-Z}{\sqrt2}
\right),
\tag{33}
\]

\[
L=\frac{I-iX}{\sqrt2}.
\tag{34}
\]

These obey

\[
C_0^2=K_0^2=I,\qquad
K_0C_0=-C_0K_0,\qquad
L^*L=I.
\tag{35}
\]

Define four qubit unitaries

\[
U_{00}=I,\qquad
U_{01}=K_0,\qquad
U_{10}=L,\qquad
U_{11}=LK_0.
\tag{36}
\]

On the color block \((a,b)\), let

\[
W_{ab}=(U_{ab}\otimes I)W,
\]
and define

\[
\widetilde W
=
\bigoplus_{a,b\in\{0,1\}}
\left(
|a\rangle_C\otimes|b\rangle_C
\right)\otimes W_{ab},
\tag{37}
\]
with the factors reordered sitewise as
\((C\otimes A)\otimes(C\otimes A)\).  Let \(\widetilde P\) be the
orthogonal projection onto \(\widetilde W\).

Each color block has rank two, so

\[
\operatorname{rank}\widetilde P=8=\frac{4^2}{2}.
\tag{38}
\]

The nonscalar part of \(\operatorname{Tr}_2Q\) is
\((X+Z)/2=C_0/\sqrt2\).  Since the two unitaries in each row of (36)
differ on the right by \(K_0\), equation (35) makes their nonscalar
parts cancel.  On the other leg, every block already has partial trace
\(I_2\).  Hence

\[
\boxed{
\operatorname{Tr}_1\widetilde P
=\operatorname{Tr}_2\widetilde P
=2I_4.
}
\tag{39}
\]

This is full two-sided standardness.

For a fixed color triple \((a,b,c)\), the dimension of

\[
(W_{ab}\otimes A)\cap(A\otimes W_{bc})
\]
is the number of \(j\in\{0,1\}\) for which
\(U_{bc}u_j\) is proportional to a computational basis vector.  The
following table records the product of the two coordinates; it vanishes
exactly for such a vector:

\[
\begin{array}{c|cc}
U&(Uu_0)_0(Uu_0)_1&(Uu_1)_0(Uu_1)_1\\ \hline
I&0&1/2\\
K_0&-(1+i\sqrt2)/4&(1-i\sqrt2)/4\\
L&-i/2&-i/2\\
LK_0&\sqrt2/4&\sqrt2/4.
\end{array}
\tag{40}
\]

Thus only \((b,c)=(0,0)\) contributes, and it contributes one dimension
for each of the two choices of the outer color \(a\).  Therefore

\[
\boxed{\dim\mathcal E_3(\widetilde P)=2.}
\tag{41}
\]

In particular, \(4\nmid\dim\mathcal E_3\).

The two surviving three-site vectors have third qubit \(|1\rangle\).
For the possible next color \(d\), neither
\(U_{0d}u_0\) nor \(U_{0d}u_1\) is proportional to \(|1\rangle\).
No fourth-site extension exists, and hence

\[
\boxed{\mathcal E_4(\widetilde P)=0.}
\tag{42}
\]

The exact exceptional-cubic residual is nevertheless nonzero:

\[
\left\|
\widetilde P_{12}\widetilde P_{23}\widetilde P_{12}
-\widetilde P_{23}\widetilde P_{12}\widetilde P_{23}
-\frac13(\widetilde P_{12}-\widetilde P_{23})
\right\|_{\mathrm{HS}}^2
=\frac{95}{36}.
\tag{43}
\]

So (37) is a fully standard tensor-local quadratic subproduct system,
not an exceptional Yang--Baxter solution.  It proves exactly that
standardness, balance, and \(\mathcal E_4=0\) do not imply divisibility
of \(\dim\mathcal E_3\) by \(d\).

## 5. The ordinary Koszul and Frobenius routes are unavailable

Let \(\mathcal A(P)\) be the quadratic algebra whose relation space is
\((\operatorname{ran}P)^\perp\).  Its degree-\(n\) dual identifies with
\(\mathcal E_n\).  For an exceptional projection its Hilbert series is

\[
h_{\mathcal A}(t)
=1+2st+2s^2t^2+s^3t^3.
\tag{44}
\]

For the base model (21), writing \(x,y\) for the basis dual to
\(|0\rangle,|1\rangle\), the relations can be taken as

\[
x^2-yx=0,\qquad y^2=0.
\tag{45}
\]

They give the dimensions \(1,2,2,1,0,\ldots\) directly.  This is an
ordinary associative quadratic algebra, so (45) is also a concrete
algebraic countermodel to any parity claim based only on associativity.

If an algebra with Hilbert series (44) were Koszul, its quadratic dual
would satisfy

\[
h_{\mathcal A^!}(t)
=\frac1{h_{\mathcal A}(-t)}
=\frac1{1-2st+2s^2t^2-s^3t^3}.
\tag{46}
\]

The first coefficients are

\[
\boxed{
1,\ 2s,\ 2s^2,\ s^3,\ 0,\ 0,\ s^6,\ldots
}
\tag{47}
\]

A graded algebra generated in degree one cannot have zero degree-four
part and then a nonzero degree-six part.  Therefore:

\[
\boxed{\mathcal A(P)\text{ is not Koszul for any }s\geq1.}
\tag{48}
\]

This includes the published \(s=2\) exceptional witness.  Koszulity is
not an automatic extra structure waiting to impose parity; it is
incompatible with the already-proved Hilbert series.

Likewise, an ordinary connected finite-dimensional graded Frobenius
algebra concentrated in degrees \(0,\ldots,3\) has a palindromic Hilbert
function.  Applied to (44), this would require

\[
1=s^3,\qquad 2s=2s^2,
\]
so \(s=1\).  The known exceptional solution has \(s=2\), proving that
this ordinary Frobenius notion is also not automatic.  A Frobenius
object over a nontrivial semisimple base, a \(Q\)-system, or a
correspondence-valued duality would be a different and substantially
stronger structure; it must first be constructed from \(P\), not
silently assumed.

## 6. What remains open

This audit separates three increasingly strong packages:

1. **Quadratic subproduct data.**
   The dimensions \(2s,2s^2,s^3,0\) occur for every \(s\).

2. **Full standardness and termination.**
   Even these do not make the common-one rank divisible by \(d\), as
   (37)--(43) show.

3. **Full exceptional tensor locality.**
   Here \(P\) is fully standard and the adjacent copies satisfy the
   exact \(1/3\)-angle cubic.  Whether this forces
   \(2s\mid s^3\), equivalently \(2\mid s\), remains open.

The third package cannot be reduced to the first two by a Hilbert-series,
Koszul, or ordinary Frobenius argument.  A successful proof must extract
new structure from the exact overlap maps, not only from the dimensions
of their intersections.

## 7. Exact replay

Run

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_subproduct_hilbert_parity_audit.py
```

The verifier independently constructs both projections over
\(\mathbb Q(\sqrt2,i)\), checks ranks, partial traces, the three- and
four-site intersections, and the nonzero cubic residuals.  It also
replays the Koszul-dual coefficient recurrence through degree six.
