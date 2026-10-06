# Original-stage independent adversarial audit: instability/amplification family

**Verdict: PASS for the explicitly scoped local-characteristic nonlinear orbital W^{1,∞} instability theorem.** No mathematical defect or required mathematical change was found. This family does not certify L²/H¹ nonlinear orbital instability, the full original source problem, a global weak continuation, historical priority, a paper, or a DOI.

Completed UTC: 2026-10-01T23:38:11.532953+00:00. Target 30004186 / OWR-17128-002, PR29. Assigned original head `5ac4a57e08dd72a6f16768f2288b9c0349999431`; base `c6975ca76f9f667f1250ba403d0e6da2aafe14d0`. Candidate SHA256 `95458afe7f030f3f0aec3b9d5150857e7dedcb8688e6325c4a0407497feb1b6c`. Main is a distinct integration state. All PR evidence was read from assigned-head Git blobs; no checkout, branch, commit, push, queue change, PR action, publication, release, installation, or external communication occurred.

## Independence and evidence boundary

The early source-first reconstruction was sealed at `2026-10-01T23:30:09.879104Z` as `EARLY_INDEPENDENT_SEAL.md`, SHA256 `71037584d34e4bd66630d820154764c17917a16671b88fdf43b76ed86fe3bcde`. Before that seal I read primary sources and the current candidate as a hypothesis. I did not read original code, old reviews, original result receipts, provenance/ledger metadata, or sibling audits. The entire original 16 files and one QUEUE change were inspected only afterward. I have not read sibling conclusions or used them in this verdict.

