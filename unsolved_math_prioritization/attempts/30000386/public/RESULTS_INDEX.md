# Accepted results and their exact scope

All statements use the [public game rules](CONSTRUCTION_CONTRACT.md).
“Accepted” means the included mathematical audit accepted the stated scope;
it does not mean external peer review, historical novelty, or full resolution.
The source papers are identified separately in [SOURCES.md](SOURCES.md).

## Restricted positive strategies

1. **Maximum lead sixteen, from empty history, for infinitely many rounds.**
   Three accepted arguments establish this same bounded-lead result:
   [chronological rescue](pass4_invariant/LEAD16_RESCUE.md),
   [continuous two-layer viability](pass4_coupling/LEAD16_INDEPENDENT_AUDIT_AND_CONTINUOUS_PROOF.md),
   and [exact W2-to-W3 closure](pass4_devil/EXACT_TWO_MOVE_INVARIANT.md).
   Audits: [rescue](pass4_audit/LEAD16_RESCUE_AUDIT.md),
   [continuous proof](pass4_audit/CONTINUOUS_LEAD16_AUDIT.md),
   [exact invariant](pass4_survival/TWO_MOVE_INVARIANT_INDEPENDENT_AUDIT.md).

2. **Maximum-lead-sixteen tracker.** Reference speed at most 1/100 in
   Euclidean norm, common initial origin, and error strictly below 80.
   [Canonical corrected proof](pass4_invariant/LEAD16_BOUNDED_TRACKING.md);
   [audit](pass4_survival/LEAD16_TRACKER_INDEPENDENT_AUDIT.md).
   The earlier [lead-fifteen tracker](pass3_independent/BOUNDED_TRACKING.md)
   supplies the rank table and is independently
   [audited](pass3_survival/TRACKER_INDEPENDENT_AUDIT.md).

3. **Mixed short and distant leads.** The
   [fresh-block theorem](pass3_independent/MIXED_LEAD_COROLLARY.md),
   [audit](pass3_survival/MIXED_LEAD_INDEPENDENT_AUDIT.md), and item 2's
   final section give short cutoff sixteen with unchanged distant thresholds.
   Specifically, set K=3000000, A=200K, ell_j=j(1+floor(log_2 j))^2,
   L_j=A ell_j, S_1=1, and S_(j+1)=S_j+L_j. An announcement in block
   S_j<=n<S_(j+1) may be ineffective, have lead 1 through 16, or target
   t>=S_(j+2). The long-hit union bound is below 25921/30000. The theorem
   excludes the intermediate lead range; it does not merely bound its risk.

4. **Four prescribed known deadlines.** The
   [computer-assisted proof](pass3_deadlines/FOUR_DEADLINES.md) covers every
   increasing quadruple, with analytic coverage and 180 exact rational cases.
   [Independent audit and replay](pass3_devil/FOUR_DEADLINES_INDEPENDENT_AUDIT.md);
   [additional review](pass3_invariant/FOUR_DEADLINES_INDEPENDENT_REVIEW.md).
   The maximum finite-case cost is 34777/50976 at gap scales (2,2,2).

5. **Three prescribed known deadlines and concentration refinement.**
   [General three-time proof](pass2_deadlines/THREE_DEADLINES.md) with
   [two](pass2_devil/ARBITRARY_THREE_DEADLINES_AUDIT.md)
   [independent audits](pass2_invariant/ARBITRARY_THREE_TIMES_INDEPENDENT_AUDIT.md).
   The [concentration-profile lemma](pass2_invariant/CONCENTRATION_PROFILE_LEMMA.md)
   gives a [52/75 certificate for {13,17,21}](pass2_invariant/THREE_DEADLINES_13_17_21.md),
   improved to [52/103](pass2_invariant/THREE_DEADLINES_PROFILE_REFINEMENT.md).
   [Initial audit](pass2_audit/CONCENTRATION_THREE_DEADLINE_AUDIT.md);
   [refinement audit](pass2_audit/PROFILE_REFINEMENT_AND_LOCAL_RESERVE_AUDIT.md).
   These replace failed sufficient estimates for this triple, not losing games.

6. **One and two known deadlines; infinite sparse prescribed times.**
   [Proofs](pass1_fixed_time/REPORT.md),
   [audit](pass1_invariant/FIXED_TIME_INDEPENDENT_AUDIT.md).
   The sufficient sparse condition includes T_j=2j^2. Weighted sole-terminal
   capacity two and the robust preload reserve are established there.
   The later three-time geometry gives sole-terminal capacity 9/4.

