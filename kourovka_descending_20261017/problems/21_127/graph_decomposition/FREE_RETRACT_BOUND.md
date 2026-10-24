# A checked free-retract lower bound for the explicit P4 chain

The exterior words g1,g2 in `P4_PROMOTION_OBSTRUCTION.md` retract, upon killing b,d, to

    h = acacAcACCC,
    h' = ACCCacacAc.

Here h' is the cyclic rotation of h beginning at position 6 (positions start at 0), so these words represent the same conjugacy class in the free group F(a,c). Thus the image of the exterior chain is 2h in the usual homogeneous chain space.

Direct free reduction verifies

    h = [acacA,cACA]
      = a [cac,AcAC] a^-1.

The word h is freely and cyclically reduced and nonempty. The universal upper bound for a commutator is 1/2. The standard 1/2 gap for nontrivial free-group elements in the commutator subgroup gives the opposite inequality. One can use the stronger published RAAG gap as a source: Heuer, *Gaps in scl for Amalgamated Free Products and RAAGs*, arXiv:1802.01107v3, Theorem 7.3, applies to this free RAAG. Therefore scl_F(a,c)(h)=1/2. Monotonicity under retraction and homogeneity/conjugacy invariance on chains yield

    scl_G(g1+g2) >= scl_F(a,c)(2h) = 1.

Together with the explicit cover-and-cap construction, the conclusion is only

    1 <= scl_G(g1+g2) <= 2.

The exact fixed-block relative cost 2 is not asserted to be the absolute scl of this chain, nor does a chain bound determine either individual element's scl.

`check_transport.py` checks both commutator identities, the cyclic rotation, and the two retraction words by exact free reduction. A separate exploratory `free_turn_probe.py` also finds value 1/2 from a 133-circuit, 26-edge free-group turn LP, with exact Fraction primal/dual verification; the direct commutator proof avoids relying on that implementation to establish this bound.
