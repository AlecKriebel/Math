# Leg commutants do not close the odd-ancilla branch

**Date:** 2026-07-28
**Status:** PROVED assumption audit; no unrestricted \(d=6\) existence or
nonexistence theorem
**Scope:** arbitrary exceptional solutions for the necessary statements;
exact abstract and non-Yang--Baxter countermodels for the insufficiency
statements

## 1. Executive conclusion

Let \(d=2s\) with \(s\) odd, and suppose that an exceptional projection
\[
P=P^*=P^2\in\operatorname{End}(V\otimes V)
\]
exists.  The odd-leg-projection theorem already proves that every minimal
projection in either one-leg commutant has even ordinary rank.

This note tests whether the remaining finite-dimensional possibilities can
be excluded by:

- low- or high-strand central-idempotent ranks;
- one-sided inclusions in the \(H_n(3,6)\) tower;
- simultaneous left/right endpoint bimodule multiplicities;
- scalar one-leg commutants;
- factor commutants \(M_k(\mathbb C)\otimes I_{\rm even}\);
- Yang--Baxter endomorphism ergodicity or index.

They cannot.

More precisely, write the two one-leg commutants as
\[
\mathcal C_L
\cong
\bigoplus_\alpha
\left(M_{m_\alpha}(\mathbb C)\otimes I_{2a_\alpha}\right),
\qquad
\mathcal C_R
\cong
\bigoplus_\beta
\left(M_{\widetilde m_\beta}(\mathbb C)
\otimes I_{2b_\beta}\right),
\tag{1}
\]
where
\[
\sum_\alpha m_\alpha a_\alpha
=
\sum_\beta\widetilde m_\beta b_\beta=s.
\tag{2}
\]
For every simple \(H_n(3,6)\)-module labelled by \(\lambda\), let
\[
f_{\lambda,n}=\dim S_{\lambda,n},
\qquad
D_\lambda\in\{1,2,3\}
\]
be its ordinary and quantum dimensions.  Every actual exceptional solution
would force the multiplicity of a minimal left-leg projection in the
\(\lambda\)-multiplicity space to be
\[
\boxed{
\ell_{\alpha,\lambda,n}
=a_\alpha D_\lambda s^{\,n-1}.
}
\tag{3}
\]
These integers satisfy every tower branching equation.

At both endpoints, all necessary transportation equations admit the
explicit nonnegative integral solution
\[
\boxed{
k_{\alpha\beta,\lambda,n}
=a_\alpha b_\beta D_\lambda s^{\,n-2},
\qquad n\ge2.
}
\tag{4}
\]
Thus every pair of algebras in (1) passes all central-rank and endpoint
bimodule arithmetic at every strand number.

For \(d=6\), there are exactly five one-leg algebra types with only
even-rank projections:
\[
\begin{split}
&\mathbb C I_6,\qquad
M_3(\mathbb C)\otimes I_2,\qquad
\mathbb C I_4\oplus\mathbb C I_2,\\
&(M_2(\mathbb C)\otimes I_2)\oplus\mathbb C I_2,\qquad
\mathbb C I_2\oplus\mathbb C I_2\oplus\mathbb C I_2.
\end{split}
\tag{5}
\]
Every one of the \(25\) ordered left/right pairs passes (3)--(4).

The surviving obstruction is therefore not a missing denominator.  It is
the relative spatial position, on the middle site, of
\(\mathcal C_R(P)\) coming from \(P_{12}\) and
\(\mathcal C_L(P)\) coming from \(P_{23}\).  Equivalently, it is connection
or cell data, not a dimension-vector condition.

## 2. Setup

Let
\[
P_{12}P_{23}P_{12}-P_{23}P_{12}P_{23}
=\frac13(P_{12}-P_{23}),
\qquad
\operatorname{rank}P=\frac{d^2}{2}.
\tag{6}
\]
Automatic standardness gives
\[
\operatorname{Tr}_1P=\operatorname{Tr}_2P=\frac d2I.
\tag{7}
\]
Define
\[
\mathcal C_L(P)=
\{x\in M_d:[x\otimes I,P]=0\},
\qquad
\mathcal C_R(P)=
\{x\in M_d:[I\otimes x,P]=0\}.
\tag{8}
\]

If \(d=2s\) with \(s\) odd, Theorem 3.1 of
`controlled_leg_divisibility.md` gives
\[
8\mid r d^2
\tag{9}
\]
for the rank \(r\) of every projection in either algebra.  Since
\(v_2(d^2)=2\), every such \(r\) is even.

