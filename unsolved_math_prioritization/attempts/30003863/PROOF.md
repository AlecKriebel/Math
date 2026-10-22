# Partial extension theorems and exact counterexample certificates

Problem 30003863 / OWR-16169-010. Public proof-only edition, 10 October 2026.

The accompanying [mathematical audit](MATHEMATICAL_AUDIT.md) accepts the scoped partial results. The full equivalence remains unproved here. This AI-assisted manuscript and audit are unrefereed; acceptance does not mean external human peer review, journal acceptance, or formal proof-assistant certification.

## 1. Target and status

Let k be an algebraically closed field of characteristic zero. The fixed ambient pair (P,S) is one of:

- an integral normal hypersurface of polynomial degree d=1, 2, or 3 in P^3, with only Du Val singularities;
- a Du Val quartic in P(1,1,1,2);
- a Du Val sextic in P(1,1,2,3).

Put U=P\S. The target asks whether absence of an anticanonically polar cylinder on S is equivalent to every automorphism of U extending to an automorphism of P preserving S. Restriction Aut(P,S) -> Aut(U) is injective because U is dense. The equality in the question means surjectivity of this restriction, for this fixed ambient P.

**This note does not prove or disprove that equivalence.** It proves elementary restrictions and complete extension results for specified subgroups, and gives exact symbolic certificates for checking proposed counterexamples. In particular, no argument below establishes that an arbitrary automorphism preserves a projection pencil. No novelty or priority is claimed for the partial results.

Polynomial degree must not be confused with (-K_S)^2. A plane has anticanonical degree 9, a quadric has degree 8, a cubic has degree 3; the weighted quartic and sextic have anticanonical degrees 2 and 1.

## 2. Precisely credited prior results

The originating statement is Park's Conjecture 5 in the Oberwolfach report [OWR], pp. 1728–1730. The following are prior theorems, not results first established in this note:

1. A polar cylinder on S gives a cylinder, hence a nontrivial additive-group action, on U, and implies Aut(U) != Aut(P,S). See [CDP], Theorem C and Corollary 4.10.
2. For smooth S of anticanonical degree 1, every complement automorphism extends. For smooth anticanonical degrees 2 and 3, [CDP, Theorem 4.1] excludes nontrivial connected algebraic group actions; it does not classify all automorphisms.
3. The cylinder-free anticanonical-degree-at-most-three cases are: smooth cubics; degree-two surfaces with only A1 singularities, if any; and degree-one surfaces with only A1, A2, A3, D4 singularities, if any. See [CDP, Theorem 4.3] and [Park, Theorem 1.5].
4. [Park, Corollary 3.2] proves the neighboring equivalence between a polar cylinder on S and a cylinder on U. This is not the full extension assertion.
5. The stronger extension assertion remains Conjecture 4.24 in the published 2021 survey [CPPZ]. [BPV, 2024, p.734] still explicitly leaves the smooth-cubic extension question unresolved. These dated statements do not certify worldwide current openness.

For clarity, the last step in the cylinder direction can be checked without invoking rigidity. If A=k[U] admits a nonzero locally nilpotent derivation delta, then trdeg_k ker(delta)=2. Given any N, choose k-linearly independent f_1,...,f_N in ker(delta). The commuting derivations f_i delta integrate to a faithful action of G_a^N: exp((sum t_i f_i)delta). Faithfulness follows because a nonzero locally nilpotent derivation has a nonidentity exponential in characteristic zero. The finite-dimensional algebraic group Aut(P,S) cannot contain all these groups. Thus some automorphism of U is nonambient. This argument does not reverse: failure of additive actions does not exclude isolated or discrete automorphisms.

## 3. Elementary degree and Jacobian restrictions for cubic complements

### Theorem 3.1

Let F in k[x_0,x_1,x_2,x_3] be any irreducible homogeneous cubic, and let phi be an automorphism of U=P^3\V(F). Represent its unique birational extension to P^3 by homogeneous polynomials G=(G_0,...,G_3) of common degree m with gcd(G_0,...,G_3)=1. Then:

