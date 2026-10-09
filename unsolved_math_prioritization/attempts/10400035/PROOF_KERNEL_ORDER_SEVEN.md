# A nonzero order-seven invariant vanishing on every free two-string exterior

Problem 10400035 / AMR-103-0035, Stanford Question 2.13.
Substantive approach 3 of a shared maximum of 5.

**Disposition: proof candidate, independent audit requested. The geometric support lemma and source checks are complete.**

## 1. Result and exact range

Work with ordinary unframed smooth ordered upward-oriented two-string links in a ball C=D²×[0,1], fixed at matching endpoint pairs and straight in endpoint collars. Let V_n(2) consist of rational-valued ordinary finite-type invariants of order at most n, including constants. Let F_2 be the string links whose actual three-dimensional exterior group is abstractly F_2, without any meridian-basis assumption, and let N_n(2) be the subspace of V_n(2) vanishing on all of F_2.

**Theorem. N_7(2) contains a nonzero rational invariant. Consequently N_n(2)≠0 for every n≥7.**

More precisely, choose the simultaneous reversal involution ρ on this fixed-endpoint category. Every L∈F_2 satisfies ρL=L as an ordered ordinary string-link isotopy class. Duzhin–Karev supply an ordinary rational finite-type invariant of order at most seven which is not invariant under ρ. Its antisymmetrization therefore belongs to N_7(2) and is nonzero. A degree-seven nonzero symbol can be specified, so the constructed invariant may be taken to have exact order seven.

This statement is specific to two strands. It gives no extension to k≥3 by forgetting components: a free k-string exterior need not remain free after deleting strands. The already accepted previous approach gives N_n(k)=0 for all k≥2 and 0≤n≤2. The intermediate values N_n(2), 3≤n≤6, and the higher-order question for k≥3 are not settled here. No minimal-order claim is made.

The proof is source-backed and existential at the integration step. It defines a nonzero invariant by rational weight-system integration and antisymmetrization; it does not claim a closed numerical formula or a computed value on a named nonsingular string link. All sources and the exact involution are specified below. The accepted turn-1 and turn-2 packets and their audits are unchanged.

## 2. The exact ordered reversal

Choose standard coordinates with the two labeled basepoints p_1,p_2 on the real diameter of D². If different basepoints were initially prescribed, transport once by a fixed orientation-preserving disk diffeomorphism; this gives an isomorphism of the string-link categories preserving exterior groups and finite-type orders. No variable boundary re-marking is taken as an equivalence.

Define the orientation-preserving rigid half-turn

r(x,y,t)=(x,−y,1−t).

It preserves each endpoint pair individually and exchanges the bottom and top endpoint within that pair. It does not exchange the two component labels. For an upward parametrization γ_i:[0,1]→C, define

(ργ)_i(s)=r(γ_i(1−s)).                            (2.1)

This again goes upward from (p_i,0) to (p_i,1), has the fixed standard collars, and satisfies ρ²=id. Ambient rotation and reversal of both component orientations preserve the sign of every crossing; hence pullback f↦f∘ρ preserves ordinary finite-type order.

This is Duzhin–Karev's simultaneous orientation reversal after restoring the standard long ends. Their v5 source fixes labeled long asymptotes γ_i(t)=(i,0,t), defines L′ by reversing all component orientations, and permits orientation-preserving Euclidean movement of the ambient oriented three-space. The rigid motion restoring these reversed asymptotes while retaining each label is (x,y,z)↦(x,−y,−z), which becomes r after centering/rescaling the string-link interval. A half-turn in the diagram plane that interchanges the two horizontal positions would be a different operation and is not used. Their chord-diagram involution likewise reverses the vertical order while keeping each support strand in its original position. Thus (2.1) agrees with the involution in the primary orientation-detection theorem, with no label permutation, pure-braid factor, or unspecified outside motion.

## 3. Every free-exterior two-string link has this exact reversal symmetry

This section gives the marked argument. Merely having an unspecified strong inversion as an unmarked tangle would not suffice.

### 3.1 The exterior is a genus-two handlebody

For L∈F_2 remove disjoint open regular neighborhoods of the two proper arcs. The resulting compact exterior H is connected and its boundary is the outer four-holed sphere together with two tube annuli. Its boundary is a closed genus-two surface. The open complement and compact exterior have the same fundamental group.

