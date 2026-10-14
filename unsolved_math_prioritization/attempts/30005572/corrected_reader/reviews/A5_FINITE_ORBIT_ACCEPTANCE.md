# Independent audit: finite-orbit ordinary normalization

Date: 14 October 2026 UTC. Shared PASS 2/5 verification, no further mathematical pass. This supplement audits FINITE_ORBIT_NORMALIZATION.md, SHA-256 a241d925353cbaa16f5bde46e75fb940d1a7cf8ab35eeed39f36ad308fc17e28, without changing it.

## Verdict

Accept all stated mathematical claims. This is a shorter independent second-annihilator proof of the already accepted ordinary lifting result. Its canonical D-fold cocycle is canonical for the specified residue primitive eta and finite reduced Gamma-stable subscheme S; it is not claimed independent of S or trace-fixed.

## Local construction and field transfers

For each closed point s outside Z_c, the local ring O_{A,s} is a regular local ring of dimension two, essentially smooth over L. The same equicharacteristic Gersten theorem checked in RAMIFIED_FIVE_ACCEPTANCE.md supplies a_s with local residue eta. This works directly at a nonrational closed point; no splitting-field extension or division is needed.

Under the adopted module-action convention, gamma maps the local object indexed by gamma^(-1)s to that indexed by s. Its local ring and residue-field maps commute with specialization. Naturality of finite-extension transfer under the resulting L-field isomorphism proves equivariance of the sum of local evaluations followed by field norms. All closed points of S are included, and Gamma permutes them. There is no assumption about a product decomposition of geometric orbits.

The element z_(gamma,s)=x_gamma-(gamma a_(gamma^(-1)s)-a_s) has zero local residues. Therefore it belongs to K_2(O_{A,s}) tensor R, so its evaluation is well-defined. The family has group coboundary equal to the same constant defect k at each s. Evaluation followed by transfer sends that diagonal constant to [k(s):L] times itself. Consequently dr_S=Dk and Psi_S=Dx-r_S is an ordinary cocycle lifting D theta-bar with the displayed residue.

## The choice-independence claims check exactly

Changing x_gamma by a constant c_gamma changes r_S by D c_gamma, which cancels in Dx-r_S.

Changing a_s by u_s with zero local residues gives u_s in the local K_2 group. The aggregate evaluation-and-transfer map is equivariant to the trivial Gamma-module C. Thus its value on gamma u-u is zero. Equivalently, the change in r_S is a coboundary of a zero-cochain in the trivial module C, hence literally zero. This proves pointwise independence of the local primitives, rather than only independence of the resulting cohomology class.

For the eta-variation assertion, choose an ordinary representative y of q and set eta'=eta+partial y. One can choose a'_s=a_s+y and x'_gamma=x_gamma+(gamma y-y). Then every z'_(gamma,s)=z_(gamma,s), so r'_S=r_S and

Psi'_S-Psi_S = D(gamma y-y).

Thus the resulting cohomology class for fixed S is independent of this change of primitive. This direct calculation confirms the stated ordinary-coboundary claim. It does not assert trace normalization.

## Auxiliary torsion and ordinary lift

For S=A[q] minus the origin, the scheme is finite reduced and Gamma-stable because the characteristic is zero and Gamma is O-linear. Its disjointness from Z_c follows from (q,c)=1. Its degree is D=(Nq)^2-1. With Nq congruent to 2 or 3 modulo 5, D is congruent to 3 modulo 5, so is prime to 5. The existence of q was independently checked in the main acceptance.

Hence this construction supplies D delta[theta-bar]=0 directly over L. Combining Psi_S with the fivefold trace-fixed cocycle using 5a+Db=1 gives an ordinary cocycle lifting theta-bar, without any division. The remaining choices listed in the note really remain: this is not a canonical unmultiplied, trace-fixed, or component-isogeny-compatible theta system.

The Q(sqrt(-5)) norm-two example has D=3, a unit of R. Thus Psi_S/3 is a valid ordinary lift when c is prime to that q. This coefficient division is legitimate and does not imply invariance under the full trace monoid.

## Combined boundary

Together with the accepted unconditional eta construction, this gives another proof of ordinary geometric K_2-valued cocycles on all source components, including ramified-5 fields. It does not settle the exact two-stage invariant-representative test, 5-primary constant normalization, ray descent, arithmetic auxiliary removal, integrality, compactification, arithmetic bad-U identities, or the relative theta-symbol formula. The original problem remains UNSOLVED.
