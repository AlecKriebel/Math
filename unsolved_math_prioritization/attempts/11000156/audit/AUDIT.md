# Independent mathematical and distribution audit

Problem 11000156 / AMR-109-0156, rank 1013. Audit date: 2026-10-08.

## Verdict

Accept the mathematical analysis as a scope-sensitive **unsolved, 5/5** result for the literal commutation-only, individual-Dehn-twist operation. Credit Baykur's published negative theorem for the untwisted operation. Do not label the broader question solved, do not claim that the broader question is globally open, and do not advertise the finite checks as formal certification.

The only correction found is bibliographic: the cited two-chain relation on PDF page 132 of the Farb volume is in **Wajnryb's chapter**, rather than Auroux's. An actual unified patch and a separately frozen corrected distribution are supplied. The mathematical text, five-turn status, proof checker, and verifier otherwise remain unchanged. The original packet and archive were preserved byte for byte.

The report below audits the mathematical arguments and their source scope, independently of whether the supplied scripts pass. The deep geometric results used as prior theorems are source-reviewed, not reproved or machine-certified here.

## 1. Target, conventions, and quantifiers

The recovered target uses a compact oriented genus-g surface with n boundary circles, with its mapping class group fixing the boundary pointwise. Its distinguished element is the product of the positive twists around **all** boundary circles. Thus n counts boundary components and marked square-minus-one sections, rather than punctures; for n greater than one, the target is a multitwist. The two factorizations have the same fixed g and n and only nonseparating positive factors. The surrounding correspondence requires 2-2g-n < 0; the pencil interpretation has n at least one. No genus-at-least-three restriction is present in the question. The relevant source locations are Auroux's chapter, PDF pages 139 and 144-145, especially Question 2.5 on displayed page 138. [Farb volume](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf).

The Euler calculation is internally correct: a genus-g fibration over a sphere with r Lefschetz singularities has Euler characteristic 4-4g+r. Therefore matching Euler characteristic, at fixed genus, forces equal factorization lengths. Matching signature remains an additional condition in general. Equality of these numbers does not itself identify fibrations or factorizations.

Let B=(x_k,...,x_l) have product P. The printed algebraic operation sends each x_i in B to t_a x_i t_a^-1, subject to [P,t_a]=1. This gives the same total product because the new block product is t_a P t_a^-1=P. Conjugation by an orientation-preserving mapping class preserves positivity and whether a curve is nonseparating. The inverse move uses t_a^-1, so allowing inverse moves is appropriate for the equivalence relation. The report's right Hurwitz move (x,y) -> (y,y^-1 x y) preserves the ordered product xy exactly.

Three different questions must be distinguished:

- U: the block preserves the conjugating curve with its orientation.
- T: the block merely commutes with its Dehn twist.
- C: the block can be conjugated by an arbitrary centralizing mapping class.

The report uses T for the literal operation and does not silently substitute C. For an essential curve, conjugation gives P t_a P^-1=t_{P(a)}. A positive twist does not depend on an orientation chosen on its curve. Consequently P can preserve the surface orientation and nevertheless reverse the orientation of a while commuting with t_a. This is precisely the distinction relevant here. Statements about inclusions of move sets do not prove strict inclusions of the resulting orbit relations.

Global conjugation is available. Every boundary twist is central in the boundary-pointwise group, so the full block P=Delta is admissible for every individual twist. The allowed indices include k=1 and l=r. Express an arbitrary mapping class as a product of twists and their inverses, and apply the corresponding whole-word moves successively. For U as well, boundary twists can be represented away from an interior curve and preserve its orientation. This argument does not assert that twists individually centralizing an arbitrary *proper* block generate that block's full centralizer.

## 2. Prior theorem and source scope

