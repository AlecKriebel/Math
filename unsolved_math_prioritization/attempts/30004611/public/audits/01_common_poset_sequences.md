# Independent audit: common-poset logarithmic sequences and defects

Date: 13 October 2026 UTC. Row 1775 / 30004611, shared mathematical pass 1. This is a qualified mathematical acceptance of the exact versions below, not a solution certificate for the full original problem or a novelty certificate.

## 1. Audited versions and verdict

1. `common_poset_sequences.md`: 12,264 bytes, SHA-256 `d9d90ab55629dbabcb955651e0c4b3ee69a387eb99b313316828226577c93e78`.
2. `RESULT.md` of the parallel restriction-defect component: revised 18,971 bytes, SHA-256 `37ea8ba0f43498f48e3f790d0d0ac10249d35b2c49f04285e3d99bed9201b7ef`.

The original defect draft was 18,229 bytes with SHA-256 `c8ba61209c53a557c151e9271bdd717f24f9944a838539a7a0be21b40ef6ada6`. Its mathematics passed, but I required two source corrections before final acceptance:

- The rank-three arrangement xyz(x+y+z) and its differing ordinary/Ziegler cokernels are already Abe–Kawanoue Example 4.3(2). The revised report credits this, in addition to the seven-plane Example 4.3(3). The present argument supplies an all-field witness and the promotion to a nonzero stalk of an essential rank-four arrangement; no novelty claim follows.
- Mücksch arXiv:2008.13700v3 Definition 4.1 is on printed/PDF page 13, not page 11. Page 11 contains the general poset-sheaf setup. Problem 6.3 is on page 18. The revised report fixes this.

I verified the complete revised diff and final byte pin. No mathematical correction to the pinned common-poset component is required. Both components are accepted with the scope limits below.

## 2. Exact source target and acceptance scope

I read the source-verification record and inspected the retained primary text at Mücksch's introduction, Section 3, Definition 4.1, and Problem 6.3. The source uses covariant logarithmic derivation functors on the intersection lattice with its center removed and order reversed to geometric inclusion. Its question is broadly constructive and does not prescribe the maps or transports under audit.

Consequently the accepted outcome is a partial answer consisting of:

- natural common-poset left-exact ordinary and Ziegler sequences, with independent descriptions of their kernels;
- genuine named-target short exact sequences in dimensions two and three, for a marked coloop in every dimension, and under the stated local-freeness hypotheses;
- an unconditional normal-evaluation short exact sequence;
- canonical reflexive-hull identifications and a natural pointwise Ext description of the ordinary defect;
- essential rank-four obstructions to universal surjectivity of these particular maps.

This neither proves that every arrangement has the proposed right-exact sequences nor excludes other constructions answering the source's broad question. It does not derive an unrestricted addition–deletion theorem or freeness criterion from cohomology. The source's assumptions, altered conventions for nonessential deletion, and dimension-one restriction boundary must remain visible.

## 3. Posets, variance, and transport

Let P be the nonzero flats of an essential arrangement A, ordered by inclusion, and Q the flats contained in H. The equality Q=L(A^H) minus the zero flat is valid: an intersection in H of restricted hyperplanes is an intersection in V including H, and every flat contained in H can be represented this way. Q is a lower ideal, hence closed in the upper Alexandrov topology. All displayed derivation functors are covariant, with inclusions in the correct direction.

The deletion closure c(X), defined by intersecting deletion hyperplanes containing X, is a nonzero deletion flat because it contains the nonzero X. It is monotone, fixes deletion flats, and satisfies A'_{c(X)}=A'_X. The geometric deletion poset embeds into P. For its inclusion j, the deletion flats above any X have the least element c(X), so (j_*G)_X=G_{c(X)}, compatibly with arrows. Thus c^*G=j_*G, not merely a stalkwise noncanonical identification.

