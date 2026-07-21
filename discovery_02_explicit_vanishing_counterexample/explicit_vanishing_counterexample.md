# An explicit Hessian-nilpotent quartic in 54 variables witnessing the failure of Zhao's Vanishing Conjecture

*Provisional research note — 20 July 2026*

*Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol.*

*First public release: 21 July 2026, 13:11:39 UTC (21 July 2026, 06:11:39 PDT).*

*Revised: 21 July 2026.*

> **Superseded status (21 July 2026, 15:20:23 UTC).** Exploration 03 replaces
> the 27-variable cubic and 54-variable quartic dimension counts by 22 and 44.
> Thompson had also posted a 24-variable cubic map before this note's first
> release. This document is retained as a timestamped derivation of the
> factor-reusing 13-variable stable model and its original 54-variable certificate;
> its compactness claim is historical, not current. Its surviving construction
> has been consolidated into the canonical 22/44-variable paper; this note
> should not be cited separately.

> **Verification disclaimer.** I am a complete amateur and cannot independently
> verify the mathematical claims in this note. This is an experiment in the
> limits of AI-assisted mathematics, not an established result. Every argument,
> computation, and novelty claim requires independent expert review.

## Abstract

We execute a factor-reusing Bass–Connell–Wright degree reduction of the
recently announced three-dimensional noninjective Keller map, obtaining a
cubic homogeneous noninjective Keller map in 27 variables. Applying the de
Bondt–van den Essen symmetric reduction then gives an explicit homogeneous
quartic Hessian-nilpotent polynomial

\[
  \mathcal P\in \mathbb Q(i)[A_1,\ldots,A_{27},B_1,\ldots,B_{27}]
\]

with 598 monomials for which the gradient Keller map
\(Z\mapsto Z-\nabla\mathcal P(Z)\) is noninjective. This is an explicit witness
to the failure of Zhao's Vanishing Conjecture; in fact
\(\Delta^m\mathcal P^{m+1}\ne0\) for infinitely many \(m\). The expanded
polynomial and a two-point collision are supplied as machine-readable exact
certificates. The underlying three-dimensional map was posted by Levent
Alpöge on 20 July 2026, crediting Akhil Mathew for posing the question and
Claude Fable for producing the example.

## 1. Statement of the result

Let \(i^2=-1\).  The straight-line construction in Sections 2–4 defines a
cubic homogeneous map \(h:\mathbb C^{27}\to\mathbb C^{27}\).  For
\(A,B\in\mathbb C^{27}\), set

\[
  \boxed{\quad
  \mathcal P(A,B)=i\sum_{j=1}^{27}h_j(A+iB)B_j.
  \quad}                                                    \tag{1}
\]

**Theorem 1.**  The polynomial \(\mathcal P\) is homogeneous of degree four,
has 598 monomials when expanded, and its Hessian is nilpotent.  The polynomial
map

\[
  \Gamma:\mathbb C^{54}\longrightarrow\mathbb C^{54},
  \qquad \Gamma(Z)=Z-\nabla\mathcal P(Z),                  \tag{2}
\]

has Jacobian determinant one and is noninjective.  Therefore

\[
  \Delta^m\mathcal P^m=0\quad\text{for every }m\ge1,
  \qquad
  \Delta^m\mathcal P^{m+1}\ne0
\]

for infinitely many integers \(m\ge0\) in the second assertion.  Thus
\(\mathcal P\) is a counterexample to Zhao's Vanishing Conjecture.

The description (1), the formulas below, and ordinary differentiation form a
finite exact certificate.  The accompanying `potential_sparse.json` is the
fully expanded polynomial over \(\mathbb Q(i)\), and `collision.json` contains
two distinct points with the same image under (2).  Their SHA-256 hashes are,
respectively,
`556683b30fd9e7b9ecfb4c4d5395ee3be6a8dc5f918da08ed60db8c125f0df28` and
`cbea49f88cc59ba7955a4dbd710c68224590ae310a320369c49f8c63e1f78cae`.

## 2. A 13-variable cubic stable model

Write \(u=1+xy\).  Postcomposing the map announced in [4] by the inverse of its
linear part gives the identity-linear Keller map \(\Phi=(\Phi_1,\Phi_2,\Phi_3)\):

\[
\begin{aligned}
\Phi_1&=x-\frac32x^2y-\frac12x^3z,\\
\Phi_2&=y+3xu^2z+3xy^2(4+3xy),\\
\Phi_3&=u^3z+y^2u(4+3xy).
\end{aligned}                                               \tag{3}
\]

