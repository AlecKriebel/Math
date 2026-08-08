# Lower diagonal to fitness two: research log

## 2026-08-08 — branch opened

- Started from the proved separated response normal form and the exact
  `R_hyb` library; no fixed-order clone or doublet screen is being repeated.
- Isolated a new self-dual macro mechanism for growing strong-pair modules.
  If monomorphic pair `i` has inverse internal strength `a_i` and weak
  symmetric coupling `e_ij`, its leading Bd module-conversion rates use
  source activity `a_i`, while dB uses target activity `a_j`.
- The target-activity chain `(a,e)` is exactly the source-activity chain for
  `(1/a, a_i a_j e_ij)`.  An involution satisfying
  `a_phi(i)=1/a_i` and `e_phi(i),phi(j)=a_i a_j e_ij` therefore makes the two
  macro fixation probabilities identical under uniform singleton starts.
- A numerical search is testing whether this self-dual class contains a
  growing strong amplifier.  Any lead must still be lifted through exact
  pair-resolution, uniform entrance, separated-gate, and diagonal error
  bounds before it becomes a lower-bound theorem.

## 2026-08-08 — paired-star hierarchy exactly stopped

- The self-dual, rank-one, unconstrained small-rank, and two-center star
  macro searches all returned to the source/target tradeoff boundary.  These
  are numerical route triage only.
- An apparent dB hierarchy lead was replayed in the exact paired-star
  quotient.  With central-pair weight `A=L^3`, peripheral-pair weight
  `W=L^6`, and bridge weight one, peripheral dB singleton fixation tends to
  `(1/2)(1-r^-4)`, but peripheral Bd fixation tends to zero.  For example at
  `r=2` the exact-quotient floating values fall from `0.0403105` at `L=4`
  to `0.0015443` at `L=12`.
- The reason is now exact and topology independent.  After a singleton has
  resolved in its `K_2`, Bd macro conversion uses source activity and dB
  uses target activity.  Their first favorable/adverse odds are `r^2 x`
  and `r^2/x`.  Even granting fixation with probability one after the first
  gain gives a sharp scalar envelope.
- **PROVED CLASS OBSTRUCTION:** that envelope becomes nonpositive in the
  leaf-eliminated response at the unique algebraic crossing
  `R_pair=1.6986624639825652...` and remains so through fitness two.  The
  theorem permits arbitrary growing macrograph rank and later recovery
  paths.  It excludes every hierarchy that first separates into monomorphic
  strong pairs; it does not exclude a portal acting during the discordant
  pair state.
- Next executable task: build the smallest nonseparated pair--portal trace,
  retain portal events during the discordant-pair episode, and optimize its
  exact first-excursion response against the separated envelope.

## 2026-08-08 — exact star--reservoir diode and entrance obstruction

- A star between two clique reservoirs is an exact same-direction diode.
  With `L` leaves and reservoir order `C`, its two-interface odds products
  grow as `r^(C+2L)` for Bd and tend to `r^(C+4)` for dB, up to the displayed
  exact rational factors in `STAR_RESERVOIR_DIODE_AND_ENTRANCE_OBSTRUCTION.md`.
- The diode does not rescue a three-scale construction in which each clique
  and star locally absorbs before coupling.  The total dB singleton fixation
  mass of the star is only `O(1)`, while it contributes `L+1` uniformly
  sampled vertices, and `K_C` itself loses one finite-population unit.
- **PROVED CLASS OBSTRUCTION:** for every fixed `r>5/3`, every separated
  cycle with at least two `K_C` reservoirs and one `S_L` antenna per
  reservoir is eventually dB-suppressing, even after granting certain global
  fixation once the initially occupied component fixes.  The proof is the
  exact inequality `A_L<=A_1=-(2r-3)/r` and the complete-baseline correction
  `p/m`.
- The necessary escape is now sharper: star--reservoir events must act while
  the initial clique or antenna is polymorphic and create a positive entrance
  correction of order at least `1/C`.
