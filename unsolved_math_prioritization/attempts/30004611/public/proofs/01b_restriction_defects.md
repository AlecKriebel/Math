# Stalk restrictions and canonical defects for logarithmic lattice sheaves

13 October 2026 UTC. Row 1775 / 30004611, same shared mathematical pass 1. This is an authored, unrefereed mathematical component of the ongoing investigation, not an independent acceptance report or full solution of Mücksch's broad Problem 6.3. The Euler seven-plane calculation below is explicitly reused, credited work from row 992 / 30003081 (a distinct target); it is not a fresh discovery or fresh investigation of that previous problem.

## 1. Precise category and notation

Let K be any field, V a finite-dimensional vector space, A a finite central essential simple arrangement, H in A, and alpha a fixed nonzero defining form of H. Put S=Sym(V*), R=S/(alpha). All polynomial derivation degrees refer to coefficient degree. Graded shifts M(-1) place an element of degree d in degree d+1.

Let P be the nonzero flats of A ordered by geometric inclusion. Let Q={X in P : X is contained in H}; it is the punctured restriction lattice and a closed subposet. Write i:Q→P. A sheaf of S-modules for the upper Alexandrov topology is a covariant functor; exactness is pointwise. For X in P write B_X=A_X. For X in Q the ordinary restriction of B_X equals (A^H)_X, and its Ziegler multiplicity is exactly the localization of the original multiplicity m^H. Indeed every original hyperplane with a given intersection hyperplane K in H contains X if and only if K contains X. Thus an entire multiplicity class is retained or omitted, never partly retained.

Define D_X=D(B_X). The restriction targets on Q are

T_X=D((B_X)^H), and Z_X=D((B_X)^H,m_X^H),

over R, regarded also as S-modules through S→R. Their maps for X⊆Y are the usual inclusions. Extension i_* has these stalks on Q and zero stalks outside Q: if X is outside H, no flat Y≥X lies in Q, while if X is in Q it is the minimum such flat.

Define the ideal sheaf I by I_X=alpha S on Q, I_X=S outside Q, with inclusion maps. It is tensor-flat because every stalk is free of rank one. It is generally NOT an invertible/locally free rank-one sheaf on this finite ringed space: an arrow from Q to its complement has the nonunit inclusion alpha S→S. In particular I is not a uniform global grading shift of the constant S sheaf.

