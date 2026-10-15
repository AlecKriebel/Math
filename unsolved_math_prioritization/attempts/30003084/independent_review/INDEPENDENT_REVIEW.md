# Independent full partial-result review: 30003084

**Verdict: PASS_SCOPED_PARTIALS. No mandatory mathematical correction found. The original arbitrary-cardinality complex ordinary-conic problem remains unsolved, 5/5 author turns.**

The verdict binds FROZEN_MANIFEST.json SHA-256 `9e118c02af3ffd7938588f7064f76873b52a827390e2c89cf40a9b7ff581cbce` and all its23 author files, including RESULT.md `0b9f0e7bc2f57ee3cd63474b24138d71bdd260a45d5d4f8681de4f2e22ad08f6`. The reviewed claims are the at-most-ten-point theorem, the theorem for all cubic-supported nonconic sets, the large-line criterion and the stated fixed-configuration/Fermat results. No full general theorem or novelty claim is accepted or asserted.

The reviewer did not contribute to the author's five proof-search turns. The frozen files were left unchanged. I independently checked the algebraic and geometric arguments, reconstructed decisive symbolic identities, verified actual conic witnesses in a different quadratic-field representation, and replayed every author receipt separately. The all-configuration proofs below are not inferences from finite controls.

## 1. Source target and uniqueness

The official OWR p694 question and its preceding definition were visually inspected. The published conics paper explicitly permits singular/reducible conics and requires the five points to determine a unique quadratic. Thus a conic merely passing through five points is insufficient. All retained arguments use rank5 of the quadratic evaluation matrix, and every ordinaryness argument also excludes all additional points of the full set. The source distinction from the real theorem and the finite-field example is correct. Details and classical-source locators are in SOURCE_REVIEW.md.

For distinct projective points, any set of at most three quadratic evaluation columns is independent: a product of two lines can separate any one from the others. Four such columns are dependent precisely for four collinear points. The converse construction in Turn2 works even when three of the four are collinear. More generally, for five points with no four collinear, partition the other four points into two pairs on lines avoiding a selected point. The groups lying on a line through that selected point have size at most two, so such a pairing always exists. Its product separates that point. This proves rank5 and uniqueness in all later selections, without a generic-position hypothesis.

## 2. Gale duality and small cardinalities

I checked the complement identity by dimensions of relation spaces:

    rank(G_C)=|C|-6+rank(V_complement(C)).

A circuit C of size n-5 gives a rank5 complement of size5; deleting any one member of C shows that adding the corresponding original point raises its rank to6. Hence the conic's support is exactly that complement. Loops and proportional Gale columns retain their usual one- and two-element circuits; none are silently discarded from the original configuration.

For n8 the absence of a three-circuit forces precisely two nonzero Gale directions. Their independent supported relations each require at least four original points, leaving exactly two four-point lines and no zero Gale columns. For n9, the no-quadrangle lemma is valid: an extra point on one side of a basis triangle excludes extra points on either other side by a four-point quadrangle. Restoring multiplicities gives rank2 and rank1 blocks. They need at least five and four original points, respectively, so the original evaluations have two rank3 blocks and lie on two lines. These conclusions contradict the full rank6 hypothesis. The n6 and n7 cases, and the vacuity below six points, are correct.

## 3. Full rank-four classification

The rank4 lemma was audited as a universal complex-linear argument. A full four-support column with the chosen basis gives a five-circuit, so all outside supports have size at most three. If a three-support column is normalized to a=e1+e2+e3, its three alternative bases give outside coordinates

    q_i, q_j-q_i, q_k-q_i, q_4.

For q_4 nonzero, absence of a five-circuit forces each nonzero q_i to equal another one of q_1,q_2,q_3. Combined with the forbidden full support, this gives either e4 alone or exactly two equal nonzero first-three coordinates. This justifies the first support reduction, not merely a necessary generic constraint.

Two different outside support pairs are impossible. The unequal-parameter five-column matrix has four-minors proportional to t, u and u-t, so all are nonzero under its stated hypotheses. The equal-parameter matrix has four-minors ±1 and2t. Thus the characteristic-zero second case really closes the equality exception. Applying the same support argument with the new three-support vector forces the remaining inside columns onto the three concurrent lines claimed in the packet.

