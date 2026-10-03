# Geometry and Morse family review of PR377

Frozen head: 75bea4d3be9904e90c3843892671a440ba4d2c42.
Family verdict: PASS_GEOMETRY_MORSE_FOR_STATED_SCOPE. This is not whole-PR acceptance, an independent universal syzygy theorem, or a worldwide source-completeness finding.
Mandatory candidate repairs identified by this family: none.

The exact sharpness request is nonfree rational equivariant cohomology of order floor((r-1)/2) for every torus rank r>=5 in a rational Poincare duality setting. The candidate correctly presents a credited prior resolution, restricted to a=b=1 odd equilateral big polygon spaces and the extra sphere factor for even ranks. General-length order computation is corroboration, not the proof mechanism under review.

## Independence, artifacts, and reproduction

Before opening any candidate, history, root work, or sibling work, this family fetched, extracted and visually read the literal Franz contribution at EMS OWR49/2012 printed2954-2956, then Franz's actual primary arXiv1403.4485v4 (corrected2023 author version of IMRN2015). The independent proof, exact-control code, full stdout, source receipts and first research log were sealed at2026-10-03T05:06:38Z by independent_seal_manifest.json. Those sealed files were left unchanged. Subsequent acquisition and candidate reads are recorded separately.

The independent proof gives a regular-value argument for all generic nonnegative lengths, an explicit connectedness path, orientation and effective-rank checks, coordinate stabilizers and finite skeleton hypotheses. It derives a weighted Hessian congruence for arbitrary positive lengths and identifies the negative bundle and its reflection characters. Its proof is symbolic; 2,114 exact rational Hessian cases and 9,217 independently generated orientation-sign controls are local falsification checks. The sample counts make no universal inference.

After sealing, every file in the attempt packet was read in full, including all written guides, the prior review, metadata/manifests, and all three scripts. Only the relevant row416 of the large QUEUE was semantically inspected. All20 entries in snapshot_manifest.json match their bytes and SHA256 at the specified head. candidate_read_coverage.json binds the19 attempt files individually.

Full candidate replay outputs are retained and inspected:

- author_replay.stdout.txt:358,064 assertions,131,040 length subsets,35 symbolic Hessian cases,8,100 formal Koszul-square cases, matching SOURCE_CASE_CHECKS.json byte for byte.
- old_review_replay.stdout.txt:983 assertions, matching review/INDEPENDENT_CHECKS.json byte for byte.
- publication_replay.stdout.txt:18 publication-bound files,11 frozen author files,5 frozen review files, byte-exact replay receipts. Its source_pdfs_reverified field is explicitly false.

The source omission is real but stated: verify_publication.py checks packet hashes and replay outputs, not PDF content or hashes. This family independently downloaded allfour PDFs, including AFP1111.0957v2 and Franz-HuangAGT2020, and separately verified every SOURCE_MANIFEST byte count and SHA256. replay_and_source_receipt.json supplies that missing check. All third-party PDFs, extracts, images and a private SymPy1.14.0 dependency target remain under ignored raw_sources/. Two initial missing-dependency runs are preserved, not represented as successful evidence. They do not change the candidate.

## Claim-by-claim geometric audit

