# Independent geometry and exact-algebra audit

Scope: independently audit the frozen claim in `public/PROOF.md` for problem 30003571 / PR 521. No original source files or external services are modified. All audit artifacts remain in this directory.

Target hypothesis: the proposed globally smooth positive metric on the ample tautological bundle loses total-space curvature positivity at finite time under the stated probability-normalized flow. Success requires a correct projectivization convention, global chart compatibility, an exact continuum positivity certificate, an independently derived central-fiber evolution, and an exact finite-time negative value.

## Checkpoint 2026-10-13 03:08 UTC

Completion estimate: **20%** of this geometry/algebra audit.

Read repository instructions and frozen proof as hypotheses. Confirmed the workspace remains on `main`. Identified the root weight and the asserted normalized flow as the claims to verify. The default Python environment lacks SymPy; the existing repository virtual environment has SymPy 1.14.0 and will be used without altering dependencies. No supplied verification script has been run.

Preliminary deduction: for the convention that projectivizes lines in `E*` and takes the dual tautological bundle, scalar cancellation gives `P(E*) = P¹ × P¹`, while `O_E(1) = O(1,1)`. The stated transition weights agree with its square. This will be documented and checked in the final report.

## Checkpoint 2026-10-13 03:12 UTC

Completion estimate: **75%** of this geometry/algebra audit.

The new `verify_independent.py` passed 54 exact checks without importing or running either supplied verifier. It differentiates the four chart weights in real coordinates, reconstructs their complex Hessians through Wirtinger derivatives, and generates a Bernstein certificate for the exact determinant. The certificate gives the stronger uniform bound `AB-Q >= 1/48` on `[0,1]²`; the same method gives `A >= 1/96` and `B >= 3/2`. These are continuum statements and include the chart boundaries.

The central horizontal evolution was solved independently using the generator matrix on the polynomial basis `(1,x,x²)`. It gives `w = epsilon - delta(1-q)/6 + delta(1-q)x + delta q x²`, with `q = exp(-2t)`, hence exactly `w(0,log(2)/2)=-1/96`. The two eigenmodes and the claimed Legendre formula agree with this separate derivation. The local real-coordinate Laplacian was also checked for a generic smooth radial function.

A first verifier run encountered only a symbolic-log simplification limitation in a valid positive-radius transition identity; using SymPy simplification before factoring fixed the checker. No mathematical formula was changed. Remaining work: write the global bundle/analytic argument, normalization controls, and explicit limitation statement; compare the provided code against the independently checked equations.

## Checkpoint 2026-10-13 03:17 UTC

Completion estimate: **100% of this assigned geometry/algebra audit**.

Completed `REPORT.md` and strengthened the normalization controls in the independent checker. All **57 exact checks** pass. The root-weight/time conversion preserves the negative sign with the translated coefficient and time. Removing the anticanonical probability denominator instead changes the evolution and makes the central pole coefficient grow, confirming that the negative result depends on the stated normalization. Compared the supplied proof/verifier formulas only after deriving the independent result; found no inconsistency in the checked geometry or algebra.

Strongest verified result: conditional on the displayed normalized flow having a unique finite-time smooth solution, the proposed globally smooth strictly positive metric loses total-space positivity at `(0,0,log(2)/2)`, with exact horizontal coefficient `-1/96`.

Exact remaining gap outside this sub-audit: published-equation/source-scope authentication and verification of the smooth finite-time existence theorem's applicability. No repair to the checked chart patching, continuum positivity, Laplacian, or finite-time sign computation is needed. No supplied source file, external service, branch, commit, or push was changed.
