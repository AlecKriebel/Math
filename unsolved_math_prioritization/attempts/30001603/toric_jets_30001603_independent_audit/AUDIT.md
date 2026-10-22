# Independent audit: jet spanning from toric positivity

Target: rank 698, ID 30001603 / OWR-4527-007. Audit date: 2026-10-05 UTC.

## Verdict

**Mathematical refutation verified. Frozen packet requires a factual source correction before publication or unconditional acceptance.**

The proposed counterexample is a genuine rank-three toric vector bundle on the complex projective plane. It is nef (indeed ample), has invariant-curve minimum degree tau = 1, and fails even value generation at one fixed point. The complete first-jet image there has dimension 7 rather than 9. This contradicts the precise primary conjecture at k = 1. The original construction is prior work of Di Rocco, Jabbusch, and Smith (DJS), not a new counterexample.

The sole blocking finding in this audit is the repeated claim that the journal prints an incorrect polygon vertex. **It does not:** the journal PDF bound below prints (-1,-2), agreeing with arXiv v3 and the bundle data. The packet's statement that the journal prints (-1,2) is false. Correct the descriptions and labels, regenerate the dependent hashes, and obtain a bound delta review. No change to the bundle, gluing, section enumeration, or numerical conclusions is needed. CORRECTIONS.md identifies every affected location.

Recommended eventual disposition: `already_solved`, preserving the recorded 1/5 substantive author turns, after the correction gate. The source-description repair and this independent audit are not additional mathematical approaches. The present verdict does not authenticate a future revised packet.

## 1. Exact object reviewed and audit independence

The ten-file frozen packet was authenticated against two externally supplied anchors:

- MANIFEST.json: 5ae79fd9ca09fc095a33d7acfa27818377163c1eb2161977ff172cf641420616
- PROOF.md: 76d197a8fc07f7e3796d67a24308531aa315b0aa03a69f3a2122c3bdf7f77b68

All nine manifest members matched their byte counts and hashes. The directory contained exactly the intended ten regular, non-symlink files. The packet was not edited. EXACT_BINDING.json lists every input's independent byte count and hash.

I read the complete proof and all accompanying public files, freshly downloaded all four scholarly PDFs, inspected relevant text and rendered pages, and independently recomputed the mathematics. The new code does not import author modules. Its principal section calculation solves a single ungraded polynomial-extension problem using SymPy rational matrices; the author's program instead enumerates torus weights and solves filtration constraints using its own rational-arithmetic routines. The author programs were also replayed separately. No helpers or remote writes were used.

## 2. Source and hypothesis gate