7. **Sharp two-move terminal deficit reserve and capacity 5/2.**
   [Two-move reserve](pass3_invariant/TWO_MOVE_DEFICIT_RESERVE.md),
   [sole-terminal capacity](pass3_invariant/FIVE_HALVES_TERMINAL_CAPACITY.md),
   [audit](pass3_audit/TWO_MOVE_AND_FIVE_HALVES_AUDIT.md),
   [second audit](pass3_deadlines/NONLINEAR_TERMINAL_SECOND_AUDIT.md).
   The weighted capacity is uniform over terminal horizons, but does not
   protect unlisted intermediate lethal times. The claimed sharpness is for
   the specified two-move total-deficit threshold, not the global 5/2 capacity.

8. **Minimum-lead hidden-block wins.**
   [General criterion](pass2_survival/HIDDEN_BLOCK_CRITERION.md),
   [cubic blocks](pass2_survival/CUBIC_DELAY_THEOREM.md), and
   [logarithmic blocks](pass2_survival/LOGARITHMIC_DELAY_THEOREM.md);
   [independent audit](pass2_audit/HIDDEN_BLOCK_AND_SURVIVAL_AUDIT.md).
   An explicit sufficient lead is ceil(21 sqrt(n)(1+log_2 n)) at round n.
   Adaptive targets and mixed timestamps are allowed subject to that lead.

9. **Sharper reserves under separate restrictions.**
   [Euclidean rank reserve](pass4_coupling/EUCLIDEAN_RESERVE_PRELIMINARY.md)
   gives lead-fifteen tracking at reference speed 1/4 and radius 20. It also
   gives an arbitrary-H tracker of radius 12+H/3 when at most eight handled
   sites occur at every target time. Common initial origin is essential.
   Read the [audit](pass4_audit/EUCLIDEAN_RESERVE_AUDIT.md) together with the
   [current-version anchor addendum](pass4_audit/EUCLIDEAN_RESERVE_ANCHOR_ADDENDUM.md)
   and [independent acceptance](pass4_survival/EUCLIDEAN_RESERVE_INDEPENDENT_AUDIT.md).
   Neither unrestricted arbitrary-H safety nor the lead-sixteen speed-1/4
   tracker follows.

10. **Full-game survival through move seventeen and a local transport tool.**
    [Analytic survival-17 proof](pass1_survival/REPORT.md),
    [independent audit](pass1_game_audit/AUDIT.md).
    Section 5 of the [delayed-announcement report](pass2_survival/REPORT.md)
    gives a moving 2-by-2 room primitive under at most one local bomb per time;
    its [audit](pass2_audit/HIDDEN_BLOCK_AND_SURVIVAL_AUDIT.md) preserves the
    cardinal-motion restriction. Neither is infinite unrestricted survival.

## Exact reductions and conditional continuation tools

11. **Exact finite horizon and extraction to infinity.**
    [Recursion and cone reduction](pass1_survival/REPORT.md),
    [independent proof and audit](pass1_game_audit/AUDIT.md).
    Online winning strategies for every finite horizon imply one infinite
    strategy through nested subsets of nine Angel moves, despite unbounded
    Devil action choices.

12. **Finite maximum-lead arenas and the all-H equivalence.**
    [Arena and tail-age constraints](pass4_audit/BOUNDED_LEAD_FINITE_ARENA.md),
    [all-finite-leads reduction](pass4_audit/ALL_FINITE_LEADS_REDUCTION.md),
    [audit](pass4_survival/STRUCTURAL_REDUCTION_AUDIT.md).
    Decidability for each fixed H is proved; no large-H game was solved here.

13. **Initialized invariant criteria and negative-certificate format.**
    [Exact fixed point, fixed-depth obstruction, and ranked forcing graph](pass5_audit/FIXED_POINT_CRITERION_AND_DEPTH_OBSTRUCTION.md),
    [audit](pass5_devil/FIXED_POINT_AND_DEPTH_AUDIT.md),
    [deletion-monotonicity boundary](pass5_audit/DELETION_MONOTONICITY_ACCEPTANCE.md).
    [Critical-gap bootstrap](pass5_coupling/CRITICAL_GAP_BOOTSTRAP.md) and its
    [audit](pass5_audit/CRITICAL_GAP_BOOTSTRAP_AUDIT.md) give a sufficient
    all-depth route with a valid base induction. Its higher-depth geometric
    premise remains unproved.

