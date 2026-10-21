# Turn 2: characteristic-free adjoint nonvanishing via Picard–Albanese and Riemann–Roch

2026-10-02. Second substantive research turn. Status: complete arbitrary-characteristic proof candidate awaiting independent review. No novelty or priority claim is made.

## Claim and original scope

Let k be an algebraically closed field of arbitrary characteristic. Let L be a nonempty finite reduced union of projective lines in P^3_k, with homogeneous radical ideal I. If alpha(I^(2))=alpha(I)+1, then L is coplanar or a pseudostar: the union of all pairwise intersections of finitely many distinct planes, no three of which contain a line. In particular L is ACM. If validated, this answers Janssen's non-ACM existence question negatively in its arbitrary-characteristic setting.

Primary statement: Janssen, https://arxiv.org/pdf/1306.4387, opening of section 1 (PDF p1) explicitly allows arbitrary characteristic, and Question 3.1 (PDF p8) asks the target question. Oberwolfach printed514 repeats it: https://ems.press/content/serial-article-files/46557. Pseudostar terminology and its ACM property are existing results, credited to Janssen and his cited Geramita–Harbourne–Migliore results. This proof is not a novelty certificate.

The new argument replaces the only characteristic-zero step, adjoint nonvanishing, entirely. It uses neither Kodaira/Kawamata–Viehweg vanishing nor smooth Bertini for the pulled-back hyperplane system. It also avoids classification of surfaces and any separability assumption on maps to curves.

## Standard inputs, stated precisely