The standard representation theorem for a finite-dimensional
\(C^*\)-subalgebra of \(M_d\) then gives (1), with minimal projections in
the \(\alpha\)-summand having ordinary rank \(2a_\alpha\).  Equation (2)
is simply \(\dim V=d=2s\).

No irreducibility or faithfulness hypothesis is added here.  Faithfulness
of the \(H_n(3,6)\) representation is already automatic for every
exceptional solution by the Markov-trace argument.

## 3. Endpoint conditional traces

Let
\[
\rho_n:H_n(3,6)\longrightarrow\operatorname{End}(V^{\otimes n})
\tag{10}
\]
be the local representation.

### Lemma 3.1

For every \(x\in H_n(3,6)\),
\[
\boxed{
\operatorname{Tr}_{2,\ldots,n}\rho_n(x)
=d^{\,n-1}\tau_n(x)I_V,
}
\tag{11}
\]
where \(\tau_n=d^{-n}\operatorname{Tr}\circ\rho_n\) is the normalized
Markov trace.

### Proof

The standard Hecke-tower spanning relation is
\[
H_n=H_{n-1}+H_{n-1}g_{n-1}H_{n-1}.
\tag{12}
\]
After applying \(\rho_n\), tracing the last site sends the first summand
to \(d\rho_{n-1}(H_{n-1})\).  For a term
\[
\rho_{n-1}(a)R_{n-1}\rho_{n-1}(b),
\]
the two outer factors do not act on the last site and can be pulled through
the partial trace.  Automatic standardness makes
\(\operatorname{Tr}_nR_{n-1}\) a scalar on site \(n-1\).  Hence the last
partial trace again lies in \(\rho_{n-1}(H_{n-1})\).

Iterating leaves an element of \(H_1=\mathbb C\), hence a scalar multiple
of \(I_V\).  Taking its ordinary trace fixes that scalar to be the
right-hand side of (11). \(\square\)

The same proof works from the other endpoint.

## 4. Forced one-sided relative-commutant multiplicities

Let \(z_{\lambda,n}\) be the central identity of the
\(\lambda\)-block.  Its represented rank is
\[
\operatorname{rank}\rho_n(z_{\lambda,n})
=f_{\lambda,n}D_\lambda s^n.
\tag{13}
\]
Let \(e_\alpha\) be any minimal projection in the \(\alpha\)-summand of
\(\mathcal C_L\).  It has rank \(2a_\alpha\) and, acting on the first site,
commutes with the entire braid image: it commutes with \(P_{12}\) by
definition and with all later generators by disjoint support.

Equations (11) and (13) give
\[
\begin{aligned}
\operatorname{rank}
\bigl(e_\alpha\rho_n(z_{\lambda,n})\bigr)
&=
\operatorname{Tr}
\bigl(e_\alpha\rho_n(z_{\lambda,n})\bigr)\\
&=
\frac{2a_\alpha}{d}
f_{\lambda,n}D_\lambda s^n\\
&=
f_{\lambda,n}a_\alpha D_\lambda s^{n-1}.
\end{aligned}
\tag{14}
\]
Because the central block is
\[
M_{f_{\lambda,n}}(\mathbb C)
\otimes I_{D_\lambda s^n},
\]
the factor \(f_{\lambda,n}\) in (14) is the ordinary simple-module
dimension.  Dividing it out proves (3).

The required inclusion recurrence is automatic:
\[
\begin{aligned}
\sum_{\nu:\lambda\nearrow\nu}
\ell_{\alpha,\nu,n+1}
&=
a_\alpha s^n
\sum_{\nu:\lambda\nearrow\nu}D_\nu\\
&=
2a_\alpha D_\lambda s^n\\
&=
d\,\ell_{\alpha,\lambda,n}.
\end{aligned}
\tag{15}
\]
The second equality is the exact Perron--Frobenius identity
\[
\sum_{\nu:\lambda\nearrow\nu}D_\nu=2D_\lambda.
\]

Thus every one-sided relative-commutant multiplicity and every inclusion
is integral for arbitrary positive integers \(a_\alpha\).  In particular,
neither the scalar algebra \(a=s,m=1\) nor the factor algebra
\(M_s\otimes I_2\), \(a=1,m=s\), is excluded.

## 5. Both endpoints: the complete dimension equations

