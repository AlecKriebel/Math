# A sharp uniform quadratic lifting bound

Problem 30000403 / OWR-1188-004. Author-stage mathematical claim, pending independent review.

## 1. Statement and conventions

Let k be a field of characteristic zero, with algebraic closure kbar. Let G be a finite group and C an r-tuple of nonidentity conjugacy classes, r >= 3. Work over a field containing the field of definition Q_C of the Hurwitz data. Let H(C) be the **inner, coarse** Hurwitz space of connected G-Galois covers of a fixed projective line, including the identification of the deck group with G. Let H^rd(C) be its geometric quotient by postcomposition by PGL_2. For x in H^rd(C)(k), define

    m_k(x) = min { [k(p):k] : p is a closed point of the k-fiber Pi^(-1)(x) }.

Here k(p) is the residue field relative to k. Equivalently, minimize finite degrees [K:k] for which the fiber has a K-rational point; a K-point has residue field contained in K, so both minima coincide. This formulation also applies when x's smallest absolute field of definition is properly contained in k.

**Theorem.** For every such x, m_k(x) <= 2. The constant 2 is optimal uniformly in k, G, C and r. Indeed, it is attained already for k=Q, G=C_2, r=6. If the geometric base stabilizer is V_4, then m_k(x)=1.

This is an optimal universal upper bound. It does not assert that 2 is the best bound after fixing every particular branch number, inertia type, group, or field. For example, some fields and strata have bound 1. The theorem does not compute which of 1 and 2 occurs for every individual x.

The invariant concerns **fields of moduli as marked G-covers**, namely rational points of a coarse space. It is not a claim that a G-cover model always exists over the same degree-2 extension when Z(G) is nontrivial. That further descent obstruction is separate. No centerless hypothesis is needed for the theorem. With Z(G)=1 the usual inner field-of-moduli obstruction vanishes, but that additional fact is not used. We do not change to absolute covers, forget the G-marking, quotient the source independently, or claim positive-characteristic results. In this terminology “non-reduced Hurwitz space” means the space before the PGL_2 quotient, not a nonreduced scheme.

The exact source is Anna Cadoret's contribution to *The Arithmetic of Fields*, Oberwolfach Reports 6/2006, printed pp. 325–328, especially the problem on p. 326. The characteristic-zero and r>=3 conditions come from that contribution. The source explicitly distinguishes coarse points from actual models.

## 2. The normalizer reduction, with cocycle directions fixed

Write H=PGL_2(kbar), acting on geometric points of H(C) on the left. Pick a geometric point p0 above x. Its stabilizer E is finite: it acts faithfully on the r distinct branch points, and a projective linear transformation fixing three distinct points is the identity.

The classical classification of finite subgroups of PGL_2 in characteristic zero gives, after conjugation, a Galois-stable standard representative E. The required list and its normalizers are recorded in Cadoret, Lemma 2.1. Put N=N_H(E) and Q=N/E. For each sigma in Gamma_k choose a_sigma in H such that

    sigma(p0) = a_sigma^(-1) p0.

Both stabilizers are E, so a_sigma belongs to N. Its coset c_sigma=a_sigma E is independent of the choice. Applying sigma then tau to p0 shows

    c_(sigma tau) = c_sigma sigma(c_tau).

Thus c is a continuous Q-valued 1-cocycle. Continuity can be checked over a finite extension defining p0, the finite stabilizer and the finitely many transition maps. The quotient class changes by a coboundary when the normalized representative changes.

The elementary lifting criterion we need is this:

    If b_sigma = h^(-1) sigma(h) belongs to N and b_sigma E=c_sigma
    for some h in H, then h p0 is fixed by Gamma_k.

Indeed, sigma(h p0)=sigma(h) a_sigma^(-1) p0
=h b_sigma a_sigma^(-1) p0=h p0. Equality of cohomology classes is enough: adjust h by an element of N so that the cocycles themselves agree in Q. More explicitly, if p(b_sigma)=q^(-1)c_sigma sigma(q), lift q to n in N and replace h by h n^(-1); its coboundary has quotient c_sigma.

A weaker sufficient condition is [c]=1 in H^1(k,Q). If c_sigma=q^(-1)sigma(q), choose h in N mapping to q. Then h^(-1)sigma(h) has precisely the required quotient. The same statements hold after any finite extension of k. This is a direct coarse-point argument; isomorphisms of source curves need not be selected compatibly.

## 3. Every stabilizer except V_4

We record the cases so that no hidden automorphism hypothesis is needed.

### 3.1 E=1

Now N=Q=H and a_sigma is an actual H-valued cocycle. Its class represents a smooth projective conic B over k, by descent of P^1. Every such conic has a point over an extension K/k of degree at most two: intersect a plane-conic model with a k-line not tangent to it. Such a line exists because k is infinite; the resulting degree-2 zero-cycle has either a k-point or a degree-2 closed point. A smooth conic with a K-point is P^1_K, so the cocycle becomes a coboundary over K. The criterion in section 2 gives a K-point above x.

