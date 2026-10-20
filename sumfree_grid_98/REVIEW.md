# GREEN-006: independent source and proof audit

Audit date: 2026-10-20 UTC. Target: fixed dimension, ordinary componentwise integer addition; repeated summands are allowed.

## Disposition

**QUALIFIED PASS for the all-fixed-d asymptotic theorem, after the explicit local repairs and independent exact computation below. NOT an acceptance of an exact finite-cardinality solution.** Keevash–Lim v2 is a directly relevant submitted preprint, not a verified peer-reviewed publication. Its supplied numerical script is not a rigorous certificate as written. This review independently replaces that computation and repairs the identified Markov-chain proof error; neither error produced a counterexample to the theorem.

Green's literal question asks for the largest sum-free subset of the positive integer cube. His comments identify the limiting density as the main aspect. The underlying catalog uses that same broad literal question, although its dated discussion narrows the residual to determining every fixed-d density. Consequently an unqualified `already_solved` label for the whole literal question would overstate what has been established. Recommended wording: **all-fixed-d asymptotic density resolved by a submitted preprint, with independently checked corrections; exact finite maximum not established by this audit.** If a workflow requires an exact finite solution, retain that target as a distinct unresolved obligation rather than silently substituting its asymptotic aspect. This is not a claim that every exact finite instance or formulation is open.

## Theorem mapping and grid boundary

Write F_d(N) for the maximum on {1,...,N}^d and G_d(N) for that on {0,...,N}^d. Intersection preserves sum-freeness and the former cube is contained in the latter. Therefore

F_d(N) ≤ G_d(N) ≤ F_d(N) + (N+1)^d − N^d.

No translation of a sum-free set is used; such translations need not preserve this property. Keevash–Lim's Theorem 1.1 supplies G_d(N) ≤ c*_d N^d + O_d(N^(d−1)). The slice {x: u*_d N ≤ Σx_i < 2u*_d N} is sum-free even when x=y: the coordinate sum of two slice points is at least the excluded upper endpoint. Counting lattice points of this fixed polytope gives the matching c*_d N^d + O_d(N^(d−1)) lower bound, on either cube. Hence

F_d(N) = c*_d N^d + O_d(N^(d−1)),

where c*_d is the maximum volume of {x∈[0,1]^d: u≤Σx_i<2u}. This establishes the limit, not merely a limsup. It neither supplies exact finite maxima, nor classifies extremizers, nor gives a uniform growing-d assertion.

## Proof dependency audit

1. Theorem 1.5 constructs uniform discrete-slice couplings inductively. The d=2 base imports the interval-mixability criterion in Perchet–Rigollet–Le Gouic, Proposition 15: parity plus triangle inequalities. This is a cited external theorem, not reproved here. The induction uses a stationary distribution of a finite stochastic map, and uniqueness of each one-coordinate stationary distribution. Its printed connectivity justification is incorrect but has the complete elementary repair below.
2. Corollary 2.4 reflects one coupled slice to obtain X+Y=Z with all three marginals uniform. This follows directly from the repaired coupling theorem.
3. Lemma 3.1 supplies strict slice-volume margins. The large-d argument is analytic, based on convolution preserving log-concavity, exponential tilting, and the mean/mode/variance inequality proved in Lemma 3.4. The large-deviation discussion in §3.1 is explicitly heuristic and is not needed for the final proof. Dimension 3 is elementary; dimensions 4–200 are computational. The independent certificate below covers every one of these dimensions and certifies the real constants needed for the analytic tail.
4. Lemma 4.2 transfers strict continuous inequalities to discrete slices with uniform fixed-d O(N^(d−3)) error. Inclusion–exclusion for the bounded-composition counts supplies that uniformity. The strict margins absorb the error, including the floor in m=⌊u*_d N⌋.
5. Lemma 4.3 constructs three nonnegative coupling weights. The middle weight uses each intermediate slice at most twice and the last at most four times. Lemma 4.2 controls their combined load. O(N^(d−2)) boundary defects are permitted. Assuming N even is harmless: enlarge an odd N by one, changing N^d by O_d(N^(d−1)).
6. The final fiber inequalities, attributed to Lepsveridze–Sun, give the dual bound. The comparison of weighted and unweighted sums needs a two-sided error estimate, not merely the printed one-sided inequality; the repair is immediate below. The already-known d=1,2 bounds remain external base results.

