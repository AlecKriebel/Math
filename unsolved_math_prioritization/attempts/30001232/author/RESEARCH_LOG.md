# Research log: five substantive approaches

Problem: 30001232 / OWR-3471-006. Work date: 2026-10-04 UTC. The budget below counts mathematical approach responses, not individual tool calls. No sixth search approach was opened. Publication and independent verification are separate gates.

## Source checkpoint, 12:20-12:23

Read live repository instructions and queue; no previous exact-target attempt was found. The original OWR page corrected a materially stronger catalogue mistranscription. Primary target: epsilon >=1/(2+|K^2|^(1/4)) on smooth minimal complex projective surfaces. Completion estimate for a full resolution: 0%. Formula identification complete; no status inference from the catalogue's open label.

## Approach 1: adjunction, multiplicity, and Kodaira-zero surfaces

Mechanism: test the sharpest boundary K numerically zero before seeking a universal proof. For any integral curve C through x, put d=L.C>=1 and m=mult_x(C). Adjunction and the genus drop give m(m-1)<=C^2+2; Hodge gives C^2<=d^2/L^2<=d^2. If d/m<1/2 then m>=2d+1, forcing (2d+1)(2d)<=d^2+2, impossible for d>=1. Hence epsilon>=1/2 when K is numerically zero. This establishes the primary conjecture in that class and is consistent with the known sharp K3/Enriques examples; it refutes the possibility of proving the catalogue's stronger literal bound.

Status: special case only, not a full resolution. The general formula has the additional term K.C, which this route does not control. Completion estimate toward full-target resolution after this route: 10%, purely a planning estimate.

## Approach 2: ruled-surface numerical geometry

Mechanism: use the rank-two ruled-surface intersection cone rather than general adjunction. Fuentes Garcia's formulas yield epsilon>=1 for an ample integral class A=a sigma+b f. For invariant e>0, the potential lower values a and b-ae are positive integers. For e<=0 the remaining lower expression is 2b-ae, again a positive integer because A^2=a(2b-ae)>0 and a=A.f>0; the alternate value is a, or min(a,b) when e=0 and the section class passes through x. Thus the primary lower bound, which is at most1/2, holds on geometrically ruled surfaces. Together with P^2, this covers the minimal negative-Kodaira-dimension class over C.

Status: known results give a complete class, but do not address elliptic/general-type surfaces. Completion estimate: 15%. No novelty claimed.

## Approach 3: Picard rank one and canonical polarization

Mechanism: exploit proportional numerical classes, where K.C is controlled by L.C. Szemberg's Theorem 7 gives the stronger bound 1/(1+(K^2)^(1/4)) in general type and >=1 otherwise under rho=1. Independently, for ample K itself, the Bauer-Szemberg canonical-polarization results give >=1/2; replacing an arbitrary L by K would be invalid.

Status: the route cannot extend numerical proportionality to arbitrary Picard rank. K^2 controls a norm, not all intersection ratios with arbitrary ample L. Completion estimate: 15%. This was a scoped known-theorem route, not a general proof.

## Approach 4: canonical slope and the Hodge obstruction

Mechanism: let sigma(L)=min{s : sL-K is nef}. Bauer's bound is epsilon>=2/(1+sqrt(4 sigma+13)). Writing t=|K^2|^(1/4), this alone implies the target when sigma<=t^2+3t-1. There is no proven uniform estimate of this shape. In fact the proposed final family would have sigma(L)>=K.C'/L.C'=d(d-3), whereas t^2 grows only linearly in d. A positive-square Hodge inequality controls K.C only after retaining K.L and the transverse negative-definite components; it does not replace sigma by K^2.

A precise formal obstruction considered before the geometric construction: set L^2=2, L.C=1, C^2=0, K^2=0, K.C=s=m(m-1)-2, and K.L=s+2 for m>=3. The corresponding 3x3 symmetric Gram matrix has leading minors 2,-1,4s and hence signature(1,2). Canonical parity and m(m-1)=C^2+K.C+2 hold. It permits d/m=1/m<1/2 at the level of these numerical constraints. It is not asserted to be the intersection data of an actual surface. It only shows that adjunction plus Hodge alone do not supply the missing geometry.

Status: universal lower-bound route blocked by an uncontrolled canonical slope; the formal numerical model is not a counterexample. Completion estimate: 20%.

## Approach 5: Miranda pencil plus branched base change, 12:25-12:30

Mechanism: start with the known ample A=2F+E polarization on the blowup of an integral degree-d plane pencil carrying an ordinary (d-1)-fold point. Blowing down loses this polarization, so direct minimalization was rejected: A.E=1 prevents descent as a pullback. Instead make a degree-two base change branched over four smooth fibres. It preserves an unbranched singular fibre isomorphically and makes K the pullback of K_Y+2F. Bezout proves this latter divisor ample, hence the covering surface is smooth and minimal with ample K.

Outcome: complete candidate counterexample family for every d>=7. At d=7, K^2=144, L^2=6, and an integral curve of L-degree1 has multiplicity6. The strict target failure follows from 144<4^4. All existence, smoothness, ampleness, canonical-class, and multiplicity steps are written in PROOF.md, including a dimension proof of an all-integral pencil. The degree choice d=m+1 is also explicitly supported by Bauer's original calculation.

Completion estimate: 100% of a candidate proof artifact; independent mathematical acceptance and historical priority remain unestablished. This is not a claim of 100% confidence or an audited result.

## Author controls, 12:30-12:32

Two separately expressed exact programs passed: blowup-lattice pairing calculations for d=4,...,30, and polynomial/dimension/double-cover formulas for d=4,...,100. They include the d=6 negative threshold control, d=7 strict failure, and Noether's identity using an independent topological cover calculation. These finite tests validate encoded algebra only. They do not prove nonempty-open existence, smoothness, or ampleness, and do not count as independent audit.

Candidate freeze: recorded in SHA256SUMS. Next action is a fresh adversarial mathematical audit of the pinned packet, especially pencil existence, fibre-product smoothness, branch canonical formula, all-curve ampleness, and preservation of fibre degree and multiplicity. No remote writes before that gate.
