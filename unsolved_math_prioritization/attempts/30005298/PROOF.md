# General Weddle dimensions: an incidence-and-pencil argument

Problem 30005298 / OWR-11695864-003.

**Disposition:** accepted partial dimension results, with the scoped mathematical audit in [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md). AI-assisted and unrefereed; this is not external human peer review, journal acceptance, or formal proof-assistant certification. The original all-parameter problem remains OPEN. No priority claim is made. All statements below concern the reduced closed jumping locus, not its degree, multiplicities, Cohen–Macaulay property, or irreducibility.

## 1. Conventions and statements

Work over C. Integers n,d,r are positive. “General r points” means that the ordered tuple belongs to a specified nonempty Zariski-open subset of the distinct-point configuration space in (P^n)^r; the conclusions are invariant under permutation, and hence also hold for unordered general sets. The open subset may depend on n,d,r. Write

N_j(n) = binomial(j+n-1,n-1), N=N_d(n), D=n+N-1.

For Z={z_1,...,z_r}, let

δ_Z(P)=dim_C (I(Z) ∩ I(P)^d)_d, for P outside Z,

and let W_d(Z) be the Zariski closure in P^n of the locus where δ_Z(P) exceeds its generic minimum. We write “empty” rather than assign a dimension to the empty set.

### Theorem A: the supercritical range

For every n≥2,d≥2, and general r points Z in P^n with r≥N,

- if N≤r≤N+n−1, then W_d(Z) is nonempty and dim W_d(Z)=n+N−r−1;
- if r≥N+n, then W_d(Z) is empty.

### Theorem B: one point below the square case

For every n≥3,d≥2, and general r=N−1 points Z in P^n,

**dim W_d(Z)=n−2.**

In particular, for n=3 this gives dimension 1 without an expected-codimension assumption. This is the locus-dimension assertion underlying Conjecture 5.4 in [WS], rather than an assertion about its possibly nonreduced scheme. Section 5 below supplies the proof, including the common-factor strata.

### Corollary C: complete dimension classification in P^3

For every d≥2 set N=binomial(d+2,2). For general r≥1 points in P^3:

| r | W_d(Z) |
|---|---|
| 1 | empty |
| 2≤r≤N−1 | dimension 1 |
| N | dimension 2 |
| N+1 | dimension 1 |
| N+2 | dimension 0, nonempty |
| r≥N+3 | empty |

This determines the dimension, not the components or degree, in P^3. For example, the cubic locus of eight general points can have both curve and isolated-point components without contradicting the table.

### Theorem D: elementary edge regimes

1. In P^1, W_d(Z) is empty for all positive d,r.
2. For d=1 in P^n, W_1(Z) is empty when r=1 or r≥n+1; when 2≤r≤n, it equals the projective span of Z and has dimension r−1.
3. For n≥2,d≥2 and 2≤r≤d+1, W_d(Z) is exactly the union of the lines joining pairs of points of Z, and has dimension 1. For r=1 it is empty.
4. In P^2 and d≥2 the full answer is: dimension 1 for 2≤r≤d+1; dimension 0 for r=d+2; empty for r=1 or r≥d+3. At r=d+2 the locus consists of the 3*binomial(r,4) distinct intersections of secants with disjoint pairs of endpoints, for general Z.

The remaining all-parameter dimension question includes n≥4,d≥2 and d+2≤r≤N_d(n)−2, insofar as not otherwise settled. This range is a conservative residual, not a claim that every one of its parameter values is independently open.

## 2. Basic facts used, with the needed scope

We use ordinary dimension theory of algebraic varieties: a projective bundle of rank a over a b-dimensional base has dimension a+b−1; Gr(2,a) has dimension 2(a−2); a morphism has generic fiber dimension dim(source)−dim(image) on each irreducible component; and an intersection of subvarieties in a smooth ambient variety has each component of dimension at least the sum of dimensions minus the ambient dimension. All applications below are to finite-type varieties and finite unions of explicitly indexed strata. Thus every assertion for general tuples follows by removing finitely many proper closed subsets and using generic fiber dimension. No assertion of uniform genericity over infinitely many n,d,r is needed.

