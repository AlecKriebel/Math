# Independent audit: crossing minimizers and halving-line maximizers

Date: 8 October 2026. Problem 7200057 / AMR-071-0057.

## Verdict and accepted scope

The original frozen report requires one localized mathematical correction: its rounded quantitative slack inequality (4) did not assume that the lower bound being subtracted was integral. The corrected current report is accepted as a partial-result packet after that explicit correction. No complete solution or finite counterexample is certified. The five proof-search mechanisms remain exhausted, 5/5. This audit is verification and correction of those mechanisms, not a sixth approach.

The original report was read in full and every proof reconstructed. Its target, its small-order universal implication for 3 through 7 points, its weighted-profile tightness theorem, mutation lemmas, deletion identities and conditional induction, and its exact nonoptimal eight-point witnesses are valid within the hypotheses below. The audit preserves the distinction between a mathematical proof and bounded regression evidence.

`../current/REPORT.md` is the accepted current report. `CORRECTION.patch` is contextual correction history. Removed patch hunks are explicitly superseded, not endorsed statements. The full rejected original report is not included in this audit delivery. `ORIGINAL_PINS.json` identifies the unchanged original through hashes and sizes only.

## 1. Explicit correction and downstream impact

The original (4) inferred

E_last - L_last <= floor(B / a_last),

where B = U - A_n - sum_k a_k L_k. What the nonnegative-slack argument directly gives is E_last - L_last <= B/a_last. E_last is an integer, but its difference from an arbitrary real lower bound need not be an integer.

An exact counterexample to the unqualified rounding is n=4 with points (0,0), (6,0), (0,6), (1,1). The fourth point is strictly inside the outer triangle, no three are collinear, C=0 and E_0=3. The lower bound L_0=5/2 is universally valid because a general-position planar hull has at least three vertices. Here A_4=-3, a_0=1, U=0. The original rounded statement reads 1/2 <= floor(1/2)=0 and is false.

The corrected simple form explicitly requires integral L_last. For arbitrary real lower bounds, the correct statement is

E_last - L_last <= floor(L_last + B/a_last) - L_last.

This follows by first rounding the bound on the integral E_last. In the counterexample the corrected right side is 1/2. The corrected report states both versions and separates n=3 from the m>=1 discussion, avoiding the otherwise undefined last coordinate when m=0.

No downstream theorem uses the defective floor operation. The tightness theorem uses a zero sum of nonnegative slacks and remains valid even for real L_k. The hull argument uses exact identities; mutation and deletion proofs use exact integer counts; the obstruction witnesses use exact coordinates. Searches through the full report, status, verification text and checker found no second use of the invalid rounding. The old checker did not exercise (4), explaining why all original runs could pass despite this proof defect. The corrected supplied checker and the independent checker both contain the exact rational-L regression.

## 2. Target and hypotheses

The target is universal over each crossing minimizer, for each n>=3, among realizable real-plane point sets with distinct points and no three collinear. It is stronger than existence of one simultaneous optimizer. The reverse implication is a separate question. Finite attainable integer ranges establish existence of both extrema; compactness is unnecessary. A nonstretchable abstract order type would not be an admissible counterexample.

Crossings count unordered edge pairs meeting in relative interiors, not distinct intersection locations. A separate convex six-point fixture has 15 crossing pairs but 13 locations because of concurrence. It checks that the distinction matters even in general position.

The halving index is floor((n-2)/2). For odd n the two open-side cardinalities differ by one. An equal-split definition at odd n would invalidate the target and all parity arguments.

## 3. Reconstructed proof: weighted profiles and tightness

For each supporting pair, choosing one additional point on each side contributes j(n-2-j). A convex four-set contributes two such supporting pairs; a four-set with one interior point contributes three. Thus the total is 3 binom(n,4)-C. This proves identity (1) without importing the source's mutation-based proof.

Since e_j=E_j-E_(j-1), summation by parts with sum e_j=N yields the stated constant A_n and coefficients a_k=w_(k+1)-w_k=n-3-2k. All coefficients in the sum are positive. The last is 1 for even n and 2 for odd n. Also H=N-E_(m-1) when m>=1.

If a configuration attains the weighted lower-bound sum, the actual optimum equals that lower bound. For any minimizer the weighted sum of nonnegative slacks is zero. Positive coefficients force every slack to vanish, including the final coordinate. This proves the every-minimizer conclusion, not merely an existence statement. Its missing global hypothesis is simultaneous attainability of the lower-bound certificate. Separate sharp coordinates or formal integer profiles do not supply a common realizer.

