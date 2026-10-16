# PR 372: root universal proof reconstruction before executable evidence

The original target is Aldous's 2012 Open Problem 34, renumbered Open Problem 8 in the 2014 published paper: for independent uniform unit-disc endpoints U_i, independent of an ordinary planar SIRSN, is the expected value of M = sup_i len R(0,U_i) finite? Additional sufficient assumptions are part of the question, but a sufficient assumption alone does not establish the assertion under the ordinary axioms. The frozen submission has five substantive turns and is being evaluated as an unsolved partial result.

This document follows the immutable ROOT_SOURCE_FIRST_BASELINE.md. All five TURN mathematical texts were read in full before any submitted executable, verification output, old referee report, or final-result summary. The additional original-source passages read after TURN 1 exposed its binary-hierarchy dependency were Aldous (2014), Proposition 3.1, the plane extension in section 3.6, all of section 3.7, Proposition 5.1, Lemma 6.2, Proposition 6.3 and (6.4), and Kahn Remark 5.1. These passages confirm the actual hypotheses and credits. They do not certify present-day novelty or universal resolution.

## 1. Uniform Poisson-model envelope

Let gamma>d>=2 be the marked Poisson-line exponent, and fix a unit ball. Kahn's Theorem 3.1 bounds a common random metric diameter tau: deterministic T_n=C(n+1)^(1/(gamma-1)) satisfy P(tau>T_n)<=2^(-n-1). This is a common environment envelope, rather than separate bounds for each endpoint. All origin-to-endpoint geodesics in the ball have travel time at most tau. The theorem's compact-set hypothesis and constants apply to that ball.

If any such path has Euclidean length greater than r and time at most T, its initial arclength-r portion stays inside the radius-r Euclidean ball. If every marked line meeting that ball had speed less than r/T, traversal time for that portion would exceed T. Therefore its fastest available speed V_r is at least r/T. This implication needs length, not a path's radial escape; backtracking does not evade it. A countable family with supremum greater than r has an actual witness path greater than r.

For r_j=2^j r_0, j=0,...,m, simultaneous required speeds v_j=r_j/T imply a nested sequence of record maxima. Partition the Poisson lines by the first radius layer they hit. Their marks in distinct layers are independent. For a pattern 0=l_0<l_1<...<l_k<=m and l_(k+1)=m+1, each preceding record must attain the threshold at the last radius before the next record. The Poisson mean bound for layer l_i and threshold v_(l_(i+1)-1) is at most

    c r_(l_i)^(d-1) v_(l_(i+1)-1)^(1-gamma)
      = a 2^((d-gamma)l_i-(gamma-1)(l_(i+1)-l_i)),
    a = 2^(gamma-1)c r_0^(d-gamma)T^(gamma-1).

Since d-gamma<0, dropping the first exponent bounds the product for that pattern by a^(k+1)2^(-(gamma-1)(m+1)). There are binomial(m,k) patterns. Summing gives

    P(all required speeds) <= 2^(-(gamma-1)(m+1)) a(1+a)^m
                           <= [2^(-(gamma-1))(1+a)]^(m+1).

This is an unconditional probability of a Poisson event. The appropriate route implication is

    {M>r_m, tau<=T} subset {all required speeds}.

No assertion about the Poisson law conditional on tau<=T is used. This correctly repairs the conditional-probability display in Kahn's printed argument. T=sum L/v and a speed-times-time length bound, rather than the source's two inconsistent printed products/quotients, are the quantities actually used.

For 0<kappa<gamma-1 choose a=2^(gamma-1-kappa)-1, r_0 proportional to T_n^((gamma-1)/(gamma-d)), and m=floor((n+1)/kappa). Then r_m is at most b_n=C'2^((n+1)/kappa)(n+1)^(1/(gamma-d)); the speed failure probability is at most 2^(-n-1). Adding P(tau>T_n) gives P(M>b_n)<=2^(-n). Decomposing M into the layers [b_n,b_(n+1)] shows that its q-th moment is bounded by a constant plus the convergent series sum_n 2^(-n)b_(n+1)^q for every q<kappa. Choosing kappa between q and gamma-1 proves every q<gamma-1. In the planar construction gamma>2, so q=1 is available. The estimate is uniform over all countably sampled endpoints, with no endpoint union bound and no assertion requiring an uncountable jointly measurable route version.

The source's binary-hierarchy example is a separate credited sufficient mechanism. Aldous Proposition 3.1 gives lattice stretch K_gamma in the l1 norm; the plane extension preserves this upper length bound, and section 3.7 explicitly gives len R_0(x,y)<=sqrt(2)K_gamma|x-y|, unchanged by the translations, rotation and random scalar dilation used to obtain R. Thus for a fixed root and countably many independent unit-disc endpoints the maximum is at most sqrt(2)K_gamma almost surely. The exceptional zero-area set in the intermediate plane construction is removed for prescribed pairs by its randomized translation; countable sampled pairs suffice. Neither example proves the ordinary-axiom assertion for other SIRSNs or is claimed as historically novel.