Both exactness and the claimed cohomology comparison follow: evaluation at c(X) is exact, inverse image is exact, j_* preserves injectives as its right adjoint, and global sections agree. The same argument for the closed inclusion i gives extension by zero, exactness of i_*, and equality of its sheaf cohomology with cohomology on Q. There is no inappropriate transfer of homology or contravariant-functor results.

The nonessential deletion qualification is necessary. Mücksch removes the center T(A'), while this construction retains its nonzero center and removes literal zero only when present. This extended deletion poset has a minimum and therefore no positive sheaf cohomology for any coefficient sheaf. Its cohomology cannot be identified with the source's center-punctured deletion cohomology without further work. In the essential original arrangement, nonessential deletion is precisely the marked-coloop case and its center is one-dimensional.

## 4. The ideal twist and ordinary kernel

The ideal I has stalk alpha S on Q and S elsewhere, with inclusions. It is the kernel of the constant S sheaf's quotient to i_*R. All stalks are free and hence tensor-flat, but I is generally not locally free/invertible on this finite ringed space: on an arrow H→V its transition is the proper inclusion alpha S→S. It cannot be replaced by a constant grading shift.

The ordinary map reduces tangent derivations modulo alpha on Q and is zero off Q. On Q the localized restriction is exactly (A_X)^H=(A^H)_X. Arrows within Q commute with reduction; arrows leaving Q commute because the target transition is zero; no arrow enters the lower ideal from outside.

For X in Q, induced reduction zero forces every coefficient to be divisible by alpha, including the normal coefficient by tangency to H. If theta=alpha eta, distinct linear forms alpha and alpha_L are relatively prime, so eta is logarithmic for A'_X. Conversely every such multiple lies in the kernel. Off Q the source is already D(A'_X), and the kernel is the whole stalk. These identifications commute with every arrow and are exactly the image of multiplication I tensor c^*D'→D.

This verifies the left-exact sequence and its coefficient grading. On Q the kernel has the usual (-1) shift; off Q it has no shift. A globally shifted deletion injection already fails at the top flat V because alpha Der(S) is a proper submodule of Der(S).

The additional sequence 0→I tensor F→F→i_*(R tensor i^*F)→0 is also correct: every deletion stalk is torsion-free, so multiplication by alpha is injective. The final term is deletion reduced modulo alpha, and must not be renamed the ordinary restriction derivation module.

## 5. Normal evaluation and Ziegler kernel

Define E_X by theta(alpha)=0 even when X is outside H. This gives a genuine subfunctor everywhere. On Q, evaluation D_X→alpha S is onto via the Euler derivation. Off Q, a vector v in X with alpha(v)=1 gives a constant derivation tangent to all hyperplanes through X and evaluating to 1. Thus 0→E→D→I→0 is a stalkwise exact, natural sequence over every field.

The ideal and kernel E are unchanged when alpha is scaled by a nonzero scalar. Evaluation scales by that scalar; the resulting sequences are canonically isomorphic through the corresponding unit on I. No invariant choice of evaluation map without a defining form is silently claimed.

For Ziegler restriction, normalize all original forms over one restricted factor beta as beta+c_j alpha. A derivation killing alpha has the same derivative on each of these forms. Their pairwise coprimality forces divisibility by their product; reduction therefore has precisely the required power beta^m. A multiplicity class is either entirely retained in A_X or entirely omitted. Hence the target is the localized global Ziegler sheaf, not an unrelated Euler-multiplicity restriction.

The kernel is alpha E_X on Q by coefficient division and is E_X off Q. This identifies it naturally with I tensor E and proves the claimed Ziegler left-exact sequence. The notation E or D_H denotes the normal-annihilating domain, not the ordinary restriction D(A^H).

Stalkwise splitting does not imply global splitting. An independent example is the three-line arrangement with equations x, y, x-y and marked equation alpha=x. A hypothetical sheaf splitting s:I→D has s_V(1)=partial_x+g partial_y, because evaluation must equal 1. Naturality from the two off-H hyperplane flats forces y to divide g and x-y to divide 1-g. Evaluating both divisibilities at the origin gives g(0)=0 and 1-g(0)=0, a contradiction over every field. Thus normal evaluation need not split as a sheaf map. The audited components assert no global splitting and use only the long exact cohomology sequences.

