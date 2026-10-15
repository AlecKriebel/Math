# PDE and relativity frontier screen

Timestamp: 2026-10-06 PDT. Screening completion: 100% for this assigned comparison; no target theorem proved, no probability of resolution asserted.

## Recommendation from this sector: strong cosmic censorship for one-ended vacuum collapse

**Conditional impact: 9.3/10. Risk: very high.** This is a more consequential and better-defined follow-on than simply attaching the Navier–Stokes or quantum Yang–Mills Millennium labels to unrelated inputs.

**Exact aspirational theorem:** Construct a nonempty family, ideally an open set in a precisely specified asymptotically flat constraint-data topology, of smooth complete one-ended vacuum initial data on R^3 describing collapse to a slowly rotating subextremal black hole, and prove that a residual subset has full maximal globally hyperbolic developments with no future continuous, nondegenerate W^{1,2}_loc extension. No symmetry. Genericity must be in a natural collapse-data family, not merely in an artificially chosen already-bad parametrization. This is a local one-ended-collapse version of strong cosmic censorship, not full generic cosmic censorship for arbitrary vacuum data.

**New input:** OpenAI family264 now establishes the corresponding full-MGHD inextendibility near every fixed rotating *two-ended Kerr bridge*, in a weighted smooth topology with only its tenth seminorm small. Its main theorem and exact topology appear in:
`/Users/alec/Desktop/math/preprints/Generic-Future-Inextendibility-with-Square-Integrable-Connection-Near-a-Fixed-Kerr-Spacetime-September-23-2026/build/sections/introduction.tex`.
Its packet preparation and weak-holonomy obstruction mechanism is the plausible portable component; merely citing its two-ended theorem is insufficient.

**Independent established bridge:** Kehle–Unger, *Event horizon gluing and black hole formation in vacuum: the very slowly rotating case* (Adv. Math.452,109816,2024), https://arxiv.org/abs/2304.08455 and https://doi.org/10.1016/j.aim.2024.109816, constructs one-ended asymptotically flat vacuum collapse to very slowly rotating Kerr, using characteristic gluing from Minkowski to an event horizon. The abstract specifically states C^2 gluing, so smooth regularity cannot be silently inherited.

**Why opened now:** Before264, even the relevant generic nonlinear weak-connection obstruction near two-ended Kerr was missing. The new theorem offers a concrete radiation-packet/blueshift/holonomy obstruction to transplant into a physically meaningful collapse geometry supplied by horizon gluing.

**Actual remaining central challenges:**
1. Localize the packet perturbations and constraint correction to the retained exterior of a one-ended collapse construction. Show they survive the gluing and do not require the second asymptotic end.
2. Establish a perturbation-transfer map with enough openness/density control to transfer the Baire argument. The preimage of a residual set under an arbitrary continuous gluing map need not be residual.
3. Upgrade or otherwise match the gluing regularity to264's smooth finite-order estimates. C^2 characteristic gluing is not immediately enough for tenth-order smallness or high-frequency preparation.
4. Exclude all future extension exits for the full collapse MGHD. An obstruction on one nontrivial Cauchy-horizon patch does not rule out extension somewhere else. The collapse center and remaining interior can introduce new exits absent in the two-ended theorem.

**First falsifiable milestone:** Prove a constraint-preserving one-ended packet insertion lemma: for one fixed slowly rotating collapse seed, every prescribed finite-order neighborhood contains data whose late-time horizon slab carries the264 nonzero radiation coefficient, with the same controlled errors, while the gluing region and regular center remain unchanged. If this cannot be done without presupposing the full one-ended stability/censorship statement, mark the route blocked. It is an independently significant lemma if obtained, but is not full SCC.

**Relevant primary current context:** Dafermos–Luk, Annals2025, https://annals.math.princeton.edu/2025/202-2/p01, proves C^0 extendibility for the controlled Kerr interior setting. Therefore the target must retain the square-integrable-connection threshold, not falsely promise C^0-inextendibility. Sbierski2026, https://doi.org/10.1007/s00222-025-01387-0, supplies a related lower-regularity inextendibility mechanism; the new264 already claims stronger threshold. These sources do not prove the one-ended target.

## Runner-up: arbitrary-large-data massive Vlasov–Yang–Mills in 3+1 dimensions

