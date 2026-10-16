# PR210 / 5100033: classical and general theorem priority audit

Audit date: 2026-10-15 UTC. Exact source: arXiv2004.12497v11 k605,a, published k606. This is the **outer tangent polygon's signed focal-pedal area product**, for odd primitive periods and all coprime star windings, with the original common foci and a nondegenerate confocal elliptical caustic.

**Strongest verified result.** The target has a complete, independently derived reduction to an old published arbitrary-order Jacobi dn sum identity. The analytic method is established. The exact focal-foot projectivity, its bicentric contact-polygon interpretation, contact-area telescope, and opposite-focus phase alignment were freshly derived during this audit; an older primary publication of that complete geometric bridge or the exact target has not been verified. Consequently historical priority of the source-specific application remains unresolved. This is neither a novelty certificate nor a finding that the target was already published as solved.

The detailed mathematical artifact is [EXACT_BICENTRIC_DN_BRIDGE.md](EXACT_BICENTRIC_DN_BRIDGE.md). The 21-entry [PRIMARY_SOURCE_LEDGER.json](PRIMARY_SOURCE_LEDGER.json) gives actual passages, versions, hashes, and access limits. [CONTROL_RESULTS.json](CONTROL_RESULTS.json) and [check_controls.py](check_controls.py) provide fresh exact and high-precision controls. Private paper text is excluded from the authored manifest and must not be redistributed as this audit's work.

## Independence and claim discipline

I read only the intake and submitted original PROOF/SOURCES before freezing [INDEPENDENT_EQUIVALENCE_MAP_FROZEN.md](INDEPENDENT_EQUIVALENCE_MAP_FROZEN.md) at12:17:29Z. The exact initial independent mechanism was the focal-foot map from the original ellipse to its auxiliary circle, with the original caustic carried to a general conic. Only afterward did I use the completed PR211 primary ledger and reading copies as source locators. PR211's target and verdict were not transferred. Parent messages subsequently supplied a matching circle/focus observation and useful leads; the derivation and new controls here were independently executed.

The source target is not the unprimed chord-pedal product (arXiv k604,a/published k605), an antipedal product, an inverse-vertex product, an inner polygon invariant, or a construction using the outer locus's own foci. Hyperbolic and collapsed caustics are outside the claim. The source question mark records an edition's status, not an absence-of-prior-art proof.

## What the exact reductions establish

For E:x²/a²+y²/b²=1 and c²=a²−b², the plus focal foot is the restriction of the real projectivity

T_+(x,y)=(a²(x+c)/(a²+cx),a²y/(a²+cx)).

It maps E to the auxiliary circle S of radius a. It carries each billiard chord to a chord tangent to the image caustic. For caustic axes α,β and λ=a²−α²=b²−β²,

(a⁴/α²)(X−c)²+(b⁴/β²)Y²=(a²−cX)².

The quadratic coefficient difference is −c²λ²/(α²β²), so the caustic is strictly noncircular. Its focal-distance square equals its center-distance square: O is one focus. Thus the focal feet themselves form a circle/ellipse Poncelet family. No circle/circle theorem can be applied merely because their vertices are concyclic.

A second operation supplies a genuine bicentric pair. Polarizing about S sends the image caustic to the outer circle of radius R=αb²/β², centered at d=−cλ/β², while S remains the incircle, radius r=a and center O. The feet Q_j are its **contact polygon**. The transformed outer tangent vertices are the bicentric vertices R_j. Their ordered contact-area ratio is

B_+/A_R=r²/(R²−d²).

That ratio is derived here from elementary tangent geometry and the Jacobi addition identity, including physical signs for stars. It has not been assumed from an unidentified older theorem. The negative center sign is fixed by the polar equation q·R=a². A mistaken + sign would correspond to the wrong homogeneous line coordinate; the exact offset-ellipse sanity control and direct geometric projections both check the negative sign.

The canonical phase is particularly useful. If original vertices have phase w+jδ, the tangent intersections have midpoint phase z=w+v+jδ and coordinates

V(z)=(-a²/α sn z,b²/β cn z).

The ascending quadratic transform gives k_b=2√k/(1+k), K_b=(1+k)K and u=(1+k)(z−K)/2. The bicentric tangent lengths are t_M dn(u+jσ,m_b), with parameter m_b=k_b² and σ=2K_bτ/N. The exact focus switch w→w+2K becomes u→u+K_b. This is the specific paired phase; an arbitrary pair of bicentric polygons is not covered.

