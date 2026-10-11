# Independent audit: pointwise signature approximation reductions

This AI-assisted manuscript is unrefereed. Acceptance refers to an internal AI mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification. This is not a computational reproduction package. No novelty or priority claim is made, and no exhaustive current-openness claim is made.

## Disposition

PASS for the stated elementary reduction, rational modulo-4 eventual sequence, and torus-family eventual sequence, with the explicitly imported mathematical dependencies below. No proof defect was found that changes these partial conclusions. The original all-knots full-signature problem is unresolved by this packet and by this audit. This is not a full-problem acceptance, an all-degree separation computation, a novelty certificate, or an exhaustive current-literature search.

The complete authored mathematical report and source-scope report were byte-authenticated within the closed 41-member creator evidence inventory before mathematical reliance. All listed member hashes and byte counts and exact file-tree closure passed independently at initial reliance and in subsequent verifier runs. The independent audit has a separately authenticated closed 19-member inventory. VERIFICATION.json records the original inventory and external-seal identities; the scholarly-source ledger is a distinct authenticated record.

The audit recommended a nonblocking clarification: explicitly take p,q coprime, handle every unknot representation before dividing by v2, and state torus invertibility so the classification also suffices for oriented knots. PROOF.md includes this clarification and the invertibility argument reviewed below. The original mathematical report remains unchanged.

## 1. Finite-type algebra and scalar scope

The Boolean-cube proof of the product bound is valid. For a singular knot with r independently resolvable crossings, resolving the complementary coordinates leaves any selected subset as a singular knot; consequently all mixed differences of order greater than a vanish for a type-a invariant. Its unique multilinear cube polynomial has degree at most a. Multiplication and reduction x_i squared = x_i cannot increase total degree, yielding type at most a+b for the product. Constants and finite sums have the stated bounds.

A fixed connected sum may be made in a small regular arc away from the singular points, so the varying singular crossings are unaltered. Mirroring reverses the sign of each crossing difference, yielding a harmless factor (-1)^r in an r-fold difference. Knot-orientation reversal preserves the same vanishing requirement. These pullbacks preserve upper degree bounds. This justifies every connected-sum/mirror operation used later; no assertion about taking a nonlinear sign function of a finite-type invariant is used.

The rational/real separation reduction is also valid. Extend a numerical type-d invariant Q-linearly from knot types to the free rational space. It annihilates the rational alternating-resolution span F_(d+1). A separator means the class of K-L in the rational quotient is nonzero. Choosing a rational linear functional nonzero on that vector supplies a rational finite-type separator. No finite-dimensionality assertion is needed; a basis extension suffices. This works for a complex separator as well. For integer signature, therefore, allowing real or complex approximants does not weaken the existence problem.

## 2. Finite interpolation and one countable sequence

For a finite E, choose separators only for pairs whose target f-values differ. Their finite feature vector has the property that coincident features imply equal labels. After retaining its distinct attained nodes a_i, the squared-distance denominators are nonzero positive rational numbers. Evaluating the i-th product at node a_i gives 1; evaluating it at any other node a_j gives 0 because the j factor vanishes. The weighted sum therefore takes the required labels even when distinct knots share a feature vector. Repeated feature nodes must not be inserted independently.

Each squared-distance factor has finite-type degree at most 2D when every coordinate invariant has degree at most D. The complete i-th product has degree at most 2D(m-1). The construction is a finite rational polynomial and hence a finite-type invariant on all knots, not merely a function on E. If E is empty use the zero invariant; if f is constant on E use that constant. The singleton case has empty products and degree zero.

Countability of smooth tame knot types follows from finite diagrams. Enumerate once, and interpolate on the nested initial segments E_n. A fixed K_i is covered for every n at least i, which gives eventual exactness by one global sequence. The proof does not select a different sequence for each knot. The opposite direction is immediate: knots agreeing for every finite-type invariant agree at every approximating stage and therefore have equal limits. This verifies all four equivalences, including the stronger eventual-exact formulation for a rational target.

The method is nonconstructive until the finitely many separators are supplied; it is not an algorithm to resolve the missing separation hypothesis. The elementary interpolation construction has no novelty claim.

## 3. Mirror detection is exactly the signature question

