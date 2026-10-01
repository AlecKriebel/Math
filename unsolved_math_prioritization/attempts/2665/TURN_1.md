# Turn 1: a universal-knot partial for unit or prime leading coefficient

**2665 / KP-1.6. Unreviewed partial, author turn 1/5.** The general prescribed-pair
problem and the stronger whole-class formulation remain unresolved here.

## 1. Quantifiers and the partial result

The main K3 statement asks whether each prescribed pair V1,V2 of S-equivalent
integral Seifert forms can occur on two Seifert surfaces of one knot. The
following remark asks for one knot realizing *all* forms in a given S-class.
The latter implies the former, but the converse is not a formal quantifier
rearrangement. This turn proves the stronger conclusion on a specified class.

Let V be any integral Seifert matrix, so J=V−V^T is unimodular. Remove powers
of t from det(tV−V^T), and let d be the absolute value of its leading
coefficient. Then:

**Partial theorem.** If d=1 or d is prime, there is a single oriented knot K
whose Seifert forms realize every matrix S-equivalent to V. The matrices are
realized on possibly different, possibly intersecting surfaces. In the
Alexander-polynomial-one class, K can be the unknot.

This is a classical-consequence partial, with Trotter's nonsingular congruence
theorem and the established geometric enlargement fact credited below. It is
not a resolution of composite-leading-coefficient S-classes, and no novelty
claim is made.

## 2. Singular matrices reduce integrally

We first prove the algebraic step rather than assume an algebraic reduction
can be performed on an already specified knot surface.

Suppose V is a nonempty singular Seifert matrix of size 2g. Its rational kernel
contains a primitive integral vector v. Because Vv=0,

    v^T J = v^T V.

The row v^T J is primitive since J is unimodular. Choose an integral vector w
with v^T J w=1. The alternating pairing J splits the lattice as the integral
orthogonal direct sum

    Z v + Z w  direct-sum  E,

where E has rank 2g−2. In detail, for any x the expression

    x+(w^T J x)v−(v^T J x)w

lies in E, giving the integral projection onto E and proving that the two
vectors extend to an integral basis. The restriction J|E is unimodular.
Choose any integral basis e_1,...,e_(2g−2) of E.

In this basis V has the form

    [ 0  1    0  ]
    [ 0  b  alpha^T ]
    [ 0 alpha A  ].                                      (1)

The first column is zero because Vv=0; the first row off w is zero because
E is J-orthogonal to v. The two alpha vectors agree because E is also
J-orthogonal to w. Replace w by w−b v. This kills the b entry without
changing alpha or A. Thus V is integrally congruent to

    E_alpha(A) = [ 0  1    0  ]
                 [ 0  0 alpha^T ]
                 [ 0 alpha A  ],                         (2)

an ordinary S-enlargement of A. Its skew part is a hyperbolic alternating
plane plus A−A^T, so A is again a Seifert matrix. Expanding along the first
row and column gives the exact polynomial identity

    det(t E_alpha(A)−E_alpha(A)^T)=t det(tA−A^T).           (3)

Repeat whenever the reduced matrix is singular. The dimension drops by two,
so the process ends at a nonsingular Seifert matrix A or at the empty matrix.
Only integral congruences and reductions have been used. Reversing the
sequence expresses the original V as congruences and enlargements of A.
The construction makes no geometric assertion about reducing a given
Seifert surface, which can indeed be impossible.

If A is nonempty of size 2h, its determinant is both the leading and (up to
the even-dimensional transpose sign) the constant coefficient of
`det(tA−A^T)`. In particular there is no remaining factor t. Equation (3)
shows that |det A|=d and the normalized polynomial has degree 2h. If A is
empty, that normalized polynomial is 1. Conversely polynomial 1 forces the
empty outcome, because a nonempty nonsingular matrix has positive polynomial
degree. The usual invariance of this normalized polynomial under
S-equivalence is enough for the following step.