**Generic minimum.** For general Z,

δ_Z(P_gen)=max(N−r,0).                                                (2.1)

To prove this, fix a center P and identify the degree-d forms vanishing to order d at P with degree-d forms on P^{n−1}. Projection of general points from this fixed P gives general points of P^{n−1}. General points impose independent conditions on a finite-dimensional space of forms until that space is exhausted: inductively, a nonzero remaining form does not vanish everywhere, so the next point can be chosen not to annihilate the entire remaining space. Maximal rank is open. The same rank condition on the product of configurations and centers gives (2.1) for general Z and general P. In particular, existence of a cone is the jumping condition only when r≥N.

**The evaluation bundle.** Let V=C^{n+1}. On P(V), let E_d have fiber Sym^d((V/CP)^*) at P. It has rank N and is a subbundle of the trivial bundle Sym^d(V^*). Its fibers are exactly the degree-d forms in I(P)^d. Fix representatives for the z_i. Evaluation gives a bundle map

E_d → O^{r},   F ↦ (F(z_1),...,F(z_r)).                              (2.2)

Its kernel at P is the cone space defining δ_Z(P), including at P∈Z when used only as an auxiliary extension. Local trivializations give an r×N matrix of regular functions. We impose the jumping condition on P^n\Z first and take its closure afterward.

**Rank-locus dimension bound.** If an r×N matrix on a smooth n-dimensional variety has r≥N, then every nonempty component of the locus of rank at most N−1 has dimension at least n−(r−N+1). Indeed, the universal rank-at-most-N−1 determinantal variety in the affine space of r×N matrices has codimension r−N+1. Intersect its product with the domain with the graph of the matrix-valued map, and use the intersection inequality in the smooth product. For r=N−1, its maximal-rank-drop locus similarly has codimension at most 2. This is an upper bound on codimension, not a claim that equality occurs for a structured matrix.

**Secant inclusion.** If 2≤r≤N, then for general Z every secant line joining two points lies in W_d(Z). Off Z, projection from such a line identifies at least two of the points. Hence evaluation has rank at most r−1 and δ_Z(P)≥N−r+1, strictly greater than (2.1). The union is nonempty and has dimension 1.

## 3. A uniform cone-incidence bound

For any e≥1 set N_e=N_e(n). The projective bundle B_e=P(E_e) parameterizes pairs (P,[F]) where F is a nonzero degree-e cone with vertex P. It has dimension

D_e=n+N_e−1.

For s ordered points define

T_{e,s}={(P,[F],z_1,...,z_s): F(z_i)=0 for every i}.

Over any (P,[F]), the fiber is the s-fold product of the degree-e hypersurface V(F), so has dimension s(n−1), including when F is reducible or nonreduced. Therefore

dim T_{e,s}=D_e+s(n−1).

This is a dimension statement about the whole incidence, not an irreducibility assertion. Every irreducible component has dimension at most this value; reducible or nonreduced cones do not require that their r-fold products be irreducible. All later generic-fiber bounds are applied componentwise and need no irreducibility of T_{e,s}.

Projecting to (P^n)^s and applying generic fiber dimension componentwise proves:

**Lemma 3.1.** For general s points, the family of vertex-marked degree-e cones through them has dimension at most D_e−s, or is empty. In particular, it is empty if s>D_e.

The word “at most” allows non-dominant components to be omitted for general configurations. No genericity of a rectangular matrix is being asserted. The bound is deliberately not sharp for e=1: independently, n+1 general points of P^n lie on no hyperplane. In the special case n=3,e=1 we will use the sharper fact s≤3.

For any fixed finite r and degrees e≤d−1, general r-tuples have the conclusion of Lemma 3.1 for every subset, simultaneously. There are only finitely many such subsets and degrees. This simultaneous statement is essential in the factor stratification below.

## 4. Proof of Theorem A

Assume n≥2,d≥2 and r≥N. Put B=B_d, dim B=D. The total incidence T_{d,r} gives the upper bound

dim B_Z≤D−r                                                     (4.1)

