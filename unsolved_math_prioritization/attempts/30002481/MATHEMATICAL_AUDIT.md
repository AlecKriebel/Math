# Independent audit of the determinacy model transfers

Problem 30002481 / OWR-12862-007. Audit completed 10 October 2026 UTC.

## Decision and accepted scope

**ACCEPTED AS SCOPED PARTIAL RESULTS. THE ORIGINAL IMPLICATION REMAINS UNRESOLVED BY THIS WORK.**

The report distributed as [MATHEMATICAL_REPORT.md](MATHEMATICAL_REPORT.md) is mathematically sound with its stated conventions and cited premises. This acceptance covers Propositions 1–4, Corollaries 3.1–3.3, and the qualified route conclusions. It does not certify a proof in Z3 of lightface coanalytic determinacy implying a sharp, a countermodel, a complete reconstruction of the source's fine-structural coding, or a current-open/novelty claim.

The distributed report has 18,969 bytes and SHA-256:

`81e9820655338f8aa77f0111c3e0357da1bf2debda2027c2213f3df0605a1d2d`.

This proof-and-audit edition is AI-assisted and unrefereed. Scoped mathematical acceptance is not external human peer review, journal acceptance or formal proof-assistant certification. All mathematical arguments and qualifications are retained; supplemental computation reports and private artifact identities are omitted.

The precise accepted mathematical conclusions are:

1. A recursive initial dummy move exchanges the lightface analytic and coanalytic determinacy assertions over the stated Z3. It does not introduce a real parameter.
2. The all-sets-size-at-most-the-reals axiom prevents the real power set from being a set and prevents a Hartogs ordinal for the reals. In the explicitly stated existing-cardinal convention, the continuum has no cardinal successor in that universe. With the explicit CH bijection, neither the universe's P(omega1) nor its omega2 cardinal is a set.
3. Transitive same-reals models agree on every fixed second-order-arithmetic formula. A transitive Z3 model included in a transitive ZF model with exactly the same reals therefore satisfies the target implication, using the classical ZF theorem as a cited premise. Ordinary ambient H_(c+) models and the stated no-new-real transformations have the claimed consequences.
4. A specified elementary embedding between transitive set models, with its domain externally closed under countable sequences, produces the stated ultrafilter on the domain's subsets of the critical point. It is externally countably complete, normal for the domain's regressive functions, and gives well-founded set ultrapowers formed from domain functions. This is a conditional first-ultrapower result. It does not supply an embedding, a fine-structural premouse, or an iteration strategy.

No outstanding fatal defect was found in the accepted report. Two scope clarifications were requested and are present: the continuum's cardinal-ordinal convention, and the separation of an externally countably closed embedding domain from a countable coded premouse. The distinction between ambient omega2 and an inner model's omega2 was checked explicitly and is preserved.

## Source interpretation

The relevant public source passages were checked independently against text and rendered pages:

- [OWR 02/2014](https://doi.org/10.4171/owr/2014/02), Schindler's joint contribution with Cheng, printed pp. 127–128, PDF pp. 37–38: the exact coanalytic determinacy question and the separation from HP.
- [Cheng–Schindler, arXiv:1503.04000v1](https://arxiv.org/abs/1503.04000v1), pp. 1–2: the set-theoretic theories, the Collection convention, the classical ZF theorem, and the real-coded sharp statement. Page 6 was visually checked for Corollary 3.5 and Theorem 3.6. The relevant text of Theorem 3.2 and its construction was also read.
- [Sami, Analytic determinacy and 0#](https://doi.org/10.4064/fm-160-2-153-159), the retained 1999 paper: sections 1.4, 3.8, and 3.9 were read, and printed p. 158 / PDF p. 6 was visually checked. The final dependence on Silver's implication is explicit.

The original OWR footnote says that Power Set is omitted; it does not itself state the Collection replacement in that footnote. The 2015 Cheng–Schindler paper explicitly states the latter. The accepted report correctly pins its working theory to the 2015 Definition 1.4 and section 2 rather than claiming that the brief OWR footnote contains the additional wording.

The interpretation is set-theoretic Z3 with the real set and a bound on every set, not an unspecified third-order type theory. The determinacy payoffs are parameter-free lightface first-level projective sets. Neither the title of the imported problem nor the availability of real strategy codes licenses upgrading this to the boldface scheme.

The source theorem and its coding convention are mathematical dependencies. This audit verifies their relevant stated scope and their correct use. It does not reprove the classical Martin–Harrington theorem, the equiconsistency construction, or the full fine-structural equivalence behind the coded-sharp sentence.

## Proposition 1 and lightface duality

Fix the convention that player I moves at even-length histories. For payoff A, the new payoff is the complement of A applied to the tail of the run. New player I's first move is ignored by membership; new player II subsequently occupies original player I's turns. Complementing the payoff alone would fail to produce this turn exchange, so the added move is essential.

Both strategy cases were checked separately.

- If new player I wins with strategy tau, its initial move d is tau at the empty history. Original player II uses tau on the prefixed history d followed by the original history. The original history has odd length at precisely the times when the prefixed history has even length. The new run lies in the new payoff, so the original run lies outside A.
- If new player II wins with tau, take d = 0. Original player I uses tau on the corresponding prefixed history. The new initial player-I move is legal regardless of the value 0, because a winning player-II strategy wins against every initial opponent move. The new run lies outside the new payoff, so the original run lies in A.

Tail is recursive, and complementation exchanges the two first-level lightface pointclasses. The natural number d derived from a strategy is used in the translated strategy, not as a new real parameter in a payoff definition. In the second case d is the fixed recursive constant 0. The same construction in the opposite pointclass proves the reverse implication.

Finite positions and strategy graphs have standard countable codes. Separation on the available countable product coding set constructs the transformed graph; no power set above P(omega) is invoked. The proof is accepted as an ordinary internal mathematical derivation over the stated base, not a proof-assistant certificate.

## Proposition 2 and the cardinal restrictions

The proof of the power-set obstruction uses a legitimate Cantor diagonal argument in the weak theory. From a supposed set Q = P(R), the size axiom gives an injection i from Q into R. Its inverse on its range, extended by the empty set elsewhere, is a set function from R onto Q. Collection supplies Replacement where needed, and ordinary finite products exist without the Power Set axiom. Separation on R then constructs the diagonal subset. It belongs to Q by the supposed defining property of Q, giving the contradiction. No hidden collection of all subsets is used before the supposition Q.

The absence of a Hartogs ordinal is immediate from the actual size axiom: every ordinal in the universe is a set and therefore injects into R. This does not say that the ordinal class is a set, or that an ambient larger model has no ordinal above the model's height.

When c is the existing initial ordinal bijective with R, no cardinal ordinal lambda greater than c can exist, since the same injection bound contradicts lambda's initiality. The report explicitly fixes this convention. The acceptance does not identify arbitrary inequivalent formulations of Choice in power-set-free theories or infer a well-order of R from an unspecified weak Choice formulation.

The CH conclusions need no such ambiguity. CH is being used with an actual set bijection from omega1 to R. Images and inverse images along it would turn a supposed set P(omega1) into the forbidden set P(R). The same bijection makes the universe's omega1 the top possible cardinal, excluding its omega2 cardinal.

The CH qualification on P(omega1) must remain. The argument does not exclude that power set in every non-CH model of Z3. The statement about omega2 is also about the relevant universe's cardinal structure. An inner class may have additional cardinals that are small in the surrounding universe. In particular, an ordinal computed as omega2 in L or L[x] need not be an omega2 cardinal of the surrounding model.

The subsequent obstruction to the hull route is accepted only at its stated level: one cannot use a larger ambient cardinal or a strictly larger ambient set whose existence the size axiom precludes. It does not establish that all proper closed hulls are impossible. A continuum-sized hull can still be a proper subset of a continuum-sized structure; its properness simply cannot follow from the prohibited larger-size argument.

## Proposition 3 and the exact meaning of transfer

The hypotheses use actual transitive models M contained in N. Both have the same natural numbers and exactly the same subsets of those naturals. They are not merely externally well-founded presentations with an unspecified identification. An extension of an arbitrary relational presentation would require verifying compatible transitive collapses, or explicitly identifying the full arithmetic reducts, before this proposition could be applied.

For the stated hypotheses, induction on every fixed formula of second-order arithmetic proves agreement:

1. Number terms, arithmetic relations, and membership of a natural number in a shared real have the same interpretation.
2. The number quantifiers use the same domain.
3. The real quantifiers also use the same domain.
4. Boolean combinations and successive quantifiers preserve the equality of truth values.

This is stronger than a low-complexity absoluteness argument within that common reduct. In particular, a Sigma-1-3 existence statement is covered without invoking Shoenfield absoluteness. The result is not an assertion that Sigma-1-3 sentences are absolute between arbitrary nested models with different reals.

Strategies and runs on the natural numbers can be represented by subsets of omega through fixed recursive encodings. Transitive models of the stated theory reconstruct the corresponding functions from these codes. A winning-strategy assertion for any fixed lightface payoff therefore has identical number and real quantifiers in the two models. The same holds for the real-coded analytic witness relation and for each effective payoff index. Thus the determinacy antecedent agrees in both directions.

The coded-sharp predicate requires particular care. Cheng–Schindler require a nontrivial premouse of the displayed L-alpha form with a nonempty measure predicate, and explicitly state a second-order Sigma-1-3 existence formulation. The accepted report denotes that full fixed formulation by Sharp. It does not replace it by the existence of a passive structure, well-founded initial code, well-founded first ultrapower, or arbitrarily long finite iteration. Its transfer proof works for all real quantifier alternations in the fixed predicate, so none of the iterability quantifiers is discarded.

A code here is a real describing a countable presentation, including the relevant infinite relations. It is not a finite description that by itself certifies iterability. Countability and all iteration quantifiers are interpreted in the indicated models. If an object is countable only from a further ambient universe, its enumeration need not be a real of M or N. The proof never imports such an enumeration. Likewise, sameness of the M and N real domains does not mean either contains all reals of a still larger universe.

Apply the classical ZF theorem inside N, using the dummy-move reconciliation if its analytic formulation is chosen. It gives Sharp in N. Because Sharp is the fixed real-coded sentence just described, both its witness real and the full truth of the witness predicate transfer back to M. This establishes the implication in M. It supplies no construction of N from arbitrary M and hence no internal solution over Z3.

Corollary 3.1 is the correct contrapositive: a hypothetical transitive countermodel has no transitive ZF extension with the same reals. A transitive containing extension necessarily contains the old reals, so failure of equality means that an additional real is present. No conclusion about arbitrary nonstandard countermodels follows.

Corollary 3.3 follows from the same formula induction even without a ZF model. A verified no-new-real transformation between the stated transitive models cannot change either sentence's truth. This does not establish that a suggested forcing over the weak base is legitimate, preserves its axioms, or adds no reals. Those are separate hypotheses to check.

## Corollary 3.2 and hereditary-size models

Let c and kappa = c+ be computed in an ambient ZFC universe. Regularity of kappa is being used externally, where full ZFC is available. In particular, a union of fewer than kappa sets of size less than kappa still has size less than kappa. The proof does not pretend to obtain this successor cardinal inside Z3.

For Collection in H_kappa, an input a has fewer than kappa elements. For each member, choose a witnessing object that itself belongs to H_kappa, using ambient Choice and satisfaction in that set structure. There are fewer than kappa witnesses, and regularity bounds the union of their transitive closures below kappa. The set of witnesses therefore belongs to H_kappa. Parameters are included in H_kappa as required; no power set in H_kappa was used. This verifies the stronger Collection scheme, rather than silently checking Replacement only.

Separation produces subsets of existing hereditary-small sets, so their transitive closures remain small. Pairing, Union, Infinity, Extensionality and Foundation are inherited in the usual manner. For Choice, a well-order of a hereditary-small set has hereditary size below kappa, so a witness lies in H_kappa.

The complete ambient real set has hereditary size c and is an element of H_kappa. Every member a of H_kappa has size at most c, and an ambient injection from a into the ambient real set has hereditary size at most c as well. The injection itself is therefore in H_kappa, verifying the size axiom internally. Consequently H_kappa satisfies precisely the relevant Z3 axioms and has the same reals as the ambient universe. The model-transfer argument applies.

The conclusion excludes these hereditary-size candidates, including the same construction inside a transitive ambient ZFC model. It does not exclude all transitive models of Z3. There is no conflict with Proposition 2: kappa is available outside H_kappa, but kappa is not one of its elements.

## Proposition 4 and the conditional ultrapower result

The working universe, transitive set models, and embedding are fixed as in the statement. The embedding is understood as the given set function between the set domains. Its critical point belongs to the domain, is moved upward, and lies above omega. The latter follows because the elementary embedding fixes every finite ordinal and omega.

The Boolean algebra B is a set by Separation on M, even if the full power set of kappa does not exist in the working universe. Its members are exactly the M-subsets of kappa. The ultrafilter U is defined on that algebra only; it is not asserted to decide arbitrary external subsets of kappa.

Preservation of finite intersections and relative complements establishes the ultrafilter laws. Each singleton below kappa is fixed, so no singleton lies in U. For a sequence of members of U supplied by the working universe, the crucial closure assumption puts the entire sequence in M. Its intersection is then an M-set, and application of j commutes with its omega-indexed definition. The critical point belongs to the image of every member and hence to the image of the intersection. The intersection belongs to U and is nonempty. This checks countable completeness in the correct external sense, relative to that working universe.

For normality, a regressive function in M has image value j(f)(kappa) below kappa. That value is fixed by j. The corresponding fiber, which is an M-set, therefore belongs to U. The restriction to regressive functions belonging to M is necessary and remains explicit.

For the ultrapower conclusion, equivalence classes from any set of M-functions can be formed by Separation and Replacement, and finite-intersection closure makes their membership relation well defined. An ill-founded set relation yields a descending omega-sequence using Choice. Choosing representatives gives the sequence of U-large comparison sets in the report. Countable completeness yields one coordinate witnessing an actual infinite descending membership sequence in the working universe, contrary to Foundation.

There is also a direct audit cross-check for this one ultrapower: evaluation [f] mapped to j(f)(kappa) is well defined, injective, and preserves membership in the transitive target N. This confirms the first-ultrapower conclusion independently. It does not supply embeddings for later iterates, and no full iterability conclusion follows from this observation.

The report's warning about countability is important. Since 0 and 1 belong to M, external closure under countable sequences puts every binary sequence of the working universe into M. The domain is not the countable real-coded premouse sought in the target. Passing to a countable hull later would create a new obligation to verify the premouse axioms and all required iteration well-foundedness. The proposition discharges none of those obligations.

The accepted statement does not obtain external closure from the tautological fact that M contains its own sequences. Nor can closure calculated only in L[x] be treated as closure under additional sequences of a larger universe.

## Literature routes and unresolved obligations

Sami's forcing-free presentation does not remove the weak-base issue: its final theorem obtains HP and invokes Silver's implication. This dependence is visible at the cited final step, irrespective of how much of the preceding descriptive-set-theoretic argument can be formalized in a weaker theory.

Cheng–Schindler's Theorem 3.6 is a Z4 result. It first works in L[x] and then selects a level above omega2 and an omega1-sized countably closed elementary hull. Its cardinals and sequence closure must be interpreted in that stated universe. The absence of an ambient omega2 under CH is not by itself a proof that the ordinal omega2 of L[x] is absent. The accepted report explicitly does not draw that inference and does not claim that mere existence of the inner ordinal suffices.

The HP equiconsistency/separation result is also not a determinacy countermodel. The needed direction from HP to the target determinacy assertion has not been established, so the known HP models do not settle the requested implication.

Remaining obligations for a full result include either an extraction of the source's full iterable active premouse in the actual weak base, or a model construction verifying the actual lightface determinacy antecedent and failure of the same full coded-sharp sentence. Existence of a suitable same-reals ZF extension, a sufficiently closed elementary embedding, a well-founded first ultrapower, an HP witness, and a strategy for a payoff with an added real parameter cannot substitute for those obligations.

No current-open certificate is issued. An attempted web reopening of the independently retained public Sami URL returned 403; no further retrieval attempt was made. The already retained paper was sufficient for the stated dependency check.
