# An explicit joint stationary law for the drift–jump process

9700040 / AMR-096-0040. **First-turn full candidate, not yet independently reviewed.** This is an explicit classical RSK/Schur-process consequence, with no novelty claim. The source asks for a fairly explicit stationary distribution; the result below supplies every finite joint distribution by positive factorial-determinant sums and an effective certified truncation. It does not claim a closed elementary density, an efficient algorithm for large indices, or a Markov property in particle index.

## 1. Exact process and notation

There are k ordered particles 0 < X_1 < ... < X_k < infinity. Between jumps dX_i/ds=X_i. A rate-one Poisson point process on positive space times time moves the closest particle strictly to the right of an event to that event; events above X_k do nothing. Write X_0=0. The generator on suitable smooth functions is

L f(x) = sum_i x_i partial_i f(x) + sum_i integral_(x_(i-1))^(x_i) [f(x with x_i replaced by y)-f(x)] dy.

No particle is inserted into this finite-k process. Boundary equalities have probability zero. The finite process is nonexplosive on bounded time intervals because X_k(s) <= X_k(0)e^s and only finitely many events lie below that deterministic bound.

A partition lambda is a finite decreasing sequence of positive integers, including the empty partition. Its size is |lambda| and its largest part is lambda_1 (zero for the empty partition). For t>=0 put h_r(t)=t^r/r! for r>=0, h_r(t)=0 for r<0, and h_0(0)=1. For mu contained in lambda define

D_t(lambda/mu) = det [ h_(lambda_i-mu_j-i+j)(t) ]_(1<=i,j<=ell),                 (1)

padding by zeros to any ell at least both lengths; the empty determinant is one. Set D=0 if containment fails. The value does not depend on extra zero padding. Classical skew Jacobi–Trudi and the exponential specialization give

D_t(lambda/mu) = t^(|lambda|-|mu|) f^(lambda/mu) / (|lambda|-|mu|)!,            (2)

where f^(lambda/mu) is the number of standard tableaux of that skew shape. In particular every weight is nonnegative. Formula (1), rather than an unknown tableau count, can be used for evaluation. These classical inputs are cited precisely in SOURCES.md.

## 2. Full joint-law formula

Fix 0=x_0<x_1<...<x_m and positive integer indices r_1,...,r_m. Put b_j=r_j-1 and Delta_j=x_j-x_(j-1). For the unique stationary law of the source process,

P( X_(r_j) > x_j for every j )
 = exp(-x_m) sum D_1(lambda^(m)/empty) product_(j=1)^m D_(Delta_j)(lambda^(j)/lambda^(j-1)),       (3)

where the sum runs over all nested partitions

empty=lambda^(0) contained in lambda^(1) contained in ... contained in lambda^(m),
with lambda^(j)_1 <= b_j for every j.

Containment may be equality. The series is absolutely convergent and positive. All finite joint survival probabilities, and hence all finite joint distributions, are specified. To use arbitrary thresholds, sort the distinct positive thresholds, retain the associated indices, and merge repeated thresholds by taking the smallest index. Nonpositive thresholds impose no condition. Inclusion–exclusion recovers distribution functions with <= rather than >. There is no requirement that the indices increase in the sorted threshold order.

There is a useful fixed-dimension version: transpose every partition in (3). Since skew standard tableaux transpose bijectively, all D weights are unchanged by (2), while each constraint becomes length(lambda^(j)) <= b_j. Thus every determinant can be padded to the fixed size B=max_j b_j, independently of the total number of boxes. If B=0 only the empty chain contributes, giving exp(-x_m).

## 3. Stationary construction and exact identification of the dynamics

Let Pi be a unit-intensity Poisson point process on the quadrant (u,v)>0. Let L(x,t) be the largest length of a chain of points in (0,x] times (0,t] strictly increasing in both coordinates. Define

Z_i(t)=inf {x>0: L(x,t)>=i}.

For fixed t>0 these positions are finite almost surely: take i disjoint successive horizontal time strips in (0,t]; in each strip there are almost surely points arbitrarily far to the right, so choose an increasing chain recursively. The positions are positive, distinct and locally finite, because the rectangle contains finitely many points with distinct u coordinates. The count identity is #{i:Z_i(t)<=x}=L(x,t).

The patience-sorting identity says these are the particle positions of the ordinary Hammersley process started from the empty configuration at time zero, with a new particle supplied from infinity when required. Indeed, processing the points by increasing v, replace the smallest pile top strictly larger than u by u, or append u if none exists. The resulting sorted pile tops are exactly the minimal possible terminal values of increasing subsequences of each length. Restricting to a bounded rectangle is consistent with larger rectangles: a point to its right cannot affect the pile tops inside it. This finite identity constructs the stated infinite process without an infinite-event ordering assumption.

Define, for every real s,

Y_i(s)=e^s Z_i(e^s).                                                        (4)

The event transformation (u,v) -> (x=uv,s=log v) has Jacobian one, since du dv = dx ds. Between transformed events (4) drifts with derivative Y_i. At an event it makes the nearest-right jump. The first k coordinates form an autonomous system: events above Y_k leave them alone, and all particles have already entered from infinity at every finite s. Thus its generator is exactly Section 1, with no immigration in the finite-k projection.

For any real a, the area-preserving map (u,v)->(e^a u,e^(-a)v) preserves the Poisson law and sends the whole trajectory Y(s) to Y(s+a). Consequently Y is strictly stationary. At s=0 its counting function is L(x,1).

