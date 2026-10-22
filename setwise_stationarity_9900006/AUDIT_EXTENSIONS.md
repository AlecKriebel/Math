# Independent audit extension: subsequence random-time coupling

Date: 2026-10-20. Target: Thorisson Problem 3.2, ID 9900006.

## Verdict and disposition

**PASS for the mathematical equivalence in Attempt 3 and the obstructions in Attempts 4–5.** The theorem works on arbitrary measurable spaces, retains one original orbit, and does not require a measurable diagonal. An explicit product-space realization below removes a possible ambiguity in the abbreviated kernel construction.

**Retain the partial/unresolved disposition for the named problem, with an important qualification:** Attempt 3 really is a necessary-and-sufficient coupling characterization of the stated full-path setwise convergence, if auxiliary stationary-law copies and a separate construction for each deterministic subsequence are allowed. It must not be dismissed as merely a finite-partition observation or a theorem confined to standard Borel spaces. The source does not expressly forbid this broad format. What has not been established is that this format resolves the intended problem, that it is novel, or that it supplies the stronger characterization using one jointly constructed original process and one stationary process.

Reviewed: Attempts 1–5, the earlier `AUDIT.md`, `COUPLING_CRITERIA.md`, the source-verification record summarized in SOURCES.md, and the original preprint's Section 3. The detailed new audit concerns Attempts 3–5; it does not replace the earlier independent audit of the rank-one lemma.

## 1. Source scope: do not silently strengthen or weaken the question

Thorisson's Problem 3.2 asks, “What then is the coupling characterization of the convergence (3.2)?” The surrounding results concern exact and shift couplings of two processes. However, Problem 3.2 itself does not specify the admissible number of auxiliary copies. The subsequent Problem 3.3 expressly asks for a two-process rather than whole-family construction for weak convergence. Thus reading an explicit single-pair requirement into Problem 3.2 would overstate the text. [Original preprint, Section 3, pp. 3–4](https://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf).

Two different assessments are therefore appropriate:

1. **Broad literal characterization:** proved. The equivalence in Attempt 3 characterizes exactly the convergence in question on the full measurable path space.
2. **Unqualified resolution of the named problem:** not established. The intended coupling format and prior literature have not been settled, and the construction does not provide a single stationary orbit supplying every comparison.

The conservative partial status is an acceptance/scope judgment, not evidence that the theorem is false or that the source explicitly rules out its format. A defensible summary is:

> A general auxiliary-copy random-time coupling characterization is proved, together with obstructions to natural simplifications. Its status as the intended or novel resolution of Thorisson Problem 3.2 remains unverified; the stronger two-process orbit construction remains unresolved.

In particular, the earlier audit's statement that no general characterization follows from the first two attempts should not be carried forward as though Attempt 3 had never been supplied.

## 2. Attempt 3: setwise convergence and convexification

### 2.1 Dominating measure and weak L1 convergence: PASS

The measure

    λ = ν + Σ_{n≥0} 2^{-n-1} μ_n

is finite, with mass two, and dominates all the measures in the theorem. Radon–Nikodym densities therefore exist without countable generation, separability, topology, or regular conditional distributions.

For a bounded measurable real function h, uniform simple-function approximation gives

    ∫ h(f_n−g) dλ → 0.

The error bound uses ∫|f_n−g| dλ ≤ 2, uniformly in n. Since λ is finite, every continuous linear functional on L1(λ) is represented by an L∞(λ) class; each such class has an essentially bounded measurable representative, and modification on a null set gives a bounded representative. Thus the displayed convergence is genuinely weak convergence in L1, not merely convergence against a smaller, countable test class.

For every subsequence and every one of its tails, weak convergence places g in the weak closure of that tail's convex hull. Hahn–Banach separation identifies weak and norm closures of convex subsets of a Banach space. Hence finite convex combinations from that tail approximate g in L1 norm. Taking the norm error below 2ε gives supremum-event TV error below ε. This proves (A) implies (B) with the stated normalization.

