# Root mathematical verification of PR883

Written 2026-10-15, during the initial mathematical gate (approximately 20% of the complete verification/publication decision). Original proof-search effort remains 1/5. This document does not decide priority or authorize promotion of unreviewed paper bytes.

## Exact target, reading order, and strongest verified result

The native complete target is PID9900008/AMR-098-0008, corresponding to Thorisson's *Some Open Probability Problems*, Problem4.1, printed pp5–6. It asks whether a diffuse pair invariant under every measurable original-pair preserving allocation must be mass-stationary. Its setup allows arbitrary locally compact second countable Abelian groups and arbitrary measurable pair actions. A counterexample on R² with constant X suffices.

Before the authored proof and inherited mathematical audits, I froze `ROOT_INDEPENDENT_RECONSTRUCTION.md` after reading the exact target and primary §4, together with the2015 preliminaries/introduction. The initial QUEUE finding/publication labels had already exposed the singular-R²/background-free/product-lift hints; this was disclosed rather than called blind discovery. I then read in full the2009 flow/allocation/mass-stationarity definitions and Example7.1/Problems7.3–7.7, the2015 §8 Proposition1 and its proof/Theorem8, and the complete authored proof. Only afterward did I read the old audit reports and complete native prior literature report. They supply historical comparison, not proof authority. The original note's two operative pages were also visually checked from the freshly retrieved, hash-matched primary PDF.

The candidate's periodic example is mathematically valid under the exact primary pointwise-covariant allocation definition. The verification below treats arbitrary measurable allocations, rather than inferring universal validity from finite tests. Current credit already correctly attributes the established product-lift and unequal-weight mechanisms. Novelty and present literature status remain a separate gate.

## Model and observed state

Put ν=Σ(n∈Z)δ_n+2Σ(n∈Z)δ_(n+1/2), μ=λ₁⊗ν, Ω=R/Z, θ_(a,b)u=u+b modulo1, ξ(u)=θ_(0,u)μ, and Q=δ₀. Here θ_tη(B)=η(B+t). Let X be constant with trivial action. This is the authored periodic model, not the nonperiodic two-line illustration in my initial memo.

Every compact set is contained in a bounded rectangle meeting only finitely many support lines, of finite horizontal length. Thus μ is nonzero, locally finite and Radon. It is atomless: for any positive finite mass on a countable sum of line-length measures, one can split a positive horizontal slice. Infinite total mass is allowed. The root is supported. The action is jointly continuous and ξ is flow-adapted. For each compactly supported continuous f, integrating horizontally makes ∫f dξ(u) a locally finite continuous sum in u. The phase map is injective because density1 and density2 line families are distinct. Compactness of Ω makes it a Borel isomorphism onto its compact canonical orbit. Consequently σ(ξ)=B(Ω); no extra unobserved coordinate or stationary randomness is available.

The stabilizer is exactly R×Z. In particular a displacement depending on the original pair cannot extract a horizontal coordinate to split a line into unequal fractions. This is admissible in both cited source formulations: neither assumes a free action, positive density, full support, or absence of invariant directions. Flow adaptation does not assert stationarity of Q.

## Universal allocation argument

For any primary-defined measurable displacement π on Ω, τ_u(s)=s+π(θ_su). Conversely, every pointwise-covariant allocation has this form by setting π(u)=τ_u(0). Write π(0)=(a₀,b₀) and π(1/2)=(a₁,b₁). At u=0 the formula forces, for every real x and integer n,

    τ₀(x,n)=(x+a₀,n+b₀),
    τ₀(x,n+1/2)=(x+a₁,n+1/2+b₁).

The pushforward along each line is a translation of Lebesgue measure. Therefore preservation at u=0 implies equality of the corresponding two periodic vertical measures. Testing on the actual finite segments [0,1)×{r}, 0≤r<1, gives

    1{[b₀]=r}+2·1{[1/2+b₁]=r}=1{r=0}+2·1{r=1/2}.

This does not push the entire infinite measure onto a compact quotient. Positivity excludes off-support target residues; collision would put mass3 at one residue, and a swap would reverse the unequal masses. Hence b₀,b₁ are integers. Within each source family the integer line index can only be translated by a fixed displacement; two light source lines cannot be combined at a target. Injectivity was never assumed. Arbitrary off-support behavior remains permitted.

It follows that π(0)∈R×Z, so θ_{π(0)}0=0. Every preserving allocation leaves the complete observed pair law fixed. Only preservation at the sole Q-supported state was used; thus state-almost-sure preservation cannot escape the proof. Identity and fixed stabilizer translations give actual preserving maps, so the premise is nonvacuous. Each admissible original-state displacement on the orbit can also be extended measurably by zero off that invariant compact orbit in the full canonical measure space. Conversely any full-space map restricts to this class.

