# Independent classical/general-theorem audit: k203,a / 5100011

Checkpoint: 2026-10-16 08:05:38 UTC. Completion estimate: 90% of this bounded audit; this is not a percentage estimate of historical novelty. Source-first plan was frozen before the submitted SOURCES or prior favorable reports were read. No prior review report was read. No external communication, Git action, publication, source modification, installation, render, or saved source download occurred.

## Decision-relevant findings

The generic flag-curve and pole-cancellation method is established prior art. The radial pedal-area principle is also classical. The full N=4 arbitrary-point target is an explicit elementary corollary of a verified 2020 theorem. I have not found a completed exact N>=8 original-sideline pedal product in the classical primary sources checked. This bounded finding does not establish novelty or exhaust the literature. A separately reported October 2026 exact-target preprint was not used to guide this classical audit and is left to the exact-target audit.

The exact target is signed A(P)B_M(P), E:a>b>0, proper nested confocal elliptical caustic, physical primitive LEAST period N divisible by four, arbitrary chosen fixed finite real M, original ordered side LINES, including star windings, reversal, zero and negative pedal areas. The RGK literal Table 3 row does not print least. RGK journal p.343 defines signed shoelace areas; p.344 defines the original pedal; p.346 lists k203,a, A A_m, N=0 mod4, all M, experiment4/20, proof ?. The complementary outer-pedal entries are separately in Table4.

## A completed prior implication for N=4

Let a nondegenerate ordered parallelogram be P=(U,V,-U,-V). Put D=det(U,V), s=|V-U|, t=|V+U|. Its signed area is A=2D. The two consecutive central pedal feet are

    q1 = D J(V-U)/s^2,     q2 = D J(-U-V)/t^2,

where J is clockwise rotation by pi/2. The other feet are -q1,-q2. Since det(V-U,-U-V)=2D,

    B_0 = 4 D^3/(s^2 t^2),
    A B_0 = 8 D^4/(s^2 t^2).

The distances from O to the successive side lines are p,q,p,q, with p=|D|/s and q=|D|/t. Therefore

    A B_0 = 8 p^2 q^2 = 8 product_i dist(O,side_i).

The radial quadratic coefficient vanishes for every parallelogram: consecutive direction changes alternate Delta and pi-Delta, so sum sin(2Delta_i)=0. Hence B_M=B_0 for every fixed M. Bialy--Tabachnikov, *Dan Reznik's identities and more*, arXiv:2001.08469v2 (5 May2020), Theorem4.3(2), pp.8-11, proves the origin-to-sideline distance product equals (alpha beta)^(N/2) for N divisible by4. Its N=4 case completes the exact target:

    A B_M = 8 alpha^2 beta^2.

This covers reversal since both signed areas reverse. The derivation is algebraic; no area division or positivity of B_M is needed. A standard-library exact-fraction diagnostic at P=((3,1),(-1,2),(-3,-1),(1,-2)) and M=(0,0),(5/3,-8/7),(-10,11) returned A B_M=19208/221 in all three cases, equal to the derived formula. The diagnostic is not the proof. No verified extension from the distance PRODUCT alone to the pedal-area SUM for N>=8 was found.

## What Steiner already supplies, and the remaining gap

Steiner's actual 1838 text was read in the ETH/e-rara primary OCR, DOI10.3931/e-rara-3816. Sections XIV-XVI (reprint pages18-22), equations25-29, derive the polygon pedal-area quadratic and radial level circles about the weighted centroid. Section XVI explicitly discusses coefficient signs, nonconvex polygons, and the zero-coefficient case. This records a literal historical statement, not a valid general inference for every modern signed crossing polygon. The general signed expansion is B(M)=B(0)+ell dot M+C|M|^2; C=0 alone does not remove the linear term or produce a finite centroid. A counterexample supplied by the root adversarial audit after this draft has C=0 and ell nonzero. The present centrally paired setting separately forces ell=0, so its displayed radial identity and the N=4 deduction are safe. The introduction p.4 refers back to Crelle1825 volumeI p.51 and volumeII p.265. I did not independently retrieve those 1825 originals. OCR mangles some formula glyphs, so the coefficient below was independently derived by the ordered shoelace calculation, rather than transcribed from OCR.

For a centrally symmetric ordered polygon, with consecutive side direction changes Delta_i, the signed identity is

    B_M = B_0 + |M|^2 S/8,       S=sum_i sin(2Delta_i).

It is the centrally symmetric signed form of the classical principle. It avoids division by the centroid denominator when S=0. Exact all-M phase invariance of A B_M is equivalent to BOTH A B_0 and A S being phase invariant: necessity follows by taking M=O and any unit M; sufficiency is immediate. Central symmetry or K=O by itself gives neither coefficient invariant. The known even A A_outer result and its elementary polarity transfer give A A_contact constant, but still require phase-independent B_M/A_contact (or equivalent coefficient identities). Calling that last requirement classical without a proved cited statement merely transfers the central difficulty.