This is the classical Mazur convexification argument. It does not require any of the separable-measure-algebra approximation used in `COUPLING_CRITERIA.md`. There is no circular appeal to the desired coupling result.

### 2.2 Index convention

The subsequences must consist of **nonnegative** integers:

    0 ≤ n_1 < n_2 < ...

This is the natural time convention throughout the source and attempts. Saying merely “integer sequence” is an avoidable notational ambiguity when θ need not be invertible. It should not be read as asserting a theorem about undefined negative iterates.

## 3. Attempt 3: full construction without a measurable diagonal

### 3.1 The common part and residual measure: PASS

Fix a subsequence and the finite probability vectors from (B), and set

    q_j = Σ_k a_{j,k} μ_{n_k},
    δ_j = ||q_j−ν||_TV < 2^{-j},
    r_j = q_j ∧ ν.

The common part is defined by the minimum of the two Radon–Nikodym densities with respect to q_j+ν. It has mass 1−δ_j. Its density b_j=dr_j/dq_j can be chosen everywhere measurable with values in [0,1], by changing a null set if necessary. For δ_j>0 set β_j=(ν−r_j)/δ_j. For δ_j=0 take β_j=ν.

These are ordinary finite-measure constructions on any measurable space.

### 3.2 Explicit implementation of the success branch

Use a countable product probability space carrying mutually independent families:

- X with law μ;
- K_j with probability vector (a_{j,k}) on its finite support;
- U_j uniformly distributed on [0,1];
- Z_j with law β_j.

Countable product measures of probability spaces exist for arbitrary measurable factors. In particular, the Z_j are coordinate projections on their own factors; there is no claim that an arbitrary S-valued law can be generated by a measurable function of a uniform random variable.

Define

    V_j = θ^{n_{K_j}}X,
    H_j = {U_j ≤ b_j(V_j)},
    Y_j = V_j on H_j, and Y_j = Z_j on H_j^c.

The map V_j is measurable because K_j takes finitely many values and every corresponding iterate of θ is measurable. The event H_j is measurable because b_j(V_j) is a measurable real variable. For every A∈Σ,

    {Y_j∈A}
      = (H_j ∩ {V_j∈A}) ∪ (H_j^c ∩ {Z_j∈A}),

so Y_j is measurable. The equality Y_j=V_j holds at **every point** of H_j by definition.

Independence gives Law(V_j)=q_j and

    P(H_j^c) = ∫(1−b_j) dq_j = δ_j,
    P(Y_j∈A) = ∫_A b_j dq_j + δ_j β_j(A) = ν(A).

The entire sequence (K_j) is independent of X. The construction even makes the K_j mutually independent, although the theorem does not need that additional property.

This explicit realization is the safe meaning of the kernel description in Attempt 3. Merely writing a Dirac-success kernel on a canonical product space and then asserting support on its diagonal would not by itself justify a pointwise statement when that diagonal is nonmeasurable. Defining the output by cases, as above, avoids that issue altogether. The theorem is valid; this explicit realization has been incorporated into the publication version of Attempt 3.

Finally,

    E = ⋃_{J≥1} ⋂_{j≥J} H_j

is measurable and has probability one, because the probability of any failure at or after J is at most Σ_{j≥J}δ_j→0. At every point of E, equality holds for all sufficiently large j. No assertion about measurability of the entire equality event is needed, and no independence of the H_j is used.

### 3.3 What independence does and does not mean

The theorem requires sampling times to be independent of the whole original X. It does **not** require K_j to be independent of Y_j, nor the Y_j to be mutually independent. Those stronger claims would not follow from the construction.

The residual samples Z_j are independent auxiliaries, but the final Y_j are not those samples alone. They inherit dependence on X and the indices through the success branch. This distinction is essential to preserving one original orbit.

## 4. Attempt 3: converse and quantifier audit

