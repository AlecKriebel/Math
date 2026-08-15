# Specialist referee guide

## Fast audit path

1. Read the exact scope and Definition 2.1 in the manuscript.
2. Read `THEOREM_AND_PROOF_MAP.md` in this packet.
3. Inspect `s_tc_jc_landmark_closure/THEOREM_CERTIFICATE_CROSSWALK.md`.
4. Run:

   ```bash
   bash reproducibility/verify_quick.sh
   ```

5. For a complete replay, run the full and regenerate-all commands listed in
   the repository README.

The whole-release checker is a consistency gate. The mathematical evidence
is in the graph-derived component scripts and their independent replays.

## Exact scope

- four-state open Jukes–Cantor model only;
- binary, LSA-valid, already-simple, reticulation-preserving semi-directed
  strongly tree-child level-2 networks;
- topology modulo ordinary triangle redirection;
- symmetric full-dimensional regular overlap and source-relative one-sided
  generic containment;
- no physical bridge-parameter recovery and no complete-image equality claim.

## Questions for a human specialist

1. Is the fixed mixed-graph rooting convention described accurately relative
   to Englander et al. v4 and Holtgrefe et al.?
2. Is ordinary triangle redirection stated at the correct common-germ
   stochastic strength?
3. Is the pointwise cut theorem's two-active case complete?
4. Does the projective bridge-fibre proof establish the full kernel on the
   incidence-saturated positive tensor locus, with the physical-domain
   qualification stated correctly?
5. Is the semialgebraic localization argument valid without a continuous
   target-parameter selection?
6. Is the genericity argument stated at sufficient real-algebraic precision?
7. Is the triangle-free Omega pair correctly interpreted as weakly but not
   strongly tree-child under the fixed-graph convention?
8. Does identical leaf substitution preserve that interpretation and add
   exactly two dimensions per leaf?
9. Does the repaired one-active cut handoff legitimately pass from the
   at-most-eight-port compression to the four-active strict-minor universe?
10. Is complement-normalized zero-sum descriptor grouping sufficient for the
    marginal constant-rank argument?

No human specialist review is claimed to have occurred merely because this
packet exists.
