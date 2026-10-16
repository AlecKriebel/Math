# Robin bound states: a dimension dichotomy

AIM Problem 1.4, *Shape optimization with surface interactions*. Corpus 20000488 / AIM-ANALYSIS-0020, rank 1269. Accepted full negative answer to the dimension-unrestricted universal question, substantive attempt 1 of 5.

## Established result

A nonzero smooth compact perturbation of a half-space need not have an attractive Robin eigenvalue below the flat threshold when the ambient dimension is unrestricted.

In R⁴, write x∈R³ and set h(x)=exp(−1/(1−|x|²)) for |x|<1 and h(x)=0 otherwise. Let f=h/100 and Ω={y>f(x)}. For outward-normal boundary condition ∂νu=u, the spectrum is exactly [−1,∞), with no spectrum below −1. The domain is connected and smooth, its boundary is connected, and its symmetric difference from the upper half-space is bounded. This is a genuine nontrivial deformation.

The [complete mathematical report](MATHEMATICAL_REPORT.md) and [independent mathematical audit](MATHEMATICAL_AUDIT.md) prove more:

- In ambient dimensions n=2,3, every nontrivial connected smooth compact half-space perturbation has a discrete eigenvalue below −β² for every attractive coupling β>0. Overhangs and compact additional boundary components are allowed.
- In every n≥4, every compactly supported Lipschitz graph has no spectrum below −β² for all sufficiently small positive β. At any prescribed coupling, a sufficiently small nonzero smooth graph also gives a counterexample.
- The essential spectrum is [−β²,∞). The proof includes the closed form, form core, IMS/Rellich exclusion and explicit Weyl sequences.
- The global boundary-defect identity, the graph capacity test, self-contained Hardy–trace estimate, all-function lower bound, and exact analytic constants for f=h/100 are retained in full.

The audit's two presentation corrections are already included: the support ball is closed, and Lipschitz flattening is justified directly by the weak chain rule and vertical-fiber integration. The audit retains its authored power-series and rational-inequality argument for the stronger constant bounds.

## Scope and credit

The full dimension-unrestricted universal assertion is disproved by a single dimension-four example. The positive smooth dimension-three theorem addresses a separately dimension-three-restricted reading. No classification of all higher-dimensional nongraph domains or all-coupling absence is claimed. Equality of spectral sets with the essential spectrum does not exclude embedded eigenvalues.

Exner–Minakov are credited for the standard planar theorem. The large-coupling Pankrashkin–Popoff result is compatible with weak-coupling absence. The cited September 2026 magnetic result concerns a different operator. Lotoreichik's 2017 talk records expectations and is not treated as a proved Robin theorem. [SOURCE_METADATA.json](SOURCE_METADATA.json) records public source identities, titles, links, status and inspection limits. The canonical AIM HTML has disclosed plain-HTTP provenance; no HTTPS certificate warning was bypassed.

This is AI-assisted, unrefereed mathematical work. Scoped acceptance is not external human peer review, journal acceptance, formal proof-assistant certification or a novelty certificate. Retrieval and inspection claims are recorded history; edition preparation makes no new scholarly retrieval, source-file rehash, source inspection or literature search claim.

## Publication boundary

Exactly six text files are distributed. Complete authored mathematical proofs and audit are retained. Programs, checker outputs, computational results, source copies, extracted source text, images, datasets and private coordination material are excluded. No excluded computation is rewritten as prose.

The addition-only edition leaves QUEUE.md and unrelated repository entries unchanged. Editorial preparation adds no substantive proof turn and does not reset attempt accounting.