This is a mathematical audit of the critical argument, not a machine-formalized proof, and does not claim independent reproof of every imported theorem. The unrelated convex-body discussion in §5 is outside the needed dependency chain and has not been accepted here.

## Repair 1: Markov-chain connectivity (v2 p.5)

For the chain in the paper,

M(i,u)=N_(d−2)(r−i−u)/N_(d−1)(r−i).

Thus its positive transitions satisfy 0≤r−i−u≤(d−2)n. The printed upper bound (d−1)n is wrong. The claim that state 0 is adjacent to every state whenever r≤(d−1)n is also false: d=3,n=2,r=3,i=0 gives M(0,0)=0. Both errors were verified against the rendered PDF, not only text extraction.

Here is a complete replacement. Assume d≥3 and n≥1; n=0 is trivial. The state space is the integer interval J=[max(0,r−(d−1)n),min(n,r)]. A universal neighboring state h exists:

- If 0≤r≤n, use h=0. For i∈J, 0≤r−i≤n≤(d−2)n.
- If n≤r≤(d−1)n, J=[0,n]. Use h=max(0,r−(d−2)n). Then 0≤h≤n, h≤r−n, and r−h≤(d−2)n. Consequently 0≤r−i−h≤(d−2)n for all i∈J.
- If (d−1)n≤r≤dn, use h=n. Here i∈[r−(d−1)n,n], so 0≤r−2n≤r−i−n≤(d−2)n.

Thus every state is adjacent to h, including h itself. The chain is irreducible and aperiodic; in particular its stationary distribution is unique. The stationary-marginal argument and induction then go through unchanged. This repairs the theorem rather than merely flagging a typographical error.

## Repair 2: numerical certification

### What the supplied script actually does

The public script linked from Appendix A was retrieved, read, and not executed. Retrieval metadata: 3189 bytes, SHA-256 4f9a43cd765c3097f9b3c01170d0cb861accd7ecdf115d895f24badae428d29f. It uses floating-point root candidates and mpmath interval recurrences. Its certificate logic has three defects:

- It accepts 0∈g([a,b]) as proof that [a,b] contains a zero. Interval range inclusion alone does not prove existence; overestimation can contain zero while g has constant sign. Strict opposite endpoint signs would suffice because g is continuous and has a unique zero in the prescribed range. The script does not perform that test or an actual interval-Newton existence test.
- Its reciprocal coefficient is computed as an ordinary rounded mp.mpf value and then wrapped in a singleton interval. A rounded reciprocal of an arbitrary integer is not generally an exact enclosure of the true reciprocal. Interval division should be used instead.
- It tests B≥1.01, whereas the lemma needs B≥1/0.99=100/99. The observed margins are much larger, but those are not identical thresholds.

Separately, the printed Appendix recurrence has coefficient d−k+1−t where d−k−t is required. For d=2,x=1.5 the printed version gives 1.5 rather than the triangular density 0.5. The supplied script uses the correct coefficient. This typo was verified visually in PDF p.18.

### Independent replacement and results

The authored `verify_slice_exact.py` uses the exact identity, for rational x=p/q and d≥2,

f_d(p/q) = [Σ_(0≤j≤⌊p/q⌋) (−1)^j binom(d,j)(p−jq)^(d−1)] / [(d−1)! q^(d−1)],

with f_d zero outside its support. Python arbitrary-precision integers and Fraction perform all acceptance arithmetic. SciPy proposes root locations only; it has no authority to make a certificate pass. Each accepted rational interval [a,b] must satisfy exact g(a)<0<g(b), where g(u)=f_d(u)−2f_d(2u). Continuity and uniqueness then locate u*_d rigorously. Unimodality bounds each needed density over its argument interval by endpoint minima and endpoint/mode maxima. Rational comparisons enforce A≥201/100 and B≥100/99.