For \(n\ge2\), \(\mathcal C_L\) on the first site and \(\mathcal C_R\) on
the last site commute with one another and with \(\rho_n(H_n(3,6))\).
Consequently, inside the \(\lambda\)-multiplicity space there are
nonnegative integers \(k_{\alpha\beta,\lambda,n}\) such that
\[
\mathbb C^{D_\lambda s^n}
\cong
\bigoplus_{\alpha,\beta}
\left(
\mathbb C^{m_\alpha}
\otimes
\mathbb C^{\widetilde m_\beta}
\otimes
\mathbb C^{k_{\alpha\beta,\lambda,n}}
\right)
\tag{16}
\]
as an \((\mathcal C_L,\mathcal C_R)\)-bimodule.

The one-sided calculation forces the transportation equations
\[
\sum_\beta
\widetilde m_\beta k_{\alpha\beta,\lambda,n}
=
a_\alpha D_\lambda s^{n-1},
\tag{17}
\]
\[
\sum_\alpha
m_\alpha k_{\alpha\beta,\lambda,n}
=
b_\beta D_\lambda s^{n-1}.
\tag{18}
\]

For every \(n\ge2\), equations (17)--(18) have the explicit solution (4).
Indeed,
\[
\begin{aligned}
\sum_\beta\widetilde m_\beta
k_{\alpha\beta,\lambda,n}
&=
a_\alpha D_\lambda s^{n-2}
\sum_\beta\widetilde m_\beta b_\beta\\
&=
a_\alpha D_\lambda s^{n-1},
\end{aligned}
\]
and similarly on the other side.  Moreover,
\[
\sum_{\alpha,\beta}
m_\alpha\widetilde m_\beta
k_{\alpha\beta,\lambda,n}
=D_\lambda s^n,
\tag{19}
\]
so the entire multiplicity space closes exactly.

This product solution is an assumption countermodel for the arithmetic.
It is not a claim that an actual exceptional solution must have product
endpoint multiplicities.

### Three strands

At \(n=3\), the three simple blocks have
\[
(f_\lambda,D_\lambda)=(1,1),(2,3),(1,1).
\tag{20}
\]
For endpoint-minimal projections of ranks \(2a\) and \(2b\), (4) gives
\[
\begin{array}{c|ccc}
&\text{common one}&\text{generic }2\times2&\text{common zero}\\ \hline
\text{module multiplicity}
&abs&3abs&abs\\
\text{central-space dimension}
&abs&6abs&abs.
\end{array}
\tag{21}
\]
Their dimensions sum to
\[
8abs=(2a)d(2b),
\tag{22}
\]
the exact dimension of the endpoint-minimal corner
\[
e_\alpha V\otimes V\otimes f_\beta V.
\]

For \(d=6\), this becomes
\[
(3ab,9ab,3ab)
\tag{23}
\]
at the simple-module multiplicity level.  In the
\(M_3\otimes I_2\) versus \(M_3\otimes I_2\) case, every one of the nine
minimal/minimal endpoint corners has multiplicities
\[
(3,9,3);
\]
summing the nine corners gives the required global values
\[
(27,81,27).
\]

No denominator survives.

## 6. Exhaustive \(d=6\) algebra types

Every summand in (1) contributes \(2m_\alpha a_\alpha\) to \(d=6\), so
\[
\sum_\alpha m_\alpha a_\alpha=3.
\tag{24}
\]
Enumerating the multiplicative partitions of \(3\) gives exactly (5).
There are no other unital finite-dimensional \(C^*\)-subalgebra
representation types on \(\mathbb C^6\) whose minimal projections all
have even rank.

The exact verifier checks all \(25\) ordered pairs from (5), every active
simple block, all endpoint row and column equations, all represented
dimensions, and every one-sided branching equation through \(n=14\).
The formulas above prove the same result for all \(n\).

This explicitly disposes of two tempting claims:

1. A hypothetical \(d=6\) solution need not have a nontrivial one-leg
   commutant.  The scalar type \(\mathbb C I_6\) passes everything.
2. Even if a nontrivial factor is forced, the type
   \(M_3(\mathbb C)\otimes I_2\) has only even-rank minimal projections and
   passes everything.

## 7. Exact scalar-commutant standard guard

It is useful to verify directly that standardness imposes no hidden
nontrivial leg algebra.