If no three-support column exists, the support graph on four basis vertices either disconnects or contains a three-edge path unless it is a star. I independently checked all64 graphs: of38 connected ones, exactly the four labeled stars have no such path. For arbitrary nonzero edge coefficients, the weighted path's relevant minors are1, a, ab and -abc, all nonzero. Thus the graph argument is valid for every nonzero complex weighting, not just the test weights. A star gives the same concurrent-line geometry.

The Veronese-origin exclusions also pass. In the concurrent-line case an annihilating row functional has support exactly on each private branch, regardless of whether the actual other columns span the entire geometric hyperplane. Each branch is nonempty by rank4 and supplies an original dependency on at least four points; three disjoint branches would require at least twelve points. In the decomposable case, relation spaces split by blocks, so the original column spans split as well. Every dependent block has rank at least3, and zero Gale columns are free original columns. Total rank6 therefore permits exactly two rank3 dependent blocks and no free columns. Each block is collinear by the four-point criterion. This is the required contradiction. Nothing in this proof classifies higher Gale rank.

## 4. Smooth cubics and the abstract-character argument

On an irreducible cubic no four distinct points are collinear. The unique conic through five points has intersection degree6 with the cubic. On a smooth cubic with a flex as origin, its intersection divisor is linearly equivalent to6O. Picard theory therefore gives the residual point as minus the sum of the five selected points, with multiplicities included. If the residual is one of those five, there are exactly five distinct cubic points on the conic and it is already ordinary. This handles tangencies and reducible conics without a continuity argument.

Assuming no ordinary conic consequently forces each four-point-deletion reflection to map the complement bijectively to itself and avoid fixed points. The character lemma only uses the bijection. I independently derived the subtraction identity with an arbitrary nonzero constant K, covering both versions in Turns4 and5. Comparing two pairs with a common first value forces Q*z_d*z_e*z_f=K; a fourth distinct value is then impossible. Protecting four values while deleting three other points requires exactly the stated threshold n>=7. Repeated character values and torsion cause no division by zero because the subtraction is used only for distinct values.

The subgroup generated by the finite point set on E(C) is finitely generated. Its torsion part has at most two cyclic factors because it embeds in E[m], isomorphic to (Z/m)^2 for its exponent m. Two abstract characters give an injection: one records all free coordinates by positive prime powers and one torsion factor, and the other records the remaining torsion factor. Absolute values followed by unique prime factorization verify injectivity. No continuity on the elliptic curve is required. Each image has at most three values, yielding at most nine points; the already established small-cardinality theorem finishes the contradiction. The proof is not restricted to finite subgroups or torsion configurations.

## 5. Singular irreducible cubics

If the singular point is selected, its local intersection multiplicity with a conic through it is at least2. Four additional selected smooth points use the remaining four degrees of the Bezout count. Uniqueness holds by the no-four-collinear criterion, and a degree2 curve cannot contain the irreducible cubic. Therefore no unselected point can lie on that conic.

When the singular point is absent, the nodal and cuspidal normalizations cover all smooth points with the stated parameter exclusions. I checked their curve incidence directly. A conic through five smooth points cannot also pass through the singularity, since that would require intersection degree at least7. Consequently its z² coefficient is nonzero. In the nodal pullback, this is both the constant and degree6 coefficient; all six parameters are finite and nonzero and their product is1. In the cuspidal pullback the degree5 coefficient vanishes and the degree6 coefficient is nonzero, giving the sum-zero law with no missing infinity root.

The normal-form classification is complete in characteristic zero. At a singular point the cubic is z*q2+q3. Distinct tangent factors reduce to xy and nonzero pure-cubic coefficients; repeated tangent factor reduces to a cusp after a shear and absorption of x²-divisible terms. If the quadratic tangent cone vanished, the cubic would factor into lines over C. The multiplicative or additive reflection arguments then apply to the smooth parameter set. The additive finitely generated subgroup is torsion-free and has the stated prime-power injective character. All low-cardinality exceptions are already covered.

## 6. Conic plus line, including their intersections

For an irreducible conic C plus a line L, nonconicity forces at least three points off L and at least one point of L off C. If at most four points are off L and the total exceeds ten, the large-line criterion applies with room to spare. If there is exactly one point of L off C, four points on C together with it determine a conic exhausting all four intersections with C, so all component-intersection points and all other C points are excluded.

