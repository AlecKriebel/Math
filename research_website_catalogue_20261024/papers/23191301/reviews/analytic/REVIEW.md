# Independent analytic review — Zenodo 23191301

**Verdict: PASS for both clauses of Theorem 1 at the published scope.** No substantive mathematical defect or unresolved load-bearing gap was found. This is an AI review, not human peer review, formal proof-assistant verification, novelty certification, or publication clearance.

The verified claims are: `C(3*10^62,6,3)` is nonconvex with the specified disjoint coefficient-1 modified Motzkin sextics as inputs and their average as a witness; and for **each fixed odd q >= 3**, there exists a finite dimension n(q) in which `C(n(q),6,q)` is nonconvex. The proof also supports closedness of each fixed-power set and persistence under unused-variable extension. It does not supply a ternary counterexample, smallest dimension, complete classification, or one dimension uniform in q.

## Binding and reading scope

- Six-page public PDF `odd_power_sos_nonconvexity.pdf`, SHA256 `78930bbd8e727df2de0ca64ac3b5994a7e3392a289bd9058a4fc8dce02fd9e66`.
- Public verification ZIP, SHA256 `680fb649cc1288684611fd2767334c5c9d9b62f8be086441319539704551033c`.
- Both files and all 13 extracted members were independently checked against their immutable ZIP/receipt bytes. `evidence/source-binding.json` retains these and the seven primary-source PDF bindings.
- Read all six PDF pages and complete paper.tex, then visually inspected all six rendered pages. Read the two mathematical lemmas, Proposition 1, the complete moment table and cube identity, all submitted mathematical checker code, the portable verifier, README, CLAIM_SCOPE and source-version metadata. All compressed witness fractions were actually verified by replay, not accepted from positivity flags.
- No sibling review, dedicated historical verdict, or PRIORITY_NOTE was read. The manuscript and required support expose an accepted-scope heading, old priority-audit summaries and historical source-reading statuses. These incidental opinions are disclosed and were not evidence. Historical claims of having read sources are not treated as this review's reading record.
- The independent exact implementation was written and completed before reading the submitted certificate checker or expected output. No submitted helper is imported by it. The stored expected stdout is used only by the later published verifier replay.

## Reconstructed proof and domain checks

### 1. The objects and the two different exponent quantifiers

The ambient vector space consists of real homogeneous forms of a fixed positive even degree m. SOS means a finite sum of real polynomial squares, with no rational-function denominators, complex coefficients or quotient-ring equivalence. For odd q, SOS of f^q implies f >= 0 pointwise. Nonnegative scaling is automatic, including zero; calling the set a cone does not assume convexity.

The assertion is `for every fixed odd q, there exists a finite n(q)`, not `there exists n for all odd q`. The separating functional in Lemma 2 depends on q through d=qm/2. The order-nine table is used only for q=3. These quantifiers are explicit and consistent throughout the paper.

### 2. Finite-product positivity is valid at the required total degree

Let M index all local monomials of total degree <=d. Positivity on squares is exactly M positive semidefinite. Define L_s first on monomials with degree <=2d **in each block**. Multiplying the finitely many local moment values gives a well-defined linear functional on this finite-dimensional rectangular-degree space.

Every monomial in a polynomial H of global total degree <=d has local degree <=d in every block. Its moment matrix is therefore a principal submatrix of the finite tensor product M tensor ... tensor M. For any finite s this tensor product is positive semidefinite, and hence L_s(H^2)>=0. The enormous number of blocks is irrelevant to the algebraic implication; no infinite product, representing measure, numerical construction or limit of matrices is being assumed.

Every monomial in S_s^q has global degree qm=2d and local degree <=qm, so it lies in L_s's actual domain. Any SOS representation of a polynomial of total degree <=2d has factors of degree <=d: if a higher degree occurs, the sum of squares of the highest homogeneous parts is nonzero and cannot cancel over the real field. Thus L_s's positivity is enough to exclude **every** SOS representation when L_s(S_s^q)<0, not just homogeneous or prescribed-support candidates.

