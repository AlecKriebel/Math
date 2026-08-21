# Hostile review checklist: unmarked \(a_3=\tfrac12\) contact family

Audit `HALF_CONTACT_EXCLUSION_NOTE.md` from the original homogeneous
Jacobian identities, without importing its solved formulas.

## Stratum and normalization

- Reconstruct the unmarked exact-\(\delta=1\) chart before specializing to
  \(a_3=\tfrac12\).  Verify that the common Hilbert--Burch divisor is
  exactly \(q\), rather than the marked factor \(p\).
- Compute all three reduced minors directly and prove that their gcd has
  degree one exactly when \(z(64z-1)\ne0\).  Check the boundary fibres
  \(z=0\) and \(64z=1\) separately; do not cancel either factor.
- Derive
  \(N=q^{-1}(\partial_q-\tfrac14\partial_p)(P,Q,R)\) and prove that it
  spans the degree-one tangent space on the exact open.
- Recompute the signed curvature and the contact relation
  \(K_N=\tfrac12\alpha-\tfrac5{32}\beta\), with the same Jacobian sign
  convention used in the parent Hilbert--Burch identities.

## Gauges and lower identities

- Check that scaling the source \(r\) normalizes every nonzero contact
  parameter without changing the leading normal form.
- Replay the target shears setting \(u_0=v_0=0\), followed by the source
  shear setting \(t_0=t_2=0\).  Verify explicitly that repeating the
  target shears restores the first gauge and introduces no hidden
  condition beyond \(64z-1\ne0\).
- Starting with every coefficient of \(H_3,H_2,L\) independent, solve
  \(E_6\) and \(E_5\) again.  In particular retain
  \(\ell_{13},\ell_{23},\ell_{32},x_2,y_2,u_3,v_3\); deleting these free
  coefficients can create a false singularity.
- Confirm that the coefficient of \(r\) in \(E_4\) vanishes only after
  the full \(E_5\) solution is substituted.
- Independently derive the two quartics \(A_z,B_z\), and verify that the
  indicated \(pq^3,q^4\) minor is \(-9216z^2\).  Do not replace this
  division-free test by a generic numerical specialization.
- Check literally that the third row of
  \(L(1,-4,2u_1)^T\) vanishes using the \(E_6/E_5\) formulas, while the
  first two rows are \(M_1,M_2\).

## Mutation and scope tests

- Change one sign in the tangent, delete one of
  \(\ell_{13},\ell_{23}\), and specialize \(z\) before taking the
  coefficient minor; the independent suite must reject each mutation.
- Recheck the zero-contact all-binary exit rather than inferring it from
  the nonzero-contact calculation.
- The permitted conclusion concerns only the \(a_3=\tfrac12\)
  one-parameter component.  The cubic-root contact component and all
  boundary charts of the unmarked exact-\(\delta=1\) locus remain open.
- Exact scripts certify the encoded algebra, not the completeness of the
  parent contact decomposition, scholarly priority, or peer review.