(a) F(G)=a F^m for a nonzero scalar a.

(b) det(DG)=b F^{4(m-1)/3} for a nonzero scalar b. In particular m=1 mod 3.

(c) If m=1, phi extends to a projective linear automorphism preserving S. If m>1, the birational extension contracts S, and contracts no other prime divisor. Hence every nonambient automorphism has m>=4. The same conclusions apply independently to the reduced degree n of its inverse.

#### Proof

The reduced tuple G has no common zero on U: a regular map represented by a reduced tuple can have no removable base locus in a smooth variety. Explicitly, near a point where a target coordinate is nonzero the tuple is a local scalar times regular coordinates, one of which is a unit. A common zero would therefore give a common local divisor, contradicting the absence of a common global prime factor. Thus G defines a map on the affine open F!=0 in A^4, and F(G) is nonzero there. Units of k[x_0,...,x_3,F^{-1}] are precisely c F^r. Homogeneity of F(G), of degree 3m, proves (a).

The differential of G is invertible at each point with F!=0. On the quotient by the radial tangent direction it induces the invertible differential of phi; the radial direction is sent, by Euler's identity, to mG, which is nonzero in characteristic zero. Consequently det(DG) has no zeros off V(F). Its degree is 4(m-1), so the same unit argument gives (b), including divisibility by 3.

A reduced degree-one birational tuple is an invertible linear tuple. Conversely, suppose m>1 and S were mapped dominantly to a divisor. That divisor must be S, by (a). A birational map between normal varieties mapping a divisor dominantly to a divisor identifies the corresponding discrete valuation rings at their generic points. Its multiplicity on that divisor is therefore one. Choose a target coordinate G_j nonzero at the generic point of the source S. The pullback of the local equation F/x_j^3 is a F^m/G_j^3, whose order along S is m, a contradiction. Thus S is contracted. Every other prime divisor meets U, on which phi is an isomorphism, so none is contracted. This proves (c). ∎

This congruence is stronger in this particular dimension and degree than mere invertibility of m modulo 3. The general homogeneous lifting and composition framework is also in [BPV, Proposition 2.1 and Remarks 2.2–2.3]; the proof here includes the additional Jacobian argument rather than assuming that liftability proves linearity.

### Theorem 3.2: the first possible degree cannot contract a smooth cubic to a point

Suppose S is smooth and m=1+3q>1. If phi contracts S to a point, then q>=2, so m>=7. In particular a reduced degree-four nonambient automorphism would have to contract S to a curve.

More precisely, if the image is a point z, choose regular parameters y_1,y_2,y_3 at z with S=(y_1=0). Then

q >= ord_S(phi^*y_2)+ord_S(phi^*y_3) >= 2.

If the image is a curve C, and y_2 is a local equation of C inside S at its generic point, then q>=ord_S(phi^*y_2). Thus degree four forces this latter order to be exactly one.

#### Proof

Work on source and target affine coordinate charts containing the relevant generic points. The determinant of the projective differential has order 4q along the source S. Indeed the standard homogeneous-coordinate calculation gives, up to a nonzero sign,

Jac(phi)=det(DG)/(m G_j^4)

on a source chart x_i=1; G_j is a unit at the generic point of S. The pullback of y_1 has order m=1+3q.

For functions h_i=t^{a_i}u_i along a smooth divisor t=0, each term in dh_1 wedge dh_2 wedge dh_3 has order at least a_1+a_2+a_3-1: at most one factor can supply dt. If the center is a point, a_2,a_3>=1. Hence

4q >= (1+3q)+a_2+a_3-1,

which gives the claim. At a generic curve center one uses a third coordinate with order zero and obtains 4q>=(1+3q)+a_2-1, or q>=a_2. ∎

The theorem does not exclude a degree-four contraction onto a curve, nor higher-degree maps. It is not a proof of the conjecture.