This uses the index bound for a conic, not the false assertion that every 2-torsion Brauer class over an arbitrary field has index 2. Only classes in H^1(k,PGL_2) occur here.

### 3.2 E=S_4 or A_5

These groups are self-normalizing in H, hence Q=1. The normalized point p0 is already k-rational.

### 3.3 E=A_4 or D_(2n), n>=3

Here D_(2n) has order 2n; V_4 is reserved for n=2. The normalizers are S_4 and D_(4n), respectively. Thus Q is the constant group C_2. The homomorphism c:Gamma_k -> C_2 is killed by an extension K/k of degree at most two, and section 2 applies. We do not need an assumption that this normalizer extension splits over k.

### 3.4 E=C_n, n>=2

Take E={z -> zeta_n^j z}. Its normalizer is

    N = kbar^* semidirect C_2,

where the nontrivial element acts by inversion. The quotient Q has the same Galois-module form, via the map (a,epsilon) -> (a^n,epsilon). Project c to C_2 and pass to the extension K/k of degree <=2 killing this character. Restricted to Gamma_K, c is a kbar^*-valued cocycle. Hilbert 90 makes it a coboundary, hence trivial as a Q-cocycle. Section 2 again gives a K-point.

Together these cases cover all finite stabilizers except V_4.

## 4. The V_4 case: all cubic etale actions have a split realization

Set

    E0 = { z, -z, 1/z, -1/z } subset PGL_2(k).

This group is constant over k. Its normalizer N is geometrically S_4. Conjugation on E0 induces

    N/E0 -> Aut(E0) = S_3,

an isomorphism of Galois groups with action. In detail, the centralizer of E0 in PGL_2(kbar) is E0 itself, and the normalizer realizes all six permutations of the nonidentity involutions. Since E0 is pointwise k-rational, the quotient S_3 has trivial Galois action. The group N itself need not be constant or split as E0 semidirect S_3 over k.

We prove the stronger assertion that **every** c in Z^1(k,S_3) is the image of a coboundary h^(-1)sigma(h) with values in N.

Interpret c as a Galois action on three elements. Choose a separable monic cubic F(T) in k[T] with roots e1,e2,e3 realizing this action. This is possible for every cubic etale algebra, including products: because k is infinite, choose an element whose images under the three geometric embeddings are distinct, avoiding finitely many proper linear subspaces. Its characteristic polynomial has the required roots and action.

Consider the elliptic curve Y^2=F(X), with the k-rational point at infinity as origin. Its three nonzero 2-torsion points are Ti=(ei,0), and their Galois action is c. Translation by Ti commutes with inversion and so descends along X:E -> E/{+1,-1}=P^1_k. The resulting projective transformations, together with the identity, form a Galois-stable subgroup E' of PGL_2(kbar) isomorphic to V_4; its Galois action on nonidentity elements is precisely c.

Everything here can be seen directly. For {i,j,l}={1,2,3}, the descended translation is

    phi_i(X) = ei + (ei-ej)(ei-el)/(X-ei),

represented by

    M_i = [[ei, ej*el-ei*(ej+el)], [1,-ei]].

Its determinant is -(ei-ej)(ei-el), hence nonzero. Its square is scalar, and M_i M_j is projectively M_l. Thus these matrices realize V_4 without needing a point of the elliptic curve beyond the origin. Their coefficients are symmetric in the two roots other than ei, so sigma(phi_i)=phi_(sigma(i)). The supplied symbolic checks verify these identities, but the translation argument proves them independently.

Over kbar all Klein four subgroups of PGL_2 are conjugate, and the normalizer realizes all automorphisms of E0. Consequently we may choose h in H carrying E0 to E' with a chosen labelling of its three nonidentity elements matching the labelling used for c. For e in E0,

    sigma(h e h^(-1)) = h c_sigma(e) h^(-1).

It follows that b_sigma=h^(-1)sigma(h) normalizes E0 and acts on E0 as c_sigma. Under N/E0=Aut(E0), its quotient is exactly c_sigma. It is a PGL_2 coboundary by construction. The criterion in section 2 therefore gives a k-rational point above x.

This proves m_k(x)=1 when E=V_4. It does not incorrectly infer that an abstract section S_3 -> S_4 is Galois-equivariant, and it does not kill the S_3 cocycle by a degree-6 splitting field. The elliptic realization supplies the particular lift whose PGL_2 class vanishes.

Combining sections 3 and 4 proves the universal upper bound 2.

## 5. An exact sharpness example over Q

Let i^2=-1, a=2+2i and b=-(1+i)/4=-1/conjugate(a). In P^1(Q(i)) take the six-element divisor

    D={0, infinity, 1, -1, a, b}.

Let f:X -> P^1 be the smooth projective double cover with affine equation

    y^2 = x (x^2-1) (x-a) (x-b).

The polynomial has five simple roots, so the branch divisor is exactly D, including infinity. The smooth projective curve has genus 2 by Riemann-Hurwitz. This is a connected G=C_2 cover over Q(i), with all six inertia classes the nonidentity class. For a fixed even branch divisor over an algebraically closed field of characteristic zero, its connected double cover is unique up to isomorphism over the target: the quotient of two defining rational functions has even divisor on P^1 and is a square. The C_2-marking is unique. Therefore the base stabilizer of the coarse G-cover point is exactly Stab_(PGL_2)(D).

