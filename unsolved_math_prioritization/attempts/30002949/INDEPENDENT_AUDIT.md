# Independent AI-assisted audit of the Coxeter stratification reconstruction

## Verdict

Accept the repaired partition-equality proof for its stated basic, length-zero-representative, classified Coxeter-type scope, with the explicit invariant-subset clarification supplied in INVARIANT_SUBSET_CORRECTION.md. The core geometric replacement, its rational group realization, the gallery argument, all support cases, the zero-dimensional branch, and the component-preserving reductive argument withstand this audit.

Do not accept the literal all-wall escape assertion in the inspected Görtz arXiv proof. The displayed unitary affine A3 example genuinely disproves that auxiliary assertion. It does not disprove the stratification theorem. A second auxiliary-source wording defect was found in the inspected Görtz–He Lemma 4.6.1; the actual subset Q used by the reconstruction is correct, and the separate correction proves it in all ranks.

The target is problem 30002949, corresponding to Miaofen Chen's Oberwolfach contribution, joint with Eva Viehmann, and subsequently Chen–Viehmann Conjecture 4.2. Görtz Theorem 0.1 expressly credits that conjecture; Theorem 3.4 gives the precise basic statement. Acceptance here is credited prior-theorem coverage with a repaired proof. There is no new-theorem claim, no theorem-counterexample claim, and no claim to have checked an unavailable final journal proof.

## Reviewed text and editorial identity

The complete reconstruction and source audit were read. The reconstruction reviewed before public editing had 28227 bytes and SHA-256 94a2d63b697ceeec5c4f5b55894bf97094f67936cc8de446c314ef7edbdeda15; the source audit had SHA-256 de37818dee61958adefc8c62cd63097177430cce2f4194760346098354027ab6. The complete mathematical regions are unchanged in this public edition. EDITORIAL_MAP.json records the exact editorial transformation, and ACCEPTANCE.json binds the accepted proof, required invariant-subset correction, and audits to their public hashes. This separate AI-assisted mathematical check is not external human peer review or formal certification.

## Accepted statement and precise boundary

Let G be a connected reductive group in the stated tamely split, minuscule GH category, with connected reduced affine diagram S and one of the thirteen listed affine Coxeter quadruples. Let K=S\{v} be σ-stable, where one σ-fixed vertex is omitted, and use connected parahoric level P_K. Let τ be a normalizer lift of the designated length-zero element, θ=Int(τ)σ, and J=G(L)^θ.

For each EO Coxeter element w with finite θ-support P, let Y(w) be the projected classical twisted-Coxeter DL set. The accepted comparison is between the functions

    j ↦ P_K j^{-1}gP_K,  j∈J,

and the individual translated pieces

    iY(w),  i∈J/(J∩P_{S\Σ_w}).

It is essential that the pieces are these refined BT pieces and that the complete rational coset index is retained. Entire EO unions are not the pieces being separated. In the original hyperspecial minuscule category the space is X_μ(τ).

The audit accepts the direct reductive argument for this connected reduced affine datum. It does not infer rational surjectivity J(F)→J_ad(F). It also accepts literal direct products of covered data by factorization of the varieties, relative positions, and rational test elements.

The following are outside this acceptance:

- Arbitrary replacement of τ by a σ-conjugate representative
- Nonbasic representatives or the separate a-number conjecture
- Arbitrary parahoric levels, including omission of an entire multi-node σ-orbit
- Arbitrary disconnected diagrams with factor-permuting Frobenius
- A fresh classification of all Coxeter-type data beyond the GH hypotheses
- A new independent proof of scheme-theoretic or mixed-characteristic closure statements
- The assertion that every line of the final Transactions article or the complete GH erratum was inspected

The proof directly establishes equality of the partitions on geometric points. Existing scheme/perfect-scheme and closure results transfer only within the ranges in which those results are already established; no broader closure theorem is certified here.

## The genuine obstruction in the old escape step

For the unitary affine A3 example, θ=(01)(23) acts in simple-root coordinates as

    θ(x1,x2,x3)=(1−x1−x2−x3,x3,x2).