**Conditional impact: 8.7–9.0. Risk: high.** Exact target: for a compact gauge group such as SU(2), positive particle mass, nonnegative smooth compact phase/color-orbit data and compatible smooth finite-energy gauge fields on Minkowski space, prove global smooth evolution, unique modulo gauge, without smallness or symmetry. This is a classical kinetic gauge-field theorem, not quantum Yang–Mills existence or mass gap.

**Actual new input inspected:** `/Users/alec/Documents/Math/openai_followon_multispecies_vlasov_maxwell/publication/main.tex`. Its theorem has finite species, positive masses, arbitrary real fixed charges, finite-energy Maxwell fields, no neutrality. Its source–receiver kernel coefficient is e_a e_b/m_a. The universal cancellation is valid for arbitrary differentiable timelike source and receiver curves, independent of acceleration signs; the new multispecies work controls the shared momentum bootstrap using positive mass-weighted energy and an aggregate label space. Those are genuinely relevant mechanisms.

**Potential mechanism:** Replace fixed scalar source–receiver coefficients by invariant inner products of color charges after parallel transport. Wong transport preserves charge-orbit norm. The mechanical null-cone geometry and timelike angular-occupation estimates may persist. Use Yang–Mills positive energy and covariant null flux to control gauge-field self-interaction.

**Central unresolved obstacle:** Maxwell linearity is used explicitly to write a source-labeled retarded kernel. Yang–Mills has self-interaction, and parallel transport differentiations generate curvature/holonomy terms; a fixed scalar coefficient is no longer constant. No checked estimate currently bounds these remainders within the same selected-receiver bootstrap. Treating Yang–Mills nonlinear terms as an arbitrary external force would lose precisely the needed control.

**First falsifiable milestone:** Derive an exact gauge-covariant analogue of the pair cancellation for SU(2) in temporal gauge and estimate its first non-Abelian remainder by energy/cone flux and the existing momentum-scale quantities with no uncontrolled field-derivative norm. An estimate that asks for the desired global gauge-field bound is circular.

**Primary priority source:** Choquet-Bruhat–Noutchegueme1991, https://www.numdam.org/item/AIHPA_1991__55_3_759_0.pdf, proves local Yang–Mills–Vlasov existence, discusses charge-orbit conservation, and explicitly notes that local theory plus conformal methods can yield global existence for massless particles on Minkowski. Thus massless global existence is not a safe novelty claim; target massive arbitrary data and perform a full priority audit. The exact broader modern massive-global literature was not exhaustively certified by this short screen. The 1999 general-charge-density local result is https://doi.org/10.1016/S0764-4442(99)90006-X.

## Screened-out shortcuts

- **Unforced 3D Navier–Stokes from376 and371:** no direct bridge identified.376 constructs selected smooth velocity fields and their external forces; computational universality does not create autonomous energy transfer or blowup.371 concerns high-dimensional scalar defocusing NLS and its own profile/spectral structure. Choosing a famous target without a mechanism is not deeper research triage.
- Separate current primary source arXiv2609.35406 (https://arxiv.org/abs/2609.35406) describes forced Navier–Stokes blowup Part I and a residual-correction Part II. Removing forcing from a verified complete construction could be a10-level program, but is not a consequence of376 and requires inspecting the full separate source. No claim of its completeness was made here.
- **3D defocusing NLS blowup from371:** generic dimension reduction is no longer a fresh target. Buck et al. https://arxiv.org/abs/2609.23685, Sept2026, already claims smooth radial compact-support blowup for (d,p)=(3,27),(4,9),(5,7). Full nonradial open-set stability could remain distinct; must not advertise bare3D blowup as new.
- **Global Einstein–Vlasov regularity for arbitrary data:** false as a blanket spacetime-completeness target because collapse and trapped surfaces occur. A weak-censorship/exterior theorem would require curved-cone geometry, focusing and horizon control absent from the flat Maxwell cancellation. It is a much less direct route than264 plus collapse gluing.
- **Lane–Emden:** user's solved follow-on, inspected at `openai_followon_lane_emden/publication/main.tex`, is a full subcritical a-priori estimate/Dirichlet compactness consequence via PQS. Critical or supercritical classification and parabolic Liouville theorems do not follow from that elliptic compactness statement. No10-level bridge found.
- **Boltzmann:**363's entropy-solution nonuniqueness does not yield smooth large-data blowup or global smooth solvability;364's kinetic-limit theorem is conditional on a regular Boltzmann lifespan. Extending it beyond that lifespan would merely restate the central kinetic singularity problem.
