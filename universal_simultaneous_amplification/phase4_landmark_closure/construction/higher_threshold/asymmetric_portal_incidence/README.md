# Asymmetric portal incidence

Status: **EXACT CLASS THEOREM PROVED; HIGHER-RANK CASE OPEN**.

This folder studies strong-pair blades coupled to a finite, generally
nonexchangeable portal network.  Portal-to-blade incidences may depend on
the blade type.  The aim is either to find a simultaneous-amplifying
rare-mutant trace above the established `r=3/2` threshold, or to prove an
exact tradeoff for this broader class.

Main files:

- `GENERAL_TRACE_AND_RANK_ONE_NO_GO.md` derives the exact
  `2^Q-1`-state portal-subset episode and the full multitype branching trace.
  It then proves a no-go theorem for arbitrary unequal portal loads under
  rank-one blade incidence and no direct portal edges.
- `verify_rank_one_tradeoff.py` checks the rate specializations, exact PGF
  sign criteria, sum-of-nonnegative-terms certificate, and independent
  portal-subset/count agreement.
- `search_asymmetric_trace.py` and `search_load_allocation.py` are discovery
  optimizers for the genuinely higher-rank case.  Their output is numerical
  evidence only.

The exact obstruction is the pointwise identity

\[
 \Phi_B(B)+\Phi_D(B)
 =-{(B-1)^2(B+1)+(r-1)B^2+(r-1)^2B(B+1)+(r-1)^3B
     \over (B+r-1)(1+(r-1)B)}<0.
\]

All rates are derived from the atomic Bd and dB rules.  Numerical work is
used only to discover exact statements.  No literature search or external
contact is used.
