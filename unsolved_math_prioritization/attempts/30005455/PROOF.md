# Finite WARM: sharp forest threshold and a bounded whisker improvement

Problem 30005455 / OWR-12697708-008. Mathematical research note; independent audit supplied separately. The combined two-clause problem is **not fully resolved**: the forest clause is proved below; the equal-rate whisker clause is proved here only for alpha >= 17/4. No novelty or priority claim is made.

## 1. Model, normalization, and the stochastic bridge

Let G=(V,E) be a finite simple undirected loopless graph, with a positive firing rate lambda_v at each non-isolated vertex, unit initial tallies, and reinforcement W(n)=n^alpha, alpha>1. At a firing at v, choose an incident edge with probability proportional to its current tally to the power alpha. We use continuous-time limiting weights a_e=lim N_t(e)/t, not proportions summing to one. Their sum is sum_v lambda_v. Isolated vertices have no effect and may be discarded. If E is empty, the support conclusions are immediate; henceforth assume E is nonempty, so the total rate after discarding isolated vertices is positive.

For comparison with probability-normalized formulations, put Lambda=sum_v lambda_v, p_v=lambda_v/Lambda, and x=a/Lambda. Then F_lambda(a)=Lambda F_p(a/Lambda), so their Jacobians are identical and the change preserves stability and support.

Write S_v(a)=sum_{e incident to v} a_e^alpha. The mean vector field is

F_e(a)=-a_e+sum_{v incident to e} lambda_v a_e^alpha/S_v(a).

The published Hirsch–Holmes–Kleptsyn paper, Nonlinearity 36 (2023), 3013–3042, Theorem 1, proves almost-sure convergence to an equilibrium with no positive Jacobian eigenvalue, and positive-probability convergence to each linearly stable equilibrium. Its Proposition 1 identifies edges reinforced infinitely often with edges of positive asymptotic growth. These are imported published results, not proved anew here. The model in that paper starts every tally at one. Thus excluding linearly non-unstable equilibria of a support type excludes that stochastic support almost surely, and a strictly stable equilibrium supplies a positive-probability stochastic example from the prescribed initial state.

At a limit equilibrium every vertex with positive firing rate has an incident positive edge: the sum of incident tallies is at least the number of firings at that vertex, so the sum of the limiting incident weights is at least lambda_v. On the positive support H, S_v>0 and the vector field restricted to H is smooth. Positive eigenvalues of this support restriction are positive eigenvalues of the full Jacobian: for alpha>1 the rows corresponding to zero edges have derivative -1 on their own coordinate and zero derivatives in supported coordinates. The cross block in the other direction also vanishes, because derivatives of a zero edge's power are zero for alpha>1. Thus the full Jacobian is block diagonal with the support Jacobian and a negative identity block. In particular it is valid to do the following calculations on H. The retained support may have several components; all arguments are componentwise.

## 2. Hessian reduction

On a fully positive support define

L(a)=-sum_e a_e+(1/alpha) sum_v lambda_v log S_v(a).

Then F_e=a_e partial_e L. At an equilibrium a, grad L(a)=0, and DF(a)=diag(a) Hess L(a), similar to the real symmetric matrix diag(sqrt(a)) Hess L(a) diag(sqrt(a)). A positive Hessian direction therefore implies a strictly positive Jacobian eigenvalue, including if the equilibrium has critical directions.

Put y_e=a_e^alpha and define the same scalar function in these coordinates:

Phi(y)=-sum_e y_e^(1/alpha)+(1/alpha)sum_v lambda_v log(sum_{e incident to v} y_e).

At an equilibrium, changing from a to y gives a congruence of Hessians, since the gradient vanishes. Set

b_v=lambda_v/S_v, c_v=lambda_v/S_v^2, D_e=a_e^(1-2alpha).

The equilibrium identity, after division by a_e^alpha, is

a_e^(1-alpha)=b_u+b_v for e=uv.                                           (2.1)

For any real vector w on support edges, direct differentiation gives

alpha^2 Hess Phi(y)[w,w]
  =(alpha-1)sum_e D_e w_e^2-alpha sum_v c_v(sum_{e incident to v}w_e)^2.     (2.2)

Equivalently, in relative a-coordinates z_e=delta a_e/a_e, the Hessian is

Hess L(a)[delta a,delta a]
  =(alpha-1)sum_e a_e z_e^2-alpha sum_v lambda_v(sum_e q_{ev}z_e)^2,

where q_{ev}=a_e^alpha/S_v. In particular every non-linearly-unstable equilibrium satisfies the diagonal necessary condition

sum_{v incident to e} lambda_v q_{ev}^2 >= (1-1/alpha)a_e.                 (2.3)

All signs and scale factors are important here. The proof uses positive directions of an ascent Lyapunov function.

