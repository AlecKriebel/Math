# Fresh independent whole-preprint/package adversarial review 02

The repaired candidate is pinned before review in `PINNED.json` (also copied as `INPUT_PINS.json`). Original head: `f6570e093267a7f910faf9cdd60dfbc1c12f5681`. The candidate ZIP has 135 entries, 446002 bytes and SHA256 `d0c41fad32886f48cf87cb6f981836ccce9610bbe778af4fcf3999d0055f4d70`. This review covers the entire current six-page preprint, supplement, portable code, metadata, archive, preserved original tree, independent audit evidence and historical/current navigation.

**Verdict: REPAIR_REQUIRED.** The complete stated mathematical theorem survives a fresh independent derivation and adversarial checks. No actionable P0, P1 or P2 concern was found. One actionable P3 defect remains: a missing space in current supplement prose. CLEAN is unavailable while that defect remains. The pending immutable-publication gate is correct; this review grants no publication, release, deposit, merge or service authorization.

I derived the proof from the current paper and complete pinned original proof before reading the earlier package review's conclusions. Existing PASS labels were never mathematical premises. Primary theorem interfaces were checked in freshly retrieved exact source bodies. No agent was spawned, no other shard was read, no individual was contacted, and no outreach was prepared. No candidate/original, Git/index/queue/PR/service/publication state was mutated. Authored outputs are restricted to this review folder; raw third-party PDFs, extracted text and rendered source images remain exclusively under `sources/raw`.

## Exact claim, assumptions and success criteria

The target is the oriented real mass ball `C(4,12)`, the convex hull of all real unit decomposable four-vectors of both orientations in the 495-dimensional fourth exterior power of R12. The claim excludes every arbitrary finite projected semidefinite lift. The consequences are failure of the original universal supporting degree-at-most-one SOS assertion modulo the full real vanishing ideal, existence of an unnormalized failing functional with rational coefficients, and existence of a constant closed comass-one four-form on R12 with no norm completion by finitely many four-forms even at one point, hence no local completion.

The decisive external input is Fawzi's published Theorem 1 specialized to normalized **complex** Sep(3,3), not a real product-state body, unnormalized cone, fixed hierarchy, finite positive-map test or unprojected LMI. Fawzi is not reproved here. The exact elementary section transfers that established theorem. No explicit coefficients, exact maximum/comass, rational normalized form, minimal dimension, lower-dimensional classification, proof-assistant certification or worldwide priority is within the claim.

Success requires the entire Kähler equality characterization, orientations and normalization, reality and injectivity of A on all 225 Hermitian coordinates, the exact full generator-hull section, PSD positivity without cancellation, normalized tensor identification, ambient linear inverse, arbitrary lift transfer, compact full-ideal moment argument, rational strict-gap stability and correct pointwise/local Harvey–Lawson interface. It also requires faithful source credit and versions, meaningful actual code executions, consistent current/historical records, complete original Git preservation, safe reproducible packaging and legible rendering. Finite checks support the elementary derivations; they do not establish the external theorem or the existential calibration by numerical infeasibility.

## Actionable finding

**PK02A — P3 — residual fused word boundary in current supplement.** `SUPPLEMENT.md:75` reads:

> Sturmfels's G(3,6)result excludes an unprojected LMI, not every finite lift.

Insert a space after the closing parenthesis: `G(3,6) result`. This is current reader-facing prose, not a code identifier or a historical record. It is a residual instance of round 01's PK02 copyediting obligation. The mathematical statement itself is correct. No corresponding fused occurrence appears in the current README, evidence index or metadata description/references. `receipts/PROSE_SCAN.json` records the exact current location.

Regenerate the manifest and deterministic archive after the prose repair, preserving original and historical bytes. Under the requested review/fix loop, changed bytes need a fresh whole-package review. No TeX/PDF or mathematical checker repair is required for this concern.

## Independent universal derivation and attempted falsification

### Kähler equality and orientation

Let J be the fixed orthogonal complex structure on the real underlying space of C6. The compression to a real four-plane is skew symmetric. Its two skew singular values have magnitude at most one. Evaluating `Phi=omega^2/2` gives their signed product. A positive value one forces both singular values one. Orthogonal compression then loses no component of Jv for every v in the plane, so the plane is J invariant. Its complex orientation is precisely the positive Pfaffian orientation. Conversely a complex-orthonormal pair gives the real oriented frame `(a,Ja,b,Jb)` of value one.

