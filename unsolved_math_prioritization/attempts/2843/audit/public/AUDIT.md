# Independent audit: K3 Problem 3.45 / catalogue 2843

Audit date: 2026-10-08 (UTC).

## Verdict

**The mathematical partial report is accepted within its stated scope. Both problem parts remain unresolved after five distinct mathematical approaches. No new contact-topological theorem, genus-two example, or unbounded-support-genus family is certified.**

One reproducibility defect requires correction before claiming optimization-safe packet verification: the frozen scripts use `assert` for every substantive validation predicate. Those predicates disappear under Python optimization. A separately pinned correction replaces the 23 arithmetic assertions and 6 packet assertions with explicit checks. It leaves the mathematical report, saved arithmetic results, result classification, source metadata, and five-approach ledger byte-for-byte unchanged.

The original frozen packet remains untouched. Its manifest SHA-256 is:

`9e290bec9d6ba40ec3a61a1c41b9e70381f75c3ab80db6e2a4ef55f83d3aa751`

The corrected candidate's manifest SHA-256 is:

`daaf2d88de9272733ea1d674396ec2236cfe250d4796dc922e841890ff087b69`

`OPTIMIZATION_FIX.patch` is the actual code patch. `CORRECTION_NOTE.md` states its narrowly defined assurance and remaining trust boundary. Nothing was published, and no global queue was changed in this audit.

## 1. What was inspected

The complete nine-file original packet was read, including its report, scripts, manifest, results, metadata, and turn ledger. All eight manifest-listed file sizes and hashes matched. The externally supplied manifest pin also matched. The author's source-free packet does not contain a PDF, copied source document, dataset record, or private coordination material.

All ten locally available source PDFs matched the exact byte counts and SHA-256 values in the author's metadata. The catalogue-record and statement byte counts and hashes also matched without placing their contents in this audit. Those matches are recorded in `SOURCE_AUDIT.json`.

The actual K3 PDF's page 163 was checked in text and visually. It is also printed page 163. Problem 3.45 has precisely the two target questions reported, with unrestricted page genus and no bound on binding component count; the proposal/scribe attribution is J. Baldwin. The connected-sum suggestion belongs to the surrounding remarks, not to a third problem part.

The mathematical portions inspected in the cited PDFs were:

- EO08: open-book filling/group presentation, relative-arc relations, support invariants, and the plane-field normalization.
- M12: the Euler-number -1 circle-bundle candidate, its single positive boundary twist, and the fixed-Reeb limitation.
- E04: planar realization of overtwisted structures and its formal-homotopy consequence.
- GGP20: Theorem 1.7, its proof, Corollary 1.8, and the identification of Boothby-Wang structures with their supporting boundary-multitwist books.
- OSS05: the exact direction and universal U-divisibility quantifier in Theorem 1.2.
- K14: the U-depth discussion, grading conventions, and Remark 6.6's limitation.
- BMV17: Proposition 1 and the capping proof for genus one.
- BVM18: the introduction and Theorem A's distinction between infinitely many and arbitrarily large fillings.
- OS26: all mathematical statements, the polygonal construction and its figures, the general-genus reduction, and the contact connected-sum import.

The audit re-opened the public arXiv records for OS26, K14, and BVM18. The OS26 record still lists only v1, submitted 2026-07-22, with no journal reference displayed. E89's DOI did not load in the audit's web fetch. The overtwisted-realization theorem is therefore accepted as a standard imported theorem corroborated by E04 and the original Ozsvath-Szabo contact-invariant paper; this audit does not claim independent full-text inspection of E89.

No bounded source search proves that a problem is globally open. The defensible assertion is that this packet does not solve either part and the checked current primary literature does not supply a verified resolution.

## 2. Definitions, contact identity, and quantifiers

The report works with positive cooriented contact structures on closed, connected, oriented three-manifolds and connected pages with nonempty boundary. This is the correct domain for the stated support-genus question. Support genus minimizes over all supporting books of the specified contact structure, allowing arbitrarily many binding components.

