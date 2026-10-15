# Independent recent/broad priority falsification report

PR239 / 30001321 / OWR-4081-005. Audit date: 2026-10-15 UTC.

## Disposition

**No exact antecedent to the submitted full theorem, and no nontrivial
law-special antecedent with its complete scale/tail quantifiers, was found in
this bounded lane. This is not a certification of novelty.** A closely related
all-scale result already exists for one-dimensional directed random walk on
the backbone of supercritical oriented percolation. In particular, it would
be incorrect to say that all previous one-dimensional dynamic-environment
comparisons require a fixed power of the elapsed time as their coarse scale.

The strongest verified comparison is BBDS, arXiv:2410.14302, Lemma 4.1. It
has a genuinely stronger coarse conclusion than the fixed-power mesoscopic
result earlier in that paper. Its model is not the iid elliptic transition
environment in Berger's 2009 source. The audit found no valid theorem-level
transfer across this model difference. The 2024 first version already states
the lemma; the January 2026 revision is not its first appearance.

The mathematical candidate itself is not re-proved or promoted here. Priority
of its proof method is also not certified: coarse-scale iteration,
environment exposure, replica differences, invariant densities, coupling,
and concentration from coupling have substantial prior literature.

## Frozen claim and success criteria

The only submitted mathematical claim read for this lane is
`../submitted/unsolved_math_prioritization/attempts/30001321/PROOF.md`
(its title and Section 1 inputs). No other new priority lane was read.

For each fixed iid law of p_{s,x} with 0<p_{s,x}<1 almost surely, a walk jumps
by +1 with probability p_{s,x} and by -1 otherwise. For every deterministic
M_N→∞, every deterministic alignment of M_N-site interval partitions, and
each fixed ε,K>0, the target is

    P_env(sum_I |μ_N^ω(I)-E_env μ_N^ω(I)| > ε) = O(N^{-K}).

A prior theorem counts as **full coverage** only if its assumptions include
all these fixed laws and its conclusion implies all these quantifiers. A
genuine law-special theorem with the same scale and tail statement is tracked
separately, because it may answer a stronger informal reading of the negative
conjecture even without full coverage. Mere convergence in expectation,
probability, or almost surely; fixed-power mesoscales; weak invariance
principles; and local limits with a random density do not automatically count.

