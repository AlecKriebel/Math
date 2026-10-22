# Turn 3: a natural global-potential route fails

2026-10-01 06:19 UTC. Third substantive author turn. Status: exact obstruction to the proposed gradient mechanism, plus a finite diagnostic search; general deterministic convergence remains unresolved.

A tempting use of turn 2 is to seek a scalar H with ∂H/∂w_e=p_e(w)/w_e. The equilibrium equations would then be critical-point equations for H−sum w_e, and strict concavity might force a unique limit. This would be a useful global argument, but it is false even on an admissible simple triangle.

Take edges a={N,F}, b={N,U}, c={U,F}, all positive. No parallel food edge is present. The exact trace probabilities are

    D=ab+ac+bc,
    p_a=a(b+c)/D,   p_b=b/(a+b),   p_c=bc/D.

For p_b, crossing b occurs exactly when the first step is N→U. The two terminal probabilities follow either by first-step equations or turn 1. Therefore the per-capita probabilities q_e=p_e/w_e satisfy

    ∂q_a/∂b = -c²/D²,
    ∂q_b/∂a = -1/(a+b)².

At a=b=c=1 these are -1/9 and -1/4. Their difference is 5/36, so the field q is not the gradient of any C² scalar potential on the positive orthant. Nor does any fixed positive diagonal weighting repair this: equality of the corresponding cross derivatives would require

    d_b/d_a = c²(a+b)²/(ab+ac+bc)²,

which depends on c. Thus the simple separable weighted-gradient/concavity route is blocked. This does not rule out a state-dependent metric, a non-gradient Lyapunov function, or a different global mechanism.

## Counterexample search diagnostics

The reproducible script explore_turn_3.py computes the exact drift using finite killed-edge linear systems, rather than Monte Carlo transition estimates. It tested a fixed-seed sample of twenty connected simple graphs with five or six vertices, at least one cycle, and no direct N–F edge. Three initial states per graph were constructed as averages of genuine stopped-walk traces, with the initial unit baseline; they respect the trace-polytope constraints instead of using arbitrary points of the cube.

Sixty ODE integrations reached time 50. The largest final spread between the three trajectories of one graph was about 0.00693, and the largest remaining drift about 0.000615. These residuals are not small enough to identify exact equilibria or infer nonuniqueness. The search did not produce a rigorously isolatable pair of distinct equilibria or a stochastic counterexample. A 10^-12 weight floor was used in the numerical evaluation, so even stronger apparent convergence would not certify the boundary dynamics. The complete graph list and diagnostics are retained.

## Gap and next direction

Coordinatewise strict negative feedback from turn 2 is compatible with nonzero curl and does not yield a global potential. The finite search neither proves uniqueness nor proves its failure. Even unique equilibria would still require global attraction and stochastic boundary control before deterministic almost-sure convergence followed.

The next turn attacks a full structural graph class using the resistance formula for edge-hitting probabilities. It will retain exact boundary-zero behavior rather than assume every edge survives.