| Frozen guide location | Claim | Independent mechanism and status |
|---|---|---|
| line7 | Odd equilateral X is a closed regular level, compact, oriented, dimension3r-2 | PASS. An annihilating equation-gradient relation either vanishes or forces all u_j to be signed collinear unit vectors with signed length sum0. Odd equilateral rank forbids this. Fixed equation target orients the globally framed normal bundle. |
| line9 | Connectedness by pathwise scaling | PASS. Formula z_j(t)=sqrt(1-t^2|u_j|^2)xi_j remains continuous at initially zero z_j. The endpoint is (S^1)^r for this b=1 scope. No global phase selection or deformation retraction is claimed. |
| line11 | Effective rank, finite coordinate stabilizers, tame skeletons, source assumptions | PASS. u=0,z=(1,...,1) has trivial stabilizer. Stabilizers are exactly coordinate subtori indexed by zero z_j. X_i is a finite union of sets imposing z_j=0 outside a set of sizei. These compact real algebraic sets admit finite triangulations and satisfy local contractibility and finite ordinary pair cohomology. AFP Sections3.1,3.2 and Assumption4.1 were independently read and rendered. Hausdorffness and second countability hold by the Euclidean embedding. |
| line13 | Even-rank zero length is generic, splits as S3 times the odd example | PASS. The equations literally decouple. The number of positive1s is odd, so no signed sum is0. Replacing0 by0<epsilon<1 preserves the signed-gap sign. The new circle acts effectively on its S3 factor. |
| lines17-27 | Critical circles, index3|J| and exactly one-dimensional tangent kernel | PASS. For q=r-2|J|>0, the candidate angular form is q diag(s)-s s^T. Its kernel is the common-angle vector. Splitting off that vector through its positive signed norm gives inertia(|J|,r-|J|-1,1). The complex w-block adds2|J| negatives. |
| line27 | W_J supplies all negative directions | PASS. In the general independent coordinates x_j, set y_j=x_j+h onJ and x_i=h offJ. The exact restriction is -c sum_J l_j|y_j|^2-|sum_J l_j y_j|^2-c sum_J l_j|w_j|^2, with only the critical tangent kernel. It is maximal negative on the normal quotient. |
| line29 | Source sign/extrema cautions and equal-length restriction | PASS. Literal source3.10 has opposite derivative sign. Source p6 minimum/maximum wording is wrong in the chosen negative-f convention. Source3.9 also omits length weights. Candidate records the first two and restricts the unweighted function to equal lengths; thus it does not inherit the last defect. |
| line31 | Perfection by distinct reflection characters, with V_J,W_J basis | PASS. Reflecting the relevant real z_i coordinate reverses the negative bundle orientation exactly for i inJ and is trivial on P_J. Earlier levels have disjoint characters. The relative Thom groups have two generators, supplied by the fibre and sphere classes of W_J. Same-value critical components are handled simultaneously. |
| lines35-40 | Equivariant free bases, Euler coefficient t_i and shuffle sign | PASS. The ordinary cycle basis lifts by oriented invariant fundamental classes; this supplies the extra equivariant collapse input. The normal bundle to S1 in S3 is the complex weight-one line, whose Euler class is t_i. Bringing the final sphere factor into increasing order crosses exactly #{j inJ:j>i} odd-dimensional factors. |
| lines49-54 | PAL extension and corrected grading controls | The geometric PAL extension and shifts PASS against v4 Lemma4.4 and Proposition5.1. At a=b=1 the Koszul shifts are3m and3m+3; free shifts are3|J| and3|J|-2 as stated. The proof of the algebraic splitting/order belongs to the algebra family; this family found no geometric inconsistency. |
| line60 | Extra S3 Borel sphere bundle and free two-summand module | PASS. S3 is S(1 direct_sum L) over BS1. The oriented rank4 Euler class is the top Chern class, zero because of the trivial summand. Its Gysin sequence splits as Q[t] modules with generators in degrees0 and3. |
| line62 | Product action/Kunneth geometry | PASS. Torus and equations separate exactly. The even-rank product creates two shifts after extension by the new polynomial variable. Preservation of the exact syzygy order remains the algebra family's check. |

## New adversarial evidence and boundaries

1. General positive-length local Hessian. With c=l(J^c)-l(J)>0 and s=-1 onJ, the transverse real-u block is A=c diag(s_j l_j)-l l^T. Its exact inertia is(|J|,r-|J|-1,1). The proof uses D^{-1}l=s/c and l^T D^{-1}l=1, removing a positive direction in the rank-one congruence. This is materially broader than the candidate's equilateral characteristic-polynomial controls and does not rely on a general-length syzygy theorem.

2. A literal-source falsifier. For r=2,l=(1,2),u=(1,-1),z=0, the point lies in the complement of the weighted X but the printed unweighted f is0 with zero derivative. Thus the unweighted source display cannot serve as the general-length negative exhaustion. Candidate line29 already avoids this. No mandatory repair follows for its stated equilateral use.

3. The negative bundle and the fixed-sphere Euler map are different. The general negative bundle is direct_sum_{j inJ}(TS^{2a-1} direct_sum C_j^b). For nonemptyJ, its equivariant Euler class vanishes because the odd sphere tangent Euler class is0. Perfection cannot be justified by multiplication injectivity for that Euler class. The nonzero t_j^b in the inclusion map is the Euler class of the fixed-sphere normal C_j^b, with no tangent summand. Candidate uses the reflection method and does not make this confusion.

4. Zero-length Morse locus. For l=(0,1,1,1), the corrected weighted f is independent of the entire first V factor. Critical components are V times the old critical circles, not merely circles. D is singular and the positive-length inertia derivation must not be applied unchanged. The candidate uses a geometric product and Gysin/Kunneth extension instead, as required.

5. Nongeneric walls. Even all-one rank has signed collinear points at which the equation differential has an explicit nonzero relation. The genericity assumption is essential. The exact control includes these wall relations for ranks2,4,6,8,10. This is not a counterexample within candidate assumptions.

6. Higher b source caveat. The literal primary connectedness proof identifies the u=0 subset withT; for general b it is (S^{2b-1})^r. It remains connected. Candidate usesb=1 and is correct as written.

7. No use of general-length order as an assumption. Big polygon v4 Conjecture6.6 remains labelled a conjecture there. Franz-Huang's later Theorem1.2 and its Section2 characteristic-zero convention were acquired and checked as corroboration only; its full proof was not reconstructed by this family. Sharp existence needs only the equilateral case and zero-length product. The source qualification is exact to this target and these acquired papers, not global literature completeness.

## Remaining gaps and disposition

No unresolved geometric, Morse, Euler-map, orbit-hypothesis, or even-product gap remains for the frozen guide's stated a=b=1 scope. The global sharp upper bound, the exact Koszul order, extension closure and faithful-polynomial-extension assertions require the other families' independent judgments; this report supplies no final acceptance decision. The requested source omission is separately closed by actualfour-PDF hash verification, not by claiming verify_publication.py does it.

Optional additive improvement only: retain the exact weighted Hessian and zero-negative-Euler distinction in audit notes to prevent future broadening of the guide from importing the source display defects. This is a future boundary guard, not a candidate repair.
