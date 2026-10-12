# Independent probability audit: PR316 / 9900002

Closed 2026-10-04 UTC. **PASS within the renewal/probability scope; no mathematical gap found in that scope.** Original substantive author count remains **1/5**. This is verification of the complete existing candidate, not a new author search turn, historical-priority finding, publication clearance, or whole-package acceptance.

The immutable source-first assessment was recorded before any candidate access. The immutable first candidate assessment was recorded after reading only `TURN_1.md` and before author code/inherited review access. After the root's separate releases, all 18 files in the frozen target folder were read. Other fresh-family/root scientific conclusions remained unread through this closure. The submitted proof is pinned at SHA256 `996947d8d995699411499b3bbdb781f25ae9a729900fb33074104cbf9e411cab`.

## 1. Admissibility, without invoking a renewal theorem

Write `p_n=2^(-2^n)` and `a_n=2^(4^n)`, for `n>=1`. Since `p_{n+1}=p_n^2`, for `j>=0` we have `p_{1+j}=(1/4)^(2^j)<=(1/4)^(j+1)`. Therefore `sum p_n<=1/3` and `p_0=1-sum p_n>=2/3`. The countable mixture with mass `p_0` uniform on `[1,2]` and masses `p_n` at finite `a_n` is a normalized probability measure on finite positive real values. It has no atom at infinity, even though its support is unbounded. Every draw is at least one.

For every `d>0`, the countable set `d Z` has zero uniform probability. Consequently `P(X in d Z)<=1-p_0<=1/3<1`; the law is non-lattice under the source's definition. The mean is infinite: `E X>=p_n a_n=2^(4^n-2^n)` for every `n`, and these lower bounds diverge. This argument does not conflate infinite mean with a positive chance of an infinite draw.

Zero delay is an admissible independent nonnegative delay. For zero delay, `S_k>=k`; hence the strictly-after index `N(t)=min{k>=1:S_k>t}` is finite for every finite `t>=0`. The possible source ambiguity involving `X_0` before a positive delay is absent from this example.

## 2. Independent concentration proof from a bounded number of failures

Fix `n>=2`; put `q=P(X>=a_n)` and `K=min{j>=1:X_j>=a_n}`. Let `r=1-q`. Independence gives

`P(K=j, X_K=a_n)=r^(j-1) p_n`.

Thus `K` is geometric, finite almost surely, and the exact desired mark probability is `p_n/q`. All failures before `K` have length at most `A=a_{n-1}`. Set

`t=a_n/2`,  `B=t/A=2^(3*4^(n-1)-1)`.

`B` is an integer. If `K<=B+1`, then the first success's start time `T=S_{K-1}` obeys `T<=(K-1)A<=BA=t`. If additionally `X_K=a_n`, all earlier renewal times are at most `t`, whereas `S_K=T+a_n>t`. Hence `N(t)=K` and `D_t=a_n`. This includes `T=t` exactly, as required by the strictly-after convention.

Summing the independent draw probabilities gives the finite geometric event bound

`P(D_t=a_n)>=(p_n/q) [1-r^(B+1)]`.

For every `0<p<1`, `sum_{j>=0}p^(2^j)<=sum_{j>=0}p^(j+1)=p/(1-p)`. Therefore `p_n<=q<=p_n/(1-p_n)` and `1-p_n/q<=p_n`. For integer `m>=1`, Bernoulli's inequality applied to `(1-q)^(-m)` gives `r^m<=1/(1+m q)`. It follows that

`P(D_t!=a_n)<=p_n+r^(B+1)<=p_n+1/(p_n B)`.

Finally

`p_n B=2^(3*4^(n-1)-1-2^n)>=2^(4^(n-1))` for every `n>=2`,

because `2^n+1<=2*4^(n-1)` (true at `n=2`, and directly `2^n<=4^(n-1)` for `n>=2`). Hence the independent explicit bound is

**`P(D_(a_n/2)!=a_n)<=p_n+2^(-4^(n-1)) -> 0`.**

Also `t_n=a_n/2->infinity`. This verifies the essential probability input by a mechanism that needs neither an expectation of a stopping sum, Wald's identity, nor Markov's inequality.

## 3. Separate verification of the candidate's expectation and error bound

For `M=E[X 1_{X<a_n}]`, support boundedness gives `0<M<=a_{n-1}<infinity`. Pathwise,

