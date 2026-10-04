# Minimal subdegrees of twisted-wreath groups: proved partial results

Problem 30000203 / OWR-793-006. Research date: 2026-10-04 (UTC).

**Disposition: unsolved.** None of the statements below settles the universal strict inequality. The exact reduction is an independent rederivation of the established construction in Giudici--Li--Praeger--Seress--Trofimov [GLPST], Section 4; it is not claimed as new. The finite example and the elementary criteria are supplied as checkable research artifacts. No novelty priority is asserted.

## 0. Exact question and conventions

Let G be a finite primitive permutation group of twisted-wreath type. Write its regular socle as B = T^k, where T is nonabelian simple and k >= 2. Write G = B semidirect P, where P is a point stabilizer and acts transitively on the k simple factors. The primitive component is H = T semidirect phi(Q), where Q is the stabilizer in P of one factor and phi: Q -> Aut(T) has image containing Inn(T). Put

- k = [P:Q];
- B = { f: P -> T : f(xq) = f(x)^{phi(q)} for x in P, q in Q };
- f^p(x) = f(px);
- s = MinSubDeg(G), and m = MinSubDeg(H).

The functions B are a direct product of k copies of T, via evaluation on a left-coset transversal. The point stabilizer at the identity function is P, so s is the smallest P-orbit size on B minus the identity. The component point stabilizer is phi(Q), so m is its smallest orbit size on T minus the identity.

The question is whether s < k m for every such primitive group. The known inequality s <= k m is not enough. A negative solution requires a primitive example with equality and a proof that no shorter orbit exists.

For t != 1 define

C_t = { q in Q : t^{phi(q)} = t }, and c = max_{t != 1} |C_t|.

Then m = |Q|/c and k m = |P|/c. All maxima and minima below are over finite nonempty sets.

## 1. Exact subgroup optimization, and why support one cannot prove strictness

### Proposition 1

Call R <= P admissible if C_T(phi(R intersect Q)) contains a nonidentity element. Put M = max { |R| : R is admissible }. Then

s = |P|/M.

Consequently the exact original question is equivalent to M > c for every primitive twisted-wreath datum. Equality s = k m is equivalent to M = c.

### Proof

Choose t != 1 fixed by phi(R intersect Q). Define

f_{R,t}(rq) = t^{phi(q)} for r in R, q in Q,

