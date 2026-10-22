# Independent priority bridge audit: PR239 / 30001321

Audit date: 2026-10-15 UTC. Scope: the exact frozen files in `../submitted/unsolved_math_prioritization/attempts/30001321/`, with independent primary reading of the BCR / BBDS / BCD16 bridge. No other new priority report was read. No external communication, Git operation, index/ref mutation, or provider mutation was performed. This report is research assessment, not a manuscript.

## Verdict

**The all-scale coarse-L1 conclusion and the multiscale strategy are established prior art in other model classes. A direct, previously published theorem covering the complete scalar iid claim has not been authenticated by this bridge audit.** This is not evidence that no such theorem exists.

There is a substantive positive bridge result: the old iteration can be adapted to accept one quantitative polynomial coarse scale gamma<1/2, rather than an input at every polynomial scale. The frozen TURN_2 supplies that quantitative input after explicit parameter choices. `ABSTRACT_BOOTSTRAP.md` gives a complete audit derivation, including the bad-box density concentration needed at arbitrarily slow final scales. Thus the all-scale conclusion does not require the candidate's particular final-segment strip construction: an old mechanism also closes the candidate's earlier estimate.

The exact dating distinction matters. The newly checked scalar input (H) below is not a theorem stated in the examined prior sources. Using its derivation now cannot backdate that application. The strongest supported priority assessment is: **old conclusion shape, old generic closure mechanism, classical iid replica input, and an exact scalar iid application whose earlier publication remains unverified.** A claim of a newly invented all-scale bootstrap would be untenable. A claim of a new application is not falsified by model titles or by the fact that its proof uses older mathematics. The frozen candidate itself explicitly makes no novelty or priority claim.

## Exact claim tested

For every fixed iid law of p_(s,x) with 0<p<1 almost surely, X jumps ±1 with the two probabilities p and 1-p. Let mu_N and alpha_N be the quenched and annealed endpoint laws. For every deterministic sequence M_N to infinity, every deterministic equal-interval alignment, and epsilon,K>0, the claim is

    P_env(sum_(I in Pi_N) |mu_N(I)-alpha_N(I)|>epsilon)
        <= C_(epsilon,K) N^(-K)

eventually. The threshold can depend on M_N; fixed-law constants need not be uniform as the law approaches deterministic arrows. There is no uniform ellipticity, inverse-moment condition, symmetry, or rate of M_N divergence. The real-length extension in PROOF Section 6 is acknowledged separately from integer lengths. This audit's explicit abstract bridge is written first for integer interval lengths; its mechanism also permits real-length partitions once the corresponding local estimate (H) is supplied.

The question is a negative conjecture about this iid model. A law-special positive theorem can already refute an interpretation that every nondegenerate law fails. Such a theorem would not establish the candidate's universal law quantifier. Neither a theorem in a different dependent environment nor the deterministic p example alone establishes the exact universal result. No nondegenerate scalar iid law is shown below to be a special case of the BCR or BBDS model theorem.

## Primary objects, dates, and locations

All whole reading PDFs, text extractions, rendered source pages, and arXiv history HTML are under `private_reading/` and are excluded from the public authored manifest. Full URLs, independent retrieval timestamps, bytes, SHA256, and failed retrievals are recorded in `SOURCE_RETRIEVAL.json` and `SOURCE_DATES.json`. These are original primary sources; search snippets were used only to locate them.

