# An explicit 44-variable vanishing witness from a 22-variable cubic Keller map

*Provisional research note — 21 July 2026*

*Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol.*

*First public release: 21 July 2026, 14:42:57 UTC (21 July 2026, 07:42:57 PDT).*

*Priority correction: 21 July 2026, 15:20:23 UTC (21 July 2026, 08:20:23 PDT).*

> **Verification disclaimer.** I am a complete amateur and cannot independently
> verify the mathematical claims in this note. This is an experiment in the
> limits of AI-assisted mathematics, not an established result. Every argument,
> computation, attribution, and novelty claim requires independent expert
> review. Exact checks of the encoded algebra are evidence, not peer review.

## Abstract

Starting from the recently announced three-dimensional noninjective Keller
map, we record a compressed route to an explicit vanishing witness. The cubic
components of a certified
13-variable degree-three stable model span only an eight-dimensional constant
coefficient space. A rank-compressed homogenization therefore gives a
22-variable cubic homogeneous noninjective Keller map. Applying the
de Bondt–van den Essen symmetric reduction produces an explicit homogeneous
quartic Hessian-nilpotent polynomial in 44 variables, with 538 monomials, whose
gradient Keller map is noninjective. The expanded potentials and collisions
are supplied as machine-readable exact certificates.

For reuse, we also give a normalized six-variable degree-eight potential from
Meng's classical gradient lift. After the first release, a priority audit found
that Eliott Cassidy's public repository had already executed the equivalent
six-dimensional symmetric transport, with the same lifted three-point fiber,
on 20 July 2026. We therefore claim no novelty for the six-variable
construction. The narrower candidate contribution is the executed
22-variable cubic and 44-variable quartic certificate. Nothing here is
logically independent of the announced three-dimensional counterexample.

## 1. Main statements

Let \(i^2=-1\). Let

\[
 \Phi=(\Phi_1,\Phi_2,\Phi_3):\mathbb C^3\longrightarrow\mathbb C^3
\]

be the identity-linear normalization of the announced map:

\[
\begin{aligned}
\Phi_1&=x-\frac32x^2y-\frac12x^3z,\\
\Phi_2&=y+3x(1+xy)^2z+3xy^2(4+3xy),\\
\Phi_3&=(1+xy)^3z+y^2(1+xy)(4+3xy).
\end{aligned}                                                \tag{1}
\]

It satisfies \(\det J\Phi=1\), and the three points

\[
 p_0=(0,0,-\tfrac14),\quad
 p_1=(1,-\tfrac32,\tfrac{13}2),\quad
 p_2=(-1,\tfrac32,\tfrac{13}2)                              \tag{2}
\]

all map to \(q=(0,0,-\tfrac14)\).

For \(A,B\in\mathbb C^3\), put

\[
 X=A+iB,\qquad \Lambda=\frac{A-iB}{2},\qquad
 \boxed{\;\mathcal S(A,B)=\Lambda^T\Phi(X).\;}             \tag{3}
\]

**Theorem A.** The gradient map

\[
 \nabla\mathcal S:\mathbb C^6\longrightarrow\mathbb C^6   \tag{4}
\]

has symmetric Jacobian, identity linear part, and Jacobian determinant one.
It is noninjective: the three distinct points

\[
 z_j=(p_j/2,-ip_j/2)\in\mathbb Q(i)^6                       \tag{5}
\]

all map to \((q/2,-iq/2)=(0,0,-1/8,0,0,i/8)\). The potential
\(\mathcal S\) has degree eight and 204 monomials when expanded.

The construction in Sections 3–5 also defines a cubic homogeneous map
\(h:\mathbb C^{22}\to\mathbb C^{22}\). For
\(A,B\in\mathbb C^{22}\), set

\[
 \boxed{\;\mathcal P(A,B)=i\sum_{j=1}^{22}h_j(A+iB)B_j.\;}  \tag{6}
\]

**Theorem B.** The polynomial map \(W\mapsto W+h(W)\) has
Jacobian determinant one and an explicit rational three-point fiber. The
matrix \(Jh\) is nilpotent. The polynomial \(\mathcal P\) is homogeneous of
degree four, has 538 monomials, and has nilpotent Hessian. The map

