# Independent review of the Bigelow source and prior art audit

**Verdict: PASS for the expressly conditional, prior-known result.** No mandatory mathematical revision was found. The package is suitable for a draft research-audit PR if it retains its present source-repair qualifications and attribution. This is an independent AI audit, not human peer review or a formal proof certificate.

**Review date:** 2026-09-30
**Model and effort:** gpt-6-astra, xhigh
**Reviewed repository commit:** `2cafb4f09688c3cfde39cada3ae317c476832f2c`
**AUDIT.md SHA-256:** `f363afd4932f5e1ba5d5df4141efbf182ef2c05145b631dbe0676b4b618af2f5`
**verify.py SHA-256:** `10e41b05201e13971442992d84199b5612934b4870a67a7e04a882908697a3f3`

The reviewer did not participate in the Bigelow construction or write the submitted audit. The submitted files were read without modification. The report covers the source transcription, two repairs, all-index matrix argument, specialization claims, scalar-route scope note, attribution, and executable checks.

## Exact approved conclusion

Let (F=\mathbb Q(q)), with (q) transcendental. Using the relation elements defined explicitly in the submitted audit, both

\[
A_n=FB_n/(R_2,\ldots,R_{n-1}),\qquad
C_n=FB_{n+1}/(R_2,\ldots,R_n),\quad n\ge3,
\]

have nonzero (X_3). The displayed Burau representation proves this for every indicated strand count. This construction is already present in the cited Argus archive. The audit therefore supports a source-correction/prior-result disposition, not a new-discovery claim.

## Source fidelity

