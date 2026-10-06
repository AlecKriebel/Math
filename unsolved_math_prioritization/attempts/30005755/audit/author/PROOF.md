# Canonical decomposition cones and TF equivalence

## Scope and result

The general problem remains unresolved in this investigation. The result proved here is a finite-witness criterion, its elementary semisimple and product consequences, and an exact calculation in a wild one-point-extension example. These are scoped results and reconstructions; no novelty or priority is asserted.

Work over an algebraically closed field k. Morita equivalence transports projectives, presentation decompositions, the pairing and torsion pairs, so passing to a basic algebra does not change the target. Let A be a basic finite-dimensional k-algebra, with indecomposable right projectives P_i and corresponding simples S_i. Put V=K_0(proj A) tensor R. The pairing is <[P], [M]>=dim_k Hom_A(P,M). Thus a projective-coordinate vector w acts on M by w(M)=sum_i w_i dim_k(Me_i). The target vector theta is integral, although every member of its equivalence class is allowed to be real.

For a real weight w define:

- T_w: modules whose every nonzero quotient has strictly positive w-value.
- Tbar_w: modules whose every quotient has nonnegative w-value.
- F_w: modules whose every nonzero submodule has strictly negative w-value.
- Fbar_w: modules whose every submodule has nonpositive w-value.
- W_w=Tbar_w intersection Fbar_w.

The pairs (Tbar_w,F_w) and (T_w,Fbar_w) are torsion pairs. TF equivalence means equality of both torsion pairs, equivalently equality of T_w and Tbar_w. In particular W_w is constant on a TF class. Write F(theta) for this class.

A canonical decomposition is the generic direct-sum decomposition of a two-term projective presentation P^- -> P^+ with [P^+]-[P^-]=theta and no common projective summand in P^-,P^+. The notation theta=u_1 direct-sum ... direct-sum u_s denotes a generic direct-sum decomposition, even when some u_i are not indecomposable. Let ind(theta) be the set of distinct indecomposable weights appearing, and let

C_N(theta)=cone(union over m>=1 of ind(m theta)).

Here cone means finite nonnegative real linear combinations. The symbol ri denotes relative interior in the real linear span, not ambient interior. The zero-cone convention is ri({0})={0}.

The original target is F(theta)=ri C_N(theta), for every integral theta and every such A. The algebraically closed-field hypothesis is part of the primary setting and is not discarded here.

## External mathematical inputs

Only the following established inputs are used in the non-elementary scoped calculation:

1. The generic-decomposition criterion: distinct summand slots u_i are compatible when E(u_i,u_j)=0 for i!=j, where E is the minimum dimension of Hom in the homotopy category into the shift by one. Canonical decompositions are unique up to order. Generic summands are sign-coherent in projective coordinates.
2. If theta=u_1 direct-sum ... direct-sum u_s, then every positive real combination of all these summand weights is TF equivalent to theta. Consequently ri C_N(theta) is contained in F(theta).

References are Derksen–Fei's decomposition theory as stated in Asai–Iyama, Proposition 2.20, and Asai–Iyama, Theorem 3.14 and Corollaries 3.15 and 3.18 [AI]. Positive scaling preserves all four torsion classes directly from their definitions. None of the claims of [HY] is needed for the proofs below.

## 1 A finite witness criterion

Let u_1,...,u_s be weights in a generic direct-sum decomposition of m theta for some positive integer m. Put C=cone(u_1,...,u_s). Suppose there are finite collections of modules Z_j in W_theta, T_l in T_theta, and N_h in F_theta for which the following subset of V is exactly ri C:

R={v: v(Z_j)=0 for every j, v(T_l)>0 for every l, v(N_h)<0 for every h}.

Then F(theta)=ri C and C_N(theta)=C. Hence the original equality holds at theta.

Proof. The generic-decomposition input gives ri C subset F(m theta)=F(theta). If v belongs to F(theta), all Z_j remain semistable, so v(Z_j)=0; all T_l remain in T_v, so v(T_l)>0; and all N_h remain in F_v, so v(N_h)<0. Thus v belongs to R=ri C. This proves equality of the TF class with ri C.

Every canonical summand z of every t theta is in the closure of F(theta): give its summand coefficient value 1 and give all other summands coefficient epsilon>0 in the positive-combination theorem, then let epsilon tend to zero. Since C is finitely generated it is closed, so z belongs to C. Hence C_N(theta) subset C. Conversely each u_i is a sum of canonical summands of m theta, after refining its generic decomposition; hence each u_i belongs to C_N(theta), so C subset C_N(theta). This proves both assertions. The proof does not assume that the u_i are linearly independent. QED.

This is a certificate criterion, not a proof that every theta admits such a finite certificate. Producing it uniformly in the remaining wild cases is an unresolved step.