Its fixed apartment is E={x2=x3, x1+x2=1/2}. The finite root β=α1+α2 is therefore constant at 1/2 on E. In particular, its values at the alcove barycenter (1/4,1/4,1/4) and the rational endpoint (1/2,0,0) coincide. Every θ-fixed alcove has barycenter in E and stays a bounded distance from the ambient wall β=0. That wall passes through the hyperspecial vertex p0, so changing the claim to all K-walls does not repair it.

The vector λ=(−1,1,1)=α2^∨+α3^∨ is a fixed coroot-lattice direction and β(λ)=0. Thus absence of rational translations is not the obstruction. The fixed apartment itself has the wrong direction for an all-wall escape. This is a positive reduced-rank-one example with connected ambient affine diagram, so it meets the literal hypotheses of Görtz Lemma 3.10.

The same stronger escape conclusion in Lemma 3.11 is unavailable in this example. Lemma 3.13 remains valid as a conditional sufficiently-far statement; its intended antecedent was the failing part. The reconstruction correctly replaces the required implication rather than pretending that antecedent holds.

## Lemmas A and B on projected vertices and finite separation

### Projection

The proof of Lemma A is valid. A finite-order affine isometry θ has fixed affine space E, and its affine average is the orthogonal projection q onto E. If u∈H=W_a^θ, then q(up)=u q(p).

The average q(p) is in the relative interior of the face spanned by the θ-orbit of p among the vertices of the base alcove. Equal projected points q(up)=q(u'p) are therefore in the relative interiors of two faces of the ambient Coxeter complex. Those faces must be the same minimal face. Since W_a preserves ambient vertex types, both up and u'p are the unique vertex of type v in that face. They coincide.

This proof uses neither θ(p)=p nor θ(K)=K. It proves injectivity only on H·p. A much stronger assertion of injectivity on the whole apartment would be false and is not used. The simplex hypothesis ensures that the convex hull of the orbit subset is a face. The subsequent type argument then recovers its distinguished vertex.

### Finite separation

The invariant lattice Q^∨∩D has full rank in the translation space D of E: the linear action of θ is integral and its invariant subspace is rational. For each distinct right-coset pair uW_K≠u'W_K in H, Lemma A implies that pr_D(up−u'p) is nonzero. The condition that a proposed λ have zero pairing with this difference is consequently a proper hyperplane in D.

Any nonempty open rational chamber cone in D contains an invariant lattice direction outside finitely many such hyperplanes, after scaling a rational point. Equality of

    W_K t_{−Nλ}u W_K and W_K t_{−Nλ}u' W_K

would imply equal distances from p to the corresponding vertex images, because W_K fixes p and acts isometrically. The squared-distance difference is

    −2N⟨λ,up−u'p⟩ + ||up−p||² − ||u'p−p||².

Its slope is nonzero. Each pair excludes at most one real value of N, so one sufficiently large positive integer handles all pairs. The argument only needs the necessary distance condition, not a claim that distances classify double cosets. No ambient root-regular direction is being smuggled back into the proof.

## Lemmas C and D on actual rational elements and galleries

### Rational lifts and ambient components

Richarz §1.2, Lemma 1.6, identifies the rational Iwahori-Weyl group with the Frobenius-fixed unramified group. Its proof explicitly makes the same identification for the affine subgroups. Therefore H=W_a^θ is the actual rational affine Weyl group, and its translations have representatives in the parahoric-generated rational group J^1. This is stronger than a formal fixed-point calculation in a Weyl group.

The reconstruction's direct ambient Kottwitz check is also valid. For h∈W_a^θ, take n0∈N(L)∩ker κ_G representing h. Then c=n0^{-1}θ(n0) lies in T(L)_1. Connected torus-parahoric Lang gives t∈T(L)_1 with tθ(t)^{-1}=c. Consequently θ(n0t)=n0t, its Weyl class is h, and κ_G(n0t)=0.