All 197 dimensions d=4,...,200 PASS. The smallest certified lower bounds occur at d=200: A>4.3119392544 and B>2.1560064806. Displayed decimals are descriptive; acceptance uses exact rational comparisons. `EXACT_SLICE_RESULTS.json` records every rational bracket and result. For portable, fail-closed replay use `python computation/check_repairs_independent.py`; it also passes under -O and -OO. The earlier candidate-generation script `computation/verify_slice_exact.py` requires SciPy and remains assertion-sensitive; do not run that script with assertion removal (-O). See [REPAIR_AUDIT.md](REPAIR_AUDIT.md) and [REPRODUCIBILITY.md](REPRODUCIBILITY.md).

Dimension 3 is certified separately with 111/100<u*_3<28/25, exact endpoint signs, and elementary triangular-density bounds. For the analytic tail, the script bounds exponentials by exact rational Taylor sums with geometric tail bounds. It verifies the two tilted-mode windows at dimension 200, the rational root-offset bounds 77/1000<α<145/1000, and the necessary ratio inequalities. Monotonicity of (Dδ−1)/√D extends the mode-window check to every D≥200. Thus apply the analytic argument for d≥201, where both densities f_d and f_(d−1) meet the threshold, while the exact computation covers d=200. `ANALYTIC_CONSTANTS_RESULTS.json` records this PASS. The certified upper bound for the second ratio sum is below 0.961844, safely below 0.99.

These checks replace the defective numerical proof logic rather than asserting that floating-point agreement establishes the lemma.

## Other local corrections and endpoints

- The derivative of the slice volume in §3 is 2f_d(2u)−f_d(u), the negative of the displayed expression. The zero equation and its unique optimizer are unchanged.
- The analytic proof invokes estimates on f_(d−1) after a threshold stated for dimension at least 200. Use d≥201 analytically and d≤200 computationally, as above.
- In the final proof, if Δ(x)=|S(x)|−|S*(x)| and H is the complement of C, then |Σ_H(W−1)Δ|≤(n+1)Σ_H|W−1|=O(n^(d−1)). Therefore the weighted sum equals the unweighted sum plus O(n^(d−1)). This two-sided estimate justifies the final conclusion; the printed 'at most' direction alone does not.
- The displayed numerical estimate for the first ratio in §3.3 contains an inconsistent decimal expression. The clean needed bound is exp(0.8)>2.01, certified here.

## Sources and publication status

- Ben Green, *100 Open Problems*, Problem 6 and its comments: https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf . The author-hosted PDF is the target authority; dated catalog prose is not a substitute.
- Peter Keevash and Jeck Lim, *On the largest sum-free subset of the lattice cube*, arXiv:2605.00816v2: https://arxiv.org/abs/2605.00816v2 ; full version https://arxiv.org/html/2605.00816v2 . The arXiv record confirms submission 2026-05-01 and revision 2026-06-16. The locally inspected PDF has SHA-256 792fe630e8162b7d017d4efd81991a4f4a537e497ad59a4906cdb21499d84fe8, 469187 bytes.
- Appendix A's public implementation: https://people.maths.ox.ac.uk/keevash/papers/sumfree_verify.py . It was inspected but not executed; authored replacement checks are supplied separately.
- Jeck Lim's author page https://sites.google.com/view/jecklim and Peter Keevash's bibliography https://people.maths.ox.ac.uk/keevash/ were checked in the source-recovery gate. The former labels the paper submitted; no journal acceptance is verified here.
- Lepsveridze–Sun's published d=3,4 result: https://doi.org/10.1093/imrn/rnag081 ; current preprint https://arxiv.org/abs/2311.18289v3 . Do not attribute a published d=5 result from stale older-title metadata.
- Imported interval coupling theorem: Perchet, Rigollet and Le Gouic, *An algorithmic solution to the Blotto game using multimarginal couplings*, Operations Research 72(5), 2061–2075 (2024), Proposition 15, as cited in Keevash–Lim.

## Publication boundary

This review and the independent checker/results are authored audit artifacts. The downloaded paper, copied public script, source extracts, catalog records, and private coordination are not part of an intended publication payload. No remote action was taken by this audit.
