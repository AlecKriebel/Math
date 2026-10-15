# Fresh independent full manuscript and publication-package audit 03

Problem 30004630 / OWR-4990378-001; native PR #248. Audit date: 2026-10-14 UTC. Reviewer: new independent adversary 03. This is a complete reconstruction and falsification audit of the revised six-page manuscript and actual publication archive, followed by a static audit of the planned current-source presentation script. It is not merely a review of the four editorial changes.

## Verdict and strongest checked result

**PASS for the stated mathematical theorem, source fidelity, current publication payload and portable scientific reproduction. Mandatory issues: NONE.** A historical intermediate-report input pin was resolved by independently verified exact reconstruction, qualified separately below. It does not enter the proof or scientific runner. The priority conclusion remains bounded: I found no authenticated earlier covering construction in the inspected material, and do not certify worldwide absence.

For a sufficiently small positive constant Hilbert cap on controls of the actual zero-data defocusing quintic Dirichlet wave on the three-dimensional unit ball, the target pi times the normalized radial eigenfunction gives a unique global optimizer at zero. The ordinary source critical cone is exactly zero and strict positivity on its nonzero elements is vacuous. Feasible pulses converge in L-infinity and have objective gap o(the squared control-L2 norm). Global optimizers exist for every terminal H target and every fixed finite nonnegative optional H-minus-one velocity weight. On the positive radial target ray, **every** global optimizer has control-L2 norm divided by target displacement tending to infinity. Local L1 quadratic growth and arbitrary-target uniform upper estimates survive; the radial L2 exponent bracket is not asserted sharp.

This is a negative answer to retaining the ordinary-cone strict-positivity implication unchanged after deleting beta2>0. It does not refute the published positive-regularization theorem, a strengthened-cone theorem, an alternate growth metric, or all unregularized control-growth results.

## Independence, custody and exact candidate

I read the revised TeX and reconstructed its proof before reading prior proof/priority verdicts. INITIAL_INDEPENDENT_RECONSTRUCTION.md was saved at UTC 2026-10-14T05:12:39Z and has remained unchanged. It records the initial 35% checkpoint, the deductions then made and the source/package questions still open. The assignment supplied older reported results; I treated them as hypotheses, not acceptance evidence. Primary-source and older priority material were read only after this checkpoint. The first and second fresh manuscript reports were consulted only near the end, after my own mathematical reconstruction and independent archive execution.

All my writes are confined to fresh_review_03/. I did not modify the manuscript, archive, metadata, deposit, original submission, Git refs/index/checkouts, or any publisher/tracker state. No external individual was contacted. Read-only web access authenticated official source/version metadata. The read-only PDF skill was used to render and inspect the manuscript; no PDF authoring occurred.

The five current candidate pins, checked from their actual bytes, are:

| File | SHA256 |
|---|---|
| critical_wave_growth.tex | bf4e13509ee738d1c5f73555e322ce77b9f2041b2306e4f80dfc588c98289584 |
| output/pdf/critical_wave_growth.pdf | a68d8d47dcf625f9ab8818924071200bff2b2280d67665e1e67dd7b83effe988 |
| output/critical_wave_verification.zip | 1da933750640177045808de748dd7f5732c33277377285b688a411f9f89771a0 |
| metadata.json | c7cb0d1e088a4caf3b584d4b8a0f8bfadea6bf85132eb3f6b4972ee58b02fb7b |
| deposit.json | ff932191523d1dcbac9250cd5a4b8f28b1ec1e0de5b654283f33b3850323ab11 |

## Independent mathematical verification

### Full-space nonlinear state and differentiability

The state space must contain compatible pairs: the continuous H position velocity is the distributional derivative of the continuous H0^1 position. With this compatibility and zero data the sum energy/Strichartz norm defines a closed Banach subspace. The linear zero-data wave map L maps L1(H) into this space. The cited Lemma 2.9 supplies this estimate on the smooth bounded ball; the underlying boundary Strichartz range includes (time,space,regularity)=(4,12,1) in dimension three.