\[
 \Gamma(Z)=Z-\nabla\mathcal P(Z):\mathbb C^{44}\to\mathbb C^{44} \tag{7}
\]

has Jacobian determinant one and is noninjective. Consequently

\[
 \Delta^m\mathcal P^m=0\quad(m\ge1),\qquad
 \Delta^m\mathcal P^{m+1}\ne0
\]

for infinitely many \(m\), so \(\mathcal P\) explicitly witnesses failure of
Zhao's Vanishing Conjecture.

## 2. The six-variable symmetric map

The symmetry assertion in Theorem A is automatic because
\(J(\nabla\mathcal S)=\operatorname{Hess}(\mathcal S)\). What matters is the
determinant. Begin with the usual Meng potential

\[
 f(X,\Lambda)=\Lambda^T\Phi(X).
\]

Its Hessian has block form

\[
 \operatorname{Hess}(f)=
 \begin{pmatrix}
  \sum_k\Lambda_k\operatorname{Hess}(\Phi_k)&J\Phi^T\\
  J\Phi&0
 \end{pmatrix}.                                             \tag{8}
\]

Swapping the two blocks of three columns makes (8) block upper triangular.
Therefore

\[
 \det\operatorname{Hess}(f)=(-1)^3(\det J\Phi)^2=-1.       \tag{9}
\]

Equation (3) is the pullback of \(f\) by

\[
 C=\begin{pmatrix}I&iI\\ \frac12I&-\frac i2I\end{pmatrix},
 \qquad \det C=i.                                           \tag{10}
\]

Hessians transform by congruence, so (9) and (10) give

\[
 \det\operatorname{Hess}(\mathcal S)
   =(\det C)^2\det\operatorname{Hess}(f)=1.                \tag{11}
\]

Since \(J\Phi(0)=I\), direct multiplication also gives
\(\operatorname{Hess}(\mathcal S)(0)=I_6\). Thus
\(\nabla\mathcal S\) has identity linear part. At a point with
\((X,\Lambda)=(p_j,0)\), one has

\[
 \nabla f(p_j,0)=(0,\Phi(p_j))=(0,q).
\]

Applying \(C^T\) proves (5) and its common image. This proof is the classical
Meng construction specialized to the new map, with the congruence (10) making
the gradient map identity-linear over \(\mathbb Q(i)\).

## 3. A rank-compressed homogenization lemma

The following elementary form of the Bass–Connell–Wright homogenization is
the source of the dimension improvement.

**Lemma 1 (rank-compressed homogenization).** Suppose

\[
 \Psi(X)=X+H_2(X)+H_3(X):\mathbb C^n\to\mathbb C^n,
 \qquad \det J\Psi=1,                                      \tag{12}
\]

where \(H_d\) is homogeneous of degree \(d\). Suppose further that
\(H_3=BK\), where \(B\) is a constant \(n\times r\) matrix and
\(K:\mathbb C^n\to\mathbb C^r\) is cubic homogeneous. Define

\[
 h(X,U,t)=\bigl(tH_2(X)+t^2BU,-K(X),0\bigr)                \tag{13}
\]

in \(n+r+1\) variables. Then \(h\) is cubic homogeneous and \(Jh\) is
nilpotent. If \(p\ne q\) and \(\Psi(p)=\Psi(q)\), then

\[
 (p,K(p),1)\ne(q,K(q),1)                                  \tag{14}
\]

collide under \(W\mapsto W+h(W)\).

**Proof.** For an indeterminate \(s\), a Schur complement in
\(I+sJh\) gives

\[
\begin{aligned}
 \det(I+sJh)
 &=\det\bigl(I+s,tJH_2+s^2t^2BJK\bigr)\\
 &=\det J\Psi(stX)=1.                                     \tag{15}
\end{aligned}
\]

Hence the characteristic polynomial of \(Jh\) is \(T^{n+r+1}\), so \(Jh\)
is nilpotent. At \(t=1\), substitution in (13) gives

\[
 (X,K(X),1)+h(X,K(X),1)=(\Psi(X),0,1),
\]

which proves the collision statement. ∎

The usual version takes \(r=n\) and \(K=H_3\). Lemma 1 only retains the
constant coefficient span of the cubic components.

## 4. The 13-variable model and its cubic rank

