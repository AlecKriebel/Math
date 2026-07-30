# Literature and priority audit

**Audit date:** 2026-07-29  
**Search cutoff:** 2026-07-29  
**Verdict:** the universal two-input closure and the resulting
setting-minimality theorem are plausibly original, but the existence of a
fixed-qubit POVM-over-PVM separation at \(3\times2\) settings is prior art.

## Executive conclusion

The publication should separate three claims that have different priority
status.

1. **Universal \(2\times2\) closure.** No primary source located in this audit
   states or proves
   \[
   \mathcal Q^{\mathrm{POVM}}_2(2,2)
   =
   \mathcal Q^{\mathrm{PVM}}_2(2,2)
   \]
   for arbitrary finite output sets, local Hilbert spaces of dimension at most
   two, and arbitrary shared classical randomness. This is the strongest
   plausible novelty claim.
2. **Minimum input architecture.** No prior source located here establishes
   that \(3\times2\), up to exchanging the parties, is the minimum number of
   local input settings for a fixed-qubit POVM-over-PVM Bell separation. This
   follows from the new closure theorem and an exact \(3\times2\) certificate.
3. **Existence of a \(3\times2\) separation.** This is **not new**. Vértesi and
   Bene gave a \(3\times2\) fixed-two-qubit separation in 2010. The new
   contribution is an independent rational Bell functional with an exact
   algebraic strategy and an exact analytic global PVM upper certificate, not
   the \(3\times2\) architecture or separation phenomenon itself.

The defensible wording is therefore “we prove” and, for the literature
comparison, “to our knowledge, no previous work established.” The present
search supports neither an unqualified “first” claim nor a claim that the
problem was explicitly posed as a longstanding open problem.

## Exact fingerprint of the new result

The result under audit concerns a standard bipartite Bell behavior
\(p(a,b\mid x,y)\) with:

- two inputs \(x,y\in\{0,1\}\) per party;
- arbitrary finite, input-dependent output alphabets;
- a bipartite state whose local Hilbert spaces have dimension at most two on
  every quantum branch;
- arbitrary local POVMs on the POVM side;
- qubit PVMs on the PVM side, including zero projectors, deterministic PVMs,
  input-dependent stochastic output postprocessing, and arbitrary shared
  classical randomness;
- equality of the resulting **convex behavior sets**, not equality of
  individual measurements;
- no dimension-increasing Naimark dilation.

The exact \(3\times2\) certificate uses a different Bell functional from the
Vértesi–Bene \(I_{CH3}\) family. Alice has two binary PVMs displayed in three
labels and one genuine ternary rank-one POVM; Bob has two binary PVMs. The
simple maximally entangled strategy attains
\[
L_0=20\sqrt2+\frac{16}{25},
\]
while every fixed-qubit PVM strategy obeys
\[
\beta_{\rm PVM}\le
U=20\sqrt2+\frac35+\frac{4+3\sqrt2}{250},
\qquad
L_0-U=\frac{3(2-\sqrt2)}{250}>0.
\]
The strengthened partially entangled strategy attains
\[
L_1=\frac{16+8\sqrt{7813}}{25}>L_0.
\]
Neither \(U\) nor \(L_1\) is claimed to be the exact global optimum of its
respective strategy class.

## Search method and limits

The audit used the following routes.

- Exact-phrase and concept searches across arXiv and publisher indexes for
  combinations of “two settings,” “two inputs,” “arbitrary outcomes,” “qubit,”
  “POVM,” “PVM,” “projective,” “Bell behavior,” and “minimal settings.”
- Full-text inspection of the primary sources closest in scenario or theorem
  type: Masanes; Toner–Verstraete; Vértesi–Bene; Barra et al.; Oszmaniec et al.;
  Guerini et al.; Gómez et al.; Schwarz et al. and its corrigendum; Rout et al.;
  Coccia et al.; Brinster et al.; and Kotowski–Oszmaniec.
- Inspection of all records returned in the OpenAlex cited-by set for the
  Vértesi–Bene paper (54 records at the audit date), followed by verification
  of relevant claims against the primary papers rather than the index record.
- DOI metadata checks through the publishers/Crossref and arXiv metadata checks
  through the official arXiv records.

This is a serious priority search, not a mathematical proof of absence.
Unindexed theses, conference notes, unpublished manuscripts, differently
phrased results, and papers appearing after the cutoff remain possible. A
qualified novelty sentence is warranted; an absolute priority assertion is
not.

## Claim-by-claim comparison