14. **Robust acceptance and correction criteria.**
    [Exact deadline predecessor](pass2_audit/ROBUST_DEADLINE_ACCEPTANCE.md),
    [block safety and spread gate](pass3_audit/ROBUST_BLOCK_COUPLING_GATE.md),
    [gate audit](pass3_devil/COUPLING_GATE_INDEPENDENT_AUDIT.md),
    [global-reference transfer](pass3_survival/COUPLING_TRANSFER.md),
    [transfer audit](pass3_audit/TRACKING_TRANSFER_AND_OBSTRUCTIONS_AUDIT.md).
    These require complete boundary states and every intermediate death
    test. No compatible controller is constructed by the criteria alone.

15. **Positive finite-block concatenation and shared-budget accounting.**
    Sections 1 and 5 of the [multiscale report](pass4_multiscale/REPORT.md),
    [scoped audit](pass4_audit/POSITIVE_BLOCK_AND_SHARED_CHARGE_AUDIT.md),
    and [current-version addendum](pass4_audit/POSITIVE_BLOCK_SHARED_CHARGE_VERSION_ADDENDUM.md).
    The charge sum must cover all charges allocated to each physical
    announcement. These lemmas assume an actual controller and closed family.

16. **Stopping-time positive resets and exact residual bookkeeping.**
    [Proof and periodic example](pass5_multiscale/REPORT.md),
    [reset audit](pass5_survival/POSITIVE_RESET_INDEPENDENT_AUDIT.md),
    [accounting audit](pass5_devil/RESIDUAL_ACCOUNTING_AND_SPARSITY_AUDIT.md).
    The identity is m_new=m-E-G+U with U<=episode length. Heavy target times
    satisfy 9K<=N+H-1. A legal periodic safe play maintains residual count
    at least H-8, disproving an automatic-flushing inference. A reset family
    is still required.

17. **Idempotent eight-neighbor envelope.**
    [Proof](pass5_survival/IDEMPOTENT_DANGER_ENVELOPE.md),
    [audit](pass5_invariant/IDEMPOTENT_ENVELOPE_INDEPENDENT_AUDIT.md).
    Filling isolated holes gives a monotone idempotent envelope J with
    |J(B)|<=4|B|/3, a sharp bound for the envelope/ever-occupied union.
    Interleaved actual seed injections obey that same envelope, and one seed
    can add as many as five envelope sites. This spatial result is not an
    identification of the game's adaptive multitime predecessor.

## Scoped obstructions and quantifier separations

18. **One-dimensional online loss versus offline survival.**
    [Six-move Devil strategy](pass1_survival/HORIZON6_READER.md) and
    [certificate](pass1_survival/terminal_1d_horizon6_certificate.json);
    [independent audit](pass1_game_audit/AUDIT.md) replays all 729 move words.
    Every fixed nonadaptive legal schedule nevertheless admits an
    [infinite offline safe path](pass1_invariant/OFFLINE_REACHABILITY_LEMMA.md),
    already in one dimension. The quantifier orders differ.

19. **Fixed-velocity and restricted-information policies.**
    [Ballistic measure and adaptive move-eight defeat; bounded and increasing
    lookahead defeats](pass1_devil/THEOREMS.md),
    [square-root deviation theorem](pass1_devil/LINEAR_MOTION_OBSTRUCTION.md),
    [fixed-k earliest raw deadline obstruction](pass2_survival/EARLIEST_DEADLINE_OBSTRUCTION.md).
    Audits: [first group](pass1_game_audit/AUDIT.md),
    [raw-deadline memory](pass2_audit/HIDDEN_BLOCK_AND_SURVIVAL_AUDIT.md).
    These policy restrictions are essential; no unrestricted Devil win follows.

20. **Static cuts and separately safe endpoints.**
    [Exact examples](pass1_invariant/STATIC_INVARIANT_OBSTRUCTIONS.md),
    [audit](pass1_game_audit/AUDIT.md). A preload can be legally realizable
    without being adversarially forceable from the empty board.

