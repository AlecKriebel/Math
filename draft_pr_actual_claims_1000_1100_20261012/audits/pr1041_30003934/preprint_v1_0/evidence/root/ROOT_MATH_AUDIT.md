# Combined root mathematical audit: PR #1041

The full coNP-completeness assertion passes the root derivation and two
fresh independent adversarial mathematical families. Head:
`ad138ddd5bd1a51c0f225f03342c0c058873f790`, problem 30003934. Priority and
the submission-ready preprint/package remain pending. This is AI mathematical
review, not conventional human peer review or formal verification.

## Exact target and source domain

UNIQUENESS means exactly one mixed-strategy pair in explicitly listed rational
bimatrix games, variable positive dimensions, rank(A+B)=1 exactly, and arbitrary
degeneracy. It is coNP-complete. The reduction supplies a known strict pure
equilibrium, unique in no PARTITION instances and accompanied by another pair
in yes instances. No nondegenerate promise, strong hardness, fixed-dimension
hardness or payoff-uniqueness conclusion is accepted.

Use the NP-complete source problem of nonempty positive-integer PARTITION
instances. This explicitly avoids S=0 from an empty source list without
weakening hardness for the target. A future paper must state this domain.
The original problem source at OWR 38/2018 printed p.2332 matches the target;
its historical conjecture is not proof of current worldwide openness.

## Source-flow obligation

The explicit two-gadget DAG matches Disser–Skutella's complete Lemmas 3.1–3.2
and figures, rather than relying on Corollary 1.7's shorthand. Its all-legitimate-
SSP execution proof forces bridge use exactly when a signed partition sum is
zero: a forward unit rise from zero to one is immediately reversed by the
next unit augmentation. The half-step gives e-flow 1/2 at q<=F-3/2.

The ternary perturbation preserves every nonzero original simple-path cost
comparison, because differences lie in (1/D)Z and the perturbation of a
comparison has magnitude below 1/(4D). Coupling keeps the two residual states
identical at each step; a perturbed shortest path is an allowable original
shortest path in that same state. It is not enough to compare paths from
different executions. A nonzero projected simple residual cycle cannot have
zero perturbed cost: either its original nonzero sign persists or its first
nonzero ternary term dominates the tail. Formal arc/reverse two-cycles have
zero projection and change no flow.

Distinct fixed-real-q optima have a nonzero sign-conformal residual circulation.
Cycle decomposition and optimality force a nontrivial zero-cost cycle, a
contradiction. This proves uniqueness for every real flow value. For fractional
SSP augmentation, any competing value-(q+Delta) flow difference decomposes
into residual paths of total Delta and nonnegative-cost cycles. Its cost is
at least Delta times the shortest residual path cost; the interpolated path
flow attains that value. Thus midpoint optimality is a proof, not an integer-
vertex interpolation assumption. A topological potential makes every original
arc cost strictly positive, preserving fixed-value optima, residual path
comparisons and cycle costs. The network encoding is polynomial; its
exponential SSP execution is used only in correctness, not construction.

Two upstream printed slips were independently noticed in the root's direct
source reading and the new flow review. The i=1 second path cost is 1-v1,
not the printed -v1; the post-base-adjustment envelope includes +/-epsilon/5.
The actual arc formulas, general state formula and strict state separation
resolve both. They do not create a missing premise in the submitted argument.

## Simplex, uniform penalty and complete game exhaustion

The simplex mapping f_i=LF x_i, h=F(1-x_0), q=h-Kf_e has a unique inverse
in (f,h), including its slack coordinate, and q>=h/2>=0 everywhere in the
simplex. Scaling a zero-e maximum flow proves LP feasibility for every real
lambda in [0,F]. DAG path decomposition gives sum f<=Lq. The no-instance
unique unrestricted optimum remains feasible in the restriction; all
restricted optima are therefore the same flow. The yes midpoint has
h=q+K/2<F and q<F-epsilon, so neither simplex clipping nor parameter bounds
remove it. Here "unrestricted optimum" always uses the perturbed, potential-
shifted costs, as must be made explicit in a future note.

The dual feasible polyhedron is rational, independent of lambda, nonempty
and pointed. Its attained optimal face has a vertex of that polyhedron even
at degenerate or irrational parameters. Clearing constraint denominators and
Cramer's rule bound every such multiplier's l1 norm by one polynomial-bit C.
With M=C+1, the penalized objective is at least the feasible optimum plus
(M-C) times the maximum violation. Every infeasible point is strictly worse.
This controls all minimizers uniformly, not only a chosen basic solution.

The auxiliary zero-sum row minimax is exactly this penalty with b_j=-Ms_j.
The opposite parameter inequalities make b nonzero, and a_0=-epsilon makes
a nonzero, so A+B=ab^T has exact rank one. At lambda=a^T x=h-epsilon,
the complete original and auxiliary best-response sets coincide. This gives
both directions for every support and opposing-strategy degeneracy.

Every candidate parameter lies in [-epsilon,F-epsilon]. For lambda<0,
the q-lambda violation and q>0 away from pure row zero force that row to be
the unique optimizer. Its sole crossing is -epsilon. There the diagnostic
column is the unique best response; the pair is strict for both players.
For nonnegative lambda, exact penalty forces q=lambda and the hyperplane
forces f_e=1/2. At lambda=0 a DAG value-zero flow is zero. The no-case
all-optimal flow statement excludes every nonnegative crossing; the yes
midpoint supplies one. This exhausts every pair and continuum, not just a
selected equilibrium path. All matrix sizes and binary encodings, including
the large determinant-bound M, are polynomial in the source length.

## Membership and verification limits

The equilibrium set of any rational finite bimatrix game is a finite union
of compact products of rational best-response support polytopes. Closed
cells with some zero declared probabilities add no nonequilibria. If the
union is nonsingleton, its cell vertices include two distinct rational pairs.
Active normals span the ambient space at each vertex even in lower-dimensional
cells; Hadamard and Cramer give polynomial numerator/denominator bounds.
Exact simplex, best-response and distinctness tests verify the two witnesses
in polynomial time. Nash existence makes the complement exactly uniqueness.
Rank-invalid inputs form a polynomial-time complement branch, giving the
ordinary rank-one language as well as its promise interpretation in coNP.

The root read the full current proof and certificate report and both full
fresh reports/derivations, and directly read/rendered the complete controlling
DS gadget and lemma pages. Both fresh families preserve early independence
and mutually discharge their exact conditional premises. The fresh flow
checker tests 37 instances, 660 augmentations/half-flow certificates and
864 cycles per normal/optimized run, with four negative controls. The game
family tests six full games, 204 auxiliary pairs, strict default pairs and
all-minimizer/certificate negative controls. These are actual new checks,
not replacements for the quantified proof or alleged replays of omitted
historical scripts.

All eleven original Git files/full tree remain frozen at the exact head.
The original theoretical edition contains no executable, fixture or check
log. Its six-game/39-network script references remain historical; the future
preprint must distinguish them from included fresh verification. The game
review's private sources use an ignored rawprivate subfolder; that entire
folder, like every raw source body, must be excluded from public packaging.
No actionable mathematical gap remains under the stated source domain.
Global exposition must include these domain, optimizer terminology, version-
specific Adsul theorem-number and computational-history clarifications.
Novelty and current worldwide status require a separate priority audit.
