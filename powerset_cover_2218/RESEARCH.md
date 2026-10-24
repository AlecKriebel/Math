# Erdős 624: unrestricted powerset cover threshold

Date: 2026-10-21. Queue 1866, database ID 2218. Status: partial analysis only; the requested divergent-excess conjecture is not proved or refuted here. This report contains authored mathematics, not copied source text. The source recovery gate is `SOURCE_GATE.md`; its live-status caveat remains in force.

## Exact problem and variant ledger

For a set X of n>=1 points, define H_u(n) to be the minimum h in {0,...,n} for which some map f:P(X)->X has f(P(Y))=X for every Y with |Y|>=h. All subsets, including the empty set and Y itself, are allowed as inputs. One f must work for every Y. Checking exactly h-element Y suffices, because every larger Y contains an h-element subset.

The target is H_u(n)-log_2(n) -> +infinity through all positive integers n. In particular, a fixed positive excess, a constant fraction of missing colors on some log-sized set, or an unbounded subsequence does not prove it.

- Exterior variant H_e: require f(A) in X\A for every proper A⊊X, and use all proper-domain inputs A⊆Y. No exterior value f(X) exists. For n>=2 this variant has a finite threshold at most n: f(X\{x})=x forces coverage on X. For n=1, f(empty)=the sole point gives threshold 0. An exterior map extends arbitrarily at X to an unrestricted map, so H_u<=H_e. The reverse implication is not justified.
- Empty-input omission removes one input from every ideal. A necessary count becomes 2^h-1>=n. This is not the present definition.
- Strict inputs A⊊Y likewise give only 2^h-1 inputs for an h-set. This condition must not replace A⊆Y.
- An independent or free set requires its images to avoid that set; it is a different property. Lower bounds for the historical independent-set parameter h(n) are not lower bounds for H_u(n).
- At n=2^k, H>=k+1 and H>k+1 are different integer assertions: the latter is H>=k+2.

Example separating variants: H_u(2)=1. On X={1,2}, set f(empty)=1 and both singleton values to 2. For exterior maps with f(empty)=1, the singleton {2} has both its permitted images equal to 1, and the symmetric case is identical. Thus H_e(2)=2.

## Approach 1: counting and forced collisions

**Counting.** If an h-set covers n colors, n<=2^h. Hence H_u(n)>=ceil(log_2 n).

**Collision proposition.** For k>=2, H_u(2^k)>=k+1. Among the n+1 inputs empty,{x}:x in X, two have the same image. Their union has size at most 2 and extends to a k-set Y. Consequently the n=2^k inputs in P(Y) have at most n-1 distinct images. This is an elementary baseline, not a new asymptotic advance. The proof does not impose exteriority. The exception k=1 is real, by H_u(2)=1.

A graph formulation makes the exact boundary transparent. Take the inputs A with |A|<=h as vertices, joining distinct A,B whenever |A union B|<=h. If n=2^h and every h-set is covered, f must be a proper n-coloring of this graph: a repeated color on an edge gives a non-injective h-ideal. For h>=2, empty and the n singletons form a clique of size n+1, contradiction. This argument uses no probabilistic or historical result.

**Limitation.** For h=k+d with d>=1, covering allows collision excess 2^h-n=(2^d-1)n inside each ideal. One forced collision gives no contradiction. A lower-bound proof at fixed d must control an extensive loss, or use a substantially different obstruction, uniformly over every f.

**Reduction to powers of two.** H_u is nondecreasing: if m>=n and a map on an m-set covers every h-set, restrict its input to a fixed n-subset and compose its values with any surjection from the m-set to that n-set. This covers every h-set in the n-set. If h>n, monotonicity follows instead from H_u(n)<=n<h. Therefore proving H_u(2^k)-k -> infinity would suffice for the full target: for 2^k<=n<2^{k+1}, H_u(n)-log_2 n >=H_u(2^k)-(k+1). This is a reduction, not a proof of either limit.

## Approach 2: disjoint covering families and the fractional barrier

For each output x let F_x={A:f(A)=x}. The F_x partition P(X). The desired property is that each F_x is a cover of the h-layer from below: every h-set contains some member of F_x. Only ranks <=h matter. Replacing each F_x by its inclusion-minimal members preserves this property; each resulting family is an antichain, and families of different colors remain disjoint. Conversely disjoint families covering every h-set can be extended to a full coloring by assigning all unused inputs arbitrarily. Thus this is exactly a packing problem for n disjoint downward witnesses, not merely n independently existing covers.

For uniform random h-set Y, define N_x(Y)=|F_x intersect P(Y)| and
w(A)=C(n-|A|,h-|A|)/C(n,h) for |A|<=h.
Then E N_x=sum_{A in F_x}w(A). Coverage implies this sum>=1 for every x. Summing over colors gives n<=sum_{|A|<=h}w(A)=2^h, exactly the elementary bound.