A free ball tangle has handlebody exterior; this equivalence is explicitly part of Nogueira's free-tangle definition [N], Appendix §4. It can also be seen from irreducibility and the Loop Theorem. An embedded sphere in the arc exterior bounds a ball inside C, disjoint from the proper arcs because each arc runs to ∂C. Thus the exterior is irreducible. A positive-genus closed boundary surface group cannot inject into a free group, whose subgroups are free. The Loop Theorem supplies a compressing disk; the smooth Schoenflies and Loop Theorem inputs are recorded in [3M]. Cutting along such disks retains free groups by the free-product decomposition, and repeating gives irreducible pieces with spherical boundary, hence balls. Reattaching the one-handles reconstructs a handlebody. In the present case its boundary genus is two.

In particular no full-group freeness conclusion is inferred only from nilpotent quotients or from the bottom meridians being a basis.

### 3.2 Construct the required boundary map before extending it

Let L^0 be the standard trivial two-string link and H^0 its exterior, using the same endpoint disks on ∂C as for L. The outer four-holed sphere S is literally the same marked subsurface of ∂C in the two constructions. Write A_i^0 and A_i for the lateral tube annuli in ∂H^0 and ∂H.

Choose tubular coordinates f_i:D²_ε×[0,1]→N(L_i), with f_i(0,s)=γ_i(s), and standard prescribed coordinates on the two endpoint disks. The normal bundle along an interval is trivial, so these prescribed end coordinates extend; different total tube twists simply give different permissible choices of f_i. Use the corresponding standard coordinates f_i^0 for L^0. Define an orientation-preserving boundary identification

F:∂H^0→∂H

as the identity on S and as f_i∘(f_i^0)^{-1} on each lateral annulus. The end restrictions agree pointwise, and product collars allow smoothing at the joins. We do not assume F extends over the two handlebodies.

The rigid r preserves L^0 and H^0. Its restriction τ_0 to ∂H^0 is the genus-two hyperelliptic involution: it is orientation preserving and has six fixed points, two on the outer sphere piece and two on each lateral annulus. Define the exact target boundary involution

τ=F τ_0 F^{-1}.                                  (3.1)

On S, τ equals the originally fixed r pointwise. On A_i, its formula in the chosen tube coordinates is

(z,s)↦(conjugate(z),1−s), |z|=ε.                 (3.2)

Thus it reverses each arc's longitudinal direction and keeps its component label. Any twists in the chosen tube coordinates occur only by this explicit conjugation; they do not alter the outer four-holed-sphere map or produce an unknown boundary factor.

### 3.3 Extend over H, matching the entire boundary map

For a genus-two handlebody, the hyperelliptic mapping class on its closed boundary extends over the handlebody. Moreover every orientation-preserving conjugate of that boundary mapping class is the same hyperelliptic mapping class. One formulation is centrality in the genus-two surface mapping class group; another is that the hyperelliptic involution preserves the unoriented isotopy class of every simple closed boundary curve, including every meridian in a complete disk system. The downloaded primary source [BM] states both extension and centrality; [HS] supplies a supplementary simple-curve formulation. Full details and source inspection are in MARKED_FREE_REVERSAL_LEMMA.md.

Apply this to τ. Its mapping class extends over H, although the earlier identification F need not extend. If an initial extension has boundary value only isotopic to τ, correct it using the boundary isotopy extended across a collar. We thereby obtain an orientation-preserving diffeomorphism h_H:H→H whose boundary value is exactly τ, not merely the same unmarked mapping class. Choose its collar germ to be the required product germ for gluing to the tube extensions.

This collar correction is decisive: without exact agreement on S, composing later with r might leave a nontrivial four-punctured-sphere mapping class or pure-braid factor. Here it leaves neither.

### 3.4 Fill the tubes and remove the outside half-turn

On the entire ith tube extend (3.2) by

h_i=f_i ◦ ((z,s)↦(conjugate(z),1−s)) ◦ f_i^{-1}.

Reflection of the disk and reversal of the interval together preserve the three-dimensional orientation. This map preserves the ith arc setwise and reverses its direction. It agrees with h_H on the lateral annulus, and on the endpoint disks it agrees with the original r because the end coordinates were fixed beforehand. Product collars make the glued map smooth.

Gluing h_H and the two h_i gives an orientation-preserving diffeomorphism h:C→C with

h(L_i)=L_i for each label i, reversing its parametrized direction,
and h|_{∂C}=r|_{∂C} exactly.

Now g=r∘h is an orientation-preserving diffeomorphism of C fixed pointwise on its entire boundary. It carries each upward labeled arc of L to the corresponding upward labeled arc of ρL, up to a monotone reparametrization of that interval.

