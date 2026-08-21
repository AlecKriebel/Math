# The binary fixed-linear triple-cover row has no \(\delta=0\) counterexample

**Exact candidate checkpoint:** 2026-07-25T11:36:00Z.  
**Status:** pending an independent row-specific hostile audit; not peer
reviewed.

## Statement

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\to\mathbb A^3_{\mathbb C}
\]
have total degree four and \(L_0\in\operatorname{GL}_3(\mathbb C)\).
Suppose its leading part lies in the binary half of the fixed-linear
line-triple-cover row.  Thus, after source and target changes,
\[
H_4=(P,Q,0),\qquad
P=pA(p,q),\quad Q=pB(p,q),
\]
where \(A,B\) are coprime binary cubics and \(A/B\) has degree three.
Write
\[
R=(H_3)_3,\qquad
\alpha=J(Q,R),\quad\beta=-J(P,R),\quad\gamma=J(P,Q).
\]

The degree-eight identity first makes \(R\) binary.  If \(R\ne0\) and
\(\alpha,\beta\) are constant-linearly independent, put
\[
\delta=\deg\gcd(\alpha,\beta,\gamma).
\]

**Candidate theorem.**  Every Keller map in this row with
\(\delta=0\) is a polynomial automorphism.  Equivalently, no Keller
counterexample in this row has \(\delta=0\).  Consequently every
counterexample in the binary row must lie in one of
\[
\delta\in\{1,2,3,4\}
\]
or in the constant-dependent power-fibre exception
\[
\lambda P+\mu Q=L^4,\qquad R=L^3.
\]
In the present fixed-linear row the latter condition says, after scaling,
that \(L=p\) and the cubic pencil \(\langle A,B\rangle\) contains \(p^3\).

This is a structural reduction, not an exclusion of the whole binary row.

## Proof

The abstract binary-quartic Hilbert--Burch lemma applies to arbitrary
binary quartics \(P,Q\) with \(J(P,Q)\ne0\); it does not require
\(\gcd(P,Q)=1\).  Its top identities are
\[
E_8=\gamma R_r,\qquad
E_7=\alpha U_r+\beta V_r+\gamma T_r,
\]
where \(H_3=(U,V,R)\) and \(T=(H_2)_3\).

If \(R=0\), the third component has degree at most two.  The banked
quadratic-component theorem and plane low-degree exit make \(F\) a
polynomial automorphism.

Assume \(R\ne0\).  On \(\delta=0\), the degree blocks of \(E_7\) have
nullities \((0,0,0)\).  Hence \(U,V,T\) are binary.  The signed
\(E_6\) identity then has no curvature terms, and its remaining
degree-\((1,1,0)\) syzygy block is injective.  Thus the first two
components of \(H_2\) are binary as well.  Every nonlinear term of \(F\)
therefore depends only on \(p,q\).  After a linear change, \(F\) is a
degree-four plane Keller map together with a triangular shear in the
third coordinate.  The unconditional plane low-degree theorem makes the
plane block an automorphism, so \(F\) is an automorphism.

The same abstract lemma shows \(\delta\le4\).  If \(\alpha,\beta\) are
constant-linearly dependent, it gives
\(\lambda P+\mu Q=L^4,\ R=L^3\).  Since
\[
\lambda P+\mu Q=p(\lambda A+\mu B)
\]
is a fourth power and \(p\) is irreducible, unique factorization forces
\(L\sim p\) and \(\lambda A+\mu B\sim p^3\).  Rescaling gives the stated
normalization.

## Verification and disclosure

The abstract lemma, including its height-two hypothesis, weighted degree
table, signed \(E_6\) formula, \(\delta=0\) injection, and power-fibre
normalization, is independently reconstructed and fault-tested in

```text
../../fixed_quadratic_line_doublecover/binary_locus/
  audit_abstract_hb_e6_hostile/
```

This corollary uses no normal form for the degree-three cover \(A/B\), so
all of its left-right moduli remain present.

AI systems materially assisted the proof, verification, and exposition.
Exact checks establish facts about the encoded algebra; they are evidence
supporting the proof, not peer review.

The abstract input has passed an independent audit.  This row transfer is
still labeled a candidate until a separate hostile review has checked the
fixed-linear scope, the two automorphism exits, and the power-fibre
specialization.
