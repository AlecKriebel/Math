# Root target and proof inspection

Root inspected the complete current 19-file exact-head author packet (including all historical proof/checker copies via exact byte identity) at PR411 head `ac8b960bdda61c154cc30d7e3aba70389a9b139e`. This is an author-aware inspection, not an independent blind review. The new geometric and algebraic families are still pending.

## Exact target

Fresh HTTPS retrieval of the original Morgan–Pansu TeX succeeded, redirecting from the `~pansu` to `~pierre.pansu` path. SHA256 `33d853a6de512584aeedfaf5b491bcc7f0cf02d2964e8b1f1be67a5b3b97c48e`, 42288 bytes. Section11, Question14, printed PDF p12, asks whether local maxima of `F=Scal²/|Ric|²` among left-invariant metrics on a fixed solvable group satisfy `Ric=cI+D` for a derivation of that group's Lie algebra. It imposes no real-type, complete-solvability, global-maximality or strictness restriction. The accessible PDF independently agrees. [Original source](https://www.imo.universite-paris-saclay.fr/~pierre.pansu/problems_MTDG.pdf).

The fresh aggregator request returned HTTP429; the web tool also yielded no accessible mathematical content. Its current wording/openness is unverified. The exact original problem is verified; a blank or inaccessible live status is not evidence of present openness.

Fresh Lauret–Will I v2 PDF retrieval succeeded (279890 bytes, SHA256 `22d5fa5e6daa63a3c2a6bf231450024e0b06af91190f2c5f4eae4cc6da98e878`). Theorem1.5 distinguishes Ricci-soliton local maxima from solvsoliton global maxima. The statement following Lemma6.12 explicitly leaves small-parameter local maximality unanswered. Section6.4 displays the exact `D_t=J⊕tE12` family and value1/3. These statements are context and attribution; a comprehensive priority audit has not yet passed. [Primary version](https://arxiv.org/abs/1808.01380v2).

## Author-aware deductions checked by root

Jacobi is automatic for `[e0,v]=Av` with abelian codimension-one ideal; the derived algebra lies in that ideal. The simply connected integration is a solvable group. The four Koszul connection formulas lead to `Ric00=-tr(S²)`, `Ric0V=0`, `RicVV=[K,S]-(tr A)S`. Since the orbit is traceless, `s=|S|²`, `q=|[A,Aᵀ]|²` yield `F=s²/(s²+q/4)`, and `F≤1/3` is exactly `P=q-8s²≥0` for positive s.

Every nearby positive-definite Gram matrix has a fixed-ideal orthonormal basis given by `T=G_V^(-1/2)` and unit complement `c(e0-G_V^(-1)β)`, where `c=(α-βᵀG_V^(-1)β)^(-1/2)>0`. The complement shift acts trivially on the abelian ideal. Its bracket matrix is `c T^(-1) A T`, smoothly approaching A. Scaling leaves F unchanged. Hence a full nearby conjugacy result covers every nearby metric, including cross terms.

For a conjugate, `I+A²` is a smooth rank-two idempotent onto `ker A²`; it need not be orthogonal. Local orthonormalization and the nonzero nilpotent block provide smooth f3,f4 with positive v. The quotient has trace0/determinant1. Its oriented skew coefficient is the positive `k=sqrt(1+a²+b²)`. Retaining all four lower-left entries gives the stated six-variable transverse slice; no invariant orthogonal splitting is silently imposed.

The written quadratic form and remainder are algebraic claims pending new exact reproduction. Conditional on the displayed identity, the analytic implication is fully valid: on a compact interval `v∈[v-,v+]⊂(0,1/2)`, put `c0=1-4v+²`. Each mixed block is twice `[[1,±v],[±v,1-3v²]]`, with determinant `1-4v²` and trace `2-3v²`. Its smallest eigenvalue is at least `2 det/trace≥1-4v²≥c0`. The a,b coefficient is larger. Thus `Q≥c0 rho²`.

For `rho=|ξ|≤1`, k≤sqrt2, k-1≤(a²+b²)/2, and `|wx-yz|≤(x²+y²+z²+w²)/2`. Bounding the six remainder terms separately by `12`, `12sqrt2`, `12sqrt2`, `sqrt2`, `1/2`, and `1` times rho³ gives `|R|≤(13.5+25sqrt2)rho³<50rho³`. Therefore `rho≤c0/100` gives `P≥c0 rho²/2`. Uniformity handles the flat v direction; semidefinite Hessian alone is not used. `s≥v²/2>0` prevents undefined F.

The candidate's diagonal Ricci operator excludes `Ric=cI+D`: the rotation bracket forces c=-u²/2 and d0=0; the nonzero nilpotent bracket then demands d3=d0+d4=0 although d3=u². The fixed Ricci-minus-scalar operator is diagonal; allowing arbitrary off-diagonal derivations does not evade that equation. Isometry to a solvsoliton realized on a different group does not satisfy the literal equation on this group.

Both displayed conjugations give the same-group comparison B, with `F=9/17>1/3`; exact arithmetic reproduction remains pending. No global-maximum statement replaces the local assertion. The maximum is non-strict, and no endpoint u=0 or1/2 is included.

## Custody and remaining work

All18 entries in the author PUBLICATION_MANIFEST verify by bytes, SHA256 and Git blob SHA1. All6 frozen-author files verify against their original size/SHA256 list. The original standalone pre-audit manifest digest and original pre-path-adjustment independent script digest have no corresponding bytes in this19-file packet and remain UNATTESTED. Presently available files verify; absent historical artifacts are not retrospectively certified.

New independent mathematical reviews and corruption-aware reproduction are pending. Then priority review, preprint preparation, new sequential package adversaries, production Zenodo publication, native GWS row, and final guarded merge remain. No novelty or historical firstness claim is accepted. Author attempt count remains2/5; this inspection adds zero new proof-search turns.