## 2. FDD increment criterion and its critical counter-control

Assume consistent measurable finite-location laws for F(z)=len R(0,z), F(0)=0, on Q=[-1,1]^2, and an additional bound

    E|F(u)-F(v)|^p <= C|u-v|^(alpha p),
    p>=1, alpha>2/p.

Use dyadic grids of spacing h_n=2^(-n), with at most 9*4^n vertices, and a rounded parent at level n-1 whose distance is at most sqrt(2)h_n. At level zero use 0 as the parent. Let A_n be the largest absolute parent increment. The elementary maximum-to-sum inequality gives

    ||A_n||_p <= 9^(1/p)2^(alpha/2)C^(1/p)2^(-n(alpha-2/p)) = B rho^n.

The sum H=sum_n A_n exists in Lp, by Minkowski and monotone convergence, with ||H||_p<=B/(1-rho). Every grid value is dominated by H by telescoping its ancestor chain. For an independent endpoint U and its rounded grid approximation g_n(U), integrating the measurable finite-location kernels gives E|F(U)-F(g_n(U))|^p<=C2^(alpha p/2)2^(-n alpha p). Markov and Borel-Cantelli, first for rational positive error thresholds and then for each of countably many endpoints, give convergence to the actual sampled route values. Hence M<=H and the claimed Lp bound holds. A consistent countable extension, rather than a continuum continuity assumption, is sufficient.

If route lengths additionally satisfy the metric triangle inequality in every finite configuration, then |F(u)-F(v)|<=len R(u,v). Invariance and E D^p<infinity give the increment hypothesis with alpha=1. This is a substantive extra condition: the source chooses minimum cost/time routes, whose Euclidean lengths need not satisfy the triangle inequality. The criterion requires p>2 in this application. More generally an increment exponent alpha>1 on a connected deterministic domain forces fixed-location values to be almost surely constant by partitioning a segment and using Minkowski. Thus such a hypothesis is extremely restrictive for a nontrivial SIRSN, but this does not invalidate the stated sufficient implication.

The critical counter-control is only a scalar field. On the unit flat torus take g(x)=log log(1/|x|) for 0<|x|<exp(-1), zero outside, with any finite assignment at the isolated center. For uniform Z, P(g(Z)>t)=pi exp(-2 exp t), so all positive fixed-point moments exist. Its squared gradient integral is 2pi integral_0^(exp(-1)) dr/[r log(1/r)^2]=2pi. Truncations at height N, assigned N at the center, are Lipschitz periodic functions. The line integral, Cauchy-Schwarz and translation invariance give integral |g_N(x+h)-g_N(x)|^2 dx<=2pi|h|^2; L2 convergence passes this bound to g. The radial cutoff is continuous at exp(-1) and lies inside the fundamental square, so no boundary discontinuity was dropped.

Set F(u)=|u|+|g(u-Z)-g(-Z)|. Then F(0)=0, F(u)>=|u|, all fixed-point moments are finite, and E|F(u)-F(v)|^2<=(2+4pi)|u-v|^2. Almost surely a representative of Z is strictly inside the unit disc and g(-Z)<infinity. Each arbitrarily high level has a punctured positive-area neighborhood there. An independent infinite iid disc sample visits each such neighborhood almost surely, so its maximum is infinite. This demonstrates that the critical p=2, alpha=1 scalar estimate, even with all individual moments, is insufficient. It is not a SIRSN, does not satisfy the additional length-metric hypothesis, and does not disprove the source problem.

## 3. Tail frequencies, sufficient visibility and pair obstruction

Measurable SIRSN FDDs and iid independent endpoints make the sampled lengths exchangeable. For I_i=1{L_i>t}, write a=E I_1 and b=E I_1 I_2. Exact exchangeability gives E Q_n^2=a/n+(1-1/n)b and E(Q_n-Q_m)^2=(a-b)(1/n-1/m), where Q_n is the empirical frequency and m>=n. Thus Q_n converges in L2 with squared error (a-b)/n. Along square indices Chebyshev is summable; squeezing the nondecreasing numerator between consecutive square indices proves almost-sure convergence along the whole sequence.