The source is the full [OWR 38/2009
report](https://ems.press/content/serial-article-files/46239), printed p.2151,
Berger's Theorem 1 and Conjecture 1. The negative sentence is not accompanied
by a formal additional quantifier on laws. The two logical readings and
their different law-special priority consequences are set out explicitly in
`QUANTIFIER_AUDIT.md` §1. No claim that the problem stayed open until the
present work is justified by this search.

## Primary-source screening

The following are theorem readings from full primary sources, not conclusions
drawn from search snippets. Full source bytes and text extractions remain in
`private_reading/`. Names below are source aliases in `SOURCE_INVENTORY.json`.

| Source | Exact location checked | Main gap from target | F / S status |
|---|---|---|---|
| BBDS 2024/2026, arXiv:2410.14302 | v1 p.19, v2 p.21, Lemma 4.1, (4.1)–(4.2) | Correlated, nonelliptic percolation-backbone transition law | Neither; genuine same-strength result outside source model |
| BBDS 2021/2023, arXiv:2105.09030 | Lemma 2.1, (2.1)–(2.2); §4; Theorems 1.3–1.4 | The original coarse result requires d≥3 and has the same model gap | Neither |
| Drillick–Parekh 2025, arXiv:2510.22155 | Assumption 1.2, Example 1.4, Definition 1.11, Theorem 1.13 | Distribution-valued fluctuation limit; no full coarse L1/tail statement | Neither |
| Das–Drillick–Parekh 2023/2024 preprint, 2026 journal | arXiv:2311.09151v2 pp.2–3, Theorems 1.1–1.2 | Exponentially tilted moderate-deviation window and weak convergence | Neither |
| Parekh, 2026 final | Theorem 1.5, Definition 1.4, printed pp.6–7 | General-flow KPZ scaling limit, not all-cell coarse error | Neither |
| Drillick–Parekh–Sau 2026 | arXiv:2607.21443, introduction and Theorems 1.1/1.3 | Special continuous-time averaging process and fluctuation regimes | Neither |
| Dunlap–Gu 2021/2022 | arXiv:2105.07907v3 p.2, Theorem 1.1, (1.8)–(1.11) | Smooth Gaussian velocity diffusion; L2 random-corrector estimate | Neither |
| Kotitsas–Luo–Maurelli 2025 | arXiv:2509.07956v2 p.9, Theorem 1.9 | Continuum SPDE, smooth initial data, negative-Sobolev weak limit | Neither |
| Barraquand–Corwin 2015/2017 | arXiv:1503.04117v5, Theorem 1.15 / final Theorem 2.15; §1.6 | Beta law; large deviations / weak bulk CLT, not target strength | No law-special A(ν) found |
| Thiery–Le Doussal 2016/2017 | arXiv:1605.07538, §IV.D–E, (74)–(83), pp.14–16 | Beta point-to-point fluctuations; forward/backward distinction | No law-special A(ν) found |
| Balázs–Rassoul-Agha–Seppäläinen 2018/2019 | arXiv:1801.08070v2, model and §2 results | Beta walk conditioned at atypical velocity; Doob-transformed law | No law-special A(ν) found |
| Joseph–Rassoul-Agha–Seppäläinen 2011/2019 | Final pp.77–79, (1.3)–(1.5), Theorem 1.1 | Equilibrium for particle system, not fixed-start endpoint comparison | Neither |
| Yu 2014/2016 | arXiv:1412.3911v2, Theorems 1.5, 1.6, 1.8, Appendix A | Invariance/current/mean fluctuation limits | Neither |
| Peretz 2022/2025 | arXiv:2204.12238v2, Theorem 1.5; Proposition 4.1 | Static uniformly elliptic ballistic environment | Neither |
| Andres–Chiarini–Slowik 2020/2021 | arXiv:2001.10740v2, Assumptions 1.1–1.2, Theorem 1.4 | Undirected dynamic conductances, d≥2, inverse moments, a.s. limit | Neither |
| Deuschel–Guo 2021/2022 | Full publisher text, model and assumptions, Theorem 4 | Balanced uniformly elliptic continuous-time environment, d≥2 | Neither |
| Intermittent dynamical environment 2025 | Full publisher text, model and Theorem 2.9 | Holding/jump mechanism from site maps, moment/mixing conditions | Neither |

“F / S” refers to full-law coverage / nontrivial law-special exact target
property. A negative cell means the inspected theorem does not establish that
property; it does not assert that the source contains no useful estimate or
that no adaptation could ever work.

### The strongest prior coarse result

[BBDS arXiv:2410.14302](https://arxiv.org/abs/2410.14302) Lemma 4.1 bounds
the coarse quenched/annealed L1 error by C/M^c+C/N^c outside an event of
probability C̃N^{-c̃ log N}, in every spatial dimension d≥1. Substitution of
any M_N→∞ gives the desired every-K tail in that model; the complete
deduction is in `QUANTIFIER_AUDIT.md` §2. The underlying independent site
variables are not independent transition probabilities: transitions use
infinite future backbone membership. Equation (2.2) also allows holding and
zero probabilities. This source must be acknowledged as close prior context.

The earlier [arXiv:2105.09030](https://arxiv.org/abs/2105.09030) Lemma 2.1
states the analogous bound for d≥3. Its §4 explicitly iterates along
successively smaller powers of N, and Proposition 4.1 bounds the incremental
coarse error. Thus there is prior art for the very idea of passing from
fixed-power comparisons to arbitrary large block sizes. The 2024/2026 paper
extends the dimension-dependent input; it does not make independent iid
transition environments a special case of percolation.

### General-law subcritical fluctuation literature

[Drillick–Parekh arXiv:2510.22155](https://arxiv.org/abs/2510.22155) covers
general iid-in-time random kernels with translation invariance, exponential
annealed moments, rapidly decaying spatial correlations, and a nondegenerate
difference chain. Example 1.4 treats nearest-neighbor iid environments after
handling parity by a skeleton. For the nondegenerate iid ±1 case (symmetry
parameter p=1), the bulk centered density has normalization N^{1/4};
Theorem 1.13 gives convergence
in a space of distributions to an additive-noise SPDE. Neither that topology
nor the theorem's tail conclusion gives the target. An explicit smooth-test
countermodel to the tempting implication appears in `QUANTIFIER_AUDIT.md` §4.

[DDP arXiv:2311.09151](https://arxiv.org/abs/2311.09151) Theorem 1.1 uses iid
[0,1] weights of mean 1/2 and variance σ²<1/4. Its density is exponentially
tilted in a window N^{3/4}t+sqrt(N)x, and converges weakly to multiplicative
SHE. Theorem 1.2 concerns jointly finitely many similarly normalized tail
observables. The paper discusses biased-law extensions, but neither result
is the unweighted bulk coarse L1 statement. A rare-event profile at distance
N^{3/4} cannot directly contradict or prove the target's fixed ε error.

[Parekh's 2026 final
paper](https://doi.org/10.1017/fms.2026.10220), Theorem 1.5, extends such
KPZ limits to a general stochastic-flow framework. The observable in
Definition 1.4 is still a tilted density paired with smooth tests in a
negative-regularity space. [Drillick–Parekh–Sau
arXiv:2607.21443](https://arxiv.org/abs/2607.21443) studies continuous-time
averaging and how degeneracy changes the critical fluctuation scale. It
does not assert a coarse endpoint comparison for every iid law in (0,1).

### Random density factors do not erase the quantitative gap

[Dunlap–Gu arXiv:2105.07907](https://arxiv.org/abs/2105.07907), Theorem 1.1,
approximates the density of a Brownian particle in a spatially smooth,
white-in-time Gaussian velocity field by G_t(x)U(t,x). In d=1, (1.8) gives
uniform squared error bounded by Ct^{-4/3}log t; U has mean one and covariance
decay. The corrector becomes one in the incompressible case. These are real
quantitative local results, but the model and the environmental tail
conclusion differ. The immediate integrated error estimate gives only a
fixed polynomial rate; see the calculation in `QUANTIFIER_AUDIT.md` §6.

[Kotitsas–Luo–Maurelli arXiv:2509.07956](https://arxiv.org/abs/2509.07956),
Theorem 1.9, proves an additive Gaussian limit for a rescaled continuum
advection-diffusion equation, with smooth compactly supported initial data,
in C^γ([0,T];H^{-α}_loc). It supplies no theorem that upgrades all tiny
macroscopic intervals to total coarse L1 with arbitrary-K environmental
tails. It is relevant recent continuum fluctuation literature, not F or S.

### Beta environments: a real law-special priority check

The [Barraquand–Corwin
primary paper](https://www.phys.ens.psl.eu/~barraquand/papers/BetaRWREjournal2.pdf)
has exact formulas for beta transition laws and a large-deviation
Tracy–Widom theorem; the original preprint's Theorem 1.15 is restricted to
α=β=1 and part of the velocity range. Its bulk discussion invokes a general
quenched CLT. Exact formulas, the CLT, and an expected replica-overlap
equivalent do not state the all-scale, every-K coarse theorem. This audit
does not infer generality from beta solvability, and does not dismiss beta
solely because it is a special law.

[Thiery–Le Doussal arXiv:1605.07538](https://arxiv.org/abs/1605.07538)
obtains Gamma fluctuations in the diffusive region. Its §IV.E, (82)–(83),
explicitly distinguishes multiple starting locations with a fixed terminal
point from a fixed start with varying terminal points. For the latter, the
authors explain that endpoint Gamma factors must average away on the
diffusive scale and can remain correlated on smaller scales. That is not an
independence theorem or an every-diverging-scale concentration bound.
Consequently this source has not already supplied S by its stated results.

[Balázs–Rassoul-Agha–Seppäläinen
arXiv:1801.08070](https://arxiv.org/abs/1801.08070) studies conditioning at
an atypical velocity and its harmonic-function/Doob transform; that new
environment is time-correlated. Its fluctuation and large-deviation results
do not supply the target bulk all-scale theorem even for the original beta
law. No nontrivial beta S was located in these inspected primary sources.

### Other close families and why they do not transfer

[Joseph–Rassoul-Agha–Seppäläinen](https://www.math.utah.edu/~firas/Papers/walkers.pdf)
Theorem 1.1 treats finite-range iid environments under a nondegeneracy
condition and a span-one condition. It characterizes invariant occupation
measures and proves convergence to equilibrium for d=1,2. The span condition
does not directly include the ±1 parity lattice. More fundamentally,
equilibrium of an infinite particle system is not a uniform quantitative
local approximation for one particle started at a fixed site. Its coupling
proof is useful context, with no exact target coverage established here.

[Yu arXiv:1412.3911](https://arxiv.org/abs/1412.3911) proves a quenched
invariance principle for Howitt–Warren motion, quenched-mean fluctuations,
and particle-current limits. Appendix A gives a discrete iid-environment
invariance-principle argument. These are weak convergence observables; no
all-diverging-width coarse L1 theorem with a superpolynomial time tail was
found in those statements.

[Peretz arXiv:2204.12238](https://arxiv.org/abs/2204.12238), Theorem 1.5,
extends invariant-density local limits to static uniformly elliptic ballistic
RWRE in dimensions at least two. Proposition 4.1 has a quantitative
semi-local exit comparison. Its resolution of a different conjecture from
Berger–Cohen–Rosenthal is not a resolution of Berger's OWR 2009 conjecture.
The space-time lift here has zero backward transition probabilities, so
static uniform ellipticity fails. `QUANTIFIER_AUDIT.md` §7 gives the exact
obstruction, including when the original p is uniformly bounded away from
zero and one.

[Andres–Chiarini–Slowik arXiv:2001.10740](https://arxiv.org/abs/2001.10740),
Theorem 1.4, is an almost-sure local Gaussian limit for continuous-time
undirected dynamic conductances on Z^d, d≥2. Its inverse/direct moment
condition is explicit in Assumption 1.2. The directed normalized transition
law here is outside that model; arbitrary target laws need not satisfy any
inverse-moment condition. The theorem also does not provide every-K
environmental failure tails.

[Deuschel–Guo](https://doi.org/10.1007/s00440-021-01097-7) concerns balanced,
uniformly elliptic continuous-time nearest-neighbor rates in d≥2. Its
invariant-density local limit and heat-kernel estimates should not be
transferred to a nonbalanced d=1 iid transition law. In the target's
discrete-time nearest-neighbor normalization, pointwise balance would force
p=1/2. The full [2025 intermittent-environment
paper](https://doi.org/10.1007/s10959-025-01478-x), Theorem 2.9, instead uses
a site-dependent intermittent holding mechanism, moment bounds and
polynomial mixing, and an almost-sure local expansion. It is another model
and another quantitative conclusion.

## Citation/version audit and bounded-search limits

Eighteen recorded search batches contain **67 executed queries**. The exact
strings are in `SEARCH_LOG.json`; full results are private and hashed.
Queries included the exact source title, Berger plus conjecture/local-limit
phrases, M_N and coarse/superpolynomial terms, mesoscopic concentration,
beta diffusive limits, invariant densities, and explicit 2010–2026 variants.
The search followed the references and related primary works of the recent
general-law fluctuation and percolation papers. Secondary mirrors and search
summaries were used for discovery only. They support no theorem conclusion
in this report.

ArXiv landing-page bytes preserve the available submission histories. The
critical dates checked include:

| Work | First version | Later version inspected |
|---|---|---|
| 2410.14302 | 2024-10-18 09:05:50 UTC | v2, 2026-01-05 16:11:44 UTC; v1 PDF also checked |
| 2510.22155 | 2025-10-25 04:20:55 UTC | v1 only listed |
| 2311.09151 | 2023-11-15 17:48:47 UTC | v2, 2024-12-13 20:20:19 UTC |
| 2401.06073 | 2024-01-11 17:43:07 UTC | v4, 2025-12-01; 2026 publisher final inspected |
| 2105.07907 | 2021-05-17 14:40:42 UTC | v3, 2021-12-08 23:01:35 UTC |
| 2509.07956 | 2025-09-09 17:43:59 UTC | v2, 2025-10-17 16:47:43 UTC |
| 1503.04117 | 2015-03-13 15:48:21 UTC | v5, 2021-05-17; 2017 final also inspected |
| 1605.07538 | 2016-05-24 16:49:35 UTC | v1 only listed |
| 2204.12238 | 2022-04-26 11:36:53 UTC | v2, 2025-08-03 12:51:29 UTC |
| 2607.21443 | 2026-07-23 15:50:08 UTC | v1 only listed |

This was not a complete crawl of MathSciNet, zbMATH, every author's complete
bibliography, every source citing the 2009 workshop, nonindexed theses, or
unpublished work. It also was not a line-by-line proof audit of every paper
in the matrix. A title/abstract match was followed to full model/theorem
statements and relevant proof passages for the strongest candidates. Some
sources were screened and excluded at the model or conclusion level. A
failed author-host URL for the 2020 Blondel–Hilário–Teixeira paper was
recorded; no theorem conclusion in this report relies on that failed fetch.
No individual was contacted or outreach prepared.

## Exact remaining priority gap

The remaining issue is whether another primary theorem, a rigorously checked
combination of older estimates, or an uninspected source proves A(ν) for all
merely elliptic iid laws, or proves a nontrivial law-special A(ν) that already
answers a possible reading of the negative conjecture. No such implication
was verified here. Replacing that gap with “a local limit is known,” “the
field converges weakly,” “the environment is iid underneath,” or “a nearby
conjecture was disproved” would be invalid.

Bounded audit completion: **100% of this specified recent/broad search lane**.
Completion of absolute priority certification: **not established and not
assigned a percentage**. The appropriate combined disposition remains
**priority not certified**, with the percolation all-scale comparison
preserved as essential prior context and a serious proof-method comparator.
