# Research log

## 2026-07-25T05:55:00Z

- Opened the marked-critical infinity orbit
  \(H_4=(x^4,y^2z^2,0)\), \((H_3)_3=x^3\).
- Solved the raw degree-seven identity as
  \(U=(4/3)xW+a x^3+Axyz\), with \(V,W\) otherwise arbitrary.
- After exact affine gauges, degree six has two controlling parameters
  \(A\) and \(C=A+4w_4/3\).  Its square and product compatibilities split
  the full system into four branches.
- Closed the two \(C=0\) branches by degree-five cubes followed by
  degree-four squares.
- Closed \(A,C\ne0\) directly by zero column pairs in the linear part.
- In the resonant \(A=0,C\ne0,K=0\) leaf, found the division-free identity
  \(\det L_0=(\ell_{31}/3)[x^2]E_2\).
- Added exact SymPy and independent PARI/GP checks.  Promotion is withheld
  pending hostile audit.

## 2026-07-25T06:11:00Z

- Independent hostile audit returned PASS for exactly the orbit
  \((a,c)=(0,0)\).
- Corrected one typesetting sign, recorded all target-shear and source-
  translation effects, clarified the post-shear definition of \(K\), and
  added the harmless \(K=0\) products \(v_1Q=v_2Q=0\).
- The independent reconstruction verifies the complete raw kernels and
  converses, every zero specialization, and
  \(\det L_0=(\ell_{31}/3)[x^2]E_2\).
- Python optimized-mode and strict-PARI fault injections fail closed.
- Promoted the scoped theorem.  Every other outer-infinity modulus remains
  active.
