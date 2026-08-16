# Exact JC effect of every active cleanup operation

## Ordinary degree-two suppression

Two serial ordinary JC edges with multipliers `x1,x2` have effective multiplier

\[
x=x_1x_2.
\]

The map is onto `(0,1)`, has nonzero differential there, and has the strict analytic section

\[
x_1=(1+x)/2,\qquad x_2=2x/(1+x).
\]

Thus suppression preserves the complete open tensor image and is a positive analytic submersion.

## Root-created parallel pair: the zipper

In the only tree-child full-network cleanup artifact, the parallel copies have the same arrowhead at the root-child reticulation. The complete two-terminal tensor has nonzero multiplier

\[
\kappa=uv\{\lambda\alpha\beta+(1-\lambda)\gamma\}.
\]

It equals the complete open model of one ordinary JC edge. The explicit strict section and nonzero derivative are proved in `docs/THEOREM_Q_PROOF.md` and independently replayed by two algebra implementations.

## Parallel ordinary copies in restrictions or displayed networks

This is a different operation from forming the full semi-directed topology. If alternatives have effective JC multipliers `r,s` and mixing weight `lambda`, identification gives

\[
\lambda r+(1-\lambda)s.
\]

The diagonal section `r=s=x` realizes every `x in (0,1)`. This formula is used only where the cited restriction/displayed-network convention performs that identification.

## Reticulation and 2-sub-blob cleanup

The full convention comparison does **not** silently suppress arbitrary 2-sub-blobs. The only reticulation removed while forming a full strong topology is the root-created zipper reticulation above, for which exact open-image equality is proved. More general 2-sub-blob suppression is a separate statistical transformation: it is not part of `q` and no equality beyond the special zipper is asserted here.
