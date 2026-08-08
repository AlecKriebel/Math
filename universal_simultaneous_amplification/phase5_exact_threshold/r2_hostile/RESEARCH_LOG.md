# Fitness-two exact hostile branch

Date: 2026-08-08 (America/Los_Angeles)

## 09:00 -- exact solver and finite supports

- Built an independent FLINT solver for both Bd and dB absorbing equations at
  `r=2`.  It deletes state-dependent self loops and normalizes only the exact
  changing rates, so weak bridges do not create floating-point cancellation.
- Replayed the complete-graph formulas for every `2<=n<=7`.
- Exactly evaluated every connected unweighted graph in the NetworkX atlas
  through order seven: 995 graphs and 1,990 rule-specific solves.  There was
  no dB or simultaneous violation.  The complete graph was the unique dB
  equality at every order.
- Status: **PROVED IMPLEMENTATION / EXACTLY COMPUTED FINITE CORPUS**.  This is
  not a universal theorem.

## 09:04 -- multiscale structured graphs

- Exactly screened 9,471 rational graphs in 51 templates.  The templates
  cover two- and three-block dense graphs, single-bridge and weakly completed
  barbells, sparse and completed double hubs, paired satellites on clique
  cores, and ring/chord completions.
- Relative tied-role weights ranged from `10^-4` to `10^4`.
- Found no dB, simultaneous, or marked-promotion violation.  The strongest
  nontrivial dB ratio was

  `382593861056199739292388 / 384695063664906455754437`

  (approximately `0.9945380047544956`) on an order-seven two-block graph;
  its Bd ratio was approximately `1.0003119900381823`.
- Exactly screened 4,180 independently weighted trees through order six,
  with relative edge scales through `10^12`.  No relevant sign failed.
- Status: **EXACTLY COMPUTED FINITE EVIDENCE**.

## 09:10 -- true F0 and directed diagnostics

- Kept the canonical distinction

  `F0=1/m-1/m_K`

  versus the stronger sufficient promotion margin

  `F_prom=1/m-U M_P^2 psi`.

- Ran a final bounded exact `F0` search on 2,300 reversible rational graphs of
  orders five, six and seven.  The corpus deliberately combined positive
  complete support, random sparse support, nearly disconnected cuts,
  multiple hubs and core--periphery structure with integer weights through
  `10^12`.  No `F0<0` graph appeared.  The smallest margin was

  `57329341893/13193475083440 > 0`

  on an order-six almost-complete support.
- Exactly screened 1,570 positive loopless directed row kernels for both
  `F0` and `F_prom`.  Neither failed.  This does not prove a directed theorem
  and does not weaken the need for reversibility in the admissible problem.
- Status: **EXACTLY COMPUTED FINITE EVIDENCE; UNIVERSAL SIGN OPEN**.

## 09:15 -- permutation-orbit midpoint audit

- Recovered the already committed phase-four exact refutation of nonregular
  conductance averaging: a connected weighted path and a transposition have
  strictly lower dB fixation after midpoint symmetrization.
- Independently found a simpler connected path with edge weights `(5,1,1,1)`
  and transposition `(0 3)`.  Its exact midpoint slack is

  `-27235691462770866071897033062192847 /
   6341472920592709123366290939507789100`.

- Replayed the independent SymPy certificate for the earlier witness.
- Screened 924 exact regular-conductance midpoint comparisons built from all
  small regular atlas graphs and rational sums of perfect matchings or
  Hamilton cycles.  No regular failure appeared.  This is finite evidence;
  the regular orbital conjecture remains open.
- Status: **NONREGULAR CONJECTURE EXACTLY REFUTED / REGULAR SUBCASE OPEN**.

## Freeze

- Assigned hostile-search milestone completion: **100%**.
- Universal `r=2` dB maximality completion: **0% from this branch**; no proof
  and no admissible counterexample was found.
- Strongest verified conclusion: the exact hostile corpora contain no true
  collision counterexample, while nonregular permutation symmetrization is
  unusable as a global proof route.