For completeness, uniqueness can be proved by the classical synchronous coupling. Couple two finite-k processes with the same future event field. Suppose their first i-1 coordinates have already coalesced at time tau, and let a be the smaller i-th coordinate then and b the common (i-1)-st coordinate (b=0 for i=1). We have a>b. Until the i-th coordinates coalesce, the smaller one cannot jump: any event that would move it lies above the common previous coordinate and below both i-th coordinates, so moves both to the same point. It therefore remains a exp(s-tau); the common previous coordinate is at most b exp(s-tau). An event in the deterministic moving strip b exp(s-tau)<x<a exp(s-tau) forces coalescence if it has not happened already. That strip has accumulated area (a-b)(exp(s-tau)-1), tending to infinity. The strong Markov property of the driving Poisson field gives finite coalescence time almost surely. Induction couples all k coordinates in finite time. This yields uniqueness of each finite invariant law; consistency identifies the infinite locally finite law. This coupling is credited to Aldous–Diaconis's 1993 Lemma 33; the argument here spells out its use.

## 4. Derivation of the joint formula by finite RSK counting

At the stationary time s=0, sort the points of Pi in (0,x_m] times (0,1] by increasing u. Their u-coordinates form a rate-one Poisson process, and their v-marks are independent uniform random variables. The number in each strip (x_(j-1),x_j] is an independent Poisson variable d_j with mean Delta_j. Conditional on the strip counts, the relative order of all n=sum d_j marks is a uniform permutation of n letters. Let n_j=sum_(i<=j) d_i.

Apply the classical Robinson–Schensted bijection to that permutation in its u order. The insertion shape lambda^(j) after n_j letters has first row equal to L(x_j,1), by the increasing-subsequence theorem. The recording tableau Q has shape lambda^(j) on entries 1,...,n_j. For prescribed nested shapes with these sizes, the number of possible Q is product_j f^(lambda^(j)/lambda^(j-1)); labels in distinct successive blocks are forced into their respective skew strips, and each block is a standard skew tableau. The final insertion tableau P can be any of f^(lambda^(m)) standard tableaux. Therefore the conditional probability of this shape chain is

f^(lambda^(m)) product_j f^(lambda^(j)/lambda^(j-1)) / n!.

Multiplying by the independent strip-count probability exp(-x_m) product_j Delta_j^d_j/d_j! gives precisely the summand in (3), by (2). Finally X_r>x iff L(x,1)<=r-1, which yields the constraints in (3). This direct counting proof needs no unproved Markov property of either the pile tops or the shape process.

Summing all chains of terminal size n, without the row constraints, recovers the probability that the rectangle has n points. Thus the raw (pre-exponential) sum at size n is x_m^n/n!. This proves positivity, normalization, absolute convergence, and the tail bound used next.

## 5. Certified finite computation

Let W_N be the raw constrained sum in (3) with terminal size at most N. It is a finite sum of explicit determinants. For rational x_j it is rational. Define

T_N = sum_(n=0)^N x_m^n/n!,
R_N = [x_m^(N+1)/(N+1)!] / [1-x_m/(N+2)]   when N+2>x_m.

The omitted raw mass E satisfies 0<=E<=R_N by a geometric bound on the exponential tail; the omitted constrained raw mass lies between zero and E. Also 0<=W_N<=T_N. It follows that the exact target probability P obeys the entirely rational enclosure

W_N/(T_N+R_N) <= P <= (W_N+R_N)/(T_N+R_N).                                  (5)

For the upper bound write P<=1-(T_N-W_N)/(T_N+E) and use E<=R_N; the lower bound follows directly. The width is R_N/(T_N+R_N), tending to zero. Hence (3) is an effective arbitrary-precision description of every finite joint law, without simulation, unknown stationary functions, or a special-function oracle. Standard partition enumeration with fixed determinant size B and a finite terminal-size cutoff is enough. No favorable runtime bound as the indices grow is claimed.

The same representation defines the law at arbitrary real query coordinates; computability of unspecified noncomputable reals is not asserted. Continuity follows, for example, because an atom at a deterministic coordinate would require a Poisson point with that exact u-coordinate, an event of probability zero.

## 6. Known low-index checks, not new results

For r=1 only the empty shape is allowed, so X_1 is exponential of mean one. For 0<x<y, the r=(1,2) event forces the first shape empty and the final shape a column. Equation (3) reduces to

P(X_1>x, X_2>y) = exp(-y) sum_(n>=0) (y-x)^n/(n!)^2.                         (6)

Differentiating this locally normally convergent series twice gives

p_2(x,y) = exp(-y) sum_(n>=0) (n+1)(y-x)^n/[n!(n+2)!],  0<x<y.              (7)

This is exactly the already recorded 1993 density, equations (46)–(48), and is explicitly credited. It also shows X_1 independent of X_2-X_1. The old notes already express all positions as independent Poisson arrival times evaluated at random limiting pile-top ranks B(i). Our additional explicit formulation here removes the unspecified joint B-law: every joint probability is a positive fixed-size determinant sum with the explicit error (5). No claim is made that these classical ingredients or this reformulation are historically new.

## 7. Scope of the proposed answer

The candidate answers the literal request for a fairly explicit stationary distribution by an all-index, all-threshold joint formula and certified rational evaluation, not merely an existence construction or one-particle marginals. Whether this level of explicitness meets the source's descriptive aim is part of the requested independent source review. The mathematical assertions are the exact dynamics, uniqueness, formula (3), fixed-dimension transpose form, and certificate (5). No outreach or attribution of acceptance to the problem's proposer has occurred.
