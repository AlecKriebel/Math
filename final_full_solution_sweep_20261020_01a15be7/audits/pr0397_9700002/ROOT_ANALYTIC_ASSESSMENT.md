# Root independent reconstruction: PR397 /9700002

The target is a specialized existence response to Aldous's conceptual toy-model request, not a universal traffic theorem or a uniquely determined conjecture. The original live primary congestion page and index were independently read on 2026-10-21. The optional linear-variance example must not be silently replaced by the candidate's quadratic-variance affine random slopes. Novelty and full source adequacy remain pending fresh independent source/priority review.

## Exact mathematical claim reconstructed

For the complete binary tree of height H, k=2^(H-1), 4k-1 vertices, cross-root k^2 commodities have unique paths. Positive linear prices and feasibility of doubled unit demands give componentwise necessary and sufficient capacities 2k*k_e, hence the unique cheapest capacity vector. Each finite network is frozen before iid Exp(1) future slopes X_ij are sampled. Admitted-demand optimization for d_ij(t)=1+(t-1)X_ij reduces exactly to a k-by-k transport problem with every row/column capacity 2k; internal tree constraints are sums of terminal constraints.

Max-flow/min-cut gives F_k(t)=min_{A,B}[2k(k-|A|+|B|)+|A|(k-|B|)+(t-1)sum_{A x (R\B)}X]. Its right derivative is the minimum slope among active affine pieces, divided by S=sum X for the normalized marginal. A finite minimum of nondecreasing affine functions is concave and continuous; right derivatives exist at ties. S>0 almost surely. Cases with S=0 are outside this probability-one model, not silently divided by zero.

If all offered row/column sums are strictly below 2k, full admission is the unique optimal admitted matrix and every physical edge is strictly spare. If optimal total reaches 2k^2, every row and column equals capacity; consequently every physical edge is saturated for every optimizer. These conclusions do not rely on an optimistic optimizer or an extraneous routing convention.

## Independent probability derivation

For a sum Z of n independent Exp(1) variables, Chernoff with lambda=1-1/a gives exponent n I(a), I(a)=a-1-log(a). For 0<delta<1, derivative comparisons yield I(1/(1-delta))>=delta^2/2 and I(1/(1+delta))>=delta^2/8: the respective delta derivatives are delta/(1-delta)^2>=delta and delta/(1+delta)^2>=delta/4. A 2k union bound at t-=2-delta gives failure <=2k exp(-k delta^2/2); no row/column independence is assumed.

For t+=2+delta, only cuts with a=|A|,d=|R\B|, a+d>k require a positive lower bound. The identity ad-k(a+d-k)=(k-a)(k-d)>=0 shows that a failing cut implies its ad independent rates sum to less than ad/(1+delta). Thus failure <=exp(-c ad), c>=delta^2/8. Put q=min(a,d),ell=k-max(a,d), so 0<=ell<q and ad=q(k-ell). For q<=floor(k/2), at most 2q k^(2q) set pairs occur and ad>=qk/2. For q>k/2, use at most4^k pairs and ad>k^2/4. At delta=8 sqrt(log(k)/k), the two failure sums are <=2k^-2/(1-k^-2)^2 and (4/k^2)^k. The lower phase contributes2k^-31. All estimates concern a single event and all times outside the two endpoints by monotonicity; no timewise union bound is hidden.

The proof is valid for all sufficiently large binary k with delta<1. For fixed t<2 or t>2, the shrinking interval eventually excludes t; full-tree versus isolated-vertex spare components follow. S/k^2 tends to1 with variance1/k^2. At t=2, squeeze F_k(2) between k^2+(1-delta)S and2k^2 on the same event; derivative convergence at2 is not asserted. The failure bound is summable along binary k, so Borel--Cantelli needs no independence across sizes.

## Present verdict and limitations

Root finds the stated deterministic and probability arguments complete, conditional on the precise declared model, after reading every proof section. This is a proof reconstruction, not empirical certification of rare events or a literature conclusion. The original clean replay attempted with bundled Python failed before execution at missing SciPy; a fresh probability reviewer is investigating the dependency/version-specific output comparison using the existing repository virtual environment. Frozen originals are unchanged. Independent flow, probability and original-source/priority families remain pending before any publication decision.