## 3. Cycle theorem, arbitrary positive rates

**Theorem A.** If the positive support of an equilibrium contains an even cycle, it is linearly unstable for every alpha>1. If it contains an odd cycle of length m, it is linearly unstable whenever

alpha > sec^2(pi/(2m)).                                                    (3.1)

Consequently, for every finite graph and every collection of positive rates, the stochastic surviving support is almost surely a forest for alpha>4/3.

**Proof.** Number the distinct edges of a simple cycle e_0,...,e_{m-1} cyclically; v_i meets e_{i-1} and e_i. Put A_i=a_{e_i}^alpha. From (2.1),

sum_{i=0}^{m-1} D_{e_i}
 =sum_{i=0}^{m-1} b_{v_i}(1/A_{i-1}+1/A_i).

Furthermore S_{v_i}>=A_{i-1}+A_i, so

c_{v_i}=b_{v_i}/S_{v_i}
 <= b_{v_i}/(A_{i-1}+A_i)
 <= (b_{v_i}/4)(1/A_{i-1}+1/A_i).

The last inequality is (A+B)^2>=4AB. Summing yields

4 sum_i c_{v_i} <= sum_i D_{e_i}.                                         (3.2)

This remains valid when there are chords, other cycles, or trees attached: their positive weights only enlarge the denominators S_v. Perturbations below are zero on all non-cycle edges.

If m is even, take w_{e_i}=(-1)^i. Every vertex sum in (2.2) vanishes, and the remaining positive diagonal term proves instability.

If m is odd, let theta=pi-pi/m. Since m theta=(m-1)pi is an integer multiple of 2pi, the real vectors

u_{e_i}=cos(i theta),  w_{e_i}=sin(i theta)

are well-defined cyclically. At each edge u_{e_i}^2+w_{e_i}^2=1. At each cycle vertex,

(u_{e_{i-1}}+u_{e_i})^2+(w_{e_{i-1}}+w_{e_i})^2
 =2+2cos(theta)=4sin^2(pi/(2m)).

Apply (2.2) to both vectors and add. By (3.2),

alpha^2[Hess Phi[u,u]+Hess Phi[w,w]]
 >= [(alpha-1)-alpha sin^2(pi/(2m))] sum_i D_{e_i}
 = [alpha cos^2(pi/(2m))-1] sum_i D_{e_i}.

Under (3.1) this is strictly positive. At least one of the two real perturbations is therefore a positive Hessian direction. For every odd m>=3, sec^2(pi/(2m))<=4/3. Every nonforest finite graph contains a cycle, proving the deterministic forest assertion. Apply the published finite-graph convergence theorem from Section 1 to obtain the stochastic assertion. QED.

**Sharp lower obstruction.** On the equal-rate triangle (lambda_v=1), a=(1,1,1) is an equilibrium. The Jacobian has diagonal alpha/2-1 and off-diagonal -alpha/4, hence eigenvalues -1 and 3alpha/4-1 (twice). It is linearly stable for every 1<alpha<4/3. The published positive-attainability clause implies positive probability of convergence to this equilibrium from unit initial tallies. All three edges then survive, and their component is neither a tree nor a whisker. Thus no universal bound alpha>alpha_0 with alpha_0<4/3 can imply either requested conclusion. This triangle obstruction is already in the cited literature; it is included as a checked sharpness control, not a new discovery.

At alpha=4/3 the two triangle eigenvalues are zero. Neither the strict-instability argument nor the published strict-stability attainment clause answers its stochastic behavior. This report makes no assertion at that endpoint.

## 4. Equal-rate whiskers for alpha >= 17/4

Here lambda_v=1. Common equal rates reduce to this normalization by time scaling. In a positive support, write q=q_{eu}, r=q_{ev}, so a_e=q+r and 0<q,r<=1; thus a_e<=2. Condition (2.3) becomes

q^2+r^2 >= (1-1/alpha)(q+r).                                              (4.1)

**Lemma B (least-weight edge).** For alpha>2, every positive edge at a non-linearly-unstable equilibrium has weight at least 1.

**Proof.** Select an edge of least positive weight in one component. If neither endpoint is a leaf of the support, each endpoint has another positive incident edge of at least the same weight. Hence q,r<=1/2 and q^2+r^2<= (q+r)/2, contradicting (4.1) because 1-1/alpha>1/2. The least-weight edge has a leaf endpoint; that endpoint always selects it, so its weight is at least 1. All other weights in the component are no smaller. QED. This is the least-weight leaf argument of Holmes–Kleptsyn, restated in the continuous-time normalization.

If e has no leaf endpoint and a=a_e<=3/2, Lemma B implies

q,r <= s_alpha(a):=a^alpha/(1+a^alpha).                                   (4.2)

