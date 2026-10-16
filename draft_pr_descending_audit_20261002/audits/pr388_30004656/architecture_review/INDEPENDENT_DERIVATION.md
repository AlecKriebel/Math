# Independent reconstruction of Turns 4–5

Reconstruction completed before reading `review/ADVERSARIAL_REVIEW.md` or `review/independent_checks.py` in the frozen candidate. Inputs used: `TURN_4.md`, `TURN_5.md`, `ADDITIVE_CHAINING_CLARIFICATION.md`, and `RESULT.md`. The aim is falsification and verification of these restricted theorems, not validation of the unrestricted conjecture or historical novelty.

## Exact claims, assumptions and success criterion

Turn 4: positive integers n, d >= 2, 1 <= k <= d; iid uniform spherical inputs and iid independent fair labels; f=c+sum a_j ReLU(w_j.x), with rank W=k and arbitrary sample-dependent parameters. Outside a single failure event of probability at most 4 exp(-d)+2 exp(-n/8), every such f with total squared error <=n/256 has chord-metric sphere Lipschitz constant L >=sqrt(n/k)/4096.

Turn 5: integers d >=2 and n >=8d with the same sample law. Outside a single failure event of probability at most 2 exp(-n/32)+2 exp(-d)+2 exp(-6d), simultaneously for every positive integer k and every symmetric A of rank <=k, every f=x^T A x+b.x+c of squared error <=n/256 has L >=sqrt(n/k)/8192. Quadratic-core realizations of the specified fixed globally 2-Lipschitz activation inherit this conclusion. Units leaving that core do not.

Success requires checking all deterministic implications, uniform conditional probability bounds, infinite-index reduction, and boundary cases. Finite controls supplement those proofs; they are not probability-theorem certification.

## Sphere moments reconstructed without a concentration citation

For fixed v and X uniform on S^{d-1}, rotation reduces v.X to ||v|| X_1. Writing a standard Gaussian vector as R X gives independence of R and X, E G_1^{2m}=(2m-1)!!, and E R^{2m}=d(d+2)...(d+2m-2). Thus

    E(v.X)^{2m}=||v||^{2m}(2m-1)!!/[d(d+2)...(d+2m-2)]
                  <=||v||^{2m}(2m-1)!!/d^m.

Odd moments vanish. The identity works for all integer d>=2 and m>=0. It proves E exp(t v.X)<=exp(t^2||v||^2/(2d)), since the power series is absolutely convergent for bounded v.X.

## Turn 4 deterministic mechanism

Full row rank makes W:R^d -> R^k onto. Each orthant in R^k therefore has a nonempty open preimage. In particular there is a unit u_empty with every w_j.u_empty<0, hence h(u_empty)=0 for h=f-c. On the sphere |h(u)|<=2L. This point is allowed to depend on the eventual network because this entire step is deterministic.

For r>=s>=0 and unit u,v, positive homogeneity gives

    |h(ru)-h(sv)|<=sL||u-v||+2L(r-s).
    ||ru-sv||^2=(r-s)^2+rs||u-v||^2.

Each of the two terms is dominated by the ambient distance times its coefficient, so the global Lipschitz constant G of h is at most 3L. The formula includes the origin by continuity. Within the open cone corresponding to a subset A, the gradient is g_A=sum_{j in A} v_j, where v_j=a_j w_j, so ||g_A||<=G. For every Rademacher sign vector eps,

    ||sum eps_j v_j||=||g_A-g_{A^c}||<=2G.

Averaging its square gives sum ||v_j||^2<=4G^2<=36L^2. No inverse norm or conditioning of W has been used.

## Turn 4 independent probability reconstruction

Fix the entire label vector and z_i=y_i-bar y. Then sum z_i=0 and sum z_i^2=n(1-bar y^2)<=n. Let P_u(X)=ReLU(u.X) and H=P_u-P_v with ||u||=||v||=1. By rotation EP_u=EP_v, hence EH=0, and |H|<=|(u-v).X|. If H' is an independent copy, conditional Jensen gives E exp(tH)<=E exp(t(H-H')). The difference is symmetric, with

    E|H-H'|^{2m}<=2^{2m} E|H|^{2m}.

The even exponential series therefore bounds its mgf by exp(2t^2||u-v||^2/d). For the atom itself apply Jensen directly to P_u-EP_u and P_u-P_u'; the same argument uses |P_u|<=|u.X| and gives exp(2t^2/d). One need not incorrectly compare the centered atom's absolute moments directly with spherical moments.