In a convex expression in mass-ball generators, all generator values are at most one. Equality of the average forces every positive-weight summand to be a maximizer. Thus the equality face really is the full hull of positive complex two-planes, rather than a sampled subset or an unsupported face classification. Reversing orientation gives Phi=-1. Totally real planes and planes containing only one complex line do not attain one. Near equality is insufficient for invariance; the proof uses exact equality.

### Full Hermitian embedding, signs and inverse

The independent sign calculation uses `u_j=(e_j-if_j)/sqrt(2)` in the +i eigenspace. In the complexification, all 225 `(2,2)` monomials `u_I wedge conjugate(u_J)` are complex independent. Hermitian coefficients make their sum real: conjugation exchanges I,J and degree-two exterior factors commute. Hence A is a real-linear injection on the entire 225-dimensional real Hermitian space, not just a nonlinear identification of pure projectors.

Replacing u with w=e-if introduces factor 1/4. On the standard real Hermitian basis the resulting real coefficients are rational. From `a wedge Ja=-i ahat wedge conjugate(ahat)`, the two -i factors give -1; reordering the middle antiholomorphic factor gives another -1. Therefore the projector identity has positive complex orientation. Unit decomposable z has a complex-orthonormal factorization, including any unit phase, and the resulting real plane is unit. The converse covers every Kähler maximizer. Thus `F=A(K)` exactly.

The trace and pure-block evaluations follow from diagonal paired-coordinate coefficients. Fresh exterior-algebra code, independent of the submitted determinant construction, reconstructs all 225 columns in 495-space and matches every certificate coefficient. It checks all 25,425 upper-triangle Gram entries; the Gram matrix has 15 diagonal ones and 210 diagonal twos, with zero off-diagonals. Rank 225 follows exactly. The ambient extension `G^{-1} A^T` is explicitly linear. A rational test using arbitrary full Hermitian coordinates is recovered exactly by that inverse. There is no nonlinear inversion of z or p-to-ppT substitution.

The new code additionally checks 32 varied rational complex a,b cases: product-projector identity, reality, both traces, unit-phase invariance and the squared Gram-determinant norm relation. These exact finite controls complement the full polynomial identity in the genuine symbolic baselines. They do not replace the universal exterior-algebra derivation.

### PSD support and normalized complex Sep section

Under `W=Lambda2 U + (U wedge Z) + Lambda2 Z`, the support functional `tr(P_D H)` is nonnegative on every unit decomposable projector. For a convex sum its value is a positive weighted sum of squared D-projection norms. Value zero forces every generating z into the mixed block. This is stronger than merely proving matrix support, and excludes cancellation. A fresh positive mixture control verifies that pure-block contribution cannot be canceled by mixed-block generators.

For a nonzero `a wedge b` in U wedge Z, both pure exterior components vanish. The two U projections are dependent, and the two Z projections are dependent. Neither span is zero, since that would place both factors in the other summand and force the mixed wedge to vanish. Their spans therefore have dimension one each. Writing the factors in these two spans gives a nonzero scalar times `x wedge y`. Conversely such a wedge is decomposable. This is exactly the N=2,k1=k2=1 specialization of Vrana–Lévay's prior theorem.

Orthogonality makes `T(x tensor y)=x wedge y` unitary. A unit decomposable mixed z can be rescaled to two unit factors, preserving its product projector. Under T the projector is `xx* tensor yy*`. The convex hull is therefore the normalized, complex, trace-one Sep(3,3) of Fawzi, with no real-only restriction or missing phase factors.

On A(H), the ambient Q equals `tr(P_D H)`. The two equations Phi=1,Q=0 are imposed simultaneously **inside the mass ball**. Q is nonnegative only on its Kähler equality face. A reversed pure complex coordinate plane provides an exact mass-ball generator with Q=-1, so any unsupported global Q-nonnegativity argument would fail. An exact normalized mixed rank-two entangled projector has Phi=1,Q=0 but is not in the generator hull: a rank-one PSD mixture can only use proportional generating vectors, and this vector is nondecomposable. This confirms why the two hyperplanes alone are insufficient. The manuscript and supplement retain this boundary explicitly.

### Arbitrary finite lift transfer

If the mass ball were the image pi(S) of any finite spectrahedron, adding the two equations to the projected lift variables gives the exact affine section. Applying the ambient extension of the left inverse gives a finite lift of normalized complex Sep(3,3). Arbitrary additional affine equalities may be retained or encoded within a finite LMI. Real-symmetric lifts are a subcase of the Hermitian definition; conversely a Hermitian LMI can be realified at finite size. Thus no restriction to unprojected LMIs, exposed faces of spectrahedra, equivariant lifts or a specified hierarchy is hidden in the transfer. Fawzi's exact established obstruction supplies the contradiction.

