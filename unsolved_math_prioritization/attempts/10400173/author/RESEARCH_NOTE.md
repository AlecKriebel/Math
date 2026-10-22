# Sato's lens-space question: an explicit A6 specialization and limits

**Record:** 10400173 / AMR-103-0173, queue rank 637.  
**Catalogue status proposed:** `unsolved`; five substantive approach families used.  
**Mathematical scope:** A rigorous finite calculation for the literal lens-space clause, known structural obstructions, and an explicit remaining scope gap. No novelty or complete-resolution claim.

## 1. Exact target and source boundary

Ohtsuki's edited problem list, printed p. 513, Problem 9.9, asks for a subfactor whose associated three-manifold invariant separates L(7,1) and L(7,2), and then asks for the strongest possible classification of three-manifolds by a subfactor. The neighboring prose about strongly amenable subfactors introduces the separately numbered Problem 9.10. It is not an additional requirement of Problem 9.9.

We use the Turaev-Viro-Ocneanu invariant of the finite-index, finite-depth subfactor, equivalently the state sum of either even unitary fusion category. Manifolds are closed and oriented. We normalize the state sum by TV(S2 x S1)=1 and TV(S3)=1/Dim(C).

The first clause has a literal answer using the Jones A6 subfactor. The second clause does not specify a class of manifolds, an order on classification strength, an index bound, or a success criterion. It is therefore retained as an unresolved, unformalized part of the bundled target. Interpreting it as complete separation of all closed oriented three-manifolds would make it false in the finite-depth setting, by Funar's theorem below.

The historical motivation concerned exotic subfactors, but no exclusion of Jones or quantum-group subfactors occurs in the printed question. Our calculation does not address an additional, unstated requirement that the example be exotic.

## 2. Approach 1: the realizable A6 category

### 2.1 Imported construction facts

Let N be the Jones subfactor with principal graph A6, of index

    [M:N] = 4 cos^2(pi/7).

Its even fusion category C is the even part of SU(2)5. This is the A_n construction explicitly identified in Kawahigashi, Example 4.1 [K]. Bischoff, Section 3.3 and Proposition 3.7 [B], gives the SU(2)k fusion and twist conventions and the corresponding subfactor construction. These are established construction theorems, not conclusions inferred from numerically plausible matrices.

The simple labels of C are 0, 2, 4. Their dimensions are sin((a+1)pi/7)/sin(pi/7). Writing the nontrivial objects as X=2 and Y=4, their fusion rules are

    X^2 = 1 + X + Y,   XY = X + Y,   Y^2 = 1 + X.

C inherits a unitary ribbon structure from SU(2)5. Its normalized S matrix and twist matrix are, in the displayed label order,

    S_ab = (2/sqrt(7)) sin((a+1)(b+1)pi/7),
    T = diag(1, exp(4 pi i/7), exp(12 pi i/7)).

The dimension normalization is determined by the even sector's total dimension 7/(4 sin^2(pi/7)). The S formula can also be recovered from the displayed fusion rules and twists by the balancing identity. Its square is the identity, so the inherited ribbon category is nondegenerate and is modular. In particular no modular extension of a degenerate category is being assumed.

For a unitary modular C, TV_C(W)=|RT_C(W)|^2. This is the modular case of the center theorem in Turaev-Virelizier [TV, Introduction and Theorem 11.1]. The quantum double of C therefore gives the actual subfactor state sum; we do not confuse a chiral RT phase with a TV value.

### 2.2 Exact lens-space calculation

Put z=exp(2 pi i/28). Then T=diag(1,z^8,z^24). In the cyclotomic field Q(z), the defining polynomial is

    Phi_28(z) = z^12 - z^10 + z^8 - z^6 + z^4 - z^2 + 1.

Set a=sin(pi/7), b=sin(3pi/7), c=sin(5pi/7). Then

    S = (2/sqrt(7)) [[a,b,c],[b,-c,a],[c,a,-b]].

Direct multiplication yields the following exact identities:

    S^2 = I,   T^7 = I,   (ST)^3 = z^4 I,

    ST^7S = I,

    ST^4ST^2S = [[0,0,z^6],[-z^4,0,0],[0,1,0]].

Here the nontrivial scalar in the modular relation is the unit-modulus framing anomaly. Squaring the absolute value removes it.

For a negative continued fraction p/q=[a1,...,an], the lens-space amplitude is the vacuum entry of ST^a1 S ... T^an S, up to a unit-modulus anomaly. Sato-Wakui [SW, p. 28] gives the corresponding exact lens-space formula for an anomaly-free TQFT. Applying it to the double of C is equivalent to taking the absolute square of the chiral matrix entry. In particular, 7/1=[7] and 7/2=[4,2]. Thus

    TV_A6(L(7,1)) = |1|^2 = 1,
    TV_A6(L(7,2)) = |0|^2 = 0.

