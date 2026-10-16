# Independent adversarial review: PR 1037 invariant/constant-quotient family

## Disposition and exact limit

**PASS for the assigned invariant-space, determinant-character, and polynomial-lifting family.** No defect, missing hypothesis, or necessary mathematical repair was found in submitted Section 3 (Lemmas 3-5) or Section 5. The strongest independently verified all-n result in this family is:

For every n>=1, the all-partitions map Phi onto W=Lambda(U tensor Q^2)^SL2 is a constant rational surjection with dim W=C_n. For n>=2 and g in GL(U), det rho(g)=(det g)^C_n. Given the exact forest-transfer intertwining and Gaussian quotient determinant claimed in the other proof family, the full Bell-state determinant is divisible by (det A)^C_n in Z[a_ij].

**This is a modular verdict.** The theorem-level conclusion remains conditional on the separate family verifying the exact identity Phi L_A=G_A Phi and det(G_A|W)=(det A)^C_n with the same edge-subset conventions. I checked their stated algebraic interface for consistency, but did not read that family's report or independently enumerate every transfer entry in its finite examples. The written invariant and lifting arguments have no remaining internal gap. No exact multiplicity, irreducibility, complete factorization, new-method, publication, or priority claim is accepted or inferred.

## Frozen inputs and independence

The reviewed PR head is e87236a97c4b87818d2768cd5789043c7c3f4e39. All ten original files in SUBMITTED_PINS.json were hashed before review and their bytes matched the pinned snapshot. PROOF.md was 25072 bytes with SHA-256 546d9df387da3266b1b20d31b1cd6017a65fe9f497f1b37d2a99319e6194755c. INPUT_PIN.json records every original's byte count and hash.

I read the submitted theorem and proof, derived the assigned mechanisms in DERIVATION.md, wrote fresh exact code, and ran its checks before reading the historical submitted AUDIT.md or ACCEPTANCE.md. I read those two only afterward for provenance comparison. No other fresh-family report or code was read. The historical verdicts were not used as mathematical evidence. The historical audit describes finite checks but none of the ten submitted originals is an executable; its omitted historical computation cannot be replayed or simulated from this package. All checks described below are new code and new output, distinguished from that historical description.

All authored artifacts and third-party source bodies were written solely under reviews/invariant_01. No original input, Git branch/index, PR, queue, remote, service, or external individual was changed or contacted.

## Adversarial issue-by-issue findings

| Potential failure | Mechanism independently checked | Finding |
|---|---|---|
| Wrong infinitesimal sign or unproved rank | [E,F]=H, E*=F; on weight two, an orthogonal cokernel vector would give 2||w||^2=-||Ew||^2 | Correct; E:M_0->M_2 is onto, and weight-zero E-kernel is the whole invariant space |
| Complex argument failing over Q | Operator matrices have rational entries; ranks/kernels commute with extension to C | Correct rational dimensions and kernels |
| Spurious matching independence | Noncrossing matching tensors have distinct largest Dyck words; choose the largest largest-term in an alleged relation | Valid; the analogous all-matchings shortcut would fail |
| Exterior invariants assumed to lift without a section | Normalized antisymmetrization is an explicit equivariant section of exterior projection | Correct in every degree over Q |
| Only degree-two or low-degree invariant generation | Tensor invariant basis projects to products of paired b(u,v) in arbitrary even degree | Complete all-degree generation; odd degree excluded by -I |
| Anticommutation changes b's sign | epsilon projects to xi(u)barxi(v)-barxi(u)xi(v)=xi(u)barxi(v)+xi(v)barxi(u) | Plus sign is required and is correct |
| Diagonal generator factor omitted | b(ui,ui)=2q_in and b(ui,uj)=q_in+q_jn-q_ij | Correct; 1/2 is a rational constant, no integral-lattice claim is needed |
| Only noncrossing partition states justified | All q monomials either vanish or equal the forest polynomial of their arbitrary component partition | The actual Bell-state map is onto; noncrossing is used only in the tensor proof |
| Quotient depends on A | Phi(e_P)=f_P has rational constant coefficients | Constant kernel and constant quotient are established |
| Catalan formula fails at an endpoint | Exact binomial formula with zero out-of-range coefficients; m=0 gives W=Q | All n>=1 included; d_0=d_m=1 |
| Wrong determinant exponent | d_r=d_(m-r), scalar degree sum md, and equal torus exponents by permutation conjugacy | Each determinant exponent is d=C_n |
| Character only checked diagonally or numerically | Polynomial restriction to W, conjugacy, and density of distinct-eigenvalue matrices over C | All characteristic-zero fields covered by a rational polynomial identity |
| Generic kernel instead of a polynomial kernel | Rational splitting of Phi extends to a split exact sequence over Q[a_ij] | N tensor R is the actual kernel and a free direct summand |
| Quotient factor has variable denominators | Constant basis of kernel and constant quotient lifts produce K_A over Q[a_ij] | Actual polynomial factor, rather than rational spectral evidence |
| Matrix convention changes determinant | Column action L_A e_P=sum_Q T(P,Q)e_Q has matrix T-transpose | Determinant unaffected; convention explicit |
| Q-divisor fails to descend to Z | (det A)^C_n is primitive; the content argument forces integral quotient | Correct multivariate Gauss descent, including zero quotient |
| m=0 divided by zero in character proof | Lemma 5 restricted to m>0; n=1 transfer computed directly | Boundary case complete |

The full checkable derivation appears in DERIVATION.md. It shows where each implication is used and where the separate transfer/Gaussian obligation begins. No central difficulty is transferred to an unsupported invariant-basis theorem: the matching basis and explicit equivariant exterior section discharge that obligation within the proof.