Reznik--Garcia--Stachel's *Area-Invariant Pedal-Like Curves Derived from the Ellipse*, arXiv:2009.02581v3, section2 and AppendixB, explicitly restates Steiner and derives smooth-curve pedal area quadratics. These concern moving M for a fixed smooth curve, not orbit phase for discrete billiard polygons. They support attribution, not a completed implication to the present theorem.

## Closest published area theorem and method overlap

Chavez-Caliz, *More About Areas and Centers of Poncelet Polygons*, journal2021 pp.91-106, received17April2020, online14August2020: Theorems3/6, complete proof p.104, give A(P)A(Q) constant for even Poncelet families between concentric ellipses in complex-projective general position, Q the polygon of outer tangents at P's vertices. This is not the original-sideline pedal. Page98 explicitly uses the incidence flags E, two involutions, translation on a genus-one curve, meromorphic signed area, and simple poles at infinity. Page104 removes product poles through complementary zero-area degenerations. Those are close predecessors of the alternative flag proof's architecture. The candidate's fixed linear polarity transfer from outer vertices to contact vertices is an additional explicit reduction, not the target pedal identification.

Schwartz--Tabachnikov, *Centers of mass of Poncelet polygons, 200 years after*, arXiv:1607.04766v1, section3, already gives the same flag double cover, involutions, torus translation, invariant meromorphic functions, two infinity-pole orbits, local Laurent cancellation, and holomorphic-on-compact implies constant. Its centroid conclusion is not used here: Chavez p.92 acknowledges a gap in its CM2 argument. The explicit flag construction and general mechanism are still direct method evidence.

Akopyan--Schwartz--Tabachnikov, *Billiards in ellipses revisited*, arXiv:2001.02934v2, sections4-5, Theorems5/6, uses complexification, Liouville, and cancellation at infinity for cosine sums/products; section6 gives further related angle invariants. There is no occurrence of pedal in the checked complete HTML. This is method prior art, not the exact theorem.

## Other checked primary families

- Bialy--Tabachnikov Theorem4.1 gives fixed-point outer-tangent feet centroid and sum of squared distances; Theorem4.3 gives original-side distance products. The first is a distinct polygon; neither printed statement is the exact N>=8 pedal-area product.
- Stachel, *On the motion of billiards in ellipses*, online24January2022, Theorem4.3/(4.9) gives Jacobi canonical parameters; Theorems5.2,5.4,5.6 give angle/contact-length identities. Full relevant theorem contexts were read. They do not state pedal-area invariance.
- Stachel, *The geometry of billiards in ellipses and their Poncelet grids*, online18October2021, Theorem4.7 uses central pedal feet to prove cosine-sum/perimeter formulas; Corollary4.9 gives squared outer-tangent distances and curvature sums. The central feet are not a hidden pedal-area theorem.
- Levi--Tabachnikov arXiv:math/0511009v1 (1November2005), Theorem1 and sections3-5: Poncelet-grid conics, commuting shifts, projective/linear equivalences. The v1 main grid statement explicitly assumes odd n. No Euclidean polygon-area product is proved in that text. The word area there principally concerns the phase-space symplectic form.
- Connes--Zagier, Monthly114(2007),909-914, Theorems1/2 and section4: orthoptic/maximal-perimeter parallelograms, a confocal extension, and billiard integrability. It supplies useful N4 background, not an all-period pedal-area theorem.
- Darboux-related targeted queries led to grid/closure results, not a verified exact pedal-area-product statement. I did not read Darboux's full original volumes. No historical claim of absence is warranted.

Griffiths--Harris1978 was pursued as the earlier flag-method reference: the IAS PDF endpoint returned zero extracted lines through the web tool and403 through memory fetch; the e-periodica PDF endpoint presented verification. The text was not counted as read. A tertiary DOI link misdirected to an unrelated article and was discarded.

## Honest possible editorial wording

"We give a proof of the signed original-sideline pedal-area product for primitive elliptic-caustic billiards whose least period is divisible by four. The proof uses Steiner's classical pedal-area principle and established Poncelet elliptic-curve methods, together with Chavez-Caliz's even area-product theorem. The four-period case also follows directly from Bialy--Tabachnikov's distance-product invariant."

Use this only after reconciling the separately discovered exact-target2026 source. Do not claim a new flag-curve method, new radial pedal-area principle, absolute priority, or resolution of literal repeated-length scope. The target-specific general-period deduction, its full hypotheses, and signed boundary cases remain what must be compared with earlier exact-target texts.