`T=sum_{j>=1} X_j 1_{K>j}`.

The event `K>j` contains both the preceding draws being small and the current draw being small. Tonelli plus independence therefore gives

`E T=sum_{j>=1} r^(j-1) M=M/q`.

Equivalently, the number of failures has mean `r/q` and the conditional failed-draw mean is `M/r`, giving the same product. Substituting the unconditional infinite mean would be invalid. The candidate does not do so and does not invoke Wald on an infinite-mean crossing increment. No independence of `T` and the successful mark is needed for its union bound.

The failed crossing event is contained in `{T>t_n} union {X_K!=a_n}`. Its probability is at most `(q-p_n)/q+2M/(q a_n)`. From `q>=p_n`, `q-p_n<=p_n^2/(1-p_n)`, and `M<=a_{n-1}`, this is at most the candidate's

`epsilon_n=p_n/(1-p_n)+2^(1+4^(n-1)+2^n-4^n)`.

The exponent equals `1+2^n-3*4^(n-1)` and is at most `-4^(n-1)` for `n>=2`, by the inequality proved above. Thus the submitted explicit bound also vanishes. Its starting index `n=2` is sound; the uniform component is below the preceding atom and below `t_n`.

## 4. Truncated-mean scale, with an exact split

For `m(t)=E[min(X,t)]`, `1<=m(t)<=t` for `t>=1`, and monotonicity follows pointwise. At `t_n`, all lower support is at most `a_{n-1}<t_n`, while all upper support is at least `a_n>t_n`. Exactly

`m(t_n)=M_n+t_n q_n`.

Consequently

`0<m(t_n)/a_n<=2^(-3*4^(n-1))+p_n/[2(1-p_n)] -> 0`.

On the concentration event, `D_(t_n)/m(t_n)=a_n/m(t_n)->infinity`. For each fixed real `L`, choose `n` sufficiently large that this deterministic ratio exceeds `L`; then the probability of exceeding `L` is at least the concentration-event probability and tends to one. Thus the normalized subsequence escapes to infinity and is not tight. This is a direct failure of the proposed scale, not merely an inferred corollary of the all-scale argument.

## 5. Finite controls, failures, and exact scope

`probability_controls.py` is a fresh exact-rational checker with binary-shift parameter generation, enumeration of actual finite renewal paths, and separate enumeration of failed-draw tuples with the unfinished partial sum retained. It checks the geometric hit-mark and stopped-sum identities, the candidate bounds and truncated-mean identity, and 12 finite law/time cases. Meaningful controls remove needed conditions: equal desired/larger-tail masses give desired probability `7/16`; an excessive wait with success probability `1/100` gives desired probability `3940399/100000000<1/20`; a first successful length three at time four need not contain the observation; and the strict endpoint convention selects six after the path `[2,6]` at time two, while a weak crossing selects two. These are controls of the mechanism, not substitutes for the infinite proof.

The current fresh checker passes **263 exact assertions**. The submitted author checker passes **7,852** and the inherited checker passes **646**, both with byte-identical stdout to their recorded outputs. Complete current stdout, stderr, UTC, actual argv, working directory, and exact program bodies are in the single `CONTROL_EXECUTION_RECEIPT.json`; the fresh output is `CONTROL_OUTPUT.json`. The only actual failed execution in this family's work was the initial attempt to use the not-yet-created assigned directory. Its complete available error/body/arguments and observed-after-failure UTC are preserved in `FAILED_EXECUTIONS.jsonl`; the process never started. No mathematical test failed, and no failed run was silently replaced.

**Strongest verified result:** the explicit law is admissible and has `P(D_(a_n/2)=a_n)->1`, with the full submitted expectation, tail, endpoint, and truncated-mean claims independently proved. No unresolved mathematical gap remains in this assigned probability scope. The proper-limit/tightness transition is assigned to the independent normalization family; the source binary authentication, historical priority, all-family/root acceptance, and any preprint adversaries are outside this scoped clearance. Original primary institutional PDF binary/visual access is still pending; the source correspondence rests here on the supplied indexed-primary-source account and pinned statement, not independently acquired PDF pixels.

Checkpoint: assigned probability mathematics **100%**; assigned verification workflow **100%**. These are scoped completion estimates, not probability-of-truth claims. All held source/candidate-stage artifacts remain unchanged. No external contact, Git mutation, publication, or extra author turn was performed.
