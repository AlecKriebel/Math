# Five substantive approaches and corrections

Target: 30000707 / OWR-1460-014, rank 607. Date: 2026-10-04 UTC.
Prior recorded turns: 0/5 on the live queue. This attempt uses five
substantive approach responses and stops proof search at 5/5. Auditing
these frozen results is verification, not another search turn.
Completion estimates below concern the full classification and are
subjective planning judgments, not success probabilities or certificates.

1. **11:32–11:35, local divisors and multiplicity ratios.**
   Derived the exact pole orders, residue signs, finite multiplicity
   condition, and integer preimage loci in PROOF.md §1. These force
   infinity CM but do not force a second CM value. Status: proved partial;
   full-target completion estimate 15%. No result from adjacent Problem 1
   is assumed.
2. **11:33–11:38, global growth and current-theorem dependency.**
   Applied and checked the scope of Steinmetz's published characteristic
   inequality to obtain order one/two and logarithmic-width confinement
   of shared finite points. Examined the recent finite-order theorem
   claim and found a specific failed positivity inference, documented in
   DEPENDENCY_CHECK.md. Status: proved reduction with stated standard
   inputs; recent claimed closure unavailable. Full-target estimate 25%,
   reduced from a provisional 60% before checking the dependency. A
   finite-order reduction is not itself 3IM+1CM rigidity.
3. **11:36–11:39, Möbius/four-value classification.**
   Classified completely the branch with any extra CM value, including
   the case where infinity is a fixed rather than omitted value. Exact
   first-system representatives require the minus signs in (7). The
   quadratic system has no CM-branch solutions. Status: proved
   conditional classification. Full-target estimate 35%; the three
   finite non-CM values remain the central gap.
4. **11:36–11:42, differential elimination and pole recursion.**
   Eliminated g to a scalar equation and computed the generic Laurent
   coefficient determinant. Meromorphic pole germs, if they exist,
   admit no free nonnegative Laurent coefficient once location/sign are
   fixed. Neither formal recursion nor periodic coefficients establishes
   global meromorphic existence or periodicity. Status: exact necessary
   reduction; no global classification. Full-target estimate 35%.
   An initially explored autonomous linearization used the wrong
   exponential factor in the reconstruction of g; it was discarded
   before any claim, and the correct formula (9) and independently
   expanded identity (10) are used. No autonomous-integrability claim
   survives.
5. **11:39–11:43, rational-exponential and parity mechanisms.**
   Proved the first-system classification for rational functions of e^z
   of degree at most two, by endpoint orders, residues, and coefficient
   contradictions. This is a symbolic degree bound, not a coefficient
   grid search. Excluded simultaneous rational-in-e^(z^2) solutions of
   the second system by parity/chain rule. Status: proved restricted
   exclusions. Full-target estimate 40%; arbitrary rational degree and
   nonperiodic functions remain outside the argument. Budget exhausted.

## Verification checkpoints

* 11:41–11:42: inspected primary PDF pixels of OWR p.542 and recent
  preprint pp.39–40, confirming displayed exponents and positivity text.
* 11:45–11:48: completed the written proof and exact symbolic controls.
  The first control run failed because the finite-root ratio check had
  `-value/x` instead of `value/x`. Direct algebra corrected the control;
  it was not used as a proof premise. All 37 controls then passed. The
  negative literal-sign and quadratic-composition controls reject as
  intended.
* Frozen artifact receives an independent/root audit before any remote
  change. No external outreach, release, publication, push, or queue
  mutation was performed by this worker.

## Terminal research disposition

UNSOLVED, 5/5. The recent theorem's truth is not refuted. Its printed
inference is insufficient for this package's required verification.
No novel resolution, first priority, paper, or DOI is proposed. The
adjacent psi=1 target shares sources but has a broader hypothesis and
its own gap; these are not independent discoveries of a common proof.