## 6. Surjectivity classes and characteristic checks

For a target-bearing stalk of rank two choose alpha=z and a second normal coordinate t, with common-flat coordinates u_j. The remaining equations normalize to t+c_j z. With q their product, direct coefficient subtraction gives

D(A_X)=S(z partial_z+t partial_t) direct-sum S q partial_t direct-sum sum_j S partial_{u_j},

E_X=S q partial_t direct-sum sum_j S partial_{u_j}.

These are valid over arbitrary fields. The ordinary generators t partial_t and partial_{u_j} lift, while the Ziegler generators t^r partial_t and partial_{u_j} lift via q. Rank-one stalks are equally immediate. Since a nonzero flat in an essential arrangement of dimension at most three has localization rank at most two, both sheaf maps are surjective in that range. No division by an arrangement size or characteristic-dependent integer occurs.

For a coloop, V splits as H plus the one-dimensional deletion center. All deletion forms are independent of alpha, restriction has no duplicate factors, and coefficientwise lifting proves both surjections even if the deletion arrangement is not free.

The ordinary local-free-deletion hypothesis is sufficient. Independently checking the parallel report's proof: if F=D(B)/alpha D(B minus H), then F embeds in the ordinary target and is torsion-free over R. For a height-h prime p of R and its height-(h+1) preimage q in S, the free left term has depth h+1 and the reflexive middle term has depth at least min(2,h+1). The depth lemma gives depth F_p at least min(2,h), exactly the S2 bound needed over R. Its reflexive hull is the named target by Section 7 below, so surjectivity follows. The depth index and the switch between S- and R-depth are correct.

The local-free-arrangement hypothesis for Ziegler is also sufficient over arbitrary fields. D(B)=S Euler direct-sum E(B), so when D(B) is free, E(B) is projective. Its reduction modulo alpha remains projective, hence reflexive over R. The same reflexive-hull identification gives surjectivity. This proves the needed assertion without importing an unstated characteristic restriction. The corresponding cited Abe–Denham free-surjection theorem matches the simple-arrangement ordinary target because Euler multiplicity is one in that case.

In dimension two the restriction has dimension one, outside the source's standing dimension assumptions. Its punctured lattice is just {H}, and its sole stalk is Der(R). This does not equal the full logarithmic module for its zero hyperplane. In particular neither an ordinary nor a Ziegler module-surjectivity theorem may be inferred by identifying those global sections with the full restriction module. The caveat in the common-poset component is indispensable and correct.

## 7. Reflexive hulls and naturality

For either image module F or G in the parallel report, the map to the named target is an isomorphism at generic and height-one primes of R. At a height-one prime p, only linear restricted factors contained in p survive. If there is one, all surviving original forms lie in the span of alpha and that factor; otherwise only H remains. The resulting localization has arrangement rank at most two, where the preceding explicit lifting proof applies. This remains valid for nonhomogeneous primes and finite fields.

The named ordinary and multiarrangement derivation modules are reflexive: inside their common rational derivation space they are the intersection of the free height-one divisibility lattices. Thus F** and G** canonically equal the respective named targets. This also proves that the defects have R-codimension at least two. Double duals here are over R, not over S.

For X contained in Y the image maps induced by inclusions commute with target inclusions. After double dualization both candidate maps agree generically, and their targets are torsion-free, so they agree everywhere. This establishes naturality, rather than merely unrelated stalkwise isomorphisms.

## 8. Ext defect: exact rings, shifts, and variance

The ambient-S modules in the report are U_X=Ext^1_S(Omega^1(A_X minus H),S)(-1) and W_X=Ext^1_S(Omega^1(A_X),S). Logarithmic forms have inclusions in the opposite direction to logarithmic derivations under localization of the arrangement. Contravariance of Ext reverses that direction back to X→Y. Hence U and W really are covariant pointwise module functors.