The smooth diffeomorphism group of the three-ball relative to its boundary is path connected (indeed contractible), as supplied by the ball form of the Smale-conjecture theorem [Ha]. Thus g is smoothly isotopic to the identity relative to ∂C. The resulting isotopy carries L to ρL in exactly the required ordered fixed-endpoint category. No outside-ball modification is required; if one uses long closures, extending g by the identity outside C gives the same fixed-at-infinity isotopy.

Therefore

L∈F_2  ⇒  ρL=L.                                 (3.3)

The proof uses the special genus-two hyperelliptic property. It is not asserted for arbitrary genus k or arbitrary string links.

## 4. The ordinary rational order-seven input

Use Duzhin–Karev [DK], arXiv:math/0507015v5, dated 25 July 2005, rather than the initially retained v1. Theorem on p.2 states the existence of an order-at-most-seven orientation-sensitive invariant of two-component long links. Section 2 expressly allows coefficient field Q. The framed proof is in Sections 3 and 5, and **Section 6, p.9, explicitly supplies the ordinary unframed conclusion** using the one-term/framing-independence quotient. Thus no omitted framing generators or framed-only theorem is being substituted.

For a sharper nonzero-symbol specification, let H be the connected seven-wheel Jacobi diagram of Proposition 2: its seven external legs have cyclic colors 1121222, with the displayed vertex orientations. It has seven trivalent and seven univalent vertices, hence degree seven. Lemma 4 identifies simultaneous reversal in the colored-Jacobi model with multiplication by (−1)^(number of legs), so τ(H)=−H. Proposition 2 proves H≠0, and Lemma 8/Section 6 proves that its symmetrization remains nonzero in the ordinary unframed diagram quotient. H is connected and is not either of the deleted single-color struts.

The fundamental theorem of finite-type invariants, in the rational form used in [DK] Section 2, says that every rational ordinary weight system integrates to a rational finite-type invariant of that order. Since the unframed class χ(H) is nonzero, choose a rational weight system W with W(χ(H))=1, and replace W by

W^−=(W−W∘τ)/2.

Then W^−(χ(H))=1. Choose a rational ordinary f∈V_7(2) with top symbol W^−. Finally set

v(L)=(f(L)−f(ρL))/2.                             (4.1)

This is a rational ordinary finite-type invariant of order at most seven. Its degree-seven symbol is W^−, nonzero on χ(H), so v has exact order seven and is not the zero function. Formula (4.1) and the rational weight-system selection specify the existence construction; no numerical nonsingular-link value or canonical choice of integration is claimed.

## 5. Universal vanishing and nontriviality

For every L∈F_2, equation (3.3) gives f(L)=f(ρL), so v(L)=0. Therefore v∈N_7(2). Its nonzero degree-seven symbol proves v≠0 on the full string-link space. This proves the theorem.

The universal quantifier comes from the marked handlebody argument, not from tests on finitely many free diagrams. Conversely, the nonzero conclusion comes from the ordinary rational symbol and integration theorem, not from treating a finite set of zero values as a proof of vanishing. These are logically separate obligations.

Since V_7(2)⊆V_n(2) for n≥7, the same v witnesses N_n(2)≠0 for every n≥7. This does not imply that all nonzero members of N_n are reversal-odd or give a classification of N_n. It also does not resolve the spanning question at order seven; the negative spanning result at (2,2) remains the already accepted separate answer.

## 6. Reproducible rational certificate for the nonzero symbol

This check supplements the cited Proposition 2. It does not replace the deframing, integration, or geometry arguments.

For two N×N matrices X,Y and a word w in colors 1,2, write T_w for the trace of the ordered product, assigning X to color 1 and Y to color 2; T_empty=N. Expanding the seven-wheel weight as the trace of a product of adjoint maps, with ad_X=L_X−R_X, gives 2^7=128 terms. The left factors retain their order, the right factors reverse theirs, and each right factor contributes a minus sign. Grouping traces cyclically gives

P(X,Y)=N(T_1121222−T_1122212)
       +3 T_2 (T_112212−T_112122).                (6.1)

The script checks this complete 128-term expansion, independently of simply trusting the printed polynomial. It agrees with [DK]'s formula for the wheel up to the fixed global vertex-orientation convention.

Take N=4 and the integer matrices

X = [[0,1,1,1], [1,0,0,0], [0,−1,0,0], [−1,−1,−1,1]],
Y = [[0,0,−1,1], [−1,−1,1,1], [−1,0,0,0], [0,0,−1,−1]].

Exact integer multiplication gives

