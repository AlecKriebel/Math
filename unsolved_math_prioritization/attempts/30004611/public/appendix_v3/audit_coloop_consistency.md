# Independent adversarial audit of the coloop consistency calculation

14 October 2026 UTC. Row 1775 / 30004611, the same shared substantive pass 3. It independently reconstructs the particular candidate's algebra and sheaf cohomology, audits the author's written proof, and limits the source conclusion to the exact inspected preprint.

## 1. Verdict and frozen scope

**Mathematical acceptance in the stated scope.** The essential central arrangement

    A: x y z (x+y+z) w = 0 in K^4

is nonfree over every field K, while its actual geometric-inclusion lattice sheaf on all nonzero flats has zero cohomology in every positive degree. This is a counterexample to the unrestricted Corollary 1.6 printed in arXiv:2008.13700v3. The independently checked punctured-affine calculation also contradicts that version's Theorem 1.1 at n=2. No missing variance, removed-flat, essentiality, grading, local-freeness, or field hypothesis was found that avoids these conclusions for the literal v3 statements.

The precise audited artifact is `coloop_consistency_calculation.md`. The initial submitted artifact had 16,189 bytes and SHA-256 `ecca88f1ee1089702a1dfdbc30ae7a3d6ad1a8f38118503b329037df6165d254`. The auditor requested one explicit boundary qualification in Section 7: the general punctured-spectrum formula is for l>=2. That condition already holds throughout the source's setting and the four-dimensional counterexample. It is a wording hardening, not a repair of either substantive result. The accepted final artifact has 16,199 bytes and SHA-256 `3511bddcddc30d7cf3998a298ccca072c0de9a2ffbc8fdc5ddf5eb81e227bf62`. The original reviewed bytes are preserved unchanged in `adversarial_audit/coloop_consistency_calculation.initial_reviewed.md`.

The complete literal delta is: `For a polynomial ring S=K[u_1,...,u_l], the top cohomology of its` becomes `For a polynomial ring S=K[u_1,...,u_l] with l>=2, the top cohomology of its`. No other byte of the authored proof changed. The exact unified diff is retained as `adversarial_audit/precision_correction.diff`.

No conclusion about the published version of record is licensed by this audit. Its full text was unavailable to the separate source-version check and was not inspected here. The audit does not certify a repair of the source's general Kunneth theorem, solve its broad Problem 6.3, or assert novelty.

## 2. Independently reconstructed topology and full functor

Let B be the arrangement xyz(x+y+z) in K^3, let T=Kw, and let H=K^3 direct-sum 0. The five normals of A include the coordinate normals, so their common kernel is zero over every field. All flats of A have one of the two forms

    a_Y=Y direct-sum 0,    b_Y=Y direct-sum T,    Y in L(B).

Only a_0 is removed. In particular b_0=T is a nonzero flat of the full arrangement and must remain. Omitting it would change the source's object. The punctured poset has 23 flats and its strict-chain counts are 23,88,114,48. The four factor normals form the rank-three uniform matroid over every field: each three-by-three determinant is 1 or -1, which remains nonzero in characteristic two.

At a_Y, localization includes the lifted B_Y and H; at b_Y, it includes exactly the lifted B_Y. Expansion in w is valid coefficient by coefficient over an arbitrary field. It gives the full covariant functor decomposition

    D(a_Y) = (S tensor_R D(B_Y)) direct-sum wS partial_w,
    D(b_Y) = (S tensor_R D(B_Y)) direct-sum  S partial_w,

where R=K[x,y,z], S=R[w]. Every map is an actual inclusion in Der_K(S). Thus the tangent summand E has identical values and identity transitions on a_Y -> b_Y, while the normal-coefficient summand I has wS on the a-layer, S on the b-layer, and the inclusion wS -> S across layers. This checks the diagram, not just isomorphic isolated stalks.

There is no reversal between this functor and the source: for upper Alexandrov topology, U_X={Y:X subset Y}; a sheaf has F(U_X)=F(X), and X subset Y gives the map F(X)->F(Y). The increasing geometric-inclusion order used in the artifact is exactly this convention.

## 3. An independent acyclicity proof, and the author's contraction signs

The following derivation does not assume the earlier audit's acceptance or use a freeness theorem from the source.

Let U={X:T subset X}, with inclusion j:U->P. It is a principal open with minimum T. For every flat X, U_X intersect U has minimum c(X)=X+T, which is the flat b_Y when X is a_Y or b_Y. Thus, for every module sheaf G on U,

    (j_*G)(X)=Gamma(U_X intersect U,G)=G(c(X)).

Consequently j_* is exact in this situation: exactness is checked at each stalk, where it is simply evaluation at c(X). This is a special property of the present principal-open intersections; the proof does not assume that arbitrary open-inclusion direct images are exact. The inverse-image functor j^-1 is exact, so its right adjoint j_* preserves injectives. The identity Gamma(P,j_*G)=Gamma(U,G) therefore gives equality of derived global sections. Since U has a minimum, Gamma(U,G)=G(T) is exact. Hence j_*G is acyclic in every positive degree.