| Candidate claim | Closest prior primary source | What the source actually proves | Priority assessment | Safe manuscript language |
|---|---|---|---|---|
| Binary-output \(2\times2\) quantum correlations need only qubit PVMs | [Masanes (2005)](https://arxiv.org/abs/quant-ph/0512100) | For two **dichotomic** observables per party, every extreme quantum correlation is attained with a pure multiqubit state and projective observables. | Prior art; essential ancestor. | “Masanes proved the corresponding statement when every measurement is dichotomic.” |
| Dimension reduction for two dichotomic observables per site | [Toner and Verstraete (2006)](https://arxiv.org/abs/quant-ph/0611001) | Bell-functional maxima with two two-outcome measurements at each site have qubit support, via the two-projector block decomposition. | Prior art; output restriction is decisive. | “Jordan-type block reduction handles the fully dichotomic case but not genuine ternary qubit POVMs.” |
| Every binary qubit POVM is projectively simulable | [Oszmaniec et al. (2017)](https://doi.org/10.1103/PhysRevLett.119.190501) | Measurement-level characterization: qubit PM-simulable POVMs are the convex hull of two-outcome POVMs. Genuine extremal ternary and tetrahedral POVMs are not individually PM-simulable. | Prior art; does not imply the new behavior-level theorem. | “Individual genuine qubit POVMs remain non-projectively-simulable; our equality is instead at the level of finite Bell behaviors.” |
| Fixed-qubit POVMs can beat fixed-qubit PVMs in a \(3\times2\) Bell scenario | [Vértesi and Bene (2010)](https://doi.org/10.1103/PhysRevA.82.062115) | Alice has two binary settings and one ternary setting; Bob has two binary settings. A ternary qubit POVM beats qubit PVMs. The arbitrary-two-qubit PVM comparison is supported by coincident numerical lower and NPA upper values. | Definitely prior art. | “Vértesi and Bene established the first known \(3\times2\) fixed-qubit separation.” |
| Improved values and experimental analysis for \(I_{CH3}\) | [Barra et al. (2012)](https://doi.org/10.1103/PhysRevA.86.042114) | Numerical optimization of the same \(3\times2\) family for maximally and partially entangled states, plus detection-efficiency analysis. | Prior art; not a universal closure or setting lower bound. | Cite as refinement of the Vértesi–Bene construction. |
| Exact rational \(3\times2\) separator with a symbolic global PVM upper certificate | No matching prior certificate located | The new functional has rational coefficients; both the achieved values and the strict global PVM upper gap are proved algebraically. | Appears new, but is an exactification/strengthening of a known architecture, not a new existence phenomenon. | “We also provide an exact rational \(3\times2\) separation certificate.” |
| Universal \(2\times2\) equality for arbitrary finite outputs | No matching prior theorem located | The new result closes the residual binary-plus-genuine-ternary architecture on both parties and then completes all boundaries by convex reduction. | Plausibly original and the principal priority claim. | “We prove that …”; optionally “To our knowledge, this arbitrary-output two-setting closure was not previously known.” |
| \(3\times2\) is setting-minimal | No matching prior theorem located | One-input scenarios are local; the new theorem rules out \(2\times2\); the exact separator supplies \(3\times2\). | Plausibly original. | “Consequently, \(3\times2\), up to exchanging the parties, is the minimum input architecture.” |
| Lorentz-incidence/rank-trichotomy proof mechanism | No matching construction located | A residual five-ray incidence model, positive local-dual multipliers, ambient inertia, exceptional fibers, and an explicit rank-zero PVM decomposition. | Appears methodologically new. | Present as the proof method; do not make a separate priority superlative unless needed. |

## Direct comparison with the 2010 \(3\times2\) result

The closest historical source is not merely adjacent; it uses exactly the same
input counts. It must be credited in the abstract or first page.

| Feature | Vértesi–Bene \(I_{CH3}\) | Present exact separator |
|---|---|---|
| Inputs | Alice \(3\), Bob \(2\) | Alice \(3\), Bob \(2\) |
| Outputs | Alice \((2,2,3)\), Bob \((2,2)\) | Alice displayed as \((3,3,3)\), with a zero third effect on the first two inputs; Bob \((2,2)\) |
| Genuine generalized measurement | Alice’s third, ternary qubit POVM | Alice’s third, ternary rank-one qubit POVM |
| State for displayed lower bound | Maximally entangled two-qubit state | Maximally entangled state for \(L_0\); a partially entangled algebraic state for \(L_1\) |
| Bell coefficients | \(I_{CH3}=cI_{CH}+I_3\), including \(1-1/\sqrt2\) | Rational coefficient table |
| PVM comparison on the maximally entangled state | Analytic | Covered by the global analytic bound |
| PVM comparison over all two-qubit states | Numerical level-two NPA upper bound coinciding with a numerical qubit lower bound for the six PVM support cases | Exact analytic upper certificate \(U\), valid globally over all fixed-qubit PVM strategies |
| Exact global PVM optimum claimed? | Numerical equality is reported as “numerically exact,” not a symbolic identity | No; only \(\beta_{\rm PVM}\le U\) is needed and claimed |
| Exact global POVM optimum claimed? | No; the displayed POVM value is a lower bound | No; \(L_0,L_1\) are achieved lower bounds |
| Shared randomness | Not foregrounded; irrelevant to a linear optimum because a mixture cannot exceed its best component | Included explicitly in both behavior sets; the linear separator remains valid after convexification |

Accordingly, the new paper must not say that it discovers the first \(3\times2\)
separation. It can accurately say that it gives a new exact rational
certificate and uses it, together with the new \(2\times2\) lower bound, to
obtain the first located minimum-setting classification.

## Related results that do not subsume the theorem

### Measurement-level projective simulability

[Oszmaniec et al.](https://arxiv.org/abs/1609.06139) and
[Guerini et al.](https://arxiv.org/abs/1705.06343) study whether a fixed POVM
can be reproduced, on every input state, by randomizing and postprocessing PVMs
on the same Hilbert space. That is strictly different from the new theorem.
A genuine ternary qubit POVM can fail their measurement-level test while every
finite two-input Bell behavior containing it still has a PVM realization after
convexifying complete bipartite strategies. The PVM components may change the
state and the entire measurement family; they need not simulate the original
POVM as an operator identity.

[Brinster et al. (2026)](https://doi.org/10.1103/nsjr-vnmg) provide a current
hierarchy and experiment for certifying measurement-level non-simulability.
[Kotowski and Oszmaniec (2026)](https://doi.org/10.1109/TIT.2026.3678498)
prove approximate/noisy projective simulation results in arbitrary dimension.
Neither is an exact fixed-qubit Bell behavior-set equality.

### Device-independent and fixed-measurement certification

[Gómez et al. (2016)](https://doi.org/10.1103/PhysRevLett.117.260401) use four
Alice settings (three binary and one ternary) and three binary Bob settings to
certify an irreducible ternary qubit measurement. The extra settings are
essential to that certification and lie outside \(2\times2\).

[Coccia et al. (2026)](https://doi.org/10.1038/s41534-025-01175-x) associate
rank-one qubit POVMs with saturated Tsirelson bounds by adding self-tested
Pauli/tilted-CHSH measurements. Their full protocol has multiple extra inputs.
Their reminder that arbitrary POVMs admit projective dilations explicitly
allows a larger Hilbert space, which the fixed-qubit comparison forbids.

[Rout, Bhattacharya, and Horodecki
(2025)](https://doi.org/10.1088/1367-2630/adc0b4) study a randomness-free task
with fixed copies of an unknown measurement and bounded pre-shared resources.
Their comparator is measurement-level projective simulability (or a
dimension-bounded classical shared system), not the convex hull of complete
fixed-qubit PVM Bell strategies with unlimited shared classical randomness.
Their result therefore does not contradict the fact that every one-input
standard Bell behavior is local.

### A cautionary corrected claim

[Schwarz et al. (2016)](https://doi.org/10.1088/1367-2630/18/3/035001) claimed
that a ternary Bell inequality required a genuine qubit POVM at its maximal
violation. Their
[2018 corrigendum](https://doi.org/10.1088/1367-2630/aabe5c) reports a qubit
PVM strategy attaining the same value and identifies the numerical omission of
zero POVM elements as the source of the error. This history directly supports
the present paper’s insistence that zero projectors, deterministic
measurements, and every qubit PVM rank partition be included. It also argues
for restrained novelty language and exact certificates.

## Recommended historical wording

### Abstract-level wording

> Vértesi and Bene showed that three inputs on one party and two on the other
> suffice for a fixed-qubit Bell separation between general and projective
> measurements. We prove the matching lower bound: with two inputs per party
> and arbitrary finite output alphabets, the convex sets of fixed-qubit POVM
> and PVM behaviors coincide. An exact rational \(3\times2\) certificate then
> makes \(3\times2\), up to exchange of the parties, the minimum setting
> architecture.

### Introduction-level novelty wording

> To our knowledge, previous work did not determine whether genuine
> multi-outcome qubit POVMs can separate the two behavior sets when each party
> has only two inputs. We close this case for arbitrary finite outputs.

### Exact-certificate wording

> Unlike the earlier numerical global two-qubit comparison for \(I_{CH3}\), our
> independent \(3\times2\) separator has rational coefficients and is certified
> by exact algebraic lower and upper bounds. We do not determine either global
> optimum.

## Claims to avoid

- “The first \(3\times2\) qubit POVM–PVM separation.”
- “POVMs first become useful at \(3\times2\)” without immediately defining the
  standard Bell model, fixed local dimension, shared randomness, and
  postprocessing convention.
- “All pairs of qubit POVMs are projectively simulable.”
- “Every two-setting POVM strategy has the same-state PVM realization.”
- “The exact PVM optimum is \(U\)” or “the exact POVM optimum is \(L_1\).”
- “POVMs and PVMs are equivalent on qubits.”
- “Dimension-independent equivalence.”
- “First proof” or “longstanding open problem” without an additional
  author-conducted expert and thesis search.

## Remaining priority risks before submission

1. Search theses and conference proceedings using the exact set-equality
   formulation and the residual \((2,3)\)-by-\((2,3)\) terminology.
2. Check references citing both Masanes (2005) and Vértesi–Bene (2010), not
   merely the cited-by set of the latter.
3. Search recent 2025–2026 preprints once more immediately before arXiv
   submission.
4. Ask any independent human reader already within the project’s permitted
   collaboration structure to flag remembered folklore results. This audit
   does not authorize or initiate external outreach.
5. Preserve the exact public timestamp of the repository release, but do not
   describe a repository commit as peer review or as conclusive legal priority.

## Verified primary bibliography map

The machine-usable records are in `paper/references.bib`. Central metadata was
checked as follows.

| Work | DOI | arXiv |
|---|---|---|
| Vértesi–Bene (2010) | [10.1103/PhysRevA.82.062115](https://doi.org/10.1103/PhysRevA.82.062115) | [1007.2578](https://arxiv.org/abs/1007.2578) |
| Barra et al. (2012) | [10.1103/PhysRevA.86.042114](https://doi.org/10.1103/PhysRevA.86.042114) | [1207.0712](https://arxiv.org/abs/1207.0712) |
| D’Ariano–Lo Presti–Perinotti (2005) | [10.1088/0305-4470/38/26/010](https://doi.org/10.1088/0305-4470/38/26/010) | [quant-ph/0408115](https://arxiv.org/abs/quant-ph/0408115) |
| Masanes (2005) | — | [quant-ph/0512100](https://arxiv.org/abs/quant-ph/0512100) |
| Toner–Verstraete (2006) | — | [quant-ph/0611001](https://arxiv.org/abs/quant-ph/0611001) |
| Haapasalo–Heinosaari–Pellonpää (2012) | [10.1007/s11128-011-0330-2](https://doi.org/10.1007/s11128-011-0330-2) | [1104.4886](https://arxiv.org/abs/1104.4886) |
| Navascués et al. (2015) | [10.1103/PhysRevA.92.042117](https://doi.org/10.1103/PhysRevA.92.042117) | [1507.07521](https://arxiv.org/abs/1507.07521) |
| Gómez et al. (2016) | [10.1103/PhysRevLett.117.260401](https://doi.org/10.1103/PhysRevLett.117.260401) | [1604.01417](https://arxiv.org/abs/1604.01417) |
| Oszmaniec et al. (2017) | [10.1103/PhysRevLett.119.190501](https://doi.org/10.1103/PhysRevLett.119.190501) | [1609.06139](https://arxiv.org/abs/1609.06139) |
| Guerini et al. (2017) | [10.1063/1.4994303](https://doi.org/10.1063/1.4994303) | [1705.06343](https://arxiv.org/abs/1705.06343) |
| Schwarz et al. corrigendum (2018) | [10.1088/1367-2630/aabe5c](https://doi.org/10.1088/1367-2630/aabe5c) | incorporated in [1511.05253v3](https://arxiv.org/abs/1511.05253) |
| Rout et al. (2025) | [10.1088/1367-2630/adc0b4](https://doi.org/10.1088/1367-2630/adc0b4) | [2412.00213](https://arxiv.org/abs/2412.00213) |
| Coccia et al. (2026) | [10.1038/s41534-025-01175-x](https://doi.org/10.1038/s41534-025-01175-x) | [2503.13282](https://arxiv.org/abs/2503.13282) |
| Kotowski–Oszmaniec (2026) | [10.1109/TIT.2026.3678498](https://doi.org/10.1109/TIT.2026.3678498) | [2501.09339](https://arxiv.org/abs/2501.09339) |
| Brinster et al. (2026) | [10.1103/nsjr-vnmg](https://doi.org/10.1103/nsjr-vnmg) | [2511.04446](https://arxiv.org/abs/2511.04446) |
