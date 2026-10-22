# Independent structural and labeled-law acceptance audit

Audit date: 14 October 2026 UTC. No universal-resolution claim is made.

## Verdict

**Accepted for the fixed cases alpha=132 and alpha=213**, conditional only on the explicitly cited Bóna bijection and his tree-count generating function, used with the corrected vertex indexing. No unresolved mathematical obstruction was found in the frozen author draft reviewed below. This is an independent correctness audit of the written argument, not a novelty certificate or a full audit of Bóna's published proof.

Reviewed artifact:

- `pass1_uncovered_case/HEIGHT_PROOF_DRAFT.md`
- Length: 12089 bytes
- SHA-256: `c05d0fec32c80fa4c4508e9617e0792f4ab94b097ba6282901d32e894a2dd747`

The argument proves an exponentially small probability of fixed positive weak-metric deviation for uniform Av_n(1342), followed by exact geometric symmetries. It does **not** resolve the universal nonempty-alpha target, and in particular does not cover alpha=312 / forbidden4231 / reversed1324.

## 1. Exact-law and decomposition audit: pass

Bóna's word “indecomposable” means **skew-indecomposable**, as his explicit definition requires a putative cut to put all larger entries before all smaller entries. The general class is an ordered skew forest. This distinction is essential: a direct-sum forest would not align component anti-diagonals, whereas the actual skew forest does.

The source's labeled-tree bijection sends each permutation to precisely one labeled forest. Uniform permutations are therefore uniform labeled forests. The author does not assume that the unlabeled tree shape is uniform, or that labels can be sampled independently. This repairs the principal law-transfer obstruction raised in the initial audit. The relaxed-root class is used solely as an upper-counting device, with an injective inclusion of proper trees, so its different law causes no mismatch.

At n=3, the path has two proper labelings and the star one. The author never applies the uniform-Catalan height theorem to this biased shape law.

## 2. Catalytic equation and analytic branch: pass

For relaxed-root trees, let B(z,u) weight the root label by u and let C(z)=B(z,1)/(1-B(z,1)). For a nonempty child sequence with label sum S, summing its permitted parent labels gives `(1-u^(S+2))/(1-u)`. This proves exactly

`B=z+z/(1-u)[C-u^2 B/(1-B)]`.

The proper-tree identity `T=z/(1-B(z,1))` is exact, including the singleton tree. Its root label is determined, so it contributes no extra multiplicity.

I independently expanded and simplified the quadratic at u=3/2. With s=sqrt(1-8z), multiplying the author's quadratic by a nonzero scalar gives the polynomial

`[-16(s+1)b^2 + (4s^3+12s^2+8s+8)b + 5s^3-3s^2-s-1]/[32(s+1)]`.

Its discriminant is

`s^3(s^3+6s^2+33s+24)/[64(s+1)^2]`.

The author's displayed smaller-root formula has zero residual in that polynomial, is zero at z=0, and is analytic near zero. The discriminant is strictly positive for 0<s<1; the denominator is nonzero. Thus there is no positive-real singularity below rho=1/8. Together with the nonnegative coefficients and Pringsheim's theorem, this establishes convergence of the actual combinatorial series on 0<=z<rho, rather than just formal manipulation.

An alternative elementary positive-radius justification is available if desired: changing a proper root to a relaxed root adds at most n+1 root-label choices, and the root label is at most n. Hence the u=3/2 coefficient is at most `(n+1)(3/2)^n t_n`. The displayed analytic formula already gives positive radius, so this is optional clarification rather than a missing hypothesis.

The independent critical expansions are

`b=1/4-(sqrt(6)/4)s^(3/2)+(3/8)s^2+(5sqrt(6)/64)s^(5/2)+O(s^3)`,

`M=1-(2sqrt(6)/3)s^(3/2)+(5sqrt(6)/24)s^(5/2)+O(s^3)`.

These verify the weaker error bounds used by the author. In particular the negative `(1-8z)^(3/4)` term genuinely dominates the positive `log(rho/z)` term, whose order is `1-8z`.

## 3. Marked-depth inequality: pass

W_h counts every node at depth h, with multiplicity, and weights only the root label. For a marked child and arbitrary ordered siblings, replacing the parent-label sum by `u^(S+2)/(u-1)` factors the weights exactly into one W_h and two sibling sequences. This gives