Consequently

B_+(w)=Γ Σ_j dn(u+jσ,m_b), Γ=r³t_M/(R²−d²).

Coprimality permutes jτ modulo N. The old arbitrary-order dn sum identity turns this into a single scaled dn with nome q_b^N=q_original^(N/2). For odd N the opposite-focus shift becomes its real half-period, so the old dn half-period product proves the exact focal-pedal invariant. Every geometric and analytic equality is recorded in the derivation, with an explicit constant and no use of the submitted adjacent-pole cancellation.

## Actual primary theorem coverage and obstructions

| Route | Primary result actually checked | Exact applicability / gap |
|---|---|---|
| General Poncelet area ratio | Akopyan–Schwartz–Tabachnikov v2 Thm3; final Thm1.3 and §7 | Odd original/tangent area ratio for **concentric ellipses**. The focal-image conic has displaced center. Affine area-ratio reasoning is valid; a general projective substitution is not. Our contact ratio is a fresh additional bridge, not the printed AST theorem. |
| Complementary area divisors | Chavez-Caliz Thm6, full proof, printed104 | **Even** n product of original and tangent areas in a concentric ellipse pair. It establishes precedent for complementary zero/pole arguments, but neither the parity nor the two geometric areas match this target. |
| General billiard support identities | Bialy–Tabachnikov §§2–4 | Fixed pedal vertex centroid and squared-distance sums, angle invariants, and even focal side-distance products do not identify the adjacent cross-product sum or paired area product. No unproved implication through those quantities was accepted. |
| Old cyclic principal-parts method | KLS-II §2; KLS-local §4 Eqs39–45 | The analytic character/divisor framework is old. A generic area summand must first have its actual poles and character established. Merely calling it a cyclic elliptic function does not prove constancy. |
| Actual arbitrary-order analytic theorem | **Khare–Sukhatme, Pramana63(2004), Eq7 p923, proof§2.1 pp924–926, Eq58 p931** | This is a directly applicable old dn sum identity after the complete geometric bridge. Its exact published text was fetched and read. It supports established-method credit, while the source-specific geometric application is not printed in the inspected passage. |
| Focal polarity / bicentric pedals | Roitman–Garcia–Reznik Thm2/Cor1 and AppendixA | Their proved observable is limiting-point pedal perimeter / elliptic focus-inverse perimeter. Our Q is a pedal at the **incircle center**, which is not a limiting point (the limiting-point quadratic has nonzero constant r²). Genuine bicentric membership after the second polarity does not repair that observable/reference-point mismatch. |
| Conjugate bicentric area products | Radic2011 Conj2, printed65–66 | An important older lead, but the all-n perimeter/area product is explicitly conjectural in the passage. Low-order2n=6,8 formulas and rotation-one conventions do not prove all odd primitive stars here. This route is blocked as a proof source unless an actual theorem or new mechanism is supplied. |
| Canonical/grid/polarity geometry | Stachel motion Thm4.3/Eq4.9; grid Thms3.5–3.6; diagonals Thm5/Cor6 | Canonical shifts and conic/polar correspondences are legitimate credited inputs. Incidence and grid conics alone do not preserve the focal signed area expression. The read motion §5 conclusions concern even tangent-length products. |
| Harmonic/Brocard family | Garcia–Reznik–Roitman2112.02545v3, Props4–6/Conj1 | Harmonic families are polar to homothetic ellipse pairs; the lateral reciprocal-area sum is proved forN3,5 and conjectural generally. Our confocal pair has four transverse complex intersections, unlike the homothetic double-contact pair. No family identification follows from a circular outer conic. |
| MacBeath triangles | Garcia–Gheorghe2026 §3 Remark3.2 and main theorem scopes | Correct name/identification atN3: circle center is a caustic focus, the other focus common orthocenter. The read results are3-Poncelet/isogonal-locus theorems, not an all-odd paired area theorem. |
| Steiner / continuous pedal curves | Reznik–Garcia–Stachel2009.02581 §§2–3 | Fixed-polygon area isocurves or full continuous-curve area do not prove a finite moving polygon's product. The individual discrete focal areas vary in actual-target controls. |
| Broad Poncelet curve construction | Hungerbuhler–Wasem2025 main statements | Universal closure/construction does not identify a metric area invariant. No exact implication verified. |