### 3. The partition expansion gives eventual negativity for each fixed odd q

Expand S_s^q by assigning q labelled occurrences to copies. The fibers of an assignment form a set partition pi, and distinct blocks inject into copies in `(s)_(|pi|)` ways. Unused copies contribute L(1)=1. Consequently the displayed partition formula has exactly the stated factors; no missing multinomial or block-order factor occurs.

The singleton partition is the only partition with q blocks. Its contribution has leading coefficient a1^q, negative when a1<0 and q is odd. Every collision partition has degree at most q-1 in s. Since q and the finitely many moments a_j are fixed, a real polynomial with this negative leading coefficient is negative for all sufficiently large real s and therefore for sufficiently large integers. This is a finite-existence argument; it does not exchange q with a limit in s or claim a uniform threshold.

The independent controls compare direct labelled assignments with partition counting for q=1,...,7 and four values of s each. They support the transcription; the all-q conclusion is the preceding proof, not extrapolation from those 28 examples.

### 4. Closedness and finite-dimensional separation are justified

For the SOS cone of degree <=2d, use the complete monomial vector v of degree <=d. The standard Gaussian matrix G=Gamma(vv^T) is positive definite: a nonzero polynomial has positive square integral against the full-support Gaussian density. If `v^T Q_j v` converges coefficientwise and Q_j is positive semidefinite, then Gamma of those polynomials is bounded. Since G >= lambda_min(G) I, this bounds trace(Q_j), and positive semidefiniteness bounds all matrix entries/norms. A convergent subsequence has a positive semidefinite limit representing the coefficient limit. The proof does not assume that arbitrary linear images of closed cones are closed; it supplies the needed coercive bound.

A non-SOS p is outside that finite-degree cone. Finite-dimensional strict separation gives L0 nonnegative on the cone and L0(p)<0. Here L0(1)>=0 because 1 is SOS. Adding sufficiently small epsilon times the Gaussian functional retains L(p)<0 and makes the moment matrix positive definite. Its constant value is strictly positive, so normalization to L(1)=1 is valid. This construction works separately at every d=qm/2 and does not require an extension of the explicit degree-18 functional.

The coefficient-continuous power map f -> f^q pulls back this closed cone to the stated fixed-power set. For odd q, the separate nonnegativity requirement is automatic. Hence nonconvexity does not contradict closedness.

### 5. The seed and its powers

For `p=x^4 y^2+x^2 y^4+z^6-x^2 y^2 z^2`, AM-GM on the three nonnegative terms gives p>=2*x^2*y^2*z^2>=0. This includes zeros and all real sign choices.

The exact degree-nine factors in Appendix A, with nine weights 3/2, six weights 1 and one weight 2, expand to p^3. The independent polynomial implementation verified equality coefficient by coefficient. The coefficient is **1**, not the coefficient-3 original Motzkin form; a control replacing it by 3 fails the displayed identity.

The explicit functional is positive on squares of factors up to degree nine and has L(p)=-1. If p were SOS, its square factors would have degree <=3 and its functional value would be nonnegative. Thus this independently certifies p is not SOS. BCJ's original Lemma 1 gives the same dehomogenized seed as an independent primary antecedent.

For each odd q>=3, `p^q = p^3 * (p^((q-3)/2))^2` is SOS. Applying Lemma 2 at that q and then Lemma 1 yields a finite number of disjoint copies whose qth power is not SOS. There is no claim that the explicit cube functional can evaluate p^5 or a higher power outside its degree domain.

### 6. The local rational certificate

The table specifies every moment of total degree <=18: odd-coordinate moments vanish, degrees 0/2/4 are specified, all ten even degree-six multi-indices are listed, and the remaining even total degrees use the displayed Gaussian scales. There is no undefined moment needed by the order-nine matrix.

Coordinate parity makes every cross-parity entry zero, leaving eight blocks whose total dimension is 220 and whose maximum size is 35. The independent reconstruction uses lexicographic monomial order from the manuscript, rebuilds each moment directly from the table, computes exact positive LDL pivots and checks exact matrix reconstruction. All 220 pivots are positive. The independently calculated twenty order-three leading minors match the displayed table.