The quantitative extension is valid only in its corrected form from Section 1 of this audit.

## 4. Reconstructed proof: triangular hull and n<=7

The source hypotheses and quantifiers were checked directly in S1. Theorem 4 applies to every general-position crossing minimizer at every n>=3. Theorem 7 supplies at least one triangular-hull halving maximizer. The next source paragraph explicitly rules out replacing its existential quantifier by a universal one. The report uses these two different statements correctly.

For n=3, C=0 and H=3. At n=4 and n=5 the weighted identity gives C+H=3 and C+2H=15 for every admissible set, so crossing minimization and halving maximization coincide. At n=6, triangular hull gives e_0=3 and e_1+e_2=12; substitution gives C=9-H. At n=7 it gives e_1+e_2=18 and C=33-2H. For any crossing minimizer P and a triangular halving maximizer Q, both triangular by the distinct source results, C(P)<=C(Q) implies H(P)>=H(Q)=h_n. The definition of h_n provides the reverse inequality.

At n=8, e_1+e_2+e_3=25 and the weights 5,8,9 yield C=-15+4e_1+e_2 and H=10-C+3e_1. The surviving e_1 parameter blocks this scalar argument. It does not by itself disprove the conjecture.

## 5. Reconstructed proof: generic mutations

In an isolated triple reversal the center point crosses the relative interior of the opposite segment. Only four-sets containing that triple can change convexity. The k same-side fourth points change from nonconvex to convex; the n-3-k opposite-side points change the other way. Therefore delta C=2k-n+3.

Only the three supporting pairs within the triple change side counts. For k<(n-3)/2 their before multiplicities are two k-edges and one (k+1)-edge; afterward they are one and two. Thus the entire edge profile changes by minus one at k and plus one at k+1. At the balanced odd value the profile is unchanged. Increasing mutations are the reversals, with the complementary index n-3-k. These facts imply the report's parity-specific changes in H and preservation of H along a nonincreasing-C mutation path.

The source defines precisely this isolated event and permits relabeling so that the point in the center role crosses the segment. The formula is not justified for an unresolved simultaneous degeneracy.

Repeated strictly decreasing mutations terminate because C is a nonnegative integer. Starting at a halving maximizer preserves maximal H. The endpoint is only locally crossing-minimal. Global accessibility to each crossing minimizer is the explicit additional hypothesis in the conditional result; configuration-space connectedness does not prove it. No claim of a certified nonglobal local minimum is made.

The independent checker constructs 55 separate fixtures for n=3 through 12 and every k, checks that exactly one triple reverses, and verifies the full profile transfer, rather than only the two objective values.

## 6. Reconstructed proof: deletion identities and induction

Each crossing pair has four distinct endpoints, so it survives exactly n-4 vertex deletions. This gives the crossing deletion sum.

For odd n=2r+1, an original halving pair has sides r-1 and r. It is halving after deleting any of the r larger-side points and no other point. A nonhalving pair cannot reach equal sides by one deletion. Hence the halving sum is rH.

For even n=2r, an original halving pair survives in all n-2 deletions away from its endpoints. An edge of type r-2 has sides r-2 and r and becomes almost-halving in precisely the r larger-side deletions. All other types contribute zero. Hence the sum is (n-2)H+r e_(r-2). This includes n=4. Endpoint deletions contribute nothing in both parities.

For the conditional odd-order theorem, every deletion crossing count is at least c_(n-1). If their sum equals n c_(n-1), every deletion is optimal. The induction hypothesis then makes all deletion halving counts h_(n-1). The odd halving identity gives H=n h_(n-1)/r. Applying the same identity to an arbitrary competitor bounds its H by this value. Integrality follows from the attaining configuration, rather than being an extra assumption.

For defect D, every nonoptimal deletion has integer crossing defect at least one; at most D deletions are nonoptimal. At least max(0,n-D) deletions therefore contribute h_(n-1), while all others contribute nonnegative counts. This proves (12). Neither exact deletion-bound equality nor an even-order scalar analogue has been silently assumed.

## 7. Exact witnesses and independent geometry

