# Independent analytic derivation — record 23124601

This derivation concerns the entire stated fixed-generator theorem. It was reconstructed from the actual six-page paper and complete controlling TeX before foreign primary bodies, archived review narratives, current opinions, or supplied verification code were read. The initial reconstruction is preserved separately by EARLY_SEAL.json. The computations below use newly authored code and no supplied action records. Classical imports are identified explicitly; they are not proved by a finite computation.

## 1. Universe, quotient, and equivalences

Write B6 = <a1,...,a5 | adjacent braid relations and distant commutations>. Let

    c = (a1 a2 a3 a4)^5,
    h = a5 a4 a3 a2 a1 a1 a2 a3 a4 a5,
    d = a1 a2 a3 a4 a5,
    z = d^6,
    G = B6 / <<c h^-1>>.

The standard full-twist decomposition is z = ch = hc in B6. My faithful F6 action independently verifies both word equalities, all five centrality equalities z ai = ai z, and the four shifts d ai d^-1 = a(i+1), i=1,...,4. In G, c=h, hence c²=h²=z. The equality c²=z is in G; it is false in B6 by exponent sum. The F6 representation is used on B6, while a different F4 action descends to G.

Inputs are literal positive words in the five fixed generators whose product is c² in G. They are not arbitrary tuples of conjugates. A strict Hurwitz move sends (x,y) to (xyx^-1,x), with its inverse also permitted. Intermediate tuples can contain conjugates. Global conjugation of every factor is a separately allowed operation only for the second equivalence convention.

The claim is one strict class at length 20, one at length 30, two at length 40, and no other lengths. The length-20 inputs are asserted to be exactly ten literal words. Global conjugation merges precisely the two length-40 classes. All these claims are retained here.

## 2. Why the search is finite: the geometric input

The five-curve chain has genus-two, two-boundary regular neighborhood. Capping one boundary produces five nonseparating curves on the genus-two one-boundary surface. The odd chain relation sends z to the remaining boundary twist; the even four-chain relation sends c² to that same twist. From z=ch their images satisfy c=h, so the B6 homomorphism factors through G. No injectivity of G is needed for this step.

Baykur–Monden–Van Horn-Morris, Theorem A, applies to the product of all boundary twists on a genus-g surface with n>=1 boundaries, where length counts positive twists about nonseparating curves. At g=2,n=1 its finite exact maximum is 40. These are precisely the image curves and target here. Consequently every input has length m<=40. The relation c=h has exponent sums 20 and 10; the usual braid abelianization gives G_ab = Z/10. Thus m belongs to {0,10,20,30,40}.

This is a deduction using the published length theorem, not a new proof of that theorem or a numerical assumption about length. The actual theorem and definitions were read. The alternative Sato attribution is discussed in REPORT.md and is not needed in this proof.

## 3. Necessary linking constraints for every input

The relator is pure. Thus the permutation map descends to G and any input is pure as a B6 braid. For a pure braid, l_ij is half the signed crossing count of labelled strands i,j. It is an integer homomorphism on the pure braid group; conjugation by any braid permutes label pairs. Positivity makes every l_ij>=0 and m=2 sum l_ij.

The vector beta of c² is 2 on the ten pairs among labels 1,...,5 and 0 on the five pairs incident to label 6. The relator c h^-1 has vector +1 on pairs away from label 6 and -1 on pairs incident to it. Its B6 conjugates therefore have vectors

    (r_k)_ij = 1 - 2*1_{k in {i,j}}.

If w(c²)^-1 belongs to the normal closure, additivity gives signed integers t1,...,t6, with T=sum ti, such that

    l_ij(w) = beta_ij + T - 2(ti+tj) >= 0,
    T = m/10 - 4.

The second equality follows either from exponent sums (each conjugated relator has exponent 10) or by summing the first over all 15 pairs. This uses only a necessary consequence of normal-closure membership. No sufficiency of linking data or abelian quotient is used.

Put s=t1+...+t5, t6=T-s. Internal pairs have ti+tj<=floor((T+2)/2); pairs with label 6 have ti+t6<=floor(T/2).

