# PR261 / 5100021 geometry adversary review

Completed: 2026-10-12 09:51:44 UTC. Audit completion estimate: 100%.

## Finding and exact scope

**No mathematical counterexample or material geometry/domain gap was found.** The complete submitted proof appears valid for its exact stated domain: a fixed noncircular outer ellipse, a fixed strictly nested nondegenerate confocal **elliptical** caustic, primitive least period divisible by4, either original focus, original side-line feet and original vertex antipedal lines, and ordered signed areas. Primitive star winding, finite intersections, negative/zero antipedal area, four-period coincidences, both foci, reversal and fourth-degree scaling are accounted for. This is a mathematical verification judgment, not a novelty, openness, publication, merge, or priority judgment.

The all-period conclusion is verified by inspecting the candidate's analytic argument after the independent evidence freeze and checking its geometric and classical inputs. A separate all-period proof using only projective/Euclidean geometry was **not** obtained. The independent direct geometry and algebra below substantiate the proof's construction and its boundary behavior; finite numerical samples do not prove the theorem.

## Provenance and exposure order

1. At09:32:45UTC read only `/Users/alec/Documents/Math/AGENTS.md`, `unsolved_math_prioritization/AGENTS.md`, the parent-provided exact target, and a file-name inventory. Wrote `PRE_EXPOSURE_PLAN.md` and began `RESEARCH_LOG.md` before any proof/checker/source/prior-review exposure.
2. Derived direct focal-origin line formulas, geometric finiteness, fixed pedal-circle locus, four-period caustic, central-quadrilateral pedal area, and full four-period construction. Wrote the direct conic generator and performed 18 high-precision target cases plus two outside-target controls. An exact symbolic certificate covers every phase for a=5,b=3,c=4,N4.
3. At09:41:55UTC froze the independent artifacts with `PRE_EXPOSURE_MANIFEST.json`. All frozen hashes were rechecked and match at the final checkpoint.
4. Only then read the **complete** submitted `PROOF.md`, followed by `TARGET.json`, `SOURCE_GATE.md`, `source_manifest.json`, and `SHARED_PROVENANCE.md`. Checked the primary source scopes and Jacobi formulas online. Wrote fresh post-exposure incidence/projection checks, trace comparison, and exact zero-area stress tests.
5. **No submitted author checker, author receipt, previous review/checker/receipt/verdict, or independent_review document was read or run.** Shared-method provenance was read as a provenance declaration, not as mathematical evidence. No external communications, Git mutation, remote writes, PR changes, or contacts occurred. All audit writes stayed in this directory.

## Direct deductions obtained before exposure

For focus-relative consecutive vertices P,Q, put d=Q-P and k0=det(P,Q). The foot is k0(dy,-dx)/|d|². The antipedal intersection is

    ((|P|²Qy-|Q|²Py)/k0, (Px|Q|²-Qx|P|²)/k0).

Half this intersection is the circumcenter of (F,P,Q). These equations pin the original constructions without a pole substitution.

For outer semiaxes a>b>0 and caustic parameter0<lambda<b², both foci lie strictly inside the caustic: (a²-b²)/(a²-lambda)<1. A tangent cannot pass through a focus, hence k0 is never zero; a true tangent from an outer boundary point produces distinct outer endpoints, hence |d|² is never zero. This proves real finiteness independently of any Jacobi denominator.

Every focal foot lies on the circle centered at the original ellipse center with radius sqrt(a²-lambda). A caustic support line n dot X=h has h²=(b²-lambda)+(a²-b²)nx², and its foot from(c,0) satisfies |H|²=a²-lambda. This exactly agrees with normalized candidate formula12.

For a centrally symmetric quadrilateral P,Q,-P,-Q, the pedal signed area from **any fixed pole** is

    4 det(P,Q)³/(|Q-P|²|Q+P|²).

This pole cancellation is a four-period fact, not a license to change the target's antipedal focus.

The axial four-period caustic is lambda=a²b²/(a²+b²). Direct areas are 4a³b³/(a²+b²)² and4ab, with product16a⁴b⁴/(a²+b²)². For a5,b3,c4 the exact values are3375/289,60,202500/289.

The complete direct four-period phase construction has consecutive eccentric angles t,s satisfying b²cos(t)cos(s)+a²sin(t)sin(s)=0. For a5,b3, writing z=tan(t/2) and h0²=81z⁴+2338z²+81, the difference between the full signed product and202500/289 has numerator divisible by h0²−81z⁴−2338z²−81. The polynomial remainder is exactly0. This is a complete phase identity for one noncircular ellipse, not just two sample orbits.

## Submitted proof cross-check