Signature additivity follows from block-diagonal Seifert forms, and mirroring negates the symmetric form (transposing a Seifert matrix, if that convention is used, has no effect on the symmetric form). Thus sigma(mK)=-sigma(K).

If signature has a pointwise finite-type approximation and sigma(J) is nonzero, its limits at J and mJ are different, so some approximant separates them.

Conversely, given sigma(K) different from sigma(L), J=K#mL has nonzero signature. A finite-type u separating J from mJ produces

w(X)=u(X#mL)-u(mX#L).

The two summands are finite type with the same upper degree as u. Oriented connected sum is commutative, so w(L)=0; mirroring commutes with connected sum, so w(K)=u(J)-u(mJ), which is nonzero. This supplies exactly the pair-separation hypothesis needed for Section 2. No cancellation or inverse in a monoid of knot types is assumed.

For the negative certificate, if K and L agree under every finite-type invariant but have different signatures, fixed-sum and mirror pullbacks show K#mL equivalent first to L#mL, then to L#mK=m(K#mL). Hence the conversion to a single nonzero-signature mirror-invisible knot is valid in both directions.

The antisymmetrized approximant (v_n(K)-v_n(mK))/2 is mirror-odd, remains finite type, and has the same signature limit. Averaging with reversal preserves it. Eventual exactness survives because only finitely many related knot types occur for a fixed K. The unknot is fixed by mirror and has value zero under the antisymmetrization.

## 4. Rational eventual approximation modulo 4

Each Conway coefficient a_(2j) has ordinary finite type at most 2j by the iterated skein relation. The proof uses the link Conway polynomial at intermediate oriented smoothings, which does not invalidate the coefficient bound for knots. Therefore D_n=sum_(j=0)^n (-4)^j a_(2j) has type at most 2n and stabilizes at each fixed knot to the signed normalized value D=Delta(-1).

Let a Seifert matrix have size 2g and set S=V+V^T. The skew form V-V^T is unimodular, so S modulo 2 has odd determinant. Thus S is nonsingular. Normalization gives D=(-1)^g det S, including g=0, where the empty determinant is 1. If q is the negative inertia index, then sign(D)=(-1)^(g+q)=(-1)^(g-q)=(-1)^(sigma/2). Consequently 1-sign(D) is exactly the representative 0 or 2 of sigma modulo 4. Reversing the global signature sign convention does not change this residue.

The h_n construction is odd Lagrange interpolation in x squared followed by multiplication by x. Its rational denominators do not vanish. It has ordinary polynomial degree at most 2n-1 and matches sign at the 2n positive and negative odd nodes through 2n-1. Hence R_n=1-h_n(D_n) is type at most 2n(2n-1). Given a fixed knot, take n at least its Conway half-degree, at least (abs(D)+1)/2, and at least 1. Both exact truncation and membership in the interpolation node set then persist for every larger n. This proves eventual exactness, not merely convergence.

The absolute determinant is insufficient. For either trefoil D=-3, whereas abs(D)=3 would give residue 0 instead of 2. The residue is also insufficient for full signature: opposite trefoils have signatures 2 and -2 with the same residue 2. The frozen-truncation control uses a connected sum with Conway polynomial (1+z squared)^2: truncation at degree two gives -7 while the full D is 9, giving different residues after adequate sign interpolation. These are actual counterexamples to the indicated invalid modifications.

## 5. Full signature on every torus knot

Willerton's normalization makes v2 and v3 equal to 1 on the positive trefoil; v2 is mirror-even and type two, v3 mirror-odd and type three. The two formulas in the packet agree with the source. These formulas and the standard torus classification are imported facts, not derived solely from the arithmetic tests.

For coprime integers p,q, every case with abs(p)=1 or abs(q)=1 is the unknot and gives (v2,v3)=(0,0). This includes parameters (0,1),(0,-1),(1,0),(-1,0) if zero parameters are allowed; coprimality excludes all other zero-parameter cases. They represent one knot, so the enumeration includes the unknot only once. Noncoprime parameters describe links and are outside this theorem.

Otherwise both absolute parameters exceed one, v2 is positive, and v3 is nonzero. Setting a=v2,b=v3 gives pq=6b/a, p squared+q squared=(6b/a) squared+1-24a, and p squared q squared=(6b/a) squared. The unordered positive squares are recovered as the roots of the resulting quadratic, and sign(pq) separates the two chiralities. Simultaneous sign change and exchange give exactly the stated redundancies. One must not apply the division formula at the unknot.

Oriented knots do not create missing torus nodes: standard torus knots are invertible. In the model (r exp(ipt),s exp(iqt)) in the unit 3-sphere, simultaneous complex conjugation reverses t and has determinant +1 in R4; it lies in SO(4), which is connected. It therefore gives an orientation-preserving ambient isotopy identifying the knot with its reverse. The cited classification consequently suffices for both oriented and unoriented versions.

With distinct torus feature nodes, the displayed cardinal construction is globally defined on every knot. Each squared feature distance has upper finite-type degree 6: the v2 square has degree at most 4 and the v3 square at most 6. Products have type at most 6(n-1), with degree zero when n=1. At any fixed enumerated torus knot T_i the cardinal evaluation is its signature for every n at least i. The signature labels must still be obtained independently; interpolation does not discover them. No behavior at nontorus knots is asserted.

## 6. Imported finite-cutoff and S-equivalence restrictions

Stoimenow Theorem 3, PDF page 5 / printed page 467, allows a fixed knot, an arbitrary fixed n, and any admissible single signature value. Its n-similarity convention is equality of ordinary Vassiliev invariants in degrees strictly less than n. Thus a type-d v requires n=d+1. At xi=-1 the admissible values are exactly 2Z: the symmetric Seifert form is nonsingular of even size, and connected sums of opposite trefoils realize all even values. There is no full-Alexander-polynomial preservation hypothesis in Theorem 3. Fixing that polynomial while freely prescribing arbitrary signatures is not what is used. The source is [Stoimenow's published PDF](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/stoim2.pdf). The full geometric realization proof and its cited input lemmas were not re-audited.

For a fixed v, its value remains v(K0) on these moving knots while their signatures range through 2Z, proving infinite supremum error. This does not obstruct pointwise eventual equality: for the discrete model f(k)=2k, set f_n(k)=f(k) for k at most n and zero otherwise. Each stage has unbounded global error, but every fixed k is eventually exact. This is a logical model, not a proposed knot invariant. The packet correctly distinguishes “for every cutoff, some knot” from “one knot, every cutoff.” The Conway escape argument is also valid when the prescribed signature differs modulo 4: once all nonzero base coefficients are within the cutoff, the new knot needs a nonzero higher coefficient or the residues would agree.

CMS v2, PDF page 2, explicitly attributes to Murakami-Ohtsuki the theorem that every Q-valued ordinary Vassiliev invariant invariant under S-equivalence is a polynomial in Conway coefficients. Its subsequent primitive, abelian-group extension has the no-2-torsion hypothesis; it does not restrict the preceding all-rational theorem to primitive invariants. PDF page 3 states that extension precisely. The inspected [current arXiv record](https://arxiv.org/abs/math/0511189) confirms v2 and the correction. The full clasper proof is imported. The packet correctly uses the stronger explicit CMS formulation rather than expanding the terse original Murakami-Ohtsuki corollary by guesswork.

Opposite trefoil Seifert forms have identical normalized Conway polynomial and symmetric signatures 2,-2 in an appropriate convention. Thus Alexander-only approximants fail, and the imported S-equivalence theorem makes individually S-equivalence-invariant rational finite-type approximants fail as well. There is no conflict with signature itself being an S-equivalence invariant; closure within the restricted subalgebra is the issue.

## 7. Source qualifications and novelty boundaries

The source packet clearly distinguishes complete PDF retrieval, selected-page reading, and complete proof audit. This audit preserves that distinction. CDM's historical signature-domination question supports the relationship to known separation problems, not a verified global 2026 open-status assertion. The self-contained finite interpolation and mirror argument do not rely on a supposed theorem from a search snippet.

Garoufalidis v1 Section 1.3 defines a simple knot through simple unit-circle Alexander roots; its signature consequence is expressly conditional on its conjecture. The multiple-root limitation and all-knots higher-order question are explicit. Neither its computational claims nor its torus-special-case proof were independently accepted here. The torus result under audit instead uses Willerton's formulas. No source-author mathematical software was executed.

No full Rogen article, Alvarez-Labastida formula proof, or standard torus classification proof was retrieved afresh or audited in full. No new broad literature search was conducted in this independent pass. The creator's recorded bounded searches and retrieval history were read as a record, not independently replayed. No priority or novelty conclusion follows from them.

## 8. Independent computational evidence

After reading the creator arithmetic script in full, I wrote a separate implementation rather than executing it. It constructs the sign polynomial from Newton divided differences, computes inertia by exact rational congruence elimination, enumerates all signed parameter quadrants including degenerate representations, and expands the cardinal polynomial into sparse two-variable coefficients to check weighted type degrees. All checks use explicit exceptions, not assertions.

Normal, -O and -OO outputs are byte-identical. They check 156 sign nodes; 184 integral Seifert matrices of genera 0 through 3 with unimodular skew parts; 21 eventual residue instances on an unknot/trefoil/connected-sum family; 640 coprime signed parameter instances in [-16,16] squared, including 128 representations of the unknot and 129 distinct types; and 15 growing cardinal interpolation nodes.

Ten actual mathematical negative controls reject: absolute determinant; residue mistaken for negative full signature; omission of the (-1)^g factor; removal of chirality-sensitive data; wrong v3 normalization; noncoprime torus parameters; division by v2 at the unknot; sign interpolation beyond its node set; fixed Conway truncation; and different labels at a repeated feature node. The exact failing checks are retained in the authenticated historical evidence; VERIFICATION.json records the normal and identical optimization-mode receipt identities. Raw computational outputs are not distributed here.

A separate independently authored verifier authenticated the creator's hardcoded inventory pin and closed member tree. Five copied-fixture corruptions were actually attempted and rejected: same-length member mutation, member truncation, same-length inventory mutation, an unlisted added file, and a changed external seal count. The restored fixture passed. Normal/-O/-OO receipts are identical. Input files were never mutated; controls operated only in temporary copies.

These finite checks corroborate the proved algebra. They do not prove source geometry, produce a universal finite-type invariant, check all degrees on a knot, prove signature mirror detection, or settle the original problem.

## 9. Exact audit scope

Read completely in the independent audit: the creator mathematical report, source-scope report, README, scholarly-source ledger, arithmetic-check program, packet-verification program, and anchored package-inventory metadata and member records. Creator code was inspected, not executed. All package members were byte-read for authentication, which is not a content-reading claim.

Selected source text pages actually read completely: Stoimenow 2005 PDF pages 2-5; Willerton 2001 pages 1,4,5,6; Murakami-Ohtsuki v2 pages 1-4; CMS v2 pages 1-3; CDM pages 75-77; Garoufalidis v1 pages 3-4. A truncated command also exposed part of Stoimenow page 10; pages 10-12 are not counted as complete reading. No reading is claimed for Willerton's thesis, Murakami-Ohtsuki v1, or inherited Ohtsuki/Kofman full documents in this independent pass.

Fresh PDF extraction was performed for Stoimenow page 5, Willerton page 5, and CMS pages 2-3, so the key claims were not accepted solely from creator-provided text sidecars. Fresh renders were visually inspected for Stoimenow page 5, Willerton page 5, and CMS page 2. The key formula signs, coprimality condition, normalization denominators, theorem quantifiers, and degree convention agree with the packet. An initial Willerton render command failed because its output destination did not exist and was successfully rerun; no source or mathematical output was altered.

Fresh web reads: current official arXiv landing records for Willerton math/0104061, CMS math/0511189, and Murakami-Ohtsuki math/9903069, plus the publicly hosted published Stoimenow PDF record. These verified manuscript/version metadata; no current worldwide resolution inference was made. The resulting metadata receipt is retained in the authenticated audit evidence.

The scholarly-source ledger records existing PDF byte hashes and sizes, actual selected-page audit scope, and external proof limitations. No fresh whole-PDF download is claimed for the independent audit. This public prose edition retains the complete mathematical review and inspection qualifications. It excludes programs, raw computational outputs, copied source PDFs, derived source extracts, source-page images, and private coordination material. Edition preparation performs byte-integrity and packaging verification only; it adds no mathematical computation, scholarly-source-body inspection, or literature survey.
