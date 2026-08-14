# Research log: singleton Kac-cycle MP

All times are America/Los_Angeles.  No external communication, graph
enumeration, or kernel search was used.

## 2026-08-13 19:00 PDT — exact Kac form and canonical Hellinger obstruction

- Schur-compressed each dual around one named singleton and identified its
  root reward with the Kac return-cycle quantity
  `psi_Ui=q_Ui E_i integral_cycle (|A|/s-p) dt`.
- Proved `rho_U-p=pi_U({i}) psi_Ui` at every root.  On the active branch all
  `psi_Ui` are positive, so both global excesses cancel from MP.
- Obtained the exact normalizer-free target
  `(x.psi_B^-1)(x.e psi_D^-1)>=r^3(x.1)(x.e)`.  Its diagonal is simply
  `r^3 psi_Bi psi_Di<=1`; its pair condition is the sharp two-by-two
  copositivity test in the four reciprocal Kac rewards.
- Derived the literal two-root trace form.  If the Bd trace rates are
  `i->j=a,j->i=b` and the dB rates are `i->j=c,j->i=d`, then clearing the
  two signed trace-reward numerators gives diagonals `bd-Qhat`, `ac-Qhat`
  and cross `e_jbc+e_iad-Qhat(e_i+e_j)`.
- An independent normalization audit of Sections 1--4 confirmed
  `psi_B=(Y_B/b,Y_B/a)`, `psi_D=(Y_D/d,Y_D/c)`, every cleared pair
  coefficient, and the raw-cycle factor `r^4 t_i`.
- Proved that direct macro path-space Hellinger has singular support on one
  analytic weighted three-path: dB has a positive singleton-centre to
  two-leaf jump, while neither Bd nor reversed Bd has the matching jump.
  This singular sector can carry arbitrarily large positive cycle reward.
- Audited exact target-locked micro expansion.  Its likelihood ratio retains
  repeated-source powers after the endpoint degree potential is removed.
  Two hidden histories with the same projected closed singleton cycle have
  different ratios, so Kac closure does not turn the ratio into a
  coboundary.
- At `R_hyb`, singleton and doubleton excess rewards on the three-path have
  opposite signs.  The reward-weighted cycle functional is therefore a
  signed measure, not an object to which standard positive Hellinger applies.
- Scalar Hellinger also keeps only the geometric mean of the two swapped
  root assignments and deletes the exact orientation square.
- Scope: these are obstructions to canonical macro Hellinger,
  endpoint-coboundary expanded reversal, and scalar positive reward
  Hellinger.  They do not refute a multiplicity-labelled, signed,
  assignment-valued full-cycle proof.
- Best-guess completion: **100% for this Kac reformulation and route audit;
  roughly 50% for universal `(MP)`.**  The remaining inequality is now
  normalizer-free and root-local, but the full signed cross-rule cycle
  comparison is unproved.