The reviewer inspected the actual typeset preprint p. 14 and published scan p. 298. Both use the inverse of the whole braid word; in particular the inverse of the word with indices 2,1 has factors in inverse order. Both write a quotient of (RB_n) while the terminal relation contains a generator with index (n). The earlier braid-group convention only provides indices through (n-1). The edited-volume draft, printed pp. 315–316, was separately checked by text retrieval and has the same issue. The stated repairs are therefore explicit mathematical choices, rather than a silent transcription correction. [Preprint](https://arxiv.org/abs/math/0505064), [published scan](https://web.math.ucsb.edu/~bigelow/publications/10.pdf), [volume draft](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf)

The author's publications page has no listed correction for this paper in its errata section and describes its coverage as through 2020. The submitted audit correctly limits the inference from that negative finding. Authorial intent and possible corrections elsewhere remain unestablished. [Author's list](https://web.math.ucsb.edu/~bigelow/publications.html)

## Mathematical audit

1. **Representation.** The proposed block is invertible over (K=\mathbb Q(q,u)). Its stated inverse is correct. The adjacent three-coordinate braid identity is correct, and distant blocks commute. Thus the assignment extends to an (F)-algebra homomorphism from the braid-group algebra into matrices over (K).

2. **Local mechanism for arbitrary indices.** Write a vector on three consecutive coordinates as (w=(a,-a/u,0)^T), where (a) is arbitrary. Direct multiplication by the two adjacent forward blocks gives ((0,a,-a/u)^T), and multiplication by the two inverse blocks in the stated order gives ((0,a/u,-a/u^2)^T). This independently reproduces the propagation formulas for every admissible index. All remaining prefix factors have support disjoint from the resulting two-coordinate vector and fix it. The same observation applies when the prefix begins at index 2. There is no commutation or inverse-order shortcut hidden in this argument.

3. **Induction.** The rank-one formula for (X_2) is correct. Applying the preceding local identities to each recursive multiplier gives

   \[
   \rho(X_k)=\prod_{j=1}^{k-1}(q^j-u)\,v_{k-1}\lambda.
   \]

   This is an all-index induction, not an extrapolation from finite computations.

4. **All ideal generators vanish.** The exceptional row (R_2) needs its own three-coordinate calculation; equation (6) supplies the correct one. For every later legal row, both multipliers send (v_{k-1}) to the same vector ((q^{k-1}-u)v_k). Their difference therefore kills the rank-one image of (X_k). A homomorphism's kernel is a two-sided ideal, so checking these generators suffices. Taking the matrix size to be (n) verifies every generator of (A_n); taking it to be (n+1) also verifies the terminal generator of (C_n). The proof does not infer nonvanishing in a further quotient merely from nonvanishing before that quotient.

5. **Nonvanishing.** An explicit entry, in row 2 and column 1, is

   \[
   \rho(X_3)_{2,1}=-\frac{(q-u)(q^2-u)}{u}\ne0.
   \]

   Hence (X_3) was nonzero in each (F)-algebra. An (F)-algebra map into matrices over the extension field is enough for this implication; faithfulness and finite dimension over (F) are not needed.

6. **Twists and specializations.** The identities for the first-generator twist of (X_2) and the three-strand full twist of (X_3) are correct. Specializing (u=q^3) is valid in their Laurent-polynomial matrix formulas, annihilates (X_4), and preserves the displayed nonzero (X_3) entry over (F). The different specializations (u=q) and (u=q^2) are correctly described as vanishing controls. None of these facts establishes finite-dimensionality of a universal quotient.

7. **Preliminary scalar route.** The factorizations in `SCALAR_SCOPE_CHECK.md` are correct. Under nonvanishing of (x_3), the first relation forces the sixth-root branch; the next row forces the exceptional specialization (q=s), and the following row contradicts nonvanishing in characteristic zero. This correctly blocks promotion of the small-strand scalar observation to an all-strand proof. It is not needed for the Burau conclusion.

## Reproduction and independent checks

The exact submitted verifier was loaded without executing its file-writing entry point. Its 42 documented parameter/strand cases were rerun unchanged: **1,590 equality and rank assertions passed**. The resulting receipt is `verifier_rerun.json`. Code inspection confirmed that the barred words are inverted as entire matrices, every legal relation is included, and the closed-form formula is compared against a separately formed recursive expression.

A separate SymPy 1.14.0 implementation, `independent_symbolic_check.py`, imports no candidate or Argus code. Its **23 symbolic checks passed**. They cover the arbitrary-amplitude local propagation identities, exceptional row, an explicit nonzero entry, twists, direct word evaluations for four and five strands, the (u=q^3) specialization, and scalar factorizations. The receipt is `independent_symbolic_check.json`.

The initial independent test harness used structural equality between differently arranged symbolic expressions for one entry; that assertion was replaced by rational-function equality. No submitted mathematical claim or file changed. These computations supplement the algebraic proof and are not presented as formal certification for all strand counts.

## Attribution and historical limits

The reviewer independently retrieved the Argus `review-package.md` at both cited commits. Both returned the same blob, `274c04c5f59fd5f56be95373191ae36d278b3618`, containing the same two repairs and rank-one Burau construction. GitHub reports author/committer timestamps of 2026-08-30T12:01:44Z for the initial archive commit and 2026-09-03T09:58:29Z for the extension. The extension README explicitly distinguishes its finite-dimensional image construction from finite-dimensionality of the universal quotient. [Initial archive](https://github.com/Argus-AiTeam/argus-mathematics/tree/b8f60542f758750e263016cad1d45cc0650ed64d/results/11000263), [extension](https://github.com/Argus-AiTeam/argus-mathematics/tree/5abed447441b42dbe9f735e8b2960ee0a0705235/results/11000263)

These observations substantiate attribution to existing public work. They do not establish a worldwide priority date, human specialist acceptance, or the original author's intended correction. The bounded independent search also encountered the historical BIRS discussion of diagrammatic zipper algebras; no equivalence with the two presentations was assumed.

## Disposition and required scope preservation

No mathematical revision is required. An administrative update from “review pending” to “independent AI review passed” may link this report without changing the approved proof. Any mathematical edit should receive a new hash and targeted re-review.

A PR should be labeled as an audit of prior work and source scope. It must not describe the literal defective presentation as unconditionally solved, erase the distinction between the repairs, claim a newly discovered result, assert a universal finite-dimensional quotient, or close neighboring Questions 5, 7, or 8. The present submission already observes these boundaries.
