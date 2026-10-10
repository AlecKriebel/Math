# Independent audit of the exterior quotient investigation

Problem 1500024 / AMR-014-0024, queue rank 882. Reviewed 6 October 2026.

## Verdict and accepted scope

**Accept the bounded mathematical deductions and the unsolved disposition, with the separately frozen editorial clarification.** No error was found in the path-model identification, hyperplane homology recurrence, Koszul identity and odd support argument, cubic obstruction, or printed small-dimensional calculations. The five approaches do not prove the conjecture for general odd dimension.

The clarification concerns attribution and wording. The inspected 2026 preprint has different endpoints in its conjecture displays and its theorem; the theorem itself already has the correct endpoint. The derivative makes this distinction explicit. This is not a repaired proof, a newly discovered counterexample, or progress beyond the mathematical deductions in the original author freeze. All original author bytes remain unchanged.

This is an independent conventional mathematical audit, not formal verification or human peer review. The mathematical findings below were checked by direct reasoning. No numerical experiment, random specialization, rank-computation program, or unprovided executable checker is claimed as evidence. Commands were used only for provenance, source inspection, archive validation and exact patch replay.

## Frozen inputs and exact selection

The original six public files were read in full. The original ZIP has 13,958 bytes and SHA-256 `12fe11bb39480e3b5ea007700073c7f00b33770e7233f2e10998e3710fcad4cc`. Its external manifest has 1,642 bytes and SHA-256 `f7a8b632205875218a64d09067c6b76722a7daa581cb8c63bd7741e6203b559c`. The ZIP passes its CRC test, contains exactly the manifest's six regular files, and each member equals the corresponding original public file byte for byte. Every individual size and SHA-256 was recomputed, rather than accepted from the author summary.

The complete catalog, complete problem collection and complete research-results collection were separately read and hashed. Their sizes and hashes agree with all supplied pins. There is exactly one catalog entry and one complete problem record with ID 1500024. The selection is AMR-014-0024 at rank 882. The standalone statement hash is `5e008c914887baf017b7c2bdbfb19bb774cc8841e5a54c125be8f4f301fb5fe4`.

Serializing the **complete exact-ID problem record**, together with the report selected by its exact problem number, using `json.dumps([record, reports.get(problem_number,{})], sort_keys=True).encode()` with Python defaults produces 4,258 bytes and SHA-256 `ed59f0234ec2b85903563ce4ca2bd32f6d0a22aa76a02f2383d4d2be389e1a2b`. The author's locally selected catalog entry, problem and report equal the records recovered from the complete inputs. The whole report was inspected: it contains wording/source verification and literature triage, without a substantive mathematical proof attempt. Neither it nor the datasets is reproduced in this package.

`VERIFICATION_RESULTS.json` supplies the recomputed public hash/size/match metadata. Hash agreement authenticates the audit target and selection; it is not mathematical evidence and does not certify the truth of an inherited status summary.

## Primary sources and prior-results boundary