In the remaining case, selecting three C points and two L points excludes either carrier as a component. The two L intersections are exhausted, so the resulting conic avoids C intersect L even when those points belong to the original set. In the secant normalization, the quartic product of C parameters equals the product of the two L parameters. In the tangent normalization, their sums agree. I reconstructed both identities from a general homogeneous quadratic. The leading/constant coefficients used as denominators are nonzero because the two distinct finite L parameters exhaust its intersection and L is not a component. The two-deletion character lemma therefore applies to every required residual reflection. Its n>=5 threshold is exactly the branch treated; no small or intersection-point case is omitted.

## 7. Three-line supports

For a triangle of carrier lines, a two-two-one selection is unique and has no carrier component. The two fully occupied carriers force avoidance of all three vertices. The three quadratic restrictions give the exact product relation (aa')(bb')(cc')=1, with nonzero denominators. Thus ordinaryness is checked against vertices as well as smooth carrier points.

When all three parameter sets have at least three elements, comparing reflections with a shared pair member generates all ratios. Each ratio subgroup stabilizes the other finite sets. Multiplicative stabilizers act faithfully and are finite, and each stabilizer element is itself a ratio of two points. Cycling these inclusions makes the three ratio groups equal and shows that each set is a single coset of their common finite cyclic group. Every group element is a product of two distinct elements when the order is at least3, since a square equation has at most two roots. The coset relation then allows pairs forcing the residual intersection to repeat the chosen fifth point. This proves an ordinary conic rather than assuming a tangent construction exists in advance.

The smaller-set cases are exhaustive. A singleton gives an immediate ordinary conic from two points on each other carrier. A two-element smallest set forces every residual involution to swap the same two points; varying a pair on a carrier of size at least3 contradicts the resulting constant pair product. All-three-small cases have at most nine points including vertices. In the remaining (a,1,1) pattern, absence of the opposite vertex makes the set conic; if that vertex is present, select it, the two singleton points and two points on the large carrier. They have no four collinear and the conic has no carrier component. The vertex contributes multiplicity2, exhausting the total6 with the other four points and excluding every other vertex or smooth point.

For three concurrent lines, the parameter restrictions give the stated additive sum law. Comparing pair reflections produces a nonzero translation stabilizing a nonempty finite subset of C, impossible in characteristic zero. The only large-cardinality alternatives are covered or lie on two lines. The common vertex is excluded by the two fully occupied carriers, or is already on the large carrier in the conic alternative. Repeated cubic components have support of degree at most2, so they cannot carry a nonconic set. This completes the entire cubic classification.

## 8. Large lines and Fermat configurations

The large-line proof chooses a first point away from at most three pair-line intersections. For every additional outside point, the five-point conic is unique and cannot contain the large line because the original outside triple is noncollinear. There is at most one further forbidden point on that line. The count l-1>r-3 under l>=r-1 leaves a second point, and uniqueness excludes every extra outside point. The resulting conic contains exactly two large-line points and the chosen three outside points. This works projectively, including intersections at infinity.

The Fermat construction has the stated incidences and exactly three configuration points on each noncarrier line. Two such lines meeting at a selected point give exactly five distinct points. Three points on each component force any quadratic through the five to contain both lines, proving uniqueness. Distinct unions cannot be counted at different selected intersection points. The lower bound is therefore valid and does not claim to be sharp.

The fixed Hesse/Fermat counts were reproduced byte-for-byte over exact Q(omega). Separately, I verified the four recorded ordinary witnesses using polynomial reduction modulo omega²+omega+1 rather than the author's pair-field operations, checking a nonzero rank5 minor and the entire point-set support. The six rational reducible-cubic witnesses also passed independent rank and support checks.

## 9. Verification and final boundary

All23 author hashes and all four pinned primary PDF hashes match. The five saved receipts replay exactly, including all29,835 fixed five-subsets and the1,018,610,873 later controls. The independent checker passes4,866 exact controls, with symbolic circuit minors, residual identities and actual ordinary-conic witnesses; its finite integer-threshold controls are separately itemized in the receipt.

The universal results rest on the proof audit above, not these totals. The final necessary counterexample conditions follow correctly: at least eleven points, no common cubic, and at most floor((n-2)/2) points on any line. They are not sufficient conditions for a counterexample and do not answer the unrestricted question. Preserve the historical/classical credit, all source conventions, the distinction from real/finite-field results, and the overall **unsolved5/5** disposition. No mandatory change to the frozen mathematical packet is required.
