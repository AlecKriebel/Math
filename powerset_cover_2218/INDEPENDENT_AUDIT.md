# Independent mathematical audit: Erdős 624

Date: 2026-10-21 UTC. Scope: unrestricted powerset-cover threshold, comparison with the exterior model, elementary estimates, finite witnesses, and limits of amplification. This is not a solution or novelty claim. 

## Definitions and boundaries

For n>=1 fix an n-point X. Let H_u(n) be the least integer h in {0,...,n} for which a single f:P(X)->X has f(P(Y))=X for every Y subset X of size at least h. Empty input and full input are included. Checking exactly h-element Y suffices: any larger Y contains such a Y0, and P(Y0) is contained in P(Y). The same f must work for all Y. Changing f with Y invalidates a construction.

H_u(1)=0 under this nonnegative-threshold convention. Requiring positive h instead changes this boundary only. The n=0 problem has no map from its nonempty powerset to its empty codomain and is excluded.

For the exterior variant, the domain must exclude X, since f(A) in X\A is otherwise impossible. One consistent convention quantifies all Y and evaluates f on P(Y) intersect P_proper(X). Equivalently one may quantify only proper Y and permit threshold n; this can make the last condition vacuous but gives the same minimum for n>=2 because the forced values f(X\{x})=x cover X at Y=X. Empty input remains allowed. Any exterior map extends arbitrarily at X to an unrestricted map, so H_u<=H_e. The reverse inequality is not available. At n=2 the unrestricted choice f(empty)=0, f({0})=f({1})=1 has threshold 1; every exterior choice fails on one singleton, and H_e(2)=2.

## Independently verified elementary lower bounds

The number of inputs in P(Y) is 2^h, so H_u(n)>=ceil(log2 n). If n=2^k and k>=2, the n+1 inputs consisting of empty and the n singletons have two equal outputs. Their union has size at most two and extends to a k-set Y. Its n inputs have a collision, so cannot cover n colors. Therefore H_u(2^k)>=k+1. This argument does not prove >=k+2. At k=1 it fails precisely because the union need not fit inside a singleton, and the n=2 example disproves the claimed extension. The pair-collision argument in the recovered original source also does not use exteriority, but its simple union-size bound only directly handles k>=4.

## Independently verified random upper bounds

Assign all inputs independently and uniformly among n colors. For a fixed h-set Y and color x the missing probability is exactly (1-1/n)^(2^h). The union bound is over n*binom(n,h) pairs, not over only n colors or only binom(n,h) sets. Thus

n*binom(n,h)*(1-1/n)^(2^h)<1

is a sufficient, not necessary, condition for H_u(n)<=h, provided h<=n. A convenient stronger condition is 2^h/n>ln n+ln binom(n,h). The logarithms in this display are natural.

Writing L=log2 n and h=ceil(L+2log2 L) gives 2^h/n>=L^2 and ln n+ln binom(n,h)<=(h+1)ln n<=(L+2log2 L+2)L ln2. For L>=32 the latter is less than L^2: the ratio ln2*(1+(2log2 L+2)/L) is less than 1 at 32 and decreases thereafter. Also h<=n. Hence the explicit large-n bound H_u(n)<=ceil(log2 n+2log2 log2 n) is established for n>=2^32. This is not an optimized starting point.

An independent exterior construction chooses f(A) uniformly from X\A for every proper A. For fixed proper h-set Y and x, at least 2^(h-1) subsets A of Y omit x; each such trial has probability at least 1/n of outputting x. Therefore the failure probability is at most exp(-2^(h-1)/n). The same union-bound argument gives H_e(n)<=ceil(L+2log2 L)+1 for n>=2^32. The additional constant is harmless and the second-order coefficient is 2 on loglog, not on log n. No independence between different missing events is required; only the distinct input assignments are independent.

These upper bounds and the elementary lower bound leave the requested divergent lower excess unresolved. Changing loglog bases adds only a constant, but changing the coefficient of log n changes the assertion substantially.

## Amplification audit

The sequence H_u is nondecreasing. For m<=n restrict a covering map on an n-point set to a chosen m-point subset of its domain and compose its outputs with a surjection from n colors to m colors. If H_u(n)<=m this proves H_u(m)<=H_u(n); otherwise H_u(m)<=m<H_u(n) is trivial. Consequently a proved divergent dyadic excess would imply the full limit: for 2^k<=n<2^(k+1), H_u(n)-log2 n>=H_u(2^k)-k-1. A fixed +1 dyadic lower bound does not yield divergence through this argument.

A k-set missing c*2^k images does not by itself force any (k+1)-set to miss a color: adding one point introduces another 2^k inputs, enough to supply the missing colors. A restriction changes the codomain unless it is projected; projecting colors can eliminate missing colors. Thus repeated restriction, extension, projection, or tensoring needs a new proved invariant, not merely the same fixed-fraction deficit. No such invariant or complete amplification proof was supplied in the audited material. Personal-communication claims in the source gate are not independently verified theorems in this audit.

## Source scope