The report correctly separates:

1. the topology of the underlying three-manifold from the supported contact structure;
2. genus minimized among connected-binding books from unrestricted support genus;
3. support norm from support genus;
4. one fixed circle-action Reeb field from all contact forms defining the same contact structure;
5. a formal oriented plane field from its particular contact realization;
6. arithmetic in an abstract U-module from the actual Floer module and contact class;
7. all positive factorizations of one monodromy from all Stein fillings of the contact boundary.

None of the five approaches silently replaces one of these quantifiers by another. The examples and calculations are accordingly useful partial analysis rather than a solution certificate.

## 3. Approach I: boundary twists and rank

### 3.1 Group and homology

For a once-bordered genus-g page, a boundary twist acts on the based free group by inner conjugation by the oriented boundary word or its inverse. The distinction only changes the sign of the power. Filling the binding kills the mapping-torus direction. It does not kill the page-boundary longitude. Thus the stated relations forcing the nth power of the boundary word to commute with each free generator are correct.

Abelianization kills every commutator and produces no additional linear relation. Consequently the group abelianization is exactly free of rank 2g, for every g,n >= 1. The exponent n need not equal one for this conclusion. This does not identify all n as the same circle bundle, and the report correctly restricts the later Euler-number -1 identification to n=1.

For a page of type (h,b), its free fundamental group has rank 2h+b-1. After one binding meridian kills the mapping-torus generator, further solid-torus fillings impose relations without adding generators. Therefore b1(Y) <= 2h+b-1, including in the multi-boundary case. The equivalent Heegaard-splitting argument has the same rank.

### 3.2 Consequences

For b=1, the inequality forces h >= g. The exhibited supporting book attains g. The minimum among supporting connected-binding books is therefore exactly g. Likewise every supporting page has -chi >= 2g-1, and the exhibited page attains equality. This proves the exact support norm claimed, independently of the unknown unrestricted support genus.

A genus-one page with b=2g-1 satisfies the same rank and Euler-characteristic constraints. For g>=2 it is a genuine alternative numerical type, not a page whose existence has been established. A planar numerical alternative requires b>=2g+1. Large first Betti number, norm, or group rank therefore does not force large support genus.

The annulus control is important and correct: an n-fold core twist acts trivially on absolute H1, but the relative arc between the boundary components supplies the relation n times the core equals zero. For nonzero n the filled H1 is Z/n, not Z. EO08 explicitly includes these relative arcs. The frozen script labels this fact as a control but hard-codes its two ranks; the proof and source, not that literal JSON value, justify it.

Attaching an oriented stabilizing 1-handle to the same boundary component changes (h,b) to (h,b+1), and the positive Dehn twist preserves the contact structure. Thus the number of boundary components of all supporting books is not bounded by this argument. The distinction from the minimum binding number at minimum genus is maintained.

**Verdict:** Proposition 2.1 and its limitations are correct. No correction to the mathematical text is required.

## 4. Approach II: horizontal pages and conformal Reeb change

The circle-bundle model has Euler number -1 with the convention for which the supporting once-bordered book has a right-handed boundary twist. M12 and GGP20 agree on the relevant contact identification, not merely on a diffeomorphism type.

Under the explicitly stated covering hypothesis, truncating neighborhoods of b distinct binding fibers gives an unbranched finite cover of a genus-g base with b boundary components. The page also has b boundary components because the book is ordinary and those are exactly its bindings. Therefore its Euler characteristic is multiplied by degree d. Solving the identity gives

h-g = (d-1)(g-1+b/2),

which is nonnegative for g,b,d >= 1. The assertion is conditional on the actual covering and ordinary-book hypotheses. Integrality, boundary degrees, bundle Euler number, and realizability can further restrict (g,b,d); the report does not claim sufficiency of its numerical identities. In particular, no nonexistent covering is needed for its lower bound.

For beta=f alpha with f>0, write R_beta=R_alpha/f+Z with Z in xi. On v in xi,

