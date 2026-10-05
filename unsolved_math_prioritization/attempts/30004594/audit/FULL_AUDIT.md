# Independent full audit of retained contact-process partial results

Problem 30004594 / OWR-4990373-008, rank 780. Audit date: October 5, 2026 UTC.

## Verdict

**PASS_RETAINED_PARTIALS_FULL_AUDIT. The original problem remains UNSOLVED after 5/5 substantive approaches.** No mandatory mathematical correction was found. This is a separate mathematical and computational audit of the entire retained partial package, not a proof of the original target, formal proof-assistant certification, human peer review, novelty determination, or external acceptance.

The author freeze was preserved byte-for-byte. All nine manifest-listed files match, and the tenth file is the separately anchored manifest. The archive has exactly the ten allowlisted regular files. Its SHA-256 is a945c97336f27b6cb4fc750e5eb7aa4819e3e459778422dd0a427cc78ac318b5 and size is 24,142 bytes; the manifest SHA-256 is b7cec3611fed2152a42b7e7b4c2daa7ca18d899b3f03603898df838ab9819fd6.

Author replay reproduces all 72,940 exact assertions and the recorded JSON byte-for-byte. Independent code passes 875,433 additional exact assertions. This total explicitly includes 343,400 divisibility checks inside the independent fraction-free solver; assertion counts are accounting information, not measures of mathematical certainty.

## 1. Exact target and normalization

The problem concerns every integer d >= 2, the nearest-neighbor contact process on Z^d, recovery rate one, survival from one infected site, and nearest-neighbor spatial connectivity of the occupied sites at one time under the upper invariant measure. It does not concern survival in space-time, a stationary law selected arbitrarily, diagonal infection edges, a random tree, or a dynamic environment.

Use lambda for the total infection-attempt rate and b=lambda/(2d) for each directed nearest-neighbor arrow rate. If a paper instead uses its symbol lambda for the per-neighbor rate, its parameter is b here. Its two thresholds must both be multiplied by 2d to compare with the author packet. In particular:

- The singleton exit probability is lambda/(1+lambda)=2db/(1+2db).
- The adjacent conditional identity is 1-1/lambda=1-1/(2db), where positive stationary density is required.
- The branching-process extinction bound is lambda<=1, equivalently b<=1/(2d).
- The audited no-go range is lambda>=1, equivalently b>=1/(2d).

Thus the wording “all lambda>=1” is correct only in the expressly adopted total-rate convention. It covers every supercritical rate because lambda_c>=1. Rath-Valesin equation (1) uses this total-rate convention; the inspected Fernley-Jacob and van den Berg papers use a per-neighbor infection parameter. No numerical per-neighbor threshold has been inserted into a total-rate calculation.

Duality identifies the one-site density with single-site survival probability. The upper invariant law is delta_0 below and at the survival threshold, using critical extinction as a credited classical input. A countable union over lattice roots equates zero probability of any infinite occupied component with zero probability that a prescribed root belongs to one. Attractiveness gives monotonicity in the infection rate. These facts justify lambda_c<=lambda_p and the equivalence between strict separation and finding one nonpercolating rate strictly above lambda_c. The author's definitions make no assertion about spatial percolation exactly at lambda_p. Large-rate lower domination, credited to the established literature, gives finiteness of lambda_p for d>=2; it is not independently reproved here.

## 2. Proposition 1 and the one-dimensional boundary

For each destination x, the recovery clock and all directed incoming-arrow clocks have respective rates 1 and lambda. Their latest mark strictly before time zero exists almost surely. Its type is an arrow with probability lambda/(1+lambda). Destination-indexed collections are disjoint independent Poisson families, even when two destinations are adjacent: opposite directed arrows are different primitives. Consequently these latest-mark types are independent across all vertices.

If the latest mark at x is a recovery, x cannot be occupied at zero. This implication is necessary, not sufficient: an incoming arrow from an uninfected neighbor does not infect x. Therefore the domination direction is correctly an upper bound by product Bernoulli. The finite-time construction also works: on a fixed finite set the chance of a vertex with no mark since -T tends to zero. Finite-coordinate couplings pass to the upper stationary limit, avoiding any unjustified uniform statement over infinitely many sites at finite T.

For every lambda with lambda/(1+lambda)<p_c, the product field has no infinite cluster. Taking the supremum of these rates yields lambda_p>=p_c/(1-p_c). Nothing is assumed at p_c, and no strict comparison with lambda_c follows. On Z, independent vacant sites occur arbitrarily far in each direction whenever the Bernoulli parameter is below one. An infinite connected subset of Z must contain a half-line. This validates lambda_p(Z)=infinity at finite rates, without resolving any d>=2 case.

The graphical comparison is explicitly credited to the existing spread-out literature and its attribution to Bethuelsen. The author offers a self-contained exposition, not a novelty claim.