The quintic is a bounded five-linear polynomial. Assign four factors to L4(L12) and one factor to L-infinity(L6): temporal reciprocal exponents sum to one and spatial reciprocal exponents sum to one half. Each factor is controlled by the compatible state norm, so this also proves the mixed-factor derivative estimates, rather than merely a formal scalar Taylor formula. The fixed point y=L(u-y^5) preserves a radius-2KA ball and is a contraction for A=norm(u)_1 below a positive threshold. Thus norm(y)_Y<=EA and norm(y-Lu)_Y<=RA^5. The entire admissible set lies in this regime because T=1 and A<=rho. This is a full-space argument: e^5 is not in span(e), and no nonlinear spatial truncation is used.

The residual y+L(y^5)-Lu maps the compatible zero-data state space to itself and has identity derivative at zero. Local implicit-function theory therefore gives a smooth map, S'(0)=L and S''(0)=0, independently of the printed source's arbitrary-pair codomain step. Endpoint maps are bounded, including the velocity map into H-minus-one.

The smooth part of the objective is genuinely C2. For the mixed-space quartic, at a nonzero spatial function v in L12 the second derivative of norm(v)_12^4 has the two terms 44 norm(v)_12^(-8) integral |v|^10 z1 z2 and -32 norm(v)_12^(-20)(integral |v|^10 v z1)(integral |v|^10 v z2). Its absolute value is at most 76 norm(v)_12^2 norm(z1)_12 norm(z2)_12; at v=0 its second derivative is zero. Integrating and using time Hölder proves boundedness and continuity on L4(L12), including zero. Composition with S proves the required C2 property. In particular, the state quartic contributes neither first nor second variation at zero.

### Actual global minimum, constants and cap boundaries

The eigenfunction normalization follows directly from spherical volume: 4pi/(2pi) times integral_0^1 sin^2(pi r) dr equals one. The center is a removable smooth radial value and the trace at r=1 is zero. The linear terminal kernel is sin(pi(1-t))/pi=sin(pi t)/pi.

For arbitrary feasible vector-valued u, let f=norm(u(t)), A=integral f and r=norm(u)_2. The cap implies 0<=A<=rho, A<=r and r^2<=rho A. Pairing with e and using sin(pi t)>=0 gives the lower bound integral(1-sin(pi t))f-C0 A^5 after dropping only nonnegative square, quartic and velocity terms. This estimate is valid for every spatial direction of u, not just radial inputs.

The centered saturated density with mass A has half-width b=A/(2rho). The signed product ((t-1/2)^2-b^2)(f-f*) is nonnegative on the interval and its complement, yielding second moment >=A^3/(12rho^2). The trigonometric weight is >=2(t-1/2)^2 on the full time interval. Consequently the objective gap is >=A^3/(6rho^2)-C0 A^5. Since A<=rho, choosing C0rho^4<=1/12 leaves A^3/(12rho^2). A=0 and A=rho are included; equality of controls is understood almost everywhere. This proves actual global optimality and uniqueness, and hence the inherited source local-optimality premise in either topology. The constants and small positive cap are independent of nu. The paper claims no numerical value for an unknown wave constant.

### Ordinary cone, dense tangents and the pulse

In the beta2=0 natural L1(H) space, and separately in L2(H), truncate any direction by its pointwise Hilbert norm. Each bounded truncation becomes feasible after sufficiently small scaling and converges in the chosen norm. Thus the closed tangent cone is the whole space. Pointwise slack does not assert norm interiority; the L2 interior is empty, as arbitrarily small L2 spikes can exceed any fixed cap.

The adjoint is -sin(pi t)e, its cancelling sparse subgradient is sin(pi t)e with norm<=1, and the multiplier is zero. The whole-cost directional derivative is >=integral(1-sin(pi t))norm(v(t)), strictly positive for every nonzero equivalence class, since the sole zero-weight time has measure zero. The source's ordinary cone is therefore {0}. Its substitute sparse j'' is defined to be zero at the zero control; it is not a classical second derivative of a norm. Vacuity is explicit throughout the paper and metadata.

For u_h=h e on |t-1/2|<h, feasibility holds for 0<h<min(rho,1/2), the L-infinity norm is h, A=2h^2, r^2=2h^3, the terminal linear position is 2h sin(pi h)e/pi^2 and the terminal linear velocity cancels exactly by symmetry. The complete linear tracking-plus-sparse gap has leading coefficient pi^2/3+2/pi^2 times h^4 and remainder O(h^6). The actual nonlinear position error is O(h^10), the state quartic is O(h^8), and the velocity cost is O(nu h^20). The latter estimates are for fixed finite nu; they are harmless for nu=0. Thus the asserted full nonlinear asymptotic, with positive leading coefficient, is valid. Dividing by 2h^3 disproves positive strong control-L2 growth in both the OWR L2 neighborhood and the source preprint's smaller L-infinity neighborhood.

