# Independent audit: the once-punctured super-Kähler line test

Problem 30004711. Audit date: 7 October 2026.

Frozen target: `AUTHOR_APPROACH_2_SUPER_KAEHLER_LINE.md`, SHA-256
`602322f2a58d6294e875e648dd6f6cc9a3a47c0b480d9f8a0479996a235916b0`.
The target was inspected and its hash verified; its bytes were not changed.

## Verdict

**Accept the conditional local calculation and the compactified odd-spin line calculation. Accept the harmonic-projection criterion. Do not accept this as a proof of the literal OWR torsion-volume identity.** A short, separate clarification is required to pin down tangent versus cotangent, the orientation sign, and what “canonical integral” means. It does not change the magnitude 1/32.

Specifically:

1. The complex 1|1 holomorphic splitting is canonical over an ordinary complex base. The displayed left-derivative Hessian and its Berezinian are correct, including the product of the two odd mixed entries.
2. With a fixed real-density/Euler convention, odd integration gives the Chern curvature of the odd tangent line. The complex determinant calculation by itself does not choose the real Berezin orientation.
3. On the unrigidified compactified odd-spin component, the asserted global identities hold:
   `F = H^(-3)`, `F^∨ = H^3`, `H^2 = λ`.
   They hold at the Ramond boundary, not merely on smooth elliptic curves.
4. Consequently, with ordinary complex orientations,
   `∫ c1(F) = -1/32` and `∫ c1(F^∨) = +1/32`.
   These are compactified stack characteristic numbers. Passing from them to a specified open-locus measure requires the separate representative/extension input stated below.
5. The inspected sources do not establish that the actual once-NS-punctured genus-one Goldman/torsion form satisfies the full super-Kähler and identified-metric hypotheses. The hyperbolic projection connection is also not identified with the actual torsion connection here.

The accompanying `APPROACH_2_CONVENTION_CLARIFICATION.md` makes the accepted statement unambiguous. No new theorem about the original raw torsion integral, no counterexample to that integral, and no final unsuccessful disposition follow from this audit.

## 1. Retraction: what is canonical, and what is not

Let `X` be a complex supermanifold of dimension 1|1 over `C`, with no odd parameters in the base. In a local chart its holomorphic structure sheaf is `O_U ⊕ O_U θ`. Its even subalgebra is exactly `O_U`, because `θ²=0`. Thus a parity-preserving holomorphic change of coordinates necessarily has

`z' = f(z),  θ' = a(z) θ`,

where `f'` and `a` are invertible. The reductions of these even subalgebras glue canonically. This gives both a canonical holomorphic retraction and a split holomorphic odd line. The same argument is equivariant for an ordinary finite orbifold group acting on such charts.

On the associated smooth real supermanifold, `θ` and `bar θ` are independent Grassmann generators before imposing a reality convention, and `bar θ θ` is nonzero. A smooth replacement `z' = z + b(z,bar z) bar θ θ` can therefore change a smooth retraction. It is not a transition in the fixed holomorphic atlas. The report correctly rules out using such a replacement to claim that its *pointwise* holomorphic pushforward is unchanged.

This argument would need modification for a family over an odd base: an odd base parameter times `θ` is an even nilpotent. The report explicitly restricts to ordinary complex numbers, so that objection does not apply. Likewise, this audit does not assert that every compactification of the *super* stack possesses the same smooth holomorphic retraction at a nodal degeneration. The algebraic calculation below takes place on the reduced compactified spin stack.

## 2. Full local algebra, signs, and normalization

Put `u = bar θ θ` and use left odd derivatives. For

`K = K0(z,bar z) + h(z,bar z) u`,

one has

`∂_(bar θ) u = θ`, `∂_θ u = -bar θ`, and
`∂_θ ∂_(bar θ) u = 1`.

For the order `G_(A bar B) = ∂_A ∂_(bar B) K`, its four blocks are exactly

`A = g + h_(z bar z) u`,
`B = h_z θ`,
`C = -h_(bar z) bar θ`,
`D = h`,

where `g = ∂_z ∂_(bar z) K0`. Crucially,