for general Z, where B_Z is the family of vertex-marked cones through Z. If r>D the same incidence shows B_Z is empty for general Z, proving the empty range.

Suppose N≤r≤D. We must prove a cone with vertex outside Z exists; this is not supplied by a dimension count alone.

Let K be the image of B under the projective map (P,[F])↦[F] in the projective space of all degree-d forms on P^n. Then K is projective and dim K=D. To justify the last equality, choose a cone over a smooth degree-d hypersurface in P^{n−1}. It has singular locus exactly its vertex P. (For n=2 the base is d distinct points of P^1, and the cone is d distinct concurrent lines, still with unique singular point.) Every vertex of a degree-d cone for d≥2 is singular; hence this example has exactly one vertex. Generic fiber dimension of the map B→K is zero, so dim K=dim B=D.

Each condition F(z_i)=0 is a hyperplane condition in the projective space of forms. The projective dimension theorem implies that K intersected with r such hyperplanes is nonempty of dimension at least D−r. Its preimage B_Z therefore has dimension at least D−r.

We now exclude the possibility that all these vertex-marked cones have P∈Z. For a fixed index i consider the universal boundary incidence with z_i=P. Its dimension is

D+(r−1)(n−1),

because z_i is fixed by P and all other z_j range on V(F). For general Z, the fiber of this boundary has dimension at most

D+(r−1)(n−1)−nr = D−r−(n−1),                                    (4.2)

or is empty. Because n≥2, this is strictly less than D−r. The finite union of these r boundary fibers cannot exhaust B_Z. Thus there is a center outside Z with a degree-d cone through Z.

For r≥N the generic kernel of (2.2) is zero, so the nonempty outside-Z locus just established is precisely the rank-at-most-N−1 locus. Its dimension is at least n−(r−N+1)=D−r by the rank-locus bound in Section 2. Its dimension is at most dim B_Z≤D−r, because it is the image of the outside-Z part of B_Z. Closure preserves its dimension. This proves Theorem A, including the endpoint r=D, where the locus is a nonempty finite set. No assertion about degree or scheme structure has been used.

## 5. Proof of Theorem B: do not discard common factors

Fix n≥3,d≥2, r=N−1. By (2.1), δ_Z(P_gen)=1. Thus a center P outside Z is exceptional exactly when there is a two-dimensional vector subspace (“pencil”) U of degree-d cone forms with vertex P, every form in U vanishing on Z.

We bound the dimension of the incidence of (Z,P,U). A two-dimensional subspace of a polynomial ring has a well-defined greatest common divisor up to scalar: the gcd of any basis of the subspace. Work in the n-variable polynomial ring of the quotient V/CP. There are two cases.

### 5.1 Pencils with no common factor

The parameter space of all (P,U) has dimension

n+dim Gr(2,N)=n+2N−4.

The no-common-factor condition is open. Two linearly independent degree-d forms in n≥3 variables with no common factor have a codimension-two common zero set in P^{n−1}, of dimension n−3. Its cone in P^n has dimension n−2. Each z_i in the incidence lies on this cone. Consequently the total incidence dimension is at most

n+2N−4+r(n−2).

After projecting to the nr-dimensional configuration space, its fiber for general Z has dimension at most

n+2N−4−2r=n−2.                                                  (5.1)

This bounds the image consisting of corresponding centers. It is valid even if the pencil has additional base components of smaller dimension or nonreduced base structure.

### 5.2 Pencils with a common factor

Let the gcd be G of degree e with 1≤e≤d−1. Write f=d−e and U=G U', where U' is a coprime pencil of degree f. For fixed P, the choice of [G] has dimension N_e−1, and the choice of U' has dimension 2(N_f−2). Thus the parameter space has dimension at most

n+N_e+2N_f−5.                                                   (5.2)

Every base point of U is either on the hypersurface cone G=0 or on the common zero cone of U'. For a particular configuration assign a subset S of s indices to the points on G=0, and assign the other r−s points to the residual common-zero cone. One may take S to consist of all indices on G; overlaps cause no difficulty. The first locus has dimension n−1; the second has dimension n−2. There are finitely many e and S. For each such stratum, generic fiber dimension bounds the (P,G,U') fiber by

