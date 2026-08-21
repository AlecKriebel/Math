# Hostile review checklist: exceptional power fibre

The target is `POWER_FIBRE_EXCLUSION_NOTE.md`.  Do not reuse its branch
conclusions without independently reconstructing them.

## Scope and normalization

- Re-derive the complete \(E_7\) solution (3), including the claim that no
  coefficient of \(B=(H_2)_2\) or \(V=(H_3)_2\) was silently removed.
- Check that the power-fibre normal form
  \(H_4=(p^4,p^2q^2,0)\), \((H_3)_3=p^3\) is the exact exception supplied
  by the audited Hilbert--Burch lemma.
- Verify that the source shear used on \(v_9t_p\ne0\) preserves this normal
  form, preserves \(v_9\ne0,t_p\ne0\), and really kills both \(c_0,c_1\).
- Reconstruct the stabilizer action on
  \(\ell=v_7p+v_8q\).  Confirm that \(0,p,q,p+q\) exhaust the zero patterns
  and that no normalization divides by a coefficient on its zero locus.

## Exact algebra

- Independently reconstruct the weighted determinant through \(E_3\),
  preferably by sparse exterior algebra or PARI rather than copying the
  SymPy determinant expansion.
- Replay every terminal obstruction in (5), (8)--(12), (16), and
  (18)--(21).
- On the \(\ell=q,\ell_{33}\ne0\) leaf, verify that all relations used
  before \([pq^2]E_3=(8/9)\ell_{33}^3\) are necessary consequences, not a
  convenient specialization.
- On the \(\ell=p,a_a\ne0\) leaf, compute \(\det L\) after the full lower
  solution and confirm the proportional-row argument.
- Check all simultaneous-substitution hazards: in particular, when a
  parameter is set to zero, dependent formulas for \(u_i,x_i,\ell_{ij}\)
  must be resubstituted explicitly.
- Inject at least one sign, coefficient, and orbit-normalization fault into
  the verification wrapper and require each to fail.

## Plane exits

- For \(\ell=0,t_p=0,\ell_{33}\ne0\), independently substitute
  \(r=(w-G)/\ell_{33}\) and confirm plane degree at most \(6\).
- For \(\ell_{33}=0\), check that a critical point of \(G(p,q)\) would make
  the full Jacobian determinant zero.  Reprove the special cubic
  classification and the conclusion
  \(c_1=c_2=0,\ell_{32}\ne0\).
- Substitute
  \(q=(w-p^3-c_0p^2-\ell_{31}p)/\ell_{32}\) and confirm plane degree at
  most \(9\).
- Audit the low-degree plane theorem after algebraic base change to
  \(\overline{\mathbb C(w)}\), generic-degree descent, and the classical
  birational Keller implication.  Reject any hidden use of the unresolved
  plane Jacobian Conjecture.

## Verdict wording

- Separate branches with no Keller map from the zero orbit, where Keller
  maps may exist but are polynomial automorphisms.
- The strongest permitted conclusion before the rest of the binary
  \(\delta\)-table is closed is: “the exceptional power fibre contains no
  Keller counterexample.”  Do not state a universal degree-four theorem.
- Record that exact scripts verify encoded algebra and degree ceilings, not
  the cited plane or birational Keller theorems and not peer review.