Indeed each endpoint has a competitor of weight at least 1. As q+r=a, the maximal possible q^2+r^2 subject to (4.2) is attained at an extreme split. In particular, whenever the split is feasible,

(q^2+r^2)/a <= f(a,s_alpha(a)),
f(a,s):=[s^2+(a-s)^2]/a.                                                  (4.3)

Feasibility gives s_alpha(a)>=a/2. On s>=a/2, f(a,s) is nondecreasing in s. For 1<=a<=3/2, s_alpha(a) is nondecreasing in alpha.

### 4.1 Symbolic bound for 17/4 <= alpha <= 7

We first prove the elementary estimate

1/2 <= s_B(a)/a <= 2/3 whenever 3<=B<=7 and 1<=a<=3/2.                  (4.4)

For the lower bound, a^(B-1)(2-a)>=a^2(2-a)>=1: indeed

a^2(2-a)-1=(a-1)(1+a-a^2)>=0.

For the upper bound, s_B(a)/a<=s_7(a)/a=a^6/(1+a^7), and the polynomial

R(a)=2a^7-3a^6+2

is strictly positive for all a>=0. Its derivative is 2a^5(7a-9), so its minimum is at a=9/7, where

R(9/7)=2-3*9^6/7^7=52763/823543>0.

Now put z=s_B(a)/a. Since s_B'(a)>0, differentiation gives

d/da f(a,s_B(a))=1-2z^2+2(2z-1)s_B'(a)>=1-8/9=1/9>0.                 (4.5)

Thus f(a,s_B(a))<=f(3/2,s_B(3/2)). For A<=alpha<=B<=7 with A>=17/4, monotonicity in the second argument also gives

(q^2+r^2)/a<=f(a,s_alpha(a))<=f(a,s_B(a))<=f(3/2,s_B(3/2)).            (4.6)

It remains to make five scalar rational comparisons, which are all displayed here. If T>=(3/2)^B and S=T/(1+T), then the last expression is at most f(3/2,S). The following intervals cover [17/4,7]; each listed margin is exactly (1-1/A)-f(3/2,S), and is positive:

- [A,B]=[17/4,13/3]: take T=29/5 and S=29/34. Then f(3/2,S)=1325/1734, with margin 1/1734.
- [A,B]=[13/3,9/2]: take T=25/4 and S=25/29. Then f(3/2,S)=3869/5046, with margin 163/65598.
- [A,B]=[9/2,5]: take T=(3/2)^5=243/32 and S=243/275. Then f(3/2,S)=117039/151250, with margin 5399/1361250.
- [A,B]=[5,6]: take T=(3/2)^6=729/64 and S=729/793. Then f(3/2,S)=991335/1257698, with margin 74117/6288490.
- [A,B]=[6,7]: take T=(3/2)^7=2187/128 and S=2187/2315. Then f(3/2,S)=8580639/10718450, with margin 527104/16077675.

The two fractional-power upper bounds require no numerical logarithms or floating-point calculation:

(29/5)^3-(3/2)^13=504313/1024000>0,
(25/4)^2-(3/2)^9=317/512>0.

Positive powers preserve order, proving the desired bounds on T. Every other number in the five comparisons is a displayed rational obtained by substituting S in f(3/2,S)=(2/3)[S^2+(3/2-S)^2]. Consequently (4.6) is strictly smaller than 1-1/A<=1-1/alpha, contradicting (4.1), at every point of the closed interval [17/4,7]. No external coefficient table or generated certificate is required for this proof.

### 4.2 Analytic tail alpha >= 7

If 1<=a<=3/2, put r_0=a-1 in [0,1/2]. Without the competitor bound, q,r<=1 and q+r=a imply q^2+r^2<=1+r_0^2. Thus (4.1) implies

alpha r_0^2-(alpha-1)r_0+1>=0.                                          (4.7)

For alpha>=7 this quadratic is negative at r_0=1/2. Its smaller root is r_-(alpha). Consequently r_0<=r_-(alpha). Set C=3-sqrt(2). Substitution gives

alpha(C/alpha)^2-(alpha-1)(C/alpha)+1
 =1-C+(C^2+C)/alpha
 =-(C-1)(1-7/alpha)<=0,

using C^2+C=7(C-1). Hence r_0<=C/alpha. Therefore

a^alpha=(1+r_0)^alpha<=exp(alpha r_0)<=exp(C)<6<=alpha-1.                 (4.8)

For completeness, exp(C)<6 uses only elementary bounds. We have sqrt(2)>7/5, hence C<8/5. The exponential series has partial sum through degree four

sum_{k=0}^4 (8/5)^k/k! = 9067/1875.

For k>=5 the ratio of consecutive terms is at most 4/15. Therefore its entire tail from degree five is at most [(8/5)^5/5!]/(1-4/15)=4096/34375. The sum of these two rational upper bounds is 510973/103125<6. Thus exp(8/5)<6, as used above.

