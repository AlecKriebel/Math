# Independent comparison of the proof mechanisms

This derivation was made from the frozen candidate and primary manuscripts. It
does not infer the contents or date of an unavailable Angel--Hermon--Yao proof.
The primary-source byte identities are recorded separately. This is a check of
scope and mechanism, not an additional attempt to solve a missing theorem.

## Exact overlap, including connected components

Put `c=1-alpha`, `beta=alpha/c`, for `0<alpha<1`, and

`S_v(x)=sum_{e incident v} x_e^alpha`.

The candidate's equation is

`x_uv = x_uv^alpha (p_u/S_u(x)+p_v/S_v(x))`.

Qin's Theorem 1.1 has the identical equation and hypotheses on the graph,
exponent and rates. His positive real initial weights include the candidate's
positive integer initialization. His connectedness assumption supplies no
substantive unmatched generality: restrict to each connected component, apply
the theorem and intersect the at most countably many probability-one events.
Equilibria on the entire graph are products of component equilibria. Isolated
vertices do not affect any edge. Thus neither arbitrary disconnected graphs nor
small rate infimum creates a new theorem beyond that known result.

## The two deterministic equations describe the same structural reduction

For a complete bounded positive edge solution of the limiting ODE, set
`y_e=x_e^c` and `rho_v(y)=p_v/sum_{e incident v} y_e^beta`.
Differentiation gives

`y_uv'=c[-y_uv+rho_u(y)+rho_v(y)]`.

Variation of constants on `[s-T,s]`, followed by `T -> infinity`, removes the
bounded initial term and gives

`y_uv(s)=c integral_{-infinity}^s exp(-c(s-r)) [rho_u(y(r))+rho_v(y(r))] dr`.

Both terms in the integrand are positive. Therefore each separate endpoint
integral is finite and bounded by the common bound on `y_uv`. Define

`b_v(s)=c integral_{-infinity}^s exp(-c(s-r)) rho_v(y(r)) dr`.

Then `y_uv=b_u+b_v`, and coordinatewise differentiation of the convolution
gives

`b_v'=c[p_v/sum_{w~v}(b_v+b_w)^beta-b_v]`.

This is precisely the candidate's limiting vertex ODE. No uniform positive
lower bound on rates was inserted. Conversely, any positive vertex solution
of this ODE gives an edge solution by `x_uv=(b_u+b_v)^(1/c)`. This equivalence
shows that calling the basic power/incidence reduction new would be excessive.
It does not make the two rigidity proofs identical.

For the candidate, subtract the equilibrium `z` and let
`M=sup_{v,s}|b_v(s)-z_v|`. An approximate positive maximum at a coordinate
forces the adjacent sums to differ from their equilibrium sums by at least
`-epsilon`; a modulus of continuity bounds the denominator error. In that
strip the signed derivative is strictly negative. Completeness lets the same
coordinate be traced backwards inside the strip, contradicting boundedness.
The negative strip has the reverse sign. This needs neither an attained
supremum nor differentiation of an infinite supremum norm.

Qin instead compares two complete edge trajectories, forms divided differences
and integrated vertex differences, and proves a contraction estimate using
equality of the extra diagonal coefficient and off-diagonal row sum. That
argument establishes norm regularity before using a logarithmic norm. The
candidate's modulus/strip argument does not invoke that quantitative
contraction estimate or norm regularity. Both exploit the same underlying
balanced antitone interaction, but the propositions and intermediate estimates
are different. This supports the description "alternative proof", not a claim
of an entirely unrelated conceptual strategy or a stronger conclusion.

## Stochastic persistence is obtained differently

The candidate uses the discrete antiderivative

`H(n)=sum_{j=1}^{n-1} j^(-alpha)`.

At a reinforcement from `n` to `n+1`, the jump of `H` is exactly `n^(-alpha)`.
Multiplying that jump by the intensity `n^alpha q_e` gives compensator `q_e`.
The squared jump gives bracket integrand `n^(-alpha)q_e <= q_e`, since
`n>=1`. Thus the martingale normalized by the integrated compensator vanishes,
and local clock upper bounds imply positive linear growth. The accumulated
endpoint compensators also give the scaled vertex representation directly.

The comparison manuscript obtains persistence through a coupled pure-birth
chain, then applies stochastic approximation to the untransformed edge counts.
These are different auxiliary constructions. Both subsequently use local
coordinate bounds, logarithmic time, diagonal compactness and rigidity of
complete limits; those general tools are shared and standard.

## Equilibrium existence also differs

The candidate minimizes a strictly convex finite-volume vertex functional,
obtains bounds independent of volume at each fixed vertex and takes a diagonal
limit. The comparison manuscript uses a compact product of edge intervals and
a fixed-point theorem. Replacing one construction with the other is possible
after the result is known, but the candidate's submitted proof does not depend
on the comparison manuscript's fixed-point result.

## Literal counterexample and prior credit

On the integer line with unit rates, put two on a perfect matching and zero
on all other edges. At every vertex the denominator is `2^alpha>0`. For a
positive edge each endpoint contributes one, so its total is two; for a zero
edge both contributions vanish, for every `alpha>0`. Translating by one edge
gives another equilibrium, and the all-ones profile is a positive equilibrium.
Thus unrestricted nonnegative uniqueness is false even though positive
initial weights converge to the positive profile.

On an even cycle with uniform discrete vertex selection, the same calculation
instead gives positive weight `2/n`. The alternating cycle vector is displayed
in the 2014 finite WARM manuscript, Section 3.6, printed p.28. That paper states
stability for strong reinforcement; extending the equilibrium identity to
`0<alpha<1` is a direct calculation, not a reported stability theorem there.
The infinite-path construction is the same local matching mechanism and is
also explicitly recorded in Qin's Remark 1.3. It must not be advertised as a
new boundary construction.
