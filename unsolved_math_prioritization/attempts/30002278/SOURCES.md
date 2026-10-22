# PML source and prior-work audit

Checked 30 September 2026. This is a bounded audit of the exact formulation;
no present-day openness or novelty certificate is claimed.

## Original contribution and important scope distinction

The complete Kaltenbacher contribution, *Stability Analysis of Time-Domain PML*,
printed pp.196–200 of [OWR 03/2013](https://ems.press/journals/owr/articles/12331),
was read from the publisher's complete PDF. Pages 197–198, containing the equations,
functional, inequalities and final warning, were also visually checked.

The report first presents the full auxiliary-variable equations, then proposes
setting C=0, and finally says that spatial variation generates an uncontrolled
term even in the proposed argument. It credits Patrick Joly for that observation.
The pinned “original_statement” is a paraphrase of the third step in the proposed
energy proof, not the final open-problem sentence. The cleaned record broadens
this into a variable-profile Lyapunov construction request. The package does not
convert a failure of the displayed δ,F family into a negative answer about all
possible functionals.

The original's “true PML in 2D” statement concerns a genuinely two-dimensional
reduction with the unused variable and derivative absent. In three dimensions,
setting one damping profile to zero does not by itself make the entire C matrix
zero. Our single-active-profile test has both other profiles zero, so C=0 exactly.

## Detailed primary paper

[Kaltenbacher–Kaltenbacher–Sim, JCP 235 (2013), 407–422](https://doi.org/10.1016/j.jcp.2012.10.016),
was retrieved in complete publisher-deposited XML from the public Europe PMC
full-text endpoint, PMCID PMC3719215. Its equations (12)–(17), Section 3 weak
formulation, functional (29), conditions (33)–(34), and full Theorem 1 were read.
The weak formulation has Dirichlet p,v and no imposed boundary condition on the
auxiliary vector u. Theorem 1 assumes zero initial u; it does not impose a
physical-region support condition on all pressure data. Those are the data
conventions of the scoped obstruction.

The original model derivation and numerical applications often start with zero
initial data and later forcing. That more restrictive reachable-state problem is
not refuted by a layer-supported initial test. No instability of its numerical
method or of the actual acoustic dynamics is inferred from increasing η.

The PMC browser route returned a browser challenge; the complete XML was obtained
from the official Europe PMC API without solving a challenge. No full PDF of this
paper is claimed. The XML preserves its MathML equations and is hashed below.

## Later sources checked

1. **Baffet–Grote–Imperiale–Kachanovska (2019)**,
   [HAL hal-01865484v2](https://hal.science/hal-01865484v2),
   [J. Sci. Comput. DOI](https://doi.org/10.1007/s10915-019-01089-9).
   Complete author-manuscript PDF retrieved. Section 2 model and boundary/initial
   conventions, Theorem 2.2 and its proof, and Remarks 2.1–2.4 were checked.
   The theorem assumes damping constant throughout the analyzed domain.
   The variable-profile identity explicitly contains coefficient-gradient terms;
   the piecewise-constant case has an interface remainder. These known facts
   are credited, including the state augmentation. The introductory physical
   setup takes initial data zero in the PML, which is not the initial-data class
   of our test. The old Basel PDF URL returned an HTML landing page; the full
   manuscript was instead obtained through its public HAL record.
2. **Bécache–Kachanovska (2021)**,
   [SIAM J. Numer. Anal., DOI 10.1137/20M1330543](https://epubs.siam.org/doi/10.1137/20M1330543).
   Publisher abstract and scope checked. It establishes stability/convergence
   in waveguides for arbitrary nonnegative bounded damping using Laplace-domain
   methods. This is relevant affirmative prior work in a more specific geometry,
   not evidence that every variable-profile PML is unstable. No claim to have
   independently verified its full proof is made, and no theorem from it is a
   premise of the scoped obstruction.
3. **Feriani et al. (2025)**, Journal of Sound and Vibration 595, 118779,
   [public institutional full PDF](https://vtechworks.lib.vt.edu/server/api/core/bitstreams/7519b48c-d711-496e-b2c7-192565b695d2/content),
   [arXiv record](https://arxiv.org/abs/2404.08464).
   Full published PDF retrieved; model motivation and Sections 5–6 checked.
   Its decoupled formulation explicitly changes edge/corner couplings and is
   assessed through numerical performance and long-time simulations. It is not
   imported as a proof for the unchanged OWR equations or for (3).
4. **Model order reduction of time-domain acoustic finite element simulations
   with perfectly matched layers (2024)**,
   [publisher article](https://www.sciencedirect.com/science/article/abs/pii/S0045782524005541).
   Publisher abstract and introduction checked. Its stable model-reduction
   construction uses modified/reduced PML models. No full-paper proof review
   or direct solution of the present continuum variable-profile task is claimed.

Targeted searches combined the exact report/paper titles with “Lyapunov”,
“spatial variation”, “variable damping”, “stability”, and recent acoustic PML
work. No verified construction with the full requested scope was identified.
This is not an exhaustive literature review. In particular, constant-coefficient
results, different PML equations, waveguide results and discrete numerical
stability evidence remain separate from the broad source task.

## Prior-attempt gates and provenance

The pinned source record is ID 30002278 / OWR-12331-002, dataset revision
37e53eabe540fb458758e198be61634bd02ee008. No exact-code imported research report
was found. The live queue showed rank 103, queued, 0/5. Exact-ID and PML all-state
PR searches returned none; the branch and attempt path were absent from prior
history, and the related-target index had no entry. Repository-wide matches
were desk-review/ranking metadata only. The campaign skip rule did not apply.

All research is confined to this attempt folder. No queue generator, shared
catalog or queue edit was performed. Primary caches remain outside the public
package. The exact retrieved source files are recorded in source_manifest.json.