| Source | Authenticated history | Relevant location in exact copy |
|---|---|---|
| [BCR arXiv:1405.6819v1](https://arxiv.org/pdf/1405.6819v1) | 2014-05-27 07:17:28 UTC | Thm 5.1 and start of proof, PDF p.19; model and ellipticity, pp.1–2 |
| [BCR arXiv:1405.6819v2](https://arxiv.org/pdf/1405.6819v2) | 2016-09-02 09:12:21 UTC | Thm 5.1, PDF p.28; proof pp.29–34; model p.1 |
| [BBDS arXiv:2410.14302v1](https://arxiv.org/pdf/2410.14302v1) | 2024-10-18 09:05:50 UTC | model (2.2), PDF p.3; Lem 4.1, pp.19–20; Lem 3.11–3.12 / Thm 3.2 proof, pp.15–19 |
| [BBDS arXiv:2410.14302v2](https://arxiv.org/pdf/2410.14302v2) | 2026-01-05 16:11:44 UTC | Lem 4.1, PDF pp.21–22; model Section 2 |
| [BBDS23 arXiv:2105.09030v1](https://arxiv.org/pdf/2105.09030v1) | 2021-05-19 09:53:23 UTC | Lem 2.1 p.7; Prop 4.1 p.14; model-specific iteration and independent bad-box approximation, Section 8 pp.34–47 |
| [BCD16 arXiv:1505.02791v3](https://arxiv.org/pdf/1505.02791v3) | v1 2015-05-11 20:12:06 UTC; inspected v3 2016-06-01 13:02:09 UTC | Thm 3.1 p.23; Ass 3.2–3.3 pp.24–25; Ass 3.9 and 3.11 p.27 |
| [BRAS06 author copy](https://www.math.utah.edu/~firas/Papers/rap.pdf) | arXiv math/0507226 v1: 2005-07-11 17:27:45 UTC; v2: 2006-04-07 22:18:07 UTC | model pp.6–7 and 14–15; Thm 3.1 p.15; difference chain pp.18–20; Lem 4.1 pp.21–22 |

History dates come from the [BCR history](https://arxiv.org/abs/1405.6819), [BBDS history](https://arxiv.org/abs/2410.14302), [BBDS23 history](https://arxiv.org/abs/2105.09030), [BCD history](https://arxiv.org/abs/1505.02791), and [BRAS history](https://arxiv.org/abs/math/0507226). The BBDS v1 cover has an internal October 21 date, while the version submission history is October 18; the latter is the authenticated availability date. PDF file metadata creation dates are not used as publication dates. The BBDS copies independently hash-identically to those supplied by the parent. The independently retrieved BRAS arXiv v2 also contains the Green-function Lemma 4.1, authenticating that ingredient in a dated 2006 version; the author copy supplies convenient page locations.

An attempted nonexistent BBDS23 v3 retrieval failed. A journal URL returned HTML rather than a readable PDF and is marked failed; no mathematical claim relies on it. The arXiv v1 full primary copy is the working BBDS23 source.

## What the older all-scale results really say

BCR Theorem 5.1 bounds coarse L1 by C/M^c+C/N^c outside a superpolynomial environment exceptional set, uniformly over bounded starting sites and a deterministic partition. Its hypotheses are static iid random transition vectors on Z^d, d>=4, uniform ellipticity on all 2d coordinate directions, and the stated ballisticity condition (P). The theorem is already in v1 (2014), not newly added in 2016. Its iterative contraction from large boxes down to fixed-size boxes is therefore established prior methodology.

BBDS Lemma 4.1, both v1 and v2, has the stronger explicit failure bound C exp[-c(log N)^2], with discrepancy C/M^c+C/N^c, for all spatial d>=1 in its percolation-backbone walk. It therefore immediately gives the candidate's arbitrary-diverging-scale quantifier **in that model**. At fixed epsilon,K, first let M_N and N make the discrepancy threshold small, then use log N>K/c for the failure bound. This part has no hidden polynomial lower bound on M_N.

BBDS23 supplies the more detailed proof dependency, rather than an abstract general theorem: the iteration step is Prop 4.1, derived from a polynomial-box comparison theorem, annealed derivatives, and high-probability control of the annealed mass of bad boxes. Section 8 explicitly approximates its infinite-range backbone field by finite-range fields to recover independent separated boxes. The iid scalar model has exact finite-range dependence for a finite path segment, so that particular approximation is unnecessary. The bad-box **density** step is still needed: a union bound at the very last scale does not have a superpolynomial rate in N when M_N diverges slowly.

## Direct model inclusion and exact shear checks

### BCR: exact directed embedding, incompatible hypotheses

On the reachable parity lattice define

    A_s=(s+X_s)/2,   B_s=(s-X_s)/2.

The environment p_(s,x) becomes an iid scalar field indexed by (A,B), since s=A+B and x=A-B is a bijection on that lattice. A positive step increments A by one, and a negative step increments B by one. Thus this is an exact static directed random environment on a quadrant of Z^2 with moves +e1 and +e2 and probabilities p and 1-p. It preserves quenched finite path probabilities exactly.

This does not meet BCR Thm 5.1. It has only two allowed successors, no negative-coordinate transitions, dimension two, and no uniform lower bound for general p laws. An injective affine coordinate change preserves the number of successors. An embedding into Z^4 adds unused directions with probability zero; it cannot produce the required positive lower bound on all eight directions. A random time change permitting backward moves revisits old space-time environments and is no longer this exact iid dynamic walk. Neither device is an admissible theorem application without a new equivalence proof.

### BBDS: exact transition-kernel obstruction

For d=1, the BBDS walk selects uniformly from nonempty subsets of the three next-layer neighbours {-1,0,+1} on the backbone, and selects uniformly from all three when outside it. Possible nonzero kernel weights are reciprocals of integers. Among these local kernels, a strictly positive two-sided no-holding kernel must have p=1/2; this local enumeration alone does not make the whole BBDS process deterministic or iid.

More decisively, the BBDS annealed one-step law has positive probability for all three successors. For percolation parameter p_perc<1, the event that the current Bernoulli site is closed has probability 1-p_perc>0 and forces the outside-backbone uniform kernel. At p_perc=1 the kernel itself is uniform on all three successors. Any per-layer injective spatial map still has three possible one-step successors, whereas the target has two. Passing to a skeleton or a noninjective lumping is a new operation that requires proof of the resulting quenched Markov law and iid scalar environment; none is supplied by the examined theorem.

The future-dependent backbone transition field is not a fresh independent field of p_(s,x), even though its underlying Bernoulli site variables are iid. Conditioning on those sites and conditioning on independent scalar transition probabilities are distinct quenched models. Hence Lem 4.1 cannot be invoked directly for even a generic discrete scalar law such as p in {1/5,4/5}, much less every continuous merely elliptic law.

### BCD16: broad environment class, insufficient conclusion

BCD16 Section 3 really is a general framework, not just a different paper title. Nevertheless Thm 3.1 concludes a zero-speed LLN and an **annealed** CLT. It has local integer-valued medium states, good-block coupling and irreducibility assumptions, a block confinement condition, and point-reflection symmetry of the walker. It does not assert a quenched coarse-L1 rate or the input (H).

For the arbitrary biased scalar law even the zero-speed conclusion and reflection hypotheses do not directly fit. A deterministic centering by the usually noninteger velocity changes the spatial lattice and jump kernel; it is not a verified application of the printed assumptions. The finite local integer-state representation also does not directly encode an arbitrary continuous one-site quenched scalar law without modifying the state-space assumptions. These are additional direct-inclusion issues, but the missing output alone suffices: an annealed CLT cannot supply environmental superpolynomial tails. BBDS explicitly treats extension of its local limit results to that broader class as a prospective extension (v1 Remark 2.4; BBDS23 discussion before the outline). The class name is not a license to promote that extension to a theorem.

## BRAS06: an exact earlier source for the central iid ingredients

This inclusion succeeds. Put Y_s=(X_s+s)/2 and r_(s,j)=p_(s,2j-s). The r field is iid and Y jumps 0 or 1 with probabilities 1-r and r. This bounded-range transition-vector model has annealed span one and satisfies the BRAS nondegenerate-randomness assumption because r is in (0,1) almost surely. Its environment law need not be uniformly elliptic, symmetric, or discrete. Both forward and backward time orientations are covered by its definitions. This removes the parity issue without replacing the environment by a new law.

BRAS derives the common-environment replica difference transition kernel, homogeneous away from zero and perturbed at zero. Lem 4.1 yields cumulative Green growth G_L(0,0)=O(sqrt L). The first-hit identity implies G_L(d,0)<=G_L(0,0) for every initial difference d: a walk starting at d can only collect visits after its first hit of zero. Therefore, for every old environment and deterministic segment length L,

    E[sum_(j<L) I_(s+j) | F_s] <= C sqrt L.

Ordered-time expansion of this same conditional bound gives the explicit Kac estimate

    E[(sum_(j<L) I_(s+j))^k | F_s] <= k! C^k L^(k/2).

This is a direct, checkable deduction from an established source ingredient, not a new hypothesized high moment. Pointwise g_n monotonicity is not needed for this deduction. Binomial heat-kernel and same-parity derivative bounds, independent time-layer exposure, and the scalar exponential martingale estimate are likewise classical tools. The earlier source does not claim the target coarse-L1 tail or (H); its quenched invariance theorem and quenched-mean fluctuations do not alone give them.

A raw import of BBDS's adjacent-site O(1/n) derivative estimate into the original ±1 coordinate would be wrong. On that coordinate the adjacent point lies on the opposite parity, so the gradient has size O(n^(-1/2)). One must use a same-parity shift of two or the exact {0,1} shear. This is a checkable substantive repair in a proof transplant, not just notation.

## A full mechanism transfer and its precise priority boundary

`ABSTRACT_BOOTSTRAP.md` proves the following independently: if, for one gamma<1/2 and b>0,

    P_env(L_(n,H)^z > n^(-b)) <= C exp[-c(log n)^2]

uniformly for H>=n^gamma, z, and deterministic alignment, then the old BCR/BBDS iteration yields the complete all-scale target. The proof chooses time shrink rho>2gamma, contracts the previous discrepancy, smooths inside old cells by the annealed kernel, and controls annealed mass on bad restart cells through finite-dependence weighted concentration. It includes the exceptional-set rate in N at the arbitrarily small final scale.

The frozen TURN_2 has the required quantitative margins with gamma=5/16, beta=9/32, eta=1/64 and b=1/128. Choosing rho=7/8 gives positive within-cell smoothing exponent 1/7, and the audit lemma gives a possible coarse error power M^(-7/320), in addition to the N term. The exact fractions and numerical checks are saved. This is stronger quantitative information than needed to answer the fixed-epsilon target.

This establishes a complete **mathematical proof route from the candidate's earlier estimate through old methodology**. Combining BRAS's Green bound with the explicitly repeated elementary derivation of TURN_2 supplies all its inputs as mathematics. It does not establish that somebody published the scalar application before this candidate. The distinction is essential: a newly assembled derivation from old results is not automatically an authenticated old theorem.

The route labelled “invoke a prior theorem and conclude the universal scalar target as an already published corollary” is therefore **BLOCKED at the dated scalar-model local quantitative comparison (H), or at a genuinely model-general published theorem accepting only the already cited Green/semigroup/independence inputs**. Neither BCR Thm 5.1, BRAS Thm 3.1/Lem 4.1, BCD Thm 3.1, nor BBDS Lem 4.1 is such a theorem as written. Simply declaring that the printed proof goes through would transfer its central local comparison estimate without checking it. This audit checks a new derivation rather than silently assuming that step, and preserves the dating gap.

The alternative route labelled “all-scale closure is a novel conceptual ingredient” is **falsified at the mechanism level** by BCR 2014 and BBDS's independent bad-box implementation. The candidate's particular one-final-segment construction may be a different simplification; this audit has not authenticated priority for that specific construction. Since the frozen candidate claims no novelty, this finding calls for accurate credit and continued priority review, not a finding of a false novelty statement in the supplied text.

## Finite controls and reproducibility

Run `python3 finite_controls.py` in this folder. It writes `FINITE_CONTROLS.json` and checks:

- Exact rational path-law equality under the directed shear for N=12 and transition probabilities ranging from 1/10000 to 9999/10000. Maximum error is exactly zero; all 13 reachable endpoints agree.
- Enumeration of all seven nonempty uniform-successor kernels in d=1 BBDS. The only strictly positive no-holding two-sided local kernel has scalar value 1/2.
- The parity obstruction numerically: sqrt(n) times the maximal adjacent gradient stays about 0.824–0.826 for n=100,400,1600, while n times the same-parity gradient stays about 1.04. This supports the exact parity argument, not an asymptotic proof by numerics.
- Exact rational positive margins for the quantitative TURN_2 reading and rho=7/8 bootstrap.
- A logarithmic comparison showing why an exceptional-set tail at M=log log N cannot be relabelled superpolynomial in N.

An initial numerical-control implementation overflowed by converting a large binomial coefficient to float; it was replaced by log-gamma evaluation before any control output was accepted. Exact shear and kernel controls remain rational arithmetic. These tests validate coordinate/support and exponent bookkeeping only; the asymptotic theorem is established, if at all, by the displayed deductions and the independently validated candidate proof.

## Completion and remaining question

This scoped bridge investigation is complete at 100% of its assigned check. The wider priority question remains open in the sense that no exact earlier scalar theorem has been authenticated here; this is not a claim that the mathematical research goal is 100% complete. The checkable outcome is a precise limitation on direct theorem inclusion, a successful exact BRAS ingredient inclusion, a complete reusable old-method bootstrap, and an explicit dated-publication gap. No outreach was prepared or initiated. No absence-of-match novelty inference is made.