Let
\[
\zeta=e^{2\pi i/6},\qquad
X|j\rangle=|j+1\rangle,\qquad
Z|j\rangle=\zeta^j|j\rangle,
\]
and define the generalized Bell basis
\[
|\Phi_{a,b}\rangle
=
(I\otimes X^aZ^b)
\frac1{\sqrt6}\sum_{j=0}^5|j,j\rangle.
\tag{25}
\]
Use the following balanced sign table, with rows indexed by \(a\) and
columns by \(b\):
\[
(h_{a,b})=
\begin{pmatrix}
-&+&+&-&-&-\\
+&+&+&+&-&-\\
+&+&+&-&-&-\\
+&+&+&-&-&-\\
+&+&+&-&-&-\\
+&+&+&-&-&-
\end{pmatrix}.
\tag{26}
\]
Put
\[
H_{\rm Bell}
=
\sum_{a,b=0}^5h_{a,b}
|\Phi_{a,b}\rangle\langle\Phi_{a,b}|.
\tag{27}
\]
There are eighteen signs of each kind.  Since every Bell projector has
both partial traces \(I_6/6\),
\[
H_{\rm Bell}=H_{\rm Bell}^*,\qquad
H_{\rm Bell}^2=I,\qquad
\operatorname{Tr}H_{\rm Bell}=0,\qquad
\operatorname{Tr}_1H_{\rm Bell}
=\operatorname{Tr}_2H_{\rm Bell}=0.
\tag{28}
\]

The Weyl expansion of the Bell projectors pairs every left Weyl operator
with a linearly independent right Weyl operator.  Two symplectic Fourier
coefficients of (26) are
\[
\sum_{a,b}h_{a,b}\zeta^a=-1+i\sqrt3\ne0,
\tag{29}
\]
\[
\sum_{a,b}h_{a,b}\zeta^b=8+12i\sqrt3\ne0.
\tag{30}
\]
They supply both Weyl generators \(X\) and \(Z\) among the left slices,
and \(X\) and \(Z^{-1}\) among the right slices.  Since \(X,Z\) generate
\(M_6(\mathbb C)\),
\[
\boxed{
\mathcal C_L(H_{\rm Bell})
=\mathcal C_R(H_{\rm Bell})
=\mathbb C I_6.
}
\tag{31}
\]

This is deliberately only an assumption guard.  It is not a Yang--Baxter
solution.  The exact coefficient of its cubic residual from
\(|0,0,1\rangle\) to \(|3,5,3\rangle\) is
\[
\frac{-1+i\sqrt3}{27}\ne0.
\tag{32}
\]

Nevertheless, if
\[
p=P_{\rm Bell}\otimes I_6,
\]
then \(p\) has rank \(108\), and the abstract two-projection relation can
be completed exactly by taking
\[
27\text{ common-one blocks},\qquad
81\text{ generic blocks},\qquad
27\text{ common-zero blocks},
\tag{33}
\]
with each generic block
\[
p=\begin{pmatrix}1&0\\0&0\end{pmatrix},
\qquad
q=\begin{pmatrix}
1/3&\sqrt2/3\\
\sqrt2/3&2/3
\end{pmatrix}.
\tag{34}
\]
Then
\[
pqp-qpq=\frac13(p-q).
\]
The failure is precisely that this abstract \(q\) is not
\(I_6\otimes P_{\rm Bell}\).  This cleanly isolates the missing spatial
shift condition.

## 8. Exact \(M_3\otimes I_2\) standard guard

There is an equally explicit standard object with the largest
even-multiplicity factor algebra in (5).

Write
\[
V=\mathbb C^3\otimes\mathbb C^2
\]
and let \(X,Y,Z\) be the Pauli matrices.  On the right copy of
\(\mathbb C^6\), put
\[
\begin{aligned}
D_1&=\operatorname{diag}(1,1,1,-1,-1,-1),\\
D_2&=\operatorname{diag}(1,1,-1,1,-1,-1),\\
D_3&=\operatorname{diag}(1,-1,1,-1,1,-1).
\end{aligned}
\tag{35}
\]
These are commuting traceless reflections with six distinct joint sign
patterns.  Define
\[
H_{\rm fac}
=
\frac1{\sqrt3}
\left[
(I_3\otimes X)\otimes D_1
+(I_3\otimes Y)\otimes D_2
+(I_3\otimes Z)\otimes D_3
\right].
\tag{36}
\]
The Pauli matrices anticommute while the \(D_i\) commute, so all cross
terms in \(H_{\rm fac}^2\) cancel:
\[
H_{\rm fac}=H_{\rm fac}^*,\qquad
H_{\rm fac}^2=I,\qquad
\operatorname{Tr}_1H_{\rm fac}
=\operatorname{Tr}_2H_{\rm fac}=0.
\tag{37}
\]
Linear independence of the \(D_i\) gives
\[
\boxed{
\mathcal C_L(H_{\rm fac})
=M_3(\mathbb C)\otimes I_2.
}
\tag{38}
\]
The distinct joint sign patterns give a diagonal right commutant.

