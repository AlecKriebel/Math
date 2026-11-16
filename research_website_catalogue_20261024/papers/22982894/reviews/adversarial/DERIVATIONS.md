# Checkable universal derivations and falsification boundaries

This authored derivation concerns the full original real-GL theorem, not a replacement. INITIAL1aa50cd5 and actual own RESULTS71a14097 already froze its mechanisms before support/code/foreign exposure. Later archived slice-proof overlap was explicitly disclosed. This is extensive AI review, not formal certification or external human peer review.

## 1. Ordered tensor normalization

For a degree-d real homogeneous polynomial p, let A be its symmetric d-linear polarization. The tensor coefficient for multiplicities alpha is the ordinary monomial coefficient divided by d!/(alpha_1!...alpha_m!). Thus p(S t)=sum_(j_1,...,j_d) A(z_j1,...,z_jd)t_j1...t_jd for S whose columns are z_i. This is the coefficient contract used in all deductions below. It is distinct from an unweighted monomial expansion. Positive definiteness on R^m\{0}, m>=1, implies positive even integer degree d>=2.

## 2. Tangent slice with a genuine strictly positive lower bound

Let c=min_{||y||=1}p(y)>0 and choose ||v||=1 attaining c. Write P=p/c and T=A/c. Homogeneity gives P(y)>=||y||^d, with equality at v. For u perpendicular to v,
  h(t)=P(v+tu)-(1+t^2||u||^2)^(d/2)>=0,
  h(0)=0.
The usual two-sided derivative test gives
  T(v^(d-1),u)=0,
  T(v^(d-2),u,u)>=||u||^2/(d-1).
No global convexity is used. In particular, if B(a,b)=T(v^(d-2),a,b) and a=sv+u with u perpendicular to v, then
  B(a,a)=s^2+B(u,u)>=s^2+||u||^2/(d-1)>0 for a!=0.
This remains true for a flat sphere minimum, e.g. P(y)=||y||^d.

## 3. Exact quadratic coefficient and finite-neighborhood argument

Choose w_1,...,w_(m-1) orthonormal in v-perp and w_m=0. The columns x_i=v+epsilon*w_i have det magnitude |epsilon|^(m-1), so any epsilon!=0 works for rank. Fix an ordered tuple J and set a_r=w_jr. Define
  N(epsilon)=T(v+epsilon*a_1,...,v+epsilon*a_d),
  D(epsilon)=product_r P(v+epsilon*a_r),
  F(epsilon)=D(epsilon)-N(epsilon)^d.
Multilinearity and the vanishing first tangent derivative give
  N=1+epsilon^2 sum_(r<s)B(a_r,a_s)+O(epsilon^3),
  P(v+epsilon*a_r)=1+binom(d,2)epsilon^2 B(a_r,a_r)+O(epsilon^3).
Since the constant in N is1, [epsilon^2]N^d=d*sum_(r<s)B(a_r,a_s), whereas [epsilon^2]D=binom(d,2)*sum_r B(a_r,a_r). Also
  sum_(r<s)B(a_r-a_s,a_r-a_s)
    =(d-1)sum_r B(a_r,a_r)-2sum_(r<s)B(a_r,a_s).
Therefore the coefficient in F is exactly
  delta_J=(d/2)sum_(r<s)B(a_r-a_s,a_r-a_s).
For a mixed index tuple, some difference is nonzero because the w_i are pairwise distinct. Every term is nonnegative and one strictly positive. More quantitatively, pair differences of unequal chosen w's have squared norm>=1. A mixed d-tuple has at least d-1 unequal unordered pairs: if multiplicities are n_i, their number is (d^2-sum_i n_i^2)/2>=d-1. Hence delta_J>=d/2. This is not a uniform epsilon estimate because polynomial remainder coefficients can be unbounded as the input form varies.

For each fixed J, F(epsilon)/epsilon^2 tends to delta_J>0. A finite intersection over mixed J gives F>0 for one common sufficiently small positive epsilon. A separate finite intersection of N(epsilon)>0 neighborhoods exists since every N(0)=1. Pure tuples give F identically0. This proves 0<N<=D^(1/d), strictly for mixed tuples. The positivity step cannot be replaced by taking an even root without first checking sign.

Restoring p=cP,A=cT multiplies the desired inequality by c on both sides: product_r (c P(x_jr))^(1/d)=c*product_r P(x_jr)^(1/d). Finally z_i=x_i/p(x_i)^(1/d) yields p(z_i)=1 and the full strictly bounded mixed ordered entries. All columns remain independent. For m=1 the same final scaling handles the only pure tuple; mixed tuples are absent.

## 4. Separate local-slice finite maximum mechanism

B at v is positive definite by section2. Positive definiteness of a finite real symmetric matrix is open, and every conditioned slice T(y_1,...,y_(d-2),.,.) depends continuously on all its arguments. All columns can be chosen independent sufficiently near v; their positive P-unit normalizations remain near v. For these finitely many columns all conditioned slices are positive definite and all full tuple entries are positive. The d2 conditioning list is empty.

Let M be the maximum of the finite normalized tuple entries. Pure entries are1. If a mixed tuple attained M, it contains independent columns z_i,z_j. Strict Cauchy–Schwarz in the positive definite slice with the other d-2 arguments fixed gives
  M^2 < T(remaining,z_i,z_i)*T(remaining,z_j,z_j) <= M^2,
which is impossible. Thus the maximum is pure and equals1; every mixed entry is strictly smaller. This establishes the same full theorem without expansion of F. The public native descriptions had advertised a slice/Cauchy–Schwarz alternative before this reconstruction, and its actual archived proof was subsequently read; there is no claim of novelty or complete blindness to that hint. Its stronger all-tuples cone result is not substituted for a gap in the published target proof.

## 5. Exact boundary evidence and limits

The sealed own full rational output accounts for53 binary repetition rows,9 ordered3d quadratic rows,6 positive-scale controls and all nine predeclared exact hand fractions. In particular:

- With p=x^4-x^2*y^2+y^4, columns (1+t,1-t),(1,1), the correct-minimum-direction polynomial is1+14t^2+t^4. Small t works; t1 gives a mixed equality and t2 gives the k3 gap-318264. These falsify an all-epsilon strengthening, not the existence theorem.
- The same form with columns(1,t),(1,0) has wrong-direction first gap-3/16 at t1/2. The sphere-minimizer hypothesis in the construction matters.
- For p=(x^2+y^2)^2+(xy-1000y^2)^2, at t1/5 the k3 numerator is-147/50 while F>0. The separate N>0 neighborhood is essential. This is a positive definite form; no floating-point positivity inference is used.
- A normalized radial quartic example has ordered1122=2/3 and ordinary monomial1122=4. Confusing these conventions changes the target.
- Rank-one semidefinite p=x^d cannot have all normalized mixed entries strictly below1; strict positive definiteness cannot be discarded.

The selected supplied checker was replayed only on its nonconvex quartic certificate, in a byte-identical private copy after full reading. Its five coefficient classes and five polarization cross-checks are useful arithmetic agreement, not a proof of positive definiteness, minimizer existence, the common-epsilon quantifier, the general all-degree identity, or literature priority. Those are separately reasoned or bounded by actual primary reading. No computational assumption enters the universal proof. No repair, narrowed theorem or speculative new research question is adopted.
