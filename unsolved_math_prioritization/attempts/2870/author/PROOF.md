# KP-3.72 (2870): five routes to the smooth rational-filling kernel

Date: 2026-10-05 UTC. Status: **unresolved after five substantive approaches**.
This is a scoped research record, not a solution or a novelty claim. The elementary
arguments below are proved here; deep Floer-theoretic inputs are explicitly credited.

## 0. Exact target and category

Let A = Theta^3_Z be the abelian group of closed, connected, oriented smooth
integral-homology 3-spheres modulo oriented smooth integral-homology cobordism.
The operation is connected sum, the inverse reverses orientation, and the zero
class is S^3. A cobordism is a compact smooth oriented 4-manifold, with its two
boundary inclusions inducing homology isomorphisms. Define B = Theta^3_Q in the
same way using rational homology. Write q:A -> B and K = ker(q).

The modern K3 Problem 3.72 asks (a) whether K has a subgroup isomorphic to the
countable **direct sum** of copies of Z, and (b) whether such a subgroup can be a
direct summand of K. We retain both questions. Splitting inside A is a stronger
sufficient conclusion and is distinguished below. Infinite product Z^N is not the
target. There is no prescribed embedding, boundary parametrization, contact
structure, fundamental group, or spin structure on a rational filling. In
particular, a rational filling is not assumed spin. No topological or PL analogue
is substituted for this smooth question.

The governing source is Baykur--Kirby--Ruberman, *K3: A New Problem List in
Low-Dimensional Topology*, section 3.8, definition on printed p.181 and Problem
3.72 on p.183. The 1997 Kirby Problem 3.72 is an unrelated convergence-group
question answered by Bowditch. That numerical collision is not a resolution here.

Success would require actual smooth homology spheres in K, together with a proof
of independence of every finite integer linear combination; for (b) one also
needs a splitting on the full ambient kernel. No such family is established here.

## 1. Approach 1: construct more rational fillings, then test independence

### Proposition 1.1: kernel membership is rational ball bounding

An integral homology sphere Y represents an element of K exactly when Y is the
oriented boundary of a compact connected smooth rational homology 4-ball.

Proof. If q([Y])=0, a rational homology cobordism from S^3 to Y exists. Glue a
standard B^4 to its S^3 boundary. Mayer--Vietoris, and the isomorphisms induced by
the boundary inclusions, give H_0=Q and H_i=0 for i>0. Conversely, remove a small
smooth open 4-ball from the interior of a rational ball W. Excision and the long
exact sequence of the pair give a rational homology cobordism from S^3 to Y.
The oriented local fundamental class makes both H_3 boundary maps isomorphisms.
All gluings use boundary collars and are smooth. This proves the equivalence.

If W and W' rationally fill Y and Y', their boundary connected sum rationally
fills Y#Y': the joining 1-handle connects two components, so its relative degree-1
class maps isomorphically to the reduced H_0 of the disjoint union. There is no new
positive-degree rational homology. Reversing orientation fills -Y. Consequently
every finite integer combination of known rationally filled spheres lies in K.
This provides membership, not independence.

### Proposition 1.2: the rational-homology-circle construction

Let C be a compact connected oriented smooth 4-manifold with the rational
homology of S^1, and let J be an embedded circle in its boundary whose image in
H_1(C;Q) is nonzero. Attach a 2-handle along J with any integer framing, obtaining
W. Then W is a rational homology ball.

Proof. The only nonzero relative rational homology of (W,C) is H_2(W,C;Q)=Q.
The connecting map Q -> H_1(C;Q)=Q takes the relative handle core to [J], so is
an isomorphism. The long exact sequence now gives H_i(W;Q)=0 for i>0. The boundary
is connected and has the rational homology of S^3 by duality and the pair sequence.
If its integral homology is that of S^3, it therefore supplies an element of K.

For completeness, the usual boundary criterion is sufficient: if [J] is
nonzero in H_1(partial C;Q), it remains nonzero in C. Indeed,
H_2(C,partial C;Q)=H^2(C;Q)=0 and H_1(C,partial C;Q)=H^3(C;Q)=0, so the
boundary-to-interior map on H_1 is an isomorphism. This is the homological
mechanism of Akbulut--Larson Lemma 2 and Simone Lemma 1.1, not a new construction.

### Actual family tried and exact gap

The credited Akbulut--Larson families have exponent triples
(2,4n+1,12n+5) and (3,3n+1,12n+5), with odd positive n giving nonzero Rokhlin
invariant. The analogous credited Savk families use
(2,4n+3,12n+7) and (3,3n+2,12n+7), with even positive n in the nontrivial cases.
Each triple is pairwise coprime: subtracting three or four times the middle
entry from the last leaves respectively 2, 1, -2, -1, and the remaining parity
or residue modulo 3 is coprime. This verifies the elementary parameter condition,
not the Kirby diagrams. Their rational fillings are external cited results.