We use the factor-reusing stable reduction described in Exploration 02. It
starts from (1), applies six triangular degree-reduction gadgets, and produces
an identity-linear map

\[
 \Psi=X+H_2+H_3:\mathbb C^{13}\to\mathbb C^{13}            \tag{16}
\]

with \(\det J\Psi=1\). The variable order is

\[
 X=(x,y,z,a_1,b_1,a_2,b_2,a_3,b_3,a_4,b_4,a_5,b_6).       \tag{17}
\]

For completeness, the exact stable operations are:

| step | target | new or reused factors | coefficient |
|---|---:|---|---:|
| 1 | \(\Phi_1\) | \(x^2,\ xz+3y\); add \(a_1,b_1\) | \(-1/2\) |
| 2 | \(\Phi_2\) | \(3x^2y,\ 2z+xyz+3y^2\); add \(a_2,b_2\) | \(1\) |
| 3 | \(\Phi_2\) | \(xy,\ a_2z+3xb_2\); add \(a_3,b_3\) | \(-1\) |
| 4 | \(\Phi_3\) | \(xy^2,\ 7y+3xz+3xy^2+x^2yz\); add \(a_4,b_4\) | \(1\) |
| 5 | \(\Phi_3\) | add \(a_5+a_4xy\); reuse \(b_1+xz+3y\) | \(-1\) |
| 6 | \(\Phi_3\) | reuse \(a_3+xy\); add \(b_6+a_4b_1-yb_4\) | \(1\) |

Each two-factor step replaces a term \(cPQ\) in one coordinate by
\(-c(a+P)(b+Q)\) and appends \((a+P,b+Q)\); the one-factor version reuses an
already encoded output. A final output shear subtracts the product of the
\(a_3\)- and \(b_1\)-outputs from the \(b_4\)-output. These are pre- and
post-compositions by triangular automorphisms, proving the determinant claim.

The two stable collision points used below are

\[
\begin{aligned}
\pi_0={}&(0,0,-\tfrac14,0,0,0,\tfrac12,0,0,0,0,0,0),\\
\pi_1={}&(1,-\tfrac32,\tfrac{13}2,-1,-2,\tfrac92,-10,
\tfrac32,\tfrac34,-\tfrac94,-6,-\tfrac{27}8,\tfrac92).
\end{aligned}                                               \tag{18}
\]

Exact coefficient row reduction shows that the thirteen components of
\(H_3\) span an eight-dimensional space. With \(K=(K_1,\ldots,K_8)\), take

\[
\begin{aligned}
K_1={}&\tfrac12x(a_1z+b_1x),\\
K_2={}&a_2a_3z-3a_2y^2+3b_2a_3x+b_3xy+12xy^2,\\
K_3={}&-b_1a_3a_4+a_3b_4y-3a_4xz+a_5xz-b_6xy+3xyz,\\
K_4={}&3x^2y,\\
K_5={}&2b_1a_3a_4-2a_3b_4y+6a_4xz-2a_5xz+2b_6xy-5xyz,\\
K_6={}&xy^2,\\
K_7={}&-b_1xy-7a_2a_3z+21a_2y^2-21b_2a_3x-a_3xz
       -7b_3xy-84xy^2,\\
K_8={}&a_4xy.
\end{aligned}                                               \tag{19}
\]

Then \(H_3=BK\), where

\[
 B(U_1,\ldots,U_8)=
 (U_1,U_2,U_3,0,-3U_2,U_4,U_5,0,0,U_6,U_7,U_8,0).          \tag{20}
\]

Equations (16)–(20) and the construction program are an exact finite
specification; the verifier checks \(H_3=BK\) coefficient by coefficient and
checks \(\operatorname{rank}B=8\).

Applying Lemma 1 with \(n=13\) and \(r=8\) gives the claimed 22-variable map.
It has 72 nonzero cubic monomials across 21 active nonlinear coordinates. The
two collision points are \((\pi_j,K(\pi_j),1)\). In particular,

\[
 K(\pi_0)=0,
\]

and

\[
 K(\pi_1)=(-\tfrac{17}4,-\tfrac{45}8,\tfrac{99}{16},
 -\tfrac92,-\tfrac{177}8,\tfrac94,\tfrac{213}8,\tfrac{27}8). \tag{21}
\]

