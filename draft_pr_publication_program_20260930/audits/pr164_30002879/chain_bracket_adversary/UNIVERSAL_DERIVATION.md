# Independent all-degree cochain derivation

This derivation concerns every field K of characteristic two and the specified
algebra A=K[x,y]/(x²,y²), M=A/(y), B=[[A,M],[0,K]]. It was reconstructed
from multiplication and normalized relative cochains, without importing the
submission's checker or using a prior verdict. All degree claims below are
deductions; bounded computations are separate diagnostics.

## 1. Relative bar model and the actual coefficient sequence

Write f=diag(1,0), e=diag(0,1), E=Kf⊕Ke, J=rad(B). Thus B=E⊕J, with
J having basis x,y,xy,m,xm. Multiplication is determined by x²=y²=0,
xy=yx, x·m=xm, y·m=0, x·xm=y·xm=0, and the vertex units. In
particular, the module has a nonzero x action; replacing it by two trivial
copies changes B.

The reduced E-relative bar resolution has terms
B⊗_E J^{⊗_E n}⊗_E B. The usual bar boundary has endpoint products and
adjacent internal products. This augmented complex is exact by the bar
contracting homotopy; normalization uses the E-bimodule splitting B=E⊕J.
Its terms are projective B-bimodules: every E-bimodule is projective since
E^e≅K⁴, and induction to B^e preserves projectives. Therefore its cochains
compute ordinary Hochschild cohomology and coefficient Ext groups, not a
different relative invariant.

Composable positive-length J words are exactly all-A radical words, and
radical-A words ending in one M input. Outputs are respectively in A and M.
No positive-length word has an e-to-e corner. Put

T^r=Hom_K(rad(A)^{⊗ r}⊗_K M,M), r≥0.

Then C_B^0=A⊕K and C_B^n=C_A^n⊕T^{n−1}, n≥1. The mixed differential is

(d_T h)(a₁,…,a_{r+1},m)
= a₁h(a₂,…,a_{r+1},m)
  + Σ_{s=1}^r h(a₁,…,a_s a_{s+1},…,a_{r+1},m)
  + h(a₁,…,a_r,a_{r+1}m).

For the all-A component f, the additional mixed term is exactly

theta_n(f)(a₁,…,a_n,m)=f(a₁,…,a_n)m.

These formulas follow term by term from the Hochschild differential; every
sign becomes plus in characteristic two. T is the module-bar cochain complex
computing Ext_A*(M,M), since its dual resolution has free A terms
A⊗_K rad(A)^{⊗ r}⊗_K M and the module-bar boundary.

Now let I=BeB=M⊕Ke. Its relative coefficient complex has C_I^0=K and
C_I^n=T^{n−1} for n≥1. The degree-zero differential is c↦c Id_M, and
the subsequent differential is d_T. Consequently

H⁰(C_I)=0,
H¹(C_I)=End_A(M)/K Id_M,
H^{n+1}(C_I)=Ext_A^n(M,M), n≥1.

With coefficients A=B/I, the relative complex consists only of all-A
inputs and A outputs, and is precisely C_A. Projection π:B→A induces the
degreewise exact sequence

0→C_I→C_B→C_A→0.

Thus the cohomology map C_B→C_A is the gamma of the original coefficient
sequence. Its connecting map is represented by theta_n, directly from the
cochain differential. This argument does not identify gamma merely by
matching dimensions or by replacing the coefficient sequence with another
sequence.

## 2. Ambient coordinates are fixed by shuffle evaluation

For D=K[t]/(t²), use the free D^e resolution with one generator per degree
and differential t_L+t_R. On the basis 1,t_L,t_R,t_Lt_R, multiplication
by t_L+t_R has equal image and kernel, each spanned by t_L+t_R and
t_Lt_R. The degree-zero augmentation has that same kernel. This proves
exactness, including in characteristic two.

Tensor the x and y resolutions over K. Their total free A^e resolution
has e_{i,j} in degree i+j, with differential

d e_{i,j}=(x_L+x_R)e_{i−1,j}+(y_L+y_R)e_{i,j−1}.

Exactness follows by tensoring complexes over the field; Hom_{A^e}(−,A)
has zero differential. A comparison to the normalized A bar sends e_{i,j}
to the sum of words containing i letters x and j letters y. For unlike
adjacent letters, the two possible orders give the same merged xy word and
cancel. Like adjacent letters multiply to zero. Endpoint terms are exactly
the displayed differential. This cancellation proves the chain identity in
every degree; no binomial division or factorial inversion occurs.

The ordinary derivations u=∂_x and v=∂_y are valid because ∂_x(x²)=0
and ∂_y(y²)=0 in characteristic two. The cup representative
a(∂_x)^{cup i}(∂_y)^{cup j} evaluates to a on e_{i,j}: only the word
with its first i inputs x and final j inputs y contributes. It evaluates to
zero on all other degree-i+j shuffle generators. These are therefore exact
cohomology coordinates, not a polynomial isomorphism with unspecified
normalization. They give

HH*(A)=R=K[x,y,u,v]/(x²,y²), |x|=|y|=0, |u|=|v|=1.

The generators' actual insertion brackets are [u,x]=[v,y]=1, while every
other pair among x,y,u,v has zero bracket. Here degree-one brackets are
commutators of derivations, and insertion against degree zero is evaluation.
The Gerstenhaber biderivation identity now gives, for arbitrary homogeneous
polynomials and then by bilinearity,

[F,G]=F_x G_u+F_u G_x+F_y G_v+F_v G_y.

Derivatives descend modulo x²,y² in characteristic two. This derives the
ambient formula from actual generator operations and a cochain-theoretic
identity, rather than testing the formula against itself.