We attempted to turn this construction into infinite rank. The same filling
argument works for every connected sum and therefore cannot separate any relation.
Different triples or pairwise nondiffeomorphic boundaries need not determine
independent cobordism classes. In the abstract group Z, the infinitely many
nonzero odd multiples (2n+1)g all have the same nonzero mod-2 invariant and yet
span rank one. No relation-obstruction beyond that supplied by the credited
literature is produced for these families. This route stops at membership.

## 2. Approach 2: remove the rational homology defect by handles

This route tries to simplify rational fillings enough to control or distinguish
their integral cobordism classes. The following computation shows the necessary
obstruction and rejects a handle-cancellation shortcut.

### Proposition 2.1: paired finite homology of every rational filling

Suppose partial W=Y is an integral homology 3-sphere and W is a compact connected
oriented rational homology 4-ball. Put T=H_1(W;Z). Then T is finite,
H_3(W;Z)=H_4(W;Z)=0, and

H_2(W;Z) is isomorphic to Ext(T,Z), hence abstractly isomorphic to T.

Proof. Smooth compact manifolds have finitely generated homology, so H_1,H_2,H_3
are finite when rationally zero. H_4(W;Z)=0 because the boundary is nonempty.
The orientation map H_4(W,Y;Z)=Z -> H_3(Y;Z)=Z is an isomorphism. The next
part of the pair sequence injects H_3(W;Z) into H_3(W,Y;Z)=H^1(W;Z)=0.
Thus H_3(W;Z)=0. Since H_2(Y;Z)=H_1(Y;Z)=0, the same sequence identifies
H_2(W;Z) with H_2(W,Y;Z)=H^2(W;Z). Universal coefficients identify the latter
with Ext(H_1(W;Z),Z), as Hom(H_2(W;Z),Z)=0. For a finite abelian group T,
Ext(T,Z) is its Q/Z-dual and is noncanonically isomorphic to T. No canonical
identification between H_1 and H_2 is asserted.

### Corollary 2.2: 1- and 3-handles cannot both be bypassed

If W admits a finite handle decomposition with no 3-handles, then W is an
integral homology ball. Indeed, H_2 of the handle chain complex is a subgroup
of the free group C_2 because C_3=0. It is also finite by Proposition 2.1,
so it is zero, forcing T=0. Similarly, no 1-handles implies H_1=0, again
forcing H_2=0. Thus any rational ball bounding a **nonzero class in K** must
have at least one 1-handle and at least one 3-handle in every such decomposition.
A Stein rational ball cannot supply a nonzero class in K, using the standard
handle-index-at-most-two property of Stein surfaces. The latter application
also appears as Lemma 1.2 of Alfieri--Cavallo--Matkovic (May 2026).

The converse is false as a proposed inference: the mere presence of 1- and
3-handles does not prove that the boundary class is nonzero. Nor does this
argument assert that any smooth rational ball must be Stein or symplectic.

### Exact algebra control, not a manifold realization

For m>=2, consider the augmented chain complex with C_0=Z, C_1=Z,
C_2=Z^2, C_3=Z, d_1=0, d_2=(m,0), and d_3=(0,m)^t. Then d_2 d_3=0,
H_1=Z/m, H_2=Z/m, H_3=0, and its rational homology is that of a point.
This realizes the algebraic defect in Proposition 2.1. It does not construct
a smooth 4-manifold, specify a boundary, or prove a rank result in K.
The missing geometric step is an operation on actual fillings yielding
independently distinguishable boundary classes, rather than deleting handles
which the nontriviality itself forbids.

## 3. Approach 3: separate classes by homology and Floer invariants

### Proposition 3.1: prime-by-prime filling homology

For W and T as above and any prime p, let r_p=dim_Fp(T/pT).
Then the mod-p Betti numbers in degrees 0 through 4 are

(1, r_p, 2r_p, r_p, 0).

Proof. The universal coefficient short exact sequence for homology gives a
tensor contribution in degree i and a Tor contribution from H_{i-1}(W;Z).
A finite group and its dual have the same p-primary cyclic factor counts,
so both the tensor and Tor dimensions are r_p. Apply Proposition 2.1 in
degrees 1,2,3. The degree-4 groups vanish. Thus W is an F_p-homology ball
exactly when p does not divide |T|.

In particular, if the Rokhlin invariant mu(Y) is 1, every rational filling W
has nontrivial 2-primary T. Otherwise W is an F_2-homology ball, so
H^2(W;F_2)=0 and w_2(W)=0. Its spin structure restricts to the unique spin
structure on the integral homology sphere Y. Its signature is zero, so the
Rokhlin formula would give mu(Y)=0, a contradiction. This uses the standard
Rokhlin theorem, not a new proof of it. The homological mechanism overlaps the
previous investigation of the distinct mod-2 kernel problem, catalog 2869.

