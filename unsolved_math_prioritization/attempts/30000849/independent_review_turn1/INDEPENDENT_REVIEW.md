# Independent review: coagulation 30000849

## Verdict and source-coverage decision

**PASS_COMPLETE_LITERAL_DISPLAYED_NORMALIZATION_COUNTEREXAMPLE. No mandatory mathematical correction.**

The frozen first-turn candidate gives an actual admissible infinite-system solution that contradicts the universal normalization displayed in Conjecture1 of the original OWR report. This is more than noticing an inconsistent coefficient or performing a formal scaling calculation: existence, the mass bound, and a fixed-ray contradiction are proved. The contradiction survives replacement of the printed birth coefficient by the standard physical addition coefficient.

The coverage decision is nevertheless narrow and important. The result settles the **literal displayed normalization**, also reproduced in the imported clean statement. It is a source-normalization correction. It does **not** prove or disprove convergence to self-similarity with corrected exponents, settle the intended physical problem under a repaired normalization, or identify the correct profile and constants. The packet explicitly preserves these limitations. A blanket claim that general variable-rate self-similarity has been disproved would fail this review.

If the campaign disposition tracks the exact displayed conjecture, a source-qualified negative resolution after one substantive turn is justified. If a different task is to solve the corrected physical conjecture, this packet does not resolve that task, and its remaining proof budget must not be represented as exhausted. There is no basis here to invent the intended corrected conjecture silently. No historical priority is certified.

This was an uninvolved analytic and source audit. I did not supply the author route or edit frozen author files.

## Frozen version

- `COUNTEREXAMPLE.md`: SHA256 `c9c2bc59e1f1bf169b31aaaef4ec8370676d4ece19c6053a51f359aeb9bdbb77`
- `FROZEN_MANIFEST.json`: SHA256 `42d4758c188da53b43ef20ea905d08d40d9cfee00b480d4135533f630a9f8677`, binding12 author files

All12 author files and4 pinned PDFs match their manifest hashes. The author's2,040-control receipt replays byte-identically in a separate copy. The separately authored standard-library checker passes16,585 exact finite controls. Those arithmetic checks supplement the infinite proofs reviewed below.

## 1. Original definitions and the admissible test parameters

I read the full original contribution on printed2754–2756 and visually inspected both the equation and conjecture pages. The displayed time-only composition is `c_tilde_j(sigma)=c_j(t(sigma))`; no cluster-weight factor is part of that definition. The conjecture explicitly supplies a positive constant times `t^((2+omega)/(3-2p))` and amplitude exponent `[1-omega(1-p)]/[(2+omega)(1-p)]`. Its interior profile has the separate factor `eta^-p` and the indicated power of `1-eta^(1-p)`.

The choices `p=1/4`, `omega=0`, `alpha=1`, zero initial data and constant input1 lie within the displayed parameter conditions. Zero data satisfy every polynomial decay upper bound, including the imported condition with `mu=3`, regardless of the original report's unassigned bare r in that condition. There is no requirement of positive initial mass. The argument constructs positive concentrations for later times.

The scale constant's unspecified formula causes no loophole: the proof excludes every finite `K>0` and every finite `A>0` for the same solution. A zero or negative A cannot give the positive interior profile from nonnegative concentrations. A nonreal A cannot do so either. A nonpositive or nonreal size scale does not supply the positive increasing real scaling variable used by the source's limit.

The source really prints `j^(p-1)` in the birth term. At p=0 that is inconsistent with its next equation. The candidate does not use that inconsistency as its sole counterexample: it treats this printed system and, separately, the standard coefficient `(j-1)^p` confirmed by equation123 of the later da Costa survey.

## 2. Finite approximations and genuine infinite-system existence

The finite truncations retain all losses and discard births beyond the last coordinate. Their vector fields are locally Lipschitz polynomials. Every coordinate derivative on its zero face is nonnegative, so nonnegative initial data remain nonnegative. This justifies the signs used in the subsequent mass estimate.

I independently differentiated the finite first moment. The dimer contribution is `(2b2-2)c1^2`; an interior `c1*c_i` has coefficient `(i+1)(b_(i+1)-a_i)`; the final loss is `-(n+1)a_n*c1*c_n`. For the standard model all interior terms vanish. For the printed coefficient every extra term is negative. Thus `M_n(t)<=t`, with `0<=c_j^(n)(t)<=t/j`, for both systems. These bounds also prevent finite-time explosion of each finite ODE.

On every compact time interval the stated component derivative bounds are uniform in truncation size. Diagonal Arzela–Ascoli extraction gives one subsequence converging locally uniformly for every fixed component and all integer time horizons. Nonnegativity lets the mass inequality pass first through finite sums and then through their increasing limit.

The nonlinear monomer term is not passed to the limit on component convergence alone. The essential tail estimate is

`sum_(j>L) j^(1/4)c_j^(n)(t) <= T(L+1)^(-3/4)`.