The sign in this Lang equation is correct: θ(n0)=n0c and cθ(t)=t. This avoids both a hidden adjoint rational-point lift and any loss of torsion or central component information. The existence of lifts in J^1 follows from Richarz's affine subgroup result; ambient κ-zero can independently be seen from the displayed calculation. These should not be conflated with an unsupported claim about all rational adjoint points.

Connected parahorics of J descend from the relevant θ-stable ambient parahorics, hence their elements have ambient Kottwitz value zero. Richarz's affine BN-pair provides the chamber and apartment transitivity needed below. Its hypotheses apply to J, a connected reductive inner form over the finite-residue-field local field.

### Gallery extension

Haines–Ngô §5 is applied to the rational apartment E, not to the ambient apartment. Every minimal rational gallery has a finite-Weyl direction, and the acute cone in that direction contains the appropriate translated chamber. The λ chosen above can be chosen in that same open chamber, so its large positive translates stay in the required acute cone. Concatenation of galleries in one direction is minimal.

Richarz Sublemma 1.12 says precisely that multiplication by a rational simple generator along a rational reduced expression remains length-additive for ambient length. Induction supplies

    ℓ_ambient(z^{-1}t_{Nλ})=ℓ_ambient(z^{-1})+ℓ_ambient(t_{Nλ}).

This is a genuine necessary bridge: rational simple generators need not have ambient length one. The reconstruction cites the bridge rather than silently identifying the two length functions.

Replacing the first rational gallery segment by any ambient gallery of the same reduced Weyl type is legitimate. The concatenated type is still reduced, so that ambient gallery is minimal even if its initial alcove is not rational. Reversing the resulting gallery yields the exact order t_{−Nλ}z used later. The extension depends on z, not on a particular point h' of the DL piece.

## All support cases and Lemmas E and F

The thirteen quadruples and their explicit EO words were checked against GH §§6.2–6.6. The reconstruction's support table agrees with the θ-orbit closures of those words. The following is an all-ranks verification of the properties used in the proof, supplemented but not established by finite calculations.

- Split affine A_{n−1}, μ=ω1: only empty support.
- Unitary affine A_{n−1}, μ=ω1: the words beginning with s0 and extending along n−1,n−2,… have θ-supports {1−l,…,l} modulo n for 1≤l≤floor((n−1)/2). They form a chain of connected cyclic intervals containing 0.
- Affine B_n, v=0: the supports are {0,1,…,l}, 1≤l≤n−1. The first consists of the two θ-exchanged arms; adding node 2 joins them. Later sets are connected and nested.
- Affine B_n, v=n, θ=(01): the supports are the nested chains {n−l+1,…,n}, 1≤l≤n−1.
- Affine B_n, v=n, θ=id: the same chain is followed by the two terminal sets S\{0} and S\{1}.
- Affine C_n, v=0, θ=id: the supports {0,…,l−1}, 1≤l≤n, are connected nested intervals.
- Affine D_n, v=0, θ=(01)(n−1,n): the supports {0,1,…,l}, 1≤l≤n−2, are nested; the first two arms are exchanged and every later set is connected.
- Affine D_n, v=0, θ=(01): the same chain is followed by S\{n} and S\{n−1}.
- The split affine A3, μ=ω2 row has the single nonempty support {0,2}, with its two components exchanged by θ.
- The twisted affine A3, μ=ω2 row adds S\{3} and S\{1} to that support.
- Affine C2, μ=ω2, v=0 has support {0,2}, with the components exchanged.
- Affine C2, μ=ω2, v=1 and θ=(02) has support {1}.
- Affine C2, μ=ω2, v=1 and θ=id has {1}, S\{0}, and S\{2}.

Every row includes ∅. Thus every nonempty support contains v; θ acts transitively on its connected components; support determines the EO element; and the order is a chain except for the indicated pair of terminal supports in exactly four rows.