The [primary OWR report](https://ems.press/content/serial-article-files/46811), printed pp. 1940–1942, has the quadratic reduced Ostrovsky model and this parabolic periodic peak. Its closing nonlinear question is not assigned a topology. The curated target matches this source. The candidate's narrower W^{1,∞} theorem is therefore audited on its exact written scope. Both [the 2019 linear paper](https://pelinovsky.mcmaster.ca/PaperBank/PeakedWaveOstrov.pdf) and [the 2020 spectral paper](https://pelinovsky.mcmaster.ca/PaperBank/PeakedSpectralUnstable.pdf) retain the nonlinear evolution-space obstacle. No inference from their linear growth/spectrum is used here.

The universal proof below is analytic evidence. The original 20 checks, old 135 assertions and new 66 controls are exact finite diagnostics, not proofs of the Banach ODE, arbitrary characteristic behavior, or PDE theorem. Their code was actually read before execution.

## Universal amplification argument

On L=2π, set κ=π/3, c=κ² and φ(x)=(x−π)²/6−π²/18, periodically lifted. One has |φ′|≤κ and the mean-zero primitive p=(φ−c)φ′, including p=0 at each crest. The kernel G(z)=1/2−z/L has distributional derivative δ_0−1/L and integral zero; ∫|G|=L/4=π/2. Hence ||P h||∞≤(π/2)||h||∞ for mean-zero h. The coefficient and sign are correct. The new kernel sign control reaches L/4 with a bounded mean-zero sign function, so replacing it by L/8 is a false substitute.

Let X′=V and V′=P u(t,X), and define r=X−ct and h=V−φ(r). The periodic φ is Lipschitz, so φ∘r is absolutely continuous. Off the countable family of crest level sets r∈L Z, the ordinary chain rule applies. On each such level set, r′=0 almost everywhere; there V=c and h=0, and p=0. Thus

h′=P(u−b)(t,X)−φ′(r)h

holds almost everywhere for b(t,x)=φ(x−ct), with any bounded choice of φ′ on the reference crest. Isolated or repeated crossings and tangencies cause no extra measure term because φ itself is continuous. The argument does not claim a classical crest derivative. Integrating and using that X is onto gives a(t)≤a0+∫(κ+π/2)a(s)ds, so a(t)≤a0 e^{At}, A=5κ/2, throughout existence. The bound requires neither a second-derivative estimate nor an independently assumed long lifetime.

For the actual transported corner q=X(t,0), ζ=q−ct satisfies ζ′=u(t,q)−c, not zero. The global periodic κ-Lipschitz bound implies

|ζ(t)|≤a0(e^{At}−e^{κt})/(A−κ),

|u(t,q)−c|≤a0[e^{At}+κ(e^{At}−e^{κt})/(A−κ)]
                 =(5/3)a0 e^{At}−(2/3)a0 e^{κt}
                 ≤(5/3)a0 e^{At}.

The actual trajectory can pass a crest of the reference wave; both periodic-lift bound and the preceding chain rule remain valid. No crest value or velocity is frozen at c.

## Uniform scales and logarithmic time

For a fixed smooth cutoff ρ and mean bump β, η=δ² and v0=−δ xρ(x/η). Its amplitude is ≤δ³, slope is ≤Mρ δ with Mρ=sup|ρ+sρ′|, and mass |I|≤δ⁵/2. The correction −Iβ has amplitude ≤||β||∞δ⁵/2 and slope ≤||β′||∞δ⁵/2. For δ≤1 one can take C0=1+||β||∞/2 and a fixed C1 depending only on Mρ, β and the chosen norm. The corrected perturbation is mean zero, continuous at the endpoints, changes only the right endpoint slope by −δ and leaves the left slope κ. The cutoff's rapid second derivative has no role in the candidate's C¹ label ODE. The source uses a normalized circle of length 2π; δ and the support relation δ² are dimensionless in that normalization, so these powers do not mix physical units.

The right slope quotient w=V_ξ/X_ξ obeys w′=V−w², including its right endpoint value. For y=w+κ and f=u(t,q)−c,

y′=2κy−y²+f, y(0)=−δ, |f|≤(5/3)C0δ³e^{At}.

The discarded −y² has the right sign for an upper estimate driving y negative. Thus

e^{−2κt}y(t)≤−δ+[5C0δ³/(3(A−2κ))](e^{(A−2κ)t}−1).

For fixed ε=κ/10 and Tδ=log(2ε/δ)/(2κ), A−2κ=κ/2. The error for t≤Tδ is at most (10C0/(3κ))(2ε)^{1/4}δ^{11/4}, whose ratio to δ is O(δ^{7/4}). The exponent is correct. An explicit sufficient smallness set is

0<δ<min{1, sqrt(L/3), 2ε, ε/(2C1), [3κ/(20C0(2ε)^{1/4})]^{4/7}}.

This also puts the initial slope norm below κ+ε and support away from β. At Tδ, if existence extends that far, y≤−ε. All constants and ε are fixed before δ varies.

More generally, support η=δ^p yields weighted error power 1+p−(A/κ−2)/2; its ratio to δ tends to zero iff p>(A/κ−2)/2. The candidate has p=2 and threshold 1/4. The new controls reject p=0, the critical p=1/4, and an excessively weakened exponent A/κ=6 with p=2. These show that the scale check has discriminating force; the controls do not claim that those alternative perturbations can never prove instability by another route.

## First hitting, essential suprema and orbital phases

The candidate's continuation prerequisite is valid. The C¹ closed-branch Banach space requires equal endpoint values, not equal endpoint derivatives, and includes φ and the perturbed data. The integral field H is a polynomial composition of continuous first-derivative products and integrations; it is uniformly bounded and Lipschitz on bounded C¹ sets. The weighted physical mean is preserved. If physical |u_x|≤M up to a finite maximal endpoint, the label Jacobian lies between e^{−Mt} and e^{Mt}; the primitive bound gives a finite amplitude bound, and V_ξ=w X_ξ and integration of Y′=V bound both C¹ coordinates. The field is then bounded, so its trajectory has a Banach norm limit at the finite endpoint, where X_ξ remains positive. Picard continuation restarts it. There is no appeal to compactness of an infinite-dimensional bounded set or an unsupported lifespan proportional to 1/δ.

S(t)=sup_{ξ∈[0,L]}|V_ξ/X_ξ| is continuous in time. It equals the physical essential derivative supremum: continuity on the one-sided branch gives positive-measure intervals approximating every endpoint value, and X_ξ>0 preserves their positive measure. The candidate therefore uses a real essential-supremum departure, not a derivative arbitrarily assigned at a single point.

If S reaches κ+ε before Tδ, its first hitting lies inside the local Lipschitz interval. Otherwise bounded-slope continuation forces existence beyond any candidate maximal endpoint ≤Tδ, and the Riccati estimate yields the hitting by Tδ. This avoids assuming logarithmic existence independently of departure.

For every θ, ||φ′(·−θ)||∞=κ. The reverse triangle inequality gives ||u_x−φ′(·−θ)||∞≥S−κ≥ε. It is valid for essential suprema and uniform in θ, so taking the orbital infimum is legitimate without a phase minimizer or corner alignment. Translation strong continuity in periodic W^{1,∞} is not assumed and would generally fail for a peak.

## Falsification limits and prior claims

A triangular function on a shrinking interval can have ||f′||∞=ε, while ||f′||²_2=2ε²h and ||f||²_2=(2/3)ε²h³. Mean correction is O(h²). Therefore a fixed slope excess alone does not force fixed L²/H¹ departure. This exact countercontrol is generic norm evidence, not a construction of a PDE solution. The candidate respects that limitation.

The [2018 v1](https://arxiv.org/abs/1804.03788v1), Section 4, asserts H¹ orbital instability through L² departure, imports a smooth-perturbation lifespan, and uses a stability bound proportional to δ. The [v2](https://arxiv.org/abs/1804.03788v2) and published version remove this claim. I checked those passages independently after sealing. Smooth perturbation of a nonsmooth peak does not put the full datum in the invoked smooth space, and qualitative orbital stability does not supply a fixed proportional bound. These are audit deductions; no author motive or official withdrawal is inferred. The current candidate uses a direct corner-compatible flow and a fixed threshold, and does not reuse either unsupported step. Model labels, query histories, old review independence, runtime/duplicate search claims and dates in original metadata are historical attestations, not facts newly certified by this family.

[The 2025 related paper](https://arxiv.org/abs/2503.15071) compares (v_t+vv_x)_x=v to its Hunter–Saxton-related equation (2cη_t−c²η_x+2ηη_x)_x=η+(η_x)². The extra squared-gradient term materially changes the model. Its gradient-instability theorem is credited methodology, not a certificate for this candidate.

The recorded negative literature search cannot establish priority. No stronger source resolution, new paper or immutable result snapshot is warranted by this family alone.

## Entire original package and code inspection

The immutable assigned-head inventory contains 16 attempt files. The full exact diff adds those 16 files and changes only the target QUEUE row. `original_blob_manifest.json` records all original Git blob IDs, SHA256 values, byte counts and the exact diff hash. Original files live in `ignoredtmp/source_snapshot`; replays live in `ignoredtmp/replays`. No closed-original byte was changed.

| Original file | Bytes | Audit outcome |
| --- | ---: | --- |
| `CANDIDATE.md` | 12805 | Universal derivation independently reconstructed; candidate unchanged. |
| `README.md` | 2285 | Scoped W1,infinity partial theorem and 20/135 finite checks accurately distinguished. |
| `RESEARCH_LOG.md` | 3939 | 1/5 history and completion estimates preserved as attestations; no new substantive attempt. |
| `SOURCE_AUDIT.md` | 5905 | OWR, published linear/spectral papers, v1/v2 and different 2025 model independently checked. |
| `check_identities.py` | 2254 | Complete code read; 20-check unchanged isolated replay. |
| `check_results.json` | 909 | Matches fresh submitted replay exactly. |
| `independent_review/REVIEW.md` | 11550 | Read only after early seal; claims compared individually against universal proof. |
| `independent_review/independent_checks.py` | 4009 | Complete code read; 135 assertions unchanged isolated replay. |
| `independent_review/independent_results.json` | 1252 | Matches fresh review replay including script hash exactly. |
| `independent_review/submitted_check_identities.py` | 2254 | Identical blob to submitted verifier; unchanged isolated replay. |
| `independent_review/submitted_results.json` | 909 | Matches fresh archived-submission replay exactly. |
| `independent_review/verdict.json` | 1016 | Scoped PASS and exclusions coherent; provenance/model labels are historical attestations. |
| `provenance.json` | 1448 | Candidate/source hashes correct; shared_queue_modified is historical stage scope, see caveat. |
| `readiness.json` | 1183 | Scope and 1/5 budget consistent; current novelty/duplicate history not externally certified. |
| `source_record.json` | 3984 | Literal curated target agrees with primary OWR model and profile. |
| `turns.json` | 395 | limit=5, used=1 and original_target_outcome=partial; audit does not increment proof ledger. |
| `QUEUE.md` | 369619 | Exactly one target row changed: queued 0/5 to unsolved 1/5; source remains unresolved. |

`provenance.json` retains `shared_queue_modified=false`, while the final separate commit changes the target QUEUE row. The log and history show this refers to the proof-author stage before the queue bookkeeping commit; as a timeless exact-head statement it is ambiguous. This is a nonblocking provenance caveat, not a theorem defect, and original bytes remain preserved.

`turns.json` still records limit five, used one, original outcome partial. Its 1/5 accounting agrees with the log and final queue. This audit is verification only and creates no new substantive attempt.

## Reproducibility and final disposition

`/usr/bin/python3` is Python 3.9.6 with existing SymPy 1.14.0 at `/Users/alec/Library/Python/3.9/lib/python/site-packages/sympy`. No dependency was installed. The submitted verifier, archived submitted verifier and old independent verifier were copied unchanged into isolated ignoredtmp folders; script SHA256 stayed unchanged before/after. Their parsed fresh receipts match the original JSON exactly: 20, 20 and 135 assertions respectively. The two 20-count scripts are byte-identical and are not independent evidence.

New `adversarial_checks.py` passed 66 exact assertions, including six deliberate false substitutes. It tests reference-crest traversal in both directions, one-sided tangency, entry/exit from dwell, representative independence during dwell, sharp primitive kernel normalization, retained moving-corner forcing, generic support exponents, fixed-threshold scale controls, a distinct quartic cutoff proxy and explicit mean bump, one-sided neighborhood excess, and weaker-norm countercontrols. The branch/path examples are finite chain-rule controls rather than PDE trajectories. The cutoff/bump proxies are C¹ diagnostics rather than the fixed C∞ objects used by the universal theorem.

Six original primary PDFs were independently fetched and extracted read-only, with URL/UTC/header/PDF/text hashes in `source_receipts.json`; downloads remain in ignoredtmp. OWR web screenshot attempts returned Internal Error; the original source PDF and its text were retrieved and checked. No numerical evidence is promoted beyond its scope.

No required mathematical revision remains in this family. The strongest independently checked result is the stated W^{1,∞} orbital departure for the constructed local single-corner characteristic class, before any gradient breakdown. The exact remaining gap is a specified weaker-norm/global-solution nonlinear result and independently established priority. Completion estimate: 100% of this assigned audit family; broader research discovery remains partial/unknown and is not upgraded.
