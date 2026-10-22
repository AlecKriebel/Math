# Supported Euler classes in the arithmetic fibre

This is a formal geometric special case, not a solution of the general geometric Chern-class problem, and not a claim of a new general theorem.

## Hypotheses

Let S be an arithmetic base for the regulator in the source, j:eta -> S its generic-point morphism, E=MGL_S, B=j_*D and A=fib(E -> B). Work in the motivic stable homotopy category with the derived adjunction j^* left adjoint to j_* and its compatibility with bigraded suspensions. Let X be smooth over S. For a closed Z in X define C_Z=X/(X\Z) and F_Z^{p,q}(X)=[Sigma^infty C_Z,Sigma^{p,q}F]. Suppose Z_eta is empty. No E-module enhancement of the regulator is necessary for the basic construction below.

## 1. Canonical comparison with support

Pullback carries C_Z to X_eta/X_eta, the zero pointed object. Adjunction gives B_Z^{p,q}(X)=0 for all p,q. The fibre long exact sequence therefore identifies A_Z^{p,q}(X) with E_Z^{p,q}(X), naturally in maps of pointed quotients. This comparison is integral. It does not use a purity theorem for Z or identify MGL with a geometric cobordism theory over number rings.

## 2. Euler class of a generically nowhere-zero section

Let V -> X be a rank-r vector bundle, and let s be a section whose zero locus Z has empty generic fibre. By definition s sends X\Z into V\0_X, so it induces
s_bar:C_Z -> Th(V)=V/(V\0_X).
Let u_V in E^{2r,r}(Th(V)) be its oriented Thom class. Define
 e_Z(V,s)=s_bar^*u_V in E_Z^{2r,r}(X),
and let a_Z(V,s) be its unique preimage in A_Z^{2r,r}(X). Define a(V,s) in A^{2r,r}(X) by forgetting support.

Proof of its underlying class: after forgetting support, e_Z(V,s) is the pullback of u_V along the pointed map X_+ -> V -> Th(V). The bundle section s is A1-homotopic to the zero section by (x,t) |-> t s(x). Their pullbacks coincide in motivic cohomology represented by E. The zero-section pullback is the Euler class, namely the top oriented Chern class c_r^E(V). Thus the image of a(V,s) in E^{2r,r}(X) is c_r^E(V). This also proves directly that its regulator vanishes, without assuming independent orientation compatibility for the regulator.

No smoothness, regular embedding, transversality, or expected-codimension property of Z is required. This is the localized Euler class of the section, not an assertion that every arbitrary singular vertical subscheme has a preferred fundamental class. For r=1 this is a supported geometric first-Chern lift for a line bundle equipped with a generically nonvanishing section.

## 3. Functoriality and controlled dependence

For a morphism f:Y -> X between smooth S-schemes, with W=f^{-1}(Z), the induced quotient map Y/(Y\W) -> X/(X\Z) and naturality of Thom classes imply
 f^*a_Z(V,s)=a_W(f^*V,f^*s).
W still has empty generic fibre. Here f^* on supported groups is precisely the map induced by this quotient, not an assumed Gysin map.

If phi:V -> V' is a bundle isomorphism taking s to s', the induced Thom-space map preserves the oriented Thom class. Consequently the two supported Euler classes agree after the evident identifications, and so do their unique A-lifts. In particular multiplication of a line-bundle section by a globally invertible function does not change the class.

If Z is enlarged to a closed vertical W, the map of supported cohomology groups sends a_Z(V,s) to the unique A_W lift of the corresponding E_W class. This follows from naturality of A -> E and uniqueness with support.

For two generically nonvanishing sections s0,s1 of the same V, put W=Z0 union Z1. Their globally forgotten E-classes agree, but no equality of their E_W classes follows merely from the unrestricted A1 homotopy. Indeed the linear interpolation (1-t)s0+t s1 can have zeroes on X_eta times A1 even when both endpoints have none. Thus the homotopy need not define a homotopy of quotient maps with vertical support. Their global A-classes can a priori differ by the image of B^{2r-1,r}(X). More precisely the difference lies in the kernel of A^{2r,r}(X) -> E^{2r,r}(X), identified with coker(E^{2r-1,r}(X) -> B^{2r-1,r}(X)). This is a possible ambiguity; no nonzero difference is proved here.

