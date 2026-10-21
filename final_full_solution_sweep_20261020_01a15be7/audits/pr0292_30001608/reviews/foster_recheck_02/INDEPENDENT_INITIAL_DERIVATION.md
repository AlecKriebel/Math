# Independent initial derivation

Written before reading the proposed proof or inherited mathematical reviews.

For f(a,b,x,y), Lf is the sum over the six indicated transitions of rate times f(new)-f(old). Arrivals increase U=a+x or V=b+y at rate lambda/2; downloads preserve the corresponding quantity; departure decreases it by one. Thus the population identities recorded in RESEARCH_LOG.md follow immediately, and subtracting gives L(U-V)=(y-x)/(x+y+1).

The total departure rate equals (2xy+x+y)/(x+y+1). At x=y=0 this is zero, and at y=0 it approaches one as x increases. A proposed proof using a fixed multiple of total population without a state-dependent correction cannot give negative drift for lambda >= 1 along this corridor. Conversely, at x,y >= k, the departure rate is at least approximately k+1 and hence overwhelms any fixed finite lambda for large enough k.

These observations suggest dividing states into an interior with enough completed jobs of both types, a low-completion region where waiting populations directly drive downloads, and a one-type corridor requiring a corrector for rare-type accumulation. They do not themselves prove recurrence.
