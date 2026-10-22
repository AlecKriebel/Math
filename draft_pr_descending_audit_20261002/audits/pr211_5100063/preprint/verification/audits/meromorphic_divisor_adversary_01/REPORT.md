# PR211 / 5100063 — independent meromorphic-divisor adversarial audit

**Result: the global meromorphic argument is verified in the stated nondegenerate elliptic-caustic scope. No blocking mathematical defect was found.** The full independently authored proof is `INDEPENDENT_DERIVATION.md`, frozen before any numerical control or inherited review/checker was read. Parent retains all source-scope, promotion, priority, and publication decisions. The overall research goal remains active and incomplete.

## Exact claim and success criteria

For 0<k<1, odd primitive N>=3, 0<tau<N/2, gcd(tau,N)=1, v=2K tau/N, and the explicit positive edge function E in frozen PROOF equation (8), the cyclic sum F has divisor

```
[R+L/2]+[R+L/2+2iK']-[R]-[R+2iK'],
L=4K/N, R=3K+iK'+v.
```

Consequently F(u)F(u+2K) is a positive real constant. The algebra connecting this E to the bilinear complex continuation of actual focal inverse outer-edge determinants has also been independently reconstructed. The real canonical parametrization is a published input from Stachel Theorem 4.3 and (4.9), checked in the frozen published source. No global divisor or pole argument from a geometry agent, another PR, or an inherited checker is assumed.

Failure criteria included any omitted pole, wrong Jacobi period sign, hidden zero leading coefficient, unexamined critical fiber, translated double-pole multiplicity, pole/zero collision, identically zero cyclic area, or use of the outer locus's foci instead of the original foci. Each is addressed by explicit identities or local orders in the derivation.

## Main independent checks

