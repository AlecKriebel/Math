# Independent adversarial audit A: sharp near-one oriented-flow asymptotic

Date: 2026-10-07. Problem 9700042 / AMR-096-0042.

## Verdict

**ACCEPTED: full canonical asymptotic, for the frozen revised C4 proof identified below.** The proof establishes

\[
\lim_{q\downarrow0}\frac{1-v(1-q)}{\sqrt{2q}}=1
\]

in the exact directed square-lattice Bernoulli-capacity model on Aldous's problem page. This is a mathematical review of an authored proof, not formal verification, human peer review, a novelty finding, or a certification of current literature status.

The external premises are the source-stated deterministic L1 flow-density limit, the classical longest-increasing-chain limit and upper-tail theorem, and the finite Bernoulli BK inequality. Their normalizations and applicability were checked. The C1 finite duality and counting argument were independently reread; the existing C1 audit was treated as supporting provenance, not a substitute for checking their use in C4.

The original C4 contained minor enclosure/indexing presentation defects. They do not reveal a failed estimate, and the separately frozen revision corrects them. Acceptance attaches to the revised bytes, not to any future edit or an unspecified version of the argument.

## Frozen input identification

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| TURN_C4_BK_POISSON_REVISED.md | 20646 | 8da7cf366948e8d4fc63e3399cc4fe804ed786ea99b01479619efbdbacfedf3a |
| TURN_C4_BK_POISSON_CANDIDATE.md | 19887 | 3ca69bacb1a4458243626ea0adfb360fc991bb2f8e2ed4293fa98b9c85534691 |
| C4_CLARIFICATION.patch | See manifest | 2429a7e365743dddff4785839b667f5b1f83a5e0be2f915d6840813a29dccfb3 |
| TURN_C1_MARKED_DEFECT_BOUND.md | 9957 | f38d6ac74d3abad6f7675a13429f09e0bc6fc8151c137284e4655e8fc0c39120 |
| verify_resume_turn4.py | See manifest | 48c6d164d839440e20a2a1f2bc6c70fd59cf7c084180e03fb2eea648aa7b5720 |
| TURN_C4_CHECKS.json | See manifest | c6665c65efbab00cbda08a0b4151be5d076bdf89d6a453dc6a3997174c88c57f |

Copies were taken and hashed before final review. The full diff from original to revision was inspected: it adds an explicit mean-uniform-integrability observation, corrects the nonlast segment index, replaces one strict inequality with its valid weak version, and proves positivity of both rectangle sides using actual endpoint displacements. No numerical estimate or parameter selection changed.

## 1. Model, duality, and constants

Aldous's [primary problem page](https://www.stat.berkeley.edu/~aldous/Research/OP/hammersley_flow.html) specifies independent north/east capacities, source vertices on the left/bottom boundary, and sink vertices on the top/right boundary. Its normalization is V(n,p)/(2n) tending in L1 to v(p). The target is the square-root asymptotic stated above. The page's heuristic continuum scaling is not used as a theorem.

With N=n−2, the exact dual reduction is V_n=c_L+c_B+T_N. An arbitrary primal cut supplies a corner-to-corner directed dual route; alternating label transitions handle four-valent faces. Conversely, a simple dual crosscut separates the prescribed boundary arcs. Nonnegative costs permit loop erasure. Thus the reduction covers nonmonotone cuts. The deterministic boundary difference is bounded and disappears after division by 2n.

For a dual path, forward steps number 2N+b, so its cost is 2N+b−k and its reward is k−b. Every cycle has equally many forward and backward steps and reward at most zero. Consequently a reward maximizer can be simple. This remains true in every enlarged rectangle and every changed mark configuration used in a witness argument.

Therefore g(q)=lim E[D_N]/(2N) is the correct normalization. Two independent mark opportunities per bulk lattice vertex produce Poisson intensity two under coordinate scaling by sqrt(q). A square of rescaled side R has limiting increasing-chain law Lambda_{sqrt(2)R}; its leading mean 2sqrt(2)R gives g(q) of leading size sqrt(2q). There is no missing factor of two.

## 2. The stronger backtracking budget really follows from C1

The C1 enumeration counts every ordered list of k distinct marked forward edges on a simple path whose coordinate negative variations are at most k. The condition b≤k supplies exactly those variation bounds; no lower bound on k−b is needed. Thus C4 may apply that enumeration to K_N^+, rather than incorrectly inferring a bound on k or b from a bound on D_N.

For k≤N/4 and k≥32sqrt(q)N, the bracket in C4 (24) is bounded by 2e²(3/2)^6/32², approximately 0.164387. For k>N/4 and q≤10^−6, the other bracket is at most 32e²·10^−6·36, approximately 0.0085122. Both are below 1/4. Summing 4·4^−k gives the stated tail with the conservative constant 6.