The complete Jabbusch contribution, printed pp.2640–2641 of [OWR45/2010](https://doi.org/10.4171/owr/2010/45), was checked in text and full-page renders, including its beginning, definitions, conjectural paragraph, and references. The field is algebraically closed; the toric setup is smooth and complete, and the jet-definition paragraph imposes projectivity. The conjecture concerns tau(E) >= k implying k-jet spanning for k >= 1. Tau is the minimum summand degree across invariant curves. Global generation is not an additional hypothesis. The preceding k = 0 caveat does not exclude the proposed k = 1 counterexample. The complex projective plane meets all these conditions. Failure at a single point suffices; no equivalence between fixed-point testing and testing every point is needed.

DJS's [arXiv v3 record](https://arxiv.org/abs/1409.3109v3) establishes first submission on September 10, 2014 and v3 on February 1, 2017. The [journal offprint](https://ggsmith.ca/Papers/diRoccoJabbuschSmith.pdf) identifies volume 370, number 11, November 2018, pp.7715–7741, DOI [10.1090/tran/7201](https://doi.org/10.1090/tran/7201), with electronic publication May 30, 2018. Its first page also records receipt February 12, 2016 and revisions January 25 and February 1, 2017. Examples 4.2 and 5.3 contain the applicable bundle. The audit uses the inspected v3 and journal versions; it does not assert that every detail already occurs in v1.

The Hering–Mustata–Payne (HMP) [primary paper](https://doi.org/10.5802/aif.2534), pp.609–611, supplies the quotient-projectivization convention and the full invariant-curve nef/ample criterion. Its relevant proof was read. Standard facts about projective cycle limits, locally free sheaf gluing, torus gradings, and line bundles on the projective line remain foundational inputs rather than proof-assistant-certified axioms.

## 3. Construction, local freeness, and equivariance

Take the three standard rays (1,0), (0,1), (-1,-1). Each pair in the stated fan is a unimodular cone, giving the usual three charts of P2. Their rings are C[y/x,1/x], C[x/y,1/y], and C[x,y]. The constant basis matrices in PROOF.md are invertible, and the listed character pairs agree with the inspected source data.

Construct each frame directly inside C(x,y)^3 as B_i diag(x^(-a_j)y^(-b_j)). Independent symbolic inversion and multiplication give exactly the three displayed transition matrices. The six ordered transitions are regular on the corresponding overlaps. For the displayed directions, determinants are y^8, x^8, and s^8; these are units in C[x,y,y^-1], C[x,x^-1,y], and C[s,s^-1,t], respectively. Thus the inverses are regular as well. Every triple cocycle holds as a rational identity, and this is sufficient on the overlaps because the chart modules embed in the same rational vector space.

Consequently the free rank-three chart modules glue to a locally free sheaf, not merely to an arbitrary torsion-free object. Each generator is a constant vector times a character. Pullback by the torus preserves the chart module and is linear on fibers; the compatible action therefore glues. This directly proves existence of the toric bundle without invoking an unverified filtration-realizability assertion.

A deliberately modified local character is rejected because an overlap entry acquires a pole. A separate modification of one transition, while leaving the other transitions fixed, breaks a cocycle. Constructing all transitions from frames makes cocycles tautological, so the second control specifically checks the independent-transition failure mode.

## 4. Curve degrees and positivity

Restricting G32 to x = 0 gives diag(y,-y^3,-y^4). Restricting G31 to y = 0 gives diag(x^5,x^2,x). Restricting G21 to t = 0 gives a monomial permutation matrix with exponents 6,1,1. These curves are the three invariant projective lines and cover all invariant curves on P2.

The sign convention was checked rather than assumed: for coordinate z at zero and z^-1 at infinity, frames related by f_infinity = z^a f_zero define O(a). In the infinity frame, f_zero has coefficient (z^-1)^a and hence a zero of order a. Nonzero constants and a constant permutation do not change the splitting degrees. The three unordered splitting types are therefore (4,3,1), (5,2,1), and (6,1,1). Their minimum is exactly 1, matching the original definition of tau, not a surrogate normalization.

The nef argument in PROOF.md is valid. Under the quotient convention P(F) = Proj Sym F, the line bundle L = O(1) restricts to the ordinary positive O(1) on fibers. On the projectivization of each invariant-curve restriction, L is globally generated because all three summands have nonnegative degree, so it has nonnegative degree on every curve there.

For completeness, the degeneration argument requires projectivity of P(F), which follows here from P2 being projective and F being a vector bundle. An arbitrary effective curve cycle has a limit under each coordinate one-parameter subgroup in a proper projective cycle space. The limits preserve numerical degrees. Apply the two limits successively. Commutativity preserves the first invariance during the second degeneration. The connected torus fixes each irreducible component of the final finite cycle, whose image is either an invariant curve or a fixed point. The preceding two positivity checks cover both cases. Additivity and preservation of degree yield L.C >= 0 for every curve C, hence nefness. This is the required geometric argument; the finite script does not establish it on its own.

All splitting degrees are strictly positive, so the ample half of HMP also applies. Ampleness is correctly attributed and is stronger than necessary. The proof would remain a complete refutation if the word ample were omitted.

## 5. Full global sections: independent exhaustive derivation

The filtration formula in the packet follows directly from monomial regularity in each chart. At a fixed Laurent weight, a forbidden coefficient cannot be canceled by a different weight. The basis changes are constant, so collecting equal weights before testing handles every possible cancellation. Thus the claimed ray-intersection formula is valid. At weight zero the first two filtrations force a multiple of e2, and the third requires coordinate sum zero, giving zero. This already excludes the missing middle value direction at the chart-3 origin.

The independent check uses a different representation. Write a section on chart 3 in its own frame as a polynomial column (p1,p2,p3). The highest third-ray height of the bundle is 3. A coefficient monomial x^a y^b in component j has Laurent weight u_3j - (a,b), and therefore a+b <= (u_3j,1 + u_3j,2) + 3. The sums of the three chart-3 weights are 2,0,2, yielding total-degree bounds 5,3,5. This proves that the arbitrary-polynomial ansatz is exhaustive; it is not an empirical search cutoff.

There are 21 + 10 + 21 = 52 possible coefficients. Transform this arbitrary column by F1^-1 F3 and F2^-1 F3, substitute (x,y) = (1/w,z/w) and (s/t,1/t), and set every negative-power Laurent coefficient to zero. The resulting 88 equations have rational rank 40 and nullity 12. Every resulting kernel vector was re-extended to all charts and checked for regularity. No filtration-intersection function or author linear-algebra helper is used in this calculation.

Up to nonzero scalars, a particularly transparent chart-3 basis is:

- (1,0,0), (x,0,0), (y,0,0)
- (0,0,1), (0,0,x), (0,0,y)
- (x^5,-xy^2,0), (x^4y,-y^3,0), (x^4,-y^2,0)
- (0,x^2,-xy^3), (0,xy,-y^4), (0,x,-y^3)

They transform into exactly the twelve Laurent weights and four vector lines enumerated in PROOF.md. This verifies the enumeration without accepting a diagram, an expected dimension, or the author's output as an oracle. The packet's own four-case exhaustive argument was separately read and has no missing range or overlap error.

## 6. Values, jets, and logical refutation

At the chart-3 origin, the first and fourth displayed basis vectors give the first and third fiber directions. Every middle component vanishes, so value rank is exactly 2. After reduction modulo (x,y)^2, the first and third frame components each contribute their constant, x, and y terms; (0,x,-y^3) adds the middle x term. The other middle contributions have total degree at least two. Therefore the seven nonzero jet directions are independent, and exactly the middle value and middle y derivative are absent.

Independently transformed chart-1 and chart-2 section matrices give value ranks 3,3 and first-jet ranks 9,9. The chart-3 ranks are 2 and 7. First-jet target dimension is rank(F) times dim C[x,y]/(x,y)^2 = 3*3 = 9. These calculations use jets as residues modulo the square of the maximal ideal; over C the equivalent first-derivative coordinates introduce no characteristic issue.

Surjectivity onto first jets would imply surjectivity onto values by composing with the quotient from O/m^2 to O/m. Consequently failure of value generation directly refutes first-jet spanning. Since tau = 1 and k = 1 is expressly allowed, every premise of the original universal implication is met and its conclusion fails. No claim about positive characteristic, all k, or a strengthened globally generated hypothesis is required.

## 7. Source-error finding and dependency analysis

Fresh downloads reproduce all four PDF hashes recorded by the author. In particular, the alleged faulty journal PDF is exactly 365,988 bytes with SHA-256 29d020ccdfffbb91149ed6d72bd3c32306865dc7d4f503bbf581d241b32d0a2b. Printed p.7728 (PDF page 14, one-based) was inspected as a full page and as a high-resolution direct PDF render. Its polygon for e1-e2 has vertices (-1,-2), (0,-2), (0,-3). Independent text extraction agrees. ArXiv v3 p.13 also prints (-1,-2). The coordinate (-1,2) does occur on the same journal page, but as a valid vertex of the different polygon indexed by e3. This audit does not infer how the author packet's misreading occurred.

The e1-e2 height bounds are (0,-2,3), yielding a <= 0, b <= -2, a+b >= -3. They independently force the three correct vertices. Substituting (-1,2) would violate b <= -2, and the corresponding section has poles. That is a valid synthetic corruption control. It is not evidence of a flaw in DJS. Rename the control accordingly.

The false allegation has no input dependency in the gluing or section calculations, which already use (-1,-2). It propagates through explanatory text, one check label/comment and one output key. Changing those descriptions requires regenerating RESULTS.json, MANIFEST.json, and the external anchors even though all 79 author assertions and all mathematical quantities should remain unchanged. The exact affected locations and replacement text are in CORRECTIONS.md.

## 8. Integrity and adversarial controls

The author verifier reproduced RESULTS.json byte for byte and reported 79 checks. CHECK_PACKET.py reproduced its pass and rejected its three temporary-copy mutations. The new independent verifier passed 60 checks, including rational frame identities, the ungraded section-system rank, all three value/jet ranks, and these mathematical controls:

- Alter one local character: overlap regularity fails.
- Alter a transition independently: a cocycle fails.
- Pretend the constant e2 section is global: extension has a pole.
- O^3: 3 sections and first-jet rank 3, preventing confusion between value and jet generation.
- O(1)^3: 9 sections and first-jet rank 9 on every chart.
- O(-1)^3: no global sections, detecting the degree-sign convention.
- Synthetically flip the e1-e2 vertex sign: the candidate fails regularity.

Eight independently anchored corruption controls rejected appended proof bytes, an equal-length proof mutation, removal, addition, a symlink member, duplicate manifest keys, recomputation of an internal manifest after tampering, and replacement of the reported results. The external manifest anchor defeats a self-consistent rewritten packet. None of these tests can validate a claim about what is printed in a PDF; human-readable source inspection supplied that missing check and found the error.

The frozen packet was authenticated before and after the independent computation, and again when finalizing this audit. No source PDF, extract, image, raw catalogue record, full dataset, or private coordination file belongs to the public audit deliverables.

## 9. Identity, provenance limits, and final gate

The full local descriptor catalogue independently hashes to 21,735,099 bytes, SHA-256 891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566, Git blob bd5c23e4e6c7e1901717a7e596477a7f6dc72425. The current GitHub connector returned that same catalogue blob. The selected descriptor matches ID, title, rank, number, and source DOI. The current queue blob 5d33a968894980499cb3fbb6d84fe5cca5a47aa4 still lists the target at rank 698, queued 0/5. Target-specific all-state PR and branch searches found no match at audit time; they are bounded searches, not exhaustive absence certificates.

The live problem page independently returned HTTP 403. Its contents and the old selected full corpus/AI record remain uninspected. A stored statement hash was not compared to unseen source bytes. The audit establishes primary-source mathematical identity through the descriptor and the original contribution, not a full-text hash match to the unavailable corpus. Public web queries and author bibliography checks found no correction invalidating the example, but absence of an erratum or earlier resolution is not exhaustively certified.

There is no residual mathematical obstacle to the attributed prior refutation of the inspected primary conjecture. Publication of this exact frozen packet remains blocked by its false source allegation. A corrected packet must be newly frozen and its changed files reviewed before acceptance; unchanged mathematical evidence can then be carried forward only through explicit hash binding and replay.
