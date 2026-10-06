# Sealed independent first pass: algebra family

Frozen PR17 head: `dae2b77074945443e1b91c92f641ff9feff12235`.
Frozen `PARTIAL_RESULTS.md` SHA-256:
`8d6995c10f48640f33afc5a437766eaccead99808e7b3c7f770bb52a8e900444`.

Independence: read the statement, SOURCES, manuscript, author verification code,
and frozen independent_checks code. Did not read the historical REVIEW,
review_summary, sibling results, or root conclusions. New probes import none
of those scripts. This pass validates the stated partial results only; it is
not a fifth original attempt and contains no search for the unresolved class.

Initial verdict: no fatal algebra defect found. Approve the algebra portions
as partial obstructions, conditional on the separate geometry validation for
the divisor-cohomology and conormal-bundle arguments. The unrestricted target
remains unresolved; no publication priority or full solution is certified.

1. Over any characteristic-zero field, global CM plus the sole minimal prime
   implies primaryness. Localizing at wxyz contracts correctly because that
   product is outside the prime. Any binomial in the toric prime has equal
   coefficients, and no monomial lies in it. The Laurent quotient is a
   coefficient-one group algebra. After faithful extension to an algebraic
   closure, its finite abelian factor splits into a product of fields and the
   Laurent variables preserve reducedness. Reducedness descends to K. This
   proves the binomial exclusion without an algebraically closed-field or
   homogenization assumption.
2. The fourth Veronese differs from A by exactly the monomial u=s^2 t^2 in
   degree one. Its T=K[w,z] basis is (1,x,u,y), and
   A=T+Tx+Ty+(w,z)Tu as a direct sum of T-modules. Independently,
   A_w intersect A_z=B inside Frac(A), and rad(w,z)=m, so the two-parameter
   Cech complex gives H^1_m(A)=B/A=K(-1). This is a universal monomial
   calculation, not an extrapolation from finite degree slices.
3. u is missing even from A_m, whereas u^2,u^3 lie in it. Thus the vertex
   fails seminormality. Over C it fails the Du Bois hypothesis of MSS
   Proposition 4.9. Away from the vertex the w- and z-charts are regular; the
   punctured-locus hypothesis of Corollary 4.10 holds, but every relevant
   nonpositive-degree local-cohomology piece vanishes. Neither test settles
   the original question. No arbitrary characteristic-zero field is assumed
   to embed into C.
4. The displayed nonboundary Koszul cycle is a genuine nonzero socle class.
   The independent monomial multigrading has four K1 basis elements at
   (1,1,1,1), with only the two boundary edges (1,4),(2,3); its H1 has dimension
   one. Multiplication by each variable makes its class a boundary. The
   minimal tensor-product resolution of I gives depth Z1=3. The exact
   depth-lemma chain then gives depth B1=1, depth Z2=2, and pdim Z2=2 at m.
   Hassanzadeh Theorem 1.2 requires pdim Z2<=1 here; it fails. SD also fails.
   Adding redundant generators cannot evade the cycle bound: after a local
   change of generators, k added generators are zero, and Z_(k+2) has Z2 as a
   direct summand while its permitted bound is still one.
5. CM primaryness also makes generic length one impossible without any
   homogeneity assumption. Length two gives a^2 contained in b by primary
   contraction, also without homogeneity. The geometric exclusion of length
   two uses Proj and is explicitly restricted to homogeneous b.
6. The rank-one/reflexive algebra step for q-contained b is valid given global
   CM: S is normal, J is maximal CM at every prime, and the unique height-one
   support forces J=P^(r). This forces grading before the geometric
   contradiction. Detailed divisor geometry is reserved for its independent
   family.

Evidence: isolated byte-identical verify.py passes 135 assertions and produces
the exact frozen verification.json. New pure-Python probes pass 10,351 exact
assertions in eight groups, including signed Cech slices, T-module support,
entire multigraded Koszul slices, a sign mutation, a deleted-generator mutation,
a true-boundary control, a nonprimary contraction counterexample, and the
positive-characteristic group-algebra boundary. These are finite checks where
indicated; the universal deductions are stated above and developed in REPORT.

Initial actionable points are clarifications, not correctness repairs: retain
the positive-degree/nonpositive-degree distinction, localize all depth and
projective-dimension numbers explicitly at m, preserve the arbitrary-ideal
scope in the question, and avoid describing this as an independent review of
a full resolution. The remaining class is non-binomial primary b with nonzero
nilpotent q; homogeneous examples require generic length at least three only
after the separate geometric proof passes.