| Issue | Verification and outcome |
|---|---|
| Source construction and parity | Both original tables give k403,b as the original focal pedal/antipedal product for N divisible by4. The sources use signed areas and define the antipedal from original vertices. No origin/odd or outer-polygon row was substituted. |
| Parametrization and primitive stars | Stachel Thm4.3/4.9 gives the stated modulus, semiaxes and increment2v, including gcd(N,tau)=1 winding. Real P(u) is injective modulo4K; least period is N because N is coprime to tau. For N divisible by4, tau is odd, m=N/2 even, and gcd(tau,m)=1. |
| Arbitrary pair covered | If original axes are a0,b0 and caustic parameterlambda, scale alpha=sqrt(a0²-lambda), k=sqrt(a0²-b0²)/alpha, cn(v)=sqrt(b0²-lambda)/b0. Then sn²(v)=lambda/b0² and the canonical formulas recover a0/alpha,b0/alpha. Thus normalization does not silently restrict the confocal pair. |
| Original antipedal formula | Fresh polynomial reductions of the candidate formula4 against both original line equations give remainder0. The actual normal determinant minus formula5 also reduces to0. These checks were written after exposure, independently of submitted checker code. |
| Pedal formula | Fresh algebra verifies formula12 is the Euclidean perpendicular projection onto the actual caustic tangent containing the original chord. Its squared centered norm is identically1, matching the pre-exposure circle proof. |
| Antipedal complex poles | The apparent 1+kS factor cancels in formula4. Common sn/cn poles are removable by order counting; the only remaining candidates are simple zeros of L at iK'±v, distinct since0<v<K. Individual vertices have at most simple poles. Area summands therefore have order at most2, even when N4 makes several singular indices coincide. |
| Antipedal double cancellation | Central symmetry equates the two focal areas. Reflection plus reversed cyclic order makes B even; the2iK' shift reflects the y-coordinate and negates B. At iK' these give an odd local germ, eliminating the double coefficient. This argument includes all cyclic edges and N4. |
| Pedal complex poles | At K+iK', both coordinate functions are even in the local variable, with at most a double pole. The two regular neighboring terms enter through an odd difference, reducing the area to at most a simple pole. No adjacent singular vertices occur because the step lies strictly between0 and2K. |
| Trace reduction | On the real-period h=2K/m, imaginary-period4iK' torus, both area functions have the appropriate two possible simple-pole classes and anti-period2iK'. T has exactly two simple poles: the original terms j0,m add equal nonzero residues. Matching a residue removes both poles; holomorphic compact-torus differences are constant, and anti-periodicity kills the constant. No area division occurs. |
| Half shift and product | K+v=(m+tau)h/2 is h/2 moduloh because m even,tau odd. Evenness and anti-periodicity place two distinct zeros of T at h/2+iK' andh/2+3iK'. Two simple poles mean exactly two zeros with multiplicity; thus shifted poles cancel and T(w)T(w+h/2) is constant. On real w, dn>0, giving a positive trace product. |
| Positivity/zero areas | The focus lies inside the caustic and q−F is a positive normal multiple. Each forward contact step turns its normal by an angle in(0,pi), so every pedal determinant is positive, including stars. Antipedal sign/zero cases do not enter any denominator. |
| Foci, orientation and scale | Half-period central inversion interchanges original foci with a cyclic relabeling. Reversal negates both areas; a similarity multiplies both areas by rho² and their product by rho⁴. These follow directly from the original constructions and agree with independent numerical checks. |