## 2 Semisimple algebras

For A=k^n and theta=(theta_1,...,theta_n), the TF class consists exactly of the weights having the same coordinate sign pattern, including the same zero coordinates. Indeed, every module is a direct sum of simples, and the four torsion classes are determined by whether each simple's value is positive, zero, or negative.

A projective presentation with disjoint positive and negative supports has zero differential. Its canonical weights are e_i where theta_i>0 and -e_i where theta_i<0, with the respective multiplicities. Multiplication by a positive integer does not alter these directions. Their nonnegative cone has precisely the prescribed signed coordinate orthant as its relative interior. This includes theta=0. Thus the target holds for all semisimple algebras. This elementary calculation is within the already known cases.

## 3 Products preserve the target

Let A=A_1 x A_2 and theta=(theta_1,theta_2). Modules, their submodules and quotients, projectives, and presentation spaces split into the two factors. Membership of a module (M_1,M_2) in any one of the four torsion classes is equivalent to membership of each component in its respective class: necessity follows by taking the component as a quotient or submodule; sufficiency follows from additivity of the weight, with strictness for at least one nonzero component.

Therefore F_A(theta)=F_{A_1}(theta_1) x F_{A_2}(theta_2). Generic decompositions split factorwise, so C_N^A(theta)=C_N^{A_1}(theta_1) x C_N^{A_2}(theta_2). Relative interior commutes with finite Cartesian products. It follows that equality for both factor weights implies equality for their product. This is a reduction, not a solution for a connected wild algebra.

## 4 An exact wild example

### 4.1 Construction

Let Q have vertices 1,2 and three arrows a_1,a_2,a_3 from 1 to 2, and put H=kQ. Define a right H-module X with X_1=X_2=k^3 and arrow maps

F_1=E_12-E_21, F_2=E_23-E_32, F_3=E_31-E_13.

These are maps from X_1 to X_2; using column vectors means the map is left multiplication by the displayed matrix. Let

B = [[k, X], [0, H]],

with the usual one-point-extension multiplication using the right H action on X. This triangular-matrix definition specifies B without relying on a possibly mistranscribed quiver presentation. Its dimension is 1+6+5=12. Use primitive idempotents e_0,e_1,e_2 and projectives P_i=e_iB. Set

p=[P_0]=(1,0,0), g=[P_1]-[P_2]=(0,1,-1), eta=p+g=(1,1,-1).

This is the n=3 instance of the construction in [AI, Examples 5.7 and 5.9]. The algebra is representation-wild because B has the wild three-arrow Kronecker algebra H as a quotient, and inflation is a fully faithful exact representation embedding. It is also nonhereditary: the submodule rad(P_0), supported at vertices 1 and 2, has dimensions (3,3). A projective supported there would have the form P_1^a plus P_2^b, of dimensions (a,3a+b); this would require a=3 and b=-6. Thus rad(P_0) is not projective. Wildness does not by itself imply failure of the conjecture.

### 4.2 A generic decomposition at the second multiple

For a presentation f:P_2^2 -> P_1^2 with arrow matrix [[a_2,a_3],[a_3,a_1]], the induced map Hom_B(f,P_0) is, up to the harmless transpose convention on block indices, the 6 by 6 matrix

M = [[F_2,F_3],[F_3,F_1]].

Its determinant over the integers is 1. For clarity, its rows are

(0,0,0,0,0,-1),
(0,0,1,0,0,0),
(0,-1,0,1,0,0),
(0,0,-1,0,1,0),
(0,0,0,-1,0,0),
(1,0,0,0,0,0).

Thus the map is invertible over every field, including characteristic 2. The homotopy-space formula

Hom_{K^b(proj B)}((P_2^2 -> P_1^2),P_0[1])
 = coker(Hom_B(P_1^2,P_0) -> Hom_B(P_2^2,P_0))

shows E(2g,p)=0. Also E(p,2g)=0 because a degree-zero projective stalk has no degree-zero target in the shifted presentation, and E(p,p)=0. The generic-decomposition criterion therefore gives

2 eta = p direct-sum p direct-sum 2g.

No assertion that 2g is indecomposable is needed. The positive-combination theorem now gives

{a p+b g: a>0,b>0} subset F_B(eta).

### 4.3 Three modules prove the reverse inclusion

The simples S_0 and S_1 belong to T_eta since eta(S_0)=eta(S_1)=1. Consequently any v=(v_0,v_1,v_2) in F_B(eta) satisfies v_0>0 and v_1>0.

