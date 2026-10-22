# PR210 independent meromorphic mathematical audit

## Assessment
**Mathematical result passes this audit. Mandatory findings:0. Optional mathematical findings:0.**

The exact outer focal-pedal product is proved for the stated strictly nested nondegenerate confocal elliptical caustic, every admitted odd least period N>=3, and every coprime star winding. The signed, ordered side-line convention matches arXivv11 Table7 k605,a and published Table7 k606. Neither original-chord feet nor inverse vertices have been substituted for the target.

This is an independent mathematical audit, not Root acceptance, a publisher instruction, an exhaustive priority investigation, human peer review, or a formal proof-assistant certificate. No localgit or provider mutation was performed. Existing publication and tracking must not be duplicated.

## Independence and sources
I began with only the two pinned inputs supplied in the task. I froze FROZEN_INDEPENDENT_CLAIM_MAP.md before opening supporting derivations, and independently reconstructed the main analytic proof and explicit residues. I subsequently read the two affirmative auxiliary mathematical derivations identified in SOURCE_SCOPE.json and checked their content independently. I did not read old mathematical reports or clearances, or another current math family's folder.

Primary checks independently verified the target mapping, signed-area convention, Stachel's full arbitrary-coprime-winding canonical theorem, DLMF periods and quarter-shift signs, ordinary addition formulas, Fourier dn series, and the old Khare-Sukhatme arbitrary-order dn identity. Exact URLs, passages, input hashes and access limits are in SOURCE_SCOPE.json. In particular, the published canonical theorem is general; the winding-one limitation belongs to a later corollary and does not restrict the theorem used here.

## Universal proof checked
1. Actual geometry: the focal foot is the orthogonal projection onto the tangent at an original vertex, hence onto an actual outer side line. Adjacent tangents meet finitely because their real canonical phases differ by less than a half real period. Distinct tangent triples cannot concur on a smooth conic. The projection denominator is positive on the real family. Its algebraic auxiliary-circle relation and the opposite-focus shift are exact.
2. Complete complex divisor: common sn/cn poles are removable in the rational foot map. On the sn torus4K,2iKprime, the two remaining simple poles are exactly r-v and r+v. The full vector requires imaginary period4iKprime; its2iKprime translate reflects the y coordinate. The other row is included explicitly, rather than mistaken for a true vector period.
3. Residues: for alpha>0 and S=sn(v),C=cn(v),d=dn(v), the residues at r-v and r+v are respectively minus and plus alpha*d/(k*C*S)*(1,i). They are nonzero, opposite and collinear. Coprimality leaves exactly two adjacent singular vertices at any singular phase. Only their determinant could have a double pole, and its double coefficient is zero. The N3 common regular neighbor and the closing edge cause no additional singularity.
4. Reduced trace: Bezout gives real periodL=4K/N. On the true reduced torusL,4iKprime, at most two simple poles remain, at b+iKprime and b+3iKprime. The cyclic reflection calculation includes both order-reversal and determinant-reflection signs. Centering at b=K-v makes the trace even, while the imaginary half shift is an antiperiod.
5. Complementary zeros: at the regular points p+L/2 and3p+L/2, evenness plus the real period and imaginary antiperiod forces zeros. They cancel every possible pole of F(z)*F(z+L/2). Compact-torus holomorphic constancy proves the product. No assumption about nonzero residues, a nonzero area, or a nonzero proportionality factor is used. If there are no poles the antiperiod kills the constant trace directly.
6. Physical focus exchange: for oddN,2K is congruent toL/2, giving the exact two-focus product. For even primitiveN it is instead a full reduced real period, which only yields equality of the two areas. The manuscript's exact primitive-four counterexample prevents an invalid parity extension.

A fully checkable reconstruction is in INDEPENDENT_ANALYTIC_DERIVATION.md. The proof treats all coprime windings algebraically and analytically, rather than extrapolating from a list of tested periods.

## Auxiliary claims
The bicentric reduction also checks out. Independent projective polarity gives the stated circle center d=-c*lambda/beta² and radius R=alpha*b²/beta² with the correct line-coordinate sign. The projected caustic contains the auxiliary-circle center, so the positive tangent-length choice remains valid for stars. The shifted quadratic dn parametrization, actual phase origin, tangent-length formula, cyclic local-addition telescope and contact-area multiplier agree. Root-of-unity filtering of the classical absolutely convergent real dn Fourier series independently supplies the arbitrary-order Landen sum. Its odd focus half-period recovers the same invariant.

The opposite-focus inverse-area transfer is valid, and is not justified merely by an arbitrary projectivity. Independently, the inverse vector's two negative Laurent coefficients are collinear in the same isotropic line at the adjacent paired poles. This bounds inverse-area order by2; reflection about a pole is odd by the imaginary antiperiod, removing its even Laurent term. Both area traces therefore lie in the same at-most-one-dimensional antiperiodic simple-pole space. Matching one residue gives Bplus=gamma*Dminus without dividing by area zeros; the samegamma applies to the other focus.

These checks establish mathematical statements. They do not establish whether or when the application was published previously, or independently certify the modern cited paper's exact printed fixture wording.

## Fresh reproduced evidence
- 248 exact symbolic and physical assertions:236 in fresh_controls.py and12 in supplemental_exact.py. They include direct boundary/reflection/caustic tests for two triangular phases and two genuine primitive-four phases, actual tangent-intersection side projections, repeat/reversal controls, circle rotation, projection and pole algebra, projective polarity, the stated distinct original-chord product, unit-inverse product and opposite-focus multiplier2016/5.
- 1,124,744 exact finite integer-lattice assertions over4,141 coprime odd families throughN201, covering558,231 phase-index cases. These exhaust the finite control range and are separate from the universal coprime argument.
- 13,410 explicitly non-interval90-digit numerical diagnostics over58 real odd families and6 complex pole families. They check physical unit reflection, shared caustic tangency, actual outer-side projections, focus/reduced-period/reflection characters, both imaginary pole rows, common-Jacobi-pole removability, opposite residues, removal of double terms, complementary zeros, complex product continuation, inverse proportionality and the bicentric dn formula. Cases include stars, N3, high winding, k=1e-10 and k=1-1e-12. They are diagnostics and do not replace the universal proof.

The exact even products are16 and25 for the same a2,b1,lambda4/5 caustic, as stated. The exact triangular product is12544/25. The original-chord product is7225344/390625 and the original-vertex unit-inverse product is1/324, confirming object distinctions.

The first harness run exposed an own symbolic substitution-order mistake before reaching geometric fixtures. It is documented in CONTROL_FAILURE_01.txt; the initial script is preserved as inert text. Expanding the rational numerator before reducing the canonical relations repaired the control. No mathematical source or manuscript edit was needed, and both repaired scripts passed.

## Exact remaining scope
No mathematical gap remains in the stated target theorem or the checked auxiliary derivations. Hyperbolic, degenerate/focal/collapsed, grazing, filled-star-area and segment-clipped constructions are outside the theorem. The circular endpoint is handled separately, and repetition/reversal scaling is explicit. This audit has not established historical novelty, public priority, causal independence, or worldwide open status. Final modern-source attribution and inaccessible final companion equation numbering should use the separate source audit; this mathematical clearance does not waive those publication checks.

Final audit completion estimate100% for this assigned mathematical audit, not for the parent research program.
