# 30005299: Weddle quartics, five-turn partial result

**Overall: unsolved after 5/5 substantive author turns. Independent review pending.** No full characterization of the unrestricted original target, and no novelty or priority assertion.

The exact source is Question 2 in Luca Chiantini's *Generalized Weddle loci*, OWR 54/2022, printed p. 3103. Its web has projective dimension three: four independent quadrics in complex P^3 in the convention used here. It is not a three-quadric net or a system required to have six base points. Singular and nonreduced quartic determinants are retained.

## Candidate partial results

- The Weddle-quartic image closure has dimension exactly 24 in the fixed P^34 of quartic equations. The general determinantal-quartic locus has dimension 33. Hence a general determinantal quartic is not Weddle; the codimension is nine. The Weddle map is generically finite onto its image. Both differential rank lower bounds have exact modular-minor certificates; written universal upper bounds complete the proof.
- A given linear determinant matrix is constant-left-right equivalent to a Jacobian of four quadrics exactly when its explicit 24-by-16 symmetrizer kernel contains an invertible matrix. This is not a test on the quartic alone. The packet gives a smooth Weddle quartic with a Jacobian representation passing the test and its transpose failing it completely, with exact rank and smoothness certificates.
- A smooth complex quartic (X,H) is Weddle exactly when it admits a fixed-point-free involution sigma with sigma^*H an H-Ulrich line bundle. Equivalently H·sigma^*H=6 and 2H-sigma^*H is not effective. The proof credits classical polar geometry, Beauville's determinantal–Ulrich theorem, and the fixed-point-free trace formula.
- For singular hypersurface schemes, an intrinsic involution/trace criterion characterizes those admitting an everywhere-corank-one Weddle presentation. Fixed points may occur; a trace-zero condition replaces the smooth freeness argument.
- Explicit quadruple-plane and four-plane webs show why higher-corank presentations cannot be ignored. Controlling all inequivalent singular presentations, their noninvertible cokernels, and actual realization at boundary points remains unresolved.

## Artifacts and reproduction

Read the five immutable substantive-turn files in order. Run `python checks/check_symmetrizer.py` and `python checks/check_dimensions.py` using Python with SymPy; both are locally authored exact checks. They reconstruct their saved JSON receipts. No downloaded executables or new software installations are needed. The dimension checker uses the prime 101 only to exhibit nonzero integer minors; its conclusions are in characteristic zero. It does not claim a finite-field sample proves an arbitrary universal statement without the accompanying argument.

`FROZEN_MANIFEST.json` fixes the authored public packet. Full upstream records, PDFs, extracted source text and exploratory scripts are reading/scratch material and are excluded from that manifest and any publication payload. `source_manifest.json` distinguishes local source hashes from web-only references.