d beta(R_beta,v)=f d alpha(Z,v)-df(v)/f.

The required equation is therefore d alpha(Z,v)=df(v)/f^2, with the positive sign stated in the report. It also implies df(Z)=0 by evaluating on Z, so the remaining Reeb condition is compatible. Taking f=2 locally and df|xi=dx in a chart with d alpha|xi=dx wedge dy gives Z=-partial_y/4, an explicit nonzero horizontal component. This is a real obstruction to identifying all adapted Reeb fields with the original fiber direction.

**Verdict:** Proposition 3.1 and the Reeb calculation are correct with their displayed hypotheses. They do not constrain arbitrary supporting books without an additional horizontalization theorem.

## 5. Approach III: the first Chern class, d3, and nonplanarity

The horizontal contact plane bundle is isomorphic, as an oriented real two-plane bundle, to the pullback of the base tangent bundle. Since the circle Euler class is a generator of H2(base;Z), the Gysin map from H0 onto H2 is surjective and the subsequent pullback is zero. Hence c1(xi_g)=0 integrally, not merely rationally.

The disk bundle of degree -1 has the Boothby-Wang contact structure on its convex boundary. Its symplectic zero section can be chosen J-holomorphic while J is adapted near the boundary. On that section, c1(TX)=c1(TSigma_g)+c1(normal)=2-2g-1=1-2g. The intersection form on H2 is [-1], so the rational square is -(1-2g)^2. Boundary c1 is zero, satisfying the torsion requirement for the rational square and the d3 invariant.

The remaining characteristic numbers are chi=2-2g and signature=-1. In the convention d3(standard S3)=-1/2, substitution yields exactly

d3(xi_g)=-g^2+2g-1/2.

Useful sign controls are g=0: -1/2; g=1: +1/2; g=2: -1/2; g=3: -7/2. The g=0 disk bundle is the negative blow-up filling of the standard boundary, so the normalization check is consistent. Changing to a convention that shifts d3 by 1/2 without changing the grading formula would be an error; the report does not do so.

The filling used here is symplectic, with a closed symplectic zero section. It is not being declared Stein or exact. GGP20's Theorem 1.7 applies to a symplectic filling containing a closed positive-genus symplectic surface and does not require a positive self-intersection. Its Corollary 1.8 directly includes the Boothby-Wang circle bundles. Thus sg(xi_g)>=1 for g>=1; the original book supplies the upper bound g. Equality sg(xi_1)=1 is justified. Nothing in this argument upgrades the lower bound for g>=2.

The formal-plane-field argument is also logically sound. On a fixed oriented manifold, every oriented plane-field homotopy class has an overtwisted representative, and every such contact structure is planar. Any lower-bound function depending only on that class and valid for all its contact realizations must therefore be at most zero there. This rules out a positive universal bound from c1 and d3 alone. It does not rule out stronger bounds using additional tightness, fillability, or geometric information.

**Verdict:** All signs, filling hypotheses, and conclusions in Proposition 4.1 and the nonplanarity discussion are correct.

## 6. Approach IV: Floer depth and grading

OSS05's planar implication has the direction stated: for every nonnegative d, c+ lies in the image of U^d. Its contrapositive obstructs genus zero. It neither bounds higher support genus nor states that a larger finite depth forces larger genus.

In the tower-plus-truncated-polynomial diagnostic, U kills the nonzero distinguished finite-summand class U^m. The images in that summand contain it exactly for d<=m. The tower's second coordinate remains zero, so no tower element can supply a missing finite coordinate. Conversely, the tower class of 1 has a preimage U^(-d) for every d. These facts hold over any field; the bit-support implementation is only a finite regression for the same monomial argument.

The correct grading with the report's convention is -d3-1/2=g^2-2g. This grading formula requires torsion c1, not a rational-homology-sphere hypothesis. The candidates have b1=2g, so importing a one-tower-plus-reduced decomposition merely from rational-homology-sphere results would be unjustified. The report avoids this: its module is explicitly an algebraic diagnostic, and it does not identify HF+(-Y_g) or locate the actual contact element.