The explicit full-functor identity E(X)=E(c(X)) with identity vertical maps shows E=j_*(E|U), including all transition maps. Therefore E is acyclic, and its global sections are S tensor_R D(B).

For an independent proof that I is acyclic, let Q={X:X subset H}. This is a closed lower ideal with maximum H. There is an exact sequence of functors

    0 -> I -> S_P -> i_*(S/(w))_Q -> 0.

The last functor has S/(w) on Q and zero outside Q; the quotient map and zero maps are natural. Extension from this closed subset is exact, and its cohomology equals cohomology on Q. The constant functors on P and Q are acyclic because their order complexes have maxima and hence are cones. The induced map on global sections is the surjective quotient S->S/(w). The long exact sequence now gives Gamma(P,I)=wS and H^n(P,I)=0 for n>0. This constant-functor argument does not make the false claim that a maximum makes every sheaf acyclic.

Combining the direct summands proves the all-degree and all-field vanishing of D independently of the artifact's explicit homotopy.

The artifact's homotopy also checks correctly. For its prism K, in degree zero

    K(ds)(x)=s(c(x))-s(x).

In degree one, expanding dKf+Kdf on x<y gives f(c(x),c(y))-f(x,y); the intermediate terms cancel with the stated signs, using the identity coefficient identifications. The general cancellation is the same normalized prism identity. Prepending the minimum of U gives dh+hd=id-pi, so H=c^*h j^*-K has the claimed sign and contracts positive degrees. Both c_E and c_I in the artifact are increasing, idempotent, extensive maps with the stated principal-open images and identity vertical coefficient maps.

An additional exact-integer formal-chain check verifies the normalized prism identity on all 273 strict chains of P, separately for both closures: 546 identities pass. This checks signs and repeated-vertex normalization. Module-valued validity follows from the stipulated identity endpoint transitions and naturality, rather than from treating varying coefficient modules as constant.

## 4. Independent algebraic nonfreeness certificate

The author's proof killing z is correct: the three vectors (xy,-xy), (xt,0), (0,yt), where t=x+y+z, generate E_z and have exactly the relation (t,-y,x). Reduction modulo t and coprimality of x,y prove generation; coprimality of t with x,y gives the whole relation module. These arguments work without division by an integer, including in characteristics two and three.

For an independent reconstruction, use the map D(B)->R given by theta -> theta(t)/t. It is split by the Euler derivation epsilon because epsilon(t)=t in every characteristic. Its kernel consists of vectors

    (x a,y b,z c) with x a+y b+z c=0.

The syzygies of the regular sequence x,y,z are generated by (y,-x,0), (z,0,-x), (0,z,-y) with the one relation (z,-y,x). Multiplying coordinates by x,y,z identifies this syzygy module with the kernel above. This gives the same minimal-resolution shape as the author's different chosen splitting:

    0 -> R(-3) -> R(-1) direct-sum R(-2)^3 -> D(B) -> 0.

Polynomial extension to S and addition of w partial_w yields

    0 -> S(-3) -> S(-1)^2 direct-sum S(-2)^3 -> D(A) -> 0.

In the author's generators the only nonzero entries in the first map are t,-y,x, all in m=(x,y,z,w). Tensoring the presentation with S/m gives a five-dimensional quotient D(A)/mD(A). Meanwhile D(A) has rank four: it is contained in Der(S), and Q(A)Der(S) is contained in it. A free rank-four module localized at m has a four-dimensional residue quotient. The contradiction proves nonfreeness as an ordinary module, not merely failure of graded freeness. The nonzero Tor_1 with S/m also shows that the resolution does not split and has projective dimension exactly one.

At the retained flat T, D(A_T) is the extended nonfree factor plus S partial_w, so A is not locally free in the arrangement sense. Thus the older locally-free criterion is not contradicted. The missing local-freeness hypothesis is exactly what the inspected v3 corollary says can be removed.

## 5. Grading, endpoints, and source hypotheses

All maps in the lattice calculation preserve coefficient grading. Exactness and the contractions work in every graded piece and in the ungraded module category. Because the poset is finite, the cochain terms are finite products, and no infinite-product or completion convention changes the conclusion. Assigning the partial derivatives degree -1 just shifts all coefficient degrees uniformly. Neither that convention nor taking the degree-zero component can create the missing positive lattice cohomology.

The arrangement has ambient dimension four, so Corollary 1.6's test range is n=1,2. Both groups vanish. Its center is a_0=0, not the deletion-center line T. The source defines arrangements by linear hyperplanes, assumes essentiality, and imposes dimension at least two and an arbitrary ground field. No irreducibility assumption or standing local-freeness assumption appears in the inspected definitions and statement. The sentence preceding the corollary expressly says that the local-freeness requirement is superfluous.

The auditor independently read the retained extraction for the introduction, standing hypotheses, Alexandrov definitions, Definition 4.1, Proposition 4.5, and the uses in Propositions 5.3 and 5.4. The page images for pp. 4 and 14 were independently visually inspected. The exact retained PDF was rehashed: 254,251 bytes, SHA-256 `2a4309b567e5113b48124cc4f17feb1c051c4dbb8ffacebd23ed700fd587676b`. This is arXiv:2008.13700v3, revision 12 October 2021, https://arxiv.org/abs/2008.13700v3 .

