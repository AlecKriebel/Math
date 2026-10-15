# Correction of an invalid extension inference

The rejected implication was:

    Every ordinary coloring of G−e fails deletion-derived palette repair
    ⇒ no full list coloring can give e its exterior color.

This implication is false. A full list coloring with exterior set F containing e gives an A-coloring of G−F. That coloring need not extend to an A-coloring of G−e.

The explicit example in [METHODS.md, Section 6](METHODS.md#6-actual-critical-graphs-distinguish-the-methods) has no successful repair from any ordinary coloring of G−e1, but has the proper full list coloring (1,3,2,0,1,2,3). Its exterior set is {e1,e6}. The base-color restriction cannot extend across e6 because the missing ordinary colors at its endpoints are different.

All eight verified actual critical examples have positive full list colorings with their selected edge exterior. Six simultaneously have exhaustive negative certificates for the more restrictive deletion-derived repair scheme. These facts are checked independently. No forced-edge uncolorability or full-list counterexample is asserted in this method analysis.