The compressed Schur argument is also valid. In a fixed parity block, an older monomial has degree at most r-2 if the new monomials have degree r, so B uses only previously fixed even moments. G is a positive definite Gaussian Gram matrix on the distinct new monomials. With A positive definite, C=B^T A^-1 B is positive semidefinite. The matrix `G^-1/2 C G^-1/2` is positive semidefinite and its largest eigenvalue is bounded by its trace, which equals trace(G^-1 C). Therefore the strict bound below T_r implies `T_r G-C` positive definite. No commutativity or eigenvalue approximation is needed.

The published helper was then run and freshly authenticated all 24 exact traces and their inequalities, all twenty initial minors, and every full local LDL reconstruction. A separate copied fixture with one trace replaced by zero was rejected at `author_Schur_trace_authenticated`. Original source bytes were not changed.

### 7. Explicit finite dimension and the convexity witness

Independent exact expansion gives a1=-1, a2=11292*10^53 and a3=35039520*10^116. The cubic partition expression is

`N*a3 + 3*N*(N-1)*a2*a1 + N*(N-1)*(N-2)*a1^3`.

With a2>=1, it is at most `N*(a3-(N^2-1))`. At N=10^62, `35039520*10^116 < 10^124-1`, so the bound and actual expression are strictly negative using integer arithmetic. No floating-point exponent comparison or materialized tensor product is involved.

Each p_i belongs to the same n=3N variable ambient cone because its cube identity remains valid with unused variables. Their average is nonnegative but its cube is not SOS; positive scaling by N cannot change the existence of an SOS representation. A convex set is closed under every finite convex combination, so this N-term witness already proves nonconvexity. The least-failing-prefix observation correctly supplies an existential two-input violation without claiming a particular smaller prefix has an SOS cube.

If unused variables are added, an SOS representation of the lifted bad average would restrict to one in the original variables upon setting the new variables to zero. Thus the asserted persistence is valid.

## Boundaries and limits

- q=1 gives the usual convex SOS cone and is not a claimed counterexample case. In classical parameter ranges where nonnegative forms equal SOS, the obstruction seed cannot exist in that range.
- Oddness is indispensable to the negative-leading-coefficient mechanism. With even q, a1^q is positive; if one extended the definition while retaining f>=0, f^q would automatically be a square and the set would be the convex nonnegative cone.
- The coefficient-3 Motzkin form cannot replace the credited coefficient-1 seed in this proof. The cube identity negative control detects that substitution.
- The moment functional is truncated positive-on-squares, not a positive measure on real points. Its negative value on the nonnegative p proves that a representing positive measure would be impossible. No probabilistic law is used in the product construction.
- Closedness, fixed-exponent nonconvexity and convexity of the union over odd powers are compatible. The BKR union result increases the exponent when summing; it makes no same-exponent promise.
- No ternary result, least dimension, explicit n(q) for q>3, common dimension for all odd q, full classification, or stubbornness of the average follows from this review.

## Primary-source audit

All seven fresh primary PDF hashes match their acquisition receipt. Reading here is restricted to the actual relevant statements/proofs except BCJ, whose complete printed article was read visually. Historical package reading claims were not adopted.