Baykur's v3 Theorem B provides, for given N,n >= 1 and sufficiently large genus, N nonseparating positive factorizations of the same boundary multitwist with equal Euler characteristic and signature, inequivalent under Hurwitz moves and **untwisted** partial conjugations. Taking N=2 supplies a prior negative answer for U. The abstract's shorter wording must be read with this exact theorem. Remark 4.1 explicitly withholds the extension to orientation-reversing blocks; Remark 4.2 distinguishes arbitrary centralizers from commuting individual twists. The report credits the theorem and does not extend its quantifiers to a smallest genus or all genera above a stated threshold. [Baykur, arXiv:1408.4869v3](https://arxiv.org/pdf/1408.4869v3).

The exceptional-sphere obstruction is tied to surgery disjointness. If the conjugating curve reverses under P, its suspension is a Klein bottle, and the corresponding isotopy-away statement is not supplied by the torus theorem. A proof of preservation for torus surgeries cannot simply be reused for that move. The report is therefore right to retain a genuine gap rather than deduce a negative T-result from a negative U-result.

The rational/ruled continuation distinguishes examples using differing numbers of reducible fibers. Such examples do not meet the requirement that both factorizations have exclusively nonseparating vanishing cycles. This rules out that particular shortcut, rather than proving no future rational/ruled construction could help. [Baykur, arXiv:1806.00375, introduction and Theorem 1](https://arxiv.org/pdf/1806.00375).

A supplementary current-source check examined Lee and Servan's author-hosted manuscript, *Infinitely many Lefschetz pencils on ruled surfaces*. Its families are produced using partial conjugation; its discussion does not supply a negative answer to the present T-question, and its general-centralizer formulation must not be conflated with T. This is a useful cross-check, not an exhaustive literature census. [Author manuscript, Sections 1.1 and 1.4](https://math.uchicago.edu/~cservan/lefschetz_ruled.pdf).

## 3. Turn 1: exceptional intersections and doubling

The proposed extension is conditional in the right place. If suitable exceptional representatives on both sides of a surgery can be kept disjoint from the surgery region, their intersections with an unaffected fiber survive. The required preservation statement, including the reverse surgery, is what could make the obstruction useful. The report does not claim to have proved this for Klein bottles.

The mod-two warning is valid: a nonzero mod-two intersection between a sphere class and a closed embedded Klein bottle prevents disjoint representatives. Conversely, zero intersection alone would not prove that disjoint representatives exist. Passing to an orientable double cover is insufficient without an equivariant construction that descends. Thus parity or a cover does not by itself repair the missing geometric theorem. No concrete mod-two obstruction for every prospective counterexample is claimed.

The arithmetic was checked independently using a sparse degree dictionary, rather than the author's list-update implementation. Starting from exceptional data (m), the sequence

    k1=m-j, k2=m+3j, k3=m-2j

has successive final data

    (4m-8j, 0, 3m+14j, 3m-7j, j).

The accumulated blowups before blowing up the final base points are

    j + (3m-7j) + (3m+14j) = 6m+8j.

Adding the remaining 4m-8j base points gives 10m, independent of j. The genus recurrence gives

    g3 = 8g0 + 4k1+2k2+k3-7 = 8g0+7m-7.

Both cancellations reflect the kernel direction (-1,3,-2), perpendicular to (1,1,1) and (4,2,1). The final exceptional-data coordinate j varies. These computations support the numerical mechanism, but their input tuples are not automatically geometric pencils.

Independent enumeration checked 1,105 admissible sequences with 1 <= m <= 70. The author's smaller range checks 214 sequences and agrees. A source detail worth retaining: arXiv v3's displayed genus equation in Lemma 3.1 has g and g-prime reversed; the later iterated formula and the genus calculation used in this packet have the correct direction g_new=2g_old+k-1. This source misprint was not imported into the code.

**Disposition:** substantive failed extension with an explicit geometric gap; no theorem proved for T.

## 4. Turn 2: the positive torus block and centralizers

This is an actual boundary-factorization scope witness, not merely a quotient example. Let a and b be positive twists about curves meeting once on a one-holed torus. They obey aba=bab. Put d=aba. The braid relation implies d a d^-1=b and d b d^-1=a, so z=d^2=(ab)^3 commutes with both generators. The two-chain relation gives

    z^2=(ab)^6=Delta.

It follows that z is a consecutive six-factor positive block of a twelve-factor positive boundary-twist factorization. The two-chain relation is the genus-one specialization of Wajnryb's relation (3), PDF p.132, displayed p.125, in the Farb volume. This is the citation corrected in the supplied patch. [Wajnryb chapter in the Farb volume](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf).

With the column-vector convention used in the packet,

    A=((1,1),(0,1)), B=((1,0),(-1,1)), (AB)^3=-I.

The underlying unoriented slope of a is preserved, while its oriented primitive homology class changes sign. The mapping class z preserves the orientation of the *surface*: -I has determinant +1. It is not an orientation-reversing surface homeomorphism. Nor is z an involution in the boundary-fixed mapping class group: z^2 is the nontrivial boundary twist. Homology alone sees that boundary twist as the identity, so the geometric relation cannot be inferred solely from the matrix equality. The report properly uses the two-chain relation separately.

There is also a direct reason this example gives no inequivalent pair. For any six-factor word W=(a,x2,...,x6) of central product z, five inverse Hurwitz moves move a to the right and produce

    (a x2 a^-1,...,a x6 a^-1,a).

Now apply five inverse Hurwitz moves in reverse index order to bring the last factor to the front. The preceding five factors are left in their current order. Their product Q satisfies Q a=z, hence Q commutes with a and the new first factor Q a Q^-1 is a. The result is exactly the global a-conjugate of W. Thus ten Hurwitz moves within the block perform the proposed T-move, leaving the rest of Delta untouched. The independent checker verifies all eleven matrix-image states; the preceding central-product argument establishes the group-theoretic statement without relying on matrix faithfulness. It is also consistent with Auroux's central-factorization Lemma 6. [Auroux, stable classification, Lemma 6](https://arxiv.org/pdf/math/0412120v2).

For the second attempted reduction, solve MA=AM with M=((p,q),(r,s)) and determinant one. Entry comparison gives r=0 and p=s; the determinant forces p=s=+1 or -1. Therefore the centralizer is {+/- A^k}. Every twist on the one-holed torus commuting with a is along a curve disjoint from a, and its homology image is a power of A (the boundary twist contributes the identity). Products of those images cannot equal -I. Thus the proposed fixed-centralizer generation shortcut fails. It does not rule out a more elaborate sequence using different blocks, and the report does not claim that it does.

**Disposition:** both reductions are genuinely blocked; no strict orbit separation or main counterexample is proved.

## 5. Turn 3: stabilization is not cancellation

Auroux's Theorem 2 concerns equal-genus fibrations equipped with one distinguished section; it assumes matching Euler characteristic, signature, section square, and reducible-fiber counts by type. It gives an isomorphism after sufficiently many copies of a universal fiber sum. The statement is for every genus, with genus zero and one separately noted as requiring no stabilization. The proof's general construction works in Map(g,1). [Auroux, Theorem 2 and Section 5](https://arxiv.org/pdf/math/0412120v2).

Consequently the report may apply that theorem after retaining one chosen section. It may not infer that an isomorphism simultaneously preserves every extra marked section when n>1. Capping the other boundaries forgets data; it does not give an injective comparison of the original marked factorizations.

Even for n=1 and higher genus, stabilization changes the positive word. In Auroux's genus-at-least-three construction the universal word has product delta^4, so appending k copies changes the product from delta to delta^(1+4k), the section square, and the number of factors. No allowed unstabilized move deletes those copies. Group cancellation is irrelevant: F and G already have the same group product. What is needed is cancellation at the level of factorization orbits. An equality of stabilized Hurwitz orbits, and therefore of stabilized T-orbits, does not establish injectivity of the stabilization map.

The union-monoid example is a correct logical illustration of this failure of inference. It is not evidence that cancellation actually fails for the precise Lefschetz-factorization quotient. The report labels it appropriately. Its universal remaining gap is compatible with some low-genus special cases already having unstabilized classifications.

**Disposition:** correct identification of two independent gaps, orbit cancellation and retained section marking.

## 6. Turn 4: quadratic refinements

Let q be a refinement of a symplectic form omega over F2, and let c=omega(x,a). Since c is zero or one,

    q(x+c a)=q(x)+c q(a)+c omega(x,a)
               =q(x)+omega(x,a)(q(a)+1).

For nonzero a, nondegeneracy supplies an x with omega(x,a)=1, so the associated transvection preserves q if and only if q(a)=1. The exception a=0 is harmless and is not omitted from the packet's stated qualification.

The ten-factor finite example is correct. The first two transvections have vector f1; the remaining eight are the four basis transvections, each repeated twice. Every paired block has identity product. Values q=1 on the basis determine the sole refinement

    q=x1*y1+x2*y2+x1+y1+x2+y2.

For a=e1+e2, q(a)=0, and the first pair's vector becomes f1+e1+e2, where that q is zero. The unchanged basis pairs still force the same refinement, so the transformed word admits none. Both full products and the selected block product were independently multiplied as 4-by-4 matrices over F2, in addition to checking all 4,096 transformation identities.

This proves failure of a proposed invariant on the stated *finite quotient move system*. It does not disprove every analogous invariant on genuinely liftable boundary factorizations. A finite-field square of a transvection is the identity, while a positive Dehn-twist square in the mapping class group need not commute with the prospective conjugator. No lift, boundary-product identity, or signature match is supplied by this finite example. The report explicitly retains these limitations.

**Disposition:** valid rejection of the unrestricted finite-quotient argument, without a geometric counterexample.

## 7. Turn 5: finite orbits

An independent implementation used 2-by-2 matrices over F2 and undirected union-find, rather than the author's S3 permutations and depth-first traversal. It enumerated all 729 words in three nonzero transvections of length six and found exactly 243 with identity product.

Hurwitz edges give components of sizes 1,1,1,240. Admissible partial-conjugation edges merge all 243 vertices. The independent pass checked 1,215 Hurwitz edge occurrences and 5,589 partial edge occurrences. The author's count 2,430 for Hurwitz occurrences is consistent: that routine enumerates them once for each of its two component passes. It is not a claim that 2,430 different graph edges exist.

The subgroup-change mechanism is sound. From six equal transpositions s, conjugate the first identity-product pair by a distinct transposition t. Its new transposition u=tst differs from s. The subgroup generated by the word changes from <s>, of order two, to <s,u>, of order six. This invalidates generated-subgroup order for that finite system. Again, the paired-product identity need not lift to an admissible mapping-class move.

**Disposition:** an accurately bounded quotient computation. Finite-image connectivity neither proves geometric connectivity nor settles the signature constraint.

## 8. Distribution and adversarial verification

The submitted original archive was independently pinned before extraction:

- Size: 13,801 bytes.
- SHA-256: 3f8104fcf841db20f90769427c0a218971bf5a542c5d24a9747a5c931f28da06.
- External manifest SHA-256: 913c3e9341eb863e7906d234707bf92188bd78f7af8a4833d1ee47b859c8a077.
- Bootstrap SHA-256: dcc50e895d0373014bc9098742b4c20bb090753958b1bc338c244f32003c03b1.

The archive contains the six intended packet files, three external integrity files, and an acceptance receipt. Membership and file types were checked before materializing it. Neither PDFs nor extracted source text, images, corpus records, nor private coordination files are present.

Both the original archive-extracted distribution and the corrected distribution passed the bootstrap in ordinary Python, -O, and -OO. All runs used actual uid 1000. Packet and distribution directories were mode 0555 and files 0444. Attempts to append to REPORT.md or the external manifest and attempts to create files inside the packet or distribution were denied by the filesystem. Snapshots before and after replay matched. These are real permission denials, not mocked writes or assertions about mode bits alone.

Thirty-one malformed cases were tested in each of three interpreter modes against each distribution, yielding **186 rejections**. Cases cover changed/missing/extra files, symlinks, a FIFO, directory substitution, oversized content, verifier substitution, rehashed tampering against the original external pin, malformed/duplicate JSON, wrong schemas and types, unsafe paths, invalid sizes and digests, duplicate status keys, and false resolved/certification status. Deliberately repinned tests exercise parser/schema checks; they are distinguished in the receipt from tests of the original trust anchor. No assertion statement is needed for a validation failure, so optimization does not disable these checks.

Independent mathematical code also passed in all three modes. Its expanded integer centralizer sample comprises 692 matrices; it checks a ten-step Hurwitz image path, 1,105 doubling sequences, all 4,096 quadratic identities, and the complete stated finite orbit graph.

These tests establish reproducibility for these frozen files and finite statements. They do not authenticate the external pins, make Python a security sandbox, prove arbitrary mapping-class identities from homology, establish geometric realizability, or verify Seiberg-Witten theory. A caller must trust the externally retained bootstrap and manifest pins before running packet code. Simultaneously replacing all files and all purported trust anchors is outside the claimed integrity model.

## 9. Correction and recommended disposition

The citation patch changes only REPORT.md and SOURCES.json, adding Wajnryb attribution and the exact page/relationship. The corrected external manifest and bootstrap are regenerated; the original proof_checks.py, verify.py, README.md and STATUS.json are unchanged. No mathematical status is upgraded.

Recommended queue cells remain the supplied values:

- Status: unsolved.
- Turns: 5/5.
- Findings: Baykur's prior negative result is credited for untwisted moves; the commutation-only question remains unresolved in this work, with the orientation-reversing/Klein-bottle gap explicit.

The required next mathematical advance is either a genuine pair and an obstruction valid for every T-move, or a fixed-length T-connectivity theorem. None of the five attempts supplies it. This audit accepts an honest partial result, not a solution claim.

## 10. Public-source inspection record

The Farb volume, Baykur v3, and Auroux stable-classification PDFs match the sizes and SHA-256 digests recorded in the packet's SOURCES.json. Relevant paragraphs, formulas, theorem qualifications and remarks were read; the question page, Baykur's remarks page, the stable-theorem pages and Wajnryb's relation page were visually inspected. Web screenshot fetching failed, so retained primary PDF bytes were used for local visual inspection. Those source images are excluded from this deliverable.

Public arXiv records confirm Baykur v3's 2015-10-14 revision and Auroux stable classification v2's 2005-01-21 revision. The publisher PDF route returned HTTP 403, so no additional publisher-byte verification is claimed. The rational/ruled continuation and the Lee-Servan manuscript were inspected through public PDF text. The bounded additional search did not produce a theorem resolving the broader T-scope; this is not proof of a global literature absence.