The normalized pulses are weakly null in L2(H): their pairing with any test is bounded by the test norm on the shrinking support. The paper's displayed normalized expression equals (pi^2/6+1/pi^2)h+O(h^3), tending to zero. This correctly diagnoses failure of weak-null NDC and does not turn vacuous exact-cone positivity into coercivity.

### All-target existence and identification of the actual mild state

The cap defines a closed convex bounded subset of the Hilbert control space, hence a weakly compact set. Every minimizing sequence has the same uniform small-input state bound independently of the target. Bounded H0^1 positions and bounded H velocities, with time equicontinuity, give strong compactness in C(H). Moreover y_tt=Delta y-y^5+u is bounded in L-infinity(H-minus-one): here the control cap supplies L-infinity(H), and the energy bound supplies y^5 in L-infinity(L6/5), embedded in H-minus-one. Compact embedding H into H-minus-one and this derivative bound give strong compactness of velocities in C(H-minus-one). This avoids the inadequate inference from a bare L1 acceleration bound to uniform time equicontinuity.

After a subsequence, almost everywhere convergence and bounded L6/5 quintics identify the weak nonlinear limit. The same limit retains the weak energy and reflexive L4(L12) bounds, hence its quintic is in L1(H) by the mixed interpolation already proved. Both initial traces pass under the strong convergences. Subtract the linear zero-data Duhamel solution forced by the limiting u-y^5; every coefficient in a complete Dirichlet eigenbasis solves the homogeneous scalar wave with zero data and is zero. Thus the limit is the actual energy/Strichartz mild solution, with its proper traces, not merely a weak state. The endpoint costs are continuous in the two strong topologies and the sparse and quartic norms are weakly lower semicontinuous. This proves global optimizer existence for every target d in H and every finite nu>=0.

### Perturbation quantifiers and surviving growth

The fixed-amplitude trial a=rho/2 with half-width pi epsilon/(2a) is feasible for sufficiently small positive epsilon. Its mass is pi epsilon, its linear terminal position is epsilon e+O(epsilon^3), and its linear terminal velocity is zero. The objective gap relative to zero at target (pi+epsilon)e is -epsilon^2/2+O(epsilon^3), so it is <=-epsilon^2/4 on a neighborhood that may depend on the fixed nu.

For every feasible u, the lower comparison is -norm(g_epsilon)_2 r-C1 A^5, with g=[(1+epsilon/pi)sin(pi t)-1]_+. The envelope [epsilon/pi-2(t-1/2)^2]_+ is valid, including outside its support. Bounding its height and support gives the manuscript's safe constant 2^(1/4)pi^(-5/4)epsilon^(5/4); direct integration gives a smaller constant, so no sharpness is being smuggled into this estimate. If any optimizer had r<=K epsilon, A<=r would make this lower bound -o(epsilon^2), contradicting the trial. For every fixed K, the exclusion holds for all optimizers below a sufficiently small threshold. It therefore proves the stated limit for every choice of global optimizers, not merely one selected subsequence.

For local L1 growth, x=<e,y(1)> is bounded above by b=A/pi+RA^5. The full tracking square gives gap>=A-pi x+x^2/2; this polynomial is decreasing for x<pi, even if x is negative. Choosing b<=pi/2 licenses the one-sided substitution. Expanding at b and imposing pi R delta^3<=1/(4pi^2) gives gap>=A^2/(4pi^2). No false inequality replacing a one-sided projection bound by an absolute bound is used.

For arbitrary w, global comparison with zero gives gap<=<w,y(1)><=E norm(w) A. The global cubic estimate first enters the local L1 neighborhood uniformly in nu; then A<=4pi^2 E norm(w) and r<=2pi sqrt(rho E) sqrt(norm(w)). Along w=epsilon e, this upper A=O(epsilon), the trial comparison and the bounds on g imply A>=c epsilon and r>=c epsilon^(3/4). All these estimates apply to every global optimizer. The radial lower neighborhood is per fixed finite nu, while the arbitrary-target upper neighborhood and constants are uniform over all finite nonnegative nu. No statement about a varying unbounded weight is inferred. No sharp exponent, pairwise selection, perturbed uniqueness or L-infinity optimizer convergence is claimed.