### Corollary 3.3: a finite inverse-degree list at the first possible degree

For reduced forward and inverse degrees m,n of a birational map of P^3, n<=m^2 and m<=n^2. Consequently, if a nonambient cubic-complement automorphism has degree four, its inverse degree lies in the explicit list

4, 7, 10, 13, 16.

#### Proof

A general target line avoids the inverse base locus, which has codimension at least two. Its image under the inverse map is therefore a rational curve of degree n: the inverse homogeneous tuple restricts to a basepoint-free degree-n parametrization of that curve, birationally onto its image. This curve is a component of the complete intersection of the two degree-m equations pulling back the two general planes defining the target line. Those equations have no common divisorial component, since the forward tuple is primitive and dominant. Bezout gives n<=m^2. Exchange the maps for the other inequality. The stated list follows from n>1 and n=1 modulo 3. ∎

This makes the first nonlinear degree a finite list of coefficient-system problems once F is fixed. No infeasibility result for those systems is claimed.

## 4. Complete fiberwise extension theorem for smooth cubic complements

For a point p in P^3, let pi_p:P^3 -->> P^2 be linear projection from p. Define

K_p={phi in Aut(P^3\S): pi_p o phi=pi_p as rational maps}.

The equality here fixes the base pointwise; it does not merely require preservation up to an arbitrary birational transformation of the base.

### Theorem 4.1

For every smooth cubic S and every p in P^3, each element of K_p extends to P^3 preserving S. More explicitly, in coordinates p=[0:0:0:1], u=(x_0,x_1,x_2), t=x_3:

1. If p belongs to S, write F=L(u)t^2+Q(u)t+C(u), where L,Q,C have degrees 1,2,3 and L!=0. If L does not divide Q, then K_p is trivial. If Q=L M with M linear, K_p has order two and its nonidentity element is

   [u:t] -> [u:-t-M(u)].

2. If p does not belong to S, scale F to write F=t^3+L(u)t^2+Q(u)t+C(u). Put v=t+L/3, so F=v^3+A(u)v+B(u). If A!=0, then K_p is trivial. If A=0, then K_p is the order-three group v -> zeta v, zeta^3=1, with u fixed.

#### Proof

Set K=k(P^2). Irreducibility of F implies irreducibility of the appropriate degree-two or degree-three polynomial in t over K, by dehomogenizing on a base chart and using Gauss's lemma. An automorphism in K_p induces an automorphism of the generic affine fiber with the roots of this polynomial removed. Any automorphism of this open rational curve extends uniquely to an automorphism of its smooth projective completion P^1_K. Among the missing points, infinity is the only K-rational point, since the polynomial is irreducible of degree at least two. Thus infinity is fixed and the automorphism is affine, t -> a t+b, with a in K^* and b in K.

This generic-fiber conclusion is valid also when p lies in U: away from the single points p and phi^{-1}(p), the maps to the base are regular, and neither of those closed points dominates the base. They do not affect the generic fiber. Equivalently, a complement automorphism preserving every line through p fixes their common point p whenever p belongs to U.

For a quadratic, an affine permutation of its two roots is either the identity or t -> -t-Q/L. This is an automorphism of the complement only when Q/L is a polynomial. To see the necessity directly, if L does not divide Q, the reduced projective formula is

[L u_0:L u_1:L u_2:-L t-Q].

It maps a dense open subset of the plane L=0 to p. That plane has a dense open subset in U because the irreducible cubic S is not a plane. Since p is in S, the map cannot be an automorphism of U. If Q=L M, the formula cancels to the asserted linear involution, which preserves F. This proves (1). The condition is the familiar Eckardt-point case, but no classification of Eckardt points is needed for the proof.

For the cubic, the centered roots of v^3+A v+B have sum zero. An affine permutation v -> a v+b therefore has b=0. Comparing the cubic with its transform gives

(a-a^3)A=0,  (1-a^3)B=0.