## 5. The 44-variable quartic

For the 22-variable map \(h\), define \(\mathcal P\) by (6). The
de Bondt–van den Essen characteristic-polynomial identity says that the
Hessian of

\[
 -i\sum_jh_j(A+iB)B_j
\]

is nilpotent if and only if \(Jh\) is nilpotent. Negation preserves
nilpotence, so Lemma 1 makes \(\mathcal P\) Hessian nilpotent.

The collision under (7) can also be transported explicitly. If
\(r_0,r_1\in\mathbb C^{22}\) collide under \(x\mapsto x+h(x)\), let
\(M_j=I+Jh(r_j)^T\), set

\[
 y_1=0,\qquad y_0=M_0^{-1}\bigl(-ih(r_1)+ih(r_0)\bigr),    \tag{22}
\]

and define \(z_j=(r_j-iy_j,y_j)\). Direct differentiation gives

\[
 \Gamma(z_0)=\Gamma(z_1).                                  \tag{23}
\]

The two 44-tuples in (23) are recorded in `output/collision.json`; their
coordinates lie in \(\mathbb Q(i)\), with numerator at most 261 in absolute
value and denominator at most 16. The fully expanded quartic is
`output/potential_sparse.json`.

Zhao proved that Hessian nilpotence of a homogeneous polynomial \(P\) is
equivalent to \(\Delta^mP^m=0\) for all \(m\ge1\), and that the formal inverse
of \(Z-t\nabla P\) is governed by

\[
 Q_t=\sum_{m\ge0}\frac{t^m}{2^m m!(m+1)!}\Delta^mP^{m+1}. \tag{24}
\]

If the terms in (24) vanished eventually, \(\Gamma\) would have a polynomial
inverse, contradicting (23). This proves the Vanishing Conjecture assertion in
Theorem B.

## 6. Exact certificates

The exported files have SHA-256 hashes:

```text
1e0c97e1c4965c3ef7d85cdfb115d468f79d8b5195a7f34f498015c3c3f5fdd4  symmetric_potential_sparse.json
6b5b546f24e839a10ab330ae9b05d1d03d23a6fbbbff8cfa6d1ce742768f7169  symmetric_collision.json
2a912728161888849e77d607ea1f635233576543ed12d5fe8b2a65e0751789f4  potential_sparse.json
aeab7adb021c07dea396d2c0eca0cc7880b93dc7b09b74f60289936a711addd0  collision.json
```

`verify.py` reconstructs both maps symbolically, checks the Hessian block
congruence, the 13-to-8 cubic factorization, the determinant identity (15),
nilpotence at exact guard points, and both collisions.
`verify_exported_stdlib.py` uses only Python's standard library and the four
JSON files. `verify_exported_node.mjs` independently implements exact rational
complex arithmetic with JavaScript `BigInt` and reads the same JSON. Both
differentiate the sparse polynomials themselves and verify the six-variable
identity linear part and finite fibers plus the 44-variable exact collision.
Neither exported-certificate checker is described as a stand-alone proof of
Hessian nilpotence.

## 7. Scope and priority

Theorem A is an explicit six-variable consequence of Meng's 2006 gradient
lift, not a new reduction theorem. More importantly, it is not a new executed
instance. Cassidy's repository commit `40e1e20f9ee113245f8e4e4b22ecd798fa1ffbfc`,
authored at 14:46:10 UTC on 20 July 2026, already applies the
de Bondt--van den Essen/Meng transport directly to the announced map in
\(\mathbb C^6\), checks symmetry, and transports the same three-point fiber.
Our determinant-one, identity-linear formula (3) is a normalized presentation
with a machine-readable potential, not an independent discovery. The original
version of this note failed to find that artifact and overstated this part of
the novelty claim.

Zhang's 20 July consequence note observes that Zhao's Vanishing Conjecture is
false in some finite dimension and asks for a small explicit quartic. Our
earlier Exploration 02 gave a 54-variable, 598-term certificate. William
Thompson independently posted a 24-variable cubic homogeneous reduction at
03:29:42 UTC on 21 July 2026; its degree-three part has a six-dimensional
component span. That work contains the same rank-compression principle in
executed form and has priority over this note for that idea. Thompson's map has
24 variables, 54 cubic monomials, and 23 active nonlinear coordinates; ours
has 22 variables, 72 cubic monomials, and 21 active nonlinear coordinates.
Both cubic maps are defined over \(\mathbb Q\) and have rational collisions.
Thus ours is smaller only in ambient dimension, while Thompson's is sparser.
The narrower quantitative statement here uses a different 13-variable stable
reduction: \(13+8+1=22\) cubic variables and hence 44 symmetric variables.