The checker does not import or call the supplied geometry code. It solves rational line-intersection equations by Gauss-Jordan elimination. Independently it finds the affine dependence of each four-set: a 2-versus-2 sign split detects convex position, while a 1-versus-3 split detects an interior point. It counts line sides using canonical rational slope equations. Hull vertices are tested through containment in triangles of the other points, not a monotone-chain hull routine. These independent representations reproduce all listed values:

- P: e=(3,6,13,6), C=22, H=6.
- Q: e=(3,7,9,9), C=22, H=9.
- R: e=(3,6,10,9), C=19, H=9.

All triples are noncollinear and every listed inner point has positive barycentric coordinates in the fixed outer triangle. The exchange Q-P=(0,1,-4,3) preserves the sum of edges and has weighted sum 5-32+27=0. It increases H by three while preserving C. R gives c_8<=19<22, so neither P nor Q is a crossing minimizer. No exact value of c_8 or h_8 is required. The witnesses refute a profile-recovery shortcut, not the conjecture.

The independent suite also checks every witness deletion, 24 independently generated auxiliary configurations of orders 3 through 10 and their deletions, 55 mutations, the concurrence fixture, and 81 bounded corrected-rounding algebra cases. These finite checks support the reconstructed proofs; they do not enumerate order types or establish new global extrema.

## 8. Source checks and limits

All four retained complete public-source PDFs match their original byte counts and SHA-256 hashes. `SOURCE_VERIFICATION.json` records only metadata. No source document, extracted text, source image, copied coordinate dataset or private coordination record is part of this deliverable.

- S1: [arXiv math/0608610v2](https://arxiv.org/pdf/math/0608610v2). Theorem 4 is on printed p.5; definitions and Lemma 5 on p.6; Lemma 6 and Theorem 7 on p.7; mutation Lemma 1 and its proof on pp.3-4; the target question is in Section 4, p.12. The pinned manuscript is the October 2006 arXiv version, distinct from the January 2007 author-hosted revision and 2007 journal publication.
- S2: [arXiv 1102.5065v2](https://arxiv.org/pdf/1102.5065v2). Definitions on p.2 and exact-extremum scope in Table 1 and Section 4 support the report. Exact extremal values through n=27 do not, by themselves, classify every optimizer; this qualification does not claim that stronger consequences cannot be extracted from that paper's proofs.
- S3: [Axioms 14 (2025), 62](https://www.mdpi.com/2075-1680/14/1/62). Indexed primary journal text confirms the every-minimizer conjecture, its express non-refutation caveat and publication on 16 January 2025. Complete journal-PDF inspection remains unclaimed.
- S4: [Preprints.org 202411.1953 v1](https://www.preprints.org/manuscript/202411.1953/v1/download). Printed pp.1-2, PDF pages 2-3 after the cover, support the same formulation and conditional status. Its unreviewed preprint status is not confused with S3.
- S5: [author-deposited 32-point manuscript](https://oa.upm.es/57576/7/INVE_MEM_2018_307610.pdf). The introduction and concluding remark/discussion distinguish an unconditional halving lower bound from a conjecture-dependent crossing improvement. No global crossing-minimum certificate follows.

This targeted source audit did not repeat the packet's broad bounded literature search. It accepts the carefully limited statement that the original investigation found no verified resolution; it does not independently certify worldwide openness, priority or best-known status.

## 9. Reproducibility and acceptance conditions

The exact supplied original, corrected current and independent audit payloads are hash-pinned externally. Runs under normal Python, -O and -OO use effective UID 1000. Read-only tests actually attempt new-file creation and write-opening every existing file and require PermissionError, in addition to checking writability flags. Before/after external hashes include the manifest files themselves. No original file is modified.

Ten semantic mutants exercise wrong crossing multiplicity, weighted identity, final parity coefficient, omitted n=8 parameter, crossing deletion coefficient, odd deletion coefficient, missing even adjacent-edge term, reversed mutation sign, reversed complete profile transfer, and the original unqualified floor inequality. Each is required to fail under all three optimization modes; a mere changed report hash is not substituted for these mathematical controls. Separate integrity and path controls reject report tampering, writable trees, internal output destinations and unexpected files, while an external output destination succeeds.

The public acceptance receipt records exact commands, return codes, output hashes, counts and before/after equality. A successful regression alone would not establish a universal theorem; acceptance relies on the reconstructed arguments and checked source hypotheses above. The permission freeze is not kernel immutability against an owner who can chmod files.