If P=P' or P' is not contained in P, then Σ'∩P can be nonempty only for the two incomparable terminal supports. In each of the four rows, both supports have singleton complement. The missing node of P belongs to P' and is connected inside P' to v: follow the B chain from its omitted arm, the D chain from its omitted end, or the immediately visible A3/C2 path. This checks all ranks and all four forks. The source's restriction to the B example is too narrow.

Lemma E is valid. A word of distinct simple reflections along a noncommuting path has a unique reduced expression: no first braid or commutation move is available. The subword criterion applies to every reduced expression of x. On a decreasing left multiplication by s≠t0, take an expression beginning with s and remove that first letter; the required subword did not use it. Repetition proves survival under every element of W_P when t0∉P.

Lemma F correctly uses this survivor. In case 1, a path inside P' from v to the first exit from P, reversed, supplies the word. θ-transitivity of components ensures that an outside node can be chosen in the component of v. In case 2 with Σ' disjoint from P, choose t0 from supp(w1)∩Σ' and rotate its adjacent P' component to the component of v. For P'=∅, the ordering forces P=∅ and θ-stability supplies v itself. In the fork case, nontrivial left-minimal w1 cannot belong to W_P; the singleton complement of P must occur in its support and supplies t0.

In all three constructions, the tail is below w0,P' and w1w0,P' is length-additive. The path therefore lies below z=w1w0,P'. Its persistence under w0,P s^{-1} proves that v is in the support of (s w0,P)^{-1}z, so s w0,P W_K≠zW_K. The order of factors and the right-coset orientation are correct.

## The invariant-subset source correction

The reconstruction's reductive argument uses Q=I(K,w,σ)=S\(P∪Σ). The literal commutant wording in the inspected GH Lemma 4.6.1 is not a sufficient general statement when θ(K)≠K.

INVARIANT_SUBSET_CORRECTION.md gives two concrete counterexamples to that wording, an elementary all-ranks proof that a finite twisted-Coxeter operator has no fixed vector, and the corrected general formula:

    I(K,x,θ) is the largest θ-stable subset of
    {j∈K\P : s_j commutes with every s_i for i∈P}.

For nonempty classified P, its containing v makes the full commutant outside P already θ-stable and contained in K. For empty P, I is S\orbit_θ(v). Both yield exactly the Q used in the reconstruction. Acceptance of the Q step is bound to this actual formula and proof, not to the overbroad source sentence and not to finite computation.

## Constancy and separation of complete BT pieces

### Constancy

For any j∈J, J^1 can reach the same rational alcove. The residual element normalizes the ambient Iwahori and hence multiplies all Iwahori relative positions by one fixed extended-Weyl component. Thus proving constancy for a J^1 representative proves it for the original j; no central component is lost.

The gate of a rational alcove to a θ-stable spherical residue is rational by uniqueness. The finite rational parahoric quotient acts transitively on rational Borels. Lusztig's twisted-Coxeter open-cell theorem, together with rational equivariance, makes every DL flag opposite that gate. Gate distance additivity therefore gives one relative position for every point of Y(w). Passing to K-double cosets preserves constancy.

### Normalization in a common component

