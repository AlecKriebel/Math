# A supplementary diffuse-incidence scope probe

This is not a counterexample to Theorem 2, nor a proof that the diffuse class's ultimate no-overlap conclusion is false. It identifies a concrete unsupported extension in the deposited supporting theorem's simultaneous-limit argument. The manuscript itself excludes “singular load scaling” in Section 11 (controlling TeX lines 765–767); that exclusion may remove the example below. Whether that phrase excludes all singular type-incidence sequences, rather than only the total B,H loads explicitly excluded in the support's final scope paragraph, must be kept explicit. No promotion of a repaired or silently restricted manuscript follows from this probe.

## Exact native interfaces

`construction/higher_threshold/direct_portal_network/growing_portal_network/DIFFUSE_GROWING_PORTAL_NO_GO.md` lines 36–47 allow T_s blade types, exchangeable incidence lambda_t/s, fixed positive B=2 sum pi_t lambda_t, and require max lambda_t=o(s) for growing types. Lines 158–163 then assert heterotypic-blade external intervention O(Q_s/s) and stopped-chain convergence. The final scope paragraph excludes singular **B,H** scaling, not every type-incidence sequence. The symbolic verifier checks the already-derived portal count/branching algebra; it has no blade-resolution simulation or uniform-lambda estimate.

## Explicit admissible family for that broader supporting statement

For integers k>=2, take s=k^4 blades, Q=k^2 complete-network portals, H=1 and portal edge 1/(Q-1). Choose k rare blades with lambda_rare=k^3/4, and s-k common blades with lambda_common=s/[4(s-k)]. These may be regarded as s separately labelled types with proportions 1/s, so T_s=s grows. Every represented type has positive incidence. B=1 exactly; H is fixed; Q/s=k^-2->0; max portal edge->0; lambda_max/s=1/(4k)->0. All weights are positive rational and independent of fitness. A portal birth hits one particular blade with vanishing probability as required.

Nevertheless a rare blade endpoint has aggregate portal load Q lambda_rare/s=k/4, which diverges. Thus the unit blade edge does not dominate its local dB competition. Rare blades have half of the total portal-to-blade incidence weight, so this is not merely an error on an asymptotically negligible exported-child mass.

For example, freeze a configuration with one mutant endpoint, its resident mate, exactly one mutant portal and all other portals resident. Put w=1/(4k), L=Qw=k/4. Under dB, after multiplication of probabilities by the population size, the two local changes have rates

    up   = r(1+w) / [r(1+w)+(Q-1)w],
    down = [1+(Q-1)w] / [1+(Q-1)w+r w].

Their first-local-change success probability up/(up+down) tends to zero; the isolated unit-edge singleton probability used to mark a dB child is 1/2. Below any fixed portal-count cutoff, the same discrepancy persists: mutant portal weight is O(1/k), whereas resident portal load is of order k. An O(Q/s)=O(k^-2) error cannot control these local rates. The missing aggregate load is Q lambda_t/s.

The exact rational probe `verify_scope_probe.py` checks the defining identities and local probability samples. It is diagnostic evidence of a failed supporting uniform approximation, not a counterexample to the ultimate no-overlap inequality. A complete new analysis of this incidence regime would be repair and is outside the assignment.

## Disposition

The published central sequence has super-small epsilon and is unaffected. The manuscript's explicit singular-load exclusion prevents treating this automatically as a false manuscript theorem. The source's broader growing-type claim and the phrase “singular load scaling” have not been reconciled by an exact definition in the 18-page paper. This lane records the discrepancy for root scope adjudication, and does not issue a whole-paper pass on the basis of the central theorem alone.