The optimal reward is nonnegative because a monotone path is available. Its simple realization therefore belongs to the class defining K_N^+. The high-probability bound b≤k≤B_N is justified. Tail summation gives a uniform fixed-theta moment bound when theta<log 4. Monotone padding into a containing square proves the nonsharp rectangular moment estimate used on bad segments. These arguments do not require the rectangle's aspect ratio to be controlled.

## 3. Fixed-scale sparse convergence includes unrestricted paths

The deterministic stability argument is valid. If at most M marked edges occur and their starting positions are separated by more than M in each coordinate, a nonnegative-reward simple path uses at most M backward steps. Its successive marked starting positions cannot decrease in either coordinate: any such decrease would exceed the total available backward variation. Thus the visited marks form a strict increasing chain and reward is at most chain length.

Conversely, a strict increasing chain of such starts can be traversed monotonically including each selected oriented edge. The gap exceeding M≥1 accounts for the one-step edge displacement; forgetting orientation in the limiting process causes no problem. Boundary starts cause no difficulty because all edges under consideration lie in the rectangle.

For bounded rescaled rectangles, the probability of a marked pair within M lattice units in either coordinate tends to zero. The number of possible such pairs is O_M(q^−3/2), each pair has probability q²; same-start orientation pairs are also negligible. The total mark count is tight. These observations, together with the Bernoulli Laplace functional and the continuity of strict chain length away from coordinate ties, give the claimed Poisson convergence.

The exponential-moment upgrade is sound: 0≤D≤Z for a simple maximizer, while Z has uniformly bounded exponential moments at every fixed exponent. Using a larger exponent supplies uniform integrability of exp(theta D). Nothing here asserts convergence when the rescaled rectangle size grows with q; the scale is frozen first.

## 4. The Poisson moment estimate is stronger than a law of large numbers

