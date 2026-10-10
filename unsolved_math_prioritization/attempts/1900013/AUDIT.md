# Independent mathematical audit: cubic Klein continued fractions

This is an independent internal AI review of an unrefereed AI-assisted mathematical manuscript. “Accepted” denotes the stated internal review disposition, not external human peer review or journal acceptance.

## Verdict and scope

**ACCEPT AS A RIGOROUS PARTIAL RESULT.** No mathematical correction is required for the claims in the sealed candidate. The result is accepted only for the historical union of all eight Klein sails, for a fixed totally real cubic number field, with integer-linear equivalence. A complete description of possible face data or decorated torus decompositions is not established. No novelty, priority, or exhaustive present-day literature-status claim is accepted.

The audited proof establishes all of the following:

1. Recovery of the defining hyperplane arrangement from the actual eight-sail union and the origin, without treating an operator as extra geometric input.
2. Recovery of the rational multiplication algebra and the integral multiplier order, up to the isomorphisms naturally induced by lattice equivalence.
3. Exact lattice equivalence modulo a nonzero field scalar and a genuine field automorphism.
4. Realization of every full lattice by a positive, irreducible operator in SL(3,Z).
5. Countably infinitely many inequivalent objects in every fixed totally real cubic field, separated by multiplier-order discriminants.
6. Finite fixed-order strata and finite bounded-order-discriminant strata.
7. The explicit same-characteristic-polynomial pair and every displayed algebraic identity checked below.

This audit reviewed the proofs independently and rebuilt exact calculations without importing the candidate's implementation. It is a mathematical review supported by exact computations, not a formal proof-assistant certificate.

## 1. Source interface and model