* T=-4 or -3: summing the internal inequalities yields s<=-3. The exterior sums yield s>=ceil((5T+10)/4), respectively -2 or -1, a contradiction. This excludes the empty word and length 10.
* T=-2: the sums give -1<=s<=0. If s=-1, t6=-1 and each first ti<=0, so exactly one first ti is -1. If s=0, t6=-2 and internal pair sums are <=0. A positive maximum M would force the other four entries <=-M and s<=-3M<0, impossible. Thus all first entries are 0. The six resulting linking vectors are exactly doubled stars.
* T=-1: the sums force s=0,t6=-1; the exterior inequalities force all first entries <=0, hence all 0. Every linking number is 1.
* T=0: the exterior sum gives s>=0. If the maximum first entry M>=1, internal inequalities make s<=4-3M<=1; if M<=0 then s<=0. For s=0, t6=0 and exterior inequalities force all first entries <=0, so all entries are 0. For s=1, t6=-1, each first entry <=1, at most one can be 1, and their sum forces one 1 and four 0. These are exactly the six doubled five-vertex cliques.

As a separate exact control on arbitrary signed integers, set a_ij=floor((beta_ij+T)/2), D_i=sum_{j!=i}a_ij and C_i=sum_{j<k; j,k!=i}a_jk. Summing pair inequalities involving i gives 4ti+T<=D_i. Summing those excluding i gives 4(T-ti)<=C_i. Therefore the finite, proved coordinate bounds are

    T - floor(C_i/4) <= ti <= floor((D_i-T)/4).

Enumerating only these exact integer boxes gives 0,0,6,1,6 solutions for m=0,10,20,30,40. These computations check the preceding proof; a guessed cutoff would not establish it. The explicit solutions and bounds are retained in SMALL_CERTIFICATES.json.

## 4. Length 40: two strict classes

A positive isolated strand has zero crossings, so it remains at its initial position. If that position is interior, labels on opposite sides never cross, contradicting the required clique on the other five labels. Therefore the isolated label is 1 or 6.

At isolated label 6, the word uses only a1,...,a4. Their four-chain neighborhood is the genus-two one-boundary surface, up to a collar. The A4 case of the actual Perron–Vannier theorem as stated in Wajnryb gives injectivity of this B5 chain homomorphism. Equality of w and c² in G gives equality of their geometric images, hence equality in B5. Embedding of the positive Artin monoid then means their positive words are connected by the defining positive relations. A distant commutation is a Hurwitz swap. For the braid relation, two inverse moves give

    (x,y,x) -> (y,y^-1xy,x)
            -> (y,x,x^-1 y^-1 x y x) = (y,x,y),

because xyx=yxy. Every such factorization is therefore in the strict class of (a1a2a3a4)^10. The symmetric endpoint gives the class of (a2a3a4a5)^10.

Strict Hurwitz moves preserve the subgroup generated by all factors. The S6 images of these two subgroups are respectively S5 fixing 6 and S5 fixing 1. They are distinct (the independent subgroup enumeration gives 120 elements in each), so the two strict classes are different. On the other hand d ai d^-1=a(i+1), so simultaneous conjugation by d identifies the two tuples. Their product remains z because z is central in G.

## 5. Length 20: complete walks, sound rejection, separate acceptance

The doubled-star linking vector forces one labelled strand to cross each other label exactly four times, and no crossings among the other five labels. Those five remain in their fixed relative order. The distinguished strand follows a nearest-neighbor walk on positions 1,...,6, beginning and ending at its initial position. Each edge corresponds to one of the fixed other labels and is traversed exactly four times; traversing position edge i writes letter ai. Conversely such a walk gives a pure word with exactly the required star crossings. The correspondence is complete in both directions.

My unpruned recursion chooses each available neighboring position while its edge count is below four. At depth 20, closure and the caps force all five edge counts to be four. It finds 81,162,162,162,162,81 walks for the six starting positions, total 810. Every resulting literal word is separately checked by moving the six labelled strands: it is pure and has exactly the claimed star crossings. No quotient rejection test prunes this universe.

The manuscript's F4 table and displayed inverse table were transcribed from the TeX into newly written free-word substitution code. Both compositions for each of the five inverses, all four adjacent braid relations, all six distant commutations, and A_c=A_h hold as complete reduced free words. Thus the table is an action of G. This is a presentation argument, not a claim of faithfulness. A malformed A5 image fails its inverse identity in a negative control.

All four complete reduced images of each of the 810 literal words were computed and compared with those of c². Exactly 1,2,2,2,2,1 words pass for the six starts. The complete ten-word set is literally the set of distinct cyclic rotations of h². The full 810 word/image records are retained in the ignored cache. The comparison uses full words; no equality is inferred from a hash.

