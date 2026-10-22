# Independent audit of the KK uniqueness application for problem 30005199

Date: 8 October 2026. New proof-search turns: 0. Mathematical credit: Gábor Szabó and the explicitly identified prior sources.

## Decision

**Accept the standard stable-ideal ordinary-absorption application, including its transfer to a possibly nonessential ambient extension. Accept the separate separable-ideal unitally absorbing application with proper asymptotic equivalence only. Retain the exact OWR relative-absorption and stability convention hold.**

No counterexample, missing analytic hypothesis, or unrepaired mathematical gap was found in these stated applications. This is independent mathematical review of a credited prior result, not an original solution, a formal proof-assistant certification, or journal-status certification. In particular, it does not authorize calling the literal unrestricted OWR formulation resolved without fixing its undefined convention.

The source proof has minor printed defects discussed below. The original authored application already repairs the target-relevant defects correctly. A separate optional clarification patch makes three compressed steps explicit; it does not change the accepted theorem or remove any reservation. No change to the original application is required for the mathematical decision.

## Publication context and independent work

This is a publication derivative of the independent mathematical audit. Its mathematical decision and proof analysis are preserved. The current PROOF_APPLICATION.md adopts the three optional clarifications described above, exactly as specified by APPLICATION_CLARIFICATIONS.patch. PATCH_HISTORY.json identifies the authored base, exact patch and resulting proof. The full superseded application is omitted.

The independent review extracted the primary PDFs, read the complete Szabó v1 main body and reconstructed the target proof chain, including the corrected stable-operator-homotopy input. It compared the relevant v2 statements, checked the ambient and separate unital bridges, and visually inspected the scanned Cuntz–Higson proof and Szabó v1 p.15. SOURCE_AUDIT.json records the public source hashes, sizes and inspection scope. These are historical inspection records; the portable validator does not obtain or replay source bodies.

Earlier local packaging and execution details have been omitted. Fresh execution of the unchanged nine authored and sixteen independent finite tests is provided by this delivery, together with mode-specific complete output references and adversarial verification. Those finite checks do not certify infinite-dimensional analysis. The source-based mathematical acceptance remains the independent review's judgment, not a computational inference.

## Precise theorem accepted

Let C be separable and D nonzero, stable and σ-unital. Let D be a closed two-sided ideal in E, and let λ:E→M(D) be its canonical multiplier action. Let Φ,Ψ:C→E be *-homomorphisms such that Φ(c)−Ψ(c)∈D for every c. Suppose φ=λΦ and ψ=λΨ are ordinarily absorbing representations. Then

[Φ,Ψ]=0 in KK(C,D)

is equivalent to the existence of a norm-continuous path u:[0,∞)→U(1+D), with u(0)=1, such that Ad(u(t))Φ(c) converges in norm to Ψ(c) for every c.

E is not required to be essential over D or separable. C need not be unital. There is no Z-stability, nuclearity, simplicity, exactness, UCT, rank or corona-factorisation requirement. D=0 is a separate immediate case: the maps are equal.

For the separately accepted unital version, D is separable as well as stable, C is unital, and λΦ and λΨ are unital and unitally absorbing. The same equivalence holds with a norm-continuous path in U(1+D), **without an assertion that its initial value is 1**. The proof uses Hua's conditional unital criterion together with Szabó's K1-injectivity theorem.

## Absorption and the exact-source bridge

Carrión–Gabe–Schafhauser–Tikuisis–White v3 Definition 5.8 requires absorption of every representation C→M(D), with differences in D at every step and norm convergence to zero. Proposition 5.9 proves that its sequence formulation is equivalent to the norm-continuous asymptotic formulation. Its proof forms double infinite repeats, extracts orthogonal approximately intertwining isometries, and invokes the established absorption-path construction. This matches Szabó v1 Definition 1.9, including the ideal-valued errors. The import requires only a separable domain and stable σ-unital coefficient algebra; no separability of M(D) is inserted.

Ordinary and unital absorption must remain distinct. At the unit, a unital φ cannot absorb zero ordinarily: the Cuntz-sum support has a nonzero complementary projection, whose norm is one after any unitary conjugacy. Unitally absorbing maps instead absorb only unital comparison maps. The set of such maps is not the eligible set required by Szabó Theorem 4.6, since that framework includes zero. The application's separate unital route is therefore necessary and correctly scoped.