Karpenkov's 2004 Definition 1.1 uses the boundaries of convex hulls of nonzero lattice points in closed orthants and takes the union of all sails. Its equivalence relation is lattice-preserving linear equivalence. Definition 1.2 specializes to real irreducible unimodular operators. Problem 3 concerns the common cubic field, rather than one polynomial or order. The source's separate determinant-one commuting criterion is not needed by this candidate. See [K04, pp.3-4,15-16](https://arxiv.org/pdf/math/0411054).

The 2017 Problem 13 occurs in a broader collection of geometric models and classification problems. The candidate explicitly confines its theorem to the predecessor's Klein model; that qualification is necessary and present. See [K17, pp.4-9](https://arxiv.org/pdf/1712.01450).

The proof sometimes starts with any irreducible integral or rational cubic operator. This does not enlarge its eventual collection of geometric objects: every resulting full lattice has a positive SL(3,Z) realization by Proposition 5. Thus the original unimodular source convention is satisfied, rather than merely approximated.

The geometry remains the lattice-embedded sail union. An abstract face poset, an unlabeled torus, a single chosen sail, a projective equivalence, or an affine equivalence with an arbitrary translation is not the input to the recovered invariant. The origin and integer lattice are part of the historical ambient setting.

## 2. Missing-ray recovery

The potentially most consequential step is Lemma 1. It is valid.

For a full lattice I in K, choosing a common denominator d puts dI inside the maximal order. Each nonzero element of dI has nonzero integral field norm. In embedding coordinates this gives a uniform bound on the absolute coordinate product, at least d^-3, at every nonzero lattice point.

Inside a fixed open orthant, make the coordinate signs positive. The set of positive triples whose product is at least d^-3 is convex: the logarithm of the product is concave, so this is one of its convex superlevel sets. Equivalently one can use concavity of the geometric mean. A convex combination of the relevant lattice points therefore stays in this set. Passing to the closure does not introduce a coordinate-zero point: the coordinate product is continuous, and the closed hull remains in the closed orthant. A finite point on a defining hyperplane has zero product and cannot belong to that hull. Escaping sequences at infinity cause no exception to this argument about finite points.

For an interior ray, a lattice parallelepiped enclosing tv has vertices whose displacements from tv are uniformly bounded independently of t. As t grows, the distance from tv to every bounding coordinate plane grows linearly, so all eight vertices eventually lie in the chosen open cone. They are nonzero and belong to the generating set. Thus tv belongs to the hull for all sufficiently large t. These eight vertices also give a full-dimensional parallelepiped, establishing nonempty interior of the convex hull itself.

The set of ray parameters meeting the closed hull is closed, nonempty, and bounded away from zero by the product bound. Its positive minimum is attained. That point is on the boundary because smaller ray parameters approach it from outside the hull. This proves the required ray intersection, without assuming a polyhedral asymptotic description or uniqueness of intersection.

Consequently the rays missing the entire sail union are exactly those lying in the union of the three hyperplanes. A real plane contained in a finite union of three real planes must equal one of them: otherwise it would be a union of finitely many proper linear subspaces. Hence the unordered arrangement is recovered, not merely its union as an unstructured set.

The insertion of closure into the hull definition is harmless. A convex set with nonempty interior and its closure have identical interiors after closure and identical topological boundaries. The full-dimensionality argument supplies the needed hypothesis; the corresponding assertion would not be automatic for an arbitrary nonconvex set.

No algebraic sail face theorem, periodicity theorem, or combinatorial rigidity theorem is being imported into this proof.

## 3. Rational algebra and multiplier order

In embedding coordinates, preserving each coordinate hyperplane individually forces every off-diagonal matrix entry to vanish. The condition is individual preservation, not arbitrary permutation of the arrangement. Zero and other noninvertible endomorphisms are correctly allowed.

For a rational linear map T with this diagonal form, a=T(1) belongs to K. Its three embeddings are precisely the diagonal entries of T. For every x in K, the embeddings of T(x) therefore agree with those of ax. This proves T=m_a. Conversely all multiplication maps preserve the planes. The rational algebra is exactly the field representation of K.

Intersecting with the integral endomorphisms of I yields (I:I). It is a unital ring. Clearing finitely many denominators in the multiplication matrices of an integral basis gives a full-rank suborder contained in it. Conversely Cayley-Hamilton applied to an integral multiplication matrix makes each multiplier an algebraic integer: evaluating the polynomial identity at 1 shows that the same monic polynomial annihilates the multiplier itself. Thus the ring lies in the maximal order and is an order.

These facts do not assume that I is an invertible ideal of its multiplier order. Indeed that assumption would exclude some legitimate lattices and invalidate a field-wide classification.

The trace of multiplication by ab is the field trace. A change of integral ring basis changes the Gram matrix by unimodular congruence. A lattice equivalence conjugates the recovered rational algebra and integral ring, preserving matrix traces. The determinant is a positive integer because the embedding trace pairing is positive definite in a totally real field. It is exactly the recovered-order discriminant.

This discriminant is not the characteristic-polynomial discriminant of a chosen realizing unit, and it is not an invariant obtained by treating a split ternary norm form as a nonsingular plane cubic. The proof makes both distinctions correctly.

## 4. Equivalence and realization

An integer-linear equivalence between two chosen lattice presentations restricts to a Q-linear isomorphism of K, because both lattices span K. Missing-ray recovery implies that it permutes the defining planes. Conjugation then normalizes the multiplication algebra and induces a Q-algebra automorphism tau of K. Setting a=T(1) gives T(x)=a*tau(x), with a nonzero. Conversely such a map permutes embedding hyperplanes and cones; if it carries I to J, it carries every defining lattice-point set, hull, and boundary to its counterpart. Hence

    S(I) is equivalent to S(J)  if and only if  J = a*tau(I).

Only actual field automorphisms are allowed. A permutation of three real embeddings need not descend to a rational linear normalizer. The candidate does not substitute the full symmetric group for the field automorphism group. This remains correct both in cyclic cubic fields and in non-Galois cubic fields.

The union of eight sails is centrally symmetric. In dimension three, -Id has determinant -1. Composing a determinant-minus-one equivalence with this symmetry produces a determinant-plus-one equivalence. Thus GL(3,Z) and SL(3,Z) have the same orbits for these complete unions. This observation does not assert that they have the same orbits for a selected single sail or in even dimension. Likewise, a narrow-ideal restriction would not match the complete union.

Dirichlet's theorem for an arbitrary order gives two independent infinite-order units in the totally real cubic case, so in particular one such unit exists. This exact order-level statement is in [Conrad, Theorem 1.1](https://kconrad.math.uconn.edu/blurbs/gradnumthy/unittheorem.pdf). Squaring it gives positive real embeddings and norm one. The multiplication matrix on I is integral and invertible over Z, because the unit and its inverse preserve I.

The square still has infinite order. A rational algebraic-integer unit is only 1 or -1, so the square is nonrational. Prime field degree then makes it primitive in K; separability makes its conjugates distinct. Its cubic characteristic polynomial is consequently irreducible. This proves the full SL(3,Z), positive-eigenvalue realization claimed.

Conversely Q^3 under an irreducible cubic operator is one-dimensional over its generated cubic field: any nonzero rational vector gives an injective field-module map, hence an isomorphism by dimension. Pulling back Z^3 gives the needed full lattice. No restriction to one ideal class, one polynomial, or a monogenic order has entered the argument.

## 5. Infinitude and the discriminant bound

For R_f=Z+f*O_K, ring closure follows by multiplication. Since 1 belongs to R_f, any multiplier of R_f belongs to R_f, and conversely its ring elements are multipliers. Thus this family's recovered order is exactly R_f.

The element 1 is primitive in the free abelian group O_K. Otherwise a nonintegral rational number 1/n would be an algebraic integer. It therefore extends to an integral basis. Relative to that basis, R_f has basis 1,f*omega_2,f*omega_3 and index f^2. The discriminant scales by the square of this index, giving f^4*disc(K). The exponent four is essential and correct.

Distinct positive f yield distinct invariant discriminants, hence distinct sail-union equivalence classes. Proposition 5 realizes all of them inside the source's operator class. Since K is countable, its finitely generated full lattices form a countable set. The result is exact countable infinitude, not merely infinitely many matrices defining possibly identical sails.

For each f with f^4*disc(K) at most X the family contributes a distinct class. The lower bound floor((X/disc(K))^(1/4)) follows. No unsupported asymptotic estimate for N_K(X), and no claim that all discriminants have this special fourth-power form, is made.

## 6. Finite order strata and what is algorithmic

The finite-stratum argument is valid and avoids assuming ideal invertibility at a nonmaximal order.

Let R be an order, O the maximal order, and c its conductor in O. Choose finitely many representatives J_i for the fractional ideal classes of O. The required inputs are available at the level of mathematical existence: O has a finite integral basis, is Dedekind, its nonzero fractional ideals are invertible, and its ideal class group is finite. These are respectively [Weston II.2.22, II.3.3, II.3.6, and IV.2.3](https://kconrad.math.uconn.edu/math5230f08/weston.pdf). The statement for fractional ideals follows from the integral-ideal statement by clearing a scalar denominator.

For an R-stable I, its saturation OI is a nonzero fractional O-ideal. Rescale so that OI=J_i. Then c*J_i=c*OI lies in RI, hence in I, while I lies in J_i. The conductor contains mO for some nonzero integer m: take mO inside R, which is possible because R has finite index. Therefore J_i/cJ_i is finite. This proves finiteness before performing any quotient identifications.

The proposed selection conditions are necessary and sufficient: select the subgroups whose inverse-image lattices are R-stable, have O-span J_i, and have exact multiplier ring R. Omitting the exact-multiplier condition would retain larger-order strata. Omitting saturation would make the normalization and unit quotient incorrect.

For two normalized lattices in the same J_i interval, a homothety between them must stabilize J_i. Multiplying by the inverse fractional ideal forces aO=O, so a is an O-unit. Conversely such a unit induces a permutation of the finite quotient and acts on the eligible subgroup set. Lattices normalized into different ideal-class representatives cannot be homothetic. Genuine field automorphisms may move both the order and its ideal class; to identify those objects, transport to the chosen representative by a compensating scalar. The candidate's order-orbit language is appropriate.

There is also a direct finite way to check exact multipliers after normalization. If aI is contained in I and OI=J_i, then aJ_i is contained in J_i, so a belongs to O by invertibility of J_i. Every element of c sends J_i into cJ_i, which is contained in I. Thus the multiplier condition is determined by the finite action of O/c on I/cJ_i. Ring stability and saturation can likewise be tested by a finite integral basis and finite subgroup arithmetic. Given generators of O-units, their images generate a finite permutation group, so the orbit computation terminates.

This is a finite arithmetic reduction once the maximal-order basis, class representatives, conductor, relevant unit action, and field automorphisms are provided. The candidate does not supply a certified implementation of general number-field class-group and fundamental-unit computation, a complexity bound, or an algorithm recovering all sail faces. Finite class number alone is not a certificate that an arbitrary search for class representatives has finished; stabilization of observed unit residues is not by itself a certificate that all unit images have been found. None of the accepted finiteness proofs needs those stronger algorithmic assertions. The candidate's actual wording is a construction and structural reduction, so this distinction is a clarification, not a blocking omission.

Finally every order of index m contains mO. There are finitely many such subgroups for each bounded m. Since disc(R)=m^2*disc(K), a discriminant bound gives finitely many orders and the preceding argument gives finitely many classes over them. No finiteness of the infinite union over all orders is inferred.

## 7. Independent exact tests

The rebuild uses polynomial remainders and resultants as well as exhaustive finite vector-space enumeration. It does not import the candidate's modules.

- Reconstructed multiplication in Q[t]/(t^3-3t+1), both displayed matrices, and determinant characteristic polynomials.
- Independently counted three positive roots of t^3-57t^2+570t-1 using exact Sturm-based root counting and checked irreducibility.
- Reconstructed the trace Gram matrix and discriminants 81 and 6561. The shared characteristic polynomial instead has discriminant 314672121.
- Verified the entire symbolic multiplier-matrix formula and norm identity; the norm was also computed as a resultant.
- Verified 32 conductor realizations using finite residue powers of theta squared and exact rational basis changes.
- Verified 90 unimodular basis and conjugation cases, with both determinant signs.
- Checked a genuine order-three field automorphism theta -> theta^2-2 and its normalizer identity.
- Rejected six deliberately false arithmetic claims using explicit exceptions, which remain active under optimized Python.

The finite-module test independently exercises the selection and orbit steps in intervals p*Z[theta] <= I <= Z[theta]. It does not assume that Z[theta] is maximal or that its ideal class group is trivial. With O0=Z[theta] and O0I=O0, any multiplier belongs to O0, so the finite stabilizer test is exact for these normalized intervals.

Modulo 2, all 16 subspaces were enumerated; 14 have full O0-span and exact multiplier Z+2O0. Their unit action has two orbits, each of size 7, distinguished by quotient dimensions one and two. Modulo 3, all 28 subspaces were enumerated; 18 have full O0-span and exact multiplier Z+3O0, forming two unit orbits of size 9. Three other full-span subspaces have strictly larger multipliers and were correctly rejected. The reductions of the actual units theta and 1-theta generate the whole finite unit group in both tests, so these finite unit orbit calculations do not assume an unproved global fundamental-unit list.

The independent normal, -O, and -OO results agree byte-for-byte. The candidate's original exact checks were also replayed in all three modes, with matching outputs; its symbolic check passed separately. Finite arithmetic checks support the displayed identities and finite examples. They do not prove the arbitrary-field geometric statements, which were reviewed above.

## 8. Acceptance boundaries

The accepted status remains PARTIAL. In particular, this audit does not approve any statement that the work classifies all geometric face arrangements, proves a complete combinatorial realizability criterion, identifies every decorated torus decomposition, resolves other sail models, or establishes that the theorem is new.

Source bodies are not reproduced in these authored audit reports or public verification metadata.