This proves separation under the literal wording of the first clause. It persists under opposite braiding, orientation reversal, and a common nonzero normalization change.

### 2.3 A finite exact certificate

`verify.py` uses rational polynomial arithmetic modulo Phi_28 and does not use a floating-point zero tolerance. It constructs sqrt(7) from the quadratic Gauss sum, then computes S and T from the formulas. It checks the entire displayed matrices, their modular relations, the division-free Verlinde identities for all three fusion matrices, and all nine ribbon balancing identities. It also checks every q=1,...,6 for p=7, obtaining

    q=1,6: TV=1;    q=2,3,4,5: TV=0.

Normalization checks give TV(S3)=S00^2 and TV(S2 x S1)=1. The continued-fraction replacement [4,2] -> [5,1,3] leaves the squared amplitude unchanged. Conjugated twists give the same two target values. Replacing the twists by identity fails the required modular relation and is explicitly rejected as valid category data.

These controls certify the finite algebra, while the cited construction and state-sum theorems supply the topological interpretation. A polynomial computation alone would not establish realizability.

## 3. Approach 2: generalized E6 and orientation sensitivity

The natural exotic candidate suggested by the original discussion is the generalized E6 system with cyclic symmetry of order seven. Wakui's 2007 report [W, p. 10], based on joint work with Sato, records the same value for L(7,1) and L(7,2):

    (11 - i sqrt(11))/22.

This is a source-attributed computation; we have inspected its table and conclusion but have not independently regenerated its large tube-algebra data. It rules out that particular proposal, not every subfactor. The nearby systems in that report also have equal values on the target pair.

The nonreal number is important: a unitary subfactor state sum need not be real when its even category is not braided. The identity TV=|RT|^2 used in Section 2 requires the INPUT category itself to be unitary modular. It must not be imposed on the generalized E6 input. For a general unitary fusion category the relevant equality is TV_C=RT_Z(C), whose value can be nonreal.

Wakui's introduction still described the general subfactor separation problem as open. This historical statement and the explicit A6 specialization must both be retained in the audit. The scope of the historical motivation, and the fact that it focused on exotic examples, is not evidence for a restriction absent from the printed question. The present note makes no claim to be the first place this elementary specialization was observed.

## 4. Approach 3: finite groups and cocycle twisting

For a finite group G and a class omega in H^3(BG,U(1)), the Dijkgraaf-Witten formula is

    Z_G,omega(M) = (1/|G|) sum_phi <phi^*omega,[M]>,

where phi ranges over based homomorphisms pi1(M)->G; see Dijkgraaf-Witten [DW, (6.8)-(6.9)]. If f:M->N is an orientation-preserving homotopy equivalence, composition with f gives a bijection between the summands and preserves their weights by naturality and f_*[M]=[N]. Consequently all these invariants agree on M and N.

The lens spaces L(7,1) and L(7,2) are orientation-preserving homotopy equivalent: the lens-space criterion reduces here to 2 being a square modulo 7, and 3^2=2 modulo 7. They are not homeomorphic, since 2 is neither plus nor minus 1 modulo 7, even after inversion. Therefore neither untwisted group counting nor any finite-group 3-cocycle twist can solve this pair.

An explicit stress test evaluates the cyclic order-14 candidate with cocycle

    omega(a,b,c) = exp(2 pi i a([b]+[c]-[b+c])/14^2).

For q=1 and q=2, the lens expression using n=q^-1 modulo 7 sums over 7a=0 in Z/14. Both have exactly the same rational-phase histogram:

    0: one occurrence; 1/7, 2/7, 4/7: two occurrences each.

Hence both values are (1+2zeta+2zeta^2+2zeta^4)/14, with zeta=exp(2 pi i/7). All fourteen powers of the cocycle also agree. This corrects a tempting but invalid separation test found during source discovery; it is an exact equality, not a numerically inconclusive result. No external communication was made.

## 5. Approach 4: the universal congruence obstruction

Funar [F, Theorem 1.1, printed p. 2291] supplies pairs of nonhomeomorphic closed oriented SOL torus bundles that agree for EVERY spherical fusion category. One explicit parameter choice is k=1, q=5, v=4 in that theorem, giving

    A = [[1,25],[4,101]],    B = [[1,1],[100,101]].

The hypotheses require q prime with q=1 modulo 4, v positive, -v a nonzero square modulo q, and v divisible by 4 or by a prime congruent to 3 modulo 4. They hold: -4=1 modulo 5 and 4 divides v. Both matrices have determinant 1 and trace 102, hence are hyperbolic.