Gabe's original Oberwolfach contribution, Report 36/2022, p.2104, Theorem 3 and Question 1, has been read in its surrounding contribution. It says that C,D,E are separable and uses absorption relative to D, but does not define that phrase or state D stable there. The later multiplier formulation is fully explicit about stable σ-unital D. This review finds no source-defined equivalence that licenses silently substituting the latter hypotheses into every possible reading of the former phrase.

Tensoring a nonstable ideal with K identifies obstruction groups; it does not supply a way to compress an arbitrary stabilized unitary path back to the original ideal's unitization. Likewise, stability of D does not imply stability of every multiplier corner pDp. A valid corner reduction would have to establish the corner's own stability, absorption, class identification and complementary-map compatibility. These conditions are correctly retained in the application. The exact-source convention hold is therefore substantive rather than cosmetic.

## Canonical multiplier transfer and the reverse direction

The canonical multiplier action may have a nontrivial kernel on E, but its restriction to D is faithful: dD=0 implies d=0 by an approximate identity. Hence λ is isometric on D. This is precisely the amount of faithfulness needed.

Carrión et al v3 Definition 5.2 and footnote 100 define the class of an ambient Cuntz pair using the canonical map E⊗K→M(D⊗K) and a rank-one corner. Applying that construction to λΦ and λΨ gives the same stabilized pair. Under the standard stability identification, the two obstructions agree. This is not a claim that E injects into M(D).

Write an output unitary as u=1+d with d∈D. The element is a unitary in the forced unitization of E because its unitary identities already hold in D's unitization. The difference

Ad(1+d)(Φ(c))−Ψ(c)
= Φ(c)−Ψ(c)+dΦ(c)+Φ(c)d*+dΦ(c)d*

belongs to D. Its multiplier image is the error for φ and ψ, so the two error norms are equal. Thus convergence transfers back to E without lifting an arbitrary multiplier unitary. Independent noncommutative polynomial and direct-sum controls check the finite algebra in this argument. A separate negative control shows that if the hypothesis Φ−Ψ∈D is removed, the multiplier map can erase a genuine nonzero ambient error.

Conversely, a proper asymptotic path compactifies to a Cuntz homotopy: use t=s/(1−s) on [0,1), and extend the conjugated map at s=1 by Ψ. For each c, the ideal-valued differences are norm-continuous through s=1. If u(0)=1 this immediately connects the original pair to a degenerate one. With an arbitrary initial u(0)∈U(1+D), stable inner invariance supplies the same result; the usual two-by-two rotation connects diag(u(0),u(0)*) to 1 within the ideal unitization. This is the correct reverse implication for both versions.

## Reconstruction of Szabó's K1 injectivity proof

Put Dφ={x∈M(D):[x,φ(c)]∈D for all c}. The letter J below denotes an arbitrary auxiliary closed ideal of Dφ; it does not denote the coefficient ideal D.

### Reduction and projection criterion

Absorption of φ∞, Proposition 1.12 and the invariance of the modulo-D commutant under unitary conjugacy allow one to replace φ by an infinite repeat. In Gabe–Szabó v4 the pertinent content is Lemma 3.11, rather than the numbering used in Szabó's published reference. Its construction uses a quasicentral approximate identity, summable almost-orthogonality bounds, a strictly convergent sum X with ∥1−X*X∥<1, and polar normalization to an isometry. Weak absorption of an infinite repeat also supplies the required isometry by compression. For φ itself, φ⊕φ∞ is unitarily equivalent to φ∞ by reindexing. No assertion that an arbitrary absorbing map was initially an exact infinite repeat is needed.

For an infinite repeat there are isometries r_n in the exact commutant with orthogonal ranges summing strictly to 1. The exact commutant, not generally all of Dφ, has zero K-theory by the infinite-repeat identity id⊕repeat=repeat. Reindexing the ranges gives an O2 pair, so Dφ and every nonzero unital quotient are in Cuntz standard form.

Set P=Σr_{2n}r_{2n}* and p=P+J. This is a splitting projection of zero K0-class. Given any other zero-class splitting projection q, Cuntz's classification of full properly infinite projections, also recorded in Blanchard–Rohde–Rørdam Proposition 2.3, gives q=w(1−p)w* for a quotient unitary w. Take a contractive lift W of w and Q=W(1−P)W*. W and Q need not be a unitary and a projection upstairs.

