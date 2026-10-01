# Turn 1: an exact general trace-probability formula

2026-10-01. One substantive author turn. Status: proved analytic reduction, general convergence unresolved. This formula is elementary finite Markov-chain analysis; no novelty assertion.

Take a finite connected loop-free undirected graph, positive edge conductances w, nest N and absorbing food F. Parallel nonterminal edges can be distinguished. Let L be the Dirichlet conductance Laplacian on U=V\{F}: its diagonal is the total incident conductance, and its off-diagonal entry is minus the total conductance joining the two vertices. Let G=L^{-1}. Positivity and invertibility follow from the Dirichlet energy and connectivity to F. We use conductance Green functions, not the discrete-time visit-count Green function (the two differ by vertex conductance).

For an edge e={u,v} with u,v∈U, let J_e have entries 1 in (u,v) and (v,u), and zero elsewhere, and let s_e=1_u+1_v. Then its trace probability is

    p_e(w) = w_e [ (L+w_e J_e)^(-1) s_e ]_N.          (1)

For a terminal edge e={u,F}, the formula instead is

    p_e(w)=w_e G_{Nu}.                               (2)

Proof of (1): declare success as soon as the chosen edge is crossed and failure as soon as F is hit. Before either event, the chosen edge contributes a killing rate w_e at each of its endpoints but no transition between them. The first-step equations, multiplied by total incident conductance, are exactly (L+w_eJ_e)p=w_es_e. Its matrix is positive definite: its quadratic form is the sum of the other conductance-edge energies, terminal killing energies, and w_e(|f(u)|²+|f(v)|²). Every component of the graph with e removed reaches F or one of u,v, so no nonzero zero-energy vector remains. Formula (2) is the usual last-exit flux: the edge can be traversed only as the final step. Equivalently, solve Lp=w_e1_u. This derivation is valid for the once-per-trace reinforcement rule, not a traversal-count surrogate.

For efficient analysis, write

    a=G_uu, b=G_vv, c=G_uv, s=G_Nu, t=G_Nv, w=w_e,
    Δ=(1+wc)²-w²ab.

A two-by-two Woodbury calculation gives

    p_e(w)/w = [s(1+w(c-b))+t(1+w(c-a))]/Δ.           (3)

The denominator is positive: it equals det(L+wJ_e)/det(L). Thus this formula introduces no extraneous sign branch or singular denominator for positive weights.

Two useful exact identities follow. First, p(tw)=p(w) for every t>0, since multiplying all conductances does not change the walk. Second,

    sum_{e incident to F} p_e(w)=1,                 (4)

because exactly one terminal edge occurs in every stopped walk. At any equilibrium p(w)=w, terminal weights sum to one. Every positive terminal edge {u,F} also forces G_Nu=1 there. This gives a concrete system constraining any proposed interior equilibrium or counterexample.

For the actual process, the published stochastic-approximation identity is

    X(n+1)-X(n) = [p(X(n))-X(n)+ξ(n+1)]/(n+2),

with bounded martingale-difference noise. Our reduction gives its entire rational drift on the strictly positive orthant, without enumerating infinitely many paths.

Remaining gap: rationality, the terminal simplex, and a finite equilibrium system do not imply a unique attracting equilibrium, exclude cyclic recurrent sets, or control boundary limits. The next turn attacks the dependence of a trace probability on its own reinforcement weight rather than assuming a global potential.