Thus \(\det J\Phi=1\), and the three points

\[
(0,0,-\tfrac14),\quad(1,-\tfrac32,\tfrac{13}2),\quad
(-1,\tfrac32,\tfrac{13}2)                                  \tag{4}
\]

have the same image \((0,0,-\tfrac14)\).

We recall a stable degree-reduction gadget.  Suppose a current map is \(M\),
and the term \(cPQ\) is to be removed from its \(k\)-th coordinate.  With new
variables \(a,b\), replace

\[
 M_k\longmapsto M_k-c(a+P)(b+Q),\qquad
 (a,b)\longmapsto(a+P,b+Q).                                \tag{5}
\]

This is a pre- and post-composition of \(M\times\mathrm{id}_{\mathbb A^2}\)
by triangular automorphisms.  A previously created output factor may be reused:
with one new variable \(a\), one may replace

\[
 M_k\longmapsto M_k-c(a+P)M_\ell,\qquad a\longmapsto a+P.  \tag{6}
\]

Both operations preserve the Jacobian determinant and invertibility.  A
collision \(p\ne q\) lifts through (5) by appending
\((-P(p),-Q(p))\) and \((-P(q),-Q(q))\), and similarly for (6).

Starting from (3), perform the following operations in order.  The symbols
\(a_j,b_j\) denote the input variables introduced at the indicated step.

| step | target | new or reused factors | coefficient \(c\) |
|---|---:|---|---:|
| 1 | \(\Phi_1\) | \(P=x^2,\ Q=xz+3y\); add \(a_1,b_1\) | \(-1/2\) |
| 2 | \(\Phi_2\) | \(P=3x^2y,\ Q=2z+xyz+3y^2\); add \(a_2,b_2\) | \(1\) |
| 3 | \(\Phi_2\) | \(P=xy,\ Q=a_2z+3xb_2\); add \(a_3,b_3\) | \(-1\) |
| 4 | \(\Phi_3\) | \(P=xy^2,\ Q=7y+3xz+3xy^2+x^2yz\); add \(a_4,b_4\) | \(1\) |
| 5 | \(\Phi_3\) | add \(a_5+a_4xy\); reuse output \(b_1+xz+3y\) | \(-1\) |
| 6 | \(\Phi_3\) | reuse output \(a_3+xy\); add \(b_6+a_4b_1-yb_4\) | \(1\) |

Finally postcompose by the shear

\[
  M_{b_4}\longmapsto M_{b_4}-M_{a_3}M_{b_1}.               \tag{7}
\]

The resulting map \(M\) has 13 variables

\[
 X=(x,y,z,a_1,b_1,a_2,b_2,a_3,b_3,a_4,b_4,a_5,b_6)         \tag{8}
\]

and degree three.  Its linear part \(L\) is the identity except for

\[
  M_{b_1}^{(1)}=b_1+3y,\qquad
  M_{b_2}^{(1)}=b_2+2z,\qquad
  M_{b_4}^{(1)}=b_4+7y.                                   \tag{9}
\]

In particular \(\det L=1\).  Put

\[
  \Psi=L^{-1}M=X+H_2(X)+H_3(X),                            \tag{10}
\]

where \(H_d\) is homogeneous of degree \(d\).  Then
\(\deg\Psi=3\), \(\det J\Psi=1\), and \(\Psi\) has the
following two preimages of the same point:

\[
\begin{aligned}
p_0={}&(0,0,-\tfrac14,0,0,0,\tfrac12,0,0,0,0,0,0),\\
p_1={}&(1,-\tfrac32,\tfrac{13}2,-1,-2,\tfrac92,-10,
\tfrac32,\tfrac34,-\tfrac94,-6,-\tfrac{27}8,\tfrac92),\\
\Psi(p_0)=\Psi(p_1)={}&(0,0,-\tfrac14,0,0,0,\tfrac12,0,0,0,0,0,0).
\end{aligned}                                               \tag{11}
\]

Equations (3), (5)–(10) are also a compact straight-line specification of all
13 components of \(\Psi\); no omitted choice is involved.

## 3. The 27-variable cubic homogeneous map

For \(X,Y\in\mathbb C^{13}\) and \(t\in\mathbb C\), define

\[
 h(X,Y,t)=\bigl(tH_2(X)+t^2Y,\,-H_3(X),\,0\bigr).           \tag{12}
\]

Every component of \(h\) is cubic homogeneous.  Let
\(\mathcal B(W)=W+h(W)\).  At \(t=1\),

