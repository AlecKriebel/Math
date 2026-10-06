# Sealed independent compatibility derivation

Sealed at **2026-10-01T19:56:30Z**, before reading author verification code, historical review/results, provenance, or sibling audit outcomes. Frozen head: `ea6b192f7e3bc094b78bbc416bf61c609ffa5b2d`. Inputs so far: frozen `SOURCE_STATUS.md`, `source_record.json`, snapshot manifest, root/queue instructions, and complete primary statements/proofs of OWR 36/2012 pp. 2247–2249 and De Philippis–Rindler 2020 Theorem 2.10 / Lemma 2.1. This is validation of a source correction, not a fresh central proof attempt.

## Exact criterion

Audit succeeds if the draft's smooth whole-space formulas are necessary and sufficient modulo one global rigid motion for arbitrary independent vectors and arbitrary nonzero parallel vectors; zero/dimension-one/signed coefficients are accounted for; locally the same conclusions hold on adapted boxes; and no arbitrary-domain global claim or positive-only replacement is silently used. Finite symbolic tests can falsify formula errors but cannot establish completeness. The source-status correction should be accepted only with its explicit whole-space/local scope and no new-paper claim.

## Independent differential derivation

Let `E_ij=(∂_j u_i+∂_i u_j)/2`. Commuting distributional derivatives gives

`∂_j∂_k u_i=∂_j E_ik+∂_k E_ij−∂_i E_jk`.

Consequently every symmetric gradient satisfies the full compatibility equations

`C_ij,kl(E):=∂_k∂_l E_ij+∂_i∂_j E_kl−∂_i∂_l E_kj−∂_k∂_j E_il=0`.

All identities hold for distributions; no positivity, absolute continuity, or differentiability is used in this algebra.

### Independent vectors

First normalize **by congruence**, not by an orthogonal rotation. Choose an invertible `B` whose first two columns are the dual basis to `a,b` inside their span, and whose remaining columns are an orthonormal basis of its perpendicular complement. Then `B^T a=e1`, `B^T b=e2`, `x=By`, `y1=x·a`, `y2=x·b`. For `w(y)=B^T u(By)`,

`E_y w=B^T(E_x u)(By)B=(e1⊙e2) f(By)`.

For a distributional scalar coefficient, `(By)^*` means scalar pullback, with action `|det B|^{-1}<f,ϕ(B^{-1}·)>`; measures stay signed locally finite measures. This convention gives the ordinary density `f(By)` for smooth densities.

In canonical coordinates the only nonzero entries are `E12=E21=f/2`. Compatibility supplies

- `C_11,22=−∂12 f`;
- `C_11,2α=−(1/2)∂1α f`, `C_22,1α=−(1/2)∂2α f` for `α≥3`;
- `C_12,αβ=(1/2)∂αβ f` for `α,β≥3`.

Thus each transverse derivative `∂α f` has all derivatives zero, hence is constant on a connected product box or on the whole space. Subtract the transverse affine function. The remainder is independent of transverse coordinates and has `∂12 f=0`, so on a product box / whole space

`f=h1(y2)+h2(y1)+2Σ_(α≥3) vα yα`.

For smooth coefficients the profiles are smooth. For measure coefficients tensor-product test functions isolate each profile (up to an additive constant), so `h1,h2` are one-dimensional signed Radon measures. Let `H1'=h1`, `H2'=h2`, distributionally, and `v=Σ vα eα`. Then the canonical field

`w=e1[H1(y2)+y2(y·v)]+e2[H2(y1)+y1(y·v)]−v y1 y2`

has exactly this strain. Transforming back yields the draft's independent-vector expression, because `B^{-T}e1=a`, `B^{-T}e2=b`, and `B^{-T}v` is the corresponding physical transverse vector. A transformed skew matrix `B^{-T}R B^{-1}` remains skew. This explicitly justifies arbitrary nonorthogonal vectors and arbitrary scales/signs.

The coefficient check is universal: differentiating the quadratic block produces terms `a⊙v (x·b)` and `b⊙v (x·a)` which are canceled by differentiating `−v(x·a)(x·b)`. Its remaining strain is `2(x·v)(a⊙b)`. Profiles supply `(H1'(x·b)+H2'(x·a))(a⊙b)`.

### Parallel nonzero vectors

