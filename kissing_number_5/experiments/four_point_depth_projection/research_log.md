# Research log

## 2026-07-23

- Initialized the isolated audit.
- Imported exact theorem C088: every hypothetical 41-code has at least seven
  points below \(-1/300\) and at least seven above \(1/300\) in every unit
  direction.
- Imported the audited pointwise common-pair theorem: a base pair of inner
  product \(q\le0\) has at most
  \(M(2b^2/(1+q))\) common neighbors whose two incident inner products are at
  least \(b\).
- Imported the exact four-point special case: if \(q\le-11/25\), there is at
  most one common neighbor at level \(b=499/1000\).
- First bottleneck: robust depth supplies one-coordinate height information
  in the \(y+z\) direction, whereas common-pair capacity requires simultaneous
  coordinatewise lower bounds against both \(y\) and \(z\).  The difference
  coordinate \(\langle x,y-z\rangle\) is uncontrolled unless a second depth
  or discrepancy argument is coupled to the same points.
- First found an exact rank-six countermodel from \(E_6\): all 32 spin
  roots, four antipodal \(D_5\) lines, and one extra \(D_5\) root.  It
  passed every nonpositive-code-base capacity but failed the separate
  positive contact-base cap seven, so it was superseded.
- A second search found a stronger exact \(E_6\) subset: 20 explicitly
  listed antipodal lines plus one extra root.  Its 41-point Gram matrix has
  rank six, maximum off-diagonal entry \(1/2\), and every contact base has
  at most seven common contacts.
- Certified robust \(\pm1/300\) depth using a 20-line antipodal core.  Every
  14-line frame operator exceeds \(I/4\); all 38,760 subsets pass exact
  integer Sylvester checks.  Therefore at least seven line pairs have
  absolute height \(>1/300\) in every direction.
- Enumerated the full \(E_6\) common-contact counts.  The stronger selected
  subset has maxima \(0,1,5,7\) at base inner products
  \(-1,-1/2,0,1/2\), so it passes every numerical code-base capacity,
  including the positive contact-base cap.
- Conclusion: robust depth, all code-base common-pair capacity shadows,
  edge-conditioned graph covariance, and all local four-point Gram-PSD tests
  are compatible at \(N=41\).  The exact missing hypothesis is global
  rank at most five; the countermodel has rank six.
- Derived the strongest immediate base-pair bridge from robust depth:
  exact lower counts in the four half-planes cut out by \(a+b\) and
  \(a-b\).  These half-planes do not contain the common-neighbor quadrant,
  and the same \(E_6\) countermodel satisfies all of them.
- Scope audit: the stronger arbitrary-axis projection family does reject
  the countermodel.  A stored five-clique is simultaneously at height
  \(1/2\) from two auxiliary axes of inner product \(-1/6\), giving five
  points where the dimension-five residual capacity is four.  The
  degree-two \(S^4\) harmonic sum also rejects it, at \(-181/4\).
- Tested the full continuum of exact pair-conditioned depth rows from
  \(\lambda y+\mu z\) against the new centered all-degree quarter-grid BV
  witness.  All 250 algebraic critical slopes, open cells, strict
  boundaries, projective infinities, signs, and base strata pass.  The
  global rational slack is
  \(9426027066077596589/342712500000000000>0\), so every triple-level
  half-plane extension is subsumed by the new barrier.
- Isolated a genuinely four-point common-source row.  For each base edge,
  \((H_e-7)(M_e-\Gamma_e)\ge0\); its expansion contains
  \(\sum_eH_e\Gamma_e\), a four-distinct-point count because the negative
  depth tail and positive common neighborhood are disjoint.  Pair/triple
  marginals cannot recover this edgewise covariance.  The rank-six
  countermodel still passes it, so a rank-five coupling remains necessary.
- Audited the stored 51-atom symmetric local Gram-PSD `K5` extension.  The
  exact without-replacement row is
  \(247P\le13MH+91\Gamma-7ME\) in the disjoint case.  The stored extension
  violates the \(q=-1/2,M=1\) and \(q=-1/4,M=3\) rows exactly.
- Generalized the product audit to every depth half-plane.  With
  sampled intersection \(i=h\cap g\) and depth lower bound \(r\), the
  correct row is
  \(247hg-234i\le13Mh+13rg-rME\), equivalently
  \(247c+13i\le13Mh+13rg-rME\) for the sampled distinct-pair count \(c\).
- Solved the amended local marginal LP and exactly reconstructed a
  64-atom alternative `K5` extension.  It matches the original
  pair/triple marginals, every atom is Gram PSD, and all 560 exact
  direction/capacity rows pass.  Thus the product family refutes one sparse
  extension but not local `K5` feasibility.  Global overlapping-subset,
  Lasserre/moment PSD, and rank-five consistency remain absent.