Here B!=0; otherwise the polynomial factors by v. Thus a^3=1. If A!=0, also a^2=1, hence a=1. If A=0, all three cube roots of unity give automorphisms. These roots lie in k, and v=t+L/3 is a linear change of projective coordinates, so all the resulting maps are projective linear. ∎

**Exact remaining gap.** The argument proves extension after the additional equation pi_p o phi=pi_p. There is no proof here that an arbitrary complement automorphism satisfies this equation for any p. Even its preservation of some projection pencil is not established.

## 5. Complete kernels for the natural weighted double-cover projections

### Lemma 5.1: the square coefficient

In each of the specified Du Val weighted models, the coefficient of w^2 is nonzero, where wt(w)=2 for P(1,1,1,2), and wt(w)=3 for P(1,1,2,3).

#### Proof

Suppose that coefficient vanishes, so S contains the w-coordinate vertex p. Its index chart is the quotient A^3/mu_r, with r=2 and weights (1,1,1), or r=3 and weights (1,1,2). The surface lifts to an invariant hypersurface T=(f=0) through the origin, where f is obtained by setting w=1. These cyclic groups act freely away from the origin. Since S is normal and the cover is etale away from p, T is normal away from its origin; being a generically reduced hypersurface, it is S2 and hence normal by the codimension-one criterion. Its dualizing module is free, with the residue generator carrying character a+b+c modulo r. The equation is invariant, so this character is 1 modulo r in both cases.

If S were Gorenstein at p, a local generator of its canonical line bundle would pull back to an invariant generator of the canonical module of T away from the origin, and then over the origin by normality. Every generator differs from the residue generator by a unit. Such a unit has a nonzero constant value at the fixed origin, so cannot cancel a nontrivial character. This is a contradiction. Du Val singularities are Gorenstein, proving the lemma. ∎

Consequently, after scaling the equation and completing a square, the two surfaces can be written as

F=w^2+B_4(x,y,z)  in P(1,1,1,2),

F=w^2+B_6(x,y,z)  in P(1,1,2,3),

where B has the indicated weighted degree. Completing the square is an automorphism of the same fixed weighted ambient space.

### Theorem 5.2

Let pi forget w, with bases P^2 and P(1,1,2), respectively. In either model,

{phi in Aut(P\S): pi o phi=pi} = {1, w -> -w}.

In uncompleted-square coordinates F=w^2+A w+B, the nonidentity map is w -> -w-A. Thus every member of this specified kernel extends to the fixed weighted ambient space, including for singular Du Val S.

#### Proof

On the base chart x!=0 use the weight-zero fiber coordinate W=w/x^r, where r=wt(w). The generic fiber of P minus the w-vertex is A^1 over the function field of the base. Its intersection with U removes the two roots of an irreducible quadratic: irreducibility follows from integrality of S on this dense chart. Every fiberwise automorphism acts on this punctured affine line. In its P^1 completion the point at infinity is the only rational missing point, so it is fixed. The affine transformation therefore either fixes both quadratic roots or exchanges them. The only possibilities are the identity and W -> -W after completing the square. Both extend by their displayed weighted homogeneous formulas to P and preserve S. ∎

As in Theorem 4.1, this computes a kernel. It does not say that arbitrary automorphisms preserve pi or act trivially on its base.

## 6. Necessary and sufficient polynomial certificates in the cubic case

### Proposition 6.1

For a fixed irreducible cubic F, a proposed nonambient complement automorphism can be certified by the following finite data:

- homogeneous tuples G,H of positive common degrees m,n, respectively;
- nonzero scalars a,b,c,d;
- the integer s=(mn-1)/3;
- the four exact identities

  F(G)=a F^m,                 F(H)=b F^n,
  H_i(G)=c x_i F^s,           G_i(H)=d x_i F^s   (0<=i<=3).