`W_(h+1) <= z*u^2/[(u-1)(1-B)^2] * W_h`.

No child-label independence is being asserted. The algebra is an enumeration of all ordered tuples. Leaf roots contribute nothing to W_(h+1), as required.

For fixed z<rho, convergence of every W_h follows, for example, from `W_h <= z*(partial B/partial z)` in the positive series and analyticity inside the radius. Consequently the analytic inequality and iteration `W_h<=b M^h` are legitimate. This convergence observation can be stated explicitly in a polished version but does not create a gap in the existing argument.

Every proper beta tree is a relaxed-root tree by retaining its existing labels. Its weight u^(root label) is at least one. A proper tree with height at least h contains at least one vertex at depth h. Therefore its unweighted generating series is dominated by W_h. The coefficient-to-value bound is then valid for each fixed n and h=ceil(epsilon n).

The corrected t_n asymptotic is `3/(16 sqrt(pi))*8^n*n^(-5/2)`. Choosing z by the negative logarithmic exponent gives `C_z n^(5/2) q^n`, where q<1. The polynomial factor can be absorbed into a weaker exponential rate. This is an asymptotic proof for the exact law, not a finite-sampling inference.

## 4. Full forest and geometry: pass

The forest estimate has precisely two unmarked sequences, producing A(z)^2, and one marked proper component bounded by W_h. This yields `A(z)^2 b(z)M(z)^h`. At the fixed selected z<rho, the factor is finite because T(z)<=T(rho)=5/32<1. The full forest denominator is at least t_n, so no unproved largest-component theorem is needed.

I independently derived the more general normalized-permutation vertex formula

`i+q_i = k+subtree_size(v)-depth(v)`.

For leaves this is `k+1-depth(v)`. Leaves are exactly the left-to-right minima; the bijection preserves their positions and values. Thus all points of the associated permutation satisfy the author's one-sided inequality. Skew-block shifts cancel to give `i+p_i>=n+1-H(F)` globally.

The square-permuton off-by-one is correct: lower-left square coordinates give `x+y>=1-(H+1)/n`. Uniform marginals imply zero mean of X+Y-1. Its mean absolute value is at most `2(H+1)/n`, and the explicit coupling to (X,1-X) bounds both W_1 and d_BL.

An avoider ending in its maximum has a potentially macroscopic **positive** displacement of one point from the anti-diagonal. This does not contradict the one-sided bound, or the weak-permuton conclusion: that point has mass 1/n. The proof makes no false two-sided maximum-displacement or total-variation claim.

## 5. Symmetry and target scope: pass

Position reversal maps1342 to2431 and anti-diagonal to diagonal. Inversion maps1342 to1423 and fixes the anti-diagonal; subsequent reversal gives3241. All these transformations are exact bijections of finite avoidance classes and isometries of their square-spread permutons. Therefore uniformity and weak convergence transfer, proving target cases alpha132 andalpha213.

This is stronger than a Wilf-count equivalence and correctly justifies its geometric effect. The unrelated pattern4231 is not obtained; neither it nor arbitrary alpha is covered.

The historical sources remain correctly qualified. The 2023 announcement is not used as a proof. The 2026 v3 paper's conjectural statement remains its reported historical status; the present argument is offered separately and is not attributed to that paper.

## 6. Finite independent regression checks

The included script `check_geometry_and_counts.py` directly generates all plane-tree shapes through n=8, enumerates every admissible label assignment by exact integer polynomial convolution, and independently counts the proper and relaxed-root trees. The proper counts are

`1,1,3,12,56,288,1584,9152`.

It also enumerates every permutation through n=7, filters1342 avoidance directly, constructs the skew components and132-normalized tree shapes, and verifies the vertex identity, each block's one-sided bound, and the full forest bound. The checked avoidance counts are

`1,2,6,23,103,512,2740`.

All checks pass. `finite_checks.json` contains the complete output. These computations are regression checks only; the asymptotic acceptance rests on the analytic and deterministic arguments above.

## Requested edits

No mathematical correction is required for acceptance of this frozen draft. Two optional expository clarifications are useful: explicitly mention analyticity at z=0 when establishing the positive radius, and note `W_h<=z B_z` when first invoking convergence of marked-depth series. Keep the indexing caution and skew-sum wording in any public presentation.