Reviewed the source gate and original 1968 article. The original excerpt distinguishes exterior maps, states the 3+epsilon upper coefficient and a modification to 2+epsilon on loglog, and formulates divergent excess. OCR is imperfect; the source-recovery report remains responsible for page-image verification and source status. No assertion here upgrades indexed open status to freshly verified live status. No source text is reproduced for publication.

## Finite certificates and final disposition

Finite witness verification and hashes are recorded in COMMAND_LOG.json. A successful exact integer coverage check certifies existence even when a witness was found by floating-point MILP. Solver infeasibility or timeout, without a separately checked proof, is not an exact nonexistence certificate. No finite table establishes the asymptotic limit.

Disposition: elementary bounds accepted with the stated parameter ranges and conventions; full conjecture unresolved by this audit. Additional research artifacts will be reviewed in a separately identified addendum if they arrive after this report.

## Review addendum: five-route report and small cases

The research report's graph-coloring reformulation at n=2^h is correct, with the h>=2 clique obstruction explicitly scoped. Its minimal-member antichain reduction preserves cover witnesses and cross-color disjointness. Its weighted counting identity and uniform fractional assignment show precisely that the stated first-moment/LP relaxation has no advantage over 2^h>=n. The lost-mass identity is exact. The explicit two-slice example is a valid counterexample to local deficit persistence, not to the globally quantified conjecture. These routes are accepted as scoped partial analysis.

Independent finite checks verify the supplied n=5,6 witnesses at h=3 and n=7,8,9 witnesses at h=4, after assigning color zero to all omitted higher-rank inputs. Every Y of size at least h, not only the h-layer, is checked with exact integer sets. These imply H_u(5)=H_u(6)=3, H_u(7)=H_u(8)=H_u(9)=4 when combined with counting, the dyadic collision argument, and the n=7 lower certificate described next.

For n=7,h=3, normalize the empty-set color to zero and remove that color from every nonempty input by recoloring it arbitrarily among the six others; empty already supplies zero in every ideal, so coverage is preserved. Every triple must therefore see at least five nonzero colors on its three singleton and three pair inputs; its top input can add at most one color. A singleton color cannot occur three times, since such a triple would have at most four colors on these six proper nonempty inputs. Since seven singleton inputs use at most six colors, the only possible multiplicity patterns are 2+1+1+1+1+1, 2+2+1+1+1, and 2+2+2+1, up to vertex and color permutations. The independent checker directly checks all three patterns, including the six-singleton-color case, and imposes no edge symmetry fixing.

For each triangle the checker enumerates exactly those ordered triples of edge colors whose union with the fixed singleton colors has size at least five. It repeatedly deletes unsupported values from each edge domain, rejecting if any triangle table becomes empty. Such deletion cannot remove a satisfying assignment. It branches on every remaining color of an unresolved edge. Thus termination with no branch accepted is an exhaustive finite proof. The three patterns terminate unsatisfiable in respectively 1, 22, and 49 search calls. Combined with the independently checked h=4 witness this certifies H_u(7)=4. This independent implementation agrees with the research worker's separately implemented certificate; solver infeasibility is not relied on.

A later extension independently verifies local-search witnesses for n=10 and n=11 at h=4, on all 848 and 1816 supersets respectively. Counting supplies the matching lower bound, so H_u(10)=H_u(11)=4. No value at n=12 is asserted. The independent checker lists stable witness filenames explicitly; empty or unfinished search output is not evidence.

## Review addendum: finalized random-bound note

RANDOM_BOUNDS.md passes independent mathematical review. The exterior products Q_m are exact because eligible subsets of each size are counted by binom(m,k), with m=h-1 for an internal target color and m=h for an external color. The split and uniform event estimates follow, including the forced-coverage endpoint h=n. Its sharper finite range n>=32 and slightly larger constants h_u=ceil(L+2log2 L+1), h_e=ceil(L+2log2 L+2) are valid: the proof bounds the union logarithm by (L+2log2 L+4)L ln2<2L^2 while both exponents are at least 2L^2. Candidate thresholds are below n. The explicit epsilon ranges, log-base conversion, and coarse middle-layer coefficient-3 explanation are valid. These accepted bounds are consistent with, and complementary to, the smaller-constant/larger-starting-point version independently derived earlier in this audit.

The finalized SMALL_CASES.md and verify_witnesses.py also pass review. The author's two-pattern/46-call report and this audit's three-pattern/72-call report are consistent: the author removes the six-singleton-color pattern analytically and fixes one edge by swapping the two unused colors in the four-singleton-color case. This audit searches the first pattern directly and uses no such edge fixing. The elementary rank-coloring constructions certify the n=1,...,4 entries. Together the accepted exact unrestricted table for n=1,...,11 is 0,1,2,3,3,3,4,4,4,4,4, under the h>=0 convention. Search timeouts and n=12 diagnostics remain inconclusive and are excluded from mathematical acceptance.

Final acceptance is limited to the reviewed files and SHA-256 hashes in the original audit hash manifest (its hash is recorded in PROVENANCE.json). Search programs are provenance, not premises for the positive witnesses; this audit's exact checker and the explicit finite reduction suffice for the accepted claims. No novelty or full asymptotic solution is certified.