For a finite-permutation invariant event B, E[I_1 1_B]=E[Q_n 1_B], hence E[I_1 1_B]=E[Q 1_B]. Taking B={Q=0} proves all indicators vanish on that event, almost surely. Conversely all indicators zero force Q=0. On the common rational-t event construct the nonincreasing right-continuous version Q(t)=sup_(r>t rational)Q(r). Equal expectations identify it with the empirical L2 limit at each fixed t. The rational union identity {M>t}=union_(r>t rational){M>r} then establishes {M>t}={Q(t)>0} simultaneously for all real t. Joint measurability follows from this countable construction. E Q(t)=a(t), E Q(t)^2=b(t), and Tonelli yields E M=integral P(Q(t)>0)dt. This needs neither de Finetti's theorem nor a continuum route field.

If Q(t)=0 or Q(t)>=h(t)>0 almost surely for almost every t, P(M>t)<=a(t)/h(t). For h=c(1+t)^(-alpha), integration of the sampled marginal tail gives E M<=E[((1+L_1)^(alpha+1)-1)]/[c(alpha+1)]. Invariance gives L_1 in law R D with independent radial R of density 2r, and E L_1^s=2 E D^s/(s+2). These hypotheses are additional. A hard positive lower mass near a finite maximum is particularly restrictive, since continuous conditional endpoint lengths can have positive tail masses tending to zero there.