Suppose setwise convergence fails. There is one fixed A and an infinite subsequence on which μ_{n_k}(A) stays at least η above ν(A), or stays at least η below it. Use that particular subsequence in (C).

Independence of each K_j from X gives the mixture identity

    P(V_j∈A) = Σ_k P(K_j=k) μ_{n_k}(A).

It therefore stays on the same side of ν(A), at distance at least η. Equality on H_j gives, for this same A,

    |P(V_j∈A)−ν(A)| ≤ P(H_j^c) ≤ 2^{-j},

a contradiction. The mismatch of the two indicator variables is measurable even when equality of the S-valued variables is not.

The quantifiers are exactly:

    for each deterministic subsequence,
    there exists one common probability space and all its variables,
    with success controlling whole S-valued equality for all j.

The construction and weights may change with the subsequence. They do not change with a test event. There is no selection measurable in the space of all subsequences, no one coupling simultaneously serving every subsequence, and no such requirement is needed.

Stationarity of ν is used to interpret each Y_j as a stationary-law path when S is path space. The analytic and measure-construction equivalence itself does not use stationarity. This explains both its generality and its origin as a general setwise-convergence reformulation rather than a specifically dynamical rigidity theorem.

## 5. Attempt 4: fixed-target and fixed-pair obstructions

### 5.1 A common unshifted target: PASS

For fair iid Bernoulli X and a fixed j, choose l larger than the maximum support point of K_j. Since K_l≥l, the two sampled indices are surely distinct. The whole index sequence is independent of X, so the two sampled bits disagree with probability 1/2.

This calculation does not require any regular conditional distribution: sum directly over the finitely many possibilities for (K_j,K_l); each distinct-index pair has disagreement probability 1/2. If both bits converged in probability to one Y_0, their mutual disagreement probability would tend to zero by the union bound, a contradiction.

The proof needs independence of the pair of indices from X, which is supplied by independence of the entire index sequence. It does not require K_j and K_l to be mutually independent.

### 5.2 One pair fixed before all subsequences: PASS, with the exact independence convention

For one fixed coupling π, the nonnegative errors e_n(A) tend to zero for every A if and only if every subsequence admits the stated tail convex averages tending to zero for every A. If e_n(A) fails to tend to zero, a subsequence bounded below by a positive constant cannot be repaired by any convex averages. The forward implication uses point masses.

When this deterministic-weight assertion is restated as randomized simultaneous sampling of the two members of π, the sampling time must be independent of the **pair (X,X′)** to identify the randomized mismatch with the convex average of e_n(A). Independence from X alone would not justify that identity. This is the natural meaning of the independent-randomization sentence in Attempt 4; it is stronger than the time-independence requirement in Attempt 3.

The result inherits the separately audited SC obstruction. It does not rule out choosing a new pair separately for each subsequence. It also does not rule out other two-process formulations, unequal random shifts, or appropriately state-dependent sampling. No such general impossibility claim should be inferred.

## 6. Attempt 5: necessity and support cost

### 6.1 Dropping universal subsequences: PASS

The alternating deterministic orbit has a stationary two-point average, while its unaveraged shifted laws fail setwise convergence on the first-coordinate event. A fair choice between consecutive times gives that stationary law exactly. An even consecutive uniform window does the same. Along the subsequence of one parity, however, every convex combination is the same nonstationary point mass.

This is a valid full-path counterexample to using only the original time sequence, even with arbitrarily late independent times and zero coupling failure. It shows that deleting the universal subsequence condition from this particular criterion fails. It does not prove that every conceivable characterization must use that quantifier.

### 6.2 Uniformly bounded sampling support: PASS

The orbit map Φ has a measurable left inverse given by first-state projection. Therefore pushforward by Φ preserves TV exactly: contraction gives one direction, and first-state events give the reverse. The density calculation is consequently a full-path calculation.

For a mixture at m distinct times, after merging any repeated indices, the density difference is W=Σ a_i ε_i with independent symmetric signs. The checked identities are

    E W² = v = Σ a_i²,
    E W⁴ = 3v²−2Σ a_i⁴ ≤ 3v².