Independence after conditioning on labels and sum z_i^2<=n imply, for Z(u)=sum z_i P_u(X_i),

    P(|Z(u)-Z(v)|>t | y)<=2 exp[-dt^2/(8n||u-v||^2)],
    P(|Z(u)|>t | y)<=2 exp[-dt^2/(8n)].

The deterministic mean term in the second bound cancels exactly.

Take a deterministic base e_1, and deterministic radius 2^{-j} sphere nets S_j with |S_j|<=(1+2^{j+1})^d<=2^{d(j+2)}. For each u choose nearest approximants pi_j(u) using a deterministic tie rule. With pi_0(u)=e_1, successive links have length <=4*2^{-j}. The union bound is only over the deterministic set of pairs at that distance (all pairs that may occur); its size is bounded by |S_j||S_{j-1}|<=2^{d(2j+3)}. Pairs at larger distance are not assigned the short-link tail bound.

At level j set t_j=32 sqrt(n/d) 2^{-j} sqrt(d(j+2)+v+j). The tail exponent for each short link is at least 8[d(j+2)+v+j]. Including its cardinality gives failure <=2 exp(-v-j). Summing over all j>=1 costs <2 exp(-v). At the base, threshold 8 sqrt(nv/d) fails with probability <=2 exp(-8v). Countable subadditivity, without independence between levels, leaves total failure <=4 exp(-v).

The process is continuous for every finite sample. Thus Z(pi_j(u))->Z(u) for every u. All increments are controlled on one event, so telescoping bounds all u simultaneously; no uniform convergence assumption on chosen pi_j is needed. The absolutely convergent threshold sum bounds all paths. With v=d,

    8 sqrt(n)+sum t_j
    <=8 sqrt(n)+32 sqrt(n/d)[4 sqrt(d)+sqrt(d)+2]
    <=232 sqrt(n)<256 sqrt(n).

Using sqrt(j+2)<=j+2 and sqrt(j)<=j makes the deliberately loose constants valid. Continuous processes on the compact sphere have measurable suprema through any fixed countable dense set.

Hoeffding gives |bar y|<=1/2 except with probability 2 exp(-n/8). On that event the fitting correlation satisfies

    sum z_i f(X_i)=n(1-bar y^2)+sum z_i e_i
                 >=3n/4-sqrt(n)*sqrt(n/256)>=n/2.

The constant c cancels. Writing b_j=a_j||w_j|| gives ||b||_2<=6L, and the same uniform atomic event yields n/2<=6L sqrt(k)*256 sqrt(n), hence L>=sqrt(n/k)/3072. This implies the announced 1/4096. The network's dependence on the entire labeled sample is harmless because both probability events precede any selection of its parameters.

## Turn 5 deterministic mechanism

For symmetric A write a_min<=a_max and s=a_max-a_min. Subtract mI, m=(a_max+a_min)/2. For sphere points,

    |x^T A x-y^T A y|
      =|(x+y)^T(A-mI)(x-y)|<=s||x-y||.

In an extreme-eigenvector great circle, q(cos(theta)u_min+sin(theta)u_max) has derivative s at theta=pi/4. Chord/arc distance tends to one. Thus the exact chord-metric Lipschitz constant is s, including scalar A where it is zero.

Even and odd antipodal projections (f(x)+f(-x))/2 and (f(x)-f(-x))/2 contract the sphere Lipschitz seminorm, so s<=L and ||b||<=L. If rank A<d there is a zero eigenvalue and ||A||_op<=s<=L, whence ||A||_*<=rank(A)L. At any rank, ||A-mI||_*<=dL/2. This shift may increase rank, which is why it is used only in the k>=d branch and with a trace-zero pairing.

## Turn 5 conditional selection and concentration

Hoeffding for label sums at threshold n/4 shows that both label counts are >=3n/8 except with probability 2 exp(-n/32). This real-valued count threshold handles all odd/even n without rounding assumptions. Conditional on all labels, take the first m points of each sign with m the minimum count. Then N=2m is even, N>=3n/4>=6d, and the selected X_i remain mutually independent with the original distribution. The selection depends only on labels, not input geometry or network errors.