This failure of the first-moment relaxation is exact. Relax integral color assignments to nonnegative z_{A,x} with sum_x z_{A,x}=1 and impose sum_{A⊆Y}z_{A,x}>=1. The uniform fractional assignment z_{A,x}=1/n satisfies all constraints whenever 2^h>=n. Thus this LP relaxation cannot distinguish the conjectured threshold from counting, even though integral feasibility can fail at equality.

The exact lost-mass identity is
2^h-|f(P(Y))| = sum_x (N_x(Y)-1)_+.
Its expectation measures repeated images. Merely bounding sum_x E N_x does not bound the loss, since overlapping witnesses in one color are the central difficulty. An argument from independent per-color covering numbers must also handle simultaneous disjointness and overlap, or it is incomplete.

## Approach 3: probabilistic upper constructions

See RANDOM_BOUNDS.md for a self-contained finite union bound and explicit constants. Its direction is an upper bound, so it cannot resolve the requested lower divergence. It also provides a check on historical coefficient confusion: log_2 n is the leading term; the coefficients 3 and 2 concern log_2 log n, not a multiple of log n.

## Approach 4: small exact instances and certificate checking

With h=0 allowed, the independently checked values for n=1,...,11 are respectively 0,1,2,3,3,3,4,4,4,4,4. See certificates in this directory for explicit witnesses, a separate verifier, and exact lower arguments. The case n=7,h=3 is excluded by a complete finite constraint search with a separate independently implemented checker; no solver infeasibility claim alone is used. These establish only the finite values stated there. Exhaustive or solver output is not extrapolated to the asymptotic conjecture, and no unverified optimization infeasibility is used as a mathematical lower bound.

## Approach 5: auditing deficit amplification

The indexed tracker attributes to Alon a constant c>0 such that every coloring of a 2^k-point set has a k-set missing at least c*2^k colors (for sufficiently large k). No primary written proof of that personal communication was recovered; it is not established anew here. Even accepting this statement, it concerns k-sets, not (k+d)-sets.

Fix a k-set Y and an extra point z. The two disjoint input slices of P(Y union {z}) are P(Y) and {A union {z}:A⊆Y}. Their images are values of two generally unrelated functions. Missing colors in the first slice may all occur in the second. For an explicit local counterexample to propagation, choose any nonempty proper color subset S⊊X. Assign the 2^k=n inputs in the first slice onto S and the n inputs in the second slice onto X\S; extend f arbitrarily elsewhere. The first slice misses n-|S| colors, yet the (k+1)-ideal covers X. This is a counterexample to local deficit persistence, not a counterexample to the conjecture or to the globally quantified tracker assertion.

More generally, for a d-set Z disjoint from Y, split P(Y union Z) into 2^d slices indexed by T⊆Z, with g_T(A)=f(A union T). Even if a theorem independently supplies a deficient k-set for every g_T, those witness sets can differ. Even if they agreed, their missing-color sets need not intersect. Both a common witness and a common missing color need proof. Applying a k-set theorem successively without such compatibility is invalid.

Nor does a constant fractional deficit alone permit a direct color-compression argument. A surjective relabeling can merge a missing color with a present color, making the compressed color present. Conversely restricting to fewer output colors without preserving all input constraints is not an admissible reduction.

A precise conditional consequence is valid: a deficit of c*2^k eventually exceeds k^C for each fixed real C. Indeed k log 2-C log k+log c -> infinity. This proves only the polynomial-deficit conclusion at size k, conditional on that reported theorem; it does not prove any fixed-d extension obstruction.

## Proven outcomes and acceptance boundary

Proved here: variant separation at n=2; elementary collision lower bound for all powers 2^k with k>=2; monotonicity and a powers-of-two reduction; exact covering-family reformulation and a sharp fractional barrier; elementary probabilistic finite upper criteria; independently checked small cases; precise identification of failed amplification steps.

Not proved: H_u(2^k)>=k+2 eventually; H_u(n)-log_2 n -> infinity; asymptotic equivalence of H_u and H_e; Alon's reported personal-communication result. No complete asymptotic claim is supported. Independent review of this report, the random-bound derivation, and executable finite certificates is recorded in the separate audit packet `INDEPENDENT_AUDIT.md`. Its acceptance is limited to these partial results, not the unsolved asymptotic target.

Public primary references: Erdős–Hajnal (1968), https://users.renyi.hu/~p_erdos/1968-01.pdf ; Erdős–Spencer (1971 article, archive identifier 1972-04), https://users.renyi.hu/~p_erdos/1972-04.pdf . The 1968 source states exteriority, the +3 theorem and +2+epsilon refinement remark. The later independent-set article does not solve this covering-threshold problem. Source retrieval and status limitations are recorded separately in the source gate; no new live status assertion is made here.