\[
 \mathcal B(X,Y,1)=\bigl(X+H_2(X)+Y,\,Y-H_3(X),\,1\bigr).  \tag{13}
\]

Consequently, if

\[
 r_j=(p_j,H_3(p_j),1),                                     \tag{14}
\]

then \(\mathcal B(r_0)=\mathcal B(r_1)=(p_0,0,1)\).  Here
\(H_3(p_0)=0\), while

\[
\begin{aligned}
H_3(p_1)=(&-\tfrac{17}4,-\tfrac{45}8,\tfrac{99}{16},0,
\tfrac{135}8,-\tfrac92,-\tfrac{177}8,0,0,\tfrac94,
\tfrac{213}8,\tfrac{27}8,0).
\end{aligned}                                               \tag{15}
\]

**Lemma 2.**  The polynomial matrix \(Jh\) is nilpotent.

**Proof.**  Homogeneity and (10) give

\[
 \det\bigl(I+tJH_2(X)+t^2JH_3(X)\bigr)
   =\det J\Psi(tX)=1.                                     \tag{16}
\]

The Jacobian determinant of (13), before setting \(t=1\), is the same
determinant by the block determinant formula.  Hence
\(\det(I+Jh(W))=1\).  Since \(h\) is cubic homogeneous,
\(Jh(sW)=s^2Jh(W)\).  Therefore \(\det(I+\lambda Jh)=1\)
identically in \(\lambda\), which is equivalent to nilpotence of \(Jh\).
∎

## 4. Symmetrization and the collision

For a polynomial map \(h:\mathbb C^r\to\mathbb C^r\), de Bondt and van den
Essen associate

\[
 f_h(A,B)=-i\sum_{j=1}^r h_j(A+iB)B_j.                     \tag{17}
\]

Their characteristic-polynomial identity implies that
\(\operatorname{Hess}(f_h)\) is nilpotent if and only if \(Jh\) is nilpotent.
Our polynomial in (1) is \(\mathcal P=-f_h\), so Lemma 2 proves that
\(\mathcal P\) is Hessian nilpotent.  It follows immediately that
\(\det J\Gamma=1\).

For completeness, the collision can be seen without appealing merely to
noninvertibility preservation.  With the linear map
\(S(x,y)=(x-iy,y)\), direct differentiation gives

\[
 S^{-1}\Gamma S(x,y)=
 \left(x+h(x),\ (I+Jh(x)^T)y-i h(x)\right).                \tag{18}
\]

Take \(r_0,r_1\) from (14), let \(K_j=I+Jh(r_j)^T\), put

\[
 y_1=0,\qquad y_0=K_0^{-1}(-i h(r_1)+i h(r_0)),             \tag{19}
\]

and set \(z_j=S(r_j,y_j)\).  Equation (18) and
\(r_0+h(r_0)=r_1+h(r_1)\) show \(\Gamma(z_0)=\Gamma(z_1)\).
The two 54-tuples are recorded explicitly in `collision.json`; all coordinates
have height at most 261.  Direct differentiation of the 598-term expansion
checks this equality exactly over \(\mathbb Q(i)\).

## 5. Failure of the Vanishing Conjecture

Zhao proved that Hessian nilpotence of a homogeneous polynomial \(P\) is
equivalent to

\[
  \Delta^m P^m=0\qquad\text{for every }m\ge1.              \tag{20}
\]

Lemma 2 and the symmetric reduction therefore show that \(\mathcal P\)
satisfies the hypothesis of the Vanishing Conjecture.  Zhao's inversion formula
for a Hessian-nilpotent polynomial \(P\) states that
the inverse of \(Z-t\nabla P\) is \(Z+t\nabla Q_t\), where

\[
 Q_t=\sum_{m=0}^{\infty}
 \frac{t^m}{2^m m!(m+1)!}\,\Delta^m P^{m+1}.               \tag{21}
\]

If \(\Delta^m\mathcal P^{m+1}=0\) for all sufficiently large \(m\), then
\(Q_t\) is a polynomial.  Specializing at \(t=1\) would give a polynomial
inverse of \(\Gamma\), contradicting the explicit collision above.  Thus
\(\Delta^m\mathcal P^{m+1}\ne0\) for infinitely many \(m\), proving
Theorem 1.

This argument does not exhibit a particular exponent \(m\) for which
\(\Delta^m\mathcal P^{m+1}\ne0\); it deduces the existence of infinitely many
such exponents indirectly from the collision and the inversion formula.
Zhao's general finite bound for quartics in \(n\) variables reaches
\(m>\frac32(3^{n-2}-1)\), or \(m>\frac32(3^{52}-1)\) here, so direct expansion
at the general bound is impractical.