The fixed-p form of the homotopy criterion is valid. In Blanchard–Rohde–Rørdam Proposition 5.1, implication (ii)⇒(i) starts with an arbitrary K1-trivial unitary u, fixes any splitting p, and takes q=upu*. If p and q are homotopic, a connected unitary v makes vu commute with p. Their Lemma 2.4(ii) then connects vu, and hence u, to 1. Thus Szabó's use of a single fixed p is supported by the actual proof.

### Selection and strict sums

Take an increasing φ(C)-quasicentral approximate identity (e_n) in D with e_{n+1}e_n=e_n. This strengthened choice is supplied by the quasicentral approximate identity lemma stated in Szabó Lemma 1.2. Choose decreasing functional-calculus tolerances and dense finite sets in the domain.

Inductively choose alternating even m_k and odd n_k so that all required quasicentral errors are small and

f_k=r_{m_k}e_{m_k}r_{m_k}*, h_j=Wr_{n_j}e_{n_j}r_{n_j}*W*, ∥f_kh_j∥<2^{−j−k}.

This induction is justified: at each stage only finitely many new interactions are imposed, and the product of a fixed ideal element with a sufficiently remote range is small. For instance ∥b r_n∥²=∥b r_nr_n*b*∥→0. It does not require a countable dense set in M(D).

F=Σf_k and H=Σh_k exist strictly, with 0≤F≤P≤1 and 0≤H≤Q≤1. The cross-product double series converges absolutely in norm. Its sum is FH because finite rectangular partial products converge strictly to FH, and a norm limit has the same strict limit. Strictness of the final bound is justified by a fixed margin: if ε=1/4−∥f_1h_1∥>0, then the full sum is at most 1−ε. One need not incorrectly interchange the facts that every finite sum is below one and that the infinite sum is below one.

Let a_k=(e_{m_{k−1}}−e_{m_{k−2}})^{1/2}, and similarly b_k with n. The subscripts are indexed sequence values, not m_k−1. The squares telescope strictly to 1. The absorbing-product property of e_n gives e_{m_k}a_k=a_k and e_{n_k}b_k=b_k. Square-root functional calculus and the chosen tolerances yield summable commutator bounds against each member of the dense union of finite sets.

For completeness, strict convergence of R1=Σr_{m_k}a_k is justified on both sides. For a finite tail T and d∈D, ∥Td∥² is bounded by the corresponding tail of d*(Σa_k²)d and tends to zero. Also TT* is bounded by the tail range projection Σr_{m_k}r_{m_k}*, so ∥dT∥ tends to zero. The sums are uniformly contractive. Thus a multiplier limit exists and satisfies R1*R1=1 and FR1=R1. The commutator series is norm-summable in D for each dense test element; density handles all c. The same argument gives an isometry R2'=Σr_{n_k}b_k in Dφ.

### Quotient identities and homotopy

Set R2=WR2'. Since W*W−1∈J, R2*R2−1∈J. Likewise HR2−R2∈J. These are quotient identities, and replacing them by exact identities upstairs would be invalid. The quotient elements s_i=R_i+J are isometries with ranges dominated by p and q, respectively. Their overlap obeys

∥s1*s2∥=∥π_J(R1*FHR2)∥≤∥FH∥<1.

The projection domination follows from FR1=R1 and its quotient counterpart: a positive contraction acting as the identity on an isometry's range dominates that range projection. The independent quotient-lift control explicitly rejects treating W as unitary upstairs.

Cuntz–Higson Lemma 1 applies to the range projections because they are equivalent and their product norm equals ∥s1*s2∥. The entire printed proof on pp.430–431 was visually read: the orthogonal case uses a self-adjoint swapping unitary; the general case deforms the second projection by continuous functional calculus to a projection orthogonal to the first. Using that lemma along the chain

p, 1−p, s1s1*, s2s2*, 1−q, q

gives the needed homotopy. Every adjacent pair is equivalent; the outer orthogonal pairs have product zero, and the middle pair has product norm below one. The projection criterion proves K1-injectivity of Dφ/J. Taking arbitrary J proves the full quotient conclusion, including the corona relative commutant at J=D.

### Printed defects

Szabó v1 p.15 prints s1*s1* in place of the range projection s1s1*. The same typo remains in the inspected v2. A rational rotation provides a concrete negative: s*s* need be neither self-adjoint nor idempotent. The application's correction is forced by FR1=R1 and is valid.

