# Route 5: trying to realize concentrated potentials by a semilinear solution

## Why prescribing a stable potential is insufficient

A counterexample must produce one common nonlinearity F=lambda* f and a source-admissible extremal solution u with

    -Delta u=F(u),   V=F'(u).

For a smooth pair, differentiating gives the necessary identity

    grad(-Delta u)=V grad u.                                  (1)

If F'' exists, one also has grad V=F''(u) grad u; thus grad V and grad u are parallel. Globally, -Delta u must take the same value on every component of a level set of u. These are restrictive compatibility conditions. Solving a linear equation using the spiky V of Route 2, or solving -Delta u=h(x) with a prescribed peaked h, does not establish them. An inverse definition F=(-Delta u) composed with u^(-1) is available in a strictly radial monotone coordinate, not for a general function of n variables.

In the radial case, such an inverse construction plus F''>=0 forces F'(u(r)) to be radially nonincreasing, and the known bound of Route 1 applies. Hence a radial realization cannot turn the Route 2 obstruction into an admissible counterexample.

## Exact angular construction test for the exponential model

The natural first nonradial ansatz is

    F(s)=lambda exp(s),   u(r,theta)=-2 log r+psi(theta).

The equation holds on a punctured ball exactly when

    -Delta_(S^(n-1)) psi + 2(n-2)=lambda exp(psi).              (2)

Its potential satisfies the exact identity

    r^2 V(r,theta)=lambda exp(psi(theta)).                     (3)

Every smooth profile on the compact sphere is bounded, so every such separated solution obeys the target upper estimate. Allowing an unbounded angular profile creates a singular ray at nonzero radii; this violates the assumed isolated singularity. Thus this ansatz cannot produce the requested counterexample. Boundary values are not automatically zero on an arbitrary smooth domain either.

## What a scale-dependent profile would have to accomplish

For the same exponential model, write t=-log r and

    u(r,theta)=2t+w(t,theta).

Direct computation gives the exact cylindrical equation

    -w_tt+(n-2)w_t-Delta_S w+2(n-2)=lambda exp(w).              (4)

For test functions phi(r,theta)=r^(-(n-2)/2) zeta(t,theta), compactly supported away from r=0, the stability inequality becomes

    integral [|zeta_t|^2+|grad_S zeta|^2+H_n zeta^2]
        >= integral lambda exp(w) zeta^2,                     (5)

where H_n=(n-2)^2/4 and both integrals use dt times sphere area. The cross term in the radial energy integrates to zero. The target in this special model is precisely an upper bound on w as t->infinity.

A potential construction would have to solve (4), preserve (5), keep w finite on every finite cylindrical slab, let its supremum diverge along t->infinity, and extend to the required zero-Dirichlet extremal branch. A chosen spiky function generally fails (4); (5) alone allows concentration. No such compatible profile has been constructed here, and no theorem excluding it has been proved. We do not assert that solving this special exponential subproblem would settle arbitrary convex f.

## Exact remaining gap and stop

The five bounded routes have neither established a uniform nonlinear nonconcentration estimate nor constructed a compatible source-admissible extremal counterexample. The nonlinear realization and extremal-branch conditions remain unsolved. No full candidate exists. This is the fifth and final substantive route; subsequent work on this packet is verification and reporting only, not continued proof search.

Status: unfinished after five routes. No novelty claim.