## 3. Stationary occupied-set hierarchy and the path criterion

For finite A, a recovery at x in A changes f_A by -f_A when x is occupied; writing this as -f_A already includes the occupation indicator. Summing gives -|A|f_A. An arrow y->x with x in A changes the product by

(1-eta(x)) eta(y) product over z in A minus {x} of eta(z).

Using idempotence eta(z)^2=eta(z), this equals the difference of the two monomials indexed by (A minus {x}) union {y} and A union {y}. This remains correct when y already lies in A. Arrows whose destination is outside A contribute zero. Integrating the bounded finite-range cylinder generator against an invariant law gives the printed hierarchy, with no exchange of an infinite sum.

For A={0}, invariance and lattice symmetry make the 2d neighboring pair moments equal. Hence rho=lambda(rho-m({0,e})). Division by rho is permitted only when rho>0, exactly as stated. This supplies a two-site conditional probability, not a sequential conditional probability given the whole preceding path. Stationarity is not a spatial Markov property. Positive association supplies an inequality in the wrong direction for the required upper path bound.

Independently, there are at most 2d(2d-1)^(n-1) self-avoiding n-edge paths from one root. Multiplying this count by Cq^n tends to zero if (2d-1)q<1. An infinite connected component in a locally finite graph supplies paths of every finite length, so the root cannot have an infinite component. The countable union over roots proves the stated conclusion. The author never claims that the pair moment verifies this path hypothesis.

The independent generator test checks all 512 configurations and all 511 nonempty subsets of a 3-by-3 torus, separating the formal coefficients of recovery rate and per-neighbor infection rate. Thus it does not merely repeat one rational substitution. These 523,264 coefficient assertions verify finite algebra; the analytic argument, not the torus calculation, establishes the hierarchy on Z^d.

## 4. The vanishing-density counterexample

For independent Bernoulli(epsilon) variables H_(j,k), define occupation at x when at least one H_(j,x_j) equals one. The density is 1-(1-epsilon)^d. A selected coordinate hyperplane is infinite and connected under nearest-neighbor edges when d>=2. There is almost surely at least one selected hyperplane, indeed infinitely many in each direction. Therefore every positive-epsilon field percolates almost surely.

Translations permute the identically distributed hyperplane variables, as do coordinate permutations and sign changes. Every increasing cylinder event is an increasing function of finitely many independent Bernoulli variables, so positive association holds, and approximation extends it to the field. The diagonal translation shifts each of the d underlying Bernoulli sequences by one. Two fixed cylinder events use disjoint variables after sufficiently many diagonal shifts, proving mixing for that transformation. Its ergodicity implies ergodicity of the full translation action because any event invariant under all translations is invariant under the diagonal one.

For finite F, the union bound gives P(some occupied site in F)<=|F|[1-(1-epsilon)^d], which tends to zero. This is local weak convergence to delta_0, with no continuity of the infinite-cluster event implied. Mixing in every spatial direction is neither true nor asserted.

For three collinear sites in dimension two, the n-site moment, n=1,2,3, is epsilon+(1-epsilon)epsilon^n: either their common horizontal hyperplane is selected or all n independent vertical ones are selected. At epsilon=1/4 this gives 7/16, 19/64, 67/256. The triple-times-density minus pair-squared difference is epsilon^2(1-epsilon)^3, giving 27/1024 at 1/4. Its strict positivity rigorously falsifies the proposed pair-factorization inference. The independent enumeration also checks three other rational epsilon values.

The construction is outside the contact-process invariant family. It neither solves the problem negatively nor shows that contact-specific information cannot yield strict separation. The counterexample only removes an insufficient collection of general assumptions.

## 5. Full audit of the finite-radius argument

### 5.1 Graphical measurability and independent classes

I_x(L) is the open infinity-ball of integer radius L, containing (2L-1)^d sites. The backwards exploration follows arrows against their original orientation, revealing recovery clocks of its interior sites and arrows whose original destination is in that interior. When such an arrow has its source outside the interior, exit is declared immediately. No recovery at that external source, and no further history there, is queried. These exact stopping and primitive-allocation choices matter.

For centers congruent coordinatewise modulo m=2L-1, different interiors are disjoint. Their recovery clocks and destination-indexed arrow families are consequently disjoint. This proves joint independence within each class, not only pairwise independence. Pooling all arrows touching an interior would fail this argument; a cross-boundary arrow would then belong to two families. The independent code includes that negative-control distinction.

A process constrained forever to a fixed finite interior dies almost surely. In each unit interval, require no arrows into that finite interior and at least one recovery at every interior site. The event has positive probability depending only on the finite interior and rate. Independent successive intervals force its eventual occurrence. On that event the interior is empty at the interval's end. Therefore infinite backwards survival cannot remain confined, giving eta(x)<=Y_x(L). Countably many exceptional zero-probability events can be removed simultaneously.