### Full real ideal, compact moment lift and rational functional

For compact nonempty unit-sphere X, `J2=I(X) intersect R[p]_{<=2}` is a finite-dimensional space, so a finite basis suffices. This is the full real vanishing ideal. No unproved claim about a particular generator list or degree of ideal multipliers is needed: any supporting affine-SOS discrepancy has degree at most two and belongs directly to J2.

The first moment matrix has M00=1 and annihilates J2. The sphere relation forces trace M=2. PSD then bounds all entries, and the feasible set is closed. It and its projected shadow are compact. Evaluation matrices include conv(X). If every supporting affine function were affine SOS, evaluation at every feasible moment matrix would make every support inequality nonnegative. Intersection of all supporting halfspaces would identify the shadow with conv(X), providing the forbidden finite lift of size 496 for the target. No Slater condition, SDP dual attainment or closure of a nonclosed shadow is presumed.

Therefore the compact shadow strictly contains the target. A point outside the compact convex mass ball is strictly separated. The support function on unit X is Lipschitz; the gap persists under sufficiently small coefficient perturbation. Rational coefficient vectors are dense, so a rational unnormalized failing coefficient vector exists. The same lifting matrix makes its supporting value negative, contradicting any affine SOS representation. Signed coordinate wedges span the ambient space, and a nonzero coefficient vector has positive maximum at least its largest absolute coordinate coefficient. This validates positive normalization without supplying the maximum or normalized rational coefficients.

Fresh exact controls check the sphere trace-two relation and equality between moment evaluation of an affine square and the nonnegative weighted square evaluations. They test the algebraic interface, not target numerical separation. The existence of the strict gap follows from the proved nonrepresentability and compact separation.

### Calibration completion and optional converse

The normalized functional phi has absolute comass one because X=-X. As a constant four-form on Euclidean R12 it is smooth and closed, attaining comass one everywhere. A finite completion on all simple vectors implies on X:

`1-phi = (1-phi)^2/2 + sum psi_j^2/2`.

Multiplication by the positive delta supplies an affine SOS for the original unnormalized support, contradicting its failure. A locally varying completion restricts at every point to such an algebraic identity; constant pointwise failure precludes it everywhere. The argument answers the original local Question 6.5 negatively in general, not merely an unrelated quadratic or nonclosed-form question.

For the optional converse, evaluating `1-phi=|a+Bp|^2` at ±p and using spanning gives `B^T a=-phi/2` and `|a|^2+|Bp|^2=1`. At a maximizer Bp0=-a, and evaluation at -p0 gives `|a|^2=1/2`. Orthogonal projection off a then gives `2|P Bp|^2=1-phi^2`. Homogeneity covers all simple vectors, including zero. The form coefficient map is linear. The proof makes no smooth-selection assertion from arbitrary pointwise solutions. Four exact rational sphere controls corroborate the two directions' normalization.

## Fresh primary bodies and credit obligations

Sixteen primary PDFs were freshly retrieved, with exact URL/version/hash records in `sources/SOURCE_FETCH_RECEIPT.json` and `sources/ADDITIONAL_FETCH_RECEIPT.json`. All fresh hashes equal the corresponding preserved source hash. Full relevant pages and critical rendered source pages were inspected; `sources/SOURCE_INSPECTION.json` records exact page sets and conclusions. Raw bodies remain under `sources/raw`; only authored descriptions belong in review evidence.