Hölder with exponents 3/2 and 3 gives

    v ≤ (E|W|)^(2/3) (E W⁴)^(1/3),

and hence E|W|≥sqrt(v/3)≥1/sqrt(3m). The claimed bound

    ||q−ν||_TV ≥ 1/(2 sqrt(3m))

is correct. Equal weights give the matching order upper bound 1/(2sqrt(m)) by Cauchy–Schwarz.

Thus attaining error at most ε requires m≥1/(12ε²), whereas equal weights with m≥1/(4ε²) suffice. These estimates hold on any deterministic subsequence of distinct times in this example. Under the failure bound 2^{-j}, the support necessarily has at least 4^j/12 points. In particular no bound uniform in j is possible.

For every coupling with a measurable full-equality success event, the failure probability dominates supremum-event TV. The proof uses indicator tests, not a diagonal-measurability assumption. The support obstruction is therefore not an artifact of a particular maximal-coupling implementation.

The lower bound assumes that the marginal is the indicated deterministic mixture, as guaranteed by independence of the sampled time from X. It is not a theorem about arbitrary adaptive sampling dependent on X.

## 7. Limited primary-source comparison and priority posture

A bounded search for combinations of setwise convergence, coupling characterization, random times, convex combinations, and Mazur did not locate an inspected primary source stating exactly the full theorem in Attempt 3. That is not a novelty conclusion or an exhaustive literature audit.

Two directly inspected primary papers make the standard analytic ingredients especially clear:

- Peletier, Rossi, Savaré, and Tse, *Jump processes as generalized gradient flows*, Section 2.2, equations (2.3)–(2.5), explicitly lists the equivalence between setwise convergence and weak L1 convergence of densities under a common dominating measure. Section 2.1 starts with a general measurable space. This supports the classical status of the analytic reduction, not a claim that their paper proves the present orbit-coupling statement. [Published open-access article](https://link.springer.com/article/10.1007/s00526-021-02130-2).
- Carmona, Tangpi, and Zhang, *Conditional McKean-Vlasov control*, Lemma 5.4, Remark 5.5, and the proof of Lemma 5.4 explicitly use Mazur's lemma to obtain total-variation convergence of finite tail convex combinations after weak L1/setwise convergence. The surrounding control theorem is not being audited or used here; this is evidence of an existing use of the same convexification step, not an exact prior version of the random-time theorem. [Primary preprint, version 1](https://arxiv.org/html/2510.06543v1).

Accordingly, the positive result should be described as a proved coupling formulation assembled from classical convexification and common-part coupling, with its quantifiers and original-orbit preservation made explicit. No priority claim, claim of expert acceptance, or validation of the inaccessible contemporary manuscript is warranted.

## 8. Corrections, carry-forward limits, and final acceptance

The earlier audit required removing the unsupported assertion that SC is “strictly weaker” than TV convergence and distributional exact coupling. The current Attempt 1 has been checked and now says only that SC can hold when those properties fail, explicitly making no reverse-implication assertion. **That correction is resolved.**

Publication corrections and limits:

1. Attempt 3 now states that the time subsequences are nonnegative integers.
2. Attempt 3 now incorporates the explicit product-space success realization in Section 3 above.
3. Attempt 4 now explicitly distinguishes independence from the pair from independence from X in Attempt 3.
4. Present the positive theorem as a full arbitrary-space coupling characterization within its declared auxiliary-copy format.
5. Do not claim one stationary orbit, one pair valid before all subsequences, independent final comparison copies, a finite exact-coupling time, or an unqualified solution/novelty result.
6. Do not misstate the source as explicitly requiring the stronger two-process format. Retain partial status because interpretation and literature acceptance remain unresolved, not because the positive equivalence lacks full-path or arbitrary-space validity.

No fatal gap was found in Attempts 3–5. The principal residual issue is the scope and status of the characterization, not its correctness.