1. **BCJ1979**, SHA256 `58b046f55459f561b63b5a3494d9cb116d4cc3bf076fb55182ee3802626363f9`: the entire printed pp.163–169 were read from the scanned images. Lemma 1, pp.164–165, is `x1^2*x2^2*(x1^2+x2^2-1)+1`, exactly p(x,y,1), nonnegative and non-SOS. Theorem 3, pp.166–167, proves closedness, including finite coefficient-degree sections; Theorem 4 applies Hahn–Banach separation to obtain positive-definite functions not representable as moments. The present paper gives its own finite Gaussian-Gram/separation proof, so it does not silently require a global moment representation or an unverified extension theorem.
2. **BKR published Forum of Mathematics, Sigma 14 (2026), e65**, SHA256 `f4058ac7b54e498c5b639eb21bf54973b421a9fc7b5ed301b1053e0e594078bb`: definitions and introductory fixed-power discussion checked, then Theorem 5.3/proof on pp.22–23, §6 fixed-power question on p.23 and the parameterized cube identity on p.24. Substitution a=1 gives the displayed Appendix A identity, including last coefficient 15-13=2. Theorem 5.3 changes exponents to k+k'-1, so its union convexity does not imply fixed-power convexity.
3. **Reznick OWR14/2023**, SHA256 `5a9bdc9f9daa12ef35185ceae208c0f2f75e191875827f78b7b6ad0f5cdbf240`: read the complete contribution printed pp.778–781, including bibliography continuation. The question on p.779 is general in n,m and the odd exponent. The coefficient-1 seed satisfies the recorded sufficient cube inequality c^3<=15/13. This review confirms the historical question formulation, not its present openness.
4. **Barak–Kelner–Steurer TR13-184**, SHA256 `e98ac494aca8f18f1085121239b523383ded08cf477ddf127be6dc714e1f202f`: Appendix A Lemma A.5 and proof state product pseudoexpectation positivity at a fixed level. The paper's direct principal-submatrix tensor argument proves the exact finite product version needed here, with matching degree restrictions. The full unrelated algorithmic body was not reviewed.
5. **Acevedo–Blekherman arXiv2303.11823v1**, SHA256 `2f75d05e957cc324688b71b5804c9502c0fa57058b26985a597f6dd6a8215565`: Lemma 2.1 and its proof (pp.5–6) distinguish distinct-index terms from collisions and establish the corresponding asymptotic product structure. This is credited precedent; the present finite partition identity is proved directly rather than imported as a stronger theorem.
6. **Blekherman–Riener arXiv1205.3102v4**, SHA256 `5c1e1c178abfb43bf0d75574bb1462177698285f40b761d0b7bafc5b6de02de6`: Proposition 6.4 and proof, p.22, establish the limiting basis transformation by its unique highest growth term. It is appropriately cited as asymptotic precedent, not as the new fixed-power conclusion.
7. **Stubborn Polynomials arXiv2602.01191v1**, SHA256 `c91b217bbe413cb934822be9c5f364c75739b38b7bdf178bbf2b764af6ecd0b9`: Theorem 2.2 and its proof concern non-stubborn quadratic forms on totally real projective varieties and again increase the exponent to k1+k2-1. The paper's credited comparison is accurate. No classification theorem from this source is needed in the present proof.

The ECCC primary report page was also checked online. The Cambridge DOI landing-page retrieval failed in the web tool; the complete fresh published PDF and its receipt were independently hash-verified and its relevant primary pages were read locally. No correctness inference rests on search snippets or publication status.

## Fresh checks and published replay

`evidence/fresh_certificate.py` is standalone standard-library exact arithmetic. It rebuilds the full table and 220-dimensional matrix, records all positive pivots, reconstructs each block, verifies the 16-square cube identity and three moments, checks the exact huge finite sign, and checks 28 direct-assignment/partition identities. Its four boundary controls reject the wrong seed, out-of-domain higher moments, a broken high-degree positive block, and the even-exponent sign inference. Full results are in `evidence/fresh-certificate.json`.

After those fresh checks, the original portable verifier passed with empty stderr and return code zero. It checked twelve manifest-listed files, 220 local pivots, twenty initial minors and twenty-four Schur traces, and matched its full deterministic expected output. `evidence/published-replay.json` and `evidence/tampered-witness-control.json` preserve the successful replay and negative fixture result.

These computations are exact certificate verifications, not a formal proof assistant. The general product, separation, degree and every-odd-q claims are justified analytically above; no finite sample count substitutes for them.

## Remaining gap and disposition

**No unresolved mathematical gap remains in the reviewed theorem.** No source repair was made. The historical priority notes and broader citation landscape were not reaudited; unavailable or unread articles mentioned in the manuscript's priority discussion are not hidden load-bearing proof inputs. This review supports the stated theorem and precise scope only. It does not certify worldwide firstness, current openness, acceptance by a journal, or human review.