- Sanyal, OWR13/2015, PDF47–49 / printed707–709: original oriented mass ball, every supporting degree-at-most-one SOS conjecture, Sanyal–Rostalski work, experimental n<=7 context and Harvey–Lawson connection. The report's small-dimensional experiments are not promoted to proof or current worldwide openness.
- Harvey–Lawson, original Acta148(1982), PDF10–11/13/22/24 / printed56–57/59/68/70: mass/comass duality, closed calibration definition, local Question6.5 equation6.6 for all simple vectors and classical complex positive examples. The question is not misrepresented as a universal affirmative theorem.
- Fawzi, published CMP386(2021), PDF1–4 / printed1319–1322: normalized complex trace-one Sep, arbitrary projected Hermitian LMI equations2–3, Theorem1 and explicit3x3 specialization. PDF12–13 / printed1330–1331 were inspected for the Choi/dehomogenization interface, not treated as a new reproof. The arXivv1 body and official abstract confirm public4May2019 provenance. The generic n+m>5 shorthand is not extrapolated to trivial m=1; only the explicit3x3 case is used.
- Vrana–Lévay, arXiv0902.2269v2, PDF8–9, Section3.1 equation25, lemma and theorem: exact prior tensor-to-wedge decomposability. Credit is explicit in abstract, body, README, supplement and metadata.
- Grabowski–Kuś–Marmo, arXiv1111.4812v2, PDF8/10, Definition4.2 and Theorem5.1: established normalized decomposable fermionic projector hull and mixed-state convexification. The source's antisymmetrization metric convention changes a displayed scalar, not the normalized projector body under the standard exterior-space identification.
- Barvinok–Blekherman, published MSRI52(2005), PDF4–5: Example1.3 establishes standard oriented mass/comass/face background. The manuscript's direct compression derivation supplies its precise equality proof; its Kähler form is a classical positive example, not the failing calibration.
- Gouveia–Parrilo–Thomas, theta paper, PDF2/7/9: degree-at-most-k SOS includes constants; theta bodies, closure qualifications and moment matrix lineage are established. Their lifts paper, PDF2–3, and *Lifting for Simplicity*, PDF4/6, provide established projected/conic lift context. The compact trace argument is accurately framed as a self-contained specialization.
- Rostalski, slides dated15February2010, PDF26–29/34–36, and Gouveia–Thomas chapter printed323 / PDF336: earlier theta1/Harvey–Lawson connection and Sanyal–Rostalski attribution precede2015. Their historical open/numerical statements are not current global status claims.
- BSV, arXiv1308.0751v1, PDF1–2, Theorem1.1: nonnegative projective quadratics versus sums of homogeneous linear squares under its projective hypotheses. BKM, arXiv1908.03713v1 PDF15–16, already has Corollary4.2 in2019. Revised v2 PDF17 includes Corollary4.2 and Remark4.3 identifying the Sym2(exterior) representation. This orientation-losing quadratic body is distinct from the oriented exterior mass ball; the manuscript does not claim the first Grassmann-related no-shadow theorem.
- Sanyal–Sottile–Sturmfels, *Orbitopes*, PDF31–35, Theorem7.6: unprojected spectrahedron obstruction and explicit distinction from projected lifts. It is not substituted for Fawzi's stronger theorem.

All nine PF01–PF09 credit/framing obligations were checked against current TeX/PDF, README, supplement and metadata. The decisive Fawzi application framing, classical components, theta/lift lineage, prior equivalence, nearby quadratic results, lift distinctions, existential limitations, bounded priority/AI disclosure and fresh-review gate are all retained. The single P3 spacing defect does not change that substantive adoption.

The preserved query ledger contains exactly84 queries in21 batches. The four fetch ledgers contain25 successful primary PDF records with25 distinct hashes, plus one explicitly failed non-PDF response. This verifies the claimed bounded count rather than merely trusting a verdict. Three additional targeted search queries were noisy discovery only; no new full predecessor was identified, and no snippet is used as theorem evidence. The search remains incomplete and does not establish worldwide originality or current worldwide openness.

## Portable code, actual executions and round01 repairs

The standalone runner, full exact checker and extracted historical mutation function were inspected before execution. The old module is neither imported nor run; its UID1000/Linux permission harness is not invoked or simulated. Only reviewed literals and the pure mutation function are compiled from pinned bytes. The portable checker uses exact integer Gaussian pairs and Fraction parsing, deterministic determinant references, the complete polynomial projector calculation and mixed Plücker/minor relations. Explicit exceptions enforce required conditions in optimized modes; the optional old permission probe is not called.

The clean, safely extracted candidate ZIP executes exactly48 unique (mode,case) runs: three unchanged symbolic baselines and45 actual defective-certificate runs in normal/-O/-OO. Every baseline exits0, every fault exits1, and every stderr is empty. Complete stdout/stderr bytes, exits, certificate hashes and recursive JSON types match pinned references. The baselines verify all495 quartic exterior coordinates in24 real indeterminates with11760 nonzero terms, all225 embedding columns, full Gram/rank and both traces, and all nine mixed minors. The code does not fabricate negative output strings.

There are exactly six coordinate fault families and nine structure/metadata families. Every portable fault is rejected before the projector and minor checks; the unchanged baselines test those latter identities. The README, supplement and both metadata copies now describe this correctly. The erroneous broader PK01 coverage wording from round01 is globally repaired. Three optimization modes repeat the same cases; they are not three distinct mathematical mechanisms. No sandbox/security property or other-platform execution is claimed. The observed fresh host is macOS/Python3.14.6.