The independently retrieved [Deuschel–Zeitouni manuscript](https://arxiv.org/pdf/math/9803035) gives the strict coordinate-chain model, the constant-two probability limit, and Theorem 2's positive-rate upper tail at speed sqrt(n). The theorem on PDF page 9 was also visually checked in the [author-hosted PDF](https://www.wisdom.weizmann.ac.il/~zeitouni/pdf/ccp.pdf). Only positivity of the rate for positive excess is needed; an explicit rate formula is unnecessary.

Poissonization is legitimate: construct an infinite iid sequence of uniform points independent of its Poisson count, and compare that count with ceil((1+delta)s²). The count-error probability is exponentially small in s²; the fixed-sample chain upper-tail error is exponentially small in s. A lower-count comparison likewise transfers the probability limit.

Here is an explicit justification of the moment conversion. Choose 0<a<epsilon, M>10e, and a small fixed theta with theta M<c_a/2 and theta<log 4. The contribution from Lambda_s≤(2+a)s is at most exp(theta(2+a)s). The middle contribution up to Ms is at most exp((theta M−c_a)s), allowing harmless endpoint constants. For k≥Ms, factorial counting gives

\[
e^{\theta k}\Pr(\Lambda_s\geq k)
\leq [e^\theta(e/M)^2]^k.
\]

The bracket is below one, and the geometric sum starts at an index proportional to s. It is exponentially small. The three contributions fit below exp(theta(2+epsilon)s) for sufficiently large s. Therefore C4 (30) follows; the proof does not deduce an exponential moment from the law of large numbers alone.

The factorial bound also gives uniform integrability of Lambda_s/s for s≥1, so its probability limit implies the mean limit needed in the lower bound. All external uses from this source are these specific classical chain facts.

## 5. Geometry, last segment, and perimeter accounting

First-hitting levels partition the entire path, including backward excursions, into J=ceil(2N/L) segments. The final increment lies in (0,L] and need not equal L. Every segment vertex is at least its starting coordinate minus b_j, and at most its ending coordinate plus b_j, in either coordinate. The rectangle (39) therefore contains the full segment; no assertion that it stays inside its level strip is needed.

The revised positivity proof is correct. With x_j=i_jh+delta_j, each side equals the corresponding actual endpoint displacement plus 2a_j and a strictly positive quantization remainder. Endpoint displacements are at least −b_j and 2a_j−b_j≥h. This applies to the final segment too. The exact perimeter identity W_j+H_j=tau_j+2h+4a_j follows directly.

For nonlast good segments, the shapes form precisely the stated finite family of possible padded dimensions. Counting some impossible shapes only enlarges the bound. All have positive limiting rescaled side lengths for fixed m,R, so their moment convergence is uniform over that finite family.

On nonlast bad segments, b_j≥h and a_j≤b_j+h≤2b_j. Summing their contributions gives at most (m+10) times their backward-step sum. The final segment contributes at most L+6h+4b_last, which is absorbed because m+10≥4. Hence (41) is valid, including the case J=1.

## 6. Skeleton entropy has no microscopic logarithm

For a fixed nonnegative s-vector of sum at most K, each next coarse endpoint has at most m+2s_j+5 choices. The product is bounded by (m+5)^J exp(K), and the number of such s-vectors is binomial(J+K,K). The prescribed final endpoint and confinement can be ignored for an upper bound. Only realizable skeletons need local rectangle variables; the loose count may include additional integer records.

At fixed q,m,R, K/J tends to 16m sqrt(q). With L=mh and sqrt(q)L tending to R as q tends to zero, the entropy contribution per 2sqrt(q)N is exactly of the form in (47). No raw lattice endpoint choices or hidden factor log(1/q) enter. The standard entropy inequality for the binomial coefficient is applicable also when K=0.

## 7. BK witnesses are genuinely disjoint

For a fixed skeleton and an actual segment with positive reward r, retain only the marked forward edges traversed by that segment. Under every assignment of the other edge states, the same segment's reward is at least its original reward. Monotone paths from the rectangle's lower corner to the segment start and from its end to the upper corner add nonnegative reward. Removing any resulting cycles cannot decrease reward. This certifies {X_j≥r} using only the original segment marks. If r=0, the empty set certifies the event.

These are valid product-space witnesses, even though their construction and the skeleton were selected using the original random environment. After fixing the skeleton the event inclusion is unconditional; there is no conditioning that changes Bernoulli laws. A simple global path has disjoint segment edge sets, hence disjoint retained mark sets. Padding paths need not be disjoint and are not included in the witnesses.

The witness definition and product inequality were checked in van den Berg–Jonasson's [primary-author restatement](https://arxiv.org/pdf/1105.3862), PDF pages 2–3. Mutually disjoint witnesses imply iterated disjoint occurrence, so the finite-many event product bound follows. Overlapping rectangle supports do not assert independence. Summing reward vectors and applying the tail generating-function identity gives (45), including its necessary per-segment factor S_theta.

Extending the mark field outside Q_N is harmless. For fixed N and the bounded skeleton family only a finite union of enlarged rectangles is needed; independent extra Bernoulli coordinates preserve every original event and certificate.

## 8. Global estimate and limit order

Combining the good moments, bad perimeter budget, skeleton count, and BK gives (46) with conservative factors. Dividing its logarithm by 2sqrt(q)N yields (47). In particular, the bad-perimeter term is 512theta(m+10)sqrt(q); this arithmetic is correct.

Choose epsilon,m first with Delta>0, then fix theta from the Poisson moment estimate. Next fix R large enough both for all finitely many Poisson shapes and for the entropy margin. Finally choose q sufficiently small, with a threshold independent of N. The terms involving K/J and the bad-perimeter contribution vanish as q tends to zero. Thus for each such fixed q the exponent is strictly negative as N tends to infinity.

The excluded K_N^+ event also vanishes at fixed q as N tends to infinity. Since 0≤D_N≤2N, the probability bound implies the expected-deficit bound. The resulting inequality holds for every sufficiently small q, allowing the final q-limit. There is no interchange of an unproved infinite-volume limit with the Poisson limit.

## 9. Fresh lower bound

Diagonal squares meet only at endpoints. Concatenating their optimizing paths is admissible in the larger square, and yields the required superadditive reward inequality. Taking expectations and the known fixed-q density limit proves g(q)≥E[D_ell]/(2ell); independence of those blocks is not needed for this expectation inequality.

Fixing R and taking ell=floor(R/sqrt(q)) invokes only fixed-scale sparse convergence. Its exponential domination supplies ordinary mean convergence. The resulting normalized lower bound is E[Lambda_{sqrt(2)R}]/(2sqrt(2)R). Sending R to infinity gives one. This lower bound is independent of the missing historical author/audit artifact and matches the audited upper bound.

## 10. Independent finite diagnostics and scope limits

A new checker imports no author code and uses a separate 0–1 shortest-path implementation. It exhausts all 198 corner-to-corner simple paths in squares with N=1,2,3, then checks nine scale choices per path: 1,782 skeletons, 4,260 rectangle enclosures/perimeter identities, and 4,260 mark-only witness tests. These include 2,206 bad rectangles. Every original segment witness is tested with every other mark set to zero. The checker also verifies 900 coordinate-separated sparse configurations against an independent strict-chain dynamic program and 90 log-space tail samples. All pass.

The frozen author checker was rerun separately. Its result exactly matches the pinned output: 541 path cases, 2,712 segment/witness checks, 172 positive-backtracking cases, 189 sparse-stability cases, and 72 skeleton-count checks. Normal, optimized, and isolated Python runs of the new checker produce identical result bytes. Its explicit failure checks remain active under optimization. These diagnostics support deterministic implementation details; none replaces the mathematical arguments or external theorems.

No unresolved mathematical blocker was found in the revised proof. Acceptance does not imply a novelty claim, an exhaustive search for prior solutions, publication, or independent human validation. Source PDFs/HTML and rendered source pages are local inspection evidence only; they are not part of an authored publication deliverable.