n+N_e+2N_f−5+s(n−1)+(r−s)(n−2)−nr
  = n+N_e+2N_f−2N−3+s.                                         (5.3)

The apparently dangerous term is s. Lemma 3.1 rules out the stratum for general Z unless

s≤n+N_e−1.                                                      (5.4)

Combining (5.3) and (5.4) bounds its dimension by

2n−4−2[N−N_e−N_f].                                              (5.5)

This is an upper bound on the parameter fiber; the center image cannot have larger dimension. No subtraction of a guessed pencil-fiber dimension is performed.

### 5.3 The binomial inequality and the sole edge case

The sequence N_j=binomial(j+n−1,n−1) is discretely convex for n≥3: N_{j+1}−N_j=binomial(j+n−1,n−2) increases with j. Therefore for 1≤e≤d−1,

N_e+N_{d−e}≤N_1+N_{d−1},

and hence

N−N_e−N_{d−e} ≥ binomial(d+n−2,n−2)−n
                    ≥ n(n−3)/2.                               (5.6)

For n≥4, (5.5) and (5.6) yield a bound

2n−4−n(n−3)=−(n−1)(n−4)≤0≤n−2.

For n=3,d≥3, the exact formula N_j=(j+1)(j+2)/2 gives

N−N_e−N_f=ef−1,

so (5.5) equals 4−2ef≤0, because ef=e(d−e)≥d−1≥2.

Finally, n=3,d=2 has only e=f=1. The coarser cone bound (5.4) is insufficient here and MUST NOT be used to finish the proof. A degree-one cone is a plane. Four general points of P^3 lie on no plane, so s≤3. Directly substituting into (5.3), with N=6 and N_e=N_f=3, gives dimension at most s−3≤0. This closes the edge case.

Thus every common-factor stratum has generic fiber dimension at most zero (or is empty). In particular none has dimension exceeding n−2. Combined with (5.1), this proves

dim W_d(Z)≤n−2.                                                 (5.7)

All strata were considered before taking their center images and closures; finite unions and closure do not increase the maximum dimension. Centers equal to some z_i are omitted in this step, as required by the original definition.

### 5.4 Nonemptiness and the matching lower bound

By secant inclusion, W_d(Z) is nonempty. Map (2.2) has size (N−1)×N and generic rank N−1. Its maximal-minor locus on P^n\Z has codimension at most 2 by Section 2, so its dimension is at least n−2. Together with (5.7), this proves Theorem B.

An elementary local check of the same lower bound is available. At a general center on a fixed secant, exactly two of the N−1 points project together, and the remaining N−2 projected points impose independent degree-d conditions. Such projected tuples are general because, with the secant and its center fixed, all other original points can be chosen freely; the maximal-rank condition is open. Thus the matrix has rank N−2 there. An invertible (N−2)×(N−2) block reduces its rank-drop equations locally to a 1×2 Schur-complement block. Two equations in a smooth n-fold cannot have local codimension more than 2.

## 6. Monotonicity and the P^3 corollary

Let Z⊂Z' be general sets with sizes r≤r'≤N. Adding r'−r point conditions decreases the cone-space dimension by at most r'−r. If P is outside Z' and exceptional for Z, then

