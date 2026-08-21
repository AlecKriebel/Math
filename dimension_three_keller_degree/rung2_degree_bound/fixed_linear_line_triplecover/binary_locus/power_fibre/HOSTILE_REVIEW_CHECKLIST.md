# Hostile review checklist: fixed-linear binary power fibre

The target is `POWER_FIBRE_NOTE.md`.  Reconstruct the argument independently;
do not treat the SymPy identities as a proof of normalization completeness or
of either plane exit.

## Scope and normalization

- Check that the preceding Hilbert--Burch analysis leaves precisely
  \[
  H_4=(p^4,pC_3(p,q),0),\qquad (H_3)_3=p^3,
  \]
  with \(C_3\) coprime to \(p^3\).
- Prove that coprimality is equivalent to a nonzero \(q^3\)-coefficient and
  that a source shear preserving \(p\), together with an allowed target
  change, gives
  \(C_3=d_0p^3+d_1p^2q+q^3\).  Track the action on
  \((H_3)_3=p^3\), and confirm that neither \(d_0\) nor \(d_1\) is lost.
- Re-derive the top multipliers
  \(\alpha=-3p^3(C_3)_q,\beta=0,\gamma=4p^4(C_3)_q\)
  and the complete \(E_7\) solution.  In particular, check that
  \((H_3)_2\) remains unrestricted and no coefficient of \(H_2\) was
  silently specialized.

## Exact branch algebra

- Reconstruct the determinant identities through \(E_3\) by a method
  independent of the supplied full SymPy determinant expansion.
- On \(v_9\ne0\), audit every division and coefficient extraction leading
  from (5) to (12).  Verify that the conclusions \(t_q=0\), \(c_2=0\),
  \(t_p=0\), \(c_1=0\), \(\ell_{33}=0\), and \(\ell_{32}=0\) remain valid
  on all zero loci of \(d_0,d_1\).
- On \(v_9=0\) and
  \(\ell=v_7p+v_8q\ne0\), check separately the leaves \(v_8\ne0\) and
  \(v_8=0,v_7\ne0\).  No normalization of \(\ell\) is permitted unless its
  stabilizer is proved.  Verify the domain cancellation in
  \([r]E_5=(2/3)\ell K\) and the final singular-linear-part conclusion.
- Check simultaneous substitutions: every formula for dependent
  coefficients must be resubstituted after a parameter is killed.
- Inject a sign fault, a coefficient fault, and a deleted-modulus fault
  into the strict suite, and require all three mutations to fail.

## Zero-\(r^2\) orbit and plane exits

- Verify that (15) forces \(t_p=0\) without dividing by \(p\) or by
  \(D=d_1p^2+3q^2\), including \(d_1=0\).
- When \(\ell_{33}\ne0\), substitute
  \(r=(w-G(p,q))/\ell_{33}\) into the first two coordinates and
  independently confirm a plane Keller map over \(\mathbb C(w)\) of degree
  at most \(6\).
- When \(\ell_{33}=0\), prove that a critical point of \(G(p,q)\) forces
  the full Jacobian determinant to vanish.  Reconstruct the binary cubic
  critical-point classification, including all loci \(c_2=0\) and
  \(c_1=0\), and justify \(c_1=c_2=0,\ell_{32}\ne0\).
- Substitute
  \[
  q=\frac{w-p^3-c_0p^2-\ell_{31}p}{\ell_{32}}
  \]
  and confirm the plane degree ceiling \(10\), retaining the arbitrary
  moduli \(d_0,d_1\).
- Audit applicability of the unconditional plane lower bound after base
  change to \(\overline{\mathbb C(w)}\), the descent from plane generic
  degree one to generic degree one for \(F\), and the birational Keller
  theorem.  Reject any hidden use of the unresolved plane Jacobian
  Conjecture.

## Verdict wording

- Distinguish the \(v_9\ne0\) and \(\ell\ne0\) branches, which contain no
  Keller map, from the zero orbit, where Keller maps may exist but must be
  automorphisms.
- The strongest conclusion available here is that this exceptional power
  fibre contains no Keller counterexample.  Do not promote it to the whole
  fixed-linear row or to all degree-four maps.
- State that exact checks certify the encoded algebra and degree bounds,
  not scholarly priority, cited theorems, or peer review.
