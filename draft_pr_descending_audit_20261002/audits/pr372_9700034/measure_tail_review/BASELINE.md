# Independent source-first probability baseline

## Scope and sequencing

Prepared before opening any candidate TURN, candidate program, receipt, previous review, parent, or sibling finding. Sources were freshly fetched exclusively at SOURCE_MANIFEST.json locators. All four bytes/hashes match the manifest. Raw sources, extracts and renders remain under ignored private/. No external communications or Git/service mutations were made.

## Exact target and source correspondence

For a SIRSN R on the plane and U_1,U_2,... iid normalized Lebesgue on the closed unit disk B, independent of R, define L_i = len R(0,U_i), M_n=max_{i<=n}L_i and M_infty=sup_{i>=1}L_i. The source asks which additional assumptions, if any, imply E M_infty < infinity. The quantifier of interest is: for every SIRSN satisfying those explicitly stated assumptions, the joint network/destination expectation is finite. The desired constant may depend on the network law. An example-specific theorem answers only the corresponding model subclass.

The exact question is Aldous long April 2012, Open Problem 34, PDF page 50; it is retained as Aldous published EJP 19 (2014), Open Problem 8, PDF page 38. Both displayed question pages were independently rendered and visually inspected. Numbering alone must not identify the published question as Open Problem 34. Source axioms include consistency and feasible compatible routes, similarity-invariant FDDs, measurable dependence of FDD kernels on destinations, finite E D_1, and finite truncated route-union intensity p(1). They do not assert that routes minimize their Euclidean lengths, nor that route length is a metric satisfying the triangle inequality. The source defines an explicit minimum-time binary example, but its general axioms do not impose any particular minimizing cost.

Kahn's Poisson line primary source is an example-specific SIRSN paper. Its Theorem 3.1 bounds a simultaneous minimum travel-time diameter of a Euclidean compact set, with stretched exponential tail. Its Theorem 5.1 is stated for Euclidean length of a single fixed-pair geodesic. Time diameter and Euclidean route length are distinct variables; neither the theorem title nor a bound on travel time alone proves E M_infty < infinity. The need for extra conversion/localization control is explicit.

## Universal consequences actually available before candidate inspection

Let m=E D_1<infinity. Rotation and scaling imply, for every fixed z, len R(0,z) has the law |z|D_1 (z=0 has length zero). FDD-kernel measurability and independence of U allow integration, giving

E L_1 = integral_B |z| m dz/pi = (2/3)m.

For any finite n, 0<=M_n<=sum_{i=1}^n L_i, so E M_n <=(2n/3)m. Monotone convergence gives E M_infty=lim_n E M_n, permitting infinity. A finite-n estimate depending on n is not enough; a uniform finite bound on E M_n is necessary and sufficient.

A slightly stronger universal baseline is E M_n/n ->0, without independence among lengths. For every t>0,

M_n <= t + sum_{i=1}^n L_i 1_{L_i>t}.

Take expectations, divide by n, let n go to infinity, then let t go to infinity using L_1 integrable. This still allows M_infty=infinity almost surely. Tail integration also gives

E M_n <= integral_0^infty min(1,n P(L_1>t)) dt.

If E D_1^p<infinity for p>=1, then E L_1^p=(2/(p+2))E D_1^p, and E M_n <= (n E L_1^p)^(1/p). This is a finite-n consequence only. Even all finite moments of the spatial distribution can coexist with an infinite essential supremum.

## Conditional sampling and the exact support-tail issue

For a jointly measurable nonnegative field f(omega,z)=len R_omega(0,z), define

q_omega(t)=mu{z in B:f(omega,z)>t},  S(omega)=esssup_{z with respect to mu} f(omega,z),

where mu is normalized Lebesgue. Conditional on omega, independent destinations imply

P(M_n>t | omega)=1-(1-q_omega(t))^n.

Hence P(M_infty>t)=P(q_omega(t)>0)=P(S>t), and