A sufficient condition for equality is a homotopy of sections over X times A1 whose zero locus is contained in W times A1 for one fixed vertical W. Then it defines a pointed homotopy C_W -> Th(V), the E_W classes agree, and hence the A_W classes agree. Ordinary A1 homotopy without this support control is not enough.

## 4. A principal vertical divisor

Let S=Spec(O_K) for a number field K, X=S, V=O_S and choose a nonzero nonunit a in O_K. The section s=a has zero locus Z=V(a), entirely vertical. The preceding construction supplies a canonical supported class a_Z(O_S,a) in A_Z^{2,1}(S). Its image after forgetting support in E^{2,1}(S) is c_1^E(O_S)=0. Thus its global arithmetic class, whether zero or not, lies in the secondary subgroup im(B^{1,1}(S) -> A^{2,1}(S)).

The supported class need not be discarded merely because the line bundle is trivial globally. Under the standard oriented map MGL -> motivic integral cohomology, its image is the localized first Chern cycle div(a)=sum_p v_p(a)[p]. In codimension-one motivic cohomology with support on this regular Dedekind scheme this is the usual divisor group supported on Z. This last identification uses the standard motivic divisor/purity description and is an IMPORT, not proved by the fibre argument. For the explicit case O_K=Z and a=p prime, the localized divisor is the coefficient-one class [p], so that standard realization detects a nonzero supported class. This detection is not needed for existence or uniqueness of the A-lift.

An alternative detection uses only the standard orientation of algebraic K-theory, avoiding the mixed-characteristic motivic-cohomology comparison. Import the oriented map MGL -> KGL and the standard description of its supported Euler class by the Koszul complex. Fix the usual K-theory orientation and Bott identification KGL_Z^{2,1}(S) with K_0^Z(S) so that c_1(L) corresponds to 1-[L^dual]. These are the explicit conventions verified in vertical_euler_audit_receipt.md, using Panin–Pimenov–Röndigs, Corollary 1.2.7 and Sections 2.6–2.7, and Naumann–Spitzweck–Østvær, Theorem 3.1, over the regular mixed-characteristic base Spec(Z). For S=Spec(Z), section p gives the two-term perfect complex Z --p--> Z, in cohomological degrees -1 and 0. Its only nonzero cohomology is Z/p in degree zero. The additive invariant on perfect complexes supported at p given by sum_i (-1)^i length_{Z_(p)} H^i detects this class as 1. Consequently its supported K-theory class, and hence the supported MGL and A classes mapping to it, are nonzero. This is an exact integral calculation. Forgetting support the alternating sum of free-module classes is [Z]-[Z]=0, consistently with the trivial underlying line bundle. The orientation and Koszul description are imported standard K-theory facts, not derived from the report; no assertion about the forgotten A-class follows from this detection.

Nothing here computes the resulting global A-class as a real logarithm, metric invariant, or numerical Arakelov degree. Such an assertion would require an explicit compatible regulator realization and normalization not supplied by the schematic triangle. In particular we do not assert that the global class for p is nonzero. The example distinguishes supported uniqueness from global secondary information.

## 5. Specialization: what is and is not obtained

Any closed fibre S_s disjoint from eta kills the j_*D contribution on objects supported there by the preceding adjunction. Thus the comparison on vertical support is insensitive to the archimedean regulator target. For a regular closed immersion with available motivic purity, one may further identify E_Z with a Thom-space theory of the normal bundle, and the same supported A group inherits that identification. This is conditional on that specific purity theorem and its hypotheses.

There is no unconditional specialization map from generic-fibre A-cohomology to special-fibre A-cohomology constructed here. Generic nearby-cycle, residue, or degeneration operations require their own localization and compatibility constructions. Calling the support isomorphism a full specialization theorem would be an overclaim.

## Exact achieved statement

For an oriented motivic source E and a regulator target pushed forward from the generic point, every vector bundle equipped with a generically nowhere-zero algebraic section has a canonical relative Euler class WITH its vertical zero support, uniquely lifting the corresponding E Euler class. Forgetting support gives a lift of its top Chern class depending a priori on the section. This is concrete geometry in a restricted class of inputs. It gives neither all Chern classes of all bundles, nor a section-independent geometric presentation of the full arithmetic fibre.
