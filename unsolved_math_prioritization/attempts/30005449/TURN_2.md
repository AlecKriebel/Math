# Turn 2: own-edge concavity and coordinate equilibrium uniqueness

2026-10-01 06:15 UTC. Second substantive author turn. Status: a proved general negative-feedback property; no proof of the full deterministic-limit conjecture.

Fix all conductances except one edge e={u,v}, and call its variable conductance t>0. For a terminal edge v=F use just u below. Delete e and run the continuous-time conductance walk on the remaining graph, with generator rates given by the other edge conductances. Stop at its first hit of F, if any. Let L_e be its total occupation time at {u,v} before that stopping time. On a component from which F is unreachable, interpret the stopping time and, when appropriate, L_e as infinity.

An independent killing clock of rate t per unit occupation time at {u,v} represents the first crossing of e. Up to that crossing it has exactly the same competing jump rates as the original walk. Stopping at the crossing records the desired event, so

    p_e(t;w_{-e}) = 1-E[exp(-t L_e)],              (1)

with exp(-t∞)=0. For a terminal edge, delete that edge and regard killing at u as reaching food through the specified edge. Other food edges still cause failure. The same formula applies. This is a first-crossing representation, so the event is a trace event, not an expected traversal count.

When e is deleted, every relevant finite component either reaches F or one of e's endpoints. In a finite closed component containing an endpoint, that endpoint is visited infinitely often and its occupation time diverges. Thus the infinity convention accounts correctly for bridges and does not lose any probability.

For every t>0, differentiation under the expectation is justified by boundedness of L_e^k exp(-tL_e) on finite L_e (the infinity contribution is zero). It yields

    p'_e(t)=E[L_e exp(-tL_e)]≥0,
    p''_e(t)=-E[L_e² exp(-tL_e)]≤0.                (2)

More generally (-1)^(k+1)p_e^(k)(t)≥0 for k≥1. In particular,

 t² d[p_e(t)/t]/dt
    =E[(1+tL_e)exp(-tL_e)-1]≤0.                   (3)

The inequality in (3) is strict whenever the edge is accessible before absorption with positive probability. The integrand is strictly negative at every finite positive occupation time and equals -1 when L_e=∞. An inaccessible edge has p_e≡0 and is already harmless for normalized convergence.

Consequences for the exact drift from turn 1:

1. With all other weights fixed, p_e(t)=t has at most one positive solution. If it exists, it lies in (0,1]. This is a genuine coordinate uniqueness statement, not uniqueness of the coupled vector equilibrium.
2. At every strictly positive equilibrium w=p(w), every diagonal derivative of F=p-w is strictly negative:

       ∂F_e/∂w_e = p'_e(w_e)-1
                   =p'_e(w_e)-p_e(w_e)/w_e <0.

3. If deletion leaves F accessible and E[L_e]≤1, then there is no positive coordinate equilibrium unless the degenerate law makes the strictness fail. For an accessible edge with P(0<L_e<∞)>0, strict concavity gives p_e(t)<t E[L_e]≤t. When E[L_e]>1 (including infinity), the ratio starts above one at zero and decreases; if p_e(1)<1, there is exactly one positive coordinate equilibrium. If P(L_e=∞)>0, the ratio instead diverges at zero and the same crossing conclusion applies.

These results explain why linear trace reinforcement can create coordinatewise negative feedback, despite the nominally linear weight update. They do not prove a global contraction: another edge's conductance may alter access to e in either direction. Negative diagonal derivatives do not imply that the full Jacobian is stable, and coordinate uniqueness does not exclude multiple coupled equilibria or recurrent sets.

Remaining gap: global structure of the multi-edge ODE and boundary avoidance. The next route explicitly tests whether the natural per-capita drift can be a gradient, rather than assuming an unproved Lyapunov function.