The exact target is Conjecture 4.3 of Fröberg–Lundqvist–Oneto–Shapiro, [arXiv:1801.01692v1](https://arxiv.org/abs/1801.01692v1). Its Section 4.4 uses the complex exterior algebra, and its polynomial notation is over the complex numbers. The target's two exterior generators are quadrics; the polynomial relations are coordinate squares and squares of two general linear forms. They are not arbitrary general quadrics.

Crispin Quiñonez–Lundqvist–Nenashev, [arXiv:1803.08918v1](https://arxiv.org/abs/1803.08918v1), is the source for the normal forms, upper bound, commutative/even equivalence, low coefficients and odd top coefficient. Theorem 1, Theorem 3, Theorem 5, Propositions 4, 6 and 7, and the Section 4.2 argument were inspected. Proposition 4 reports Macaulay2 verification through odd n=19; those calculations were not independently rerun. Its published journal reference was checked against the public arXiv record.

Boij–Lundqvist, [arXiv:2608.22823v1](https://arxiv.org/html/2608.22823v1), assumes characteristic zero. Theorem 5.5 establishes the commutative formula; Corollary 5.6 gives the even exterior consequence. Theorem 3.1 and the Section 5 proof were inspected, without independently reproving the underlying fat-point interpolation theorem. The public record gives submission on 24 August 2026 and showed no journal reference. The PDF/HTML title includes “powers of”; the abstract-page title omits those words.

The Conjectures 5.1–5.2 displays use floor(n/2); Theorem 5.5, its proof and subsequent top-coefficient discussion use the ceiling. PDF pages 14 and 18 were also rendered and visually checked, so this is not merely a text-extraction inference. We describe it as an apparent display-level inconsistency: the theorem already states the correct endpoint. It supplies no general odd exterior theorem.

All three PDF sizes and hashes match the author metadata. A fresh targeted web search located no additional general odd resolution; this is a bounded search, not a theorem that no such result exists. The saved author GitHub-search responses were inspected; their recorded empty exact-ID/keyword results support the stated bounded history gate. This audit did not repeat those repository searches or exhaust all historical branches. No new claim of an exhaustive literature or repository search is made.

## Assumptions and genericity

The entire accepted target is over C. The algebra is finite dimensional in the exterior and squarefree settings, with the usual degree-one grading on variables. Algebraically independent coefficient choices over Q avoid every nonzero rational determinantal condition involved in a multiplication matrix. For a fixed n, there are finitely many relevant degrees, and the intersection of the maximal-rank loci is a nonempty Zariski-open set. This justifies use of a generic Hilbert function; it does not mean that every concrete coefficient assignment is generic.

The odd canonical pencil is legitimate because it comes from the cited generic normal-form theorem, not because its small integer coefficients somehow qualify as algebraically independent. Basis changes and invertible recombinations of the two generators preserve the ideal up to graded isomorphism. The concrete canonical calculations consequently address generic exterior pencils over C. No step uses a finite-field calculation to infer characteristic-zero rank, and no positive-characteristic generalization is accepted.

For the commutative application, write the coefficients of the first n of the n+2 general forms as an n by n matrix M. On the nonempty determinant-open set, y=Mx is an invertible coordinate change. If the final coefficient rows are u and v, their y-coordinate rows are uM^{-1} and vM^{-1}. Conversely, given invertible M and arbitrary two rows in y-coordinates, multiplication by M recovers u and v. Thus general final rows remain general after this coordinate change, and the quotient becomes exactly the target coordinate squares plus two linear-form squares. A special squarefree sparse quadric is not substituted for a general linear-form square.

The source equivalence only transfers an all-dimensional commutative theorem to the even-dimensional exterior theorem. The accepted report does not reverse a specialization inequality or transfer that conclusion to an odd pencil.

## Sign-free path-model identification

Start with the odd canonical pencil on the basis a_1,...,a_k,b_1,...,b_(k+1):

    f = sum a_i b_i,           g = sum a_i b_(i+1).

The radical of f, viewed as a form on the dual space, is the line b_(k+1)^*, and that of g is the line b_1^*. For k>=1 their common radical is zero. For an even paired-block model with one unused variable, the unused dual coordinate lies in the common radical. Under a simultaneous congruence the common radical transforms by an invertible map; under invertible recombination, being annihilated by both new forms is equivalent to being annihilated by both old forms. Therefore simply adding an unused variable cannot produce the generic odd model.

Order the basis as b_1,a_1,b_2,a_2,...,a_k,b_(k+1), denoted z_1,...,z_(2k+1). Replacing f by -f makes its terms z_(2i-1)z_(2i), while g has terms z_(2i)z_(2i+1). These are precisely F and G in the report.

To check every sign, let J be an increasing subset disjoint from {j,j+1}. In sorting z_j z_(j+1) z_J, each element of J below j is crossed twice, and no element of J lies strictly between j and j+1. The total number of transpositions is even. If J intersects the edge, the product is zero in both algebras. Thus on their squarefree monomial bases, multiplication by each adjacent edge has exactly the same matrix in the exterior algebra and in C[x_1,...,x_n]/(x_1^2,...,x_n^2).

Summing edges preserves the equality of matrices for F and G. Since those generators have degree two and commute with every homogeneous element, the degree-s ideal equals the sum of the two multiplication images from degree s-2. The monomial identification therefore identifies the image sums and their cokernels. This proves the graded **vector-space** quotient identification in every degree. No algebra homomorphism between the two degree-one products is asserted or required. In particular this model does not turn F and G into squares of general linear forms.

## Hyperplane quotient and homology

For fixed nonzero ell in an (n+1)-dimensional vector space, the map from its exterior algebra to the exterior algebra on the quotient by ell is surjective in degree two. Consequently the map on pairs of quadrics is surjective. The inverse image of the generic n-dimensional Hilbert-function locus is nonempty and open. It intersects the nonempty open generic locus in n+1 dimensions because the parameter space is irreducible.

More explicitly, on a chart of nonzero ell, quotient coordinates can be chosen algebraically, so the same rank conditions define a nonempty open locus of pairs and hyperplanes. A general pair with a general ell lies in that locus. This is the generic interpretation of A/(ell) = E_n/(f,g). It is not a claim about arbitrary nongeneric restrictions.

In A, ell^2=0. In degree s, the cycles have dimension b_s-r_s and the boundaries have dimension r_(s-1), so

    eta_s = b_s-r_(s-1)-r_s.

The quotient dimension is q_s=b_s-r_(s-1). Substituting q_(s+1)=b_(s+1)-r_s yields eta_s=q_s+q_(s+1)-b_(s+1), hence q_(s+1)=b_(s+1)-q_s+eta_s. Degree zero gives q_0=1. These are exact rank-nullity identities. The even Hilbert function b alone does not determine the missing eta values; the report does not assume those values vanish.

The maximal-rank objection is valid. A nonzero ell in A_1 lies in the kernel of multiplication A_1 to A_2. Since quadratic relations leave A_1 unchanged and, for a generic independent pair, dim A_2=binom(N,2)-2>=N for N>=4, maximal rank would require injection and is impossible.

For N=4 the generic even normal form has two distinct block parameters, so the two quadrics span the same space as ab and cd. The quotient A therefore has degree-two basis ac,ad,bc,bd and no degree above two. For ell=a+b+c+d its four multiplication columns are

    (-1,-1,0,0), (0,0,-1,-1), (1,0,1,0), (0,1,0,1).

A linear combination of the first three vanishing forces its first coefficient to vanish from the ad coordinate, its second from bd, and its third from ac. Those three are independent, while the sum of all four is zero. The rank is three. Quotienting removes one degree-one dimension and three degree-two dimensions, giving 1+3t+t^2. This checks both the signs and the claimed lost coefficient under the invalid rank-four shortcut.

## Koszul degrees and the support cutoff

Write K_2=E(-4), K_1=E(-2)^2 and K_0=E. The differential w to (-gw,fw), followed by (u,v) to fu+gv, is zero because the quadrics commute. No regular-sequence assumption is valid or made.

In total degree s put d=s-4. The degree-s second homology is the simultaneous annihilator of f and g in E_d. Pair E_d with E_(n-d) using the coefficient of a chosen top wedge. For w in E_d and v in E_(n-d-2), the condition pairing(w,fv)=0 for every v is equivalent to fw=0, by nondegeneracy of the pairing between E_(d+2) and E_(n-d-2). The same holds for g; degree two introduces no parity sign. The orthogonal complement of the degree-(n-d) ideal therefore has dimension h_(n-d)=h_(n-s+4). This remains valid with zero graded pieces outside support.

The finite-complex Euler identity gives

    h_s-kappa_s+h_(n-s+4)
      = binom(n,s)-2binom(n,s-2)+binom(n,s-4).

The plus sign on the reflected term and its shift by four are both correct. It is the two-generator Koszul grading, rather than n-s or n-s+2.

For the support cutoff, on the 2k-dimensional symplectic part let L_i be wedge by a_i b_i and let Lambda_i be its Hermitian adjoint. On the four basis states 1,a_i,b_i,a_i b_i, the commutator [Lambda_i,L_i] has eigenvalues 1,0,0,-1. Operators associated to distinct pairs commute because they have even degree. Summing gives [Lambda,L]=(k-d)Id on degree d. Taking inner products yields

    ||L alpha||^2 = ||Lambda alpha||^2 + (k-d)||alpha||^2.

Hence L is injective for d<k. The transpose under top-wedge duality of L from degree t-2 to degree t is L from degree 2k-t to degree 2k-t+2. This transpose is injective when t>k, so the original map is surjective onto every degree above k. The quotient on the symplectic part has no degree above k. Adjoining the remaining exterior variable allows at most one extra degree; quotienting further by g cannot create a component. Thus h_d=0 for d>k+1.

For n=2k+1 and s<=k+1, the reflected degree n-s+4 is at least k+4, so the reflected quotient component vanishes. The report's h_s=P(n,s)+kappa_s and its equivalent desired formula kappa_s=a(n,s)-P(n,s) are correct. This identifies the unsolved homology count; it does not calculate it.

At n=5, Fz_2=Gz_4=z_2z_3z_4, so (z_2,-z_4) is a degree-three first syzygy. There can be no degree-three Koszul boundary because K_2 in that degree is E_(-1)=0. Its nonzero first-homology class proves that the complete-intersection shortcut loses a genuine term. No claim of a new syzygy discovery or general formula follows.

## Cubic obstruction and hand controls

For odd n>=5, lex order has leading monomials z_1z_2 and z_2z_3. The two leading cubic terms in z_1G-z_3F are the same ordered monomial z_1z_2z_3 and cancel. The next lexicographically greatest surviving term is z_1z_4z_5, with coefficient +1. Other terms containing z_1 involve later edges; all remaining terms of z_3F lack z_1. Neither proposed quadratic leading monomial divides z_1z_4z_5. Since the remainder belongs to the ideal and its leading monomial does not belong to the proposed leading ideal, the displayed two quadrics cannot be a Gröbner basis in this order. The adjacent-edge matrix/sign argument also validates this in the commutative squarefree quotient. No assertion is made about other orders or larger bases.

For n=5, the full degree-three multiplication lists are particularly transparent:

    Fz_1=134, Fz_2=234, Fz_3=123, Fz_4=124, Fz_5=125+345;
    Gz_1=123+145, Gz_2=245, Gz_3=345, Gz_4=234, Gz_5=235.

They yield nine distinct monomials individually in the ideal: 123,124,125,134,145,234,235,245,345. The sole missing monomial is 135. No product by F or G contains 135, since every nonzero term contains an adjacent edge. In degree three these products span the ideal, so its dimension is exactly nine. This proves h_3=1 without an unproved independence assertion.

The quadrics are independent, so h_2=10-2=8. Every four-element subset contains at least one of the nine killed triples; hence degree four and, by multiplication, all later degrees vanish. The Hilbert series is exactly 1+5t+8t^2+t^3. For comparison, avoiding the two monomials 12 and 23 gives the independence polynomial 1+3t+t^2 on variables 1,2,3, times (1+t)^2 for variables 4,5; its expansion is 1+5t+8t^2+5t^3+t^4. The discrepancy is exactly as reported.

At n=3 the surviving squarefree monomials are 1,z_1,z_2,z_3,z_1z_3, giving 1+3t+t^2. More generally b_1...b_(k+1) survives in the odd canonical quotient, because every term of either generator has a positive a-degree, and multiplying cannot decrease it. Along with the cited upper bound and the unique path in width one, this gives the already-known top coefficient one.

The rectangle/walk translation uses one horizontal increment per vertical step, for n+2 steps, with horizontal coordinate constrained to [0,n+2-2s]. For s=0 every increment is positive. A zero or negative width admits no such positive-length path under the stated convention. At odd top degree s=k+1 the width is one and all increments alternate, leaving one path. These conventions agree with the hand controls and do not use a floor truncation.

## Endpoint and publication safety

The cited low coefficients cover s<=floor(n/3)+1, and the top odd coefficient s=(n+1)/2 is already known. Therefore the remaining potentially undetermined odd interval is floor(n/3)+2 through (n-1)/2. Beyond the cited finite range through n=19, the first odd dimension is n=21, with degrees 9 and 10 in that interval. This identifies what remains relative to the cited results, without certifying the older Macaulay2 runs or asserting an exhaustive current-literature theorem.

The investigation used five substantive approaches. The provenance/history gate is not counted as a sixth mathematical approach. The editorial clarification and this audit add no attempted solution approach. The accepted status is **unsolved**, with all-dimensional commutative and even-dimensional exterior results explicitly credited to prior literature.

The safe artifacts contain authored proof text, this audit, a separate acceptance, a small exact patch, and public verification metadata. They contain no PDF or extracted source text, dataset or record contents, search-response payloads, private coordination material, or source-page images. The patch only changes authored exposition/metadata. No repository write, commit, push, pull request, release, or external publication was performed by this audit. The acceptance is a mathematical/content gate for the specified bytes, not a publication receipt.