Together with gcd(G_0,...,G_3)=1 and m>1, these identities prove that [G] is a nonambient automorphism of P^3\V(F). Conversely, every nonambient automorphism admits such data, with m,n=1 mod 3 and m,n>=4.

#### Proof

The first two identities ensure G and H have no simultaneous coordinate zero on F!=0 and map that set into itself. The two composition identities give mutually inverse projective maps there. A primitive tuple of degree greater than one cannot represent a projective linear automorphism. Conversely choose reduced homogeneous tuples for an automorphism and its inverse. Theorem 3.1 supplies the first two identities. Each composite tuple represents the identity, so H_i(G)=K x_i and G_i(H)=K' x_i with homogeneous polynomials K,K'. These are polynomial, not merely rational, because the x_i are pairwise coprime. They are nonzero off F=0, since both maps are defined and inverse there. Hence they are scalar powers of F. Comparison of degrees gives the displayed exponent s. ∎

The inverse identities are essential. Checking only a Jacobian power, only F(G)=a F^m, or many evaluations at sampled points is not a counterexample certificate. Also a tuple x_i F^q represents the identity despite its artificially large degree. Primitive normalization is essential.

This reduces a proposed counterexample to an independently checkable finite computation; it does not prove that no such data exist for smooth cubics. The exact control identities are displayed below and can be checked by substitution. Recorded symbolic checks covered those controls, not an exhaustive search through the unbounded degrees. No claim here requires an omitted program or raw output.

## 7. Explicit controls and the low-degree models

### Plane

For S=(x_3=0), its complement is A^3. The triangular automorphism (X,Y,Z)->(X+Y^2,Y,Z) has reduced projective tuple

(x_0 x_3+x_1^2, x_1 x_3, x_2 x_3, x_3^2)

of degree two and is nonambient. On S=P^2, deleting a line gives A^2; the effective divisor three times that line is anticanonical. Thus both sides of the proposed equivalence are false for the plane, as required.

### Quadrics

Every integral normal quadric over k has rank three or four. Use F=x_0 x_1-x_2 x_3 in rank four and F=x_0 x_1-x_2^2 in rank three.

For rank four the tuple

(F x_0, F x_1+x_3 x_0^2, F x_2+x_0^3, F x_3)

and the tuple with the two plus signs changed to minus signs define inverse nonambient automorphisms of the complement.

For rank three use

(F x_0, F x_1, F x_2, F x_3+x_0^3),

again with inverse obtained by changing the plus sign. All tuples are primitive of degree three. Each has F(G)=F^3; the compositions equal x F^4. On either quadric, x_0!=0 is A^2. If H is the hyperplane divisor (x_0=0), then 2H is anticanonical and has the same support. Thus both sides are false for both quadric types, as required. The rank-three vertex is an A1 singularity.

### A singular cubic positive control, not a counterexample

Take F=x_0 x_1^2+x_1 x_2^2+x_3^3. It is irreducible: as a degree-one polynomial in x_0, its coefficient x_1^2 and constant term x_1 x_2^2+x_3^3 are coprime. The four partial derivatives show that its only singular point is [1:0:0:0]. An integral hypersurface surface with isolated singularities is normal, by the codimension-one and Cohen–Macaulay criteria. In that affine chart the equation is y^2+y z^2+w^3; changing Y=y+z^2/2 gives Y^2+w^3-z^4/4, the E6 Du Val normal form. Also S intersect (x_1!=0) is A^2: on x_1=1 the equation solves as x_0=-x_2^2-x_3^3. Thus deleting the anticanonical hyperplane divisor x_1=0 is a polar cylinder.

The locally nilpotent derivation delta=2x_2 partial/partial x_0-x_1 partial/partial x_2 fixes F and x_1. On F!=0, exponentiate (x_1^3/F)delta. Clearing denominators gives the primitive degree-seven tuple

G=(F^2 x_0+2F x_1^3 x_2-x_1^7, F^2 x_1,
   F^2 x_2-F x_1^4, F^2 x_3).

