# PR200 / k115 — independent direct-geometry audit

**Verdict: verified within the submitted strict scope; no blocking mathematical defect found.** The claimed product is constant for a fixed proper confocal elliptical caustic whose real billiard family has primitive least period divisible by four. Both foci, all primitive admissible winding numbers, and every real phase are covered. No conclusion about novelty, historical priority, or current openness is made.

The strongest verified result is the full constancy theorem under those hypotheses. The direct one-focus divisor proof also shows that, for a noncircular ellipse and proper elliptical caustic, a primitive period not divisible by four does not have this focal-product constancy. This supplementary parity statement is proved in `DERIVATION.md`, not inferred from numerical sampling.

## Independence and reading order

1. The direct tangent-intersection conic, real elliptic parametrization, generic focal polynomial, divisor strategy and adversarial challenge list were frozen at **2026-10-16 04:15:01 UTC** in `EARLY_CHALLENGE_FREEZE.md` before reading the submitted proof or any other family report.
2. The freeze SHA-256 was printed before the submitted `PROOF.md` was displayed. Disk exhaustion prevented the first hash-file write; it was persisted after space was recovered. The unchanged freeze hash is `50d58d486d580a2829cc7de6d4a6c7e7b38cdea68998f2eb8eca0f00ed64d90b`.
3. Only then was `../original_submitted_head/PROOF.md` read. No original independent review, root report, source-family report, or algebra-family report was read.
4. The completed derivation uses a direct **one-focus quadratic factorization** and the torus with real period `4K`, rather than the submitted proof's paired two-focus fourth-degree function on a torus with real period `2K`. Its final factorization was completed after comparison with the submitted proof; this is not represented as a wholly blind completed proof.
5. Standard Jacobi facts were authenticated directly against NIST DLMF. The supplied literal source text was consulted only for the original `k115` row and definitions. Third-party mpmath/SymPy packages in the algebra family's runtime directory were imported as software; none of that family's mathematics, code or reports was read.

## Checkable independent mechanism

Put `alpha²=a²-lambda`, `beta²=b²-lambda`, `k=c/alpha`, and choose `0<v<K` with `sn(v)=sqrt(lambda)/b`. The direct chord support-function tangency calculation proves, without an unproved canonical-parametrization theorem, that every admissible oriented step has

\[
 P_i=(a\operatorname{sn}(w_0+i\delta),b\operatorname{cn}(w_0+i\delta)),
 \qquad\delta=2v.
\]

The two consecutive tangents meet at

\[
 Q(u)=(A\operatorname{sn}u,B\operatorname{cn}u),
 \quad A=a^2/\alpha,\quad B=b^2/\beta.
\]

With `M=B²+c²`, direct focal conic geometry gives the uniform identity

\[
 |Q(u)-(c,0)|^2
 =M(1-k\operatorname{sn}u)
 \left(1-k\frac{\operatorname{cn}\delta}{\operatorname{dn}\delta}
                      \operatorname{sn}u\right).        \tag{A}
\]

One root comes from the isotropic lines through the focus; the other is determined by the conic quadratic and the double-angle formulas. This factorization remains valid at the exceptional circular outer locus.

On `C/(4K Z+2iK' Z)`, with `p=iK'`, the generic divisor of (A) is

\[
 2[p+K]+[p+K+\delta]+[p+K-\delta]-2[p]-2[p+2K].
\]

Primitive closure means `delta=4Kr/N` with `gcd(r,N)=1`. If `4|N`, the translation subgroup contains `K` and `2K`; the full `N`-fold product therefore has zero divisor and is constant. Real factors are positive, so the ordinary product is the positive square root of that constant. The other focus is the phase shift `u -> u+2K` and has the same constant.

For `N=4`, `delta=K` makes the second factor in (A) constant and drops the pole order. Its separate divisor cancellation is valid, and the ordinary distance product is exactly `4a²b²`.

The full derivation, including completeness of the real parametrization, multiplicities and parity obstruction, is in `DERIVATION.md`.

## Adversarial challenges resolved

