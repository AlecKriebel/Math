# Stationary SIS virulence thresholds: source recovery and five-route investigation

Problem: 30003676 / OWR-15962-002. Investigation date: 2026-10-05.

**Outcome: NO RESOLUTION of the general conjecture.** The retained results below are proved restricted-case results, reductions, and counterexamples to proposed shortcuts. No novelty claim is made for them. In particular, neither the spectral obstruction nor the abstract monotone example is a counterexample to Aldous's conjecture.

## 1. Exact target and interpretation

The primary report is David Aldous, “Epidemics on general networks: a conjecture,” in *Network Models: Structure and Function*, Oberwolfach Report 57/2017, printed p. 3435, DOI https://doi.org/10.4171/OWR/2017/57. For a finite connected weighted graph, an infected vertex v recovers at rate μ_v, while a susceptible v becomes infected at rate

    ε + θ Σ_{y infected} w_vy.

Let X^(n)_{θ,ε} be the number infected under the stationary law on an n-vertex network. The stated premise is that some fixed 0 < θ_* < θ^* < ∞ satisfy, for every ε_n ↓ 0 sufficiently slowly,

    X^(n)_{θ_*,ε_n}/n → 0 in probability,
    X^(n)_{θ^*,ε_n}/n is bounded away from 0 in probability.

The proposed conclusion is the existence of deterministic θ_n ∈ [θ_*,θ^*] such that the corresponding two assertions hold at θ_n−δ and θ_n+δ for each fixed δ>0 (where the lower parameter is in its positive domain). The report explicitly leaves room for additional weak assumptions. It does not specify a universal numerical meaning of “sufficiently slowly.”

Aldous's 2017 slides define “bounded away from zero in probability” as

    lim_{a↓0} limsup_n P(Y_n ≤ a) = 0.

This is stronger than liminf E[Y_n]>0, and weaker than demanding one fixed a>0 with P(Y_n≥a)→1. His April 2018 slides repeat this conjecture (slide 24; PDF index 23), and explicitly describe the underlying networks as undirected. No homogeneity, bounded degree, fixed recovery normalization, or random-graph model is imposed in the primary statement. We use finite nonnegative edge weights and rates; positive recovery is an explicit hypothesis of the lemmas below, not a recovered uniform bound from the source.

Biologically, θ scales contact transmission, μ_v is individual recovery, and ε is an external infection rate **at each susceptible vertex**. Recovery returns to susceptibility. “Virulence” here is this transmission multiplier, not disease severity or mortality. The question concerns a stochastic stationary prevalence as both population size and external seeding change. An ODE equilibrium, a finite-time outbreak, and an ε=0 quasistationary law are different objects.

## 2. Source and prior-attempt checks

The catalog page https://www.unsolvedmath.com/problems/30003676 was attempted first. The web reader could not access it; a direct retrieval returned HTTP 403. No route was used to circumvent that denial. The official EMS report and author-hosted slides were successfully retrieved. Printed p. 3435 was rendered and visually inspected to resolve subscripts/superscripts and parameter quantifiers.

The author's current open-problem index still links this topic to the 2018 slides. The index itself warns that updates may be incomplete. This supports a precisely bounded report of the author's public listing, not a certification of worldwide open status.

Later literature checked includes Cantwell and Moore, *Threshold and quasistationary distribution for the susceptible-infectious-susceptible model on networks*, Phys. Rev. E 113, 064305 (12 June 2026), https://doi.org/10.1103/385j-2f29. Its publisher abstract describes an improved pair approximation and quasistationary computations. Those advertised results do not establish the present arbitrary-network stationary-with-immigration conjecture. Targeted title/author/model searches and the author's publication list did not locate a verified full resolution. This search is not exhaustive.

In AlecKriebel/Math at inspected commit 73300d9223ca6175983c78cb2370f99ffdd4b59c, the directory `unsolved_math_prioritization/attempts` returned 62 entries and no matching ID/name; the exact `30003676` subdirectory returned 404. Bounded code, pull-request, and commit searches also returned no exact ID match. These are absence findings for the inspected locations, not proof that no earlier work exists. A search of prior user context returned unrelated problem work and no usable exact-topic attempt. That unrelated material is not included here.

## 3. Five approaches and their precise outcomes

1. **Attractive coupling and linear drift.** Proved stationary monotonicity and a positive-vector subcritical certificate. A rational resolvent bound is available when the relevant nonnegative matrix has spectral radius below one. This does not prove the opposite direction; a loss of linear stability of a closure is not a stochastic onset theorem.
2. **Exact complete-graph stationary asymptotics.** Proved X_N/N → (1−μ/β)_+ for weights β/(θN), with ε_N→0 and log(1/ε_N)=o(N). Included the critical case, an exact finite-N formula, and an exponentially-fast-seeding negative control. This completely handles this restricted family, but does not handle arbitrary networks.
3. **Heterogeneous connected construction.** Proved that a connected sequence satisfying the target endpoint premise can have true prevalence onset θ=2 while the linearized inverse spectral threshold converges to 1. This is a counterexample to equating the two thresholds, not to existence of a threshold.
4. **Graphical duality and susceptibility.** Proved an exact Laplace-transform representation of all susceptible-set probabilities and a finite linear system for checking it. It exposes the missing joint-cluster/concentration information; it does not supply that information in arbitrary graph sequences.
5. **Abstract monotonicity/compactness test.** Gave a monotone Bernoulli family with the two endpoint regimes and no deterministic sharp separating sequence. It demonstrates that monotonicity plus the endpoint premise alone, without the contact-process structure, is insufficient. It is explicitly not an SIS realization.

Complete proofs are in PROOFS.md. Each route was stopped at its stated gap rather than treating a reformulation as a proof. No sixth mathematical approach is claimed.

## 4. Verification and limits

Run `python3 verify.py`. Only the Python standard library is used. The verifier constructs full finite-state generators with Fraction arithmetic, solves stationary equations independently of the birth-death formula, checks every susceptible subset against the dual killed-generator system, checks dimer formulas, drift certificates, and complete-graph lumping. It also verifies finite witnesses of the heterogeneous construction and executes deliberately wrong-formula negative controls.

These checks validate finite identities and detect specified implementation mistakes. They do not machine-prove the asymptotic arguments or settle the unrestricted conjecture. The mathematical proofs are the authority for infinite sequences.

The safe package contains authored text, exact code/output, and source/verification metadata. It contains no downloaded PDFs, source extracts, raw catalog dataset, or private correspondence. MANIFEST.json hashes every payload file other than itself; its own hash can be recorded separately when freezing/auditing.

## 5. Remaining gap

A solution needs a genuinely graph-uniform argument that turns the endpoint assumptions into the two probability regimes at a deterministic separating sequence, with one carefully quantified sufficiently-slow immigration condition. Neither an eigenvalue crossing, a positive expected density, nor single-vertex dual survival supplies that assertion. The present work leaves this gap open, and also does not select or justify the additional weak assumptions contemplated by the original author.