### 5.1 The stabilizer of D is trivial

For four distinct projective points u,v,w,t, put

    lambda = det(u,w) det(v,t) / (det(u,t) det(v,w)),
    J = 256 (lambda^2-lambda+1)^3 / (lambda^2 (lambda-1)^2).

J is unchanged by projective transformations and by any permutation of the four points. Label the six points 0,1,2,3,4,5 in the order displayed for D. The 15 four-subsets have these exact J-values:

| Four-subset | J |
|---|---|
| 0123 | 1728 |
| 0124 | (5312+35616i)/25 |
| 0125 | (218432-420000i)/169 |
| 0134 | (218432+420000i)/169 |
| 0135 | (5312-35616i)/25 |
| 0145 | 1556068/81 |
| 0234 | (6709952-2630664i)/4225 |
| 0235 | (2516672-631296i)/4225 |
| 0245 | -145793344/114075-1438100576i/342225 |
| 0345 | 290681792/342225-107349152i/114075 |
| 1234 | (2516672+631296i)/4225 |
| 1235 | (6709952+2630664i)/4225 |
| 1245 | 290681792/342225+107349152i/114075 |
| 1345 | -145793344/114075+1438100576i/342225 |
| 2345 | 1111934656/342225 |

They are pairwise distinct. Thus a permutation of D induced by a projective automorphism fixes every four-subset, and hence every complementary two-subset. Any permutation of six points fixing every two-subset fixes every point (intersect {u,v} and {u,w} with v!=w). It is the identity, and a projective transformation fixing three points is identity. This proves the claimed triviality. No approximate numerical comparisons enter this calculation. An independent exact enumeration of the 120 possible images of the ordered triple (0,infinity,1) yields the same result.

### 5.2 Reduced rationality and failure of an ordinary rational lift

The antiholomorphic involution

    tau(z)=-1/conjugate(z)

preserves D, interchanging the three displayed pairs. Its projective-linear part A(z)=-1/z has rational coefficients. Thus A(conjugate(D))=D. Every Galois automorphism over Q acts on Q(i) either trivially or by conjugation, so the reduced C_2-cover class is Q-rational by the uniqueness of the double cover. Call that point x.

Suppose some point above x were R-rational. Its branch divisor would be a real unordered divisor D'=h(D), for some h in PGL_2(C). Standard conjugation j(z)=conjugate(z) preserves D', so rho=h^(-1) j h preserves D. The composition rho tau^(-1) is a projective-linear automorphism preserving D. By section 5.1 it is the identity, so rho=tau.

But rho has fixed points, since it is conjugate to standard conjugation. Tau has none: for a finite fixed point z, z=-1/conjugate(z) would give |z|^2=-1; also tau swaps 0 and infinity. This is a contradiction. Hence the fiber has no R-point and in particular no Q-point. Its original point is defined over Q(i), so

    m_Q(x)=2.

The same argument gives m_R(x_R)=2. Therefore no constant smaller than 2 can bound all source instances.

## 6. Dependencies, limits, and status

The external mathematical inputs are the classical finite-subgroup classification and normalizer list for PGL_2, Hilbert 90, the PGL_2-torsor/conic correspondence, and the stated coarse Hurwitz-space/Galois-action properties. These are standard inputs, not outputs of the finite controls. The proof gives the essential V_4 realization explicitly and the lower bound has a fully rational finite certificate.

This solves the optimal **uniform** degree-bound formulation in the source's characteristic-zero setting. There is no claim of first historical priority: the bounded literature search did not find this exact Hurwitz statement, and neighboring results in arithmetic dynamics and descent of divisors may subsume parts of the argument. Cadoret's paper is credited for the normalizer and obstruction framework. Its manuscript Remark 3.14 explicitly leaves optimality unsettled; its older nonoptimal bounds alone are not a prior resolution.

The author-stage disposition is claimed_solved, 3/5 substantive routes. The stopping exception is a full proof with matching lower bound, reached before a fourth route. This is unrefereed AI-assisted work. Fresh independent adversarial review is required before remote publication. Nothing here is formal proof certification or external human peer review.

## References

1. Anna Cadoret, “Descent theory for covers and rational points on Hurwitz spaces”, in *The Arithmetic of Fields*, Oberwolfach Reports 3 (2006), report 6, contribution pp. 325–328. https://doi.org/10.4171/OWR/2006/06 . Repository record: https://publications.mfo.de/handle/mfo/2936 .
2. Anna Cadoret, *Lifting results for rational points on Hurwitz moduli spaces*, Israel Journal of Mathematics 164 (2008), 19–59. https://doi.org/10.1007/s11856-008-0019-0 . Author manuscript: https://webusers.imj-prg.fr/~anna.cadoret/GPGL2.pdf . Relevant manuscript locators: section 1.1, Lemma 2.1, Lemma 2.3, Proposition 2.4, Corollaries 3.9 and 3.11, Remark 3.14.
