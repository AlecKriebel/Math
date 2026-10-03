# Turn 4: uniform flag counting and a quantitative prefix upper bound

## Result and scope

Put a=log 3−1>0, where logarithms are natural. For the finite-prefix interpretation defined in SOURCE_SCOPE, this turn proves

    limsup_{D -> infinity} [log M(D) log log D]/log D
         <= C_* := (log 3−1)(log 2)^2       almost surely.   (1)

Equivalently, M(D)<=exp((C_*+o(1))log D/log log D) almost surely, with the limsup interpretation of the o(1). This improves turn 3 by controlling increasing multiplicity uniformly. It remains much larger than a power of log D, and does not determine the target log-log exponent.

The argument is a simplified diagonal-quotient consequence of the credited Ford–Green–Koukoulopoulos flag method. The sharper diagonal count also reproduces the upper half of the already known beta_2=1−1/log3 identity. That identity, including its lower half, is explicitly discussed in FGK v3 Section 3.4, page 16, equation (3.9) and Remark (a). Neither it nor this method is presented as a novelty claim. The proof below does not use the full-subflag classification or Mao–Song's recent claims.

## 1. A uniform counting lemma

Let D>1, L=log D, k>=2 be an integer, t_0=ceil(log_2 k), and 0<c<1. Assume D^c>=2, L>=2, and choose u>0. Define

    b=(u+2)log2,
    R=k log2+log(L+3)+log(2e)+b,
    q=cL−R.

If q>=1, then

    P(m(A intersect (D^c,D])>=k)
      <= 2 exp(a(1−c)L+b−t_0 q)
         +2(L+3)exp(−u^2/[2(L+2+u/3)]).                  (2)

No constants in (2) depend implicitly on k. If the exponent on its first term is positive the bound is merely uninformative, not invalid.

### Regularity

Use the endpoints D^c and D exp(−j)>=D^c, with j a nonnegative integer. There are at most L+3 endpoints. For Q(t)=|A intersect (D^c,t]|, its mean differs from log(t/D^c) by at most 2. Its mean is at most L+2. The Bernoulli Bernstein calculation supplied in turn 3 gives, by a union bound, an exceptional probability at most the second term in (2), outside which

    Q(t)<=(log t−cL)+u+2                                  (3)

at every endpoint. Only the upper bound (3) will be used. It also holds for counts of every residual subset B' of the realized window B.

### Flags and discrete data

As in turn 3, a witness of k distinct equal-sum subsets determines recorded integers K_1>...>K_t and binary vectors omega^1,...,omega^t with

    V_j=span_Q(1,omega^1,...,omega^j),  dim V_j=j+1,
    t_0<=t<=k−1.

The lower bound on t follows from the distinct coordinate patterns of the witness subsets. Put

    c_j=[L+ceil(log K_j−L)]/L, c_{t+1}=c,
    1>=c_1>=...>=c_t>c, S=sum_j c_j.

For a fixed t, there are at most

    [2^k(L+3)]^t                                         (4)

choices of the ordered recorded vectors and their integer bins. This overcounts dependent and improperly ordered choices and is therefore safe. Empirical type frequencies are not encoded. Removing the K_j gives B'. In the j-th bin (D^{c_{j+1}},D^{c_j}], all its type vectors belong to V_j. Types above D^{c_1} are in V_0 and contribute zero modulo V_0.

### Count residual sums using diagonal cosets directly

The image of V_j intersect {0,1}^k in Q^k/V_0 has at most

    q_j=2^{j+1}−1                                         (5)

members. Indeed the cube intersection has at most 2^{j+1} members by an injective choice of j+1 coordinate projections; both 0 and 1 occur and have the same image, saving at least one. No other identification is needed.

Set h_j=log q_j. For a fixed residual B' and coarse data, if n_j is its count in bin j, its number of possible quotient-valued sums is at most

    product_j q_j^{n_j} = exp(sum_j h_j n_j).               (6)

Every assignment of the quotient class of each residual entry determines one sum. Assignments within one class do not change the sum. This is an upper bound even when assignments do not respect the original witness conditions.

Write Q'_j=|B' intersect (D^c,D^{c_j}]| and Q'_{t+1}=0. Since the h_j are increasing, summation by parts and (3) give

    sum_j h_j n_j
      =h_1 Q'_1+sum_{j=2}^t(h_j−h_{j−1})Q'_j
      <= L sum_j(c_j−c_{j+1})h_j+(u+2)h_t.                (7)

This handles the error by one h_t, rather than by a sum of separately enlarged bin errors. There is no loss depending on how many entries were removed: residual counts satisfy the same upper bounds as original counts. In the probability sum we consider only residual sets obeying (3).

### Exact reconstruction and weights

