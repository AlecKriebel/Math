# Exact corrections and precision edits

No frozen submission file was edited. Apply these only to a new author revision if desired. A changed author revision needs its own fresh manifest; this audit's exact byte binding remains to the original freeze.

## 1. Concrete citation correction

In `LITERAL_SCOPE_COUNTEREXAMPLE.md`, replace:

> This standard consequence is also stated as equations (2.3)-(2.5) in Yang, arXiv:2207.06770v2.

with:

> This standard consequence is stated on p.5, equation (2.2) and the following level-curve paragraph, in Yang, arXiv:2207.06770v2.

In the `Yang2024` entry of `SOURCE_MANIFEST.json`, replace the locator by:

`pp.2-3 definition and Theorem A; p.5 equation (2.2) and the following level-curve paragraph; pp.26-27 critical-point separation`

Reason: equations (2.3)–(2.5) concern related symmetry and annular parametrizations; (2.2) is the direct stated quadratic linearization.

## 2. Recommended A(d) replacement for the topological argument-principle explanation

> Let gamma_j be the boundary curves oriented positively relative to U, so hole boundaries have negative orientation. For every a off the boundary, the signed sum of their winding numbers about a is 1_U(a). Factor the nonzero rational function f(z)-w into its finite zero and pole factors, counted with multiplicity. Additivity of winding for products and quotients then gives sum_j ind(f o gamma_j,w)=Z_U(w)-P_U. Each restricted boundary map is an orientation-preserving homeomorphism, so the left side is sum_j ind(gamma_j,w)=1_U(w). Since P_U=0, the claimed zero counts follow. This continuous-loop proof does not require rectifiable boundaries or a boundary extension of a uniformizing map.

This is a proof clarification, not a repair to a false claim. Retain the existing open-mapping and bijectivity conclusion.

## 3. Recommended common-iterate precision

After the common-iterate corollary in A, insert:

> Here the rotation-boundary exclusion ranges over periodic rotation domains of f. The Fatou and Julia sets are unchanged by iteration, and a rotation component for f^L is a periodic rotation component for f. Thus this exclusion transfers to the iterate, but the map's degree becomes d^L.

Do not replace `d^L-1` by a function asserted to depend only on `d`.

## 4. Recommended reflection identity precision in B

Replace:

> On C, g sigma_C = sigma_C g; the identity principle extends this identity to the sphere.

with:

> The rational maps g and sigma_C o g o sigma_C agree on C. By the identity principle they agree on the sphere, which is equivalent to g sigma_C = sigma_C g.

The original anti-meromorphic identity is valid; the replacement states the standard holomorphic identity-principle application explicitly.

## 5. Recommended iterate-normality precision in D

After normality of the iterates of F, insert:

> Writing any iterate exponent of f as a multiple of the iterate length plus a remainder shows that normality for F is equivalent to normality for f.

## 6. Recommended coordinate precision in E

Add:

> If a curve passes through infinity, use finitely many sphere-coordinate patches for the area-zero argument.

## 7. Preserve these distinctions without broadening their claims

- Keep the full intended target `unsolved`.
- Keep the invariant count `N<=d-1`, the periodic spherical-circle count `N<=1`, and the critical-resource counts separately scoped.
- It is accurate to say that A answers the literal individually invariant counting statement as printed in Eremenko's 2025 note under its listed hypotheses. Do not convert that into an all-period theorem or a novelty assertion.
- Keep Yang's claim restricted to the actual constructed examples being critical-point-free. Do not add a universal assertion that smooth invariant curves cannot contain critical points. The critical Blaschke circle is a counterexample to that broader assertion.
- The original printed source uses an irrational-rotation-number homeomorphism. A's topological-conjugacy hypothesis is explicit and must not silently be substituted for it in a restatement.
- No full scholarly article, extracted text, source screenshot, dataset, or private coordination record should be added to a portable public packet.
