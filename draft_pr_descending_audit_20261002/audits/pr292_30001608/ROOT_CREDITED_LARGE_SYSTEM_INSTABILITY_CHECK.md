# Independent check of the credited large-system instability

This checks the relevant background claim in Norros–Reittu–Eirola,2011authorproof §3.2 equation(9)/Proposition3.5, also2009v1Prop3.3. It is an independent deduction from the displayed equations, not a new-priority assertion, recurrence proof or extrapolation from ODE to CTMC. ROOT visually read all operative2011authorpages10–12 and originalOWRprinted2782; source/model family separately authenticated exact primary PDFs. The correct scaling changes arrivalrate toNlambda and scales occupancy byN at fixed time; it is not the fixed-arrival/time-accelerated scaling.

Fixlambda>0. On positivevisiblecoordinates the equations are
 a'=lambda/2-ax/(x+y), b'=lambda/2-by/(x+y),
 x'=(a-y)x/(x+y), y'=(b-x)y/(x+y).

For everytheta>lambda/2 the point
 (a,b,x,y)=(theta,lambda theta/(2theta-lambda),lambda theta/(2theta-lambda),theta)
 is an equilibrium, by direct substitution. The family is unbounded as theta→infinity (a,y) and as theta↓lambda/2 (b,x). This equilibrium check alone does not prove the claimed open diverging region.

Take the open nonempty initial region y0>a0>lambda,0<x0<lambda/2,b0>k0, withk=lambda/2(1+x/y). DefineF=y-a andbeta=b-k. As long asF,beta>0,
 x'=-Fx/(x+y)<0,
 b'=-y beta/(x+y)<0,
 y'=lambda/2-xy/(x+y)+y beta/(x+y)>lambda/2-x0=:delta>0,
 k'=lambda/2(x'y-xy')/y^2<0,
 beta'=-y beta/(x+y)-k',
 F'=y beta/(x+y)-xF/(x+y).

Variation of constants in the last two scalar equations preserves strictbeta,F positivity up to every finite time in the region: -k'>0 and ybeta/(x+y)>0 supply nonnegative forcing, while their initialvalues are positive. The other boundaries cannot be crossed: x remainspositive at finite time by its multiplicative equation and nonincreasing; y increases; and a'=lambda/2-ax/(x+y)>=lambda/2-x0=delta because0<a<y. These inequalities give a≥a0+delta t and y≥y0+delta t, hence both diverge. Allvariables exist for allfinite t:0<x<=x0,lambda/2<b<=b0,0<a'<lambda/2,0<y'<=b0. Consequently finite-time blowup or a singular visible denominator cannot invalidate the argument.

Finally,b decreases to a finite limit>=lambda/2. Sincey→infinity andx isbounded, y/(x+y)→1; if thatlimit were>lambda/2, the equationb'=lambda/2-b y/(x+y) would eventually bebounded above by a strictlynegative constant, contradiction. Thusb→lambda/2. No assertion thatx→0 is needed (the source only saysxdecreases). This proves the credited open set of trajectories witha,yunbounded andb,xbounded, with its symmetric counterpart.

The source conjecture asks whether the exact stochastic chain remains positive recurrent despite this already-known large-system behavior. This note verifies that background implication premise without presuming the stochastic conclusion. Allfixedfinitepositiveλ is the candidate stochastic claim; no stationary-measure limit or load-uniformbound has been established.

ActualROOTcheckpointUTC 2026-10-05T18:39:33.614516+00:00; backgroundODEverification100%, candidateall-loadmathematicalreview65%, priority0%, workflow0%.
