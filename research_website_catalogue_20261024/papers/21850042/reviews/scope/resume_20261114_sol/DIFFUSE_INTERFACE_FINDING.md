# Diffuse growing-type interface gap

The actual support note `construction/higher_threshold/direct_portal_network/growing_portal_network/DIFFUSE_GROWING_PORTAL_NO_GO.md` explicitly permits a growing number of blade types and assumes `max_t lambda_t=o(s)` as its no-concentration condition. It later says external intervention during a fast heterotypic-blade resolution is `O(Q_s/s)` and concludes the same stopped-trace limit, scalar collapse and no-overlap theorem.

The displayed conditions alone do not justify that trace. Let k→∞, s=k^4, Q_s=k^2, H=1 with complete portal edge 1/(Q_s−1). Use k heavy blades with lambda_h=k^3, and s−k light blades with lambda_l=1/(1−k^−3). All incidence is portal-exchangeable and positive. The blade load is exactly B=2[k^−3 k^3+(1−k^−3)/(1−k^−3)]=4. Thus B,H are fixed, Q_s→∞, Q_s=o(s), maximum portal edge→0, and max lambda_t/s=1/k→0. Heavy blades receive exactly half the child-type mass f_t, although their initial population proportion tends to zero.

A heavy endpoint has total outer degree Q_s lambda_h/s=k, versus internal blade edge 1. Its heterotypic resolution is therefore not an isolated strong pair. With one mutant portal and one newly mutant heavy endpoint, exact atomic dB rates (after multiplying by population size) for pair conversion and pair erasure, while portal types are frozen, are

    u_k = r(1+1/k) / [r(1+1/k)+k−1/k],
    d_k = (1+k−1/k) / [1+k−1/k+r/k].

At fixed r=3/2, u_k→0 and d_k→1; u_k/(u_k+d_k)→0, rather than the isolated-pair 1/2 success mark used by the trace. The probability of an outer replacement at the mutant endpoint is order one, not O(Q_s/s)=O(k^−2). Allowing the portal to evolve cannot turn this into the asserted isolated-pair coupling: there is no small external-intervention probability to sum. Exact rational finite cases are in DIFFUSE_INTERFACE_WITNESS.json and recomputed by verify_scope.py.

This is a failure of the supporting proof's stated growing-type interface, not a verified counterexample to its final no-amplification conclusion. No repair has been attempted. The printed Section 11 item 3 excludes “singular load scaling” but does not define whether that phrase excludes precisely this incidence-concentration regime; B and H themselves do not scale here. Its brief statement is therefore weaker in hypothesis detail than the supporting note, and its intended scope must not be silently broadened. A complete original-claim assessment should record this unresolved ancillary gap rather than replacing it by the fixed-incidence class. The main center–triangle theorem uses a different graph and is not affected by this diagnostic.
