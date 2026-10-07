# Independent arithmetic assembly audit

Checkpoint: 2026-10-07 05:39 UTC (2026-10-06 local). Reviewer: independent `/root/priority`, reassigned from the priority audit. Primary source read only: `/Users/alec/Desktop/math/preprints/A-pointwise-2-converse-for-elliptic-curves-with-rational-two-torsion-September-24-2026/build`, HEAD verified `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. No source edits, Git mutations, or external communication. This report supplements `two_converse_adversary.md`; it does not supersede other independent audits.

## Decision and scope

**The local arithmetic duality faces and the identification of the paired generic functional can be reconstructed. The final all-split full-rational-two-torsion assembly follows conditionally from the stated coefficient and height interfaces. I have not established a false lemma in this branch.** This is a positive verification of the displayed constructions below, rather than an inference from failure to find a counterexample.

It does **not** certify the whole pointwise 2-converse, H10(Q), or the geometric follow-on. The weighted coefficient construction, moving odd normalization, finite-stage ring-character/evaluation package, nonvanishing inputs, uniform height comparison, and group-ring family clearing have separate responsibilities. The exact additional trace premise used in the deeper split witness is recorded in section 6. The remaining substantive cross-report premise in this review is the initial weighted modular form and its level/character properties, not an absent derivative-plane nullhomotopy. The trace/module calculation and the applicable primary local compatibility theorem are reconstructed below.

Assigned-subtask audit coverage estimate: **90%**. The explicit faces, generic functional, specialization mechanism, and finite all-split packet/address argument are reconstructed. This percentage is audit coverage, not a probability that the research theorem is true.

Source coverage in this turn: `ring-determinants.tex` approximately lines 920–1769, with the necessary local/paired diagrams at lines 65–170 and 370–482; `ring-limits.tex` Kummer/global-duality construction lines 288–405; `pointwise.tex` entire final full-two-torsion assembly and deeper split witness, approximately lines 530–1058; `graphs.tex` address theorem, programs, and full two-symbol proof (approximately lines 190–240 and 459–649). Earlier turn read the rest of the ring limits/determinants.

## 1. What the finite local face actually is

Use cohomological grading. At a derivative prime of K, at a retained quotient A killed by 2^a, choose rational inert Frobenius gamma so gamma^2 acts trivially on the coefficient representation and q = ell^2 is 1 modulo 2^(a+1). This is stronger than merely making q = 1 modulo 2^a.

The tame presentation is

    phi sigma phi^(-1) sigma^(-q) = 1.

With trivial coefficient action at this quotient, its Fox complex has ranks 1,2,1, differentials d^0 = 0 and d^1 = (0,1-q). Both differentials vanish. Its cup diagonal has no pure finite term; its pure tame term is ±binom(q,2), which also vanishes modulo 2^a under the extra congruence. The mixed terms are units. This identifies an actual finite split local model

    L = D^0 ⊕ (F ⊕ S)[-1] ⊕ D^2[-2],       d_L = 0.

The coefficient action is indeed trivial here: the squared rational Frobenius at an inert prime is trivial on an anticyclotomic ring-class character; quadratic group variables have exponent two; precision on T imposes the remaining triviality. At the good derivative prime inertia is trivial. Thus nilpotent t and quadratic coefficient variables do not invalidate the coefficientwise calculation.

The scalar square vanishing has an independent local explanation: q ≡ 1 modulo 2^(a+1) puts the 2^(a+1)-st roots of unity in the local field; -1 is then a 2^a-th power and (x,x) = (x,-1) makes scalar self-cups vanish. This rules out the characteristic-two mistake of deducing vanishing only from skew symmetry.

The four conditions are literally the subcomplexes

    U_str = D^0,
    U_F   = D^0 ⊕ F[-1],
    U_S   = D^0 ⊕ S[-1],
    U_rel = D^0 ⊕ (F ⊕ S)[-1].

They all contain local H^0 and omit H^2. Consequently their pure-plane restrictions to the invariant target A[-2] are **zero chain maps**: only a product of two degree-one terms could contribute, and those terms vanish on either plane. A degree-zero term cannot pair with a degree-two term inside these conditions, because that latter term is absent.

Conjugate Weil transport gives the mixed pairing beta(x,y) = epsilon <x,Jy>, with epsilon a scalar unit. Since det(J) = -1, the matrix WJ for an alternating Weil matrix W is symmetric; its perfectness follows from perfectness of W and invertibility of J. Therefore U_F and U_S are exact self-orthogonal complements; U_str and U_rel are mutually complementary. The zero isotropy homotopies on the two planes restrict to the same zero homotopy on U_str.

**This reconstructs the extra arithmetic compatibility needed at 2. It is not just a cohomological dimension calculation.** The conditions are truncated conditions, not the full local complex, and confusing those would break the argument.

## 2. A checkable Selmer-cone and degree-two face construction

Fix a finite set of derivative primes, use one common global cochain complex G, common ambient local complexes L_v, and the four inclusions above at each such prime. Keep the old local conditions fixed. For each face delta define

    C_delta^n = G^n ⊕ U_delta^n ⊕ L^(n-1),
    d(g,u,l) = (d_G g, d_U u, res(g) - i(u) - d_L l).

This is the source's Selmer cone in explicit coordinates. An inclusion of conditions defines the face map by the identity on g and l and by the displayed inclusion on u. Every two-face square commutes term by term, including its degree-two component. At a derivative prime d_L = 0, a degree-one cycle therefore has res(g^1) = i(u^1); its finite/singular coordinates are the two components of this same localization. The strict face sets both components to zero. The finite and singular faces set respectively the singular and finite component to zero.

The quotients for the inclusions are the literal modules F[-1] or S[-1]. Thus the localization triangles and their connecting maps can all be taken in this same cone diagram. The identities supplied by transferred derivative classes are represented by degree-zero local boundary witnesses; retaining those witnesses preserves their identities as degree-two cycle equations, not just their H^1 classes.

For several derivative primes take the product of these four-condition diagrams. There is no new obstruction on a two-face: the underlying global/local maps are unchanged, the inclusions commute, and every new derivative-place isotropy homotopy is zero. On unchanged places use the **same** old homotopy, not a newly chosen equivalent map.

The old Kummer condition is U = M[-1], M = E(F)^wedge_2. Its isotropy map U tensor^L U → Z_2[-2] is determined by the ordinary homomorphism M tensor M → Z_2, which vanishes by finite local Kummer orthogonality. To see that no omitted Tor map produces a second choice, put D = M tensor^L M, with cohomology only in degrees -1,0. Hom(D,Z_2) is determined by H^0(D) → Z_2; Hom(D,Z_2[-1]) = 0. The latter follows from the truncation triangle and vanishing of negative Ext. Thus an integral free-model nullhomotopy exists, and any two choices agree in the required derived homotopy class. Choose it once and base-change it to the finite coefficient rings. This also retains finite H^0 Kummer invariants under derived reduction.

The specific functoriality conditions are substantive: the pairing maps use local nullhomotopies, and change of maps can require second-order homotopies. Here at derivative places all restrictions are literally zero, so these higher compatibility maps can be zero. At old places both sides are identical and the same old homotopy is used, so their difference is zero as well. If target contraction changes a representative, transport the whole pairing diagram through that contraction and retain the induced homotopies; do not independently select an isomorphic old complex. This is precisely the construction explicitly demanded at `ring-determinants.tex` lines approximately 386–436 and in `rl:limit-evaluation-package`.

Primary check: [Nekovar, Selmer complexes](https://www.numdam.org/item/AST_2006__310__R1_0.pdf), printed pp.137–145, PDF pages146–154, definitions6.2.1/6.2.7, theorem6.3.4, and functoriality6.4.1–6.4.4. The theorem requires a perfect coefficient duality, bounded finite/cofinite or dualizing-complex hypotheses, specified orthogonality homotopies, and vanishing local error complexes. It does not manufacture those data. The finite Artin rings here are Frobenius/Gorenstein (the coefficient complete intersections and finite group algebra extension); their free coefficient representation has the perfect conjugate-Weil pairing. K is imaginary quadratic, so the real-place obstruction at p=2 does not occur. The constructed local complements remove the error complexes. The displayed face maps meet the functorial homotopy conditions.

This is an independent reconstruction of the face mechanism. It still uses the separately established finite target-model/limit package to retain the finite diagrams. No theorem about duality alone proves that package.

## 3. Why the generic functional is the same at both localizations

Fix one switched index set I. Let C_I be its relaxed complex and C_I^perp its orthogonal complex. At active primes and the auxiliary r the full local complexes become acyclic over the relevant height-one rings. At switched primes the plane condition already equals its orthogonal condition; at 2N the Kummer condition does too.

The natural map j_I : C_I^perp → C_I consequently becomes a quasi-isomorphism. In the derived category its inverse is unique. Any explicit local contracting homotopy represents this inverse; two choices produce homotopic morphisms. Let D_I be the retained global duality map

    C_I^perp → RHom(C_I, R)[-3].

Then the functional attached to the point class is

    lambda_I = H^1(D_I j_I^(-1))([P_I]) ∈ H^2(C_I)^*.

This formula defines one generic functional. Constructing integral contractions over O and constructing contractions over Lambda_(t) yield representatives of this same fraction-field morphism. There is no assertion that a single O-cochain is integral at all primes. Nor are functionals for distinct I asserted to be identical; they come from the same duality diagram applied to their respective classes.

At the central height-one ring Lambda_(t), 2 is a unit. At an active ramified prime the inertia differential -2 contracts the local complex. At the auxiliary r the trace condition makes the central Frobenius determinant nonzero, so it contracts there too. Therefore the latter representative specializes to ordinary rational Kummer duality. Old Kummer homotopies are unchanged throughout. This justifies the representative choice in `rd:central-formula`, rather than assuming arbitrary O-cochains specialize regularly.

The finite central trace identity is also a boundary identity in the cone:

    z_i(0) - L m_i j_i(b_h) = d v_i,
    m_i = a_(r_i) - 2 chi_h(r_i).

Each retained local condition induces H^0 isomorphisms and H^1 injections, so the cone H^1 injects into global H^1. Kummer naturality plus the point distribution identity therefore gives such a v_i. The source retains v_i, comparison maps, and localization triangles in the same target diagram. The uniform finite bound v_2(m_i) ≤ c_E makes the ultrafilter limit m nonzero; this supplies a nonzero central point when the product has a simple zero.

## 4. Specialization and central determinant accounting

The derived specialization argument is sound under its explicitly stated constant rational dimensions. Over the DVR Lambda_(t), a nonunit pivot in a finite free model produces an extra central class in both adjacent degrees. Equal generic and central dimensions (one in degrees1,2 and zero elsewhere) exclude such pivots. The determinant line base-changes termwise; integral torsion in the entire central complex must still be included. Replacing H^1 by its naive quotient modulo t would be invalid, and the source expressly avoids it.

For the inverse determinant, an elementary divisor with cokernel in degree i contributes (-1)^(i+1) times its length. Thus degree-two finite Sha contributes negatively, while the point and its paired functional each contribute their free-line index. Relaxing an active good odd ramified quadratic place contributes exactly its H^2 length t_p; both split places over K give 2t_p. With full rational two-torsion t_p = 2, giving precisely 4 omega(h), with no hidden error per active prime.

The quadratic Sha comparison correctly needs an isogeny **identity**, not just exponent-two kernels. [Milne, Arithmetic Duality Theorems](https://www.jmilne.org/math/Books/ADTnot.pdf), I theorem7.3 proof, printed pp.97–100, establishes the ratio of local measures, global indices, and dual Sha kernels. Its derivation uses finite Sha and characteristic prime to the isogeny degree; here characteristic zero and finiteness at nonzero simple-zero vertices meet those conditions. The comparison identity is available without assuming the BSD numerical formula. At split primes the component factors cancel; the k-support can enter the error when omega(k) is bounded. I have not independently reproved every Neron model comparison at 2; that is an earlier height/local-factor audit dependence.

The fixed-base case only needs the conductor-one split Gross–Zagier theorem: [Cai–Shu–Tian, theorem1.1](https://msp.org/ant/2014/8-10/ant-v8-n10-p05-p.pdf), pp.2524–2525. Its conditions are conductor coprime to N, no inert prime dividing N, splitting if its square divides N, and a condition at common N/discriminant primes. Here c=1, k is coprime to 2N and square at its primes, so every N-prime splits and the common-prime condition is empty. The formula's scalar is nonzero. Thus vanishing of the fixed-base derivative implies the primitive Heegner sum is torsion, as used in `rd:missing-vertex`.

[Howard, proposition1.7.4](https://arxiv.org/pdf/1202.6340v1), p.21, supplies the familiar local derivative formula. His global theorem requires odd p and strong residual-image hypotheses; those do not apply here. The source explicitly redoes the local calculation and the p=2 isotropy issue. I checked that no downstream appeal here imports Howard's odd-p global theorem at 2.

## 5. Full-rational-two-torsion split witness: coefficient arithmetic

The relevant E_l has full rational two-torsion, so the pointwise argument uses the special all-K-split branch, not the quadratic residual good-simple branch.

Fix a nonvanishing negative even unit k before b; choose its fresh ramification away from the old support and Q(E[8]). For the even form of E^(k), normalized by a(1)=1, the exact coefficient ratio gives v(a(D)) ≥ omega(D) on the allowed filter. If the ordinary test has no nonempty all-K-split unit, rationality of the normalized phase-free coefficient makes its valuation an integer, hence

    v(a(D)) ≥ omega(D)+1

on every nonempty all-K-split allowed D. This use of an exact ratio, rather than subtracting unrelated O(1) estimates, is necessary.

Assume the trace/module premise described in section6. For a good split p, the divided trace test compares the zero coefficient at the matched product pp' with

    H_{p}[p^3] = (a_p-1)(a_p-p-1)/4.

The determinant contribution cancels with the unary term. Full rational two-torsion makes a_p even, so a_p-1 is odd. Zero modulo2 implies a_p ≡ p+1 modulo8. The matched fresh p' has all the same support squareclasses, so pp' lies on the total rational filter even if p alone does not. This repairs a tempting but incorrect proof requiring every individual p on the filter.

The extra /4 division is then checkable at every shell J r m^2:

* If r is nontrivial and D=(U/J)r is all split, its coefficient has valuation at least omega(r)+1 ≥2. If D has inert factors, r has at least two, because its total K-character is trivial and U is all split; again the valuation is at least2.
* If r=1 and J is proper, the common scalar 2^(-|U|+|J|) a(U/J) is even. Recurrence differences divided once by2 are integral and agree with their leading value modulo2, even when that value is zero. Multiplication by odd m preserves the congruence; the common even scalar supplies the second factor2 for cancellation with the unary shell.
* If J=U, D=1. The congruence a_p ≡ p+1 modulo8 makes b_s ≡ p^s modulo8 at a prime in U. Thus (b_(s+1)-b_s)/2 ≡ ((a_p-2)/2)p^s modulo4. Ordinary square-index factors outside U agree modulo4, giving the remaining unary cancellation.

Hence H_tilde_U = (B_U - sum_J B_U[J]Theta_J)/4 is integral; no division by a possibly zero leading multiplier was made. The diamond correction has B_U[J]/2 integral for proper subsets, and fresh trace tests kill its unary terms.

Two fresh K-split traces raise the squarefree valuation enough to vanish after this division, on the whole reduced trace orbit. Together with the trace identities this yields t(gu^2)=t(g) for g,u in G_K, and therefore the elementary K-label test. A single fresh split trace reads the deeper bit 2^(-omega(D)-1)a(D) mod2. The same local inertia identity gives its forest contraction rule for nonempty outputs.

For its nonempty witness, fresh ramification ensures K is not contained in Q(E[8]). Chebotarev gives a good p inert in K and identity on E[8]. Then p≡1 modulo8, a_p(E^(k))≡-2 modulo8, so

    (a_p(E^(k)) - 1 - p)/4 ≡ 1 modulo2.

This is the coefficient1 test of t(u)^2 on H_tilde_empty; the coefficient at1 itself is zero. In characteristic2, t(u^2)=t(u)^2. Now u^2 belongs to G_K and is trivial on every rational quadratic character. A fresh prime realizing this finite test is split and on the rational filter, and yields a nonempty deeper witness. This is a constructive witness argument, not an assumed nonempty minimum.

## 6. Exact coefficient interface dependency

The paragraph deriving a_p ≡ p+1 modulo8 needs, on the raised conductor-one portion,

    U_p^2 t(phi_p) = U_p^3 + d(phi_p) U_p.

On a principal-series eigensystem this follows directly from U_p eigenvalue lambda, t(phi_p)=lambda+mu, and d(phi_p)=lambda mu. On the unraised unary term the ordinary good-prime coefficient formula gives the same coefficient equality at p^2. No nilpotent old multiplicity space is silently discarded in the latter calculation.

To apply this to the actual theta-multiplied integral module one also needs the source's asserted level-exponent-one and primitive ramified determinant property; local modular/Galois compatibility; preservation of the integral Fourier lattice by trace limits; and finite Chebotarev approximation respecting all support tests. `co:traces` lines793–850 and `co:inertia` lines852–886 explicitly construct these, rather than citing pointwise interpolation as a black box. The residual trace identities then follow from the characteristic-zero matrix identity and the annihilation of unary corrections by fresh traces.

Primary condition check: [Carayol, theorem(A)](https://www.numdam.org/item/ASENS_1986_4_19_3_409_0.pdf), printed pp.410–411, identifies the local Galois representation with the local modular parameter at primes of residue characteristic different from the coefficient prime. The forms here have weight2 over F=Q; its additional hypothesis for even-degree totally real F is irrelevant. The raised prime p is odd while the coefficient prime is2. The paper uses geometric Frobenius; the source explicitly converts to its arithmetic convention. Thus this application does not impose an ordinary hypothesis or an odd coefficient prime. Eisenstein constituents are handled by their two characters directly.

I reconstructed the principal-series calculation, integral trace-lattice preservation argument, and complete coefficient consequences in section5, and checked the cited primary local compatibility conditions. I did **not** independently reconstruct the full modular transformation/level argument for the initial weighted theta source. That is the exact substantive cross-report dependence: it must give level exponent at most1 and primitive ramified determinant at each raised prime. It is neither a counterexample nor evidence that the source lacks a proof. The weighted-coefficient review must cover it before the deeper split witness is promoted to unconditional validation.

## 7. Final common packets and simultaneous addressing

Here is a direct reconstruction for full rational two-torsion, assuming the two symbol interfaces and uniform unit bounds have been established.

Let V_0 be the even elementary label space over the fixed imaginary K, with conjugation c. A rational total zero implies that the oriented total annihilates every c-invariant character: such a character extends to G_Q by giving complex conjugation value zero, and remains unramified outside the fixed support. Linear algebra gives

    (ker(1+c^*))^ann = im(1+c).

Thus the oriented total is in (1+c)V_0. Flipping one orientation changes label v to cv, hence changes total by (1+c)v. A reserved copy of every needed label can implement any change in this image, without changing its rational norm label.

Fix minimum nonempty witnesses for the even split test and the intrinsic odd test. The fresh ramified prime of K lies outside the old odd label extension's ramification set (once moving ell avoids k); therefore K has trivial intersection with its normal closure. Every old odd seed label has a lift compatible with splitting in K. Every even label has its own compatible lift to the common alphabet. No arbitrary pair of independently specified projections is presumed to lift. Take enough compatible lifts for each projection separately and duplicate every full label. Each packet now has rational total zero and enough supply for both certificates.

For the even certificate, retain r-1 seed anchors. Use reserved orientation flips to change the full oriented total to the seed total (their difference is in im(1+c)). Merge the remaining nonempty cluster into the last seed position. Its label is the last seed label. Minimality of the nonempty witness makes the resulting value independent of mutual edges: any edge difference contracts to a smaller nonempty configuration and hence vanishes. For r=1 there are no retained anchors or mutual edges, so the same construction works.

For the odd certificate, use the rational projection; retain all but the final intrinsic seed label and merge the rest. Rational total zero forces the final label. The even orientation corrections do not alter those rational labels. These are separate certificates that the **two terminal polynomials are nonzero**; they do not require a common unit evaluation at this stage.

Put a full packet at each nonzero linear activation form lambda on F_2^b. Each nonzero address activates at least one whole packet, so the above certificates apply to its total active collection. Duplication ensures total rational zero at every address. In particular it satisfies all added fixed k-support tests.

The two-symbol address lemma is sufficient even when the two original terminal polynomials never share a unit. To check this rather than assume it, take a coefficient1 monomial of the product of their top homogeneous parts in the **ordinary polynomial ring**, before Boolean reduction. An exponent2 variable requires a singular program that differentiates both factors once. An exponent1 variable requires a nonsingular program with a binary parameter. In the sum over all those parameters, the minimum contraction-degree budget equals the sum of both polynomial degrees at all addresses. Surviving terms must use each minimum exactly; higher forest coefficients die, and the allocation sum at each address is precisely that chosen coefficient1. Thus the sum of the product of all final evaluations is1, giving one common program choice. The source's z/z example correctly keeps z^2 in this allocation; Boolean multiplication beforehand would be false.

All primary auxiliaries are compatible identity labels in the common alphabet and can be split in K and neutral at the fixed tests. All have nonzero linear activations, so none appears at address0. The forest orientation changes are certificate choices with conjugations along a forest; they do not alter terminal data independently at different addresses.

Only after fixing b and these finite networks choose their maximum weight W_b and the required precision. A finite intersection of ultrafilter-large table/precision sets gives one actual stage. There is no countable intersection over all weights and no one stage for all b. Fixing k before b keeps the genus/height/unit constants fixed, although the networks and stage can grow with b.

## 8. Return to E_l and final dependency boundary

At every nonzero address the common realization gives analytic order1 for E^(h) and order0 for E^(hk). The supplied odd/even unit bounds and the fixed-k height comparison give

    2 j_h(k) ≤ 4 omega(h) + C,

with C independent of b. Nonnegative finite Sha lengths then give the upper determinant bound needed for missing-vertex transfer. At zero the chosen companion has Selmer corank0 by the forward theorem, while the original has corank1; the degree-two restriction/product isogenies identify the corank over K with their sum. Thus the base over K has exactly the corank required by the missing-vertex theorem. No Mordell–Weil rank or finite-Selmer dimension is substituted for that corank.

For E_l: y^2=x(x-l)(x+3l), the separate elementary Selmer calculation dim_F2 Sel_2=3 and rational E_l[2] of dimension2 only imply Sel_(2^infty) corank≤1. Applying the validated even or odd converse would then give finite Sha[2^infty]. This final implication still depends on the entire pointwise converse, not just the local diagram and packet assembly checked here.

The family-clearing/Schur claim has a separate independent reviewer. I reread it, but have not counted it as a second complete independent construction of the actual universal complex. Likewise I do not certify the weighted theta comparison, nonvanishing constants, or uniform height normalization here. Subject to those precisely named premises and the retained finite target package, the local face and final full-two-torsion all-split assembly exhibit no remaining hidden nullhomotopy, common-evaluation, or limit-quantifier gap in this reconstruction.

## Research log

* 2026-10-07 05:39 UTC: checkpoint, HEAD reconfirmed; finite derivative cup/nullhomotopy and cone faces reconstructed. Coverage90% for this assigned audit. Decision: replace an undifferentiated “assembly unverified” flag by the explicit verified mechanism and remaining coefficient-module premise.
* Primary full text retrieved in memory without saving large PDFs: Nekovar printed pp.137–149 and local proposition5.2.4; Howard proposition1.7.4 and odd-p hypotheses; Milne I7.3 proof; published Cai–Shu–Tian theorem1.1; Carayol theorem(A) and its hypotheses. Author errata URL was discovered, but direct retrieval returned403; no claim of a full errata audit is made.
* No external individuals contacted. No original source changed. No unconditional research result promoted.

* Follow-up checkpoint: primary Carayol local compatibility read and conditions matched; assigned audit coverage raised to90%. Its odd raised-prime/2-adic coefficient condition is satisfied. Initial weighted modular transformation and level properties remain a named cross-report premise.