and set f_{R,t}(x) = 1 outside RQ. If rq = r' q', then q' q^{-1} = (r')^{-1}r belongs to R intersect Q, so t^{phi(q')} = t^{phi(q)}. Thus the definition is well-defined, and f_{R,t} belongs to B. Left multiplication by R preserves RQ and the defining values, so R fixes f_{R,t}. This nonidentity function has orbit size at most [P:R]. Taking |R| = M gives s <= |P|/M.

Conversely, take any nonidentity f in B. Choose p with f(p) != 1 and replace f by f^p, so t = f(1) != 1. If R is its stabilizer in P, then for q in R intersect Q,

t = f(1) = f(q) = t^{phi(q)}.

Therefore R is admissible and |R| <= M. Every nonidentity orbit has size at least |P|/M. This proves the formula.

An admissible R cannot equal P: phi(Q) contains Inn(T), and the only element fixed by all inner automorphisms of the centerless group T is 1. Thus the functions used above never create an extraneous nonidentity fixed point. Also C_t is admissible, so M >= c. QED.

### Proposition 2: support-one saturation

For the function f supported on exactly the coset Q with f(q) = t^{phi(q)}, its stabilizer in P is exactly C_t. Indeed, a stabilizing p preserves its nonidentity support Q, so pQ = Q and p belongs to Q. Evaluation at 1 then forces p in C_t; conversely such p fixes f. Hence its orbit size is

[P:C_t] = k |t^{phi(Q)}|.

In particular, using a shortest component orbit gives exactly k m, never a strict improvement. The historical desk-review suggestion of a one-coordinate point verifies the old upper bound but does not establish the target.

**Exact gap of approach 1.** Construct an admissible subgroup of order larger than c, or show one does not exist in a valid primitive example. Restating that existence requirement is not a proof of it.

## 2. A local normalizer extension criterion and an obstruction to restricting values

### Proposition 3

Fix t != 1 and C = C_t. Let N = N_P(C) and A = (N intersect Q)/C <= N/C. If N/C has a subgroup K with K intersect A = 1, its full preimage R in N satisfies

R intersect Q = C, |R| = |C||K|,

and is admissible. Thus s <= |P|/(|C||K|); strictness follows if |C||K| > c.

In particular, when |C| = c, any nontrivial such K suffices. One elementary sufficient condition is a prime ell dividing |N/C| but not |A|: an ell-Sylow subgroup of N/C is then nontrivial and intersects A trivially.

### Proof

C is normal in N. Intersection in the quotient gives (R intersect Q)/C = K intersect A = 1, so R intersect Q = C. By definition C fixes t. Proposition 1 applies. For the prime condition use Lagrange's theorem. QED.

The condition N > N intersect Q alone is not sufficient to produce such K: for example a cyclic group of order four and its subgroup of order two have no nontrivial subgroup with trivial intersection. No unconditional quotient-splitting assertion is used here.

### Proposition 4: failure of the shortest-component-class restriction

For P = A6, Q = T = A5 (fixing the letter 6), and phi given by conjugation, fix a 5-cycle t in Q. Then every R <= A6 satisfying R intersect Q <= C_Q(t) has order at most five. Thus the least index obtainable with this fixed t is 72, exactly k m. This holds for every t in either shortest A5 conjugacy class. Nevertheless the true minimum subdegree is 15 (Section 5).

### Proof

Here C_Q(t) is cyclic of order five. Let D = R intersect Q, and r = [R:D], the size of the R-orbit of 6. Then r <= 6 and |D| is either 1 or 5.

If |D| = 1, then |R| <= 6. The only possibility greater than five is |R| = 6, in which case R would be regular on all six letters. Cauchy's theorem gives an involution in R, but every involution in A6 is a product of two disjoint transpositions and fixes two letters. This contradicts regularity.

If |D| = 5, then |R| = 5r divides 360. Apart from r = 1, the possible r are 2, 3, 4 and 6 (r = 5 would give the impossible divisor 25). For orders 10, 15 or 20, Sylow's theorem makes the subgroup of order five normal. Its unique fixed letter is 6, so its normalizer fixes 6; hence R <= Q, contradicting |D| = 5 < |R|. For order 30, R is transitive and its point stabilizers have order five. An involution of R exists by Cauchy's theorem and fixes a letter, so belongs to an odd-order point stabilizer, again impossible. This exhausts the possibilities. The subgroup C_Q(t) itself has order five and is admissible. QED.

For the same t, N_{A6}(C_Q(t)) has order ten and lies in Q: it preserves the unique fixed letter. Thus the normalizer route already fails at a smallest primitive twisted-wreath example if one insists on a shortest component class.

**Exact gap of approach 2.** Primitivity does not supply a quotient subgroup K of the required size and disjointness. Successful witnesses may use a larger component conjugacy class and need not normalize the intersection with Q.

## 3. A Sylow fixed-point criterion

### Proposition 5

For every prime p dividing |T|, a Sylow p-subgroup S of P fixes a nonidentity element of B. Hence G has a nontrivial subdegree dividing [P:S], and in particular

s <= |P|/|P|_p.

If |P|_p > c for some p dividing |T|, then the original strict inequality holds for this datum.

### Proof

The p-group S acts on the finite set B. Every orbit except a fixed point has size divisible by p, so |B^S| is congruent to |B| modulo p. Since |B| = |T|^k is divisible by p and the identity is fixed, |B^S| is a positive multiple of p. It is therefore at least p, and some nonidentity f is fixed. Its stabilizer contains S, so [P:P_f] divides [P:S]. Compare with k m = |P|/c. QED.

This route proves strictness for A5 twisted by A6 without finding its actual minimum: c = 5, |A6|_2 = 8 and |A6|_3 = 9, yielding respectively s <= 45 and s <= 40, both below 72.

It is not a universal argument. For P = A20 and Q = T = A19, the centralizer in Q of a 3-cycle already has order

3(16!)/2 = 31,384,184,832,000.

Thus c is at least this large. Every Sylow subgroup of A20 is smaller: their orders are 131072, 6561, 625, 49, 11, 13, 17 and 19. The strict numerical premise fails for every relevant prime. These exact factorial calculations are in the control file; no asymptotic assertion or unproved formula for the minimum class of A19 is needed.

This is a legitimate primitive twisted-wreath datum: A20 is primitive on 20 letters, its point stabilizer A19 maps onto Inn(A19), and the simple group A20 has no quotient A19. The sufficient primitivity criterion [CGM, Theorem 2.3] applies.

**Exact gap of approach 3.** One must combine prime-power fixed-point information into a substantially larger stabilizer, or find a different witness. The p-group congruence alone imposes no such enlargement.

## 4. Double-coset fixed points and an exact failure of global averaging

### Proposition 6

For any R <= P, choose representatives s_i for R\P/Q. Evaluation at the s_i gives a group isomorphism

B^R  ~=  product_i C_T(phi(s_i^{-1} R s_i intersect Q)).

### Proof

If f is fixed by R, it is constant on each left R-coset, and equivariance gives f(r s_i q) = f(s_i)^{phi(q)}. This assignment is well-defined precisely when f(s_i) is fixed by phi(s_i^{-1} R s_i intersect Q): if r s_i q = r' s_i q', then q' q^{-1} = s_i^{-1}(r')^{-1}r s_i lies in that intersection. Different double cosets are independent. Pointwise multiplication corresponds to componentwise multiplication of the values. QED.

This gives exact fixed-point counts, and Burnside's lemma gives the number a of P-orbits in B:

a = (1/|P|) sum_{p in P} |B^{<p>}|.

If every nonidentity orbit had size at least L = k m, then |B|-1 >= (a-1)L. Consequently

(a-1)L > |B|-1

would prove strictness. The converse is not asserted.

For P = A6, Q = T = A5, the exact data are:

| Cycle type in A6 | Number of elements | Fixed functions in B |
| --- | ---: | ---: |
| 1^6 | 1 | 60^6 |
| 1^3 3 | 40 | 1,620 |
| 1^2 2^2 | 45 | 57,600 |
| 1 5 | 144 | 300 |
| 2 4 | 90 | 240 |
| 3^2 | 40 | 3,600 |

The two A6 classes of 5-cycles are grouped because their fixed-function counts agree. Proposition 6 computes the table without enumerating any of the 60^6 points. For instance a 3-cycle has one orbit of length three on the coordinates, contributing |T| = 60, and three fixed coordinates, each contributing a centralizer of order three; the product is 1620.

The resulting number of orbits is a = 129,607,960. The average nonidentity orbit size is exactly

46,655,999,999 / 129,607,959,

which is greater than 72. Therefore this global averaging test cannot even detect the orbit of size 15 in this example. This is a proved failure of the proposed sufficient test, not a counterexample to the original question.

**Exact gap of approach 4.** A refined statistic isolating rare large stabilizers is needed. Ordinary Burnside averaging is dominated by large orbits; evaluating it does not bound the minimum below k m.

## 5. Exact smallest example and a conjugacy-class consistency check

### Proposition 7

For G = A5 twr_phi A6 with Q = A5 fixing 6 and phi(q) conjugation by q,

MinSubDeg(H) = 12, k = 6, and MinSubDeg(G) = 15.

### Proof of the hypotheses

A6 acts primitively on six letters with point stabilizer A5. The image of phi is Inn(A5). Since A6 is simple and has order 360, it has no quotient isomorphic to A5. Thus [CGM, Theorem 2.3] gives a primitive twisted-wreath group with regular socle A5^6. This uses standard simplicity of A_n for n >= 5 and the stated published sufficient criterion, not an unverified computational test of primitivity.

### Proof of the minimum

The centralizer orders of nonidentity elements of A5 are 3, 4 and 5: its element types are a 3-cycle, a product of two transpositions and a 5-cycle. Thus c = 5 and m = 60/5 = 12.

Let R be any admissible subgroup, choose t != 1 with R intersect Q <= C_Q(t), and write d = |R intersect Q| and r = [R:R intersect Q] <= 6. Then d <= 5. If |R| = dr > 24, we must have d = 5 and r = 5 or 6. The value 25 cannot divide |A6| = 360. For |R| = 30 the group R would be transitive on six letters with point stabilizers of order five. Every involution of A6 fixes two letters, whereas Cauchy's theorem gives an involution in R, a contradiction to these odd-order point stabilizers. Hence every admissible R has order at most 24.

Now let R be the even permutations preserving the unordered partition

{ {1,3}, {2,4}, {5,6} }.

The full partition stabilizer is S2 wr S3, of order 48; exactly half are even, so |R| = 24. An element in R intersect Q fixes both 5 and 6 and preserves the first two pairs. Its action on {1,2,3,4} is the Klein four group

{1, (13)(24), (12)(34), (14)(23)}.

Take t = (13)(24). The intersection centralizes t, so R is admissible. We have proved M = 24, and Proposition 1 gives s = 360/24 = 15. In particular 15 < 72. QED.

The explicit f_{R,t} is checked by the control script on all 360 arguments; it is equivariant, its full stabilizer is exactly R, and its orbit therefore has size 15. The script also independently enumerates all 501 subgroups of A6: 432 are admissible, the largest admissible order is 24, and the largest admissible order for a fixed 5-cycle is five. The elementary proof above does not depend on trusting that enumeration.

### Proposition 8: the A8 exception

For H = A8 semidirect Inn(A8), MinSubDeg(H) = 105, not 112.

For a permutation with a_i cycles of length i, its symmetric-group centralizer order is z = product_i i^{a_i} a_i!. Its centralizer in A_n has order z/2 unless all cycle lengths are odd and distinct, in which case it has order z. To see the criterion, an even-length cycle is itself an odd commuting permutation; swapping equal odd cycles is also odd. If neither exists, the centralizer is generated by distinct odd cycles and is entirely even.

For completeness the possible nonidentity even types in S8, and individual A8 class sizes, are:

| Type | A8 class size | Number of such A8 classes |
| --- | ---: | ---: |
| 1^5 3 | 112 | 1 |
| 1^4 2^2 | 210 | 1 |
| 1^3 5 | 1344 | 1 |
| 1^2 2 4 | 2520 | 1 |
| 1^2 3^2 | 1120 | 1 |
| 1 2^2 3 | 1680 | 1 |
| 1 7 | 2880 | 2 |
| 2^4 | 105 | 1 |
| 2 6 | 3360 | 1 |
| 3 5 | 1344 | 2 |
| 4^2 | 1260 | 1 |

This is exhaustive by the partitions of 8 with an even number of even-length cycles. Its class sizes, with multiplicity, add to 20159. In particular t = (12)(34)(56)(78) has centralizer order (2^4 4!)/2 = 192 and class size 20160/192 = 105, the smallest entry.

For the primitive datum P = A9, Q = T = A8, the 3-cycle u = (123) nonetheless supplies an admissible subgroup R = C_{A9}(u) of order 3(6!)/2 = 1080. Thus

s <= 181440/1080 = 168 < 9(105) = 945.

This proves strictness for this datum despite the exception. It does not assert that 168 is the exact minimum.

### Carefully scoped source corrections

1. The accessible author-upload text of [GLPST], Example 4.15, gives the shortest A_{n-1} class as 2 binomial(n-1,3) for n > 6 and displays s = n m/(n-3). At n = 9, the component value 105 proved above makes the displayed ratio 157.5, which cannot be a subdegree. The all-n component-class assertion therefore needs at least an A8 exception. The publisher's version of record was not inspected; the observation is specifically about the accessible author-upload rendering. It does not falsify the construction, the general bounds, or the original open question.
2. The July 23, 2021 author manuscript of Burness--Shalev [BS], Remark 3.9, p. 15, assigns minimum 12 to the A5/A6 twisted-wreath example. Proposition 7 proves 15 for the example specified there by its reference to [GLPST, Example 4.15]. The manuscript PDF was visually checked. Its conclusion about solvability of two-point stabilizers does not require equality with 12: the known lower bound of 12 already excludes the stated index-six nonsolvable case. This is a correction to the numerical sentence, not a challenge to that conclusion or the paper's main theorems. No author was contacted.

The A8 conjugacy-class count and the 15-subdegree witness are established mathematical objects; this report does not claim their novelty or that either discrepancy has never been noticed.

The finite cycle-partition controls also check component minima for 5 <= n <= 30. They are explicitly bounded checks, not a proof of a formula for all n or a classification of all twisted-wreath data.

## 6. Exact remaining gap

For arbitrary finite primitive twisted-wreath data (T,P,Q,phi), prove that there is R <= P and t != 1 such that

R intersect Q <= C_t and |R| > max_{u != 1}|C_u|,

or give a valid primitive datum for which every such R has order at most that maximum. The five mechanisms above supply reductions, sufficient cases and finite checks. They do not establish either universal alternative. The correct campaign disposition is **unsolved, five substantive approaches exhausted**, with no complete candidate and no verified prior resolution.

## References

- [OWR] C. E. Praeger and A. Seress, “On minimal subdegrees of finite primitive permutation groups,” in Groups and Geometries, Oberwolfach Reports 12/2005, pp. 690--693; Question 4 on p. 692. https://doi.org/10.4171/owr/2005/12 . Official report: https://publications.mfo.de/bitstream/handle/mfo/2886/OWR_2005_12.pdf?sequence=1 .
- [GLPST] M. Giudici, C. H. Li, C. E. Praeger, A. Seress and V. Trofimov, “On minimal subdegrees of finite primitive permutation groups,” Finite Geometries, Groups, and Computation (2006), pp. 75--94. https://doi.org/10.1515/9783110199741.75 . Author-upload text: https://www.researchgate.net/publication/228677624_On_minimal_subdegrees_of_finite_primitive_permutation_groups . Question 1.6; Construction 4.1; Lemmas 4.2--4.3; Construction 4.12; Example 4.15. The main reduction here is established material re-proved for auditability.
- [CGM] A. Y. Chua, M. Giudici and L. Morgan, “Coprime subdegrees of twisted wreath permutation groups,” Proc. Edinburgh Math. Soc. 62 (2019), 1137--1162. https://doi.org/10.1017/S0013091519000130 . Author preprint: https://arxiv.org/abs/1801.02456 , Theorem 2.3 and Section 2. It addresses a different coprime-subdegree question, not the universal strict inequality here.
- [BS] T. C. Burness and A. Shalev, “Permutation groups with restricted stabilizers,” J. Algebra 607 (2022), 160--185. https://doi.org/10.1016/j.jalgebra.2021.08.012 . Inspected author manuscript dated July 23, 2021: https://seis.bristol.ac.uk/~tb13602/docs/BSh_final.pdf , Remark 3.9, p. 15. The mathematical conclusion attributed here is limited to the inspected manuscript.