Since this action descends to G, a failed comparison soundly excludes a candidate. A passing comparison alone would not prove membership. Membership is certified separately: h²=z is central in G, so each cyclic rotation has that same product. Successive inverse Hurwitz moves move the first factor to the end with final conjugate P^-1 g1 P; for central total product P this is g1. Hence all ten are strictly equivalent. This proves both the literal survivor assertion and the one-class assertion.

## 6. Length 30: a finite proof for all complete words

Every labelled pair crosses exactly twice. A state q records the 15 crossing counts in {0,1,2}, with base-3 encoding. A legal positive generator swaps adjacent current labels and increments their pair count unless already 2. Counts increase, so paths have length at most 30. For a reachable state, the parity for each pair says whether its relative order has reversed. It determines the current permutation uniquely. My graph construction checks this consistency whenever two paths merge. This justifies merging continuation states, but does not assume equal braid actions for arbitrary merged prefixes.

The separately authored breadth-first construction gives R with 234,368 states and 711,342 legal edges. Let f be the all-two vector; it is reachable, pure, and has depth 30. Candidate words are exactly paths 0->f.

A reachable q has a completion iff f-q is reachable: reverse the positive adjacent swaps of a completing suffix from the final identity permutation. This has complementary labelled counts. Conversely a reaching path for f-q ends at q's permutation because their pair parities agree; reversing that positive sequence completes q. This reverses a sequence of swaps, not their braid signs. Thus S=R intersect (f-R). I independently built every reverse edge of the forward DAG and traversed backward from f; its result agrees at every R state with this complement criterion. The computation does not assert that the unrestricted reverse universe equals S. S has 90,921 states and 261,810 edges.

In rank 6 use the manuscript's signed free-group action

    Ti(xi) = xi x(i+1) xi^-1,
    Ti(x(i+1)) = xi,
    Ti(xj) = xj otherwise.

The actual González-Meneses primary gives the inverse generators in the usual left-composition convention. If rho denotes that standard faithful representation, my right-ordered image U(w) is rho(w^-1). Inversion is a bijection, so U detects exactly the same equalities. My independent calibration checks every two-sided inverse, all four braids and all six commutations, as well as the displayed generator images. This addresses both the sign and order conventions.

Choose a reaching parent for each state during BFS. Every parent on a reaching path to a state in S also lies in S because that path inherits a completion. Starting from six singleton free words, compute the full action U(q) of this parent path. Then independently compare, for every one of the 261,810 edges q--i->q' in S,

    Ti applied by substitution to every word of U(q) == U(q').

All six complete reduced words agree on every edge. U(f) equals the separately computed full action of the displayed z. The computation stored 5,598,030 letters over all state images (maximum single image length 41), and did not load any supplied action stream or checker. Its wall time was about 6.82 seconds in the successful recorded run.

Here is why this proves a universal assertion about all complete words rather than merely checking representative paths. Induct along any 0->f path. At 0 its action is U(0). If its prefix action is U(q), the verified identity on its next edge makes the extended action U(q'). All states along a complete path are in S. At f the action is therefore U(f)=U(z), independently of the path. Faithfulness gives w=z in B6. Positive monoid embedding and the explicit Hurwitz realization of the positive relations then give one strict class.

Equal crossing data alone is insufficient: a1²a2² and a2²a1² have the same state and permutation but unequal F6 images. My computation confirms that their common state lies outside S. This falsifies an overbroad count-only argument while leaving the verified coaccessible cocycle proof intact.

Two injected faults test essential gates: corrupting one state potential fails a literal edge comparison, and skipping one edge fails the complete-edge count. Both fail under normal Python and explicit -O. The successful receipt is never overwritten by these failing runs. These controls are additional evidence about the verifier; the exhaustive path induction is the proof mechanism.

## 7. Conclusion and exact remaining limits

Every input is reduced by the geometric bound and linking necessity to one of the three lengths. The length-20 certificate, length-30 cocycle proof, and length-40 chain argument account for all inputs, with no central unsupported equivalent claim left over. Different lengths remain distinct under both equivalences. The generated-subgroup invariant separates the two strict length-40 classes; explicit conjugation merges them. The original complete theorem survives these checks.

This is a verification conditional on the credited published geometric and braid theorems whose relevant statements and hypotheses were actually read. It does not reprove the deep length theorem or Perron–Vannier theorem, establish the absence of earlier orbit-classification publications, verify other braid ranks, or classify arbitrary conjugate-generator/nonseparating-twist inputs. The reported general Casson result is not used as an unproved substitute: the exact six-strand case has its own complete proof here. Source compiler and optimized-runtime limitations are disclosed in REPORT.md; no manuscript or original programme was repaired.