The finite dual process has subset states, an empty failure state, and an absorbing success state. Recoveries remove vertices; backwards internal arrows add ancestors; outside-source arrows into an active site cause success. On this symmetric lattice its internal birth rates agree with the ordinary contact-process rates. Every nonempty state can reach zero through finitely many recovery jumps with positive probability and without a birth, so there is no transient-state closed communicating class. The hitting-probability matrix is invertible. Its entries are affine in lambda; its inverse gives continuity for positive lambda and rational values at positive rational lambda. For L=1 the only active interior site faces total exit-arrow rate lambda and recovery rate one, giving the exact probability lambda/(1+lambda).

### 5.2 Union bound

Every fixed path of n+1 distinct vertices has a deterministically chosen color class containing at least ceil((n+1)/M) vertices, where M=(2L-1)^d. If the path is occupied, the independent exit indicators at those vertices must all equal one. Its probability is at most h_L^ceil((n+1)/M). The chosen class depends only on the fixed path, not on the random field, so there is no selection bias and no extra factor M is needed. Summing over paths yields decay if (2d-1)h_L^(1/M)<1, equivalent to the printed strict criterion.

### 5.3 Obstruction at every potentially supercritical rate

For L>=2 fix a straight directed backwards route from the center to an exterior site, taking exactly L lattice steps. At each newly reached site require the next arrow along this route to occur before the next recovery there. At the arrival stopping time, fresh Poisson increments give conditional success probability a/(1+a), where a=lambda/(2d). The route visits new sites; discarded marks and infections elsewhere cannot destroy this particular valid graphical path. The construction imposes no recovery-free condition on a site after the route has left it. Therefore

h_L(lambda) >= [lambda/(2d+lambda)]^L >= (2d+1)^(-L) for lambda>=1.

For L>=2, (2L-1)^d >= (2L-1)^2 >=3L. The latter inequality follows from 4L^2-7L+1>=0 for integers L>=2. Also (2d-1)^3>2d+1 for every integer d>=2. Combining the positive-base comparisons yields

(2d-1)^((2L-1)^d) > (2d+1)^L.

Thus the lower bound on h_L already strictly exceeds the required cutoff. At L=1, the exact h_1>=1/2>1/(2d-1) is used separately. The weaker one-prescribed-arrow lower bound at L=1 would not suffice in dimension two; the proof correctly avoids that mistake.

Finally, the contact population is dominated by a linear birth-death branching process of birth rate lambda and death rate one. That process dies almost surely for lambda<=1; at equality its embedded jump chain is a symmetric walk absorbed at zero. Nonexplosion follows from its linear rates. Therefore lambda_c>=1, and all rates greater than lambda_c are covered. At criticality, finite lifetime and nonexplosion do imply h_L tends to zero, but the exponentially deteriorating color cutoff makes this insufficient, as the stronger universal comparison shows.

**The result is only a no-go theorem for this specified singleton dual-exit/color-class/path-union-bound certificate.** It is not a lower bound proving actual spatial percolation, a disproof of threshold separation, or a no-go theorem for block crossings, adapted explorations, multiscale methods, or renormalization in general.

### 5.4 Independent exact finite chain

For d=2, L=2, and total lambda=1, the interior has nine vertices and 511 nonempty states. The independent code constructs all raw transition rows without importing the author's code, generates dihedral orbits by a rotation and reflection, and finds 101 nonempty orbits. It verifies lumpability for every state. Multiplying all rates by four gives integer recovery rates 4 and arrow rates 1, preserving hitting probabilities. A separate integer Bareiss elimination solves the reduced system exactly.

After lifting the solution, every one of the 511 original, unreduced state equations is checked against the raw transition dictionary, as are strict probability bounds and all 4,608 one-site-addition monotonicity inequalities. Every state has an explicit recovery step to a smaller state, validating uniqueness in the finite chain. The origin exit probability agrees exactly with the author fraction and is approximately 0.2249369358. It is greater than 1/25, which is greater than the color cutoff 1/19683. The full 512-entry rational vector, including zero, is included in the authored finite-control results. This calculation is at a single rate and finite radius and does not decide any infinite-volume threshold.

## 6. Geometry and imported mechanisms

An injective image of all depth-n vertices of a rooted b-ary tree would contain b^n distinct points in the infinity-ball of radius Kn if every edge mapped to a lattice path of length at most K. Its capacity is (2Kn+1)^d. Exponential growth beats this polynomial, so the bounded-length injective embedding is impossible. No claim is made against embeddings with unbounded edge lengths or noninjective comparisons.