Again this is not a Yang--Baxter solution.  From
\(|0,0,0\rangle\) to \(|1,0,0\rangle\), the exact cubic residual
coefficient is
\[
\frac{4\sqrt3(-1-i)}9\ne0.
\tag{39}
\]
It proves only that standardness and involutivity alone allow the
\(M_3\otimes I_2\) algebra.

## 9. Conti--Lechner ergodicity is a different condition

The one-site fixed algebra in Conti--Lechner has a direct relation to the
present leg algebra:
\[
(\mathcal F_d^1)^{\lambda_R}
=
\{x\in M_d:R(x\otimes I)R^*=x\otimes I\}
=\mathcal C_L(R).
\tag{40}
\]
Tensor flip gives the other leg.

This is **not** their von Neumann ergodicity condition.  Their Theorem 7.5
states that ergodicity is equivalent to
\[
\frac1d\operatorname{Tr}_2
\bigl(R(x\otimes I)R^*\bigr)
=\frac{\operatorname{Tr}x}{d}I
\qquad\text{for every }x\in M_d.
\tag{41}
\]
In the notation of `track_channel_identities.md`, this says that the
reduced unitary channel is exactly the completely depolarizing map:
\[
\mathcal U_R=\Omega.
\tag{42}
\]
By contrast,
\[
\mathcal C_L=\mathbb C I
\]
says only that the fixed space of this channel is scalar.  A channel can
have a unique fixed vector without becoming depolarizing in one step.

Conti--Lechner explicitly distinguish these conditions: absence of
one-site fixed points is equivalent to absence of all algebraic fixed
points, but can be strictly weaker than von Neumann ergodicity.
Consequently, a scalar one-leg commutant does not imply their ergodic case.

There is also a useful exact consequence in the opposite direction.
For the exceptional matrix,
\[
\phi_R(R)=\tau(R)I,
\qquad
\tau(R)=\frac{q-1}{2},
\qquad
\left|\tau(R)\right|^2=\frac14.
\tag{43}
\]
Conti--Lechner Proposition 7.12 proves that ergodicity forces
\[
\|\phi_R(R)\|_2^2=\frac1{d^2}.
\tag{44}
\]
Equations (43)--(44) imply
\[
d=2.
\tag{45}
\]
Therefore:
\[
\boxed{
\text{Every exceptional solution of dimension }d>2
\text{ defines a nonergodic Yang--Baxter endomorphism.}
}
\tag{46}
\]
In particular, a hypothetical scalar-leg \(d=6\) solution would have
nontrivial **non-algebraic** von Neumann fixed points.  This is not a
contradiction and supplies no projection in \(M_6\).

### Why finite depth does not presently make those fixed points algebraic

The finite-depth \(H_n(3,6)\) data concern the horizontal braid-subfactor
inclusion
\[
\varphi(\mathcal L_R)\subset\mathcal L_R.
\tag{47}
\]
The fixed algebra in the ergodicity theorem is instead the vertical
relative commutant
\[
\mathcal N^{\lambda_R}
=\mathcal L_R'\cap\mathcal N.
\tag{48}
\]
Finite depth of (47) is not finite depth of the vertical inclusion
\(\mathcal L_R\subset\mathcal N\), and does not imply that (48) is
generated by its intersections with finite tensor stages.

The missing technical property is invariance under the martingale
conditional expectations
\[
E_n:\mathcal N\longrightarrow M_d^{\otimes n}.
\tag{49}
\]
If
\[
E_n(\mathcal N^{\lambda_R})
\subset\mathcal N^{\lambda_R}
\qquad\text{for every }n,
\tag{50}
\]
then martingale convergence would make the von Neumann fixed algebra the
weak closure of its algebraic fixed points.  Proposition 7.10 of
Conti--Lechner would then imply
\[
\mathcal C_L=\mathbb C I
\Longrightarrow
\mathcal N^{\lambda_R}=\mathbb C,
\]
contradicting (46).  Thus a proof of (50) for the exceptional class would
indeed force a nontrivial one-leg commutant and would be a valuable new
bridge.