Although the root singleton has zero μ-mass, its image cannot be reassigned independently under pointwise covariance: changing π(0) moves every point of every light line, including positive-mass unit segments. A different notion specifying spatial equivalence classes without a covariant root representative is not the primary definition.

## Exact failure of joint mass-stationarity

Take C=[0,1)² and independent U uniform C. Every translated unit vertical interval contains exactly one representative of each line family; half-open endpoint conventions handle the boundaries as well. Both horizontal lengths equal1, so μ(C−U)=3. A sample V from its normalized μ-restriction lies on a heavy line with conditional probability2/3. Horizontal shift is immaterial; its phase after rooting is1/2 on that event.

The evaluation H(η)=η([0,1)×{0}) is measurable in the canonical evaluation σ-field. Initially H(ξ)=1 surely; after the required resampling H(θ_Vξ)=2 with probability2/3. Thus even the first marginal differs, which is sufficient to refute the full required joint law (θ_Vξ,U+V)=(ξ,U) in distribution. This uses an admissible relatively compact Borel C with positive Haar measure and Haar-null boundary, never a zero-mass normalization or merely a guessed Palm law.

As an independent consistency check, uniform phase P is stationary and has intensity3. Its Campbell integral over a unit square is f(0)+2f(1/2), giving normalized Palm weights1/3 and2/3. Conversely any probability law on the two supported root phases satisfying the mass-stationarity identity for this C must have these weights: the resampling row is the same (1/3,2/3) from either phase. This necessity is exact, independent of finite sampling. Sufficiency of the Palm mixture can be checked directly or by the established Palm theorem, but is unnecessary to the counterexample.

The nonperiodic illustration in the initial memo is another exact diagnostic: δ₀⊗λ₁+2δ₁⊗λ₁ forces each of two complete parallel source lines to translate into itself, while C=[0,2]×[0,1] samples the other rooted type with probability1/3. It supports the obstruction mechanism; it is not substituted for the authored periodic proof or promoted as a new result.

## Sharp limits, antecedents, and reproduction

The source-domain implication is refuted, including the possibility of constant X and singular diffuse ξ. The example does not refute a one-dimensional result, a positive-density theorem, a no-invariant-direction/free-action variant, or an independent-stationary-background test. It fails an explicit stronger Markov premise: at rooted phase0 send mass vertically by1/2; at phase1/2 send half by−1/2 and retain half; elsewhere retain mass. This kernel is measurable and covariant, preserves both line-family masses at every phase, and sends the light root to the heavy type. Hence no all-Markov counterexample is claimed.

Last–Thorisson2009 Example7.1 already provides the unequal-atomic-weight obstruction. Their2015v2 §8 Proposition1 explicitly proves preservation/reflection of mass-stationarity after adjoining a Lebesgue factor; its full short proof was read. Their Theorem8 still uses stationary independent backgrounds. The periodic lift is established machinery and must not be described as novel. Their2023 §8 parallel-line obstruction concerns balancing two different diffuse measures. Khezeli–Mellick2024v2 Theorems1.1–1.2 concern factor point processes/balancing under hypotheses this model violates. Those precise bodies and definitions were read as boundary checks, not treated as an exhaustive priority audit. The original prior report's numbering, one-dimensional attribution and broad positive-density claim require correction; the exact target itself matches the primary question.

Both complete original Python code bodies were inspected before execution. `ROOT_ORIGINAL_REPLAY.json` records a fresh externally pinned private copy with a path containing spaces, normal and optimized isolated outer runs, eight author child runs per outer run, and five designated wrapper mutations per outer run. The exact26files/211771bytes are unchanged. Those arithmetic/manifest checks are supplementary; no universal measurable claim or novelty follows from them. The omitted historical executable archive is not represented as replayed. Self-editable internal manifests do not authenticate themselves, and no hostile concurrent-filesystem/sandbox guarantee is asserted.

Primary URLs: [Thorisson original note](https://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf), [Last–Thorisson2009](https://arxiv.org/abs/0906.2062), [Last–Thorisson2015v2](https://arxiv.org/abs/1405.7566v2), [Last–Thorisson transportation](https://arxiv.org/abs/2112.13053), [Khezeli–Mellickv2](https://arxiv.org/abs/2303.05137v2). Primary binaries/extracts and native corpora are private, not distributed. Historical references to other repository PRs were not followed in this process.

No mathematical repair is presently indicated. Independent families, artifact audit and the deep bounded priority gate must be integrated explicitly before preparing/promoting a final paper; two new whole-package adversaries still remain mandatory afterward. All work is extensively AI-assisted, unrefereed, and not formal proof-assistant verification.
