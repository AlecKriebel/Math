# Independent review: admissible-structure continuation, 30004676

**Verdict: PASS_PARTIAL_CONTINUATION. The original converse remains unresolved. No mandatory mathematical correction.**

This review covers the frozen recovered turns2–5 in the continuation manifest, in addition to reading the earlier conditional-cover lemma for context. That first lemma has its own separate review; its PASS is not used as a substitute for checking the later deductions. This is adversarial AI review, not human peer review or a novelty certificate.

## 1. Frozen object and source interpretation

All five file hashes in continuation/MANIFEST.json matched at review time. The exact hashes are preserved in review_manifest.json. I read the full four continuation artifacts and BUDGET.json, together with PARTIAL.md and SOURCES.md.

I checked the original primary source, [OWR21/2021, printed pp.1181–1182](https://ems.press/content/serial-article-files/46899), including a rendered view of p.1181. It explicitly works with well-founded KPU structures in finite signatures, gives HF(M) and HYP(M) as admissible examples, distinguishes atomic Delta pullbacks from preservation of all internal Sigma relations, and states the two representation facts used in the continuation. The forward implication is credited prior work; the converse is conjectural.

The artifacts retain an explicit parameter-allowing relational convention. Their deductions are valid under that convention; they do not establish a parameter-free variant. The source's HF examples also fix the relevant KPU convention: one must not silently add an Infinity axiom that would exclude the finite-set HF structures used in turn3.

## 2. Turn2: fixed-map bounded-truth criterion

The equivalence is correct for the **same** surjective map nu. If every Sigma(B) relation pulls back to Sigma(A), both a Delta0 formula and its negation do so, giving complementary Sigma definitions. Conversely, admissibility of B puts each fixed Sigma formula into existential-Delta0 form. A Delta pullback of the matrix is in particular Sigma over A, and existential quantification of representatives preserves Sigma. Surjectivity supplies every B witness. Finite parameter tuples require only separately chosen representatives, not a global choice function or a definable inverse of nu.

There is no circular use of a uniform truth predicate. This is a formula-by-formula reduction. Nor is an internal A-set of representatives silently assumed: the criterion places the bounded-truth preservation itself in the hypothesis. The distinction between a fixed map satisfying the criterion and the existential map promised by C(A) is correctly maintained.

## 3. Turn2: finite complexity bound and presentation invariance

The safe Delta_(q+1) bound is valid in the stated prenex sense. Atomic pullbacks have both Sigma1 and Pi1 definitions. Expanding a bounded B quantifier introduces one ordinary A quantifier and a Delta1 membership guard. Finite Boolean combinations preserve the pair of prenex bounds, and adding one quantifier increases the safe two-sided level by at most one. Unused-quantifier padding is legitimate because the domains are nonempty. This is ordinary finite syntactic manipulation; it does not import higher collection schemes into A.

The bound is intentionally not uniform at level one as formula depth grows, so it cannot be used to infer strong reducibility. That limitation is correctly stated.

Strong reductions compose: the inverse image of a Sigma relation is again Sigma, including any finitely many parameters used in its definition. They also preserve Delta relations by treating a predicate and its complement separately. The directions of the two composed surjections in the proof of C(A) invariance are correct. This shows degree invariance of the closure property, not rigidity of each initial atomic presentation.

## 4. Turn3: exact covers are not necessary

The counterexample to necessity of the cover hypothesis is sound as a consequence of the source's credited graph representation. Choose a well-founded admissible B containing an infinite internal omega, and a graph G with B strongly equivalent to HF(G). Every internal set of HF(G) is externally finite, even when G has infinitely many urelements. The entire urelement domain is not an internal set merely because it is a predicate domain.

For **any** surjection from HF(G) onto B, a representative of B's omega exists. No finite internal set of representatives can map onto its infinite membership fiber. Thus pointwise exact coverage can fail for every presentation, while a strong reduction exists. This is stronger than finding a defect in one map, and it does not contradict the earlier sufficient cover lemma.

The choice of B can be the usual countable admissible constructible level above omega. No claim that ordinal height is invariant under strong reducibility is made; the example correctly shows why that proposed obstruction fails when information may be carried by the urelement structure.

This is not a counterexample to the original conjecture: C(HF(G)) and non-absorption of its jump have not been shown. The text explicitly avoids those unsupported conclusions.

## 5. Turn3: all countable targets reduce to H_(omega1)

This parameter-dependent observation is correct in ambient ZFC. A countable target in a finite relational language has a countable complete elementary diagram after naming its elements. Its code is a real, hence an element of H_(omega1). The domain omega is also an internal parameter. Mapping natural-number elements to their listed target elements and all other arguments to one default element is a surjection.

For each fixed target formula, finite sentence coding followed by lookup in that single diagram parameter yields complementary Sigma definitions on H_(omega1). Repetitions in the listing do not cause a problem because the diagram includes equality and names the actual elements. The same surjection and diagram parameter work for every formula.

This does not extend to arbitrary uncountable targets merely by naming more constants: a complete diagram may cease to belong to the admissible domain. The continuation explicitly preserves that cardinality restriction.

## 6. Turn4: internally coded targets and Delta0 relativization

The proposition is correct when the domain D and the finite list of relation codes actually belong to A. Choose a default element d0 in the nonempty internal D. The map that fixes members of D and sends all other inputs to d0 is bounded definable. Every target quantifier can then be bounded to D; an atomic relation becomes membership in its internal code.

Finite tuple coding causes no hidden unbounded quantification. For a fixed arity, the appropriate finite power of D is an internal A-set by the elementary closure properties of KPU. One may bound tuple witnesses by that finite-power set, or express coded tuple membership with witnesses bounded by the relation code. These are legitimate finite parameters for the formula. Substitution of the default-element map is likewise bounded. Thus all fixed first-order pullbacks, not merely Sigma pullbacks, have Delta0 definitions.

The argument remains valid if D contains A-urelements; equality is actual equality of the represented domain elements and the coded relations carry the target's separate interpretation of membership and sorts. No identification of external subsets with internal sets is made.

## 7. Turn4: H_kappa and the large-target obstruction

Under ambient ZFC, H_kappa is admissible for uncountable regular kappa. In particular, for collection over an internal set of size below kappa, choice selects a family of witnesses of size below kappa and regularity bounds the union of their hereditary sizes below kappa. This is an external proof of the model's collection property, not an assertion that H_kappa contains a global choice selector.

A structure of cardinality below kappa can be represented on an ordinal below kappa, with each finite-arity relation code also of hereditary size below kappa. The preceding proposition applies. Neither CH nor a claimed value of |H_kappa| is needed.

The important failure of the proposed counterexample route is correctly identified: a weak interpretation only bounds the target's size by |H_kappa|, not by a cardinal below kappa. The identity target already rules out silently imposing that stronger restriction. Small elementary substructures do not provide a surjection onto the full target or compatible complete diagrams. No proof of non-fixedness of H_kappa's structural jump is supplied, and none is claimed.

## 8. Turn5: equivalence with local transitivity

The two representation facts R1 and R2 are explicitly present in the primary report and are used as credited inputs. With those facts, the equivalence of C(A) and the displayed local transitivity rule LT is correct.

In the forward direction, C(A) supplies a strong surjection onto the admissible intermediate B. Pulling back both signs of each Delta(B) atomic interpretation predicate gives Delta(A), so composition is weakly interpretable in A.

In the reverse direction, the graph G_B from R2 is weakly interpretable in B by R1. LT moves this graph interpretation to A; R1 then supplies HF(G_B) strongly reducible to A, and composition with the other half of R2 gives B strongly reducible to A. The fact that the last graph need not itself be admissible does not harm LT, whose final object is explicitly an arbitrary finite-signature structure.

Finite-chain collapse uses C(A) repeatedly at the original base A. Each intermediate supplying the domain of the next weak interpretation must be admissible. The induction does not assume C(B) at an intermediate structure.

The proposed first step HF(A-as-structure) is legitimate: the identity weak interpretation of A in itself and R1 give HF(A-as-structure) strongly reducible to A; a strong map also has Delta atomic pullbacks, hence gives the stated weak interpretation. This fills in an elementary implicit step without changing the claim.

## 9. The jump remains a genuine missing step

None of the continuation inserts a universal Sigma predicate with a free negative definition. It does not treat an arbitrary expansion as satisfying expanded-language KPU, or an ill-founded Henkin model as a well-founded admissible. A formal set of all urelements is not supplied merely by naming one node, and taking HYP of a structure does not by itself make its atomic diagram Delta over the original A.

The final chain-to-the-jump construction is correctly presented as an unproved sufficient route obligation. The local transitivity reformulation does not construct that chain. Ordinary oracle-jump strictness is not applied to this different structural degree notion, where fixed-point phenomena are already credited in the source.

## 10. Turn accounting and final scope

The five recovered turns are mathematically substantive: the initial cover theorem; the bounded-truth/presentation results; the finite-cover nonnecessity and countable parameter barrier; the set-code/H_kappa deductions; and the local-transitivity reformulation. They are not five labels attached to source retrieval, administration, repeated checking, or publication work. Some increments are elementary consequences of known results, and no novelty claim is warranted on that basis.

The historical count remains unknown. The recovered five-turn continuation is recorded separately, so it must not be represented as zero earlier attempts or as a known historical total of five.

**The admissible-jump converse is still unproved and unrefuted.** A scoped partial-results publication may accurately carry these deductions and the unsolved verdict. It must not use `claimed_solved`, suggest the jump-compression bridge was established, or turn the smaller-target reductions into a proof of the global property.