Write `b=κa`, `a≠0`, `κ≠0`, and use a unit direction `e=a/|a|`. The fixed product is `κ|a|²(e⊗e)`, so coefficient rescaling (including a negative sign) reduces to `E=e⊗e f`. In orthonormal coordinates `s=x·e`, `t_j=x·v_j`, compatibility is precisely

`∂_(t_j)∂_(t_k) f=0`, for every transverse pair `j,k`.

It follows on a box / whole space that `f=h(s)+Σ t_j p_j(s)`; no equation forces `p_j` to be constant in `s`. Choose `H'=h`, `P_j''=p_j`. Then

`u=e[H(s)+Σ t_j P_j'(s)]−Σ v_j P_j(s)`

has `Eu=e⊗e[H'(s)+Σt_j P_j''(s)]`: the `e⊙v_j P_j'` terms cancel pairwise. Smooth profiles remain smooth. Signed measure `h,p_j` are isolated by transverse test functions with independent zeroth/first moments. Their primitives satisfy `H∈BV_loc`, `P_j'∈BV_loc`, `P_j∈W^{1,∞}_loc` (one-dimensional BV is locally bounded).

### Kernel, equivalences, and boundaries

If two fields have the same strain, their difference satisfies the displayed Hessian identity with zero right side, so every first derivative is locally constant. Connectedness makes these constants global; the field is affine with skew linear part. This argument works on **every connected open domain**, without convexity or simple connectedness. On disconnected domains there is one rigid motion per component.

For the independent family, transferring a constant `C` from `h2` to `h1` changes the field by `C(a⊗b−b⊗a)x`; integration constants add a translation. For the parallel family, replacing `P_j` by `P_j+A_j s+B_j` changes the field by a skew linear term plus a translation. Hence profile ambiguity is exactly consistent with the stated modulo-rigid formulation.

If `a=0` or `b=0`, the inclusion says `Eu=0`; the scalar coefficient itself is not determined. If `d=1` and `ab≠0`, the inclusion places no restriction on a sufficiently regular scalar `u`; the kernel consists of constants. If `d=2` and vectors are independent, the transverse vector is necessarily zero.

No argument uses positivity. For example a nonzero transverse vector gives a sign-changing affine density on all of space, and one-dimensional profile derivatives may be signed singular measures.

## Local versus global

Every interior point has a sufficiently small adapted product box (an oblique parallelepiped in the independent case) contained in the open domain. All the integration arguments apply there. A single whole-domain pair of profiles is not implied merely by local compatibility on an arbitrary connected nonconvex domain.

An explicit smooth independent-case obstruction is the connected Lipschitz U-shaped domain

`Ω=((-3,-1)×(-2,2)) ∪ ((1,3)×(-2,2)) ∪ ((-3,3)×(1,3))`.

Choose a nonconstant smooth bump `b(y)` supported in `(-1,1)`. Put `u=(b(y),0)` on the right arm and `u=0` on the left arm and top connector. The definitions agree on overlaps, so `u` is smooth and `Eu∈R(e1⊙e2)` everywhere. The coefficient is `b'(y)` on the right arm and zero on the left. A global separated coefficient `h1(y)+h2(x)` would force `h1` to be constant from the left rectangle, contradicting the right rectangle. The parallel analogue uses two horizontal arms with a right connector and puts `(b(x),0)` on the upper arm; a transverse-affine coefficient cannot be zero on a lower interval and nonzero on an upper interval at the same `x`.

This validates the draft's exclusion, not a solution of an unspecified arbitrary-domain target.

## Primary-source typing caveat

The 2020 theorem is genuinely about `u∈BD_loc(R^d)` and a **signed** locally finite measure. Its part (i) literally prints `a≠±b`; without a normalization condition that includes unequal parallel vectors, for which the independent normal form is incomplete. The draft avoids this by explicitly using independence versus parallelism and reparameterizing the fixed line. For example `a=e1,b=2e1` and `u=(4x1³x2,−x1⁴)` satisfy the inclusion but violate part (i)'s literal form. Treat the printed condition as an imprecise branch label, not as a condition to copy unqualified. Other source proof typos (index signs and factors) should not replace the direct derivation above.

## First-pass disposition

No mathematical defect found in the draft's displayed smooth classification, coefficient identities, or local/nonconvex scope distinction. The strongest independently derived result is necessary-and-sufficient classification on whole space and adapted product boxes, modulo rigid motions, including signed measures with the regularity stated above. The record's domain-free wording still requires honest scoped disposition. The audit is **55% complete** pending historical reproduction, exact new controls, line-level report, and source byte hashes.