Searches of arXiv, MathOverflow, and public GitHub code on 21 July 2026 found
no earlier public 22-variable cubic certificate or executed 44-variable
quartic certificate. Thompson's audited initial commit contains no symmetric
quartic or Zhao witness; Harrison's earlier repository executes a 79-variable
cubic-homogeneous/Drużkowski route but does not export the corresponding
symmetric quartic. These are source-specific observations, not a claim of
exhaustive worldwide priority. The literature is changing by the hour, the
work is unreviewed, and all novelty statements are provisional.

## References

1. H. Bass, E. H. Connell, and D. Wright, “The Jacobian conjecture: reduction
   of degree and formal expansion of the inverse,” *Bull. Amer. Math. Soc.* 7
   (1982), 287–330. DOI: 10.1090/S0273-0979-1982-15032-7.
2. M. de Bondt and A. van den Essen, “A reduction of the Jacobian conjecture
   to the symmetric case,” *Proc. Amer. Math. Soc.* 133 (2005), 2201–2205.
   DOI: 10.1090/S0002-9939-05-07570-2.
3. G. Meng, “Legendre transform, Hessian conjecture and tree formula,”
   *Applied Mathematics Letters* 19 (2006), 503–510.
4. M. de Bondt, “Symmetric Jacobians,” *Open Mathematics* 11 (2013),
   1621–1634. arXiv:1206.2865.
5. W. Zhao, “Hessian nilpotent polynomials and the Jacobian conjecture,”
   *Trans. Amer. Math. Soc.* 359 (2007), 249–274. arXiv:math/0409534.
6. L. Alpöge, X post announcing the three-dimensional map, crediting Akhil
   Mathew for posing the question and Claude Fable for producing the example,
   20 July 2026, https://x.com/__alpoge__/status/2079028340955197566.
7. Z. Zhang, “Direct consequences of the three-dimensional counterexample to
   the Jacobian conjecture,” 20 July 2026,
   https://zzhang-iu.github.io/papers/direct-consequences-jacobian/.
8. W. Thompson, “An explicit 24-variable cubic-homogeneous reduction of the
   Alpöge–Fable Jacobian counterexample,” public GitHub repository, commit
   `45a7616fdf5a20c065564f2676190093722696b9`, 21 July 2026,
   https://github.com/wtho704/explicit-cubic-homogeneous-jacobian-counterexample.
9. E. Cassidy, `THM-1430: An explicit symmetric-case Keller counterexample on
   C^6`, public GitHub repository, commit
   `40e1e20f9ee113245f8e4e4b22ecd798fa1ffbfc`, 20 July 2026,
   https://github.com/eliottcassidy2000/math/blob/40e1e20f9ee113245f8e4e4b22ecd798fa1ffbfc/01-canon/theorems/THM-1430-explicit-symmetric-keller-counterexample-on-C6.md.
10. A. Kriebel, with heavy assistance from ChatGPT 5.6 Sol, “An explicit
   Hessian-nilpotent quartic in 54 variables witnessing the failure of Zhao's
   Vanishing Conjecture,” provisional note, 21 July 2026.

## AI-assistance and verification disclosure

The constructions, searches, proof organization, verification programs,
website, and drafts were developed with heavy assistance from ChatGPT 5.6
Sol. Alec Kriebel is a complete amateur, cannot independently verify the
claims, and is publishing this as an open experiment in the limits of
AI-assisted mathematics. The exact checks are reproducible, but the note has
not been peer reviewed. Independent expert scrutiny is essential.

## Suggested citation

Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol, “An explicit
44-variable vanishing witness from a 22-variable cubic Keller map,”
provisional research note, first posted 21 July 2026, priority correction
21 July 2026,
https://aleckriebel.github.io/Math/papers/symmetric-keller-and-vanishing/.