Its inverse H changes the sign of 2F x_1^3 x_2 and of -F x_1^4, while leaving the -x_1^7 term unchanged. The exact certificates are

F(G)=F^7, F(H)=F^7,
H(G)=x F^16, G(H)=x F^16,
det(DG)=det(DH)=7 F^8.

This confirms that the certificate system accepts genuine nonambient automorphisms inside the original Du Val scope. It cannot refute the conjecture because this S has the explicit polar cylinder just given.

### Smooth cubic control

For the Fermat cubic F=sum x_i^3, interchange x_0 and x_1. This degree-one involution is ambient. The artificial degree-four presentation x_i F is nonprimitive, since F is a common factor; it therefore cannot supply a counterexample certificate. Recorded symbolic checks also rejected this degree inflation.

## 8. What has and has not been established

Established by proof here:

- direct cylinder and nonextension examples for every plane/normal-quadric model;
- the cubic degree/Jacobian restrictions, the point-contraction lower bound, and the degree-four inverse-degree list {4,7,10,13,16};
- full extension in every pointwise line-projection kernel for smooth cubics;
- full extension in the natural pointwise double-cover projection kernels for the two weighted families;
- finite necessary-and-sufficient algebraic certificates for a proposed cubic counterexample, with exact controls.

Unestablished:

- extension for arbitrary smooth cubic complement automorphisms;
- extension for arbitrary cylinder-free weighted degree-two or singular degree-one complement automorphisms;
- an intrinsic characterization of one of the projection pencils forcing arbitrary automorphisms to preserve it;
- a bound on the degrees of all complement automorphisms;
- impossibility of the certificate system in all nonlinear degrees for smooth F.

The strongest justified mathematical status is **unsolved, with rigorous partial results**. The complete proof and the accompanying audit preserve the distinction between pointwise projection kernels and arbitrary automorphisms. No novelty or priority is claimed. The recorded computational controls are supplementary: the theorem statements, proofs, polynomial certificate criterion, and explicit control identities are all displayed in this proof-only edition. Programs, raw outputs, datasets and copied source documents are not distributed. Edition preparation rechecked frozen byte identities and publication integrity, without new scholarly retrieval, source-text inspection, literature search, or rerunning the original mathematical programs.

## References

[OWR] J. Park, joint work with I. Cheltsov and A. Dubouloz, *Automorphism groups of the complements of hypersurfaces*, in *Subgroups of Cremona Groups*, Oberwolfach Report 28/2018, pp.1728–1730. https://doi.org/10.4171/owr/2018/28 ; primary PDF https://ems.press/content/serial-article-files/46750

[CDP] I. Cheltsov, A. Dubouloz, J. Park, *Super-rigid affine Fano varieties*, Compositio Mathematica 154 (2018), 2462–2484. The locally verified version is arXiv:1712.09148v1. https://arxiv.org/abs/1712.09148

[Park] J. Park, *Ga-Actions on the Complements of Hypersurfaces*, institutional manuscript, Theorem 1.5 and Corollary 3.2. https://cgp.ibs.re.kr/files/preprints/CGP18017_JHP_Ga-Actions%20on%20the%20complements%20of%20hypersurfaces.pdf ; byte identity is recorded in [SOURCE_METADATA.json](SOURCE_METADATA.json).

[CPPZ] I. Cheltsov, J. Park, Y. Prokhorov, M. Zaidenberg, *Cylinders in Fano varieties*, EMS Surveys in Mathematical Sciences 8 (2021), 39–105, section 4.2. https://doi.org/10.4171/EMSS/44 ; primary PDF https://ems.press/content/serial-article-files/37019

[BPV] J. Blanc, P.-M. Poloni, I. Van Santen, *Complements of hypersurfaces in projective spaces*, Journal de l'Ecole polytechnique — Mathematiques 11 (2024), 733–768. https://doi.org/10.5802/jep.264 ; primary PDF https://www.numdam.org/item/10.5802/jep.264.pdf
