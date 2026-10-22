# Independent audit: perfect-product Borel smoothness

## Verdict and binding

**ACCEPT AS AN UNSOLVED, FIVE-APPROACH RESTRICTED-RESULTS ATTEMPT, WITH THE EXPLICIT CANTOR-EXTRACTION CLARIFICATION BELOW.** No unrestricted solution or qualifying counterexample is established. The five approaches count as five distinct mathematical routes, so the defensible research disposition is `unsolved`, 5/5. This is not a novelty, priority, or present global-openness certification.

The audited submission is the exact nine-file packet bound in `BINDINGS.json`. Its manifest SHA-256 is `a387cbefe3b91492f1948ff6cb20b912b0ebe21a924a19a9b371ca0e428f31d5`. Original bytes were preserved. This audit is separate; its clarification must accompany any release claiming the preliminary construction has been fully checked. No remote write was performed.

Independent review covered every retained infinite proof. The executable controls check byte identity and small explicit models only. Neither the submitted 47,729 assertions and seven mutation controls nor the independent controls are a proof of category arguments, perfectness, smoothness, or the infinite fusion.

## Exact target and source scope

The primary statement was independently read and visually inspected on printed page 100, PDF page 16, of *Set Theory*, Oberwolfach Report 02/2011. Its location is Zapletal's contribution on joint work with Kanovei and Sabok. The formal normalization used here is:

For a Borel equivalence relation E on the countable product of real lines, suppose there are a Polish group G, a Borel action of G on a standard Borel space Y, and a Borel map f such that x E y if and only if f(x) and f(y) belong to the same G-orbit. Must there exist, for every coordinate n, a nonempty closed real set P_n without isolated points such that E on the whole product of the P_n has a Borel complete invariant in Cantor space?

The printed question is concise; the Borel-reduction and Polish-action conventions above are its descriptive-set-theoretic interpretation, rather than extra words claimed to be printed. Nonempty factors are essential: permitting empty factors trivializes the question. The adjacent discussion of E1 and a countable product of Sacks forcings confirms the countably infinite rectangular scope. Smoothness means Borel classification, with no differentiability meaning. A Borel reduction need not be injective. The target orbit graph need not itself be Borel.

The live exact-ID site remained inaccessible (web-reader failure and independently observed HTTP 403). Its current statement has not been inspected. The supplied rank 705, ID 30001678, and OWR-4792-006 are locator bindings, not independently verified byte identity with that inaccessible page. Raw AI corpora were not inspected. Source PDFs, extracts, rendered pages, responses, and raw records are excluded from this audit's safe directory.

## Required proof-precision clarification

**Location:** `PROOF.md`, section 0, “Elementary Cantor extraction”, the sentence beginning “To construct one, choose a bounded closed interval”.

**Controlling replacement:**

“Let U be the specified nonempty relatively open subset of A. Write U=A intersect O, with O open in the real line. Choose a point a in U and a bounded closed interval I such that a lies in the interior of I and I is contained in O. Begin the interval construction with I.”

Retain the subsequent requirements that each child interval lie in its parent's interior, have interior meeting A, be disjoint from its sibling, and have diameter tending to zero.

**Reason:** Merely requiring the initial interval's interior to meet U does not, by itself, keep the resulting Cantor set in U. The stronger root choice is always available because O is open. This is a missing explicitly stated containment invariant, not a false extraction theorem.

**Full downstream recheck:** Every descendant interval is contained in I and therefore in O. Its interior meets A and contains two distinct points of A: A has no isolated points, and its intersection with any such open interior also has no isolated points. Small disjoint children with closure inside the parent can therefore be selected. Along any branch, nested compact intervals with shrinking diameters determine one point. Choosing points of A in the branch intervals proves that limit belongs to A, since A is closed. It also belongs to I, hence to U. Disjoint sibling intervals separate distinct branches; shrinking diameters give continuity, compactness gives the embedding property, and continued splitting gives no isolated points.

Proposition 3 first chooses a relatively open portion U_n of A_n of diameter at most delta_n. Applying the clarified construction to U_n gives P_n contained in U_n, so every pair in P_n has distance at most delta_n. All differences in the full countable product therefore lie in the hypothesized H-box. Corollary 3.1 inherits this conclusion unchanged. Proposition 2, Proposition 4's optional Cantor-coordinate strengthening, and Proposition 5 also use extraction; their whole-factor extractions were already sufficient, and the clarification preserves them. No other proof requires a new hypothesis or a changed conclusion. `APPROACH_LOG.md` routes 2, 3, and 5 remain correct with this explicit preliminary invariant.