`BC = -h_z h_(bar z) θ bar θ = h_z h_(bar z) u`.

Therefore

`Ber(G) = (A - BD^(-1)C)/D`
`       = g/h + [h_(z bar z)/h - h_z h_(bar z)/h²] u`
`       = g/h + (∂_z ∂_(bar z) log|h|) u`.

The absolute value permits a fixed negative odd Hermitian coefficient; its sign is locally constant by nondegeneracy. No derivative changes if one instead uses a local complex branch of `log h`.

This calculation has been checked in an actual two-generator exterior algebra, not by treating the odd mixed entries as commuting scalars. The verification also builds the full mixed holomorphic/antiholomorphic supersymplectic block matrix. In one graded-skew convention, with `i` suppressed and even coordinates ordered before odd ones, it is

`W = [[0,A,0,B],[-A,0,-C,0],[0,C,0,h],[-B,0,h,0]]`.

Its super Schur complement gives `Ber(W) = -Ber(G)²`. The constant minus sign belongs to this conjugate-coordinate basis and its graded conventions. The passage to a real density includes the reality convention, coordinate Berezinian, square-root branch, and odd integration order. Thus one must not take an additional square root of `Ber(G)`, or silently read an absolute orientation from this complex matrix. Once those constant conventions are fixed, no additional function of `g` or `h`, and no genus-dependent numerical multiplier, appears. The local curvature coefficient above is the invariant content.

### The Chern sign must name its line

Let `V` denote the odd tangent line. Its local frame is `e = ∂_θ|_(X_red)`. Since `θ' = a θ`, we have `e' = a^(-1)e`. The coefficient transforms as

`h' = |a|^(-2) h`.

It is therefore a Hermitian metric coefficient on `V`, not on `V^∨`. The dual frame has metric `h^(-1)`. With the standard Chern convention,

`c1(V,h) = -(i/(2π)) ∂ bar∂ log|h|`,
`c1(V^∨,h^(-1)) = -c1(V,h)`.

The Euler-normalized Berezin pushforward, oriented by the complex structure of `V`, is the first of these. Reversing the real odd orientation gives its negative. This convention agrees with Stanford–Witten's identification of the Euler form with the top Chern form after choosing the complex structure of the odd tangent bundle: Appendix A.3, printed p.113 / PDF p.114. Their alternative identification with the dual reverses this orientation in complex rank one.

Accordingly, a positive `+1/32` is the `F^∨` complex orientation; the natural `F` complex orientation gives `-1/32`. The sign is fixed once the odd bundle and the real measure are fixed. It cannot be changed later to fit a desired volume.

Stanford–Witten's real-odd-rank-two normalization is `1/(2π)` in (A.6), printed p.109 / PDF p.110. This fixes the Euler magnitude. It is distinct from the map from raw torsion to their normalized measure, (A.18), printed p.113 / PDF p.114. The report correctly leaves the latter convention map to the actual application.

### Globality and comparison

The mixed derivative of `log|a|²` vanishes on a holomorphic overlap. Hence the curvature form above globalizes. For two metrics on the **same** holomorphic line,

`c1(V,hτ) - c1(V,hcan) = -(i/(2π)) ∂ bar∂ log(hτ/hcan)`.

Equality holds pointwise if the logarithmic ratio is pluriharmonic. If the available canonical metric is on `V^∨`, first invert it to get a metric on `V`; taking a ratio of coefficients on opposite duals is not this test.

A constant metric rescaling has zero curvature effect. A uniform full-form rescaling in real dimension 2|2 has Berezin-volume exponent `(2-2)/2 = 0`. Neither operation fixes a factor of two in the genus-one answer. These claims pass independently.

The elementary rank-one superdeterminant formula is also a specialization of Roček–Wadhwa, *On Calabi-Yau supermanifolds*, arXiv:hep-th/0408188v1, equations (9)–(11), printed p.2 / PDF p.3, after translating their left/right derivative and `θ bar θ` conventions. This audit credits that existing local formula; no novelty is claimed for it.

## 3. The global odd-spin line, including the boundary