21. **Independent-step and universal additive charging bounds.**
    [Harmonic worst-increment obstruction](pass1_invariant/INDEPENDENT_STEP_POTENTIAL_OBSTRUCTION.md),
    [supplementary audit](pass1_game_audit/INDEPENDENT_STEP_SUPPLEMENT.md),
    [universal additive-kernel minimax theorem](pass2_devil/ADDITIVE_KERNEL_MINIMAX_OBSTRUCTION.md),
    [audit](pass2_audit/ADDITIVE_MINIMAX_AUDIT.md).
    These refute specified sufficient certificates, not every minimizing
    potential policy or every nonlinear/reachable-state construction.

22. **Local linear composition cost and failed coarse recursions.**
    [Sharp 9/8 one-round reserve mass](pass2_invariant/LOCAL_LINEAR_RESERVE_OBSTRUCTION.md),
    [audit and exact failure at smoothing step 27](pass2_audit/PROFILE_REFINEMENT_AND_LOCAL_RESERVE_AUDIT.md),
    [three-time induction limit](pass2_deadlines/INDUCTION_LIMIT.md).
    The coarse failure at {7,9,11,13} is compatible with the full-game
    survival-17 theorem. A failed sufficient bound is not a losing instance.

23. **Bad-center mass amplification.**
    [Exact two-move predecessor](pass2_survival/NONLINEAR_BAD_CENTERS.md),
    [audit](pass2_audit/HIDDEN_BLOCK_AND_SURVIVAL_AUDIT.md),
    [every fixed-depth age-admissible family](pass5_coupling/FIXED_DEPTH_MASS_OBSTRUCTION.md),
    [audit](pass5_survival/FIXED_DEPTH_MASS_INDEPENDENT_AUDIT.md).
    The latter gives ratio at least 289/288 at m=12k, and asymptotic 9/8.
    It neither proves an unbounded W_k initialization nor refutes every
    nonlinear envelope or the critical-gap hypothesis.

24. **Specified reference-repair architectures.**
    [Move-then-hold obstruction](pass3_survival/MOVE_HOLD_BRIDGE_OBSTRUCTION.md),
    [endpoint-recovery obstruction](pass3_devil/ENDPOINT_RECOVERY_OBSTRUCTION.md),
    [audit](pass3_audit/TRACKING_TRANSFER_AND_OBSTRUCTIONS_AUDIT.md).
    The attacks force collision or violation of the promised tracking
    envelope. Their divergent repair-factor estimate is not loss probability.

25. **The old local tracker and a coarse multiscale bootstrap.**
    [Legal lead-sixteen defeat of the specified old controller](pass4_coupling/LOCAL_TRACKER_LEAD16_DEFEAT.md),
    [audit](pass4_devil/STRUCTURAL_AND_TRACKER_AUDIT.md),
    [equal-block radius/speed and classwise-feasibility obstructions](pass4_multiscale/REPORT.md),
    [scoped audit](pass4_devil/MULTISCALE_OBSTRUCTION_AUDIT.md).
    The strengthened history-aware controller in item 1 handles lead sixteen;
    the old-policy defeat is not a contradiction.

26. **Active/residual viability does not compose.**
    [Fifteen active plus fifty-four residual pairs](pass5_invariant/RESIDUAL_COMPOSITION_OBSTRUCTION.md),
    [audit](pass5_audit/RESIDUAL_COMPOSITION_AUDIT.md),
    [independent second audit](pass5_devil/RESIDUAL_COMPOSITION_AUDIT.md).
    Both components have their stated separate finite online viability but
    the union loses by move four. The K_70 preload history is cooperative,
    not a forced empty-rooted trap.

27. **A later update can create four intermediate dangers.**
    [Twenty-four-pair adaptive A8 counterexample](pass5_invariant/ADAPTIVE_A8_RECURSION_OBSTRUCTION.md),
    [audit and 729-word replay](pass5_survival/ADAPTIVE_THRESHOLD_INDEPENDENT_AUDIT.md).
    It defeats the displayed static timestamp sweep and is W2 but not W3
    from its preload. This does not defeat the lead-sixteen invariant or
    supply an unrestricted empty-rooted Devil strategy.

## Version and acceptance cautions

Preserved source files can contain superseded submission labels or historical
hashes. The public manifest identifies delivered bytes. In particular, use the
Euclidean reserve anchor addendum in item 9 and the multiscale version addendum
in item 15 to bind the current accepted input versions. Their earlier audits'
inline hashes identify earlier inputs, not the current files. A historical
“open” sentence in a preserved proof or audit means unresolved in the reported
work; this package makes no exhaustive current-literature certification.