Let Y be the inflated H-module with dimension vector (0,1,1), with a_1 acting as the identity and a_2,a_3 as zero. Its submodules have dimension vectors exactly (0,0,0), (0,0,1), and (0,1,1): a nonzero component at vertex 1 forces the entire vertex-2 component because a_1 is the identity. Their eta-values are 0,-1,0. Its quotients have eta-values 0,1,0. Therefore Y is eta-semistable. Every TF-equivalent weight must also make Y semistable, in particular v(Y)=v_1+v_2=0.

We have proved

F_B(eta) = { (a,b,-b): a>0,b>0 }.

Applying the finite witness criterion with u_1=u_2=p, u_3=2g, Z_1=Y, T_1=S_0, T_2=S_1 proves

C_N^B(eta)=R_{>=0}p+R_{>=0}g,
F_B(eta)=ri C_N^B(eta).

No bounded-module enumeration or finite-field experiment substitutes for the all-real reverse inclusion: it is proved by the three displayed modules.

### 4.4 Why a single decomposition gives the wrong cone

For all coefficients x_1,x_2,x_3, the 3 by 3 matrix x_1 F_1+x_2 F_2+x_3 F_3 has determinant zero as an integer polynomial. It has rank 2 whenever at least one coefficient is nonzero, over every field: the corresponding 2 by 2 principal minor is the square of that nonzero coefficient. It follows that E(g,p)=1.

Sign coherence implies that a nontrivial generic decomposition of eta must yield a binary splitting isolating at least one of p, [P_1], or -[P_2]. The three respective obstructions are:

- E(g,p)=1;
- E(p-[P_2],[P_1])=3, since Hom_B(P_0,P_1)=0 but Hom_B(P_2,P_1)=k^3;
- E(-[P_2],p+[P_1])=6, since the source is a degree-minus-one stalk and Hom_B(P_2,P_0+P_1) has dimension 3+3.

Each is nonzero, so eta is generically indecomposable. Thus cone(ind eta)=R_{>=0} eta is strictly smaller than the two-dimensional C_N^B(eta). For instance p belongs to C_N^B(eta) but not to R_{>=0} eta.

Moreover E(eta,eta)>0. Otherwise eta direct-sum eta would be a generic decomposition of 2eta. Uniqueness of canonical decomposition would contradict the established generic decomposition p direct-sum p direct-sum 2g: after canonical refinement, the latter contains p, while the former consists of two copies of the indecomposable eta. Hence eta is a wild weight and fails the ray condition. The double is enough to witness this failure. This recovers the known obstruction while separately verifying the desired multiple-cone equality in the example.

## 5 Exact remaining gap and geometric safeguards

The missing general assertion is the reverse inclusion F(theta) subset ri C_N(theta), for arbitrary integral theta of a finite-dimensional algebra over an algebraically closed field. Already proved hereditary cases may include representation-wild algebras; the words 'wild algebra' alone do not identify the unresolved scope. The calculation above does not produce a universal finite family of semistable witnesses or torsion-sign witnesses.

Relative interior, closure, and rational-point agreement are distinct. Two elementary models explain why a proposed proof cannot silently replace one with another. They are convex-geometric countermodels only, not asserted TF classes.

1. Put v=(0,1,sqrt(2)) in R^3 and F={a e_1+b v: a>0,b>=0}. This is convex and positively homogeneous, contains the rational vector e_1, and has two-dimensional span. Its rational points all have b=0, so they lie in the single ray R_{>0}e_1 and are not dense in F. Merely having a rational point does not permit a density argument in the full span.
2. Let C=R_{>=0}^3, r=(1,sqrt(2),0), and F=R_{>0}^3 union R_{>0}r. This F is convex and positively homogeneous, has closure C and relative interior ri C, and F intersection Q^3=(ri C) intersection Q^3. Yet F is strictly larger than ri C. Indeed the additional ray has no rational nonzero point. Thus even full rational-point agreement, equal closures and equal relative interiors do not by themselves eliminate real boundary points.

A finite-witness proof avoids both issues, but its hypotheses have only been supplied in scoped settings here. Statements in newer literature about the relative interior of a TF class must retain that qualification. This report neither refutes the original conjecture nor claims a general proof.

## References

[OWR] Osamu Iyama, joint work with Sota Asai, Semistable torsion classes and canonical decompositions in Grothendieck groups, in Cluster Algebras and Its Applications, Oberwolfach Reports 2/2024, pp. 123–125, Conjecture 2. https://doi.org/10.4171/owr/2024/2

[AI] Sota Asai and Osamu Iyama, Semistable torsion classes and canonical decompositions in Grothendieck groups, Proceedings of the London Mathematical Society 129 (2024), e12639. https://doi.org/10.1112/plms.12639 ; author preprint https://arxiv.org/abs/2112.14908v3

[HY] Mohamad Haerizadeh and Siamak Yassemi, The cones of g-vectors, arXiv:2501.15822v3, submitted 19 June 2026. https://arxiv.org/abs/2501.15822v3