It follows directly from the uniformly bounded first moment. Together with convergence of each finite prefix this proves uniform convergence of the whole monomer sum on compact time intervals. Its limit is continuous. The integral ODEs therefore pass to the limit, and their continuous right sides make every limiting component continuously differentiable. The initial data remain exactly zero. This establishes an actual global nonnegative classical componentwise solution of each infinite system, with its nonlinear infinite sum finite and well-defined.

There is no uniqueness assumption or need to choose a solution after seeing K or A. The one solution extracted for each coefficient convention has the same mass bound for all proposed normalization constants. An integrating factor for `c1'+(c1+P)c1=1` gives strict monomer positivity at positive times, and the positive birth terms propagate positivity to all components.

## 3. Optional mass equality in the standard model

The second-moment telescope was independently checked, including the boundary coefficient `-(n^2+1)a_n*c1*c_n` and the dimer term. Since `i*a_i=i^(5/4)<=i^2` and `c1<=t`, the differential inequality `S_n'<=1+2t S_n` gives the stated uniform compact-time second-moment bound.

That bound controls both possible losses in passing to the limit. It makes the mass tails uniformly small, and it bounds the first-moment boundary flux by `2T H_T n^(-3/4)`. Integrating the latter on a fixed time interval sends it to zero. The complete masses converge, so `M(t)=t` for the standard solution. This rules out explaining the contradiction by a mass-losing approximation or gelation selection. The literal printed system only needs the proved upper bound, not equality.

## 4. Fixed-ray Fatou lemma

The original limit holds with `eta=j/sigma` fixed; it does not grant uniformity in eta. The author's lemma respects that distinction. For every integer j, set `t_j(eta)=(j/(K eta))^(1/s)` and integrate the nonnegative quantity `j*c_j(t_j(eta))*|t_j'(eta)|` on one fixed compact interval `[a,b]` inside the positive profile region.

The change of variables is exact and strictly monotone in eta. The derivative contributes `j^(1/s)` and the conjectured amplitude contributes `j^-r`, so the normalized integral is of order `j^(1-r+1/s)`. Pointwise convergence in eta gives a positive lower bound on its liminf by Fatou. The weight is positive and finite on the compact interval; no dominated convergence or interchange with an infinite sum is needed. In the present application the profile is continuous and strictly positive there.

A positive liminf supplies one fixed d and one J such that the individual integral lower bound holds for **every integer j>=J**. Summing the band `n<=j<2n` therefore gives order `n^(2-r+1/s)`. Each individual time interval lies in the stated common interval, whose upper endpoint has order `n^(1/s)`. Nonnegativity and the first-moment budget bound their finite sum by the time integral of `C(1+t)^beta`, of order `n^((beta+1)/s)`.

The necessary inequality is consequently `s(2-r)<=beta`. The proof never infers a mass lower bound from an unproved Riemann-sum approximation at one common time. Nor does it replace exact rays by rounded indices, assume a rate of convergence, or use pointwise convergence uniformly in a parameter.

## 5. Exact contradiction and all constants

At the test parameters, `s=4/5`, `r=2/3`, and `beta=1`. The necessary mass inequality fails since `s(2-r)=16/15>1`. Equivalently, the fixed-ray integrals have individual exponent19/12; their band sum has exponent31/12; the integrated mass budget has exponent30/12. Their difference1/12 is strict.

All multiplicative constants involving K, A and the chosen interior interval are finite and positive and cannot change this power contradiction. The argument excludes convergence at every eta in the interval simultaneously; it need not identify a particular failing eta in advance. That is sufficient because the conjecture requires all fixed interior ratios.

The exact same bound applies to the mass-conserving standard addition solution. Consequently the result remains a normalization obstruction even after the obvious birth coefficient is repaired.

## 6. What the result leaves open

The condition `r>=3/4` is only a necessary mass-compatible amplitude threshold for this selected scale and parameters. Replacing2/3 by3/4 removes this particular contradiction but does not prove the limit, derive its profile or constants, or settle other parameters. The source's p=0 result has compatible exponents and is not contradicted.

The2015 survey still presents the nonconstant-rate extension formally and has mixed clock notation; it supplies no independently established corrected theorem in the inspected passage. The other pinned works concern constant aggregation rates or the critical-cluster modification. These source facts do not justify a general negative result about physically intended self-similarity.

**Disposition:** the frozen package is sound as a complete counterexample to the exact displayed universal normalization, with the explicit source-correction scope retained. It has no complete-result verdict for an unformulated corrected physical target. Publication language and the queue findings should make that distinction immediately visible.

## Verification inventory

`HASH_CHECK.json` binds all author and reading-input hashes. `AUTHOR_REPLAY.json` records the exact author replay. `independent_check.py` separately checks finite moment identities, arbitrary rational vector-field evaluations, positive fourth-power coefficient comparisons, tail inequalities, the exact change-of-variable exponents and common time windows. `INDEPENDENT_CHECKS.json` records16,585 exact assertions and no floating point. These finite controls are not presented as a numerical existence or asymptotic convergence proof.