Let `B` be the unrigidified compactified odd-spin component for `(g,n)=(1,1)` with an NS marking. Let `π:C→B` be the universal **coarse-fiber** stable curve; the base remains the spin stack. Write `p` for the marking and `λ = π_*ω_(C/B)` for the pullback of the Hodge line.

### 3.1 Which nodal spin structure occurs?

A stable genus-one curve with one marking is either smooth elliptic or an irreducible one-node rational curve. There cannot be a stable rational tail or a longer rational cycle with only one marking: a rational component would have too few special points.

On a smooth elliptic curve the unique odd theta characteristic is the trivial line. On an irreducible nodal genus-one curve, the relative dualizing line is trivial. The two locally free square roots of the trivial line are distinguished by gluing parameters `+1` and `-1` on the normalization. The `+1` line is trivial and has one global section. The `-1` line has no global sections. The non-locally-free NS-node alternative also has even parity: in the quasistable description its restriction to the normalization is `O_(P1)(-1)`, and its exceptional component contributes no global section compatible with the zero values on the other component. Equivalently, parity conservation in a stable spin family forces the odd limit to be the locally free `+1` root.

Thus the odd branch has a Ramond node and trivial coarse theta line on its nodal fiber. This agrees with the separately inspected explicit statement in Norbury 2608.25237v2, p.40. The nodal conclusion is essential: smooth-locus triviality alone would leave possible twists supported on the boundary undetermined.

### 3.2 Descending the orbifold theta line

Use `ρ:𝒞→C` for the coarse map of the twisted universal curve and `P` for its NS marked divisor, so `2P = ρ^*p`. Denote the orbifold log-spin line by `θ`, satisfying `θ² = ω_𝒞^log`. It has the nontrivial character at the NS marking and the trivial character at the Ramond node.

Then `θ(-P)` has trivial stabilizer characters at the marking **and** at the node, so it descends to an honest line `ell` on `C`. In these conventions

`θ = ρ^*ell ⊗ O(P)`,
`ell² = ω_(C/B)`.

The dual pushforward is

`ρ_*θ^∨ = ell^∨(-p)`.

This can be checked directly at the marking: an equivariant section in the nontrivial character is `z` times a holomorphic function of `x=z²`. The pairing between generators of `ρ_*θ` and `ρ_*θ^∨` is divisible by `x`, which is exactly the `-p` correction in the dual. At the Ramond node the character is trivial, so descent is locally free and there is no analogous extra character divisor. Tameness in characteristic zero makes invariant pushforward exact.

The spin stack can have a stacky boundary and its coarse family can have a ramified smoothing parameter. That does not invalidate the line descent or the following relative arguments. They are performed over `B`, with its stabilizers retained.

### 3.3 Base change excludes a hidden boundary twist

Every fiber of `ell` is trivial, including the nodal fiber just checked. Thus its zeroth and first cohomology dimensions are constantly one. Cohomology and base change give a line `H = π_*ell`; the evaluation map

`π^*H → ell`

is an isomorphism on every geometric fiber and hence globally. There is no residual boundary divisor in this identity. Similarly, relative duality or evaluation of the one-dimensional space of dualizing differentials gives

`ω_(C/B) = π^*λ`.

At the nodal fiber a nonzero dualizing differential is represented on the normalization by opposite simple residues at the two preimages of the node and has no zero as a section of the dualizing line. Therefore its evaluation is still an isomorphism.

Squaring `ell = π^*H` and using the section `p` to pull back the resulting identity gives the exact stack line relation

`H² = λ`.

The square root exists on this spin stack. No square root on the coarse modular curve is asserted.

### 3.4 Computing F

Let `F = R¹(πρ)_*θ^∨`. Projection formula and the preceding descent give

`F = H^(-1) ⊗ R¹π_*O_C(-p)`.

In the exact sequence

`0 → O_C(-p) → O_C → O_p → 0`,

the map `π_*O_C → π_*O_p` is the identity on `O_B`, while `π_*O_C(-p)=0` and `R¹π_*O_p=0`. Hence

`R¹π_*O_C(-p) = R¹π_*O_C = λ^(-1)`