1. A projective integral surface over an algebraically closed field has a projective resolution of its normalization, chosen to be an isomorphism over the regular locus. Normal surface singularities are isolated, and a normal surface is Cohen–Macaulay. This is surface resolution in arbitrary characteristic, not higher-dimensional characteristic-p resolution.
2. Surface Riemann–Roch: on smooth projective X, chi(O_X(D))=chi(O_X)+D.(D-K_X)/2. Serre duality gives h^2(O_X(D))=h^0(O_X(K_X-D)). Arithmetic adjunction for any integral Cartier curve C on X gives 2p_a(C)-2=C.(C+K_X). These are algebraic, characteristic-free statements.
3. Algebraic Hodge index: the intersection form on N^1(X)_R has signature (1,rho-1). In particular, for H^2>0 the restriction to H-perpendicular is negative definite. A nef class N has N^2>=0; therefore N.H=0 implies N numerically trivial. This is the algebraic surface Hodge index theorem, valid in arbitrary characteristic; it is not the characteristic-zero analytic Hodge theorem. See Badescu, *Algebraic Surfaces*, chapter on the Hodge Index Theorem (book treats arbitrary characteristic), or Hartshorne V.1.
4. Picard–Albanese: Pic^0(X)_red and Alb(X) are dual abelian varieties; T_0 Pic^0(X)=H^1(X,O_X). If H^2(X,O_X)=0, Pic^0(X) is smooth, hence reduced, so dim Alb(X)=h^1(X,O_X). The last implication follows directly by lifting line bundles through square-zero extensions: the obstruction is in H^2(O_X) tensored with the extension ideal; its vanishing gives formal smoothness, hence smoothness for the locally finite-type Picard scheme. A primary exposition explicitly states this consequence in Liedtke, *Algebraic Surfaces in Positive Characteristic*, printed pp13–14, https://cims.nyu.edu/~tschinke/books/simons12/lectures.pdf. It also states the Picard–Albanese duality and tangent-space formula there.
5. General plane sections of an integral surface in P^3 over an algebraically closed field are integral. Geometric irreducibility is Bertini (Stacks, https://stacks.math.columbia.edu/tag/0G4C); generic reducedness follows by applying smooth Bertini on the smooth open subset of the surface (https://stacks.math.columbia.edu/tag/0FD4). A hypersurface curve has no embedded components, so these imply integrality. No claim is made that the resulting curve is smooth at its intersections with the singular locus.
6. A finite birational normalization nu:Y->S of a hypersurface surface has canonical duality nu_*omega_Y=Hom_S(nu_*O_Y,omega_S). Since omega_S is invertible, this is c tensor omega_S, with c the conductor. Kollár–Dao, https://arxiv.org/html/1811.00042v2, Definition46 and equation(48.1). On normal Y, omega_Y is reflexive and equals extension from its smooth locus; hence a resolution q has q_*omega_X contained in omega_Y.

## A. A characteristic-free nonvanishing lemma on a smooth surface

**Lemma A.** Suppose X is a smooth integral projective surface over k, and H is a nef divisor with H^2=e>=2. Suppose |H| contains an integral curve C. Then H^0(X,omega_X(2H)) is nonzero.

**Proof.** If p_g(X)=h^0(omega_X)>0, multiply a nonzero canonical section by the square of the section cutting out C. The result is nonzero, so assume p_g(X)=0.

By Serre duality H^2(O_X)=0. Thus Pic^0(X) is smooth as explained in input4. Set A=Alb(X) and q=h^1(O_X); then q=dim A. We claim that the image of the normalization C_tilde of C generates A as an abelian variety.

Choose a point c_0 on C_tilde and choose the Albanese map a:X->A to send its image to zero. The map C_tilde->A then factors through its Jacobian J(C_tilde). Let B be the image abelian subvariety of the induced homomorphism J(C_tilde)->A. The image of C is contained in B. Let b:X->A/B be the composite Albanese-quotient map. It is constant on C. If M is an ample line bundle on A/B, its pullback N=b^*M is nef and has N.C=0. Since C is linearly equivalent to H, N.H=0. H^2>0 and Hodge index imply N^2<=0, with equality only if N is numerically trivial. Nefness gives N^2>=0; hence N is numerically trivial.

A nonconstant projective morphism to an abelian variety cannot pull back an ample line bundle to a numerically trivial bundle: if its image has positive dimension, take an integral curve in X mapping nonconstantly to that image; the pullback degree on that curve is positive. Such a curve exists by taking sufficiently ample complete intersections or a component over an image curve. Therefore b is constant. As a(X) generates Alb(X) by the Albanese universal property, the quotient A/B is zero. This proves B=A.

Consequently
q=dim A <= dim J(C_tilde)=g(C_tilde) <= p_a(C).

This uses neither separability nor a tangent-space injection on Jacobians. The final inequality follows from the normalization exact sequence of the integral projective curve.

Write g_a=p_a(C). Arithmetic adjunction gives K_X.H=2g_a-2-e. Riemann–Roch gives

chi(omega_X(2H))
 = chi(O_X) + (K_X+2H).(2H)/2
 = (1-q) + K_X.H + 2e
 = e+2g_a-1-q
 >= e+g_a-1 >= 1.

Here g_a>=0 for an integral projective curve. Moreover h^2(omega_X(2H))=h^0(O_X(-2H))=0. Indeed a nonzero effective divisor linearly equivalent to -2H would have negative intersection -2e with the nef H, impossible; the trivial-divisor case would force H^2=0. Thus h^0(omega_X(2H))=chi(omega_X(2H))+h^1(omega_X(2H))>=1. QED.

## B. The adjoint bound for integral surfaces in P^3, all characteristics

**Lemma B.** Let S be an integral surface of degree e>=2 in P^3_k. There is a nonzero homogeneous polynomial of degree e-2 vanishing along every singular curve of S.

**Proof.** Let nu:Y->S be normalization, q:X->Y a projective resolution, and f=nu q. Let H=f^*O_S(1). H is globally generated and nef, with H^2=e by birational projection formula.

A general plane section E of S is integral and is not contained in the singular locus. Choose its plane to avoid the finitely many images in S of exceptional curves of q. Its pullback C=f^*E then has no f-contracted curve components. Every component maps onto the integral E; over the generic point of E, f is an isomorphism because that point is in S_reg. Therefore there is exactly one component, of multiplicity one. Since C is a Cartier divisor on smooth X, it has no embedded components, and is integral. (It may be singular.) Thus Lemma A applies.

The restriction of a canonical form on X to the inverse image of Y_reg injects q_*omega_X into j_*omega_{Y_reg}=omega_Y. Projection formula and finite normalization duality inject

f_*omega_X(2H) into nu_*omega_Y tensor O_S(2)
 = c tensor omega_S tensor O_S(2)
 = c(e-2),

since omega_S=O_S(e-4). A nonzero global section from Lemma A is therefore a nonzero section of c(e-2).

The conductor c vanishes along the nonnormal locus: locally it consists of t in A with t B subset A, where B is the normalization inside Frac(A). If a conductor element is a unit at a point, B=A there. At the generic point of a singular curve of S the local ring has dimension one and is not regular; a normal one-dimensional Noetherian local domain would be a DVR. Thus that generic point is nonnormal. All sections of c vanish on each reduced singular curve.

Finally
0 -> O_{P^3}(-2) -> O_{P^3}(e-2) -> O_S(e-2) -> 0
and H^1(P^3,O(-2))=0 lift the nonzero section to the required nonzero polynomial. All these steps are characteristic-free. QED.

## C. Full line-configuration reduction in arbitrary characteristic

Put a=alpha(I), d=a+1, and choose 0!=F in I^(2) of degree d. For a line with linear prime p, p^(2)=p^2, and I^(2) is the intersection of these squares. Every target line lies in V(F).

### C1. Repeated factors
The squarefree radical R of F vanishes on all target lines. If deg R<=d-2, contradiction to a=d-1. If F has a repeated factor and deg R=d-1, the only possibility is F=P^2 G, with P linear and G squarefree, coprime to P. If G is constant, all target lines lie in P=0, the coplanar case.

Otherwise G has a nonzero partial derivative in every characteristic. In characteristic p, all partials zero would mean G belongs to k[x_0^p,...,x_3^p]; because k is perfect, G would be a pth power, contradicting nonconstant squarefreeness. Choose a nonzero partial D G. For any target line outside P, localizing at its prime shows G lies in p^2; since powers of a linear prime are primary, this membership also holds globally. Therefore D G lies in p. P D G vanishes on lines both outside and inside P, is nonzero, and has degree d-2. Contradiction. Thus outside the coplanar case F is squarefree.

### C2. Nonlinear components
Suppose an irreducible factor Q of squarefree F has degree e>=2. Lemma B gives a nonzero polynomial A of degree e-2 vanishing on its singular curves. A(F/Q) has degree d-2. It vanishes on every target line in another component. For a target line lying in Q but no other component, all other factors are generic units, so Q belongs to its squared line prime. Thus all first derivatives of Q vanish on the line. By the hypersurface Jacobian criterion over the perfect field k, the line is a singular curve of V(Q); A vanishes there too. Contradiction. Hence F is the product P_1...P_d of distinct planes.

### C3. Completeness and exclusion of triple lines
Every target line belongs to at least two planes. Fix i<j. If V(P_i,P_j) is missing from the target, F/(P_i P_j) vanishes on every target line and has forbidden degree d-2. If V(P_i,P_j) belongs to a third plane, the same quotient also vanishes on that line and on all other target lines, again impossible. Therefore all pair intersections are present and no three planes contain a line. There are no other target lines. This is the required pseudostar.

### C4. ACM, without extra general-position assumptions
Let J=(F/P_1,...,F/P_d). Form a d by (d-1) matrix with column i equal to P_i e_i-P_d e_d. Its maximal minors are these generators up to sign. The zero set of J is exactly the union of pairwise plane intersections, so ht J=2. Hilbert–Burch gives a perfect height-two ideal and Cohen–Macaulay quotient R/J.

At any minimal prime (P_i,P_j), all other P_k are units, because no three planes contain a line. J localizes to (P_i,P_j), so R/J is generically reduced. It has no embedded associated primes, hence is reduced. Thus J is the radical ideal I(L), and L is ACM. Coplanar reduced line unions are complete intersections of their plane equation and the product of their distinct line equations in that plane, hence ACM as well.

## D. Additional checks discovered during this turn

Before the stronger Lemma A, two independent characteristic-free boundaries were obtained:

- A degree-e integral surface has at most (e-1)(e-2)/2 distinct singular lines. A general plane gives distinct singular points on an integral plane degree-e curve; normalization's total delta invariant bounds their number by its arithmetic genus. For e<=4, the resulting at most0,1,3 singular lines are contained in a polynomial of degree e-2 by elementary dimension counting. This proves the original conclusion for alpha(I)<=3 independently of Lemma A.
- For cones over integral plane curves, a degree e-2 polynomial through all singular generator lines follows from curve normalization duality and Riemann–Roch in every characteristic.

These partial boundaries are not needed by the complete candidate, but record the genuine progression of this author turn. In a naive dimension-only quintic search, five lines can already exhaust all20 cubic coefficients (5 times4 conditions); the minimum surviving count is five, not six.

The suggested Chiarli–Greco paper does not furnish a positive-characteristic theorem: the retrieved original article text begins with a characteristic-zero hypothesis. Official bibliographic record: https://iris.polito.it/handle/11583/1412696 and DOI10.1090/S0002-9939-96-03126-7. Official AMS PDF fetch returned403; no unverified theorem from it is invoked here.

## Independent-review target

Audit especially: (i) integral pulled-back hyperplane curve despite possible inseparable behavior along the conductor; (ii) pg=0 => Pic^0 smooth and q=dimAlb in every characteristic; (iii) big-nef curve image generates Alb by the quotient/Hodge-index argument; (iv) RR sign and the final lower bound e+g_a-1; (v) canonical injection and finite conductor duality in characteristic p. The earlier TURN1 independent audit does not constitute review of these new arguments. The new proof requires its own independent review before promotion as a verified result.