For an invariant V>=1 with Q(t)>0 implying Q(t)>=V^(-1)(1+t)^(-alpha), the invariant multiplier identity, proved by truncation, gives E[V Q(t)]=E[V 1{L_1>t}]. Tonelli yields the weighted integral bound in TURN 3. Holder applies to its joint law, without independence, and finite E V^r and E D^((alpha+1)r') suffice.

For q>0, Holder on {Q>0} gives P(Q>0)<=a^(q/(q+1))(E[Q^(-q)1{Q>0}])^(1/(q+1)). If the negative-frequency moment is at most C(1+t)^beta and E D^s is finite, Markov produces an integrable power when sq>beta+q+1. The probability bound one controls the initial interval. Conversely Cauchy-Schwarz gives P(M>t)>=a^2/b, with zero assigned to 0/0; b>=a^2 rules out a positive numerator over zero. The second-moment calculation for finite counts gives the same limiting inequality. Divergence of integral a^2/b therefore obstructs integrability in an actual sampled SIRSN law, but applying it to an abstract sequence supplies no geometric counterexample.

The submitted exchangeable scalar example chooses P(J=j)=2^(-j), and, conditionally iid, L_i=2^j with probability 2^(-j^2) and 1 otherwise. Every marginal positive moment is finite, since its summand is bounded by 2^(-j^2+(s-1)j). Every conditional infinite sample hits 2^j, so M=2^J is finite almost surely but E M=infinity, with E M^q finite exactly for q<1. This correctly distinguishes pathwise finite maxima from finite mean and is explicitly not an invariant compatible planar network.

## 4. Ordinary-axiom geometry and precise remaining moments

Credit Aldous's common major-road extension, Proposition 6.3 and planted-origin identity (6.4). Independent successive arrivals in the unit disc have iid uniform locations; appending the independent outside space-time Poisson process realizes the entire countable endpoint family. For countably many needed r, all inclusions into E_r hold on a common probability-one event. Its intensity is p/r by (6.2). These source results are premises; the submission does not claim to supply a full new formalization of the source's outline measure-theoretic proof.

For endpoints in the unit disc, circle radius 3 is more than unit distance from both endpoints. Its intersection C with E_1 has E|C|<=12p by the source's circle intersection formula (circle length 6pi times 2p/pi). Thus C is finite almost surely. Every open exterior excursion of an injective compact route has two distinct boundary endpoints a,b in C; coincident endpoints would give a closed nontrivial subpath. Compatibility makes two excursion arcs with the same unordered pair coincide. There are at most binomial(|C|,2) such arcs. Each existing arc has a finite-length compact witness among the countably many routes. Their finite union has finite length and finite maximal radius. This proves common random confinement and finite exterior total length almost surely, but a finite number of possibly heavily biased arcs can still have infinite expected length. Crossing-count integrability alone is insufficient.

For annular endpoints 1/2<|V_i|<1 and eta<=1/4, at x in shell eta 2^(-j-1)<|x|<=eta 2^(-j), every route point is at least eta from V_i and beyond the shell's inner radius from 0. Hence the entire rooted union there lies in E_(eta 2^(-j-1)). Its expected length is at most (3pi/2)p eta 2^(-j); summing proves E len(H_eta)<=3pi p eta. Fixed circle boundaries have zero expected edge length under the intensity measure, and the origin contributes none.

Inside the radius-3 ball, outside the two endpoint eta-balls, every point lies in E_eta. Thus for the annular sample

    M_A <= len(H_eta)+len(E_eta intersect B(0,3))+J_eta+O,

where J_eta is the maximum destination-neighborhood length and O the maximum exterior route length. The first two terms have expected sum at most 3pi p eta+9pi p/eta. Conversely J_eta<=M_A and O<=M_A. Therefore E M_A is finite exactly when both E J_eta and E O are finite, for any fixed allowed eta. This is an exact localization, not a proof of those two missing estimates.

Dyadic annuli 2^(-k)A partition the unit disc up to null boundaries. Each gets infinitely many iid sample points and its thinned subsequence has the correct independent uniform shell law. Scale invariance gives shell maximum M_k in law 2^(-k)M_A. No independence among shell maxima is needed: M_disc=sup_k M_k<=sum_k M_k gives E M_disc<=2E M_A, and the outer subsequence gives the reverse finiteness implication. The general gap is therefore precisely the terminal and exterior first moments, not the fixed-root union or bounded middle.

## 5. Genuine mixture closure and affine no-go theorem

For genuine laws P_j, positive weights summing to one, and finite weighted Delta and p, sampling the complete route law after choosing J preserves consistency, measurable kernels, compatible feasible routes and all similarity invariances. Major-road intensities average at finite sampling intensity, and monotone convergence preserves the infinite-intensity limit. Aldous Lemma 6.2 supplies ell<=2p, so no separate sampled-network finite-intensity assumption was silently omitted. Delta is strictly greater than one for each source SIRSN, and remains so after mixing; the weaker b=Delta+p>=1 suffices for normalization. Conditioning also gives H=sum w_j H_j, with infinity allowed. No ergodicity premise exists in the ordinary class.

If all H_j are finite but H_j/b_j are unbounded, choose H_j/b_j>=4^j and Z=sum 2^(-j)/b_j, with 0<Z<=1. Weights w_j=2^(-j)/(Zb_j) have weighted b equal to 1/Z, but weighted H at least Z^(-1)sum 2^j=infinity. Thus universal finiteness in the ordinary mixture-closed class is equivalent to a universal linear bound H<=C(Delta+p). The needed genuine unbounded-ratio laws have not been constructed; numerical triples and the scalar example do not establish their existence.

For a fixed isotropic deterministic-stretch law P_0, let A=diag(lambda,1), lambda>=1, and randomize the exterior rotation. Affine maps preserve route geometry, consistency and translation/scale invariance, and exterior rotation restores rotation invariance. Route stretch is at most C_0 lambda, so H<=C_0 lambda. A transformed major-road element at distance at least r from both endpoints has an original distance at least r/||A||. Transformed Poisson intensity ranges over all positive values, so its common major-road network is contained in A E^0_(r/||A||). Expected length changes by at most ||A||/det A per unit area; p'=p'(1)<=||A||^2 p_0/det A=lambda p_0. This constructs genuine finite-parameter SIRSNs.

Let Gamma be the base route to (1,0), and c_0=E TV_y(Gamma)>0. Zero transverse variation forces the continuous injective path to be the straight segment. Source Proposition 5.1(a) excludes such sampled Poisson routes; invariance in displacement and scale makes the straightness probability the same for each fixed distinct pair. Integrating over independent Poisson endpoints then forces that probability to zero. Thus a nondegenerate base has positive c_0, finite and at most Delta_0; the submission also keeps positivity explicit in the argument.

For a unit direction u write w=A^(-1)u=d(cos phi,sin phi). Projecting the rotated base tangent and using the reverse triangle inequality gives expected original horizontal variation at least d(|sin phi|c_0-|cos phi|Delta_0). On |u_y|>=1/2, an angular event of probability 2/3, d>=1/2 and |cos phi|<=2/lambda. For lambda>=8Delta_0/c_0 these inequalities give |sin phi|>=3/4 and horizontal variation at least c_0/4. Applying A multiplies it by lambda; averaging gives Delta(P_lambda)>=lambda c_0/6. For smaller lambda use Delta>=1. Hence

    H(P_lambda)<=K Delta(P_lambda),
    K=8 C_0 Delta_0/c_0,

uniformly for the fixed base and all lambda>=1. Conditioning extends the same inequality to any countable mixture with finite Delta. This rules out heavy global anisotropy of that one fixed base as a counterexample mechanism. It does not rule out varying bases with degenerating c_0 or local distortions; no converse major-road bound is required.

## Root mathematical disposition before code and receipts

All five universal implications and the explicitly limited scalar counter-controls survive this independent proof reconstruction. No mandatory mathematical repair is identified at this stage. Additional sufficient hypotheses remain additional, almost-sure finiteness remains distinct from finite mean, source-model corollaries are credited, and none of the scalar examples is claimed to be a SIRSN. The strongest unconditional progress is geometric localization and mixture equivalence; the missing ordinary-axiom expectation estimate or genuine counterexample remains unproved. The provisional disposition is acceptance only as unsolved 5/5, subject to full executable/provenance/source-summary/final-package and fresh-head adversarial checks. Overall discovery completion estimate: 0%; audit estimate: 35%.