by relative Serre duality. All these statements hold for the nodal Gorenstein fiber as well as for smooth fibers. It follows that

`F = H^(-1) λ^(-1) = H^(-3)`,
`F^∨ = H³`,
`c1(F^∨) = (3/2)c1(λ)`.

This is an independent proof of the global line identification, not a deduction from matching the source's graph sum.

## 4. Stack degree and the number 1/32

For a general pointed elliptic curve there is one odd theta characteristic. Its automorphisms over the fixed curve include the scalar `μ2` preserving the square-root isomorphism. Thus the relative generic stack degree is

`deg(B → Mbar_(1,1)) = 1/2`.

The ordinary pointed-elliptic involution is already included in integration on `Mbar_(1,1)`; it must not be divided out a second time. At a general point the spin lift can equivalently be viewed as giving total stabilizer of order four over the base stabilizer of order two. The marking's orbifold character does not add another independent generic factor to this forgetful degree. Boundary ghost automorphisms and ramification do not change the generic pushforward of the fundamental class.

Independently, over `C` the Weierstrass presentation gives `Mbar_(1,1) = P(4,6)` and `λ = O(1)`. Therefore

`∫_(Mbar_(1,1)) c1(λ) = 1/(4·6) = 1/24`.

Projection formula now gives

`∫_B c1(F^∨) = (3/2)·(1/2)·(1/24) = 1/32`.

Duality gives `-1/32` for `F`. Rigidifying the scalar `μ2` changes the integration convention; it cannot be performed silently. Indeed the odd-weight line `H` itself need not descend to that rigidification as an ordinary line.

The total canonical `F^∨` value `1/16`, with equal parity contributions, is consistent with Norbury's separately inspected p.39–40 calculation after dualizing his displayed class. It is not used to derive the odd contribution above.

## 5. Compactified class versus the open metric integral

The preceding proof certifies a **compactified characteristic number**. It does not prove that an arbitrary metric on the open line integrates to that number. The line extension, although essential, is insufficient by itself.

If `mτ` and `mcan` are metrics on the same open line, a compact exhaustion gives the difference of curvature integrals as a boundary integral of a first derivative of `log(mτ/mcan)`. An arbitrary nonzero boundary limit need not vanish. For example a metric ratio with a nonzero logarithmic `log|q|` term near a deleted divisor can change the total integral after being interpolated to an interior metric. Finite integrals alone do not remove this possibility.

The canonical-metric integral can use the separately cited canonical extension theorem (Norbury 2005.04378v4, Theorem 6, pp.37–38; the later treatment is 2608.25237v2, Theorem 5.3, p.36). This audit directly checks the algebraic line extension; it does **not** independently reprove that theorem's analytic metric-extension estimates, nor use its conclusion for the actual torsion metric without an identification. In particular, algebraic regularity of `ell` at a Ramond node is not itself a proof of smooth or asymptotically admissible behavior of its hyperbolically defined Hermitian metric.

There is no new boundary defect in the pointwise identity of §2: equal forms have equal integrals whenever those integrals are defined on the same exhaustion. But using a compactified characteristic class to evaluate either side is a separate step. The frozen report's conditional numerical conclusion is accepted with this distinction made explicit.

## 6. Harmonic projection: exact scope of the criterion

Suppose a holomorphic Hermitian line `E` is a smooth line subbundle of a Hermitian Hilbert bundle with a **specified metric connection** `D`. Let `P` be orthogonal projection and set `∇ = PD`. For sections of `E`, orthogonality immediately shows that `∇` is metric compatible.

In a local holomorphic frame `s`, write `∇s = s A`. The projected connection is the Chern connection if and only if its `(0,1)` part equals the holomorphic operator, that is

`P D^(0,1)s = 0`.

Since the fiber is one-dimensional, this is equivalent to the corresponding inner product with `s` vanishing. In that case metric compatibility gives `A^(1,0)=∂log⟨s,s⟩`, with the inner-product convention used consistently. Conversely, the Chern connection has the stipulated `(0,1)` part. Thus the criterion is necessary and sufficient.