The full κ_G of a piece iY(w) is κ_G(i), because the standard finite DL piece lies in a connected parahoric. Different values are already distinguished by inv_K(1,−). In a common component one can left-translate to Y(w) and j'Y(w') with κ_G(j')=0.

The two residues have rational corresponding closest alcoves. A rational element of P_P moves the first one to a, and the rational Iwahori then sends a rational apartment through the pair to the standard apartment. These elements preserve Y(w) by rational equivariance. Moving the second base alcove within its rational P_P' residue preserves the second DL piece. The resulting representative can be replaced by the rational normalizer lift of the minimal double-coset element w1; the remaining quotient is in the rational Iwahori. All replacements retain ambient κ-zero.

If that normalizer preserves Y(w'), it can be replaced by 1 as an equality of sets; one then compares the standard residues afresh, so w1=1. Otherwise the exact stabilizer forces supp(w1) to meet Σ'. These are precisely the two alternatives required by Lemma F.

### The test element really separates all points of both pieces

Put z=w1w0,P' and u_s=s w0,P for s∈W_P^θ. All these elements belong to H, and Lemma F makes their right cosets different. Lemmas B and D therefore give one λ and one sufficiently large N for every such s and every h' in the second DL piece.

The first residue and the translation alcove lie in the standard apartment, so their gate is s_N a with s_N∈W_P^θ. Oppositeness and gate additivity give

    δ(t_{Nλ}a,h)=t_{−Nλ}s_Nw0,P,
    δ(t_{Nλ}a,h')=t_{−Nλ}z.

The two K-double cosets differ by Lemma B. Lemma C realizes t_{Nλ} by an actual rational test element in J^1. This proves separation, not merely a difference between formal Weyl expressions.

## Exact stabilizers and reductive groups

The exact stabilizer argument is sound once Q is computed by the corrected invariant-subset formula. Since Q⊆K, P and Q commute, and R=P∪Q=S\Σ is spherical, GH's canonical fine-to-coarse map identifies the fine K-piece with a coarse Q-level piece. Its parahoric-refinement construction uses connected parahorics and finite Weyl operations, so it applies directly to the reductive group.

At Q-level, the condition is g^{-1}θ(g)∈P_Q xP_Q⊂P_R. Connected-parahoric Lang gives g∈J P_R. The ambient cosets iP_R/P_Q, indexed by J/(J∩P_R), are genuinely disjoint. The finite quotient has commuting P and Q directions, and the subset in the standard residue is precisely the P-Coxeter DL set. Rational elements of P_R preserve it; elements outside P_R move it into a disjoint residue. Nonemptiness therefore gives the exact stabilizer J∩P_R.

This is a coset argument in the actual group G(L). It is not the generally unsafe replacement of a connected parahoric by an unlabelled full facet stabilizer. GH §4.5 separately handles the Ω components, and the reconstruction retains κ_G throughout. Central isogenies preserve the finite flag varieties and Weyl calculations needed here but are never invoked to lift arbitrary rational adjoint points.

The original CV Lemma 2.4 explicitly requires rational adjoint surjectivity for its converse. The proof audited here does not use that converse. Its rational translation, gate, and apartment operations all arise from the actual group J and its parahorics.

## The zero dimensional branch and products

If D=0, the fixed affine simplex has dimension zero. Since its fixed-face barycentric coordinates are constant on θ-orbits, its dimension is the number of vertex orbits minus one. Hence θ is transitive on all vertices of S. A proper θ-stable support is then empty. The only DL piece is the point Y(τ), and all its translates are points.

For two different points jP_K and j'P_K with j,j'∈J, evaluation at j gives the identity double coset at jP_K and cannot do so at j'P_K. This separates the points without any translation or gallery argument. The split minuscule A superbasic row is included. Positive rational reduced rank cannot be assumed in all classified cases.

For a pure torus, the connected-parahoric quotient is the Kottwitz quotient and a κ fiber is a single flag point. Evaluation at 1 already separates these points. Literal direct products factor the test functions and BT pieces, so equality follows factor by factor; this observation does not establish unaddressed factor-permuting cases.

## Independent controls and their limits

The audit authored and ran two exact controls; no source-author code was executed.

1. An exact support calculation checks all thirteen rows at 77 representative parameter values, totaling 407 supports. It uses the Tits reflection representation over Q(√2), verifies diagram automorphisms, left minimality, one representative per θ-orbit, the orbit support, maximal invariant I by direct simple-reflection conjugation, θ-component transitivity, and the exact four fork patterns. Result: PASS.
2. An exact projected-vertex calculation checks the affine A3 obstruction and 25 elements generated by the folded reflections s0s1s0 and s2s3s2. The resulting 13 distinct vertex images have 13 distinct projections. Both chamber directions ±(−1,1,1) separate all sample squared distances for N=6; the largest exceptional real N is 11/2. Result: PASS.

These finite controls detect transcription and sign errors; they do not prove the all-ranks assertions. The preceding geometric and graph proofs, and the separate general invariant-subset proof, are the mathematical justification.

## Sources actually inspected in this independent audit

Read limits here describe this separate audit alone. The source audit records its own inspection scope.

- OWR 39/2015: Chen's setup and item 1 on printed pp. 2297–2298 were read from the recovered text; the surrounding end of the contribution was located but is not needed for the target claim. Public source: https://ems.press/content/serial-article-files/46591 .
- Chen–Viehmann arXiv:1507.02806v2: setup and Remark 2.1, Lemma 2.4 and Remark 2.5, and §4.2 including Conjecture 4.2 were read from the recovered text. The unitary comparison was located but its full proof was not independently reaudited here; it is not needed to certify the replacement proof. Source: https://arxiv.org/pdf/1507.02806 .
- Görtz arXiv:1802.02225v1: introduction, §1.1–1.5, and the full §3 argument were read from the recovered text, including every replaced step and the original fork argument. Section 2's separate finiteness theorem was not reaudited. Source: https://arxiv.org/pdf/1802.02225 .
- Görtz–He 28-page author copy: the setup, §§2.2, 3.1, 4.1–4.6, 5.1–5.2, 6.1–6.6, and 7.1–7.2 were read from the recovered text. Printed p. 13 was independently rendered and visually read to verify the exact Lemma 4.6.1 wording. The explicit thirteen-row EO list was checked, but the exclusion of every nonlisted datum is accepted as the GH classification theorem rather than reproved. Source: https://archive.ymsc.tsinghua.edu.cn/pacm_download/465/10790-Xuhua_He_62.pdf .
- Old GH arXiv:1311.6263v1: the I-definition and the corresponding commutant passage were checked for comparison. The old article was not otherwise independently read in full. Source: https://arxiv.org/pdf/1311.6263 .
- Haines–Ngô: all of the relevant acute-cone definitions and proofs through Corollary 5.6 were read, together with the following chamber-translation corollary and the start of the next application. Source: https://www.math.uchicago.edu/~ngo/alcoves.pdf .
- Richarz: all printed pp. 117–124 were read, including the complete rational fixed-group proof, affine BN-pair setup, Kottwitz kernel argument, and length-additivity sublemma. Source: https://www.numdam.org/item/10.24033/bsmf.2708.pdf .
- Lusztig: printed pp. 101–103 and 107–113 were visually read. This includes the reduction over centers/products/cyclic factor permutation, the Bruhat and root-subgroup proof of §§2.2–2.4, and the full Corollary 2.5 argument. Printed pp. 104–106 and later representation-theoretic sections were not independently audited. The definitions needed for the use here are also explicit in Görtz §1.1. Source: https://gdz.sub.uni-goettingen.de/download/pdf/PPN356556735_0038/LOG_0012.pdf .

Every listed PDF's hash and size was independently checked. SOURCE_VERIFICATION.json gives the exact source pins and retrieval history. The mathematical source PDFs are not reproduced in this public packet.

The retained bibliographic metadata identify Görtz's Transactions of the AMS publication as volume 372 (2019), pp. 4675–4699, DOI https://doi.org/10.1090/tran/7715 . The final journal PDF was not available in the supplied packet and was not read here. The complete GH erratum was likewise not available. All criticisms above are tied to the precise recovered preprint/author-copy versions, not to unseen versions.

## Foundational dependencies and stopping condition

This audit accepts the standard gate/projection theorem for spherical residues, the strong transitivity consequence of the affine BN-pair, the Coxeter braid/subword criterion, connected-parahoric and torus Lang surjectivity, and GH's classification. Their exact roles have been checked; the complete foundational books and every paper behind GH's classification were not retrieved or reproved. Lusztig's needed finite DL theorem and Richarz's needed rational/length results were checked in the pinned source versions.

There is no outstanding mathematical obstruction to the accepted partition-equality scope after the explicit Q clarification. The source-version boundary remains: neither this report nor the accompanying source audit certifies the unavailable final journal text. Nothing in the accepted proof needs further all-wall escape, a rank-positive assumption in the superbasic case, or rational surjectivity to the adjoint group.
