# Independent adversarial audit: setwise stationarity attempts

Date: 2026-10-20. Target: Thorisson Problem 3.2, ID 9900006.

Publication note: this report audits Attempts 1–2 and COUPLING_CRITERIA.md. Its SC wording correction has been incorporated. The later AUDIT_EXTENSIONS.md assesses Attempts 3–5 and supersedes any implication that the full record lacks an arbitrary-space auxiliary-copy characterization. See SCOPE.md for the final disposition.

## Verdict

**PASS for the substantive results assessed here; these earlier results do not themselves characterize the convergence in Problem 3.2.** I found no fatal mathematical gap in the Bernoulli example, the freely recoupled-sequence theorem, or the rank-one obstruction for arbitrary bistochastic couplings. The last result is not merely an application of the published graph-automorphism statement: its extension is proved in the submitted argument and survives the checks below. The explicit staircase parameters meet the inspected source's hypotheses.

One unsupported comparison in the earlier wording of Attempt 1 required narrowing and has now been corrected: the example proves that SC can hold while TV convergence and distributional exact coupling fail. Calling SC “strictly weaker” additionally asserts the reverse implication, which these files have not proved in the full general-measurable-space setting. This wording issue does not affect either counterexample.

This audit assesses mathematical validity, not priority, novelty, peer review, or completeness of the literature search.

## 1. Original target and full-path scope: PASS

I independently read Section 3 of Thorisson's original public preprint, including both printed pages 3–4. It introduces an arbitrary measurable state space, and its setwise tests range over the entire infinite-path sigma-field. The separable-metric assumption appears only after Problem 3.2, in the discussion leading to Problem 3.3. No restriction excluding deterministic invertible dynamics on a large state space was found. [Original preprint](https://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf).

Problem 3.1 asks whether setwise convergence implies TV convergence. Problem 3.2 asks for a coupling characterization if not. Therefore disproving 3.1 supplies the antecedent, not an answer to 3.2. Disproving the particular aligned-coupling candidate likewise does not settle 3.2. The source does not itself formally prescribe the exact syntax of an acceptable characterization of 3.2; preservation of the original process laws is a substantive scope choice here, not a quoted additional hypothesis.

## 2. Attempt 1, Bernoulli orbit example: PASS

The orbit map Phi is measurable coordinatewise, intertwines T and the path shift, and has a measurable left inverse given by the first state. Thus every path event A pulls back to one fixed measurable state event B. The shifted density is correctly indexed as 2 times the indicator of coordinate -n being 1.

Finite-coordinate cylinder approximation in rho-measure applies to every B in the product sigma-field, not just cylinders. For a fixed approximation C, independence applies once -n is outside its finite support. The errors are bounded by 2 rho(B symmetric-difference C) for the biased law and rho(B symmetric-difference C) for the stationary law. This proves full-path setwise convergence with the quantifiers in the required order.

The detecting event A_n may vary with n in the TV supremum. Its probabilities are 1 and 1/2, and contraction under Phi gives the matching upper bound. The constant TV distance is therefore exactly 1/2 in the stated normalization. This is a valid negative answer to Problem 3.1 under the preprint's hypotheses.

The proposed single coupling changes only coordinate zero before shifting, hence only coordinate -n afterwards. Its common domination by 2 rho and rho upgrades finite-coordinate agreement to every fixed measurable path test. The coupling is chosen once; the approximation and threshold, appropriately, may depend on the event. SC follows. No almost-sure simultaneous eventwise conclusion is being smuggled into the argument.

**Resolved wording correction:** the publication version replaces “SC is strictly weaker than total variation convergence and distributional exact coupling” with “SC can hold even when total variation convergence and distributional exact coupling fail.” No reverse implication is asserted or needed here.

## 3. Attempt 2, arbitrary bistochastic extension: PASS

### 3.1 Compactness with bounded marginals

The compactness assertion is valid on the standard nonatomic space being used. Here is a precise implementation of its abbreviated justification. Work modulo null sets on the standard Lebesgue model [0,1]; all couplings with marginals bounded by K rho ignore the discarded null strips. A sequence of such probabilities has a weakly convergent subsequence on the compact square. Its limiting marginals remain bounded by K times Lebesgue measure, by testing nonnegative continuous functions. Consequently rectangles with interval sides have boundary of limiting measure zero, so their masses converge. Approximation of arbitrary measurable side sets by finite unions of intervals, using the uniform marginal bounds for both the approximants and limit, upgrades this convergence to every measurable rectangle. Transfer back to the original standard space. This supplies an actual countably additive limiting probability, not just a finitely additive rectangle functional.

The same conclusion follows through a standard Borel realization with tightness and a continuity-set algebra. The nonatomic Lebesgue formulation avoids any ambiguity. It is not an argument for arbitrary nonstandard measurable spaces, and none is needed for this counterexample.

### 3.2 Tower surrogates and approximation

For fixed a<1, M_j tends to infinity and K_j=1/(M_j rho(B_j)) stays bounded. The first marginal of gamma_{j,p,q} is the uniform average of normalized restrictions to the distinct levels p,...,p+M_j-1; the second has the analogous levels starting at q. Both densities are at most K_j. Its graph displacement remains q-p throughout.

The averaging identity on tower-measurable rectangles is exact: with p,q<m_j and i<M_j the relevant coordinates stay in known levels of the tower. The original coupling may behave arbitrarily within those levels without changing membership in such rectangles.

Crucially, the required extension to fixed measurable rectangles uses the aggregate measures. Each marginal of eta_j is bounded by rho. Each marginal of the weighted surrogate sum is bounded by K_j rho because its total weight is at most one. No bound is claimed or needed for a normalized arbitrary cell restriction of kappa. Thus the potentially dangerous replacement of within-cell structure by a graph surrogate is legitimate for fixed tests. Finite unions of rectangles, including partition mismatch sets, inherit the approximation.