## Proof-by-proof independent review

### Proposition 1: closed-orbit classification

For a continuous action, the preimage in G of an open set under g mapped to g.y is open. Therefore a nonempty such preimage meets a fixed countable dense subset of G. This justifies replacing an existential quantifier over G by countably many fixed group elements. Each code bit is Borel, since its fiber is a countable union of open subsets of Y. The code records orbit closures, and a countable base distinguishes distinct closed sets. When every orbit is closed, equality of codes is exactly orbit equivalence. Composition with any Borel reduction preserves the classifier property.

For compact G, each orbit is the continuous image of a compact space and hence closed in Hausdorff Y. Compactness of Y is unnecessary. The proof does not cover arbitrary Borel actions by assuming they are already continuous in an unmentioned topology. It states the continuous-action hypothesis where needed.

The finite-flip action has countable dense orbits and Borel E0 graph. Its closure code is constant, while E0 is nonsmooth by Lemma 4.1. This validly defeats the proposed closure-separation method. It does not refute the target perfect-product assertion. **Accepted.**

### Lemmas 2.1 and 2.2: countable sections and perfect antichains

In Lemma 2.1, a nonmeager Borel subset of C squared is comeager in some nonempty open rectangle. Its complement there is covered by countably many relatively closed nowhere dense sets. For each dense open complement D and each basic open W in the second coordinate, the first-coordinate projection of D intersect (U times W) is open dense in U. One x in the countable intersection has every D-section dense open. Baire's theorem then makes A_x comeager in V, contradicting its countability in a nonempty perfect Baire space. All topological uses are relative to open Polish subspaces. Borelness is sufficient through the Baire property; no uniform enumeration of the countable sections is needed.

In Lemma 2.2, at each finite level every ordered pair of distinct leaves concerns two different clopen sets. The complement of a finite union of closed nowhere dense sets contains a subrectangle of their product. Successively shrinking the two selected leaves cannot destroy a previously obtained exclusion. Every leaf stays nonempty, every sibling pair remains disjoint, and diameters still tend to zero. A distinct pair of limiting branches eventually lies in different leaves at all later levels, so each indexed forbidden closed set is avoided. The proof requires no avoidance of the diagonal for equal points. **Both accepted.**

### Proposition 2: coordinatewise countable-action antichains

Restriction of E_n to a Cantor subset is Borel with countable sections. The two lemmas provide a Cantor antichain separately in every coordinate. Countably many choices are available in ZFC. Consequently coordinatewise equivalence becomes equality on the entire product, with a continuous Cantor code obtained by interleaving the homeomorphism bits through a fixed bijection of omega squared with omega.

A countable discrete group is Polish; their countable product is Polish. The stated continuous coordinate actions induce a continuous product action. Orbit witnesses can be chosen coordinatewise in ZFC. The conclusion concerns native coordinate structure, not an arbitrary pullback through f. The duplication-map obstruction is exact: a product lying in y_0=y_1 would force both first factors to be the same singleton, and disjoint first factors produce an empty preimage. **Accepted.**

### Proposition 3 and Corollary 3.1: translation boxes

With the clarified extraction invariant, the proof of the box criterion is pointwise in every coordinate and then uses membership of the full box in H. It neither replaces the product topology by the box topology nor infers membership from all finite truncations alone.

For weighted l^p, positive weights and delta_n=(2^(-n-1)/w_n)^(1/p) give the exact infinite budget sum w_n delta_n^p=1. Domination by delta makes every box point a member of the group. The weight-rescaling map gives an isometry with l^p for real p at least 1; coordinate evaluation is continuous even for arbitrary positive weights. The addition action on the product is continuous. For c_0, delta_n tending to zero gives domination directly. Membership in each group is Borel by the stated countable partial-sum or eventual-smallness formulas. These are admissible Borel orbit relations.

The rational-coordinate translation group, with each rational factor discrete, is Polish and acts continuously. Each orbit has countable coordinate projections, so it cannot contain a product of nonempty perfect sets. Proposition 2 nevertheless makes its restriction equality on a suitable product. Thus the failure of a one-class construction is not a failure of smoothness. The finite-support subgroup fails the positive-box criterion and is not silently endowed with an admissible Polish topology. **Accepted with the preliminary clarification.**