M_infty=S almost surely;  E M_infty = integral_0^infty P(q_omega(t)>0) dt = E S.

Proof: for every rational t, if q=0 all countably many draws miss the exceedance set; if q>0 the probability all draws miss is lim_n(1-q)^n=0. Intersect these events over rational t. Measurability of S follows from the positive-q events at rational t. Tonelli and monotone convergence require no prior integrability. These statements require either a jointly measurable realization or an explicitly justified directing random measure for the countably sampled exchangeable length sequence; measurable FDD kernels alone should not be casually relabeled as jointly measurable sample paths.

The sampled supremum is an essential spatial supremum, not automatically a pointwise supremum or supremum over a fixed dense set. Equality with the pointwise supremum follows, for example, if f is lower semicontinuous on B and mu has full support; strict exceedances then contain a relatively open set of positive measure. A joint measurable null spike f(omega,z)=Y(omega)1_{z=V(omega)} with V uniform is missed by all independent iid destinations, while its pointwise supremum is Y. Generic dense-grid convergence needs regularity and upper control: lower semicontinuity detects lower exceedances; continuous compact fields give dense sup convergence, but neither almost-sure finiteness nor mere continuity gives expectation integrability.

This conditional identity is exact but is a reformulation of the requested integrability, not an independent checkable SIRSN hypothesis unless the positivity-tail is controlled from additional geometric structure. Bounding E q(t)=P(L_1>t) controls average exceedance mass, not P(q(t)>0). An arbitrarily small positive mass is eventually sampled with probability one. Markov bounds on q with positive thresholds cannot in general be sent to threshold zero while preserving a useful estimate.

## Original controls and counterexamples (generic fields, not SIRSNs)

1. On B set f(z)=1-log|z| for z!=0 and f(0)=0. Under uniform mu, -log|U| has exponential tail exp(-2t). Thus every finite moment of f(U) exists (indeed E exp(lambda f(U))<infinity for lambda<2), but S=infinity and M_infty=infinity almost surely. This disproves any inference from finite moments of one sampled value to uniform countable maximum, absent structural assumptions.

2. Let X have P(X>t)=1/t for t>=1. Set f_X(z)=X 1_{0<|z|<X^(-1)} and f_X(0)=0. Then S=X and E S=infinity. Yet integral_B f_X dmu = X*X^(-2)=1/X, so E f_X(U)<=1. Each fixed z!=0 has f_X(z)<=1/|z|. Conditional tail mass equals X^(-2)1_{X>t}; its expectation is integrable over t, but its positivity probability has nonintegrable 1/t tail. All values are finite and the spatial supremum is finite almost surely: a.s. finiteness is insufficient.

3. Null spike above disproves pointwise-versus-essential equality. If destinations are allowed to depend on the network and avoid a positive-mass long-route set, the conditional formula fails. The explicit destination independence is necessary.

4. No generic scalar field is being asserted to realize compatible similarity-invariant feasible routes or finite p(1). A SIRSN counterexample must construct and check the entire network, including all finite-dimensional route compatibility and the truncated union intensity. These controls identify logical insufficiencies only.

## What would constitute additional usable control

An integrable random envelope H with f<=H mu-a.e. implies the goal. For a Euclidean-length minimizing route metric, an integrable random compact diameter would suffice, but the SIRSN axioms do not supply that metric property. For a time-minimizing line model, a simultaneous time bound T plus geometric localization and a speed/length estimate with a joint integrability proof could supply a model-specific envelope. A deterministic finite geometric-scale budget times an integrable random coefficient also suffices. Conversely, merely postulating E S<infinity or the exact support-tail integral is tautological as an answer to the geometric question.

## Exact remaining target gap at this seal

The universal axioms yield finite individual and finite-n means, with sublinear expected maximum growth. They do not yet give a uniform-in-n first-moment bound. The central remaining task is a non-tautological geometric mechanism deriving an integrable essential spatial envelope from a genuine SIRSN subclass or its axioms. No SIRSN counterexample or general solution is claimed.
