# Research log: audit of `Q2-E2-A1-B2-D2-N1`

## 2026-07-26T09:39:38Z

Started a post-freeze independent promotion audit.  Read only
`FROZEN_TAXONOMY_v1.md` and `frozen_manifest_v1.json`.  Derived the intrinsic
uniform normal form
\[
LX+K_2+K_3+h(x,y,z)(x^2,xy,y^2),
\]
with arbitrary \(L\in GL_3\), arbitrary homogeneous \(K_2,K_3\), and every
nonzero ternary quadratic \(h\).  Recorded a coefficient-pivot-independent
map (later corrected as recorded below).  Created
`verify_phase_a_uniform_nf.py`.  No working bridge or bridge checker had
been opened at this checkpoint.

## 2026-07-26 correction

Corrected the phase-A pivot routing: because a conic-embedding triple is a
basis of binary quadratics, every one of its target components is nonzero.
Thus the pointwise map is `C00`--`C14` to the uniform normal form, while
`C15`--`C44` are intrinsically empty.  The checker now retains this
distinction.

## 2026-07-26 downstream hostile audit

Opened both working notes and all four exact scripts.  All four upstream
scripts execute successfully.  Independently reconstructed the raw binary
degree-seven compatibility system from the full 12 coefficients of the
binary cubic \(V\), the full 18 coefficients of \(H_2\), and all six
tangent parameters.  This confirms the forcing in equation (6) of the
binary note.

The next claimed step is not retained.  The SymPy and PARI checkers verify
the degree-six branch polynomials only after setting \(V=0\), replacing
general \(H_2\) by one displayed \(r^2Z\), and specializing the tangent
parameters to the claimed post-solve forms.  They do not compute the
degree-six compatibility after the full degree-seven solution or prove that
the resulting branch list is necessary for arbitrary lower terms.
Recorded this as the smallest fail-closed gap; no later aggregate audit
prose was used to bridge it.
