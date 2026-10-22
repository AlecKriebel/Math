# Five substantive attempts

Source retrieval and literature searching are not counted as attempts. The following calculations/derivations address the original target through distinct failure checks and normalization mechanisms.

## 1. Literal source-VOA derivation through conformal grading

**Mechanism:** compare total Sugawara/coset conformal grades of the shifted summands in the original Eq. (3).

**Result:** the report's displayed reciprocal parameter and signed momentum, if used literally with its `P+n b` shift, give grade `n²+n((2K+1)n−h−1)/(K(K+1))`. This is generically nonintegral. The BFT convention gives grade exactly `n²`; translating that convention requires the reciprocal shift with the compatible sign.

**Status:** literal printed route blocked. This identifies a source-convention issue and rules out simply substituting the displayed formulas without correction. It is not a counterexample to the intended gauge identity.

## 2. Direct use of published full normalization

**Mechanism:** insert the characters of BFT (B.3)/(B.4) into its claimed splitting relation (B.10), before evaluating any infinite product.

**Result:** the exact nonzero rational residual is `−p²q(u1²−u3²)/((p−q)(q−1))`. The publisher PDF and arXiv v3 both display the mismatch. Thus the proposed coefficient-one normalization cannot be recovered by the printed rational-character identity as it stands.

**Status:** direct transcription blocked. The finite residual is an obstruction to this particular displayed argument, not a blanket refutation of the theorem.

## 3. Repair by finite triangle characters

**Mechanism:** replace the affine numerator's squared-variable pair by the pair in the Virasoro character; align the two patch flux triples. Prove the shift ratios using finite triangular geometric sums, including negative fluxes.

**Result:** exact character splitting holds. The three-point ratio is BFT's normalized three-point coefficient divided by the incoming highest-vector norm, times `(−1)^(l+m)`. The sign follows from an explicit even-integer polynomial; the total degree vanishes, so there is no hidden scale factor. This is an all-integer derivation, supplemented by exact checks.

**Status:** proved algebraic normalization statement, using the BFT coefficient/norm formulas for the identification.

## 4. Sewing two normalized three-point factors

**Mechanism:** apply the corrected normalizers to the two ordered vertices of the four-point conformal block; compare the product ratio directly with BFT Eq. (4.59).

**Result:** the two signs cancel and exactly one inverse internal norm remains. The resulting full conformal-block identity is coefficient-free for every integer flux. Eleven nontrivial/zero flux instances were independently checked from the finite products; the proof is symbolic and general.

**Status:** proved conditional on the published generic-parameter Eq. (4.59). This is a repaired derivation of its intended normalization, not an independent proof of the coefficient theorem.

## 5. Exact physical dictionary and normalization comparison

**Mechanism:** set `K=−eps2/eps1`, `lambda=2a/eps1−1`, `d²=(eps1−eps2)eps2`, `b=eps2/d`, `P=a/d`; compare chart levels, affine shifts, Virasoro shifts, and the source's reciprocal ratio. Then test whether cited gauge descriptions determine the same full functions without extra convention choices.

**Result:** the level and both Coulomb shifts agree identically, and `b_T²=(eps1−eps2)/eps2=−(k+3)/(k+2)`. A direct comparison with Alday–Tachikawa (3.23) exposes an abelian factor and a `K`-operator in that defect convention. Nekrasov–Tsymbaliuk concerns the regular defect and KZ equation. These cannot be silently conflated without checking the coordinate/gauge transform and initial normalization.

**Status:** structural dictionary verified; final convention-specific identification not completed. No claim that this residual task is open in the literature. The strongest certified statement of this packet is the repaired conformal-block normalization/sewing theorem.

## Verification record

- 42 triangle-character identities at integer shifts −10 through 10
- 686 exact three-point comparisons across two rational parameter samples and all triples in [−3,3]³
- 9 separate Laurent-character evaluations, not merely a re-evaluation of the same triangle expression
- 11 four-point sewing checks, flux −5 through 5
- symbolic character splitting, source residual, grading, scale degree and sign parity checks

These are exact checks, not floating-point approximations. They do not replace the arbitrary-integer proof, the published representation-theory input, or the unresolved convention-specific comparison.