The target-zero boundary example J>=norm(u)_1>=r^2/rho is also correct and usefully shows that unregularized growth does not universally fail.

## Primary source and priority audit

I directly read the primary OWR contribution on printed pp. 438–440, source arXiv-v1 Lemma 2.9, printed Theorem 4.3 proof, the standing locally-optimal premise on p.24, tangent/cone and substitute derivative definitions on pp.24–26, and the full Theorem 4.17 argument on pp.35–38. The optional velocity term and ordinary-cone implication appear in the OWR contribution; its beta2-zero question follows that implication. The exact source hypothesis and the neighborhood distinction are accurately stated. Official [MFO report metadata](https://publications.mfo.de/handle/mfo/3850) and [arXiv history](https://arxiv.org/abs/1907.02744) authenticate the cited report and original proof version.

At zero, the inspected preprint's derivative into arbitrary continuous energy pairs cannot be onto: a pair (0,tg) with nonzero g is incompatible with being (z,z_t). The manuscript repairs the exact local assertion needed here through the compatible residual. This is not a claim of a defect in the inaccessible final publisher proof. The bibliography expressly names the proof version inspected; current metadata/author versions are not silently substituted for a final-body inspection.

After my independent reconstruction, I read the bounded classical/recent/bridge/attribution records and relevant primary material rather than simply adopting their verdicts. The following distinctions survive falsification:

- The Casas–Tröltzsch 2012 author preprint separates ordinary-cone positivity from weak-null coercivity. The 2015 survey reproduces Dunn's Example 4.16 completely: its exact-cone coercivity coexists with a shrinking pulse that decreases the objective. This verifies the classical method through the reproduction. Dunn's original chapter was not obtained or claimed inspected.
- Casas–Herzog–Wachsmuth 2017 is a semilinear parabolic, scalar-box sparse-control theory. Its positive-quadratic-coefficient theorem and its unregularized extended-cone/state-growth discussions give direct methodological antecedents. Changing the norm grouping does not replace a parabolic state by the nonlinear critical wave or scalar boxes by Hilbert balls. The manuscript's year 2017 is correct for volume 23, despite the earlier source's 2016 wording.
- Herzog–Stadler–Wachsmuth 2012 provides established group-norm and threshold calculus. Christof–Wachsmuth's original arXiv-v1 framework includes the weak-null nondegeneracy condition. These are appropriate credits for the mechanism, not claims of a new abstract obstruction.
- I read Borchard–Wachsmuth's necessary NDC Theorem 2.18 and proof in both original 2023 v1 and published 2024 form, as well as the standing Taylor assumptions and NDC expression. The [official journal record](https://jnsao.episciences.org/articles/14959) distinguishes submission/acceptance/publication dates. The theorem applies after the present wave data, actual optimizer and pulse have been constructed. It does not itself choose a wave instance or establish an earlier existential negative wave construction. Its L2-neighborhood statement alone also needs a restricted-cap localization to refute an L-infinity-neighborhood condition; the direct pulse already proves both.
- D. Wachsmuth and G. Wachsmuth's 2022 L1/measure theorem requires nonzero threshold gradient and O(delta) near-level mass. For sin(pi t), the threshold is a stationary maximum and near-level mass is asymptotic to a constant times sqrt(delta), so those hypotheses fail. Failure of a sufficient condition alone is not a negative theorem, and its scalar functional is not automatically the full Hilbert-valued sparse objective.
- I read the Casas–Mateos corrected author text's actual enlarged-cone/parabolic-state scope, and the Casas–Kunisch 2024 publisher Theorems 4.5 and 4.12: their hypotheses concern an extended cone and linearized-state coercivity, with state-squared growth. The latter uses finite actuators, a parabolic equation and infinite horizon. They are replacement-theory antecedents, not the same strong control-L2 counterexample.
- The inspected Wachsmuth–Walter 2024 v1 has a measure cone, saturated dual points, curvature hypotheses and bounded-Lipschitz growth for linear observation with a Radon penalty. The inspected July 2026 transport paper has fixed positive prior mass, a transport-distance regularizer, lifted measure spaces and potential/NDC assumptions. Their actual conclusions and domains differ from this wave example. The later listed 2026 final Wachsmuth–Walter body was not authenticated; no final/preprint equivalence is asserted.

Earlier coverage would not have to include global uniqueness, radial instability or the L1 extras: a genuine earlier constructive theorem encompassing the optimizer, ordinary strict-cone premise and failed strong control-L2 growth would suffice. No such covering assertion was authenticated in the bounded primary corpus. Conversely, the applicability of old conditional NDC machinery does not date the newly supplied construction to that machinery. The paper credits the old concentration mechanism, calls this a realization, and disclaims worldwide firstness. I endorse that careful scope, not an exhaustive historical novelty certificate.

The priority records explicitly retain inaccessible final/original publisher bodies, deposit/history search failures and distinctions between current retrieval and original chronology. I checked the principal model/theorem mismatches directly; I do not claim independent full-proof certification of every theorem in every adjacent transport, measure or parabolic paper. No outreach was prepared.

## Actual ZIP, original blobs, receipts and metadata

I extracted the actual frozen ZIP into my own isolated directory, checked safe unique relative paths, and verified exactly 113 files and all 112 top-level FILE_MANIFEST pins. The archived manuscript equals the frozen TeX byte for byte. Standalone metadata, deposit.metadata and ZIP metadata are exactly equal as parsed JSON. The title, author ORCID, preprint type, 2026-10-14 date, version 1.0, CC BY 4.0, AI-use disclosure and review/scope limitations agree with the manuscript. The two planned upload paths are the actual frozen PDF and ZIP. The package license excludes third-party whole reading copies.

I used the supplied existing Python 3.14.6, SymPy 1.14.0, mpmath 1.3.0 environment without installing dependencies or cloning anything. Every checker was copied from the actual archive into its own directory and executed independently; the portable verify_all.py was then executed from a separate directory. Each complete parsed receipt agrees with its reference after removing only top-level informational utc/python fields. Scientific fields, dependency versions, counts, values, diagnostics and limitations match. The emitted bridge receipt's hash also matches its stdout hash. I read all seven scientific scripts, not merely their PASS labels.

| Checkset | Exact assertions | Noncertified diagnostics |
|---|---:|---:|
| author3937 | 3937 | 0 |
| original_independent1385 | 1385 | 0 |
| source17 | 17 | 0 |
| variational215 | 210 | 5 |
| addendum21 | 21 | 0 |
| classical13 | 13 | 0 |
| fresh_bridge20 | 20 | 0 |
| Total | **5603** | **5** |

These are exact symbolic/rational finite assertions and five noncertified high-precision diagnostics. They check relevant eigenmode, pulse, moment, threshold, exponent and weaker-norm algebra. They do not solve a discretized nonlinear PDE, compute a certified wave constant, or prove historical novelty. Those boundaries are accurately disclosed in the package and paper.

All 19 original submission files match both the actual archive and read-only Git blobs at e9c5d10978764db2cf25fa7d49cf4bd14a82d604, with individual native blob OIDs and SHA256 recorded. All current public authored manifest bindings and all primary source byte pins are sound. The four relocated historical_snapshot_01 entries resolve to exactly unchanged parent-family files, as the README now explains. My first nested-schema pass verified 294 objects; the broader final scan verifies **all 375 SHA256 objects** across alternate filename/path schemas and digest-only receipts. One intermediate-report input is verified against the separately reconstructed exact historical object described below, with that method explicitly qualified. It is not treated as the current report or as a recovered native file.

PACKAGE_REPRODUCTION.json preserves the complete seven receipts and original Git comparisons. ALL_NESTED_PIN_REPRODUCTION.json records the broader pin inventory. A later retry encountered a shared-filesystem ENOSPC failure after deleting only my own duplicate extracted directory; the already completed execution receipts remained preserved. I removed only my own rendered PNGs after visually inspecting them; no frozen candidate or authored proof was touched. No scientific replay result relies on the failed retry.

## Six-page visual audit

I rendered the exact current PDF with Poppler at 110 dpi and visually inspected every page at full-page resolution. Page 1 has clean title/author/date, readable abstract and state/objective/mode formulas. Page 2 contains the complete theorem, scope/priority paragraph and small-input lemma. Page 3 contains the contraction proof and global comparison; the transition to the cone discussion is natural. Page 4 shows the exact pulse and NDC display and the compactness proof; its continuation on page 5 is readable. Page 5 shows the radial trial, dual estimate, corollary and full proof. Page 6 has explicit limitations, review/license disclosure and all nine references, with readable DOI links. I found no clipping, overlap, missing glyph, broken equation, unresolved reference or unreadable type. PDF information confirms six letter-size pages, 88,702 bytes, and no encryption or JavaScript.

## Planned current-source presentation script

I statically inspected PRE/prepare_current_source_packet.py in full and parsed its syntax without executing it. Its exact reviewed SHA256 is **0f76afa3fc623b57c25062ffcf181e484c203923d0afcf979d1304d52acdba8e**, 16,267 bytes. SOURCE_PLAN_REVIEW.json binds this script and records the assertions and four unique original-text replacement matches.

The script is guarded by mathematical PASS and at least three clean fresh full reviews, then verified publication and tracker readback, equal DOI URLs and an absent destination. Its future-tense execution plan creates a distinct current packet from the preserved original. It explicitly narrows the lower target theorem to positive radial perturbations, records uniform arbitrary-target upper bounds separately from per-fixed-nu lower neighborhoods, adds the dense-truncation tangent proof and actual Duhamel/eigenbasis mild-limit identification, and disclaims selection/uniqueness/sharpness claims. Its D. Wachsmuth–G. Wachsmuth 2022 attribution is correct, and its derivative/codomain qualification is specifically at zero in the inspected preprint. The publication review language is internal AI-assisted and unrefereed.

Current top-level manifests are regenerated; the original native head/archive and historical review byte scope are explicitly identified. The unchanged checker, original receipt, source manifest and original independent-review bytes are protected by equality assertions. The script does not claim old manifests bind the revised presentation. I found no mandatory mathematical, scope, attribution or historical/current separation issue. This static PASS does not certify future external publication/tracker facts, and the script remains dormant for the parent to execute after factual readback.

## Mandatory issues and optional suggestions

**Mandatory issues: NONE** for the mathematical theorem, reviewed current five-file payload, scientific reproduction or corrected planned script.

The initial broad scan found an older classical REPORT.md input recorded in audits/priority_attribution_falsifier_01/INPUT_PINS.json as 10,340 bytes with SHA256 7091d12b2ed3105451420fc39416d4b965ed3aff7600c2e685e45964b00d37e7; the current 10,756-byte report has its correct current authored-manifest hash. No pre-existing old file was located in the initial-review files, PRE history, local Git history or closed checkpoint tree-content records. The original reviewer subsequently provided historical_recovery/REPORT_as_read_7091d12b.md and a reproducible reverse-edit script in its own separate folder. I independently parsed the five literal old/new transformations, verified each current paragraph occurred once, applied them in memory and obtained exactly the historical length and SHA256, byte-identical to the reconstructed object. The old input binding is therefore resolved against an exact deterministic reconstruction authenticated by the prior digest. This is **not** represented as retrieval of a native/pre-existing old file, nor endorsement of the old provisional priority verdict, which was later corrected. HISTORICAL_RECOVERY_REPLAY.json records this independent readback. Separate recovery records preserve this qualification without rebuilding the frozen scientific ZIP.

Optional suggestions: none requiring a manuscript or payload change. Keep the reconstructed-object qualification with the separate historical recovery records. The final delta addendum's bookkeeping is not used as a proof premise here; my direct comparison establishes the actual current archive independently.

No mathematical edit, new source claim, new exponent or additional numerical PDE experiment is requested. The exact remaining research gaps are the explicitly excluded replacement-theory/sharp-rate questions and bounded historical access limits, not unsupported steps in the proved theorem.

Completion for this assigned full audit: 100%, subject to the stated bounded source/custody limitations. Verdict applies only to the five frozen candidate hashes and the separately pinned planned script. Final public authored artifacts are bound by FINAL_AUDIT_MANIFEST.json; own readings, renders and execution workspaces are excluded from that authored manifest.