In Q^k/V_0, the equation

    sum_j K_j omega^j = −sum_{b in B'} b omega(b)

determines at most one recorded tuple per possible residual sum, because the omega^j are independent modulo V_0. The exact finite-window probability ratio is

    P(A intersect I=B)/P(A intersect I=B')
        =product_j 1/(K_j−1) <=(2e)^t D^{−S},              (8)

since K_j>=D^c>=2 and D^{c_j}/e<K_j. Repeated or residual entries are not allowed in the reconstructed tuple; ignoring invalid solutions only enlarges the bound.

For each fixed coarse datum, sum (8), with the reconstruction count (6), over the admissible residual B'. Their probabilities sum to at most one. The exponent apart from t log(2e) is therefore at most

    L[−S+sum_j(c_j−c_{j+1})h_j]+(u+2)h_t.                (9)

This use of residual probabilities does not assert that the deletion operation preserves their law.

### An explicit negative gap

We have h_1=log3=1+a. For j>=2,

    0<h_j−h_{j−1}
      =log[(2^{j+1}−1)/(2^j−1)]<=log(7/3)<1.

The last inequality follows, for example, from e>1+1+1/2>7/3. Thus all coefficients after the first in the next expansion are negative:

    −S+sum_j(c_j−c_{j+1})h_j
      =(h_1−1)c_1+sum_{j=2}^t(h_j−h_{j−1}−1)c_j−c h_t
      <=a−c(t+a).                                        (10)

Here c_1<=1 is used on the positive coefficient a, and c_j>=c on the negative coefficients. The formula includes t=1, with an empty middle sum. Also h_t<=(t+1)log2. Combining (4), (9), and (10), the contribution from fixed t is at most

    exp(a(1−c)L+b−t[cL−R]).                               (11)

When q>=1, summing the geometric series over t>=t_0 gives a factor 1/(1−e^{−q})<2. Add the regularity failure probability. This proves (2), including its claimed uniformity.

## 2. A fixed-k annular consequence

For a fixed k and c with

    c > a/(t_0+a),

take u=L^(3/4). Then R=o(L), and the first exponent in (2) is

    [a−c(t_0+a)]L+o(L)<0.

Both terms are summable at D=2^n. Thus the annular multiplicity is eventually less than k on those scales almost surely. In particular,

    beta_k <= (log3−1)/(ceil(log_2 k)+log3−1).              (12)

For k=2 this is the known upper bound 1−1/log3. For larger k (12) is only a coarse bound; it is not an asymptotic evaluation of beta_k, and gives no finite value for the exponent zeta from turn 1.

## 3. Choose genuinely growing parameters

Fix epsilon>0. For all sufficiently large L set

    k=floor[L/(log L)^3],
    t_0=ceil(log_2 k),
    u=sqrt(L) log L,
    c=(a+epsilon)/t_0.                                   (13)

Then k>=2, t_0~log L/log2, 0<c<1, and D^c>=2. Further,

    R=O(L/(log L)^3+sqrt(L)log L+log L),
    t_0 R=o(L), b=o(L), q=cL−R -> infinity.

The first exponent in (2) is

    a(1−c)L+b−t_0(cL−R)
      =−epsilon L−acL+b+t_0R <=−epsilon L/2               (14)

for all sufficiently large L. Since u/L->0, the other exponent is at most −(1/3)(log L)^2 for all sufficiently large L. The resulting bound

    2 exp(−epsilon L/2)+2(L+3)exp(−(log L)^2/3)            (15)

is summable at D=2^n: L=n log2, and the second summand is eventually smaller than n^{−2}. All uses of growing k have thus been checked in the original explicit inequality, rather than inserted into an unknown constant C_k.

## 4. Deduce the prefix bound

For disjoint B,C, m(B union C)<=2^{|B|}m(C), as proved in turn 3. Borel–Cantelli applied to (15) gives, almost surely eventually on D_n=2^n,

    M(D_n)<k(D_n) 2^{N(D_n^{c(D_n)})}.                    (16)

The almost-sure count law N(T)/log T->1 applies along this deterministic sequence because D_n^{c(D_n)}->infinity. Hence

    log M(D_n)<=log k(D_n)+(1+o(1))(log2)c(D_n)log D_n.

Now log k=O(log L)=o(L/log L), and c~(a+epsilon)log2/log L. It follows that

    limsup_n [log M(D_n) log log D_n]/log D_n
         <=(a+epsilon)(log2)^2.

Monotonicity of M fills between consecutive dyadic D_n; the ratios of both logarithmic normalizing factors tend to one there. Take a countable intersection over epsilon=1/m, m>=1, and then let m->infinity. This proves (1).

## Remaining gap at 4/5

The sharp growth of M(D) is still not known here. In particular, (1) does not establish a finite upper bound on log M(D)/log log D. The credited lower exponent eta and the upper scale (1) are far apart. Fixed-threshold identities, even if fully verified, do not close this growing-prefix gap by themselves.