A bare derivative after an arbitrary trivialization of a varying Hilbert space need not be metric. Holomorphicity of a differential in the *surface* variable does not prove the moduli-direction vanishing above. The report is correct on both points. To use its frame of `F^∨=H³`, the harmonic line must first be identified with that **holomorphic** dual line, not merely with its underlying real two-plane.

Norbury 2608.25237v2, §4.1.3, pp.27–28, presents the closed-surface harmonic construction and a conjectural comparison; §4.1.4, pp.28–29, discusses geodesic boundary. That is not an established NS-cusp theorem or an identification with the original torsion connection. Nor does the source's ordinary exactness discussion by itself remove the noncompact boundary issue.

## 7. Primary-source verification and the remaining proof obligations

The key cited PDFs were inspected directly. Norbury 2608.25237v2 and the Uehara–Yasui preprint were freshly retrieved and exactly matched the archived SHA-256 values. Public provenance and inspection pins are in `PUBLIC_LINE_AUDIT_SOURCE_MANIFEST.json`.

- **Uehara–Yasui, July 1990 preprint YITP/U-90-16:** printed p.2 / PDF p.2 explicitly restricts to compact genus at least two; printed p.4 / PDF p.3 uses a closed-surface group and hyperbolic elements; printed p.13 / PDF p.7 contains (51). Printed p.40 / PDF p.21 explicitly leaves maximal rank unproved and cites other work for integrability. These scope and caveat statements were visually checked. The publisher's 1992 abstract was also checked. Its full revised text was not obtained, and the preprint caveats are not attributed to the uninspected final text.
- **Penner–Zeitlin, 1509.06302v4:** Omnibus B, pp.4–5, constructs a real punctured super-Teichmüller form with a negative odd square block. This does not state the needed full type-(1,1) theorem in the canonical complex genus-one splitting. There is also a visible factor-of-two convention issue between B's body display (p.5) and C's displayed bosonic Weil–Petersson form (p.7). Do not cite these displays alone as a fully verified equality of normalizations. Uniform scaling still has no effect on the 2|2 curvature result.
- **Stanford–Witten, 1907.03363v5:** (A.6), (A.17), (A.18), and the complex/dual orientation discussion were read at their exact locations. Footnote 67 establishes the intended negative odd-block comparison, not the missing punctured complex identification.
- **Norbury, 2005.04378v4:** (40), p.36, provides the canonical odd Petersson metric. A formula for the odd block alone does not establish the required mixed and nilpotent terms of the entire actual super form.

Accordingly the outstanding application requires:

1. A specific identification of the once-NS-punctured Goldman/torsion supermoduli structure with the holomorphic 1|1 structure, and proof that its actual even symplectic form is super-Kähler there, including cusp analytic hypotheses.
2. Identification of its odd coefficient with the canonical metric on the same holomorphic line, after dualizing where necessary, or proof of a globally pluriharmonic logarithmic ratio. Alternatively, for equality of total integrals alone, an appropriate direct transgression boundary estimate can replace pointwise equality.
3. The actual real Berezin orientation, spin-parity weighting, stack/rigidification, and raw-torsion normalization map. A scalar chosen to fit genus one is not that map.
4. If the harmonic-projection route is used, a specified metric ambient connection, the moduli `(0,1)` test, and an additional identification of the resulting connection/representative with the torsion-induced one.

None has been established by this audit. The canonical normalized all-NS theorem remains credited to Norbury; the original torsion statement stays pending its convention and representative comparison. The two directed author approaches remain two distinct partial approaches, rather than a completed proof.

## 8. Reproducibility

Run `python theta_line_comparison_audit/authored/verify_line_comparison.py` from the workspace containing the frozen target. The script independently verifies the left odd derivatives, the noncommutative mixed-block sign, the full mixed-supermatrix Berezinian relation, metric-dual curvature sign, constant rescaling, exact rational stack arithmetic, and the frozen target hash. Its JSON explicitly marks the actual punctured, metric, orientation, and OWR comparisons as unverified.

No source documents, dataset contents, private correspondence, or coordination material are included in the authored deliverables. No publication or queue change was made by this audit.
