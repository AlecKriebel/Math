# Countryman finite-support line: scoped results and unresolved PFA question

Numeric problem **30003403 / OWR-15216-007**. Five substantive author turns completed. **Original question unresolved; no full solution or counterexample.** This is a frozen author packet awaiting separate independent review, not a claim of human peer review or historical novelty.

## 1. Exact source question and known work

Soukup's Problem 6 in OWR 11/2017, printed p543, asks under PFA whether eta_C is strongly surjective. Fix a Countryman line C, put D=C*+{0}+C, and let L=eta_C be the eventually-zero sequences in D^omega, ordered by the first differing coordinate. Strong surjectivity asks for a monotone epimorphism from L onto every nonempty suborder of L.

Moore's theorem gives embeddability universality under PFA. It does not give the desired epimorphisms. Polymeris–Martinez-Ranero, arXiv:2503.13728v2, Question 6 and concluding Section 9, explicitly retain this problem as open. Their normal-Countryman strong-surjectivity result assumes MA_(aleph1), and their fragmented-target epimorphism lemma has a normal input C fixed for the section. We retain these hypotheses and credit the results. All four primary sources and exact locators are recorded in [source_manifest.json](source_manifest.json) and [SOURCE_SCOPE.md](SOURCE_SCOPE.md).

The prior-work gate found no exact earlier campaign/Alec attempt in the checked records, branch/path history, or all-state live PR search. This is limited provenance evidence, not a novelty certificate.

## 2. Results for arbitrary Countryman input, in ZFC

### A. Structure and normality

[Turn 1](TURN_1.md) proves directly that L is an aleph1-dense, endpoint-free normal Aronszajn line. Every finite-prefix cylinder is convex and isomorphic to L; in particular L is isomorphic to D^n×L with the first coordinate primary.

For a continuous countable exhaustion C_xi of C, the finite-support orders E(C_xi*+{0}+C_xi) form a continuous exhaustion of L. Given x outside one stage, change a coordinate beyond its support and beyond an alphabet symbol missing from that stage. Positive and negative changes remain in the same complementary interval and bracket x. Thus every complementary interval has neither endpoint. The proof does not assume that the input C itself is normal.

The published stationary-endpoint necessary obstruction is consequently vacuous for this domain. Normality alone is insufficient: the source's normal C0+C0* counterexample to strong surjectivity is credited and explained. That counterexample is not eta_C.

### B. The exact section criterion

[Turn 2](TURN_2.md) proves the elementary criterion: a specified nonempty B⊆A is the range of a monotone retraction exactly when, at every x outside B, the B-points below x have a greatest element or the B-points above x have a least element. Empty sides have no such extrema.

An abstract epimorphism A->B exists exactly when B has some embedded copy in A satisfying that criterion. A zero-prefix cylinder in L fails as a fixed retraction range, but is an isomorphic quotient of L. Hence one failed chosen copy cannot refute strong surjectivity.

### C. Every nonempty countable order is a quotient

[Turn 3](TURN_3.md) constructs a suitable rational section, rather than merely embeds Q. Inside each bounded interval choose a cylinder and its finite two-letter search-tree nodes, terminating every word with zeros. Add the interval's two endpoints. Any ambient point follows a branch only finitely long, since both branch symbols are nonzero and the point is eventually zero. At the first exit, a node or ancestor bound supplies the required adjacent section point. Hence the interval retracts onto a section of type 1+Q+1.

Glue these retractions along a coinitial/cofinal sequence indexed by Z. The resulting global section has type Q. Thus L has a monotone epimorphism onto Q. For any nonempty countable K, the countable dense endpoint-free order K×Q is isomorphic to Q; its first-coordinate projection maps onto K. Composition covers every countable K, including orders with endpoints or adjacent pairs. This result is ZFC for arbitrary C; no normal-input or PFA assumption is hidden here.

### D. Finite-prefix quotient lifting

[Turn 4](TURN_4.md) states a conditional closure theorem. If D^n has an epimorphism onto I and each A_i is a quotient of L, then L has an epimorphism onto the ordered sum of the A_i. Factor L as D^n×L, group the convex fibers J_i of the index map, and use the credited short-product epimorphism J_i×L->L before the individual target maps. The second-coordinate projection is generally not monotone and is not used.

Consequently L maps onto any nonempty finite ordered sum of orders already in its quotient class. Examples include L+L and 1+L+1. These are genuine nonfragmented uncountable target types, because they contain L. Under PFA they embed into L; the displayed quotient constructions need no forcing axiom.

## 3. Additional closure with normal input and a stated axiom

If C is normal and MA_(aleph1) holds, the source maps D^2 onto C and C*, whose strong surjectivity supplies all countable index orders and all suborders of C or C*. The lifting rule therefore closes the quotient class of L under corresponding countable and Countryman-indexed sums. In particular K×L, C×L, and C*×L are quotients for every nonempty countable K. Under PFA, the credited fragmented-target theorem supplies additional summands.

These conclusions are not silently transferred to arbitrary nonnormal C. They do not imply that an arbitrary Aronszajn target admits such a well-founded sum decomposition. Pointwise finite support does not make the recursion decrease: every first-coordinate fiber of L is L again. Nor has absorption of L×L into the required quotient class been proved.

## 4. Final PFA route and its exact gap

[Turn 5](TURN_5.md) defines the forcing of finite monotone partial maps L->A for arbitrary nonempty A⊆L. The domain and range requirements are dense; a filter meeting their at most aleph1 many dense sets gives a monotone surjection. Properness of this poset would therefore suffice under PFA.

Properness is not proved. The poset fails ccc even for A=L: mirrored Countryman source/target assignments give an uncountable antichain. This does not refute properness or the target; the identity quotient exists in that example.

An exact irrational-cut construction also shows that an onto partial map with coinitial/cofinal domain and endpoint-free fibers need not extend across a new domain interval, even when both whole domain and target have type Q. This only refutes arbitrary extension of the chosen map. It supplies no intrinsic obstruction excluding all quotient maps.

**Remaining full gap:** construct a quotient-compatible section for every uncountable nonfragmented suborder under PFA, with all input hypotheses respected, or exhibit a PFA-compatible target for which every such section fails. Neither has been obtained. A properness proof, universal good-section theorem, or decreasing decomposition rank is still missing.

## 5. Checks and disposition

Five standalone exact diagnostic scripts accompany the five proof turns. Their receipts contain 157,360; 9,738; 1,887,478; 142,914; and 12,242 checks respectively. These finite checks validate the specified formulas and countercontrols; they do not prove uncountable normality, forcing properness, or any universal epimorphism claim. The infinite arguments and credited inputs are stated separately above and in the turn files.

The exact queue ledger records five substantive attempts and the automatic exhausted state. Source triage, checkpoint work, and independent review are not extra proof attempts. Estimated completion toward the full target: 30%; this is only a research estimate.

**Proposed final original status: unsolved, 5/5.** A separate adversarial order-theoretic review must inspect the complete packet before a PR. No additional search turn is claimed.