δ_{Z'}(P) ≥ δ_Z(P)−(r'−r)
           > (N−r)−(r'−r) = N−r'.

Hence P is exceptional for Z'. Taking closures yields

W_d(Z)⊂W_d(Z')∪Z'.                                              (6.1)

This formulation accounts for the finitely many centers removed from the domain when points are added. In particular, dim W_d(Z)≤max(dim W_d(Z'),0). General r points can be extended to a general r'-tuple: equivalently, projection of the relevant nonempty open subset of the larger configuration space contains a nonempty open subset of the smaller one.

Now n=3 and 2≤r<N. Extend to r'=N−1. Theorem B gives dim W_d(Z')=1, so (6.1) gives dim W_d(Z)≤1. Secant inclusion gives the reverse inequality. Theorem A gives the remaining r≥N cases, and r=1 is dealt with below. This proves Corollary C.

This monotonicity does not transfer the same exact dimension to all r<N in higher ambient dimension: it only gives the useful upper bound n−2. It is not a solution of the original all-n question.

## 7. Proofs of the elementary regimes

**P^1.** A degree-d form with multiplicity d at P is a scalar multiple of the d-th power of a linear form vanishing at P. It cannot also vanish at any other fixed point. Thus δ_Z(P)=0 outside Z for all r≥1.

**d=1.** Let L be the vector-space span of representatives of Z. A cone form is a linear form annihilating L and P. For general Z, dim L=min(r,n+1). When r≤n, its dimension drops by one for P outside the projective span, while P in the span imposes no new condition. For r≥2 the jumping locus is the whole projective span after closure. For r=1 that span is just the excluded point, so the jumping locus is empty. If r≥n+1 there are no nonzero linear forms through Z and no jumping.

**Small r.** Any m distinct points of P^{n−1} impose m independent degree-d conditions if m≤d+1. For each target point, take a hyperplane through each of the other points but not the target; multiply these m−1 linear forms, and, if necessary, multiply by further linear forms nonzero at the target to reach degree d. This gives separating forms. For r≤d+1 the projected degree-d kernel therefore depends only on the number m of distinct projected points. It jumps precisely when m<r, which is exactly when P is on a secant of Z. A single point imposes one condition from every outside center, proving the r=1 assertion for all n≥2,d≥1.

**P^2.** For a projected set of m points on P^1 the kernel dimension is max(d+1−m,0). General original plane points have no three collinear and no concurrency of three secants away from Z. To see that the latter is a valid general-position condition, any offending triple of secants away from Z has six distinct endpoints; concurrency is a proper algebraic condition, since the sixth endpoint can be chosen off the one line that would force it. There are finitely many choices. Thus outside Z, projection loses at most two distinct images; a loss of two occurs exactly at intersections of secants with four distinct endpoints. If r=d+2≥4, the jump condition is m≤d, so these double collisions are exactly the locus. Every choice of four endpoints has three pairings; genericity makes all resulting intersections distinct, giving 3*binomial(r,4) points. For r≥d+3 the required loss is at least three and cannot occur. The other cases follow from small r. This also independently checks Theorem A when n=2.

## 8. Dependencies and limits

The mathematical proofs above use the definition and projection interpretation in the original OWR report and [WS], but do not assume [WS] Theorem 5.1, Proposition 5.2, Proposition 5.3, Proposition 5.6, or Conjecture 5.4. In particular, the inductive deletion/generality assertion in the proof of its Theorem 5.1 is not used to justify any of our dimension claims. Standard projective, incidence, Grassmannian and determinantal dimension facts are explicitly stated in Section 2.

Theorem B establishes the expected dimension of the outside-Z jumping locus and is accepted at that scope by the accompanying mathematical audit. An upgrade to the entire determinantal scheme, including possible components supported at Z, ACM structure or degree, requires a separate argument and is not claimed here. Although boundary points cannot increase a positive locus dimension, scheme-theoretic conclusions do not follow from this observation alone.

The original problem is not marked solved: the conservative residual in Section 1 remains. Historical computational checks test finite identities, ranks and explicit low-dimensional examples only; they are supplementary and are not a proof of the generic theorems. The complete proofs above do not depend on omitted programs or finite certificates.

## References

[OWR] L. Chiantini, “Generalized Weddle loci,” in *Mini-Workshop: Subvarieties in Projective Spaces and Their Projections*, Oberwolfach Reports 54/2022, printed pp. 3102–3104, especially Question 1 on p. 3103. https://doi.org/10.4171/owr/2022/54 ; official PDF: https://ems.press/content/serial-article-files/46990

[WS] L. Chiantini, Ł. Farnik, G. Favacchio, B. Harbourne, J. Migliore, T. Szemberg, and J. Szpond, *Weddle schemes*, arXiv:2606.25060v1, submitted 23 June 2026. https://arxiv.org/abs/2606.25060v1 ; https://arxiv.org/html/2606.25060v1 . This is a preprint; no journal publication or independent acceptance of its formulas was established in the historical source review.