## 3. The connecting map in every degree

Resolve M by Q_n=A, d_n=y for n>0, augmented by A→A/(y). The equality
ker(y)=yA proves exactness. Applying Hom_A(−,M) gives zero differentials.
The identity shifts of Q represent a degree-one class eta, so composition
of those shifts gives eta^n. Hence Ext_A*(M,M)=M[eta].

The comparison Q→module bar is particularly simple:

1∈Q_n ↦ 1⊗[y|…|y]⊗1_M.

The bar boundary has only its left endpoint y; internal yy terms vanish
and the right endpoint y·1_M is zero. Thus this is a chain map lifting the
identity of M in every degree. Evaluate theta_n of the above cup
representatives on that comparison. For i>0, ∂_x(y)=0 kills it; for i=0,
every ∂_y(y)=1. The result is

chi_n(a u^i v^j)=0 if i>0,
chi_n(a v^n)=(a mod y) eta^n.

For n≥1 this is surjective, represented by v^n and xv^n, and its kernel
is the degree-n part of (y,u)R. Degree zero instead lands in
End_A(M)/K Id_M=M/K, with a↦(a mod y) mod K. This is surjective and
has kernel K+yA.

The coefficient long exact sequence therefore makes gamma injective in
every degree: the preceding connecting map is always surjective. Its image
is ker(chi_n), with the explicit degree-zero exception just computed. Hence

gamma(HH*(B))=L=K·1+(y,u)R.

The center calculation independently verifies the exception: a central
element has no M component because it must commute with f and e; its
diagonal pair (a,c) satisfies a mod y=c. Projection to A has basis 1,y,xy
and is injective. It excludes x. For n≥1 the complete basis consists of
x^a y^b u^i v^j with a,b∈{0,1}, i+j=n, and i>0 or b=1, giving 4n+2.

## 4. Insertion preservation and structure constants

Restrict any relative insertion to all-A inputs. A positive-arity inner
cochain then has A output by E-bimodule linearity, and the outer cochain
also has A output. Mixed components cannot contribute. For a zero-arity
inner cochain its e-corner contributes zero; its f-corner is its projected
A value. Scalar vertex components are killed by normalized slot projection
on both sides. Thus restriction commutes with each insertion in all arities,
including zero. It commutes with cup by the same corner argument, and it
therefore commutes with bracket. This applies to the actual coefficient
gamma identified in Section 1.

The image L is closed under the ambient bracket. Expanding brackets of
yF,yG; uF,uG; and yF,uG by the biderivation identity leaves a y or u in
each nonzero term, since [y,u]=0. Constants bracket to zero. The bracket
in L is consequently the actual bracket of HH*(B), with no extension
ambiguity. On monomials it is

[x^a y^b u^i v^j,x^c y^d u^k v^l]
=(ak+ci)x^{a+c−1}y^{b+d}u^{i+k−1}v^{j+l}
 +(bl+dj)x^{a+c}y^{b+d−1}u^{i+k}v^{j+l−1}.

Coefficients are reduced modulo two. Terms with coefficient zero are
discarded before interpreting negative exponents; exponents x≥2 or y≥2
give zero. The formula covers degree-zero interactions, e.g. [uv,y]=u,
[u³,xy]=yu², and [xuv,y]=xu. Unit interactions vanish by normalization.

## 5. Characteristic-two scope and arbitrary fields

The ordinary bracket is symmetric in characteristic two and alternating:
[F,F]=0. Its shift by one is the ordinary graded Lie convention requested.
There are additional operations not recoverable by dividing a self bracket
by two. Direct relative insertion yields the restricted degree-one squares
(xu)^[2]=xu, (yv)^[2]=yv, and u^[2]=0. The even-degree divided square also
need not vanish: actual cochains give sq(xuv)=xuv² and sq(yuv)=yu²v.
These examples falsify a claim that zero self bracket forces every square
to vanish. The submission expressly excludes a full squaring/brace answer,
so this is a scope limitation rather than a contradiction of its ordinary
Lie answer. A strict Gerstenhaber or restricted presentation would require
additional formulas and validation.

All constructions, chain maps, matrix entries, multiplication and insertion
rules are defined over F₂. In each degree the relevant cochain spaces are
finite dimensional. For any characteristic-two field K, B_K=K⊗_{F₂}B_{F₂};
flat scalar extension commutes with kernels, images, cohomology and all
finite-degree cochain operations. The resolution proofs above also work
directly over K. Thus no perfectness, finiteness, algebraic closure or
F₂-only hypothesis is hidden. The F₄ diagnostics are useful independent
checks of coefficients, but are not the proof of this universal conclusion.

## 6. Independent source boundary

The [OWR report](https://ems.press/content/serial-article-files/46571?nt=1),
printed p.1363, Question 5, asks for the ordinary Lie structure and use of
the coefficient sequence. [Hermann v2](https://arxiv.org/pdf/1411.0836v2),
printed p.45, Section 9.6 and Lemma 9.7, identifies the seven-dimensional
category example with the displayed one-point extension. [Xu](https://arxiv.org/pdf/0805.3295),
printed p.15, Section 3.1, records the arrow action. Those relations make g
interchange the two arrows and h fix them. Setting x=g−1 and y=h−1, and
using a basis m and (g−1)m, gives precisely the nonzero x action and zero y
action above. The arrow-composition side can be reversed by passing to the
opposite algebra; reversing normalized input words respects the bracket
in characteristic two because all reversal signs disappear. The present
audit computes the displayed left-module B directly.

These locators authenticate the intended module and question. They do not
prove novelty or establish that no previous explicit Lie presentation exists.
Only prose, source locators and audit-created artifacts are public outputs;
downloaded third-party source bodies remain in this family's private folder.