V1 compresses the quotient norm calculation; v2 explicitly writes π_J(R1*R2)=π_J(R1*FHR2). The application correctly uses this quotient equality and does not assume HR2=R2 upstairs. These are local printed repairs, not new lemmas or a new proof search.

## From a null KK class to a proper path

Specialize Szabó's group to G={1}. Every cocycle is trivial, every pair is anchored, and the eligible class of all representations produces ordinary KK(C,D) by Example 3.7(1). Strong stability becomes ordinary stability. The σ-unital coefficient hypothesis is the standing hypothesis of both Szabó's theorem and the relevant Gabe–Szabó imports.

Mutual absorption supplies a multiplier path U_t with Ad(U_t)ψ→φ and ideal-valued errors. Because φ−ψ takes values in D, U_t belongs to Dφ=Dψ. Compactifying the conjugated pair identifies its initial Cuntz class with [φ,ψ].

The kernel argument in Theorem 4.4 then gives [U_1]=0 in K1(Dψ). Its required stable-operator-homotopy input is Szabó Lemma 3.12, using corrected Gabe–Szabó v4 Notation 2.7 and Lemma 2.8. The auxiliary representation is built from the endpoint model for C[0,1] and both members of the Cuntz homotopy. The separability/downward-closure check of Szabó Lemma 3.11 is automatic for the class of all representations, but does not replace the analytic input.

The corrected Gabe–Szabó proof was checked in detail. Its coefficient algebra E1 is σ-unital, its E2 and commutator-control set are separable, and its strictly continuous auxiliary map becomes norm-continuous after multiplication by E1. Those are exactly the conditions needed for Kasparov's technical theorem. The resulting commuting positive contractions N,M satisfy N²+M²=1 and give the rotation matrix with rows (N,M) and (−M,N). The three-piece path, consisting of a logarithmic path to that rotation, its conjugated moving middle piece, and a logarithmic exit, joins 1 to w1⊕w1*. It remains in the modulo-D commutant. Independent exact block-matrix controls verify the rotation algebra and reject the wrong lower-left sign. The earlier erroneous proof is not used.

After further summands, the stabilized representation may be assumed an infinite repeat. The exact-commutant K1 class vanishes there; the operator homotopy shows this is the class of U_1⊕1. Lemma 4.3 brings the class back to Dψ, since the corner embedding followed by absorption is conjugation by an isometry in Dψ. Lemma 4.2's two-by-two isometry homotopy proves that such conjugation induces the identity on K-theory. This step concerns multiplier-relative-commutant K1; it is not an unsupported switch to a corona class.

K1-injectivity now gives an actual path from 1 to U_1 in U(Dψ). Concatenation with U_t gives the required multiplier path starting at 1. Gabe–Szabó Corollary 4.4, appearing as Szabó Lemma 4.5, converts it to a path v_t in U(1+D), also starting at 1. Its supporting Lemmas 4.2–4.3 take logarithms only of short unitary increments, cut them down by a quasicentral approximate identity, and assemble paths with summable errors. The bound for the commutator of v_t*U_t with ψ(c) tends to zero, which proves that v_t implements the same limiting conjugacy. A multiplier path alone would not establish the theorem.

This construction is oriented ψ→φ. Taking u_t=v_t* gives the displayed φ→ψ conclusion with identical error norm and preserves u_0=1. This symmetry is implicit in the original application and explicit in the optional clarification patch. No Section 5 duality theorem is needed, so there is no circular appeal to a later duality conclusion.

## Separate unital argument

Hua's thesis Theorem 4.3.5(i), pp.79–80, has exactly the separable unital domain, separable stable ideal, unitally absorbing Cuntz-pair and corona K1-injectivity assumptions used here. Szabó Corollary 2.9 supplies the last hypothesis because a unitally absorbing map still absorbs its own unital infinite repeat.

Hua first obtains a multiplier asymptotic path. A null relative KK class and Lemma 4.3.6 supply a stable homotopy for its initial unitary modulo D. The auxiliary representation θ is unital. Adjoin a third block carrying φ, and use unitary absorption only on the second and third representation blocks, θ⊕φ. This leaves the first block, which carries the initial unitary, unchanged. The resulting corona homotopy is a stabilized null homotopy in the matrix algebra over Q(D)∩φ̄(C)'. Hence the initial corona unitary has zero K1-class, and K1-injectivity gives an unstabilized corona path.

