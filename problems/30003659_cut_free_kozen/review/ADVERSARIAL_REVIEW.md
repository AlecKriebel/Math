# Independent adversarial review: 30003659

**Verdict: PASS_FULL_SCOPED_FIVE_TURN_PACKET.** No mandatory mathematical correction identified. Original cut-free Kozen completeness remains **unsolved, 5/5**. This independent AI-assisted audit is not human peer review, a general incompleteness proof, or a novelty certification.

## Frozen packet and evidence

Author manifest SHA-256 `b0bf50c813991c638b935bceb51629c952359e4a8f5405fa43dfa3c667edf68d` binds36 files;37 including itself. All hashes and sizes match, as do32 historical manifest entries and13 local source-reading inputs. All six script outputs, including the bounded search, replay byte for byte. The declared author assertion total is1,304 without double-counting imported checker execution. The recovered search control has16 nodes.

A separate standard-library implementation, importing no author module, verifies the36-node original certificate and16-node recovered control, reconstructs the19-formula predecessor invariant, and evaluates4,164 ordinary models through three states. It passes34,205 exact assertions. These finite controls support the written metaproofs; they do not establish syntactic nonderivability by search.

## 1. Exact systems and corrected source dependencies

The complete Afshari–Leigh contribution in [OWR53/2017](https://publications.mfo.de/bitstream/handle/mfo/3617/OWR_2017_53.pdf), report pp24–26, was read; the displayed ordinary/strong-induction page was visually checked. Its target is finite Kozen completeness with cut removed. Its cyclic and stronger-induction discussions are distinct systems.

The [2016 primary preprint](https://oa.tib.eu/renate/bitstreams/50824d0c-d5f5-4a10-8518-36ade258b3e3/download), §2 and Figures1–3 on printed pp8–9, was checked, including the rule images. It specifies closed finite-set sequents, positive formal variables, capture-avoiding substitution and formulas up to alpha-equivalence. Its Koz− includes deep disjunction, both unfolding rules and generalized fixed-point identity. Core C deliberately omits several of these rules, including ν-unfolding. Every core rule used in the certificates is literally present in the fuller2016 system.

The complete2017 conference rule table was not independently recovered. Therefore this review endorses results only for the explicitly pinned systems and their justified containment directions. A negative result for a weaker core alone would not settle the original presentation; the packet does not claim that transfer.

[Kloibhofer2023](https://arxiv.org/abs/2307.06846) gives the exact U,W test sequent and refutes the distinct cyclic Clo system. Its introduction explicitly breaks the older completeness chain and leaves the strengthened well-founded candidate's completeness unknown by that route. [Demystifying μ2025](https://fi.episciences.org/16412/pdf), §5 and §7, acknowledges this error and restores the indicated full completeness with cut. [Bauer–Saurin2025](https://arxiv.org/abs/2506.09791) concerns non-wellfounded cut elimination and identifies the finitary extension as future work. None supplies the missing finite no-cut theorem. The original report's old completeness reduction is therefore correctly excluded as an accepted dependency.

## 2. Turn1: literal finite proofs and the visible cut

The formulas match Kloibhofer's published example up to permitted bound-variable renaming. Its validity and Clo-unprovability are credited rather than claimed anew.

The independent parser checks acyclicity, closedness, exact side contexts, duals, substitutions and every inference. All four component implication roots are cut-free core proofs. The constructor from X,B to A,V(X) uses only the stated modal, Boolean, weakening and ordinary-induction rules. Substitutions in these certificates replace variables by closed formulas, so there is no hidden capture issue. The least-fixed-point reverse implications have their actual syntactic bodies, not semantic placeholders.

The final Φ proof has exactly one explicit cut, on fixed-point-free □p. Its26 ancestral nodes are μ-free; the μ-bearing reverse-implication roots are separate and are not ancestors of Φ. Core membership does not rely on ν-unfolding, generalized identity, deep disjunction or cyclic discharge.

The four separate equivalences do not automatically yield a cut-free proof of their disjunction. The packet correctly displays the missing composition as a cut rather than invoking contextual semantic replacement.

## 3. Turn2: at least two ordinary inductions

Before the first induction on a backward branch, all eligible closed fixed-point principals remain U or W. Their internal disjunction subformulas are open until the relevant outer binder unfolds; unfolding produces only the other listed closed fixed point. Closed sequent syntax and capture-avoiding insertion are essential here. A nonvacuous deep-disjunction instance inside a closed formula would insert closed disjuncts, so it cannot act on those open internal disjunctions. Vacuous contexts are inessential. The fuller2016 rule list is accounted for rather than silently replaced by the core.

The swapped interpretation changes ν to least and μ to greatest simultaneously, retaining duality and monotonicity. Atomic and generalized identities, unfolding and positive deep disjunction remain sound. For the selected one-state self-loop model, modal K also preserves truth directly, because both modalities act as the identity. The endsequent is false for either truth value of p.

If there is only one induction, its principal is U or W. For U choose p=true, and for W choose p=false. The relevant body is identically false for every argument, so that particular induction preserves truth irrespective of its side context. Thus a sole induction cannot prove the false endsequent. This is an at-least-two bound, not an impossibility theorem for multiple interacting inductions.

The four core final contexts correctly include the two retained-principal cases allowed by set sequents. The fuller2016 system can also end with ν-unfolding, so these four cases are not misrepresented as its exhaustive last rules.

## 4. Turn3: failure of one context-permutation strategy

The five-node cut-free proof of νx□x and its weakening is valid with the explicit tautology convention. The alternative one-cut proof reaches the same conclusion. The demanded irredundant last induction with side context {p} instead requires p∨□¬p, which fails in the stated two-state serial frame.

The exact frame characterization is correct: validity of this schema for every atom valuation is equivalent to every edge being a self-loop. The independent checks extend that characterization through three states. Retaining the principal in the side context changes the premise and remains legal; the paper explicitly distinguishes it. The obstruction therefore applies to the specified direct permutation, not every cut-free derivation or every possible proof transformation.

## 5. Turn4: unavoidable μ-bearing intermediates in a cut-free alternative

The19-formula set S is reconstructed independently. Its only fixed-point-free members are p and ¬p. All allowed non-induction predecessors stay in S, including the effective deep-disjunction replacements of the unique possible closed disjunction H by X or Y. There is no closed disjunction inside U or W; generalized fixed-point identity cannot end a μ-free branch. The invariant is exact for this backward fragment, not a depth-limited search approximation.

Choose an ordinary induction nearest the root along one branch of a minimal μ-free proof. Its principal must be U or W and its context consists of S formulas. Any ν-bearing side formula contributes a literal μ binder to the negated context, and the positive principal body actually uses the variable. Hence the premise would contain μ. Semantic simplification is not a syntax rule and cannot erase that occurrence. Retaining U or W in the context is excluded by this same argument, not by an invalid assumption about principal duplication.

The remaining contexts are subsets of {p,¬p}. The six non-tautological cases have valid small countermodels in ordinary semantics and therefore cannot occur as conclusions of closed subproofs. The tautological context can be replaced by atomic identity plus weakening, strictly decreasing the number of inductions while preserving the endsequent and μ-freeness. This contradicts minimality. The restricted theorem follows.

It remains possible that a full cut-free proof introduces μ-bearing invariants. The result does not imply unrestricted cut nonadmissibility, and it is correctly confined to the pinned2016 calculus.

## 6. Turn5: valid premises and honestly bounded failure

The arbitrary-frame fixed-point calculation is sound. Since B=¬A, the formula □A∨◇B is valid. B is an exact fixed point of the operator defining V(A), and every fixed point is contained in B, so V(A)=B. Likewise A is an exact fixed point of F_U and bounds every fixed point from above, giving U=A and W=B. This establishes both minimal-context final premises; the retained-principal premises already contain U∨W. No finite model scan is needed for these universal identities.

Semantic equality of μ-bearing invariants to simpler modal formulas still does not give a cut-free contextual replacement theorem. The packet does not use it as one.

The reproduced bounded attempt explores338 target states,321 μ-bearing, plus15 control states. It allows only the documented focusing choices and per-branch budgets, omits several fuller-system rules, and prunes size/depth. Its no-proof result has no unprovability meaning. The16-node positive-control proof is independently validated syntactically; no certificate of Φ is claimed. The text accurately distinguishes the exact countermodels/metaproofs in earlier turns from this unsuccessful finite search.

## 7. Scope of the PASS

Accept the packet as reviewed partial research with original disposition unsolved5/5. Retain the2017 rule-version gap, explicit system definitions, old Clo-route correction, all known-result credit, and the following limits:

- The explicit final test proof uses a cut
- At least two inductions is a lower bound, not unprovability
- The context-permutation counterexample concerns a prescribed final-rule shape
- The μ-free restriction is on every intermediate sequent, not the full calculus
- Semantic validity of final premises is not cut-free derivability
- The last search is deliberately non-exhaustive

No author-file changes are required by this review. No sixth author search, general completeness/incompleteness claim, formal verification claim or novelty certification is supplied. Source PDFs and raw records remain reading inputs outside this portable review packet.