## 6. The source-proof obstruction and explicit comparison failure

For l>=2, the coordinate principal-open cover of the punctured spectrum computes its top structure-sheaf cohomology as

    J=H_m^l(S)=S_(u_1...u_l) / sum_i S_(product_(j != i) u_j).

The final Cech differential has exactly those summand images. The retained v3 Proposition 4.5 visibly has only S in the denominator. The modules differ: J has basis the Laurent monomials with every exponent negative and becomes zero after inverting any one coordinate, while the printed quotient does not. The source's explicit S_f=S[1/f] notation leaves no alternative localization convention resolving this difference.

In J, the class (u_1...u_l)^-1 is nonzero and killed by each coordinate. Tensoring the Koszul resolution of K with J produces a nonzero top homology class, so Tor_l^S(K,J) is nonzero. For l>=2 this disproves the flat-dimension-at-most-one property used in the v3 Proposition 5.3 proof. Merely correcting the denominator therefore cannot preserve that proof's application of Lemma 2.9.

The artifact additionally computes the obstruction for this particular nonfree module. Change variables to x,y,t,w, an invertible linear coordinate change in every characteristic. Applying - tensor J to its minimal resolution gives

    Tor_1^S(D(A),J)= {v in J(-3): x v=y v=t v=0}.

The kernel is exactly the span of x^-1 y^-1 t^-1 w^-d for d>=1: multiplication by a coordinate is injective on monomials with that coordinate exponent less than -1 and kills those with exponent -1. The three annihilation conditions therefore force those first three exponents. In J(-3) the displayed vector has degree -d. Thus the graded S-module is K[w,w^-1]/K[w], with x,y,t acting by zero.

Applying H_m to the same resolution, and using H_m^i(S)=0 for i<4, identifies H_m^3(D(A)) with that identical kernel. The standard punctured-spectrum exact sequence gives

    H^2(Spec S minus {m}, D(A)-tilde)=K[w,w^-1]/K[w] != 0.

The lattice H^2 is zero by the independently proved vanishing above. The n=2 comparison in the literal v3 Theorem 1.1 is therefore false in this example, quite apart from the freeness corollary. The Tor_1 term that the v3 Proposition 5.4 proof removes by its incorrect quotient identification is concretely nonzero even though D(A) is torsion-free.

This verdict concerns these specific statements and uses. It is not an audit of every other lemma or theorem in the source, and does not supply a general corrected Kunneth theorem.

## 7. Independent finite controls

The auditor wrote a separate implementation, `adversarial_audit/check_minimal_cover.py`. It does not import the author's full-poset cochain code or use its E-plus-I splitting. It reconstructs all flats from the defining normal equations, finds the minimal nonzero flats, and uses their principal opens as a different Cech cover. Every intersection is the principal open of the join, so evaluation there computes its sections and has no higher cohomology. In coefficient degree zero, the derivation stalk is exactly the geometric flat, computed as a linear-equation kernel. Actual inclusion maps are reconstructed in the ambient vector space and checked. Every consecutive differential composite is checked to be zero.

All eight controls pass over Q, F_2, F_3, F_5, for the factor B and product A. The dimensions and ranks are identical across these fields:

- B: six minimal opens; cochain dimensions (6,33,56,45,18,3); differential ranks (6,26,30,15,3); cohomology dimensions (0,1,0,0,0,0).
- A: seven minimal opens; cochain dimensions (7,45,104,121,78,27,4); differential ranks (7,38,66,55,23,4); all cohomology dimensions zero.

Thus the independent code detects the factor's nonzero H^1 rather than automatically returning vanishing, and observes its disappearance after adding the coloop. This is a bounded control in degree zero; the structural arguments prove the all-field, all-degree result. The author's separate 20 controls were read but are not substituted for the audit's proof or independent computation.

Independent control pins:

- `check_minimal_cover.py`: 4,778 bytes; SHA-256 `7b623710911fd2f6c49cc461961aee352e9307b71c15d2ce8e74431382eebab8`.
- `minimal_cover_checks.json`: 4,654 bytes; SHA-256 `44985ff4b0fc6baed6a804a3707db8b529617de4d3350d266c08cc796a06bc1d`.
- `check_prism_signs.py` and `prism_sign_checks.json` retain the exact-integer verification of all 546 closure/prism identities.

## 8. Acceptance limits and what follows

The concrete consistency question is settled against the exact inspected arXiv v3 statements. The pass-1/pass-2 authored sheaf and complex constructions do not need to be discarded on account of this example; this audit independently recovers their coloop behavior. They must remain independent of the unrestricted v3 freeness inference.

The published article has a later revision history, and its full theorem and proof text remain unverified. A bounded search finding no correction is not evidence that the inaccessible text is identical to v3. This audit makes no claim about corresponding published-version statements. The broad source problem remains outside this acceptance.