The theorem proves that their torus bundles have nonisomorphic fundamental groups yet equal TV invariants for every spherical fusion category. As a finite sanity check, the control program finds determinant-one conjugators modulo each integer 2 through 100 and checks AC=CB modulo that integer. This finite experiment is NOT a proof of conjugacy for every modulus, and does not prove integral nonconjugacy. Those universal facts are supplied by Funar's theorem and its arithmetic proof.

Every finite-depth subfactor even category lies inside this spherical category class. Thus no single such subfactor, and indeed not even the collection of all of them, completely classifies all closed oriented three-manifolds. This is a published obstruction, not a new counterexample.

The theorem does not dispose of an undefined goal such as obtaining a useful or optimal partial classification. Nor does it cover an unspecified infinite-depth construction: the source's separate Problem 9.10 concerns the difficulty of defining such state sums.

## 6. Approach 5: combining or changing presentations of categories

Two natural attempts to improve classification are replacing a fusion category by a Morita equivalent one, and taking Deligne tensor products.

Morita equivalence preserves the center, and hence the associated TV TQFT. Turaev-Virelizier [TV, Corollary 11.5] states the relevant invariance. Therefore a new subfactor presentation with the same even category up to Morita equivalence does not create a stronger invariant.

For a finite product C1 box ... box Cr, the simple labels, dimensions, and local state-sum weights factor. Summing independently over the labels gives

    TV_(C1 box ... box Cr)(M) = product_j TV_Cj(M).

This also follows by tensor-factorization of the corresponding TQFTs. Consequently a pair on which every factor agrees remains a collision for their product. In particular, tensoring failed generalized E6 or finite-group tests cannot remove their shared collision. Funar's universal pair remains indistinguishable even if successful lens-space separators are added as factors. The program checks tensor-factorization directly for the 9-by-9 modular data of C box C on three lens-space surgery words.

Conversely, a product need not retain every distinction made by an individual factor, because a second factor may vanish on both manifolds. Thus counting or combining many invariant values without retaining them separately is not automatically an improvement. A classification objective and an admissible family must be specified before an optimality claim is meaningful.

## 7. Final status and precise gap

The literal L(7,1) versus L(7,2) subproblem has the explicit A6 calculation above. The historical generalized-E6 candidate fails, all finite-group cocycle theories fail for homotopy reasons, and a complete finite-depth subfactor classification of arbitrary three-manifolds is obstructed by a published theorem. None of these establishes an optimal partial classification for the open-ended second clause.

The record therefore remains `unsolved`, with the literal lens-space clause distinguished as a resolved subproblem and the whole-source target not promoted. A next mathematical target would need to specify the allowed subfactors and manifold class, and define an order or measurable criterion for classification power. This note also does not assert novelty of the A6 specialization, which is built from long-established ingredients. Sokolov's 1997 lens-space paper was identified bibliographically, but its full text was unavailable in this inspection; it is not used as a theorem-level dependency or a certified prior resolution.

## References and inspected locations

- [O] T. Ohtsuki (editor), *Problems on invariants of knots and 3-manifolds*, 2002. Printed p. 513 / PDF page 141. https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf
- [K] Y. Kawahigashi, *A characterization of a finite-dimensional commuting square producing a subfactor of finite depth*. Example 4.1, PDF pp. 10-11. https://arxiv.org/abs/2111.14332
- [B] M. Bischoff, *A Remark on CFT Realization of Quantum Doubles of Subfactors. Case Index < 4*. Section 3.3 and Proposition 3.7. https://arxiv.org/abs/1506.02606
- [SW] N. Sato and M. Wakui, *Computations of Turaev-Viro-Ocneanu invariants of 3-manifolds from subfactors*. PDF p. 28 and Section 5. https://arxiv.org/abs/math/0208242
- [TV] V. Turaev and A. Virelizier, *On two approaches to 3-dimensional TQFTs*. Introduction, Theorem 11.1, Corollary 11.5. https://arxiv.org/abs/1006.3501
- [W] M. Wakui, *On the Turaev-Viro-Ocneanu invariant of 3-manifolds derived from generalized E6-subfactors*, 2007 report. PDF pp. 1, 10. https://www2.itc.kansai-u.ac.jp/~wakui/ILDT07wa.pdf
- [DW] R. Dijkgraaf and E. Witten, *Topological Gauge Theories and Group Cohomology*, 1990. Section 6.2, formulas (6.8)-(6.9). https://www.ias.edu/sites/default/files/sns/%5B126%5DCommMathPhys129-1990.pdf
- [F] L. Funar, *Torus bundles not distinguished by TQFT invariants*, Geometry & Topology 17 (2013), 2289-2344. Theorem 1.1 and Propositions 1.1-1.3. https://msp.org/gt/2013/17-4/gt-v17-n4-p09-s.pdf
- Bibliographic lead only: M. V. Sokolov, *Which lens spaces are distinguished by Turaev-Viro invariants*, 1997. https://doi.org/10.1007/BF02355426