Balanced signs give trace Omega=0 for Omega=sum y_i X_i X_i^T. For a fixed unit u let Q=d(u.X)^2. Then EQ=1 and E Q^h<=2^h h!. For h>=2,

    E|Q-1|^h<=2^{h-1}(E Q^h+1)<=4^h h!.

Absolute convergence and centering give, for |lambda|<=1/8,

    E exp(lambda(Q-1))
      <=1+sum_{h>=2}(4|lambda|)^h<=exp(32 lambda^2).

This remains true after multiplication by any fixed sign. With balancing, d u^T Omega u=sum y_i(Q_i-1). Choosing lambda=dt/(64N) when dt<=4N gives exponent -d^2t^2/(128N). Choosing lambda=1/16 when dt>=4N gives exponent at most -dt/32. Both imply

    P(|u^T Omega u|>t | labels)
      <=2 exp[-min(d^2t^2/(128N),dt/32)].

For t=128(sqrt(N/d)+1), the linear exponent is >=4d, and the quadratic exponent is >=128d. A deterministic 1/4-net of size <=9^d has the standard symmetric quadratic-form estimate ||Omega||<=2 max_net |u^T Omega u|: approximate a maximizing eigenvector and bound the two error bilinear forms by 2*(1/4)||Omega||. Thus failure <=2 exp[-(4-log 9)d]<=2 exp(-d) and ||Omega||<=512 sqrt(N/d), since N>=d.

The spherical mgf at the start gives for V=sum y_i X_i the tail P(|u.V|>t)<=2 exp[-dt^2/(2N)]. A deterministic 1/2-net of size <=5^d controls ||V|| by twice the maximum. Taking t=4 sqrt(N) gives failure <=2 exp[-(8-log 5)d]<=2 exp(-6d), and ||V||<=8 sqrt(N). All constants are uniform over balanced sign sequences and selected N; no union over label realizations is required.

## Turn 5 interpolation and exhaustive rank split

Full-sample squared error <=n/256 implies on the selected sample

    sum y_i f(X_i)>=N-sqrt(Nn)/16>=N/2,

because N/n>=3/4. Balancing cancels c, leaving tr(A Omega)+b.V. At least one term has absolute value >=N/4, even if the terms have opposite signs.

The linear branch gives L>=sqrt(N)/32. If k<d, the quadratic branch gives L>=sqrt(Nd)/(2048k)>=sqrt(N/k)/2048. If k>=d, trace cancellation and the shifted nuclear norm give L>=sqrt(N/d)/1024>=sqrt(N/k)/1024. Each implies L>=sqrt(n/k)/8192 using N>=3n/4. These branches cover k=d exactly, k>d, zero A, full-rank A and all permitted linear terms.

## Falsification attempts and boundary controls

* Repeated rows with opposite huge output coefficients give f=0 but unbounded coefficient energy. This falsifies extension of the Turn 4 energy lemma to dependent rows and confirms the stated restriction is essential.
* Radial scalar matrices A=M I give constant q on the sphere while ||A||_op=|M|. This falsifies an operator-norm interpretation and confirms the trace-zero scalar shift in Turn 5 is necessary.
* The input selection must use labels only. Choosing points according to their geometry or residuals would destroy the conditional iid argument; the candidate uses the first m of each sign and is valid.
* k=1,d=2; k=d; k>d; n=8d and odd n above it are covered. Turn 4 imposes no n>=d restriction. For tiny n its stated success lower bound can be negative and is consequently vacuous, not false. n is naturally a positive integer; n=0 would make empirical squared error undefined and is outside the claim.
* All-equal labels lie outside the useful label event and correctly admit zero-Lipschitz fits. No claim is being made on that failure event.
* Constants remain valid for d=2. Every spherical even moment is an upper bound derived from the exact identity; it does not assume d is large.
* Large output constants, large weights, nearly dependent but full-rank rows, arbitrary quadratic biases and adaptive coefficients do not enter the probability bounds.
* The global-Lipschitz quadratic-core realization chooses R_j>=max(1,||w_j||+|beta_j|), so |(w_j.x+beta_j)/R_j|<=1 on every sphere point, including equality. Multiplying a_j by R_j^2 exactly restores the original quadratic. No off-sphere assertion is made.

Provisional conclusion before consulting the prior review: both restricted theorems are mathematically supported as stated with the mandatory additive clarification. No proof of the broad conjecture follows, and no historical novelty assessment was performed here.