But (4.1) implies max(q,r)>=1-1/alpha. If e has no leaf endpoint, (4.2) and (4.8) instead give both q,r< (alpha-1)/alpha, a contradiction. This rules out every non-leaf edge of weight <=3/2 also for alpha>=7.

**Theorem C.** For equal firing rates and alpha>=17/4, the stochastic surviving support is almost surely a whisker forest.

**Proof.** Theorem A says its limiting support is a forest. Lemma B and Sections 4.1–4.2 say every edge not incident to a leaf has weight >3/2. Two such edges cannot meet at a vertex: for an incident edge e=uv of weight a_e>3/2, q_{ev}=a_e-q_{eu}>1/2, since q_{eu}<=1. Two adjacent edges would then receive probabilities summing to more than one at their common vertex. Thus the edges not incident to leaves form a matching. A tree of diameter at least four has two adjacent edges neither incident to a leaf (the middle two edges of a length-four path). This is impossible. Each component has diameter at most three. Apply the published convergence theorem. QED.

## 5. Exact remaining gap and limits

Theorem A proves the entire requested unequal-rate forest conclusion for every alpha>4/3, and the equal-rate triangle gives its sharp lower obstruction in the prescribed stochastic model. Theorem C improves the universal equal-rate whisker bound from >25 to >=17/4. It does **not** establish the requested whisker conclusion for 4/3<alpha<17/4. This unresolved interval includes critical equilibria; stable equilibria found by simulations alone cannot settle an almost-sure classification. No counterexample above 4/3 has been established, and no claim about the excluded equality endpoint is made.

A precise sufficient missing lemma would be: for every equal-rate fully supported equilibrium on a finite tree of diameter at least four, and every alpha>4/3, the symmetric Jacobian representative has a positive eigenvalue. This is stronger than merely testing a symmetric equilibrium on a path. The tests retained here do not prove that lemma.

The numerical tree search is exploratory only. It checks 175 non-whisker unlabeled trees with 5 through 10 vertices, four deterministic starting vectors each at alpha=1.34, and found no fully supported attracting equilibrium. This is finite evidence with no completeness claim for all equilibria, all finite graphs, or stochastic support.

## Public primary references

- Christian Hirsch, Mark Holmes, Victor Kleptsyn, *Infinite WARM graphs III: strong reinforcement regime*, Nonlinearity 36 (2023), 3013–3042. DOI: https://doi.org/10.1088/1361-6544/acc9a0. Published PDF: https://pure.au.dk/ws/portalfiles/portal/418609000/Hirsch_2023_Nonlinearity_36_3013.pdf. Theorem 1, PDF page 5 (printed 3016); unit initial tallies on PDF page 3 (printed 3014); Proposition 1 for E_infinity=E_plus.
- Mark Holmes and Victor Kleptsyn, *Proof of the WARM whisker conjecture for neuronal connections*, Chaos 27 (2017), 043104. DOI: https://doi.org/10.1063/1.4978683. Author manuscript: https://researchers.ms.unimelb.edu.au/~mholmes1@unimelb/Reinforced-graphs_final.pdf. Theorem 2(a), Theorem 3/Corollary 1, and least-weight leaf lemma.
- *MATRIX–MFO Tandem Workshop: Stochastic Reinforcement Processes and Graphs*, Oberwolfach Reports 12/2023, DOI: https://doi.org/10.4171/owr/2023/12, PDF pp. 15–18; Open Problems 1 and 2 on PDF p. 17, printed p. 655.

## Appendix: exact unequal-rate scope control

The equal-rate condition in the whisker clause is substantive. On the four-edge path with five vertices, take alpha=2 and

a=(1/12,1/4,3/4,9/4),
lambda=(1/16,5/24,5/8,15/8,9/16).

Set b=(9,3,1,1/3,1/9). Then a_e=1/(b_u+b_v) and lambda_v=b_v sum_{e incident to v}a_e^2, which proves the equilibrium equations exactly. In the power-coordinate formula (2.2), the negative of the scaled Hessian is the symmetric tridiagonal matrix K with diagonal

(4752/5,128/5,128/135,272/3645)

and successive off-diagonal entries

(432/5,16/5,16/135).

Its leading principal minors are, respectively,

4752/5, 421632/25, 782336/125, 4194304/18225,

all strictly positive. Sylvester's criterion makes K positive definite, so the equilibrium is linearly stable. The published Theorem 1 gives positive-probability convergence from unit tallies, with the whole diameter-four path surviving. This is a scope control: it does not refute the equal-rate whisker target. The 2017 paper already explains that unequal firing rates invalidate a general whisker conclusion; no novelty is claimed for that phenomenon or this explicit illustration.