Deleting a finite straight segment from Z^d does not disconnect the surrounding lattice for d>=2. Points above different segment vertices are already joined outside the segment by the parallel line at second coordinate one. More generally one can move around an endpoint to change sides. Thus components that are separated by cut vertices in a tree are not disjoint lattice side domains. The tree proof's exact graphical independence cannot simply be imported. This does not assert that all tree-inspired inequalities fail.

Adding infection arrows can monotonically shift both survival and spatial-percolation thresholds. Monotonicity by itself does not carry a strict gap between the two thresholds from one infection kernel to another. In particular, the spread-out infinity-ball graph differs from the spatial nearest-neighbor graph; even its range-one kernel includes diagonals in dimension at least two, and the inspected normalization includes ineffective self-arrows. The nearest-neighbor target is preserved throughout the audited packet.

## 7. Source, dataset and prior-attempt audit

The precise source question and dimension are visible on [OWR 4/2021, printed p. 175](https://ems.press/content/serial-article-files/46882). The independent audit read the two-page contribution and visually inspected p. 175. The earlier formulation is [Liggett-Steif, Section 8, Question 2, printed p. 242](https://www.numdam.org/item/10.1016/j.anihpb.2005.04.002.pdf), also visually inspected. This is a request for a nonpercolating supercritical parameter for each d>=2.

The [Rath-Valesin manuscript](https://arxiv.org/abs/1912.09825) was checked for the nearest-neighbor rate convention, its distinct spread-out kernel and spatial graph, the large-range theorem, and the credited product upper comparison. The [Fernley-Jacob September 2026 preprint](https://arxiv.org/abs/2609.09972) was checked at its abstract, definitions, tree theorem and Section 6 factorization mechanism; it explicitly retains the lattice gap as open. The [published two-dimensional sharpness result](https://arxiv.org/abs/0907.2843) gives exponential subcritical cluster tails but does not establish a nonempty supercritical nonpercolating interval. [Beekenkamp arXiv:1807.05591](https://arxiv.org/abs/1807.05591) remains withdrawn and is excluded from theorem inputs. Deep proofs and all dependencies of these papers were not independently re-proved.

All six stored scholarly PDFs match the author's hash metadata. Fresh downloads match the exact bytes of the five core PDFs. The supplementary [2026 Poisson-representability/mixing paper](https://research.chalmers.se/publication/549341/file/549341_Fulltext.pdf) is served with a retrieval timestamp and produced different PDF hashes on two new downloads. The retained second fresh download's entire extracted text matches the frozen text after removing only its changed download-timestamp line. Its screened theorem statements do not provide threshold separation, and it is not an input to the authored partial proofs. The audit records the differing bytes and hashes; it does not silently equate live and frozen PDFs. Full literature coverage is not claimed.

Both complete pinned dataset files were reread and rehashed against the freshly retrieved manifest at repository commit 24ae23df9ad6c9def619cdbdf2ec8066f506788f. Their exact lengths, hashes, revision and match results appear in provenance_results.json. There are 15,458 problem records and 6,701 prior-report dictionary entries. Numeric ID 30004594 and its source code match uniquely. The selected prior-report key is absent, not a present null. The statement digest matches the descriptor.

The descriptor review hash, previously recorded without recalculation, has now been independently recomputed. The repository importer substitutes an empty object for an absent report. With the complete selected problem and that empty object, SHA-256 of Python's json.dumps([problem, {}], sort_keys=True) equals dbcdeb82111990e3cd26ef9a6fc2ccab7a1986e832bcc3eb042149c5608b3d1e. Using null would yield a different digest and would not reproduce repository semantics. The retrieved queue implementation, the complete local catalog, and the dataset manifest are also bound to their Git blob IDs in the pinned repository tree.

The full 14,920-entry prioritization tree is untruncated. Its nested Git tree hashes were independently rebuilt, and its linkage to the pinned commit's root tree was checked. No path matching the target ID, code prefix, or contact topic appears. New public API searches for the numeric ID in PRs and commits return zero matches with incomplete_results=false. The author's earlier branch and broader-topic searches were inspected as historical evidence rather than mislabeled as fresh repetitions. These observations do not exclude deleted branches, unpublished or private work, unindexed contents, or every differently named attempt. The packet's lack-of-prior-attempt conclusion is correctly limited to the searched record and scopes.

## 8. Disposition and remaining gap

All retained authored propositions and theorems pass this audit within their printed scopes. The verified evidence does not locate a nearest-neighbor rate lambda>lambda_c with no infinite occupied spatial component, nor a counterexample showing equality of the thresholds. Five substantive approach families have been spent; the audit corrected no theorem and did not add a sixth proof-search approach.

The correct publication or queue disposition is **unsolved, 5/5, reviewed partial results**. Historical author files saying independent review is pending must remain frozen; this audit supplies the later disposition. No claim of full solution, general renormalization impossibility, novelty, human peer review, or source-paper acceptance is warranted. No remote write was performed by this audit.