### Proposition 3.2: a rational-cobordism invariant is blind on K

If an invariant f on A factors as f=g o q for a function g on B, then f is
constant on K, with value g(0). This holds without additivity. If f is an
additive homomorphism with g(0)=0, its restriction to K is zero. Consequently
such an invariant cannot prove independence of nonzero elements of K.

For the ordinary Heegaard Floer correction term, the precise credited input is
Ozsvath--Szabo Proposition 9.9: the term vanishes for a boundary Spin^c
structure extending over a rational ball. A compact oriented smooth 4-manifold
admits a Spin^c structure (the standard dimension-four existence theorem),
and an integral homology sphere has a unique such structure. Hence d(Y)=0
for every [Y] in K. The Spin^c qualification is essential; this is not a claim
that a rational ball is spin. For the filtered instanton r_s-invariants,
Nozaki--Sato--Taniguchi Theorem 5.15 gives rational-cobordism invariance, and
r_s(S^3)=infinity. Therefore r_s(Y)=r_s(-Y)=infinity on K. Their usual distinct
finite r_0 independence criterion cannot apply to any nonzero class in K.

By contrast, Rokhlin is an integral-cobordism invariant which need not survive
rational cobordism. For a proposed relation sum a_i[Y_i]=0 with all mu(Y_i)=1,
it only imposes sum a_i=0 modulo 2. Infinitely many coefficient vectors survive.
Neumann--Siebenmann values on plumbed spheres must not be treated as a proved
Z-valued additive character on the entire group A. We do not do so.
The remaining gap is an integral-cobordism obstruction sensitive to these
rationally null classes, with a verified family-wide separation property.

## 4. Approach 4: move an ambient infinite-rank subgroup into K

### Proposition 4.1: a rank-transfer sufficient condition

Let F<=A be free abelian of countably infinite rank. If q(F) has finite rank
r (rank means dimension after tensoring with Q), then K contains Z^(N).

Proof. For any N basis elements of F, let F_N be their Z-span. Exactness of
localization at the nonzero integers gives
rank(ker(q|F_N)) = N - rank(q(F_N)) >= N-r.
Thus K intersect F has unbounded finite rank. Inductively choose elements
whose images in (K intersect F) tensor Q are Q-linearly independent. Any
finite integer relation would give a rational relation, so these elements
generate the required countable free subgroup. No splitting follows.

A concrete sufficient variant is useful: suppose x_0,x_1,... are independent
in A and q(x_i)=m_i q(x_0) with integers m_i. Then y_i=x_i-m_i x_0 belongs
to K, and comparing the x_i coordinates proves that the y_i are independent.
If equality holds only after tensoring with Q, clear denominators and kill
the resulting torsion individually; nonzero integer multiples of the corrected
x_i still remain independent. No such rational-image relation is established
for an actual family here.

### Proposition 4.2: the standard DHST family gives no kernel elements at all

For n>=1 let B_n=Sigma(2n+1,4n+1,4n+3), with the canonical Seifert orientation,
and F=<[B_n]> inside A. Credited input from Dai--Hom--Stoffregen--Truong:
F is an infinite-rank free direct summand of A. Nevertheless,

F intersect K = 0.

Proof, with all deep inputs exposed. Lee--Savk's proof of Theorem 3.3 explicitly
records R(B_n)=1; the same paper uses the canonical negative-definite orientation.
Nozaki--Sato--Taniguchi Corollary 1.4 therefore gives

r_0(-B_n)=1/(4 E_n), r_0(B_n)=infinity,
E_n=(2n+1)(4n+1)(4n+3)=32n^3+48n^2+22n+3.

Since E_(n+1)-E_n=96n^2+192n+102>0, the values r_0(-B_n) strictly decrease.
Corollary 5.6 and Theorem 5.15 of that paper show that the classes q(-B_n)
are Z-linearly independent in B. Reversing all signs preserves independence.
A finite sum of [B_n] belonging to K must consequently have all coefficients
zero, proving the assertion. This is a deduction from existing results,
not a new independence theorem or a reproof of instanton theory.

There is also a weaker immediate check: Lee--Savk Theorems 2.5 and 3.1 give
d(B_n)=2n, excluding each individual B_n from K. Vanishing of a linear
combination of these d-values alone would not exclude a relation; the r_0
argument is what excludes every nonzero combination.