For this point the audit additionally checked the original Ozsvath-Szabo Proposition 4.6 and the convention stated in Ghiggini's Proposition 3.3, which uses precisely the torsion-c1 hypothesis. Public references:

- [Ozsvath-Szabo, Heegaard Floer homologies and contact structures](https://arxiv.org/pdf/math/0210127), Proposition 4.6.
- [Ghiggini, Strongly fillable contact 3-manifolds without Stein fillings](https://arxiv.org/pdf/math/0506380), Proposition 3.3.

K14's computations and its explicit warning about detecting support genus above one are accurately characterized. A homological calculation in a constrained plumbing class does not provide the missing statement for every genus-one book with arbitrary binding count.

**Verdict:** The algebra, grading, source use, and stated gap are correct. No realization theorem or actual candidate U-depth has been proved.

## 7. Approach V: weighted capping and fillings

Capping all but one labeled boundary defines the indicated homomorphism to the once-bordered torus mapping class group. Its abelianization sends every positive nonseparating twist to 1 and the positive boundary twist to 12, consistent with the two-chain relation.

On a genus-one surface, every separating curve has a uniquely determined planar side. For a homologically nonzero separating curve, that side contains a nonempty proper subset A of boundary components. Empty A bounds a disk; full A represents the sum of all boundary classes and is homologically zero. Both are excluded by allowability. A boundary-parallel curve around a single component is allowable when b>=2, but not when b=1; the report accounts for this edge case.

A nonseparating curve remains nonseparating after capping. A separating factor of type A contributes 12 exactly in the cappings indexed by A and contributes zero otherwise. Additivity proves each coordinate constraint and the weighted sum identity. Since an allowable factor contributes at least min(b,12) to E, the coarse length bound follows.

The sharper bound uses sum |A|s_A >= sum s_A. Thus the actual length is at most N+(E-bN)/12. The actual N belongs to the stated finite congruence set, so maximizing over that set is a valid upper bound. The optimization is not a sufficiency criterion for a mapping-class factorization. Its behavior at b=12 is benign: the coefficient of N vanishes. For b>12 its maximum is at the smaller admissible N, rather than the larger one. The additional audit checks explicitly include this untested branch of the original finite regression.

For a multitwist with one positive twist per boundary and b>=2, the coordinates are all 12. The two possibilities N=0 and N=12 are the only nonnegative integers in the permissible interval with the common residue. At N=0, every label must be covered exactly once by the planar-side types, so those types form a partition. This is a necessary combinatorial pattern; it does not certify every partition as an actual ordered factorization.

For a positive allowable Lefschetz fibration with genus-one b-bordered fiber, the handle counts are one 0-handle, b+1 1-handles, and ell 2-handles. Hence chi=ell-b and b2<=ell. The conclusion bounds fillings presented with exactly the fixed boundary open book. The report does not invoke the planar filling theorem at genus one. A Stein filling's existence of some allowable Lefschetz fibration does not preserve a previously chosen genus-minimizing boundary book.

BMV17 already proves the low-genus bounded-length mechanism. BVM18 explicitly separates the corresponding fixed-open-book statement from a bound on all Stein fillings and provides genus-one examples with infinitely many fillings of bounded size. The report correctly labels these as known inputs and retains the missing uniform-filling premise.

**Verdict:** Proposition 6.1 and Corollary 6.2 are correct, including allowability, boundary-parallel factors, signs, and quantifier restrictions.

## 8. July 2026 connected-sum correction

OS26 is a preprint import, not a theorem established by this packet's arithmetic. Its Theorem 1.1 applies to closed, connected, cooriented contact three-manifolds and gives a maximum, rather than sum, upper bound for support genus under contact connected sum.

The inspected proof constructs a polygonal Murasugi sum whose surface genus is the maximum of the input genera, then uses Torisu's contact connected-sum identification. In the equal-genus-one illustration, chi=-3 and three boundary components give genus one. For equal genus g, the pictured construction gives genus g and 2g+1 boundary components; its Euler characteristic is 1-4g, agreeing with the Euler-characteristic sum of the two once-bordered pages minus one disk. The reduction by boundary sums for unequal genera and extra boundary components preserves the claimed maximum. The companion lower bound for the genus of any such surface sum is consistent with the embedded symplectic intersection pairing of either summand.

This supports the report's use of the preprint's theorem with its manuscript qualification. The audit is not a formal verification of Torisu's theorem or every external dependency. In particular, it does not change the preprint to a published result or upgrade the imported upper bound to equality for arbitrary contact structures.

The corollary for iterated sums follows by induction and rules out the old connected-sum strategy using only genus-one summands. It proves neither requested existence nor unboundedness. Public current record: [arXiv:2607.19892](https://arxiv.org/abs/2607.19892).

## 9. Reproducibility and negative controls

`EXECUTION_AUDIT.json` records 150 subprocess runs on Python 3.12.14. Each executed script reports UID=EUID=1000 and its actual optimization flag before execution. Every packet copy had directories mode 0555 and files mode 0444. Attempts to open an existing packet file for writing and to create a new packet file both raised PermissionError. Content/size/mode snapshots remained identical after each execution. The supplied original and corrected packets remained unchanged throughout.

The modes were ordinary Python, command-line -O, command-line -OO, and separate inherited PYTHONOPTIMIZE=1 and =2 runs. The latter matter because the original packet verifier launches its arithmetic child without forwarding command-line optimization flags; an environment setting does reach that child.

All original baseline results reproduce, including the saved arithmetic JSON, but this does not make the original verifier robust. Negative controls include an unlisted file, a same-length report alteration, truncation, wrong byte count, wrong hash, a self-rehashed changed check count, a self-rehashed false no-solution flag, a self-rehashed NaN result, and wrong signs in the Reeb and Chern-square calculations. The arithmetic mutants are also run directly, so hash checking cannot hide an inactive mathematical predicate.

The original produces **44 optimized false-PASS results** for these invalid integrity/arithmetic cases. The corrected candidate rejects every one of those case/mode combinations, and rejects all of the non-type-equivalence negative controls in every mode. Both scripts still pass on the unmodified packet in every mode.

A separate exact-type characterization is deliberately retained: changing a saved JSON true to integer 1 and rehashing its manifest is accepted by Python object equality in both original and corrected versions. There are five such recorded acceptances per version, one per mode. This is outside the narrow optimization correction, and no strict JSON-schema or adversarial-manifest claim is made. A separately supplied correct manifest pin rejects the changed manifest bytes before packet testing. NaN is parsed permissively by the standard decoder but is rejected by the corrected saved-result comparison in the tested case; this must not be advertised as a strict nonfinite-number parser.

The independent supplemental script uses explicit checks and different arithmetic representations. It adds 20,800 abelianized commutator-vector cases; 64 finite page-type minimizations; 20,250 integral horizontal-cover identities; 867 full conformal-Reeb checks; 101 disk-bundle characteristic calculations; 943 finite-module image iterations; and 231 capping examples including b=11,12,13,20,51,100. Its finite examples are regression diagnostics, not proofs of realizability or the original open problem. The authored mathematical analysis above supplies the universal arguments.

## 10. Acceptance scope and remaining work

The source identity, mathematical partial conclusions, honest five-approach classification, and unresolved status are accepted. The corrected candidate is accepted as an optimization-safe implementation of the original predicates, with external manifest pinning and the parser/authenticity limitations above. The uncorrected verifier must not be described as optimization-safe.

No additional mathematical approach is counted for literature retrieval, this audit, regression tests, or the correction. No proof or source text was changed to turn partial work into a solution. The remaining substantive target is still an obstruction applying to all genus-one supporting books with unbounded binding count, or another valid mechanism answering one of the original questions.
