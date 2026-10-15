# Mathematical repair ledger

Problem 30005651 / OWR-14297741-001. Corrected partial result; **UNRESOLVED, approach 1/5**.

The earlier wording was not accepted unconditionally. Three corrections were required before the scoped partial-result acceptance. They are already implemented in APPROACH_1.md and FREE_LOCUS_PERFECT_FIELD.md. No full solution or new approach is claimed.

## R1. Correct the small-site quantifier

Location: APPROACH_1.md, Corollary 6.1 and closing limitation; FREE_LOCUS_PERFECT_FIELD.md, Section 6.

The earlier argument tested all points of the punctured standard representation V minus {0}, then invoked conservativity for its small equivariant Nisnevich site. That was insufficient: the required test family also includes points of every equivariant etale object over the punctured representation. This is separate from, and stronger than, correcting a restriction to closed points.

The corrected proof chooses every equivariant etale U -> V minus {0} and every scheme point u of U. Write H for the set-theoretic stabilizer and I for the kernel of its action on k(u). A geometric point over u maps to a nonzero vector, so I embeds in that vector's stabilizer. The standard S3 representation has nonzero geometric stabilizers either 1 or a transposition subgroup C2. If I=1, the point belongs to the free invariant open of U, and the free-germ theorem applies over the perfect field C. If I=C2, normality in H and N_S3(C2)=C2 force H=I=C2; the subgroup comparison and Bachmann's theorem apply. Every required orbit-henselian test is therefore connective.

The conclusion is sheaf vanishing on the entire small site. Any germ not controlled by this argument lies over the origin. The proof does not claim that a single evaluation at the base origin tests the full fiber, and does not assert connectivity of all global section spectra.

## R2. Specify the continuity models

Location: APPROACH_1.md, Section 2.2.

The extension uses finite-type smooth models with affine transition maps. Nonaffine objects are treated by affine charts and Nisnevich descent. An arbitrary nonaffine object is not described as an inverse limit of affine schemes. The dimension bound is applied to the actual noetherian limit scheme T x Delta^n, not to larger-dimensional finite-type models.

## R3. Distinguish etale from essentially etale

Location: APPROACH_1.md, Proposition 3.3, Step 1; FREE_LOCUS_PERFECT_FIELD.md, Section 1.

B=A tensor_{K0} F is finite etale over A. After localizing at the selected prime n, the map A -> B_n is essentially etale with unchanged residue field. That is sufficient for the henselization comparison; no finite-presentation assertion for the localization is needed.

## R4. Narrow the companion's nonessential closed-point warning

Location: FREE_LOCUS_PERFECT_FIELD.md, Section 5.

The companion previously stated that closed-point conservativity fails for ordinary Nisnevich sheaves and remains false for A1-local spectral sheaves. The report's explicit square-cover example proves the ordinary Nisnevich-sheaf assertion. It does not provide the additional strict-A1-invariance input or an A1-local spectral example needed for the stronger warning.

The stronger warning is removed. The companion now limits the statement to arbitrary ordinary Nisnevich sheaves and cites APPROACH_1.md, Section 4.3. This is an explicit mathematical scope narrowing, not merely an administrative edit. No assertion about conservativity within the A1-local spectral category is made by this warning. The free-germ proof, punctured-representation proof, all core partial theorems, and the original corrected-partial acceptance are unchanged.

## Acceptance after correction

The dimension and field-orbit estimates, subgroup comparison, free-germ theorem with its residue-field hypothesis, punctured S3 result, and tangent/codimension presentation obstruction are accepted as corrected partial deductions. The origin, the general finite-group theorem, and all free germs over arbitrary imperfect fields remain unresolved. The rank-one tangent obstruction is prior work of Heller--Voineagu--Ostvaer (2015). No counterexample, negative stalk class, or novelty certificate is supplied.

The published editions preserve the complete corrected proof and companion argument and the substantive independent mathematical audit. Edition review additionally narrows the nonessential companion warning exactly as R4 records. Other preparation changes concern administrative framing, out-of-edition references, computational-record descriptions, and public-source metadata presentation. ACCEPTANCE.json binds the actual editions. The earlier reports and exact original correction history were retained and replay-checked separately; their artifact identities are not included here.