### Lemma 4.1 and Proposition 4: E0 and E1

An invariant Borel subset of binary Cantor space is meager or comeager: from comeagerness in one cylinder, finite flips give comeagerness in every cylinder of that fixed finite length. A hypothetical Borel classifier then has one comeager fiber, by intersecting the comeager bit fibers. That fiber cannot fit in a countable E0 class. This argument is about restriction of a Borel classifier, with no measure-theoretic or cardinal assumptions.

Every factor P_n supplies two distinct points. The continuous coordinate injection from binary Cantor space transforms finite disagreement of input bits exactly into finite disagreement of real coordinates. Thus E0 reduces to E1 on every full nonempty perfect product. Choosing coordinatewise Cantor embeddings gives the stronger full Cantor-coordinate E1 embedding as stated.

The diagonal is a compact perfect set with equality restriction, but it is not a product of perfect factors. The closed tail relations F_N increase to E1, so closedness and smoothness do not survive that increasing union. The sequence of finite initial blocks of ones gives a genuine product-topology limit point outside the E1 graph. Finite-coordinate testing collapses the distinction being studied. **Accepted.**

### Imported Kechris-Louveau exclusion

The published Theorem 4.2 was independently read from the retained PDF, freshly rendered, and visually checked at printed page 239/PDF page 26. Its statement covers a Borel action of any Polish group on a standard Borel space, with no assumption that the entire orbit relation is Borel. The preceding paragraph explicitly distinguishes the additional generality from Theorem 4.1. Its nonreducibility conclusion excludes a Borel reduction of Cantor-coordinate E1 to that orbit relation. Restricting a putative real-coordinate reduction along coordinatewise Cantor embeddings would contradict it.

The displayed proof invokes additional regularity in an auxiliary metamathematical argument and explains why the conclusion is a ZFC theorem. It is incorrect to transfer its temporary MA plus not-CH assumption to the theorem's hypotheses. The theorem and its scope are verified; its deeper cited dependencies were not independently reconstructed. This imported dependency is transparently isolated from the elementary retained proofs. **Correctly used; E1 is not a qualifying counterexample.**

### Lemma 5.1: full countable-coordinate fusion

The invariant at the beginning of each stage consists of finitely many active coordinates, finitely many nonempty clopen leaves in each, and one reservoir in each inactive coordinate. Only finitely many reservoirs have been restricted at any finite stage. Hence every selected-leaf cylinder is open in the original product, even after earlier stages.

At stage m, coordinate m becomes active; exactly coordinates 0 through m need splitting. Every existing leaf in those coordinates gets two disjoint nonempty children. Children can be taken small enough for the metric diameter requirement without losing perfectness, because a nonempty clopen subset of Cantor space is itself a Cantor space. There are finitely many active-leaf combinations, although their number can grow rapidly.

For one such combination, density and openness of O_m give a basic subrectangle in its current cylinder. Replace the selected leaf in each mentioned active coordinate by a nonempty clopen subset of that subrectangle, and shrink each mentioned inactive reservoir similarly. Basic product neighborhoods mention only finitely many coordinates. No unselected leaf is deleted. Every unprocessed combination is still an open nonempty cylinder; earlier processed combinations only shrink and therefore retain their inclusions in O_m. After all combinations have been processed, their finite union covers the entire current product restriction, proving its inclusion in O_m uniformly for all remaining branches.

Fix a coordinate n. Before activation, it may have a repeatedly restricted reservoir; there are only finitely many such stages. From stage n onward, every leaf splits at every stage and none is dropped. Each binary branch has nested nonempty compact clopen sets, shrinking to one point; disjoint children make branches distinct. The coordinate limit is a compact perfect Cantor subset, not a singleton and not merely a possibly empty intersection of unrelated products. Every limiting coordinate set lies in every earlier coordinate restriction. Consequently the whole limiting product lies in every O_m. Countability is used both in the schedule and in the Baire requirements. **Accepted; no unfair scheduling or hidden coordinate collapse was found.**

### Lemma 5.2: Borel-to-continuous on a full product

A countable base in the target allows all inverse images to be approximated by open sets simultaneously modulo one meager exceptional set. On its complement, these inverse images are relatively open, which is exactly continuity of the restricted map. This does not assert that the original map is continuous at every point in that set with respect to the original unrestricted domain. Lemma 5.1 then finds an entire Cantor product inside the complement. Thus continuity holds for the map on the whole selected product, not merely on separate sections or on an arbitrary perfect set. **Accepted.**

