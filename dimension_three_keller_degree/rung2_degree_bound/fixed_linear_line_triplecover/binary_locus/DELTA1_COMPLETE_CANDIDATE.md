# Candidate exclusion of the entire exact-\(\delta=1\) fixed-linear row

**Candidate checkpoint:** 2026-07-25T14:36:33Z  
**Status:** primary synthesis complete; independent hostile completeness
audit pending; not peer reviewed.

## Statement

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\to\mathbb A^3_{\mathbb C}
\]
be Keller of total degree four, with
\[
H_4=(pA(p,q),pB(p,q),0),
\]
where \(A,B\) are coprime binary cubics and \(A/B\) has degree three.
Let \(R=(H_3)_3\), and put
\[
\alpha=J(pB,R),\qquad\beta=-J(pA,R),\qquad
\gamma=J(pA,pB).
\]

**Candidate theorem.**  If
\[
\deg\gcd(\alpha,\beta,\gamma)=1,
\]
then \(F\) is a polynomial automorphism.  Equivalently, no Keller
counterexample in the binary fixed-linear line-triple-cover row has exact
\(\delta=1\).

The theorem is a stratum exclusion, not a universal degree-four
exclusion.

## Exhaustive case tree

The constant-dependent case is the power fibre: the cubic pencil
\(\langle A,B\rangle\) contains \(p^3\) and \(R=p^3\).  It is excluded
in `power_fibre/POWER_FIBRE_NOTE.md`.

Assume the three minors have height two.  Their degree-one gcd is a
linear form \(g\).

1. If \(g=p\), this is the marked component.  The two orbits of the
   residual quadratic \(R/p\) are excluded in
   `delta1_marked/MARKED_DELTA1_NOTE.md`.

2. If \(g\not\sim p\), use \((p,g)\) as binary coordinates and write
   \(q=g\).  A target change and the three common-root equations give
   \[
   \begin{aligned}
   A&=q^2(a_2p+a_3q),\\
   B&=p^3+b_1p^2q+b_2pq^2+b_3q^3,\\
   R&=c_0p^3+\frac34b_1c_0p^2q+c_2pq^2+c_3q^3.
   \end{aligned}                                  \tag{1}
   \]
   The unmarked chart splits exhaustively as follows.

   - \(a_2=0\): the first contact coefficient forces \(q^2\) into the
     three minors.
   - \(a_2\ne0,c_0=0\): \(c_2=0\) gives \(R=0\);
     \(b_1=0,c_2\ne0\) gives a second common line; and
     \(b_1c_2\ne0\) has one exact contact orbit whose lower identities
     force \(L(9,-36,16w)^T=0\).
   - \(a_2c_0\ne0,b_1=0\): every contact point has a second common line.
   - \(a_2c_0b_1\ne0\): normalize
     \(a_2=c_0=b_1=1,b_2=0\).  A saturation tree including
     \(d=0\), \(a=0\), and both cleared pivots leaves only a
     one-parameter exact contact family and a cubic higher-gcd component.
     The former forces \(L(1,-4,2u_1)^T=0\); the latter has gcd degree
     at least three.

These cases cover every zero pattern in (1).  Each nonzero contact branch
either leaves exact \(\delta=1\) or makes \(L_0\) singular.

If the tangent parameter is zero, the injective lower syzygy block makes
all nonlinear terms binary.  The resulting map is a plane Keller map of
degree at most four together with a shear, hence an automorphism by the
unconditional plane low-degree theorem.

## Audit state

Every leaf has exact SymPy and independent PARI/GP reconstruction.
The abstract Hilbert--Burch lower block has a separate fault-injection
audit.  The generic unmarked **component completeness** currently has
only one primary elimination implementation; an independent hostile
saturation replay is mandatory before promotion.

Exact algebra checks are evidence about the encoded identities, not peer
review.  The normal-form coverage and automorphism exits remain subject
to expert checking.  This work was produced with substantial AI
assistance and is not a scholarly priority claim.