### 3.3 Invariant limits and domination

The invariance defect is at most 2/M_j by telescoping the finite orbit average. Rectangle convergence permits testing the preimage of every rectangle under T times T, so the limiting measure is invariant even though T need not be continuous in the compactness model.

For constant nonzero displacement d, gamma_j is bounded by K Delta_d. This passes to the limit. For displacement tending to either infinity, mixing gives Delta_{d_j} converging to rho times rho on rectangles; negative displacement follows by invertibility and exchanging the two test sets. Domination passes first on rectangles, then on finite disjoint unions of rectangles, and finally to the full product sigma-field by monotone-class extension. Thus the required domination of actual measures, not merely an inequality for a few test sets, holds.

An invariant probability dominated by a finite multiple of an invariant ergodic probability equals that probability: its Radon–Nikodym derivative is invariant and hence constant. Delta_d is ergodic because T is ergodic, and rho times rho is ergodic because T is mixing. These observations prove exactly the limit classification claimed.

### 3.4 Uniform finite-partition separation

The set of graph measures with nonzero integer displacements, together with the product measure, is compact for rectangle convergence: any sequence either has a constant displacement subsequence or a displacement tending in absolute value to infinity. None equals Delta_rho. Mixing on a nonatomic nontrivial space excludes T^d equal to the identity almost everywhere for d nonzero.

A countable separating generator ensures that any coupling different from the diagonal has positive mismatch for some finite partition. Mismatch probabilities for a fixed finite partition are continuous in rectangle convergence. The finite-subcover argument and common refinement therefore yield one partition with strictly positive minimum mismatch over the entire compact family. Applying subsequence compactness to any alleged exceptional tower-surrogate sequence gives the claimed eventual uniform lower bound. This is not a pointwise-to-uniform inference without justification.

### 3.5 Final estimate and application

The mass outside U_j times U_j is at most 2(1-rho(U_j)), using the two fixed marginals. It tends to 2(1-a). The off-diagonal level weights tend to zero by the separation bound. For each fixed event, tower approximation then bounds mismatch by 2(1-a). Taking a upwards to one is legal after fixing the event; the separating partition was allowed to depend on a. Zero mismatch on a countable separating family forces kappa to be the diagonal coupling.

The symmetrized measure [pi+pi-transpose+Delta_{(C-f-1)rho}]/C is nonnegative, has total mass one and both marginals rho. Its diagonal remainder creates no mismatch under any shift. SC for pi therefore implies the requisite convergence for kappa. Domination pi/C <= kappa then forces pi diagonal, contradicting its distinct marginals. This validates failure of necessity of SC.

## 4. Explicit mixing staircase: PASS, with cited mixing theorem

I independently opened Creutz–Silva's primary preprint, inspected Section 2.1, Section 7.1 and Theorem 10 on printed page 23. They use invertible transformations on a standard nonatomic probability space, define staircase spacers by s_{n,i}=i, and give mixing under restricted growth, which here is r_n squared divided by h_n tending to zero. Their general setup requires cut counts tending to infinity; the supplied r_n=n+2 meets that requirement as well. [Creutz–Silva preprint](https://arxiv.org/pdf/math/0109159).

The displayed recurrence yields h_n >= (n+1)! by induction. The widths are w_n=w_0/(n+1)!, and the added area at stage n is w_n(r_n-1)/2. Its sum is finite. Normalize the resulting finite measure. Widths go to zero, the increasing columns exhaust the constructed interval space, and the usual cutting-and-stacking construction has generating rank-one towers; null exceptional orbits may be discarded to obtain an invertible standard-space model. No additional random choice or unverified existence assertion is required.

The mixing conclusion uses the cited theorem, not an independent reproof of its entire argument. The Ryzhikov paper is background motivation, not a sufficient citation by itself for the arbitrary-kernel extension proved above.

## 5. Freely recoupled-sequence theorem: PASS within its stated scope

The finite control measure lambda dominates each marginal. Vitali–Hahn–Saks applies to the setwise-convergent finite positive measures and supplies uniform absolute continuity. A countable dense family in the lambda-measure algebra gives increasing finite partitions. The diagonal choice k(n) is valid.

The displayed finite-cell kernels are measurable kernels on arbitrary measurable spaces and have the claimed marginals. A countable kernel product supplies all variables on one probability space without regular conditional distributions. Uniform absolute continuity then upgrades the dense event family to all events. The converse is immediate from the mismatch bound. The fixed-target Bernoulli obstruction is also valid.

The proof does not handle a nonseparable measure algebra and does not preserve successive shift consistency of the freely recoupled variables. Neither limitation is repaired by the rank-one result; the latter instead shows that aligned orbit consistency can be impossible even in the standard setting. No general characterization follows from this freely recoupled-sequence theorem or the first two attempts alone. Attempt 3 and AUDIT_EXTENSIONS.md provide a separate arbitrary-space auxiliary-copy characterization, with the intended-problem and priority limits stated in SCOPE.md.

## Acceptance summary

- Accept the explicit full-path counterexample to the implication in Problem 3.1.
- Accept the separable-measure-algebra freely recoupled-sequence theorem.
- Accept the arbitrary-bistochastic rank-one rigidity lemma and its consequence that SC is not necessary, with the classical mixing theorem cited.
- The unsupported “strictly weaker” comparison is corrected, and the chronology/status statements are reconciled with Attempts 3–5.
- Do not mark Problem 3.2 solved. Do not claim novelty, literature priority, or verification of the inaccessible contemporary manuscript.