The thesis's prequotient commutant display on p.80 must be read as commutation modulo D, exactly as Lemma 4.3.6 states; exact commutation before quotienting is not claimed here. Its use of the word absorbing at that point is unital absorption of the unital θ. The original application already recognizes both issues. Hua explicitly warns that using Thomsen's ordinary absorbing Paschke duality directly for a unitally absorbing map would be a gap, and instead supplies this stable-homotopy proof.

Hua Lemma 4.3.4 and Carrión et al Lemma 5.16(i) then give a proper ideal-unitization path. The latter lemma also requires injectivity of the common corona representation; unitally absorbing maps have that property, as explained in Hua Proposition 4.2.9. One can also see it directly by absorbing an infinite repeat of a faithful representation: if the corona map killed a nonzero a, absorption would force that essential comparison representation to kill a too. The application's use of the Hua criterion imports this requirement through its proven absorption hypothesis, rather than adding an independent hidden assumption.

Normalize the scalar part of any unitization path to 1; this changes no conjugation action. This does not normalize its initial unitary to 1. Multiplying by the initial inverse can change the maps being compared, as an explicit matrix control demonstrates. Accordingly, this review asserts proper asymptotic equivalence only for the unital version. The ambient transfer and reverse implication established above apply unchanged.

## Specialized results and verification limits

Hua–White v1 Theorem 4.1 requires corona factorisation and a proper intermediate ideal that is relatively purely large. Corollary 4.2 requires real rank zero, stable rank one, K1(D)=0 and totally ordered V(D), with a full weakly nuclear unital map. Theorem 4.10 uses these regularity assumptions and vanishing in nuclear KK. None of these hypotheses follows from the OWR sentence. The application correctly does not substitute these specialized results or an unverified refined KK obstruction for ordinary KK.

The test suite deliberately contains semantic negatives: omitting the nonlinear ambient-error term; dropping the ideal-difference assumption; omitting the corner complement; compressing a unitary; retaining the printed range-projection typo; forcing the initial unitary to 1 by naive normalization; using a wrong rotation sign; treating a quotient-unitary lift as unitary upstairs; confusing delayed sequence indices; and replacing summable estimates by merely small terms. Their successful rejection is useful evidence about the local algebra and scope warnings. It proves none of functional calculus, strict topology completeness, absorption, or KK-theory.

The remaining analytic imports are ordinary continuous functional calculus, the strengthened quasicentral approximate identity lemma, Kasparov's technical theorem, Cuntz projection classification, standard K-theory homotopy/stability, and the established Cuntz-pair/KK framework. They are identified rather than reconstructed from axioms. The full equivariant or refined-group applications elsewhere in the papers are not separately accepted by this target-specific review.

The disposition remains **HOLD_EXACT_RELATIVE_ABSORPTION_CONVENTION_WITH_VERIFIED_STANDARD_PRIOR_RESOLUTION**. The independent review accepts the specified prior-result application, not an unqualified new solution of the literal catalogue wording. No original proof-search turn was spent.

## Public primary references

- James Gabe, Elements of classifying C*-algebras, Oberwolfach Report 36/2022, pp.2103–2105: https://ems.press/content/serial-article-files/46972
- Gábor Szabó, The uniqueness theorem for Kasparov theory, v1: https://arxiv.org/pdf/2601.23029v1 ; relevant update v2: https://arxiv.org/pdf/2601.23029v2
- Carrión, Gabe, Schafhauser, Tikuisis and White, Classifying *-homomorphisms I, v3: https://arxiv.org/pdf/2307.06480v3 ; numbering comparison v4: https://arxiv.org/pdf/2307.06480v4
- Gabe and Szabó, The stable uniqueness theorem for equivariant Kasparov theory, corrected v4: https://arxiv.org/pdf/2202.09809v4
- Blanchard, Rohde and Rørdam, Properly infinite C(X)-algebras and K1-injectivity: https://ems.press/content/serial-article-files/30436
- Cuntz and Higson, Kuiper's theorem for Hilbert modules, original-paper scan: https://ncatlab.org/nlab/files/CuntzHigson-KuiperForHilbertModules.pdf
- Shanshan Hua, Topics in the structure and classification of C*-algebras and *-homomorphisms, Oxford thesis, 2025: https://ora.ox.ac.uk/objects/uuid%3Adae9829a-cc2a-4e1a-9af9-558ffa2cf7bf/files/d4b29b6686
- Hua and White, Uniqueness for embeddings of nuclear C*-algebras into type II1 factors, v1: https://arxiv.org/pdf/2601.08779v1