Primary source checks: [final source paper](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), [arXiv v11](https://arxiv.org/pdf/2004.12497v11), [Stachel published theorem](https://repositum.tuwien.at/bitstream/20.500.12708/136087/1/Stachel-2022-European%20Journal%20of%20Applied%20Mathematics-vor.pdf), [DLMF periods/poles/shifts](https://dlmf.nist.gov/22.4), [addition formulas](https://dlmf.nist.gov/22.8), [derivatives](https://dlmf.nist.gov/22.13). Source PDF text and table entries were inspected through primary retrieval; the attempted Stachel page screenshot timed out, so no visual inspection of that screenshot is claimed. No novelty inference is drawn from an unproved marker in a historical table.

## Strong zero-area boundary check

A direct primitive convex N8 family is obtained for r in[3,5] from

    b=1, a²=(r-1)³(r+1)/(4r),
    x=(r²-1)/(r²+1), y=2r/(r²+1),
    lambda=a²/(a²+r²),

with vertices(a,0),(ax,y),(0,1),(-ax,y),(-a,0),(-ax,-y),(0,-1),(ax,-y). The two first-quadrant chord tangency constraints agree exactly; axis symmetries propagate them. Direct reflection is exactly checked at the off-axis vertex for both endpoint examples. The eight vertices are distinct and convex, so the orbit is primitive.

At r3: a²=8/3,lambda8/35,A_p=576sqrt(6)/245,A_a=56sqrt(6)/81>0. At r5: a²=96/5,lambda96/221,A_p=19200sqrt(30)/3757,A_a=−10064sqrt(30)/625<0. Every construction is finite over the interval, so continuity proves an admitted zero-antipedal-area shape exists, independently of the product proof.

The numeric root estimate is a/b≈1.8538473043818210146240394413011885,lambda/b²≈0.25278935048914019584628891918204004. All sampled phases have a nearzero constant product at about1.5e-44, positive pedal area about7.15, and well-separated focal normals. This confirms that zero area is unrelated to intersection singularity. Root diagnostics are floating-point; the existence bracket above is exact.

## Reproducible numerical evidence and its limits

`direct_geometry_check.py` generates polygons by **direct conic tangency and second outer intersection**, never by Jacobi functions. It then independently checks closure, outer incidence, caustic tangency, specular reflection, both original-focus products, finite normals, proper-divisor nonreturn, central symmetry, reversal, cyclic relabeling and similarity scaling.

The pre-exposure receipt has18 target cases, five phases per case, N4,8,12,16,20, primitive stars up to winding N/2−1, a/b5/3,near-circle1.0001,eccentric10. Product spans at85digits are at most2.3e-59, with the least stable case near the focal-segment limit. At a10,b1,N12,winding5 the focal-normal sine is about4.6e-13 and antipedal area about2.55e13; precision loss there is expected conditioning, not phase variation. Outside-target N6 andN10 controls vary by about0.5% and0.26%.

A minor initial fixed-circle diagnostic reported a signed deviation instead of its absolute value. Its frozen file is preserved. `post_exposure_diagnostics.py` corrects the metric and checks all18 cases at100digits, also comparing the direct conic polygons with canonical vertices and both trace coefficients. Maximum absolute circle residual is about6.9e-72; maximum conic/canonical vertex discrepancy about4.4e-86. The antipedal trace coefficient span is at most2.3e-59, and the pedal shifted-trace coefficient span at most2.4e-74. These are high-precision diagnostics rather than validated interval certificates.

## Mechanisms, status and exact remaining gaps

| Family | Mechanism | Strongest result | Status / gap |
|---|---|---|---|
| Direct Euclidean/conic geometry | Focus-relative line algebra, polarity/circumcenter interpretation, support equations | All real constructions finite; fixed pedal circle; correct original-focus scope; scaling/reversal | Verified. These identities alone do not prove general-period phase invariance. |
| Low-period exact algebra | Four-period tangency bilinear relation and polynomial remainder; eight-period tangency construction | Exact full N4 phase identity for a5,b3; exact admitted N8 zero-area existence | Verified. No stand-alone all-N algebraic identity derived. |
| Independent real computation | Tangent contacts and outer quadratic intersections, reflection checked separately | Broad primitive convex/star diagnostics and sensitive boundary cases | Verified numerical evidence only; no interval certification or all-period extrapolation. |
| Post-exposure analytic audit | Candidate pole-divisor trace proof with primary Jacobi inputs | Full specified product theorem, including N4, stars and zero coefficients | No material gap identified. Depends on standard meromorphic elliptic-function and compact-torus facts, which are explicit and applicable. |

Excluded limits lambda0,lambda=b²,hyperbolic caustics and circular outer ellipse were not folded into the theorem. Nearcircle diagnostics match the independent circle limit product(N²R⁴/4)sin²(2pi m/N). Repeated lower-period traversal was not used to change parity. Source-history novelty and publication policy remain outside this geometry review.

## Artifact index

- `PRE_EXPOSURE_PLAN.md`, `INDEPENDENT_DERIVATIONS.md`, `PRE_EXPOSURE_MANIFEST.json`: independent start and frozen provenance.
- `direct_geometry_check.py`, `PRE_EXPOSURE_NUMERIC.json`: independent conic generator and full real diagnostic receipt.
- `symbolic_four_phase.py`, `EXACT_FOUR_PHASE.json`: exact complete four-period phase certificate for a5,b3.
- `symbolic_quad.py`, `SYMBOLIC_QUAD_AREA.txt`: generic central-quadrilateral antipedal expression used during direct exploration.
- `post_exposure_line_identities.py`, `POST_EXPOSURE_LINE_IDENTITIES.json`: exact fresh incidence/determinant/projection checks.
- `exact_zero_bracket.py`, `EXACT_ZERO_AREA_BRACKET.json`: exact admissible zero-area existence bracket.
- `zero_area_boundary_check.py`, `ZERO_AREA_BOUNDARY.json`: numerical root and finite phase examples.
- `post_exposure_diagnostics.py`, `POST_EXPOSURE_DIAGNOSTICS.json`: direct-conic/canonical and trace comparisons with corrected absolute-circle diagnostic.
- `POST_EXPOSURE_DERIVATIONS.md`, `DEPENDENCIES.md`, `RESEARCH_LOG.md`: supplementary derivations, replay dependencies and checkpoint history.