| Challenge | Outcome |
|---|---|
| Fixed caustic versus a period label | The theorem varies only phase for one fixed caustic. Primitive closure retains every coprime `r`, so distinct star caustics are not identified. |
| Primitive period versus repetition | Least period is explicitly used in `delta=4Kr/N`. Repeating a constant product takes a power; repetition cannot fix the proven nonconstancy at other primitive parities. |
| Infinite tangent intersections | The real normal determinant has absolute value `2 sn(v) cn(v) dn(u)/(ab[1-k² sn²(v) sn²(u)])>0`. It is nonzero at axes too. |
| Hidden real zero or denominator | `cn(v)>0`, `dn(u)>0`, `dn(delta)>0`; addition denominators are positive. Every outer vertex is strictly outside the original ellipse. Each factor in (A) is positive on the real line. |
| Wrong complex period | The one-focus squared quantity is a polynomial in `sn(u)`, with periods `4K,2iK'`. The submitted paired quantity has smaller real period `2K`; the two lattices were independently checked. |
| Missing or colliding complex zeros | The first zero is double at `p+K`; the other two are simple and distinct for `delta != K`. At `delta=K` the second factor is constant and the divisor is recomputed. |
| Outer ellipse becomes a circle | Allowed and isolated as exactly the primitive four-periodic case. No division by `A²-B²` is needed in (A). |
| Sign after squaring | All real Euclidean distances are positive. The squared product fixes their unique positive product. |
| Both foci and reversal | A real half-period changes `Q` to `-Q`, exchanging foci. Reversal permutes the same factors. |
| Degenerate limits | `a=b`, `lambda=0`, `lambda=b²` are not smuggled into the compact-torus proof. The original circle has a separate elementary result; endpoint caustics are excluded. |
| Unjustified elementary quarter grouping | The frozen challenge correctly rejects quarter grouping of a generic full distance. The actual cancellation uses the caustic-dependent step in the second focal factor. |

The attempted elementary quarter-only route was **blocked as a general proof**: the generic product over `u,u+K,u+2K,u+3K` of the full distance is not constant unless the caustic has the appropriate closure, with `N=4` special. The completed route supplies the missing step relation rather than assuming that false simplification.

## Comparison with the submitted proof

The submitted proof's tangent formula, paired squared-distance factorization, divisor multiplicities, distinction of real periods, exceptional four-periodic degree drop, cyclic order `N/2`, and final positive-square-root argument are consistent with the independent derivation. The standard period and shift identities it needs agree with the primary DLMF reference. No repair to the submitted mathematics is required by this audit.

The direct chord derivation above gives extra checkability for the cited canonical parametrization and covers all real branches explicitly. This is a strengthening of the audit's explanation, not a discovered flaw in the submitted proof.

The literal arXiv-v11 text supplied locally has the expected `k115` product of outer vertices' distances to a focus with `N=0 mod 4` in Table 2. Figure 1 and the surrounding definitions identify the outer polygon as the tangent polygon at the original billiard vertices. That is sufficient to match the audited mathematical claim to the source row. It gives no priority clearance.

## Reproducible checks and their limits

`CHECK_GEOMETRY.py` performs exact symbolic and rational group checks, and separate 70-decimal-digit numerical geometry controls. `CHECK_RESULTS.json` records all cases and versions (`mpmath 1.3.0`, `SymPy 1.14.0`).

- Exact symbolic residuals are zero for (A) and the isotropic focal root.
- Exact rational arithmetic checks every primitive winding for `3 <= N <= 200`: **6,115 cases**, with divisor cancellation exactly when `4|N`. This finite computation supplements the general proof.
- **55 positive numerical cases** cover every primitive winding for `N=4,8,12,16,20,24` at moduli `0.2,0.8,0.9999`, plus near-circle, near-degenerate and length-scale controls. Seven phases include axes and phases with an original vertex on an axis.
- The largest observed positive-case log-product phase spread is `1.751e-67`; the largest same-phase two-focus log difference is `2.336e-67`. Direct tangent intersections agree with the derived locus to relative error at most `2.885e-63`. Direct chord-caustic tangency residuals are at most `5.853e-69`. The one-focus factor relative residual is at most `1.090e-52`, attained among the demanding limiting controls.
- Seven negative controls at primitive periods `3,5,6,7,10,14` show nonzero log-product spreads, ranging from approximately `6.67e-8` to `0.128`.

These floating-point calculations are **unvalidated numerical evidence**, not interval certificates and not the theorem's proof. The proof is the exact derivation and divisor cancellation. The checks calculate each `Q` by solving its two tangent-line equations, rather than computing the product solely from (A).

To reproduce in an environment with the two pinned dependencies installed:

```text
python3 -B CHECK_GEOMETRY.py --output CHECK_RESULTS.json
```

An optional `--runtime PATH` imports those third-party packages from that path. The audit run used only the already available software tree `../math_algebra_family_01/runtime_packages`; no package installation or other audit artifact was imported. Running in a fresh environment may produce different tiny roundoff residuals while retaining the stated assertions.

## Scope and final status

Completion toward the assigned mathematical verification goal: **100%**. Exact remaining mathematical gap within the submitted scope: **none identified**. This is an independent computational/mathematical audit, not human peer review, and it does not resolve historical novelty or licensing/publication decisions.

No Git operation, branch/ref mutation, PR mutation, release, publication, or external communication was performed by this family. All authored outputs are confined to this assigned folder. `MANIFEST.sha256` is an explicit allowlist of authored audit artifacts; it excludes all third-party sources and software.
