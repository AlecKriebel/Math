# Additional adversarial priority mechanism: punctured disc

Timestamp: 2026-10-13T04:19:21.246946+00:00

This is a separately derived mathematical inference prompted by full primary inspection of Herron (1987), section 3.2, and Bear–Smith (2005 author manuscript / 2006 publication), Proposition 2.6. It is not a claim that those authors stated or recognized a solution of Hayman–Lingham Problem 7.42. It supplies a different counterexample to the same expressly chosen equality-along-line universal interpretation, without deriving the submitted exact annular theorem.

Let D*={0<|z|<1}, a=1/2, and let K(z)=3(1−|z|²)/|z+1|², the disc Poisson kernel at −1 normalized at a. It is also a minimal Martin kernel on D*: removing a polar point does not change Green functions (alternatively, exhaustion by discs with a shrinking circular hole shows the correction tends to zero). Any nonnegative harmonic minorant bounded by K is bounded near 0, so it extends harmonically to the full disc; ordinary disc Poisson minimality then proves its proportionality to K. Thus puncture removal does not destroy minimality of this boundary kernel.

Choose the two normalized disc Poisson kernels Q+ and Q− with poles ζ±=−1/2±i√3/2, and L(z)=log(1/|z|)/log2. They are strictly positive harmonic functions throughout D*, with value one at a. In Cartesian coordinates at a, direct differentiation gives

    ∇K(a)=(−8/3,0),
    ∇L(a)=(−2/log2,0),
    ∇Q±(a)=(−52/21,±4√3/7).

Since e^(3/4)>1+3/4+(3/4)²/2+(3/4)³/6>2, log2<3/4 and 2/log2>8/3. Also −52/21>−8/3, because −8/3=−56/21. Hence ∇K is strictly inside the triangle with vertices ∇L, ∇Q+, ∇Q−. This is exact, without decimal approximations.

For completeness put δ=2/log2−8/3>0. The three gradient differences from K are (−δ,0) and (4/21,±4√3/7). For a nonzero displacement d=(u,v), their maximal dot product is

    max{−δu,(4/21)u+(4√3/7)|v|}.

If u<0 the first is positive. If u≥0 the second is positive unless u=v=0. This function is continuous on the unit circle and strictly positive there, so it has a positive minimum. The finite smooth family has a common quadratic remainder near a; therefore max(L,Q+,Q−)>K at every nearby non-base point. The Harnack envelope dominates that maximum, yielding K<H_a in a punctured neighborhood.

The deduction is elementary once the older punctured-domain representations and standard disc kernels are available. It reinforces the historical-priority gap. It does not establish which earlier author first made this deduction, and it does not show that the submitted annular theorem is a direct corollary of the cited metric-equality statements. The dated audit’s claim that no immediate implication of the *selected annular kernel’s* interior-gradient result was established remains compatible with this inference. Broad claims that the universal negative answer could not follow immediately from older classical facts would require qualification; the submitted paper makes no such historical-first claim.

Primary locators: https://www.jstage.jst.go.jp/article/kodaimath1978/10/1/10_1_9/_pdf/-char/en and https://math.hawaii.edu/~wayne/mathpapers/harnack.pdf. Download hashes are in PRIORITY_FETCHES_INDEPENDENT.json. This note is authored reasoning; it contains no copied third-party source passages.