## Fresh reproducible computations

Run from this folder:

    python3 verify_invariants.py --mode all --max-m 6 --max-n 7 --max-r 6 --output CHECK_RESULTS.json

The program uses only the Python standard library. Sparse integer elimination with gcd reduction computes ranks exactly over Q; Fraction elimination computes exact GL action determinants. There is no finite-field rank assumption, floating-point threshold, downloaded executable, historical code import, or transfer-enumeration implementation. Each individual mechanism has a separate selectable mode: sl2, partition, matching, character, projection, negative.

The saved CHECK_RESULTS.json includes interpreter version, timestamps, source-code hash, detailed dimensions, multidegree invariant multiplicities, matrix inputs, and exact determinant outputs. The completed final run passed. Its data are finite consistency and adversarial checks; the universal conclusion rests on the derivation.

| Fresh check | Range | Exact result |
|---|---|---|
| E,F commutator and adjoint | Every monomial in Lambda(Q^m tensor Q^2), m=0..6 | [E,F]=H and E*=F hold in even and odd degrees |
| E ranks | Every even degree for m=0..6 | Rank equals dimension of weight two; kernel dimensions equal d_r |
| Multidegree SL2 kernels and torus character | m=0..6 | Every coordinate's accumulated exponent is C_(m+1), including nontrivial internal degree multiplicities |
| All Bell partition images | n=1..7 | Counts 1,2,5,15,52,203,877; exact image ranks 1,2,5,14,42,132,429; kernel dimensions 0,0,0,1,10,71,448 |
| Partition image degrees | Every available degree at n=1..7 | Ranks equal d_r; E and F kill every image |
| Different tree representatives | Every partition at n=1..7 | Star and path products are exactly equal |
| Noncrossing epsilon tensors | r=0..6 | Counts and exact ranks 1,1,2,5,14,42,132; all leading Dyck coefficients +1 and distinct |
| Explicit rho matrices | m=1..4, 16 matrices total | Dense nonsymmetric, shear, cyclic permutation, and singular actions satisfy det rho=(det g)^C_(m+1) exactly |
| Normalized antisymmetrization | All 64 monomials for m=3, including every degree | Exterior projection is a left inverse and E commutes with the embedding |
| Paired epsilon-to-b projection | r=0..3 with nontrivial coefficient vectors | Exact products b(u,v) recovered with the stated signs |

Ten deliberate failure controls were detected: wrong minus sign in b, missing factor 2 in its diagonal identity, omitted diagonal generators at m=1,2,3, omitted invariant endpoint degrees, crossing-matchings falsely treated as distinct-leading basis, variable-denominator pseudo-factorization, reversed F sign, and omitted antisymmetrization factorial. The variable-denominator control is a mathematical counterexample (1=(1/x)*x) explaining why rational generic factorization alone is insufficient; it does not claim to mutate a computed transfer matrix. The other controls are exact failed algebraic identities or deficient ranks.

## Gaussian and transfer interface

For the complete theorem the separate family must establish the forest coefficient identity with each interlayer subset counted once and surviving signs +1. It must also verify the exact ordered operator factorization

    G_A=(det D) M_S rho(g_B) H_D,

with D the row-sum diagonal, B=D^-1 A, S=E-A^T D^-1 A, row-vector action u->uB, and det g_B=det A/det D. The present character calculation then gives the required quotient determinant only if both triangular factors preserve W and have determinant 1. The order matters: H_D is formed before substitution by B. The generic fraction-field calculation must be descended using the prior polynomial definition of G_A on a constant basis.

I checked compatibility of B1=1 with the zero-sum row hyperplane, quotient eigenvalue 1, symmetry and zero row sums of S, scalar factor raised to dim W, and the cancellation of all row-sum powers. These checks identify no interface conflict. They are not offered as a replacement for the assigned exact transfer/operator review. A proof only on invertible numerical matrices or with nonzero numerical row sums would be weaker than the submitted generic polynomial theorem; the constant-space polynomial identity prevents that limitation.

## Source and historical comparison

SOURCE_NOTES.md and sources/SOURCE_FETCHES.json record fresh primary bodies, exact hashes, and complete-page verification. The source check confirms the full Bell-partition problem statement and the distinction between the 2007 deferred basis announcement and the thesis's completed normalized polynomial treatment. The proof is self-contained; neither historical source announcement nor zero-parameter substitution into unnormalized scalar products is used to close an algebraic gap.

After the independent derivation and checks were saved, the historical AUDIT.md and ACCEPTANCE.md were read. Their invariant and lifting conclusions agree with this review. Their alleged finite executions remain unreplayed because the original package contains no executable artifact. This agreement is supplementary provenance information, not an independent mathematical premise. Nothing here establishes worldwide novelty, current unresolved status, formal proof-assistant validation, or human peer review.

## Remaining gap, repairs, and completion

Assigned-family internal gap: **none identified**. Necessary repairs to submitted Sections 3 or 5: **none**. Optional clarification: the normalized antisymmetrization factor could be written as 1/(2r)! and the separate largest-leading-word relation argument could be made explicit, but both are already supplied by the text's stated constructions and are not acceptance conditions.

The only theorem-level obligation outside this assigned family is the separate transfer/Gaussian verification identified above. This review does not depend on its findings and does not read its report. Subject to that separate obligation, the strongest scope is exactly the generic all-n integral Catalan divisor for the full Bell matrix. Exact multiplicity and novelty remain unclaimed.

All ten originals are rechecked in OUTPUT_PIN.json. The completion estimate for this assigned independent review is 100%; that percentage denotes review completion, not a claim of theorem novelty or overall project completion.