Fresh comparator tests distinguish Boolean/int, int/float and list/tuple recursively while accepting identical nested values. Additional hostile controls execute27 actual cases: five bad-certificate families (Boolean exterior index, Boolean coefficient, noncanonical fraction, zero entry and wrong exact denominator) plus four defective-source families (projector expected sign, Phi trace scale, Q pure trace scale and mixed expected sign), each in all three modes. All complete streams, exits, checker/input hashes and exact intended errors are saved. This verifies direct rejection at fragile polynomial/trace/minor boundaries beyond the portable certificate faults. These27 reviewer runs are clearly separate from the candidate48-run guarantee.

Independent family scripts and their historical writes/assertion guards are stage evidence, not promised portable read-only replays. Python standard-library execution requires no network, solver, special account or credentials. Fawzi, universal proof, exact calibration coefficients/comass and priority are outside the computational receipt's scope.

Round01 PK02 copyediting substantially repaired current word/number boundaries and synchronized metadata, but the single `G(3,6)result` boundary remains. Preserved original and historical reports intentionally retain their historical bytes and prose; their old spacing is not presented as a current editorial claim and is not a new repair demand.

## Archive, original completeness, navigation and state

Every one of the29 pinned original repository paths was freshly read with `git show` at the actual original head and matched its preserved public bytes/hash/size. A separate full recursive tree listing yields exactly the29-file pin set: this is whole-tree preservation, not merely29 selected matches. All29 copied authored round01 records match both the copy manifest and their actual local review originals.

All134 non-self manifest records match exact file sizes/SHA256s. Adding the self-excluded manifest gives exactly135 archive entries. Paths are ASCII, sorted, unique and casefold-unique, safe relative paths beneath the single top-level directory, without traversal, backslashes or symlinks. CRC validation passes. Every ZIP member matches its corresponding current candidate bytes. Fixed timestamps, regular-file attributes and deflate metadata agree with the builder. Rebuilding from exact entries and documented attributes yields byte-identical446002byte ZIP with the pinned hash.

The archive contains no raw third-party PDF/text/image bodies, caches, bytecode or duplicate packages. Current metadata equals its deposit wrapper exactly. Current README, supplement and index relative links resolve. All delivered JSON parses. Historical absolute paths, old input manifests, acceptance/PASS labels and original permission seals are clearly identified by the index as stage records. Round01's104-entry candidate pin remains a historical pin, while its29 authored copied records have current copy pins. The repaired135-entry candidate is not claimed equal to that earlier candidate.

`CURRENT_REVIEW_STATE.json` accurately records round01's two P3 concerns, applied repairs, false immutable-publication readiness, false all-issues-resolved and a pending NEW review02. Its pending state is not overwritten by this reviewer. This new P3 requires continued repair/review; even a future CLEAN review would not authorize an irreversible publication action.

## Full visual/source review

All six current PDF pages were freshly rendered at120dpi and individually viewed. Page1 title/abstract/original question/Fawzi interface, page2 theorem/Kähler/embedding equations, page3 support/section/lift transfer, page4 moment/rational/calibration/converse argument, page5 related work/limits/disclosure/first references and page6 remaining bibliography are legible. No clipping, overlap, missing glyphs, erroneous bars/signs, broken equation numbers, unresolved citations or reference markers were observed. All14 references correspond to the source bibliography. Bibliography continuation onto page6 is normal.

The complete source was read against the PDF. The current existing TeX log has no warning/overfull/underfull/undefined/citation lines. A terminal XeLaTeX compiler was unavailable, so this reviewer makes no fresh compiler-execution claim; current PDF/source consistency and existing successful-build evidence were assessed directly. No change requires regeneration of mathematical PDF bytes. Critical original/Fawzi/Vrana/fermionic/BKM source pages were also rendered and viewed, confirming the interfaces despite OCR imperfections in the old Harvey–Lawson scan.

## Strongest result and exact remaining gap

The full written mathematical theorem is verified as an elementary deduction from the exact established published Fawzi theorem, with no unresolved mathematical gap identified. Portable arithmetic and original preservation are reproducible, source credits and bounded-priority limits are sound, and the six-page rendering is clean. No explicit failing coefficient vector, comass value, minimality or worldwide priority has been established or is claimed.

The exact remaining package gap is PK02A at current `SUPPLEMENT.md:75`. Repair that spacing, regenerate inventory/archive and run the requested fresh full review loop. All candidate pins are checked again at final freeze. This review is100% complete, but the candidate has not reached zero actionable issues.

Frozen UTC: 2026-10-13T22:16:29.466198+00:00