The companion component constructs the deletion transport. Its stalk is D(A'_X), where A'=A\{H}. If deletion becomes nonessential, one must explicitly extend the source definition to literal nonzero geometric flats, rather than silently using Mücksch's L(A')\{T(A')}. Those sets differ when T(A') is nonzero.

## 2. Elementary local restriction maps

For any central simple arrangement B containing H there is the ordinary map

rho: D(B)→D(B^H), theta↦theta mod alpha,

with kernel alpha D(B\{H}). To prove the kernel assertion, choose alpha as one coordinate. A logarithmic theta whose induced derivation modulo alpha is zero has every coefficient divisible by alpha, including the normal coefficient because theta is tangent to H. Write theta=alpha eta. For any L≠H, alpha and alpha_L are coprime, so tangency of theta to L implies tangency of eta to L. The converse is immediate. This proof does not require essentiality, freeness, rank restrictions, or characteristic assumptions.

Let E(B)={theta in D(B):theta(alpha)=0}. Reduction gives the Ziegler map

pi: E(B)→D(B^H,m^H), with kernel alpha E(B).

For well-definedness, fix a restricted hyperplane with equation beta. Normalize the distinct original forms lying over it as beta+c_j alpha. Since theta(alpha)=0, each condition says beta+c_j alpha divides theta(beta). Distinct forms are pairwise coprime, so their product divides theta(beta). Reduction modulo alpha gives beta^m dividing the reduced theta(beta). The kernel proof is coefficient division as above, now also preserving theta(alpha)=0.

These maps and kernel identifications are natural under B_X⊇B_Y whenever X⊆Y in Q.

## 3. Rank at most two: complete characteristic-free lifting proof

Suppose B has rank two and H is in B. Choose coordinates x=alpha,y,z_1,...,z_t so that all forms of B involve x,y. Normalize the forms other than x as y+c_j x and put q=product_j(y+c_j x), r=|B|-1. Set e=x partial_x+y partial_y.

There are explicit bases

D(B)=S e ⊕ S q partial_y ⊕ direct_sum_j S partial_{z_j},

E(B)=S q partial_y ⊕ direct_sum_j S partial_{z_j}.

For a direct proof, write theta=f partial_x+g partial_y+sum h_j partial_{z_j}. Tangency to x gives f=xa. Subtract a e. The remaining y coefficient g-ya must be divisible by every y+c_j x, hence by q. This also proves linear independence. No division by |B| or any characteristic-dependent integer occurs.

The ordinary target has basis y partial_y and the partial_{z_j}. These lift to e and partial_{z_j}. The Ziegler target has basis y^r partial_y and the partial_{z_j}. These lift to q partial_y and partial_{z_j}. Thus both maps are onto over every field.

If B has rank one, B={H}; both targets are derivations of the empty arrangement on H and their coordinate derivations lift. These arguments include nonessential B and arbitrary common-flat directions.

Consequently on the original punctured lattice of any essential arrangement of rank at most three every target-bearing stalk has surjective ordinary and Ziegler maps: for nonzero X, rank(A_X)=codim X≤2. The removal of the zero flat is essential to this conclusion.

## 4. The global Ziegler domain genuinely relates to D

On all of P define E_X={theta in D(A_X):theta(alpha)=0}, using inclusions for its structure maps. On Q this is exactly the usual Ziegler domain E(B_X). Off Q it is still a natural, explicitly defined subfunctor; no expression theta(alpha)/alpha is used there.

Evaluation defines a morphism D→I, theta↦theta(alpha). It is onto at every stalk. On Q the Euler derivation maps to alpha. Off Q choose v in X with alpha(v)=1; the constant derivation partial_v belongs to D(A_X) because every hyperplane of A_X contains X, and it maps to 1. Therefore there is an unconditional natural short exact sequence

0→E→D→I→0.

The Ziegler map E→i_*Z is reduction on Q and zero elsewhere. Its kernel is canonically I⊗_S E under multiplication: on Q it is alpha E_X, and off Q the entire E_X. The ordinary kernel is likewise I⊗_S D', with D' meaning the explicit transported deletion functor. The cross-boundary structure maps are precisely inclusions, so these identifications commute with every arrow in P.

Thus if all relevant local restriction maps are onto, the genuine named-target sequences are

0→I⊗D'→D→i_*T→0,

0→I⊗E→E→i_*Z→0,

in addition to 0→E→D→I→0. They always hold when rank(A)≤3. In higher rank the hypotheses in Sections 5 and 6 are sufficient. The domains and target are actual derivation functors or explicit ideal twists; no surjectivity is obtained merely by renaming an image.

## 5. Canonical reflexive-hull identification in every rank

For a fixed B containing H put

F=D(B)/alpha D(B\{H}), and G=E(B)/alpha E(B).

The maps in Section 2 embed F into D(B^H) and G into D(B^H,m^H). These are finitely generated torsion-free R-modules.

Both embeddings are isomorphisms at every height-zero or height-one prime of R. For a height-one prime p, its inverse image q in S has height two. Hyperplanes whose equations are not in q disappear on localization. The remaining equations lie in the two-dimensional space spanned by alpha and, if present, a restricted linear factor generating p. If p is not such a linear factor, only H remains. The resulting localized arrangement therefore has rank at most two, and Section 3 proves surjectivity. Localization commutes with these derivation modules, their annihilation-of-alpha kernels, and the two reduction maps, because all are defined by finite linear divisibility conditions.

Logarithmic derivation modules of simple or multiarrangements over a polynomial ring are reflexive: they are the intersection, inside the rational derivation vector space, of their free height-one divisibility lattices. Since a reflexive module over the normal domain R is determined by its height-one localizations, there are canonical identifications

F** = D(B^H), and G** = D(B^H,m^H),

where both stars mean Hom_R(-,R). These identifications extend the displayed embeddings and commute with maps B_X⊇B_Y. One way to verify naturality is that the double-dual maps and target inclusions agree generically; the targets are torsion-free, so the maps agree everywhere.

This is a genuine identification of the named target as a reflexive hull. The ordinary and Ziegler defects are respectively F**/F and G**/G, supported in R-codimension at least two. It is stronger than merely naming the image, but does not make either defect vanish in arbitrary rank.

### Conditional ordinary surjectivity, with proof

If D(B\{H}) is free, then F is reflexive. At an R-prime p of height h, its inverse image q has S-height h+1. In

0→D(B\{H})(-1)_q→D(B)_q→F_p→0,

the left module has depth h+1 and the middle module has depth at least min(2,h+1), because D(B) is reflexive. The depth lemma gives depth F_p≥min(2,h). Depth for the R-module equals depth as an S-module. Together with torsion-freeness this is Serre's S2 criterion for reflexivity over R. Thus F=F** and rho is onto.

### Conditional Ziegler surjectivity, with proof

There is an S-linear splitting D(B)=S theta_E⊕E(B), obtained by subtracting (theta(alpha)/alpha)theta_E. If D(B) is free, E(B) is projective. Therefore G=E(B)⊗_S R is projective, hence reflexive over R, and G=G**. Thus pi is onto. No assertion that Euler and Ziegler multiplicities agree is used.

Applied stalkwise, these give sufficient sheaf hypotheses:

- ordinary: D(A_X\{H}) is free for every nonzero flat X⊆H;
- Ziegler: D(A_X) is free for every nonzero flat X⊆H.

Global freeness of the deletion or arrangement is sufficient, respectively, by the standard localization property of free arrangements. The explicit stalk hypotheses avoid needing to identify cohomology under any change of poset. They are sufficient, not claimed necessary.

## 6. Ordinary defect as a pointwise Ext kernel

This section specializes the credited Abe–Denham module result and verifies its functorial transport. It does not identify internal sheaf Ext, global Ext in the functor category, or lattice-sheaf cohomology with pointwise Ext.

For X∈Q define ambient-S-module functors

U_X=Ext^1_S(Omega^1(A_X\{H}),S)(-1),

W_X=Ext^1_S(Omega^1(A_X),S).

For X⊆Y, forms have inclusions Omega^1(A_Y)→Omega^1(A_X), and similarly for deletion. Applying contravariant Ext in the first argument gives covariant maps U_X→U_Y and W_X→W_Y. Thus these are well-defined Alexandrov sheaves, but their definition is explicitly pointwise commutative algebra.

There is a natural map u:U→W induced by multiplication

alpha:Omega^1(A_X)(-1)→Omega^1(A_X\{H}).

The ordinary defect functor C_X=coker[rho_X] is canonically

C = ker(u:U→W).

In particular the defect has an identified commutative-algebra description beyond an unnamed image quotient. Extended by i_*, it measures exactly the failure of the proposed global ordinary sequence to be right exact.

Here is the derivation and naturality check. Let C_Omega(B) be the image of the logarithmic-form restriction from Omega^1(B\{H}) to Omega^1(B^H). There is a short exact sequence

0→Omega^1(B)(-1) --alpha→ Omega^1(B\{H})→C_Omega(B)→0.

The form image agrees with Omega^1(B^H) at all R-height-one primes. For simple arrangements this can also be checked directly: a form d beta_j / beta_j from any original hyperplane over a restricted factor reduces to d beta / beta; common directions lift as constant forms. Therefore Hom_R(C_Omega(B),R)=D(B^H), since the latter is reflexive. Applying Hom_S(-,S), then the hypersurface change-of-rings identification

Ext^1_S(C_Omega(B),S)=Hom_R(C_Omega(B),R)(1),

gives the initial exact segment

0→D(B\{H})(-1) --alpha→D(B) --rho→D(B^H)
 →Ext^1_S(Omega^1(B\{H}),S)(-1)
 →Ext^1_S(Omega^1(B),S).

With the usual fixed sign convention the middle arrow is the ordinary restriction map; this is the sequence of Abe–Denham Theorem 4.8. The ordinary defect is consequently the kernel of the final displayed map.

For X⊆Y, the inclusions of logarithmic forms give a commuting diagram of the form short exact sequences, in the direction Y→X. Functoriality of the long exact Ext sequence reverses this to X→Y. The hypersurface change-of-rings isomorphism uses the same fixed alpha, and the dual identification with D(B^H) extends the natural generic identification; both commute with these arrows. This proves naturality, rather than merely asserting an unrelated isomorphism at each stalk.

Abe–Denham's general theorem uses Euler multiplicity m*. For simple arrangements Remark 2.2 explicitly states m*=1, so the target here is the genuine ordinary restriction. This argument does not replace m* by the generally different Ziegler multiplicity. For Ziegler, Section 5 supplies the canonical reflexive-hull defect; no unproved analogous Ext formula is asserted.

## 7. Sharp higher-rank failure of the specified maps

These examples do not refute Mücksch's broad constructive question, which does not prescribe these particular maps or comparison spaces.

### Ordinary map: credited seven-plane example promoted to a nonzero flat

Over Q, let B in K^3 have defining polynomial

z x y (x-z)(y-z)(x-y+z)(x-y-z),

and mark H_0={z=0}. This is the arrangement in Abe–Kawanoue, arXiv:2406.00305v2, Example 4.3(3), already reconstructed and audited in the prior row-992 packet. The restriction is the simple three-line arrangement xy(x-y)=0. The derivation eta=x(x-y) partial_x does not lift through the ordinary restriction map.

For completeness, the existing elementary proof is reproduced as authored mathematics. A homogeneous quadratic lift must have coefficients

u=x(x-y+a z), v=b y z, t=z(c x+d y+e z).

Tangency to x-z gives d=-1 and c+e=1+a. Tangency to y-z gives c=0 and b=d+e. Thus e=1+a and b=a. On x-y+z=0, the required tangency expression becomes

(u-v+t)|_(x=y-z)=-2z(y-z),

which is nonzero over Q. This excludes a quadratic lift. Any polynomial lift would have a quadratic homogeneous component lifting eta because all conditions are homogeneous, so no polynomial lift exists. The extra factor x-y-z is retained to match the credited example. No characteristic-two claim is made for this witness.

Now in K^4 with coordinate w, let A consist of all lifted hyperplanes of B together with {w=0}. It is central essential of rank four. Mark H={z=0} and take the nonzero flat X={x=y=z=0}. Then A_X is B with one free w-direction; the hyperplane w=0 does not contain X and is absent from A_X. The stalk cokernel is exactly

coker(rho_B)⊗_K K[w],

because derivation modules split into the base module extended by K[w] and a free partial_w summand, whose restriction is onto. Thus the proposed ordinary sheaf map is not surjective at this nonzero flat. This explains why a rank-three module obstruction coexists with universal rank-three punctured-lattice exactness, yet survives in rank four.

### Ziegler map: credited four-plane factor, promoted over every field

The rank-three factor xyz(x+y+z) is already Abe–Kawanoue Example 4.3(2), where its nonzero Ziegler cokernel and zero ordinary cokernel are stated over R. It is credited here as an existing example. The argument below supplies a direct characteristic-free witness and promotes it to an essential rank-four arrangement with a bad nonzero-flat stalk; neither the arrangement nor the distinction of its two module cokernels is claimed new.

In K^4 let A have equations x,y,z,x+y+z,w. Mark H={z=0} and use X={x=y=z=0}. Then A_X has the four equations x,y,z,x+y+z and a free w-direction. On H the three restricted hyperplanes x,y,x+y are distinct over every field, all with Ziegler multiplicity one.

The degree-one target derivation eta=x partial_x+y partial_y is logarithmic. A degree-one lift in E(A_X) has zero z coefficient. Tangency to x and y and the required reduction modulo z force its x and y coefficients to be exactly x and y. Its derivative of x+y+z is then x+y, not divisible by x+y+z. A w coefficient cannot alter this equation. Hence no homogeneous degree-one lift exists, and homogeneity excludes all polynomial lifts.

This gives an essential rank-four counterexample to universal surjectivity of the specified Ziegler sheaf map over every field. In this very same example the ordinary map is onto. Explicitly the two target generators x partial_x+y partial_y and y(x+y) partial_y lift to x partial_x+y partial_y+z partial_z and y(x+y+z) partial_y, respectively; free w-direction derivations also lift. Equivalently, deleting z leaves three independent hyperplanes in the x,y,z factor, a free Boolean arrangement, so Section 5 applies. It concretely distinguishes the ordinary and Ziegler maps.

## 8. Source qualification and scope

- Paul Mücksch, On Yuzvinsky's lattice sheaf cohomology for hyperplane arrangements, arXiv:2008.13700v3 (12 October 2021), Definition 4.1 and Problem 6.3, pp. 13 and 18. https://arxiv.org/abs/2008.13700v3 . The retained primary text defines the covariant lattice functor and asks the broad constructive question. Published version metadata: https://doi.org/10.1007/s00208-022-02499-1 ; version-of-record full text was not inspected in this work.
- Takuro Abe and Graham Denham, Deletion-Restriction for Logarithmic Forms on Multiarrangements, arXiv:2203.04816v3 (19 May 2026), Remark 2.2, Theorem 1.2, Proposition 4.7, Theorem 4.8. https://arxiv.org/abs/2203.04816v3 . The relevant primary text was read; page 15 was visually checked to distinguish S from R in the Ext groups. The module result is credited; its pointwise functorial transport and the elementary simple-arrangement proofs above are the present mathematical work.
- Takuro Abe and Hiraku Kawanoue, Cokernels of the Euler restriction map of logarithmic derivation modules, arXiv:2406.00305v2 (10 June 2024), definitions pp. 2–3 and Example 4.3(2)–(3). https://arxiv.org/abs/2406.00305v2 . Both the four-plane Ziegler example and the seven-plane ordinary example are credited to this source. The previous row-992 seven-plane reconstruction is reused, not claimed new.

Complete claims established here: exact kernel descriptions and naturality, all-field rank≤3 named-target sequences for the chosen transports, sufficient higher-rank freeness conditions, canonical reflexive-hull targets, a natural pointwise Ext description of ordinary defects, and explicit failures of both specified maps in essential rank four. No theorem classifies all possible short exact sequences requested in the broad original problem, no unrestricted right-exactness theorem is claimed, and no novelty or exhaustive literature-resolution claim is made.