The full Stachel *Triple of Projective Billiards* PDF returned418. Only its official abstract, metadata and indexed §2 passage were inspected. I do not claim to have excluded an implication from every theorem in that paper or all later literature. The source ledger explicitly marks this limit.

## Independent falsification and reproduction

Run the portable checker with the audit's specified scientific Python:

`/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python check_controls.py`

It imports only SymPy/mpmath, uses no network or inherited checkers, and writes its deterministic result next to itself. The final successful run checks15 exact zero identities and11 cases at70decimal digits: (N,τ)=(3,1),(5,1),(5,2),(7,1),(7,2),(7,3),(9,2),(11,4),(4,1),(6,1),(8,3). Original outer tangent intersections and Euclidean projections are computed separately from the explicit focal map. The maximum new-bridge discrepancy is below2×10⁻⁶⁹. These are numerical diagnostics, not interval certificates or universal proofs.

Exact certificates cover the focal projection/projectivity, auxiliary circle, focus-switch Möbius map, transformed caustic and its focal condition, dual circle and center sign, shifted Gauss ODE, bicentric modulus and positive-tangent squared scale. Numerical checks independently test the midpoint index, circle-coordinate Gauss identity, contact ratio, exact area-to-dn trace, arbitrary-order Landen scale, complete-period scale, focus switch, orientation reversal, and final product.

The controls deliberately expose false extensions:

- **Even periods:** relative focal-product ranges are about0.0254,0.00108,0.0000454 forN4,6,8. Equality of focal areas is not constancy of their square.
- **Wrong phase:** replacing the original2K focus shift byK gives a relative product range about0.0918 in theN3 fixture. Correct half-period alignment is essential.
- **Nonconfocal/general-conic extension:** the exact homothetic3-Poncelet family in E:x²/25+y²/9=1, with caustic x²/(25/4)+y²/(9/4)=1, has focal-foot product151875/784 at one phase and492075/2704 at a quarter-turn phase, difference97200/8281. Both families transform to circle/conic Poncelet configurations, so that fact alone cannot imply the desired product.
- **Arbitrary projective area transport:** the same exact fixture has original/tangent area ratio4 at both phases, but transformed ratios−4/3 and−52/23. Projective equivalence alone cannot transport a Euclidean area theorem.
- **Harmonic misidentification:** the exact confocal intersection certificate gives x²=α²a²/c², y²=−β²b²/c² and nonzero gradient determinant. The target pair is transverse; double-contact rational-family shortcuts are not automatically available.

An early checker assertion used the wrong signs for the displayed complex intersection coordinates. This was a derivation/control typo, corrected to the certificate above before the first successful result. It did not enter the area bridge. The parent initially supplied an incorrect positive bicentric-center sign. This shard's independently derived negative center and exact offset-ellipse control exposed that error; the parent then corrected the homogeneous polar-line sign and preserved its erratum. The submitted original proof never used this auxiliary polarity. Both control corrections are documented in the log.

## Credit and classification recommendation

Keep the exact theorem and its proved scope and formulation separate from priority. Credit Stachel's canonical parametrization, classical auxiliary-circle/polarity geometry, Jacobi quadratic and addition formulas, KLS's general cyclic/principal-part methods, **Khare–Sukhatme's published arbitrary-order Landen sum identity**, and AST/Chavez-Caliz for the older billiard-area analytic/grid mechanisms where relevant. Neither a new elliptic-function method nor a first proof of a generic two-pole product should be claimed.

The strongest defensible description is: a source-specific proof/application, with an independently verified alternative geometric reduction to established Jacobi identities; historical priority of the exact focal-pedal application remains undetermined. The original proof already disclaims novelty. An added explanatory citation to the explicit generalized Landen result would improve readers' ability to recognize the analytic antecedent.

No exact older geometric theorem covering the whole target was established, so this shard does not recommend changing its classification to “previously resolved.” Conversely it does not recommend a novelty label. If an older primary theorem is later found with the same paired contact/focal object and verified half-period alignment, reclassify the relevant claim as a theorem transfer and identify the precise existing theorem and bridge. Invoking Radic's general conjecture, an unspecified contact-area theorem, or arbitrary projective area preservation would transfer or conceal the central difficulty and is blocked.

This subtask makes no manuscript publication or promotion decision. Further independent audit of the fresh bridge by the parent remains appropriate before it is used in contribution framing. No external communication, provider mutation, Git mutation, or write outside this shard was performed.
