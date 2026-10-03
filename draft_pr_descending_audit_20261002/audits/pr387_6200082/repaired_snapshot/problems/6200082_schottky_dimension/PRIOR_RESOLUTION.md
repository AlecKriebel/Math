# Credited negative answer to Problem82

The answer is no. There is a constant D<3, independent of the free group's rank and its representation, such that every free convex-cocompact subgroup of Isom(H4) has limit-set Hausdorff dimension at most D.

Credit belongs to Bowen's published2015 result, with the metric-measure approximation dependency repaired by Abért–Bergeron–Biringer–Gelander2021/2023. See SOURCE_GATE.md and CORRECTED_APPLICATION.md. No new discovery, optimal D, or quantitative evaluation of D is claimed. Proposed status already_solved0/5; independent review pending.

## Exact reduction to the established theorem

Let G be as in the original question. Convex cocompactness gives discreteness and finite generation. A free group is torsion-free, so its discrete action on H4 is free: a point stabilizer is a discrete subgroup of a compact orthogonal group, hence finite, and is therefore trivial. Thus the quotient is a complete hyperbolic manifold, as required by Bowen's geometric-action convention.

Free groups are residually finite. Every finitely generated subgroup, and each of its finite-index subgroups, is free and has a graph as a classifying space. Its ordinary second Betti number is zero. Consequently the full free-group family lies in Bowen's class G_2. A fixed torsion-free cocompact lattice in Isom(H4) is residually finite and has positive second L²-Betti number; these are precisely the lattice input and even-dimensional fact used by Bowen's Theorem1.2 and Lemma8.1. This checks the free-group case directly, without needing the more general hyperbolic3-manifold-subgroup application.

The resulting uniform Cheeger bound is h(H4/G)≥h_*>0. Cheeger's inequality gives λ_0(H4/G)≥h_*²/4. Choose c=min(h_*²/4,1)>0. Convex cocompactness has no cusps, and its full limit set equals its conical limit set. The Patterson–Sullivan spectral formula quoted and applied on Bowen's printed572 gives, whenever δ=dim_H Λ(G)≥3/2,

    λ_0=δ(3-δ).

Hence δ(3-δ)≥c and

    δ≤D=(3+sqrt(9-4c))/2<3.

If δ<3/2, the same bound is automatic because D≥(3+sqrt5)/2>3/2. Elementary trivial/cyclic groups have dimension0 and also cause no exception. The bound uses the standard round/visual metric on the sphere at infinity; changing the basepoint gives a smooth Möbius map on this compact sphere and preserves Hausdorff dimension. Arbitrary snowflake choices of a visual parameter are not being substituted.

The conclusion covers the broader free convex-cocompact clause, so no ambiguity about classical versus nonclassical Schottky terminology affects the answer. It does not assert a full-limit-set gap for arbitrary geometrically infinite free groups; the convex-cocompact hypothesis is essential to this exact application of the dimension formula.

## Proof-history and verification limits

The primary published corollary is the prior result being credited. This packet checks its application, the repaired approximation bridge and the elementary spectral algebra. It does not reproduce every proof of residual finiteness, L² approximation, Cheeger's inequality or Patterson–Sullivan theory from first principles. These classical dependencies are explicitly identified. The finite checker verifies only exact rational algebra and the combinatorial homology estimate used in the bridge; it is not a numerical proof of any analytic existence constant.