T_2=−2,
T_1121222=38, T_1122212=20,
T_112212=−12, T_112122=−23.

Thus P(X,Y)=4·18+3·(−2)·11=6. Reversing the color word gives −6, and the antisymmetric difference gives 12. In particular this Lie weight is genuinely nonzero already over Q, at finite N=4; no appeal to a merely formal large-N independence claim is necessary for the numeric certificate.

A supplementary script, not included in this theoretical edition, contains this calculation and explicit guards effective under python -O. Its limits were stated in its separate result metadata. The displayed calculation above was already part of the audited manuscript; it is retained as supplementary mathematical exposition, not newly transcribed executable code or a claim of a rerun in this edition. The source's unframed survival remains a separately cited theorem.

## 7. Primary references and source handling

[DK] S. V. Duzhin and M. V. Karev, *Detecting the orientation of long links by finite type invariants*, arXiv:math/0507015v5, 25 July 2005. https://arxiv.org/pdf/math/0507015v5 . Retained PDF: 195094 bytes, SHA256 f92b93fe6cfe04f1720c8ee080f19af2103ced2ab4fcc616c7c95ed3df6dfae3. Relevant locations: definitions p.1; theorem and Q-valued/ordinary setup p.2; exact reversal on diagrams pp.2–3; Lemma 4 p.6; Proposition 2 and complete wheel drawing p.8; deframing Section 6/Lemma 8 p.9. Pages 1–3 and 8–9 were rendered and the relevant images inspected. The v1 lacks the explicit Section 6 and is not the controlling version here.

[N] J. M. Nogueira, *Knot complements with meridional essential surfaces of arbitrarily high genus*, Coimbra preprint 14–09, Appendix §4, pp.14–15. https://www.mat.uc.pt/preprints/ps/p1409.pdf . Its exact free-group/handlebody equivalence is read from the previously retained source without changing that file.

[HS] A. Haas and P. Susskind, *The geometry of the hyperelliptic involution in genus two*, Proceedings of the American Mathematical Society 105 (1989), 159–165, Theorem 1. DOI: https://doi.org/10.1090/S0002-9939-1989-0930247-2 . This supplementary statement was inspected in indexed primary-paper text. Publisher retrieval returned 403 and the mirror returned 202 with no bytes; no local PDF hash is claimed. The proof already has the downloaded sufficient input [BM].

[BM] A. Bruno and M. Mecchia, *On quotient orbifolds of hyperbolic 3-manifolds of genus two*, Rendiconti dell'Istituto di Matematica dell'Università di Trieste 46 (2014), relevant p.272. https://rendiconti.dmi.units.it/volumi/46/014.pdf . The hyperelliptic extension/centrality input is independently checked in the geometric lemma. Retained PDF: 780746 bytes, SHA256 b4c1c4a76c3028a54ba1223536ec7b1c1820474e6584d622161bfba743c12f0c.

[3M] A. Hatcher, *Notes on Basic 3-Manifold Topology*, Theorem 1.1 p.1 and Theorem 3.1 p.56. Author PDF: https://pi.math.cornell.edu/~hatcher/3M/3Mfds.pdf . Retained PDF: 702282 bytes, SHA256 c8add1a8633f36cb50de313f8f340a3f2b63b5548077d6e30f9c51a073398ff6.

[Ha] A. E. Hatcher, *A proof of the Smale Conjecture, Diff(S³) ≃ O(4)*, Annals of Mathematics 117 (1983), 553–607, Appendix p.604, statement (1). Author PDF: https://pi.math.cornell.edu/~hatcher/Papers/SmaleConjecture.pdf . Retained PDF: 14720341 bytes, SHA256 d85554b61d9315081c51e8cf0438d5674c41507e2ac634dd465e029753333344. The relative-ball assertion was visually checked on PDF p.52 because the extracted text has defective encoding.

All copied PDFs, extracted text, and rendered pages remain private evidence. The authored mathematical argument and public bibliographic/hash metadata are separate. No copied third-party artwork is proposed for publication.

## 8. Completion and residual scope

The new mechanism is genus-two reversal symmetry combined with an orientation-odd unframed symbol. It is distinct from the order-two finite-basis evaluation approaches. This is approach 3, with two approaches unspent.

The target of this route is the affirmative nontriviality theorem at k=2,n=7 and its immediate n≥7 consequence. Proof search stops at that scope and requests independent audit. No claim is made that orders three through six vanish, that order seven is the first nontrivial N_n, or that the construction covers k≥3. No accepted predecessor file, queue, remote branch, or publication state is changed.