## 6. Reproducibility

The repository contains two complementary exact checks.  `verify.py` rebuilds
the construction symbolically and verifies the announced map, all six stable
reduction gadgets, the cubic homogeneous map, Hessian nilpotence through the
structural reduction, and the final collision.  `verify_exported_stdlib.py`
uses only Python's standard library and the two JSON files to verify the
expanded polynomial's degree and term count and the exact collision.  The
latter is deliberately not advertised as a stand-alone proof of Hessian
nilpotence.  All arithmetic in both checks is exact.

## 7. Historical scope and post-release correction

Zhang's consequence note of 20 July 2026 observes, by Zhao's equivalence, that
the announced three-dimensional counterexample makes the Vanishing Conjecture
false in some finite dimension; it explicitly leaves the consequence
existential.  An earlier public repository [6] gives a 79-variable cubic
homogeneous noninjective Keller map.  Applying the standard symmetric reduction
to that map would produce a 158-variable quartic in principle, but the
repository did not supply an expanded quartic witness or its transported
collision at the time of our search.

At initial release, this note presented the executed 54-variable, 598-term
quartic, its exact collision, and the 27-variable factor-reusing reduction as
its narrower candidate contribution. That priority language is retained here
only as historical context. It is not the current assessment.

**Post-release correction.** Thompson's initial public commit [7], at
03:29:42 UTC on 21 July 2026, already gave a 24-variable cubic homogeneous
reduction and therefore beat this note's 27-variable dimension headline before
our 13:11:39 UTC release. We failed to find it in the first audit. Exploration
03 subsequently compressed our 13-variable stable model to a 22-variable cubic
and a 44-variable quartic. Accordingly, this note is superseded for dimension
comparisons or as a separate current result. Its surviving role is as the
derivation of that stable model and as a reproducible earlier certificate.
Both have now been incorporated into the canonical Exploration 03 paper.

## References

1. H. Bass, E. H. Connell, and D. Wright, “The Jacobian conjecture: reduction
   of degree and formal expansion of the inverse,” *Bull. Amer. Math. Soc.* 7
   (1982), 287–330. DOI: 10.1090/S0273-0979-1982-15032-7.
2. M. de Bondt and A. van den Essen, “A reduction of the Jacobian conjecture
   to the symmetric case,” *Proc. Amer. Math. Soc.* 133 (2005), 2201–2205.
   DOI: 10.1090/S0002-9939-05-07570-2.
3. W. Zhao, “Hessian nilpotent polynomials and the Jacobian conjecture,”
   *Trans. Amer. Math. Soc.* 359 (2007), 249–274. arXiv:math/0409534.
4. L. Alpöge, X post announcing the three-dimensional map, crediting Akhil
   Mathew for posing the question and Claude Fable for producing the example,
   20 July 2026, https://x.com/__alpoge__/status/2079028340955197566.
5. Z. Zhang, “Direct consequences of the three-dimensional counterexample to
   the Jacobian conjecture,” 20 July 2026,
   https://zzhang-iu.github.io/papers/direct-consequences-jacobian/.
6. A. Harrison, `jacobian-anatomy`, public GitHub repository, commit
   `74808fb2e1c1691b0007576ba0508e5e7cdcb1e3`, 20 July 2026,
   https://github.com/DrAlexHarrison/jacobian-anatomy/commit/74808fb2e1c1691b0007576ba0508e5e7cdcb1e3.
7. W. Thompson, “An explicit 24-variable cubic-homogeneous reduction of the
   Alpöge–Fable Jacobian counterexample,” public GitHub repository, commit
   `45a7616fdf5a20c065564f2676190093722696b9`, 21 July 2026,
   https://github.com/wtho704/explicit-cubic-homogeneous-jacobian-counterexample.

## AI-assistance and verification disclosure

The construction, proof organization, verification programs, website, and
typeset drafts were developed with extensive assistance from ChatGPT 5.6 Sol.
Alec Kriebel takes responsibility for the submission and for preserving the
complete source and exact certificates.  The algebraic checks are reproducible,
but the note has not been peer reviewed and independent expert scrutiny is
welcome.

## Archival citation status

Do not cite this as a separate current result. Cite the canonical consolidated
paper, “An explicit 44-variable vanishing witness from a 22-variable cubic
Keller map,” instead. This page remains the timestamped provenance record for
the 13-variable reduction and original 54-variable certificate.
