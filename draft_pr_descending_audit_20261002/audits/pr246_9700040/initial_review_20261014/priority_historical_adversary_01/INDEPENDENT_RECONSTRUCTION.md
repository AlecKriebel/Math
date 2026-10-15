# Independent reconstruction before source/review comparison

UTC: 2026-10-15T03:52:25.686728+00:00. Completion estimate: 10% of this scoped priority audit.

I have read only the parent task, the source-file inventory and retrieval receipt, and directory names. I have not read any inherited review, other priority-family report, or candidate proof. The following reconstruction is independent of their arguments.

## Exact comparison target

The target process has ordered positive locations X_1<X_2<...; deterministic drift dX_i/dt=X_i; unit area Poisson events (u,t) move the first particle strictly right of u to u. The requested output is the simultaneous stationary law, with an explicitness standard left qualitative by the question. Distinguish (A) a stationary construction; (B) all finite-dimensional joint probabilities via a finite/infinite combinatorial formula; (C) an algorithm with rigorous truncation control; and (D) historical firstness. A does not automatically establish B or D.

## Independent mapping

Start with a homogeneous PPP on (0,infinity)^2, process points by their second coordinate s, and run ordinary nearest-right Hammersley insertion from an empty boundary at s=0. For each x, the number of particles <=x is the increasing-chain length L(x,s), because patience sorting places an incoming value on the first larger pile top. Thus Z_i(s)=inf{x:L(x,s)>=i}.

Set s=exp(t), X_i(t)=s Z_i(s). Between events dX_i/dt=X_i. Under u=s z and t=log(s), dz ds=du dt, so points yield unit-rate events with the same nearest-right update. PPP scaling makes s Z(s) have an s-independent law. This is the correct stationary-law mapping; it needs suitable local construction for infinitely many particles, but it gives a checkable equivalence target.

At a single horizontal cutoff x and s=1, L is the LIS of a Poisson(x)-length uniform random permutation. For several cutoffs x_1<...<x_m, the same permutation/RSK history is required, not a product of its single-cutoff laws. Conditional on strip counts, one may use nested Young diagrams/standard skew tableaux to count successive first-row constraints. Therefore pre-existing Poissonized RSK growth formulas are a serious coverage candidate only if the mapping from that growth process to this stationary law is stated or follows by a fully explicit derivation. An old one-time LIS distribution by itself is insufficient.

## Falsifiable historical tests

1. Do 1993/1995/1999 sources already define this law through all scaled pile tops, its joint random-rank representation, or this exact PPP inverse-LIS construction?
2. Does a random-rank representation leave its own joint input unspecified? If so it can specify a law only when the rank law is independently known.
3. Is there an earlier explicit joint formula, or only first two particles, marginals, asymptotics, and conjectures?
4. Do direct progeny turn earlier constructions into a genuinely automatic all-law description with no unsupported central step?
5. Would any claimed coverage survive differences in jump convention, scaling, boundary conditions, or whether the process is the full ordered particle law versus one LIS marginal?

No conclusion about priority is made at this stage. No external outreach is authorized or needed.
