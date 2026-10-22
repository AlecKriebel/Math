# Independent final review: inner focal-pedal invariant k609 / 5100037

**PASS for the full domain-qualified claim. No mandatory mathematical correction.** The two signed areas are equal for every primitive even orbit with a strictly nested nondegenerate confocal elliptical caustic. The ratio is 1 wherever defined. Its denominator is nonzero for convex orbits, while the exact primitive eight-star certificate establishes a common zero in the extended star scope. This does not refute constancy on the defined quotient locus.

Reviewed 2026-10-01. Version 2 corrects the independent checker’s implicit-line sign convention; see CORRECTION_V2.md. The original review and receipt are preserved separately. This verdict binds `PROOF.md` SHA-256 `cac238f2bd1d673a07a2f39df30dd59b23ba5f6ac2c3b567c2d86b23a51e1b25` and `MANIFEST.json` SHA-256 `4ec32d01a1aa404c7acadbae81e6ee55a2952e27fe28191dd1883d731248aff8`. All nine author artifacts and three source PDFs matched their hashes. No novelty, priority, or human peer-review certification is implied.

The reviewer is separately investigating the neighboring outer-antipedal target k608, but supplied no proof ingredient to this k609 candidate before its freeze. Shared source navigation and the established central-symmetry input are disclosed; the inner-contact proof, convex positivity argument, and zero certificate were independently checked here.

## Exact source and period gate

The inspected [arXiv v11 source](https://arxiv.org/abs/2004.12497v11), Table 7 printed p9, has the double-prime focal **pedal** area ratio as k609. The inner vertices are the caustic contacts in traversal order, and their pedal vertices are projections onto successive inner-side supporting lines. Neither original/outer vertices nor antipedal line intersections have been substituted. The source's area convention is signed shoelace area.

The [published companion](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), Table 7 printed p349, ends at its differently numbered k607. It contains no matching k609 row. The candidate correctly targets the arXiv item, corrects the imported report's edition conflation, and does not interpret omission as a mathematical withdrawal or solution.

[Stachel, Journal of Geometry 112, article 40 (2021)](https://doi.org/10.1007/s00022-021-00606-2), Definition 4.1 and Corollary 4.2(i), printed pp22–23, supply the central symmetry. The period/turning-number reduction is explicitly stated there; primitive even period has odd turning number, and the proof identifies the opposite vertex at half the index period. Hyperbolic-caustic symmetry is treated separately in that source and is correctly excluded. An even number of labels obtained by repeating an odd primitive orbit is not covered by the inference. Repetition of an even primitive orbit preserves both area equality and simultaneous zeros by multiplying each signed area by the same repetition count.

## Universal equality and finite inner sides

A strict ellipse has a unique contact point on a tangent line. Central inversion therefore carries each billiard side's contact to the contact at the half-period shift. Orthogonal projection commutes with this isometry, giving the displayed opposite-focus, shifted-index correspondence. Its determinant is +1 in the plane and the index shift does not reverse traversal, so the two shoelace sums agree with their signs intact. This works for admissible stars as well as convex orbits.

Consecutive contacts cannot coincide in the stated model. Coincidence would force both incident sides onto the same tangent line of the caustic. The reflection law then permits only grazing or normal backtracking. The first is the outer supporting tangent and misses the strict inner ellipse. For the normal chord at `(a cos theta,b sin theta)`, direct substitution into the dual tangency condition gives the confocal parameter `a² sin² theta+b² cos² theta`, at least `b²`. A strict elliptical caustic has parameter between 0 and `b²`, so the second alternative is impossible. Thus all inner projection directions are nonzero, with no suppressed line-at-infinity singularity.

## Convex denominator theorem

The general lemma is correct with all of its hypotheses: centrally symmetric, strictly convex polygon, at least four vertices, counterclockwise traversal, origin at its center. Positive support numbers and turns strictly between 0 and pi follow. Opposite sides cancel the terms linear in the pedal point. Expanding the quadratic terms and telescoping the stated double-angle identity gives

`B(M)=B(0)+(1/8 sum sin(2 delta_i)) |M|²`.

The coefficient is not assigned a sign term by term. Instead the doubled normal angles of the first half form a cyclically ordered inscribed polygon. For at least three such points its oriented area is positive, even if one doubled angular gap exceeds pi; shoelace area of that entire convex polygon remains positive. This area is exactly twice the coefficient. For a centrally symmetric quadrilateral the two-edge shoelace sum is zero. The constant term is strictly positive in all cases because every support number and `sin delta_i` is positive.

Consequently the pedal area is positive for **every** point in this convex setting, including points outside the polygon. The inner contact polygon of a convex even billiard satisfies these hypotheses. The candidate does not transfer this positivity to star traversal. Reversal changes both signs and does not produce a zero denominator.

## Exact primitive eight-star and its zero

The rational interval `(3/8,2/5)` gives positive `S<C<1`, `C²+S²=1`, and `R=a²>1`. The eight displayed boundary points are distinct. Sorting their ellipse parameters shows that the listed traversal advances by three cyclic positions, so its winding number is 3; no smaller orbit is repeated.

The squared chord ratio has strictly positive factors, so it determines the positive length ratio without a sign ambiguity. Substitution makes the velocity difference parallel to the outward normal at the non-axial vertex; its outward orientation is correct. The other non-axial vertices follow from the two reflections. At each axial vertex, the incident sides are themselves mirror images about the normal axis, giving reflection directly. The separate checker verifies both their squared lengths and the normal determinant.

The dual-conic test holds on all eight sides, with `0<lambda<1<R`. The claimed contacts arise from the actual side equations and the positive-definite caustic quadratic form, so they are the unique physical tangencies. Their ordering matches the eight side indices. The strict inequalities `U>X>0` and `Y>V>0` also exclude all contact coincidences.

The independent calculation uses scaled coordinates `x=a xi, y=eta` and obtains each contact from an implicit side equation. It then constructs each pedal foot by the implicit-line orthogonal projection formula, with metric `diag(R,1)`. The focus has normalized coordinate `z=c/a`, hence `z²=(R-1)/R`. The area is quadratic in z; its odd coefficient cancels. This independently reconstructs the exact rational function in equation (13), including its sign, factor 8, and seventh-degree polynomial.

The independent calculation also reproduces equation (14) as the **positive squared distance of an actual adjacent contact pair**. Thus the factor G cannot vanish in the root interval. All remaining denominator factors are visibly nonzero there. The two exact endpoint values of f have opposite signs, so continuity supplies a root strictly inside; uniqueness is unnecessary because the argument covers any such root. At that root both signed areas vanish by the universal equality while every pedal projection is finite. The statement carefully distinguishes this example, which selects an ellipse/caustic, from variation of a defined quotient within one fixed Poncelet family.

## Independent controls and disposition

- Independently authored checker: **25,465 exact assertions**, including formal rational-function identities rather than floating root evidence
- All eight chord tangencies, contact incidences, and contact-on-caustic identities checked symbolically
- Separate implicit-line projections verify the star area and the physical denominator identity
- Exact centrally symmetric convex-polygon controls verify the radial coefficient and arbitrary-point positivity
- Author's **7,006-assertion** checker replayed in a separate copy; its receipt is byte-identical
- All nine frozen author artifacts and three primary PDFs hash-verified

These controls support the analytic argument; they do not replace its universal symmetry, contact, and positivity proofs. The public disposition should preserve the primitive elliptical-caustic scope, exact arXiv edition, positive convex denominator, common-zero star exception, and classical symmetry credit. The full domain-qualified candidate passes as written.