1. The complex norm is a bilinear sum of squares. The inversion components and edge determinants are meromorphic quotients, not functions involving conjugation. Independent determinant expansion and distance factorization recover E with its full positive normalization.
2. Exact DLMF 22.4 transforms give real period 4K and imaginary antiperiod 2iK' for E. All common sn,cn,dn poles are removable in E because numerator and denominator both have pole order three with nonzero leading coefficients.
3. The complete degree-two sn fibers give the first-factor roots r±v and second-factor roots r±3v. L1=Z cn(3v) is nonzero for odd primitive N. The first roots are noncritical; the only second-factor critical case is N=3,tau=1.
4. At a_±=r±v, H2(a_±)=4k'^2 h²dW>0 and the exact quadratic coefficients are ±i C0 V/(4k'^5 h³CdW). This independently excludes collisions of the two denominator fibers and verifies the coefficient signs without numerical fitting.
5. In N=3, H2 has a double zero at K+iK'; dn has a simple zero there. Their quotient has an actual simple pole with residue -2i C0 q/[Z k'(d+C)²]. It is a single local point with the stated multiplicity.
6. At every translated point a_+-j delta, exactly one summand contributes each quadratic coefficient, with indices j and j-1 modulo N. They cancel. The same bijection holds after the imaginary antiperiod translate. Second-factor roots add only simple terms, including the N=3 coalescence.
7. Bézout gives period L=4K/N. On C/(L Z+4iK' Z), only two simple poles are permitted. Real E>0 proves F is nonzero. Compactness and antiperiodicity then prove that both permitted poles actually occur.
8. Odd reflection about R gives zeros at R+L/2 and its 2iK' translate. They are visibly not permitted pole locations; degree equality makes them the exact simple zero divisor. The shifted product is holomorphic and nonzero on the torus, hence constant, positive real on the real line.
9. The exact identity J_{-f}(Q(u))=-J_f(Q(u+2K)) uses the original foci and preserves signed shoelace area. Odd N gives 2K congruent to L/2 modulo L, so the analytic product is the requested geometric product.

## Primary-source details and an auxiliary source error

The frozen v11 source's introduction defines the setting as a confocal ellipse pair; its preliminaries define signed shoelace areas, §3.9 defines unit circles at the original billiard foci and applies primes to outer vertices, and Table 10 identifies k904,a. This agrees with the target examined here. The companion and historical-status questions are left to the assigned source family.

Stachel's published text near p.1613 contains the auxiliary line dn(u+2kK)=(-1)^k dn(u). The official [DLMF 22.4 table](https://dlmf.nist.gov/22.4#T3) gives dn(u+2K)=dn(u). The submitted proof uses the correct sign; its argument does not inherit that erroneous auxiliary source line. The independent controls verify the correct transforms directly. Addition and local derivative inputs were checked against official [DLMF 22.8](https://dlmf.nist.gov/22.8) and [22.13](https://dlmf.nist.gov/22.13). All exact transforms and local expansions used are recorded in the derivation.

The primary PDF hashes were checked against the assignment:

```
invariants_v11.pdf  c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da
stachel_published.pdf  9121028d7295435740cebb25ec60abe1a0dcc4e96686c226b1b6533bd49515d8
```

No primary source PDFs, extracted text, or renderings are included in this authored artifact set.

## Boundary and counterexample controls

- Circle: separately verified by rigid rotation of a regular star; central inversion preserves its fixed radius and signed-area value. The k>0 proof is not extended through a singular formula.
- Repetition: if odd N repeats a least period n, both n and repetition count r are odd; each shoelace area multiplies by r, hence the product by r². The primitive proof therefore extends to repeated odd orbits.
- Nondegenerate hyperbolic caustic: every real tangent chord crosses the x-axis inside the ellipse, forcing vertex y signs to alternate. Its period is even. This rules out a missing odd case without imposing a new target assumption.
- Collapsed focal segment: nonaxial separatrix edges reverse y sign; an axial edge forces the period-two axial orbit. No nontrivial odd finite orbit arises. Coincident vertices or intersections of parallel outer tangents require separate definitions and are not silently supplied limiting areas.
- No counterexample was found. Detailed attacks on common poles, fiber at infinity, all four sn critical values, divisor collisions, accidental numerator cancellation, and translation multiplicities are preserved in the independent derivation.

## Reproducible controls and their limits

`independent_controls.py` was written after freezing the derivation and imports no submitted or inherited module. The assigned existing interpreter was used by its exact given path, without resolving its symlink. Versions: Python 3.14.6, Sympy 1.14.0, mpmath 1.3.0. Run from this artifact folder:

```
/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python independent_controls.py
```

The completed results in `CONTROL_RESULTS.json` are:

| Control | Result | Evidentiary role |
|---|---|---|
| Eight independently assembled polynomial identities | All reduce exactly to zero | Exact algebra controls |
| Rational lattice enumeration | 1,053 primitive odd pairs through N=101; only (3,1) coalesces | Finite cross-check of the proved universal arithmetic |
| Complex/real 90-digit diagnostics | 24 cases, k=0.1,0.55,0.93; primitive stars through N=25 | Diagnostics only |
| Edge determinant formula | Max normalized discrepancy 6.08e-92 | Checks normalization and bilinear continuation |
| Shifted-product constancy | Max normalized discrepancy 2.54e-90 | Diagnostic, not proof |
| Exact local quadratic formula | Max normalized discrepancy 2.35e-35 at displacement 1e-17 | Diagnostic Laurent check |
| Common Jacobi pole removability | Max normalized discrepancy 6.24e-35 | Diagnostic omitted-pole check |
| N=3 simple residue | Max normalized discrepancy 1.45e-36 | Diagnostic critical-fiber check |

The numerical residual size is consistent with the symmetric finite-displacement error, not an interval certificate. No universal inference rests on floating-point agreement. The exact proof is the frozen derivation; finite controls corroborate its checkable identities and arithmetic.

An alternative explicit Jacobi model with the same divisor is given in `ALTERNATIVE_MODEL.md`. It checks the global structure but is not offered as an independent proof of the already established divisor.

## Strongest result and exact remaining gap

The global complex-analytic implication and its local multiplicities are verified for every allowed k,N,tau, with no outstanding gap identified in that component. The inverse-edge algebra is verified independently. The canonical parametrization and standard elliptic-function theory remain acknowledged published inputs. Parent still needs to integrate independent geometry/source audits and decide any promotion; this artifact supplies neither historical novelty clearance nor final publication clearance.

No inherited review/PASS/checker was read. No copied submitted replay was run. No external communication, Git/index/ref mutation, provider/PR mutation, database/queue/tracker/deposit change, or write outside the assigned folder was performed by this audit.