But (50) is not automatic.  If \(x\) commutes with every braid generator,
then \(E_n(x)\) automatically commutes with the generators wholly inside
the first \(n\) sites and with those wholly outside.  The crossing
generator \(R_{n,n+1}\) is the unresolved case: partial trace across one
leg of an operator commuting with \(R\) need not still commute with \(R\).
Conti--Lechner prove (50) for their special \(R_4\) example from an
additional product-Pauli form; they do not claim it for arbitrary
R-matrices.

Accordingly, neither finite depth nor Proposition 7.10 presently upgrades
the nonalgebraic fixed point guaranteed by (46) to a finite-level
projection.  Establishing (50), or a weaker exceptional-specific
replacement, is a precise remaining route rather than an available
theorem.

The other finite relative commutant used by Conti--Lechner is
\[
\mathcal M_{R,1}
=
\{x\in M_d:R^*(x\otimes I)R=I\otimes x\}.
\tag{51}
\]
It is the first endomorphism relative commutant, not either algebra in
(8).  The algebras (40) and (51) commute, but neither equality nor a
rank-preserving identification is available.  An odd-rank projection in
(51), were one to exist, would therefore not satisfy the hypothesis of
the odd-leg-projection theorem.

## 10. The index is exactly four and carries no local-dimension parity

The \(H_n(3,6)\) Markov tower has Perron--Frobenius eigenvalue \(2\), hence
\[
[\mathcal L_R:\varphi(\mathcal L_R)]=4.
\tag{52}
\]
Conti--Lechner's commuting-square inequality gives
\[
[\mathcal L_R:\varphi(\mathcal L_R)]
\le
[\mathcal N:\lambda_R(\mathcal N)].
\tag{53}
\]
Since (43) is nonzero, their scalar-partial-trace upper bound gives
\[
[\mathcal N:\lambda_R(\mathcal N)]
\le|\tau(R)|^{-2}=4.
\tag{54}
\]
Thus every exceptional solution, in every allowed local dimension, has
\[
\boxed{
[\mathcal N:\lambda_R(\mathcal N)]=4.
}
\tag{55}
\]
This agrees with the categorical dimension \(2\), but it does not identify
the Cuntz local dimension \(d\) with \(2\).  The already existing
\(d=4\) solution is a concrete warning against that inference.  Index
therefore supplies no exclusion of \(d=6\).

## 11. What remains genuinely open

The current exact state is:

1. If either one-leg commutant has an odd-rank projection, then \(4\mid d\).
2. If \(d\equiv2\pmod4\), both leg algebras must be among the
   even-multiplicity types (1).
3. Every such algebra type passes all one-sided tower, central-rank,
   two-ended bimodule, ergodicity, and index tests.
4. Scalar commutants are not excluded.
5. A nontrivial factor such as \(M_3\otimes I_2\) is not excluded.

The unresolved datum sits on the middle tensor factor of three sites:
\[
\boxed{
\text{the relative position of }\mathcal C_R(P)
\text{ and }\mathcal C_L(P)\text{ inside the same }M_d.
}
\tag{56}
\]
Equations (17)--(18) forget that position.  A divisibility theorem must
extract an obstruction from the actual multiplication/connection
coefficients, or prove that those coefficients force an odd-rank endpoint
projection.  No central-idempotent denominator or endomorphism index can
do so.

## 12. Exact replay

Run:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_leg_commutant_obstruction_audit.py
```

The verifier uses exact Python integer arithmetic and SymPy algebraic
arithmetic.  It checks:

- the exhaustive five-type list (5);
- all \(25\) ordered endpoint pairs through \(n=14\);
- the all-level formulas (3)--(4) at those levels;
- the \(n=3\) corner dimensions;
- the Bell Fourier coefficients (29)--(30);
- the exact nonzero Bell cubic coefficient (32);
- the generic two-projection block (34);
- the factor construction (35)--(38);
- the exact nonzero factor cubic coefficient (39);
- the ergodicity and index arithmetic (43)--(55).

The retained output is
`results/leg_commutant_obstruction_audit_exact.txt`.

## Primary source audited

R. Conti and G. Lechner,
[Yang--Baxter endomorphisms](https://arxiv.org/abs/1909.04127),
especially the distinction following Theorem 7.5 between one-site fixed
points and von Neumann ergodicity, Proposition 7.12 on
\(\|\phi_R(R)\|_2^2\), and the index bounds in Section 6.