Lee--Savk's 2026 infinite-rank examples in the kernel of the involutive local
class map h:A->I are likewise not substitutes: their stated conclusion is
independence **in B**, so their span intersects K trivially. Equality of local
classes is not equality of rational-cobordism classes. The abstract implication
ker(h) subset K has not been assumed. Thus the two promising published
infinite-rank mechanisms considered here run in the wrong direction for K.

## 5. Approach 5: upgrade independence to a split subgroup

### Proposition 5.1: exact character criterion for splitting in K

Suppose x_1,x_2,... in K generate H isomorphic to the countable direct sum of Z.
Then H is a direct summand of K if and only if there are homomorphisms
lambda_i:K->Z satisfying
(i) lambda_i(x_j)=delta_ij and
(ii) for each k in K, lambda_i(k) is nonzero for only finitely many i.

Proof. If K=H direct-sum C, compose the projection onto H with its coordinate
maps; their values have finite support by definition of H. Conversely let
r(k)=sum_i lambda_i(k)x_i. Condition (ii) makes the sum defined, and the union
of two finite supports verifies additivity. Condition (i) gives r|H=id.
Every k equals r(k)+(k-r(k)), where the second term lies in ker(r), and
H intersect ker(r)=0. Hence K=H direct-sum ker(r).

If these lambda_i are defined on all A, this proves the stronger ambient
splitting. A splitting in K alone does not imply one in A: Z is its own direct
summand inside K=Z subset A=Q, but Q has no nonzero homomorphism to Z.

### Two exact negative controls

1. In K_0=direct-sum_i Z e_i, the independent elements x_i=2e_i do not generate
a direct summand: a retraction would force 1=lambda_i(2e_i)=2lambda_i(e_i).
2. K_1=direct-sum_i Q contains an independent Z^(N), but it has no nonzero
free-abelian direct summand at all. A homomorphism Q->Z sends 1 to an integer
which is divisible by every positive integer, hence to 0. The same argument
on each coordinate shows every homomorphism K_1->Z vanishes. A nonzero free
summand would give a nonzero coordinate homomorphism, a contradiction.

These are algebraic controls, not assertions that the actual K is divisible.
They prove that independence alone cannot answer (b). Nor is an arbitrary
family of coordinate homomorphisms enough: without finite support, the map
lands in a product, and the proposed sum defining r may be undefined.
The remaining task is to construct a locally finite family of integral
characters on the actual K, or another retraction, and compatible geometric
classes in K. No such construction is supplied by this approach.

## 6. Disposition and limits

All five mechanisms stop at explicit gaps. Neither part (a) nor part (b) is
resolved, and no rank-two subgroup of K has been proved here. The principal
scope-checked conclusions are the rational-filling and handle reductions,
prime-by-prime homology obstruction, invariant blindness, exclusion of the
standard DHST span from K, and the exact rank-transfer/splitting criteria.

The proof checker exercises finite chain complexes, exact integer/rational
identities and abstract group countermodels. It does not construct rational
balls, perform Kirby calculus, compute Floer theories, certify every infinite
family member, or establish worldwide current openness. The mathematical
arguments above, and the explicitly credited external theorems, carry the
infinite statements. This package awaits a fresh independent mathematical audit.

## References

- Baykur, Kirby, Ruberman, *K3: A New Problem List in Low-Dimensional Topology* (2026), pp.181,183: https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- Akbulut and Larson, *Brieskorn spheres bounding rational balls* (2018), Theorem 1 and Lemma 2: https://arxiv.org/abs/1704.07739
- Savk, *More Brieskorn spheres bounding rational balls* (2020), Theorem 1.1 and Lemma 2.1: https://arxiv.org/abs/1912.04654
- Simone, *Using rational homology circles to construct rational homology balls* (2021), Lemma 1.1 and Remark 1.4: https://arxiv.org/abs/2006.14509
- Ozsvath and Szabo, *Absolutely graded Floer homologies and intersection forms for four-manifolds with boundary* (2003), Proposition 9.9: https://arxiv.org/abs/math/0110170
- Dai, Hom, Stoffregen, Truong, *An infinite-rank summand of the homology cobordism group* (2023), Theorem 1.1, proof, Remark 1.3: https://arxiv.org/abs/1810.06145
- Nozaki, Sato, Taniguchi, *Filtered instanton Floer homology and the homology cobordism group*, JEMS 26 (2024), Corollaries 1.4,5.6 and Theorem 5.15: https://ems.press/content/serial-article-files/48226
- Lee and Savk, *On homology spheres of the trivial local equivalence class*, version 2 (26 February 2026), Theorems 2.5,3.1 and proof of 3.3: https://arxiv.org/abs/2508.15384
- Alfieri, Cavallo, Matkovic, *Brieskorn spheres and rational homology ball symplectic fillings*, preprint (May 2026), Lemma 1.2: https://arxiv.org/abs/2605.13812