The short exact form sequence begins with alpha:Omega^1(B)(-1)→Omega^1(B minus H) and has its actual form image as quotient. At height-one primes over R the form image equals the named restriction form module, since d beta_j/beta_j reduces to d beta/beta and the common directions lift. Its R-dual is therefore the ordinary restriction derivation module. For the fixed equation alpha, change of rings gives

Ext^1_S(C_Omega,S)=Hom_R(C_Omega,R)(1).

Dualizing the form sequence and shifting by (-1) yields precisely the stated initial exact segment through U→W. The kernel of that last map is the ordinary restriction cokernel. The sign choice for the connecting map is fixed once; it does not affect the defect and agrees with the cited module restriction sequence.

All form inclusions commute with multiplication by the same alpha. Functoriality of the Ext long exact sequence, naturality of change of rings, and generic agreement of the R-dual identification prove the claimed sheaf naturality. There is no assertion here that pointwise Ext is internal sheaf Ext, global Ext in the functor category, or sheaf cohomology. Those distinctions must remain explicit.

## 9. Rank-four obstructions and independent finite controls

The credited seven-plane Euler witness was checked algebraically. Writing a homogeneous quadratic putative lift as in the report, tangency to x-z and y-z gives d=-1, c=0, e=1+a, b=a. Evaluation of tangency to x-y+z leaves -2z(y-z), which is nonzero over Q. Homogeneity excludes an arbitrary-degree lift. The source states its example over the real field; the displayed rational-coefficient proof directly verifies the Q version. No characteristic-two extension is claimed.

Adding a separate w=0 hyperplane makes the arrangement essential of rank four. At the nonzero w-axis flat this added hyperplane disappears, so the stalk is the original rank-three module with a free polynomial variable and free w-derivations. Reduction is onto on the free summand. Flat scalar extension gives the displayed tensor-product cokernel, which is nonzero. This transfer is a sheaf obstruction at a retained point, unlike the deleted origin of the rank-three punctured lattice.

The credited four-plane factor's Ziegler witness was also checked directly. A homogeneous degree-one lift of x partial_x+y partial_y killing z must have exactly x and y as its first two coefficients. Its derivative of x+y+z is x+y, not divisible by x+y+z over any field. A free w component cannot repair this. The three restricted linear forms remain distinct even in characteristic two. The ordinary map in the same example is onto: Euler lifts the target Euler generator and y(x+y+z) partial_y lifts y(x+y) partial_y. Thus the two maps are genuinely distinguished.

As an independent exact finite control, I formed all homogeneous coefficient constraints and compared matrix ranks, with rational elimination over Q and modular elimination over the listed prime fields:

- Four-plane Ziegler degree-one system: 15 equations, 9 unknowns; coefficient/augmented ranks 9/10 over Q and F2, F3, F5, F7, F11.
- Seven-plane Euler degree-two system: 27 equations, 18 unknowns; ranks 17/18 over Q and F3, F5, F7. Over F2 they are 17/17, agreeing with the excluded characteristic and the vanishing of the factor 2 in the displayed contradiction.

The characteristic-two seven-plane specialization also collapses the two forms x-y+z and x-y-z, so these finite controls do not license treating it as the same simple seven-hyperplane arrangement there. The finite calculations corroborate the symbolic proofs; they are not substitutes for the all-field argument or an exhaustive search.

## 10. Source/version and completion limits

Source checks used the retained exact arXiv versions: Mücksch 2008.13700v3; Abe–Denham 2203.04816v3; Abe–Kawanoue 2406.00305v2. I checked the relevant primary text for the functor convention, target, simple Euler multiplicity, free-surjection theorem, Ext continuation, and both credited examples. No version-of-record byte identity or numbering is inferred. This audit did not repeat the historical source-search campaign or claim current literature completeness.

The corrected components provide useful genuine short exact sequences on their stated domain, not merely tautological sequences obtained by renaming an image. They remain a partial answer to the broad source problem. The earlier row-992 example remains credited reused mathematics.