## 3. Common nonsingular core under the stated arithmetic hypothesis

Trotter, *On S-Equivalence of Seifert Matrices*, Invent. Math. 20 (1973),
printed p.196, Corollary 4.7, states that when |det A| is 1 or a prime, every
**nonsingular** matrix S-equivalent to A is integrally congruent to A. The
nonsingularity qualifier is essential: the statement does not identify a
larger singular stabilization with A by a fixed-size congruence.

Fix a reduced core A for V. For any other W in its S-class, the reduction
above produces a nonsingular core A_W of the same normalized polynomial and
same dimension, or the empty core when that polynomial is 1. Both cores are
S-equivalent. If nonempty, their determinant has absolute value d, so
Trotter's theorem makes A_W congruent to A. In the empty case they coincide.
Thus the class has one nonsingular-core congruence type in the unit/prime
case covered by this turn.

We do not infer integral congruence from rational or p-adic congruence.
Trotter's nearby square-free determinant statement is p-adic only and is
not substituted for Corollary 4.7 at composite d.

## 4. Realization without changing the boundary knot

Two standard geometric facts are used here:

- Every integral matrix with unimodular skew part is the Seifert matrix of
  an oriented surface bounding a knot in S^3
- Every prescribed S-enlargement of a matrix already realized on a surface
  is realized by adding a tube to that surface, with the boundary knot
  unchanged; congruence is a change of integral homology basis

For the second fact, see Cha–Kim–Powell, *A family of freely slice good
boundary links*, Math. Ann. 376 (2020), Definition 2.5 and the proof of
Lemma 2.10, printed p.1016. Its one-component instance applies to knots,
and its enlargement convention is exactly (2), up to ordering the two new
basis vectors. The old-to-new symmetric entries alpha record winding of
the new handle relative to the old surface. The first fact is recalled in
the exact K3 source; a primary exposition is Kearton's *Quadratic Forms in
Knot Theory*, Theorem 1.17 in the q=1 case. No higher-dimensional knot
classification is used to assert equality of classical knot types.

Choose a knot K and surface F realizing the fixed core A; for empty A take
the unknot and its disk. Given W in the S-class, use a change of basis on F
to realize A_W, and reverse its finite reduction sequence. The geometric
enlargement fact realizes every step while keeping the same boundary K.
The terminal surface has exactly the matrix W in its specified integral
basis. K was chosen once, independently of W. This proves the partial
theorem and therefore the prescribed-pair conclusion in the same arithmetic
range.

One may choose K of genus h=half the normalized Alexander breadth: the
realizing core surface has genus h and the Alexander genus bound prevents
a smaller genus. This extra observation is not needed for the common-knot
assertion. A different knot in the same S-class need not realize the core;
for example a nontrivial Alexander-polynomial-one knot cannot bound a disk.
Thus this proof does not accidentally claim that *every* representative knot
is universal for its S-class.

## 5. What remains

When d is composite, reduced cores can be S-equivalent without being
integrally congruent. The preceding proof then supplies different possible
core knots, not a single knot simultaneously realizing them. A common
stabilization only supplies a matrix of higher genus and does not perform
the necessary geometric destabilizations on one chosen knot. This is the
precise remaining realization step.

The genus-one disjoint-pair criterion of Aka–Feller–Miller–Wieser is stronger
than algebraic S-equivalence at one step. Their Theorem 5.8 describes
S-equivalence by products of the elementary quadratic-form generators, but
the successive one-step realizations can have different boundary knots.
That transitivity alone does not fill the geometric gap; their Problem 7.7
expressly retains it. Neither the current Liu–Wang band-twist partial nor
inequivalence of two knots carrying equivalent forms resolves this question.

The next substantive turn must attack the composite-core/common-boundary
problem rather than repeat stabilization or the same prime determinant
corollary. Current count: 1/5; original unresolved. Completion estimate 25%,
with all prior results credited and the retained theorem pending independent
review as part of the eventual package.