### Lemma 5.3: compact-class classification and uniformity

Closedness of E in K squared and compactness of K make the displayed set of pairs with d(a_i,z) at most r compact. Its projection is therefore closed. This proves Borel measurability of every class-distance function uniformly in x, without selecting a representative or assuming an unproved measurability of x mapped to its class. Rational threshold bits recover every distance value. Agreement at a fixed countable dense set extends to all of K by the 1-Lipschitz property of distances to closed sets; equality of zero sets gives equality of classes. Reflexivity and the disjoint-or-equal property of equivalence classes finish the reduction.

The resulting distance-code functions need not themselves be continuous. For example, on K={0,2} union {1/n:n at least 1}, collapse {0,2} to one class and leave all other points singleton. The graph is closed, but distance from 2 to the class of 1/n tends to 2 while distance from 2 to the class of 0 equals 0. The proof only requires Borel measurability and does not make the stronger false assertion. Compactness, closed graph, and the common countable dense sequence provide the required uniformity. **Accepted.**

### Proposition 5: exact existential closed-restriction equivalence

From a smooth restriction on a full product, choose coordinatewise Cantor subsets. The Borel classifier remains Borel on the compact product. Lemma 5.2 makes it continuous on a further full Cantor product. The graph of E there is the inverse image of the closed diagonal under the continuous product classifier, hence closed relative to the square of that product.

Conversely, a countable product of compact metrizable Cantor factors is compact metrizable. Lemma 5.3 supplies a Borel classifier for a closed equivalence graph on it. All selected factors remain admissible nonempty perfect real sets. These are existential statements about some restrictions, not claims of global closedness or a continuous classifier before thinning. **Accepted.**

The reformulation does not prove its own existence clause. Applying continuous reading to the given orbit reduction makes the map continuous but leaves its target orbit graph potentially nonclosed. Applying it to an already available classifier presupposes smoothness. No circular inference is made in the retained packet.

## Literature boundaries and a source-only defect

The 2013 KSZ published preview's Theorem 1.26 identifies restricted positive classes: classification by countable structures and reducibility to equality modulo an analytic P-ideal. It does not assert a theorem for arbitrary Polish-group orbit reducibility. The complete published chapter proofs were not inspected. The independently downloaded earlier draft identifies the historical question in section 3.8, but contains incomplete proof placeholders and is not accepted as a completed argument or present status certificate.

Kanovei-Lyubetsky's arXiv preprint Theorem 2.1 assumes the two input equivalence relations are already smooth. The arXiv metadata and PDF date differ as recorded in `SOURCE_CHECKS.json`; no unsupported reconciliation is imposed. The later related DOI is not treated as proof that the preprint and published E0-large-product text are identical. No full publisher text was obtained.

**Source-only caveat, not a packet proof dependency:** the preprint's Example 2.2 overstates its claim when it denies ordinary Borel bireducibility with all coordinate-equality normal forms. On a Cantor product, its smooth relation is in fact Borel bireducible with equality in coordinate zero. One direction fixes all other coordinates. For the reverse direction, take its Borel classifier in Cantor space and encode that value into P_0 through a homeomorphism; fill other coordinates with fixed points. Thus its example can obstruct literal equality with a fixed coordinate normal form without establishing the stronger claimed non-bireducibility. The packet did not import that parenthetical, so the audit verdict and all five retained routes are unaffected. It must not be used in a later proof.

Current bounded searches and these inspected sources did not establish an unrestricted resolution. The packet correctly avoids treating search absence, a historical question, upload/crawl dates, or repository lookup failures as a theorem about current global openness. This audit does not independently certify all historical repository-search assertions in `SOURCE_STATUS.md`; they remain explicitly bounded reported observations and are not mathematical dependencies.

## Release boundary and conclusion

Only authored audit analysis, public-source bibliographic and verification metadata, independent control code/results, and integrity bindings are in the safe audit. It contains no source PDF, source extract, image, raw corpus or catalog record, raw search response, private correspondence, or private coordination record.

The submission's five distinct routes are closure separation, coordinate antichains, translation boxes, tail/limit obstruction analysis, and closed-graph rectangular fusion. Each has a substantive retained result and a specific unclosed gap to the unrestricted target. Their combined result supports `unsolved` 5/5 only. Any release should retain that scope, the exact-site/raw-corpus inspection limits, the imported KL dependency, and the controlling containment clarification.
