# Release addendum: audited corrections and exact scope

Date: 2026-10-04. The author and independent-audit files are preserved byte for byte. This addendum is the current release-level clarification; the historical author status and citation locator are not silently overwritten.

## Accepted restricted results; unrestricted target remains unsolved

The independent audit accepts the written restricted proofs A–E. In particular:

- **Individually invariant curves:** N <= d-1, with every curve contained in J(f), topologically conjugate under f to an irrational rotation, and excluded from being a boundary component of a periodic Siegel disk or Herman ring. Smoothness and exclusion of spherical circles are unnecessary for this restricted theorem.
- **Periodic spherical circles:** at most one can have an irrational-rotation-number homeomorphic return map.
- **Critical-resource counts:** at most 2d-2 curves containing a critical point of f, or cycles meeting that critical set. This does not count critical-point-free curves or bound cycle lengths.
- The analytic-collar and zero-area-support arguments are conditional obstructions to the attempted mechanisms, not general counting theorems.

For curves with periods dividing L, apply the first theorem to f^L, whose degree is d^L. The result is d^L-1, not a bound independent of L. The unrestricted periodic target therefore remains **unsolved, 5/5 approaches**. The 2025 note's literal individually invariant formulation is covered by the restricted theorem under its listed assumptions; it is not silently equated with the 2009 periodic question. Novelty and sharpness have not been established.

The original printed Siegel-exclusion omission admits the standard quadratic level-curve example under a bare literal reading. The preceding source context already discusses these rotation-domain examples. This observation is a scope warning, not a solution of the intended problem or a novelty claim.

## Concrete Yang citation correction

The corrected direct locator is **Yang, arXiv:2207.06770v2, p.5, equation (2.2) and the following level-curve paragraph**. The frozen LITERAL_SCOPE_COUNTEREXAMPLE.md incorrectly points primarily to equations (2.3)–(2.5). In the frozen SOURCE_MANIFEST.json, the Yang locator should be read as:

“pp.2-3 definition and Theorem A; p.5 equation (2.2) and the following level-curve paragraph; pp.26-27 critical-point separation”.

The mathematical construction and its scope are unchanged. The critical-point-free statement concerns Yang's actual constructed examples. It is not a general theorem about smooth invariant curves: the critical Blaschke circle provides a counterexample to that broader assertion.

## Exact audit-approved winding explanation for A(d)

Let gamma_j be the boundary curves oriented positively relative to U, so hole boundaries have negative orientation. For every a off the boundary, the signed sum of their winding numbers about a is 1_U(a). Factor the nonzero rational function f(z)-w into its finite zero and pole factors, counted with multiplicity. Additivity of winding for products and quotients then gives sum_j ind(f o gamma_j,w)=Z_U(w)-P_U. Each restricted boundary map is an orientation-preserving homeomorphism, so the left side is sum_j ind(gamma_j,w)=1_U(w). Since P_U=0, the claimed zero counts follow. This continuous-loop proof does not require rectifiable boundaries or a boundary extension of a uniformizing map.

Retain the frozen proof's open-mapping argument and multiplicity-one conclusion: no interior point can map to the boundary, and f:U -> U is a conformal automorphism. Since the curves lie in J(f), U is a whole invariant Fatou component. Classification and irrational boundary dynamics force a rotation domain, contradicting the exclusion. Each bounded region therefore consumes a distinct finite pole, while the fixed point normalized to infinity consumes at least one unit of the degree-d pole fiber.

## Exact common-iterate scope

Here the rotation-boundary exclusion ranges over periodic rotation domains of f. The Fatou and Julia sets are unchanged by iteration, and a rotation component for f^L is a periodic rotation component for f. Thus this exclusion transfers to the iterate, but the map's degree becomes d^L.

A's topological-conjugacy hypothesis remains explicit. It is not silently substituted for the original source's irrational-rotation-number homeomorphism. A fixed-period estimate does not imply finiteness of the union over all periods, nor a bound on periodic cycles.

## Further accepted precision points

For B, apply the identity principle to the rational maps g and sigma_C o g o sigma_C, which agree on C. Their global equality gives commutation with the circle reflection.

For D, writing an exponent of f as a multiple of the iterate length plus a remainder shows that normality for the iterate is equivalent to normality for f.

For E, if a curve passes through infinity, use finitely many sphere-coordinate patches in the area-zero argument. The support-only obstruction does not rule out surgery on neighborhoods or other positive-area sets.

## Byte bindings

- Frozen author manifest SHA-256: 63df37afcb5592e0bde27cf8e66383025710e5fcc685d38afb954a37275d48b8
- Frozen audit manifest SHA-256: 7a79ca94f1d54e59e13c67720fb1f4a3749e529d3d334395b46fb0e7cc320ebe

The full independent review is preserved separately. No full scholarly article, source extraction, screenshot, source corpus, or private coordination inventory is distributed.
