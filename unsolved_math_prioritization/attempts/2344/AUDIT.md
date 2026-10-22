# Harmonic LCM avoidance exponent audit

This is an AI-assisted, unrefereed authored mathematical audit edition. Acceptance means an independent internal AI audit of the precisely scoped written arguments and their explicitly retained standard and external dependencies. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete ten-section mathematical reconstruction and full ancillary correction note are retained, including all parameter orders, supremum qualifications, density substitutions, dependencies and limitations. Executable code, raw calculation outputs or datasets, copied source documents or text, source images and private coordination material are not distributed.

Retrieval, inspection and mathematical-check statements describe the original audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. Historical finite checks supplement the written proofs; they do not establish asymptotic claims or numerically evaluate the exponent.

## Conclusion and scope

For every fixed integer k >= 3, the existing weighted argument proves that

    gamma_k = lim_{N -> infinity} log f_k(N) / log log N

exists. Here f_k(N) is the maximum of sum_{a in A} 1/a over subsets A of {1,...,N} with no k DISTINCT elements having a common pairwise least common multiple. The corresponding finite-block characterization is

    gamma_k = sup_{n >= 1, 1 <= r <= n} r M_k(n,r)^(1/r) / (e n),

where M_k(n,r) is the largest cardinality of an r-uniform k-cosunflower-free family on an n-element ground set. The proofs in Chojecki, April 15, 2026, and Luo–Yang–Zhu, September 7, 2026, pass this audit for those claims. This is acceptance of an existing mathematical argument after reconstruction, not a claim of a new theorem, formal verification, or peer-reviewed acceptance.

Two repairs are needed when reading the ancillary full-density argument in Tang–Zhang: a factor 1/(n+1) is dropped on page 13, and the all-n wording of its auxiliary hypothesis H(beta,k) needs an asymptotic qualification. Both are addressed below. The central exponent and finite-block proof does not depend on either defective passage. Chojecki's optional full-density proposition can be justified by the direct density argument provided here.

The formula is exact as a characterization, not a numerical evaluation. None of the three inspected manuscripts evaluates gamma_3, much less every gamma_k. Nor does f_k(N) = (log N)^(gamma_k+o(1)) assert f_k(N) asymptotic to C_k (log N)^gamma_k, a bounded multiplicative error, an effective rate, or a maximizing finite block. The cited numerical interval is discussed with its external dependencies below.

The audit read the complete written text of Tang–Zhang (19 pages, including Appendix A), Chojecki (14 pages), and Luo–Yang–Zhu (9 pages). Key displayed formulas were also checked against rendered PDF pages. All three primary PDF files were freshly retrieved and matched the previously supplied bytes exactly. The provenance file records immutable byte identities, dates, public URLs, and the exact inspection scope. No source-author code was executed.

## Sources and attribution

[TZ] Quanyu Tang and Shengtong Zhang, Harmonic LCM patterns and sunflower-free capacity, arXiv:2512.20055v1, December 23, 2025. https://arxiv.org/abs/2512.20055v1

[C] Przemek Chojecki, Weighted sunflower pressure and the exact polylogarithmic exponent in harmonic LCM patterns, manuscript dated April 15, 2026. https://www.ulam.ai/research/erdos856-final.pdf

[LYZ] Yanping Luo, Ruiyi Yang, and Keheng Zhu, The exponent of harmonic LCM avoidance, arXiv:2609.07268v1, September 7, 2026. https://arxiv.org/abs/2609.07268v1

[E] Paul Erdős, Some extremal problems in combinatorial number theory, Mathematical Essays Dedicated to A. J. Macintyre (1970), 123–133. Original harmonic problem on printed page 127. https://www.renyi.hu/~p_erdos/1970-21.pdf

[ASU] Noga Alon, Amir Shpilka, and Christopher Umans, On sunflowers and matrix multiplication, CCC 2012, 214–223, especially Theorem 2.4 on printed page 216. https://theory.stanford.edu/~virgi/cs367/papers/sunflowersmult.pdf

[L] Jared Duker Lichtman, Almost primes and the Banks–Martin conjecture, arXiv:1909.00804, especially equation (4.9). https://arxiv.org/abs/1909.00804

The weighted squeezing argument belongs to [C]. [LYZ] gives a complete elementary version of the needed weighted estimates and derives the finite-block formula. [TZ] establishes the unweighted bounds, explicit lower constructions, and full-density connection. This report reorganizes and checks those arguments; it does not assert priority for their ingredients or the repairs.

## 1  Definitions and essential hypotheses

A k-sunflower consists of k distinct sets whose pairwise intersections are identical. A k-cosunflower consists of k distinct sets whose pairwise unions are identical. Complements inside ONE fixed ground set exchange these notions. Define, for z > 0,

    W(n;z) = max_F sum_{S in F} z^|S|,  F sunflower-free,
    C(n;z) = max_G sum_{S in G} z^|S|,  G cosunflower-free.

We suppress the fixed subscript k. Set W(0;z)=C(0;z)=1 and M(n,0)=1. The empty set and integer 1 are legitimate members. Their presence causes no exceptional failure: k distinctness is preserved by every injection used below.

The argument requires k >= 3. The proof of the blow-up lemma uses a third member; it is not a k=2 argument. All asymptotics keep k fixed. Prime-support encodings on the LOWER-bound side are used only for squarefree integers; the UPPER-bound side explicitly tracks valuations and therefore also treats nonsquarefree members of A.

## 2  Uniform products and existence of pressure

Let U be an r-uniform sunflower-free family on [n]. Place t copies on disjoint n-element blocks and choose one member from each copy. Their unions form a tr-uniform family U^{box t} of cardinality |U|^t.

Suppose k distinct such unions formed a sunflower. Restrict to a block. The k restrictions have equal pairwise intersections. If two restrictions coincide with B, that pair's intersection is B, and intersection of either with every other restriction is B. Every restriction consequently contains B. Since every restriction has cardinality r=|B|, all coincide. If no two coincide, that block contains a forbidden k-sunflower in U. Thus all restrictions coincide in every block, contradicting distinctness of the original k members. For cosunflowers the same reasoning uses containment in B rather than containment of B.

Uniformity cannot be dropped. The family {empty,{1}} is 3-sunflower-free and 3-cosunflower-free, but its two-block product is the complete power set of two points and contains both configurations. A direct invocation of Fekete's lemma on arbitrary nonuniform products would be unjustified. The three manuscripts avoid this through layer selection.

Choose a layer of an extremal family for W(n;z) carrying at least W(n;z)/(n+1) of its weighted mass. Its t-fold uniform product has mass at least [W(n;z)/(n+1)]^t. Embedding it in any m with tn <= m < (t+1)n gives

    liminf_{m -> infinity} W(m;z)^(1/m)
        >= [W(n;z)/(n+1)]^(1/n).

This is valid even if the bracket is less than 1: the exponent t/m tends to 1/n. Now take arbitrarily large n. The factor (n+1)^(1/n) tends to 1 and 1 <= W(n;z)^(1/n) <= 1+z, so the liminf is at least the limsup. The limit Lambda(z) exists.

Complementation is an exact finite identity:

    C(n;z) = z^n W(n;1/z).

Consequently C(n;z)^(1/n) tends to Ltilde(z)=z Lambda(1/z). The elementary bounds

    z <= Lambda(z) <= 1+z,   1 <= Ltilde(z) <= 1+z

follow from the single full set, the empty set, and the whole power set. In particular D(z)=Lambda(z)-z lies in [0,1]. At z=1 both pressures equal the ordinary capacity mu_k^S.

Quantifiers: the limit is proved separately for each fixed positive z. No uniform convergence in z is assumed or needed.

## 3  Arithmetic estimates with fixed parameters

The classical prime estimates used are

    sum_{p <= x} 1/p = log log x + O(1),
    sum_{p <= x} (log p)/p = log x + O(1).

These are standard Mertens estimates. No prime number theorem in short intervals is required. Every interval below is handled by subtracting these global estimates.

For fixed u>0, extend the harmonic sum to all integers supported on primes <=X. The finite Euler product gives

    sum_{m <= X} u^omega(m)/m
       <= product_{p <= X} (1 + u/(p-1))
       <<_u (log X)^u.

Indeed the logarithm of each sufficiently large prime factor is u/p+O_u(p^-2); finitely many small primes contribute a parameter-dependent constant.

For fixed z>0 put H_z(X)=sum_{q <= X, q squarefree} z^omega(q)/q. Its upper bound is the product of (1+z/p), hence O_z((log X)^z). For a lower bound take theta=1/[8(1+z)] and Y=X^theta. Give every squarefree product of primes <=Y probability proportional to z^omega(q)/q. The normalizing constant is

    Z_Y = product_{p <= Y} (1+z/p) asymp_z (log X)^z.

Under this measure each prime is included independently with probability z/(p+z), so

    E(log Q) = sum_{p <= Y} z log p/(p+z)
             <= z log Y + O_z(1)
             <= (log X)/8 + O_z(1).

For sufficiently large X, Markov's inequality bounds P(Q>X) by 1/4. At least 3/4 of Z_Y therefore comes from q<=X, proving

    H_z(X) asymp_z (log X)^z.

This checks and strengthens the exact analytic input required in [C, Lemma 3.2], which cites Selberg–Delange. The elementary proof is already given by [LYZ, Lemma 2.3]. Nothing needs to be uniform when z grows: X tends to infinity first for each fixed z.

## 4  Upper transference including prime powers

Let A be LCM-k-free in [N]. For each positive integer m write P(m) for its prime divisors and let F_m contain the sets S subset P(m) such that

    a = m / product_{p in S} p

belongs to A. This is a well-defined integer and S determines a injectively. If k distinct S_i formed a sunflower with kernel K, then, for every p|m,

    v_p(a_i) = v_p(m) - 1_{p in S_i},
    v_p(lcm(a_i,a_j)) = v_p(m) - 1_{p in S_i intersect S_j}
                      = v_p(m) - 1_{p in K}.

Thus the k distinct a_i would have identical pairwise LCMs. F_m is therefore sunflower-free. There is no coprimality condition between a and its squarefree multiplier, and no assumption that m or a is squarefree.

Expand

    (sum_{a in A} 1/a) H_z(N)
       = sum_{a in A} sum_{q <= N, q squarefree} z^omega(q)/(a q).

The substitution m=aq, S=P(q) is injective at fixed m, and m<=N^2. After allowing additional representations whose q may exceed N, nonnegativity gives

    (sum_{a in A} 1/a) H_z(N)
       <= sum_{m <= N^2} W(omega(m);z)/m.

The inequality direction, rather than equality, matters. From the pressure limit, for every fixed delta>0 there is a finite constant B(k,z,delta) such that

    W(s;z) <= B(k,z,delta) (Lambda(z)+delta)^s

for EVERY integer s>=0. The constant covers all small s as well as the asymptotic tail. Applying section 3 at u=Lambda(z)+delta and using log(N^2)=2 log N gives

    f_k(N) <<_{k,z,delta} (log N)^(Lambda(z)-z+delta).

Divide logarithms by log log N, let N tend to infinity, and then delta decrease to zero. With beta=limsup log f_k(N)/log log N, the conclusion is

    beta <= D(z) for each fixed z>0.

The bound is uniform over A because B depends on the extremal partition function, not on A. This justifies taking the maximum over A before the N-limit.

## 5  Blow-ups and lower transference

Partition a set into disjoint nonempty buckets U_1,...,U_t. Replace each index set G by every set choosing exactly one point from bucket i if i belongs to G, and no point otherwise. If the index family is k-cosunflower-free, its blow-up is too.

To prove this, suppose k distinct blown-up sets B_j have the same pairwise union. Their index sets G_j also have equal pairwise unions. If G_u=G_v, distinctness of B_u,B_v forces different chosen points x,y in some common bucket. A third member B_w must choose y to make B_u union B_w equal B_u union B_v, and x to make B_v union B_w equal that same union. It cannot choose two points from one bucket. Thus the G_j are distinct, a contradiction. This deals explicitly with the possible repeated projections that would invalidate a naive argument.

For positive weights all smaller than delta, a total mass >=t(z+delta) permits t disjoint buckets with masses in [z,z+delta). Add weights until reaching z and repeat. Before the last addition the current sum is <z; the overshoot is <delta. After t-1 buckets enough mass remains. The non-strict assumption w<=delta used in [C] also works, since the pre-final sum is strictly <z.

Fix z>0. If Ltilde(z)=1, the desired lower estimate is trivial because f_k(N)>=1. Otherwise fix 1<lambda<Ltilde(z), eta in (0,1/2), and 0<delta<eta z/4. These parameters remain fixed as N grows. Put

    L=log log N,
    t=floor((1-eta)L/z),
    x=N^(1/t),
    y=exp(L^(2/3)).

For all sufficiently large N, t>=1 and y<x. The reciprocal mass of primes in (y,x] is

    log log x - log log y + O(1)
      = L - log t - (2/3)log L + O(1)
      = L - o(L).

Meanwhile

    t(z+delta) <= (1-eta)(1+delta/z)L <= (1-eta/2)L,

and every 1/p for p>y is eventually <delta. Therefore the greedy lemma gives t disjoint prime buckets P_i in (y,x], with J_i=sum_{p in P_i}1/p in [z,z+delta).

Since t tends to infinity and C(t;z)^(1/t) tends to Ltilde(z), for ALL sufficiently large t there is a cosunflower-free G_t with sum_{G in G_t}z^|G|>=lambda^t. Blow up G_t over the prime buckets and encode each selected prime set by its product. Every resulting integer a is squarefree and a<=x^|G|<=x^t=N. Distinct prime sets give distinct products, and the blow-up lemma makes the resulting A LCM-k-free.

Different G give disjoint product collections: the set of occupied prime buckets recovers G. Consequently unique factorization yields the exact identity

    sum_{a in A} 1/a = sum_{G in G_t} product_{i in G} J_i
                    >= sum_{G in G_t} z^|G|
                    >= lambda^t.

It follows, for alpha=liminf log f_k(N)/log log N, that

    alpha >= (1-eta) log(lambda)/z.

Take N to infinity first, then lambda upwards to Ltilde(z) and eta downwards to zero. Thus

    alpha >= log Ltilde(z)/z for every fixed z>0.

The rounding error in t is O(1); after multiplication by the fixed log(lambda) and division by L it is o(1). The Mertens loss is O(log L) and is dominated by the fixed eta L slack. There is no estimate uniform in a parameter tending to zero with N. For [C, Theorem 4.4], its epsilon can harmlessly be restricted to (0,1/2), so the choice eta=epsilon is valid.

## 6  The squeeze and all orders of limits

The trivial bound 1<=f_k(N)<=sum_{a<=N}1/a gives 0<=alpha<=beta<=1. For each fixed z>0, the upper bound says beta<=D(z). Apply the lower bound at u=1/z and use pressure duality to obtain

    alpha >= z log(Lambda(z)/z)
           = z log(1+D(z)/z).

For t>=0, log(1+t)>=t-t^2/2. Since 0<=D(z)<=1,

    D(z)-1/(2z) <= z log(1+D(z)/z) <= D(z).

In particular, 0<=beta-alpha<=1/(2z) for EVERY fixed z>0. Letting z tend to infinity only after the N-limits proves alpha=beta=gamma_k. Moreover

    gamma_k <= D(z) <= gamma_k + 1/(2z).

Hence D(z) tends to gamma_k, its infimum over z>0 is gamma_k, and the lower expression approaches gamma_k from below. We have

    gamma_k = lim_{z -> infinity} (Lambda(z)-z)
            = inf_{z>0} (Lambda(z)-z)
            = sup_{z>0} z log(Lambda(z)/z)
            = sup_{u>0} log Ltilde(u)/u.

Finally Ltilde(u)=1+u D(1/u), so

    gamma_k = lim_{u -> 0+} (Ltilde(u)-1)/u.

There is no interchange of an N-limit with an unbounded z-limit here. All the fixed-z estimates first constrain two real numbers alpha and beta. Only those inequalities are subsequently squeezed as z grows. No differentiability of the pressure, attainment of its infimum, or monotonicity of D is needed. The bound D(z)<=gamma_k+1/(2z) is a consequence of the squeeze, not a uniform finite-N error bound.

## 7  Removing continuous weights

For fixed z>0 set

    S(z)=sup_{n>=1,0<=r<=n} [M(n,r) z^r]^(1/n).

Each uniform layer is an admissible cosunflower-free family, and uniform tensor powers imply Ltilde(z)>=[M(n,r)z^r]^(1/n) for each fixed block. Thus Ltilde(z)>=S(z).

Conversely, every cosunflower-free family splits into n+1 uniform layers. Each has cardinality at most M(n,r), giving

    C(n;z) <= sum_{r=0}^n M(n,r)z^r
            <= (n+1) S(z)^n.

Taking nth roots and limits gives Ltilde(z)<=S(z). S(z) is finite (indeed <=1+z by the reverse inequality), so the logarithm is legitimate. Its positivity is guaranteed by the r=0 contribution 1. Therefore

    log Ltilde(z) = sup_{n,r} [log M(n,r)+r log z]/n.

This uses monotonicity and continuity of log on positive numbers and the defining approximation property of a finite supremum. It does not exchange a supremum with a limit. The two suprema in

    gamma_k = sup_{z>0} sup_{n,r} [log M(n,r)+r log z]/(n z)

can be interchanged because both equal the supremum over the same Cartesian product. This is not a minimax theorem, and no compactness or optimizer is being assumed. The r=0 term is exactly 0.

For r>=1 and M>=1, differentiation of g(z)=[log M+r log z]/(n z) gives

    g'(z)=[r-log M-r log z]/(n z^2).

It is positive below z_*=e M^(-1/r) and negative above. Also g(z) tends to minus infinity as z tends to zero, and to zero as z tends to infinity. The global maximum is

    g(z_*)=r M^(1/r)/(e n).

This proves the stated finite-block formula. Since M(n,r)<=binom(n,r)<=(e n/r)^r, every block contributes <=1. The complete singleton layer is cosunflower-free for k>=3 and has M(n,1)=n, yielding gamma_k>=1/e>0 independently of any external construction.

A finite block supplies a certified lower bound. Given epsilon>0, the definition of supremum guarantees some block within epsilon of gamma_k. It does NOT bound that block's n or supply an algorithmic stopping certificate for numerical approximation from below. A finite collection of lower bounds cannot certify an upper bound on the full supremum.

## 8  Consequences and what remains unresolved

If r<=k-2, the whole r-layer is cosunflower-free. In a hypothetical common-union configuration with union U, the missing parts D_i=U\S_i would be disjoint and have a common positive size d unless all sets coincide. Thus k d <= |U|=r+d, or (k-1)d<=r, impossible for r<=k-2. Taking r=k-2 and n to infinity in the finite formula gives

    gamma_k >= (k-2) / [e ((k-2)!)^(1/(k-2))].

At z=1 the pressure formulas give

    log mu_k^S <= gamma_k <= mu_k^S-1 <=1.

Increasing k relaxes the forbidden configuration, so f_k(N)<=f_{k+1}(N) and gamma_k<=gamma_{k+1}. With r=k-2, Stirling's formula gives

    r/[e(r!)^(1/r)]
       = 1 - log(2 pi r)/(2r) + O((log r)^2/r^2),

and hence gamma_k tends to 1 as k tends to infinity. This latter statement follows after proving each fixed-k exponent; it is not a uniform-in-k asymptotic for f_k(N).

[TZ] and [LYZ] cite the established capacity estimates mu_3^S>1.551 (Deuber–Erdős–Gunderson–Kostochka–Meyer, 1997) and mu_3^S<=3/2^(2/3) (Naslund–Sawin, 2017). Substitution yields

    0.438899884194402... = log(1.551) < gamma_3
       <= 3/2^(2/3)-1 = 0.889881574842310....

The substitution, directions, and decimal arithmetic were checked here. The underlying 1997 construction and 2017 upper-bound proof were not independently re-audited in this packet. They are explicit external dependencies of this sharper numerical interval, not dependencies of exponent existence or the finite-block equality. The elementary audited bound 1/e<=gamma_k<=1 needs neither.

The following remain unsupported as stronger conclusions: a numerical evaluation of gamma_3; a closed formula for general gamma_k; a determination from the single unweighted value mu_k^S; an attained finite maximum; and a full multiplicative asymptotic equivalent for f_k(N). Exponent existence alone permits factors such as powers of log log N and much larger subpowers of log N.

## 9  Tang–Zhang proof audit and local repairs

### 9.1  Its explicit construction and capacity bounds

[TZ, section 3] takes r=k-2 primes from each of t disjoint prime buckets. Its combinatorial lemma applies to projections even when they repeat: any k r-sets with equal pairwise union must all be equal when r<=k-2. Thus distinct global products cannot form a forbidden tuple.

Writing J_i for a bucket's reciprocal mass, its r-th power equals r! times the elementary symmetric sum plus tuples with repeats. The repeat contribution is at most binom(r,2) delta J_i^(r-1) if every prime reciprocal is <=delta. With r fixed, J_i=B+O(delta), t=(1+o(1))L/B and delta=L^(-1/2), the accumulated logarithmic loss is O(t delta)=O(sqrt L)=o(L). Its available prime mass loses only O(log L), while the deliberate slack is of order sqrt L. Optimizing (r log B-log(r!))/B at B=e(r!)^(1/r) gives the advertised lower exponent. These uniform errors check out.

[TZ, sections 4 and 6] are the unweighted endpoint and one-prime-per-bucket constructions reconstructed above. Its section 4 displayed use of log N+log 2 in place of log(N^2)=2 log N is a harmless scale typo: the needed bound is still O_delta((log N)^(mu+delta)). The final upper conclusion is unchanged.

Its Appendix A derives a uniform H_ell(N) lower bound from squarefree Sathe–Selberg. Fix eta>0, L=log log N and 2<=ell<=(1-eta)L. Restrict partial summation to log log t in [L/2,L]. The range ell<=(2-2eta)log log t stays inside the stated theorem's compact parameter range, its relative error is O_eta(1/L), and the continuous positive Euler factor has a positive minimum on [0,2(1-eta)]. Integrating u^(ell-1) from L/2 to L gives at least L^ell/(2ell), hence H_ell(N)>>_eta L^ell/ell! uniformly in ell. The ell=1 case is Mertens. Equation (4.9) of [L] matches the squarefree Euler factor and form used. The general Sathe–Selberg theorem itself is treated as a standard cited input, not reproved here. The main weighted audit bypasses it through section 3.

### 9.2  The factor dropped in Lemma 5.6

On [TZ, printed page 13], the first displayed inequality contains 1/(n+1), but the immediately following equality discards it. Rendered-PDF inspection confirms this is present in the source, not an extraction artifact. With the paper's c, m=floor(cn), delta and W, the correct chain is

    mu_w(A) >= (n+1)^(-1)
       exp(-c(m+1)-(n-m)/n) exp(-2 delta n)
       >= exp(-log(n+1)-cW-c-1-(epsilon/5)W).

The missing term is -log(n+1) in the exponent. The existing choices have 0<epsilon<=1/10, c=1/ceil(1/epsilon^2)<=epsilon/10, delta=epsilon c/10, and n<=W/c. Define

    a_epsilon = (log 2-1/5)epsilon-c >0.

Enlarge K(epsilon) so that, for every W>=K(epsilon),

    log(W/c+1)+c+1 <= a_epsilon W.

Such a finite threshold exists because c and epsilon are fixed and log W/W tends to zero. Since log(n+1)<=log(W/c+1), the corrected chain gives

    mu_w(A) >= exp(-(log 2)epsilon W) = 2^(-epsilon W).

All other earlier requirements on K are finitely many lower bounds, so they can be met simultaneously. This repairs the lemma with its original conclusion and original parameter dependence. It does not justify the printed equality or its particular final numeric threshold on its own.

### 9.3  The all-n hypothesis and a complete density substitute

[TZ, Theorem 5.5] formulates H(beta,k) using every positive admissible n. Read literally, H(2,3) fails already at n=1: both singleton sets on [2] form a family of size 2, meet any threshold 2^(1-eta) for eta>0, and contain no three distinct members. Thus the intended asymptotic hypothesis should specify all sufficiently large n. Failure of a literal all-n hypothesis does not by itself provide arbitrarily large counterexamples. The cited [ASU] proof uses asymptotic estimates and uniform products; it does not remove the need to handle small-n wording.

For clarity, here is a direct proof of the precise consequence needed later, valid for every fixed k>=3. Assume mu_k^S=2; by complementation the largest nonuniform cosunflower-free family also has size 2^(m-o(m)) for every large m. Selecting its largest layer gives an s-uniform family of that size. The entropy bound on binomial coefficients forces s/m=1/2+o(1).

First construct almost-full exponential-size middle layers for every large q. Fix a small constant rho>0 and take m=floor((2-rho)q). For large q, both s<=q and m-s<=q. Adjoin q-s common new elements to every set and enough additional unused elements to obtain ground-set size 2q. This preserves cosunflower-freeness and produces q-sets on [2q], of cardinality 2^((2-rho)q-o(q)). Taking q to infinity and then rho down to zero yields

    M_k(2q,q) = binom(2q,q) exp(-o(q)).

The meaning is a logarithmic equality; no ratio tending to 1 is claimed.

Now fix alpha in (0,1), let r=floor(alpha n), q=max(r,n-r), and start from such a q-uniform family F on [2q]. Its relative density in the q-layer is delta_q=exp(-o(q)). If r<=n/2, set d=n-2r. Average over d-sets D to find one contained in at least

    |F| binom(q,d)/binom(2q,d)
       = delta_q binom(n,r)

members. Remove this common D from those members and the universe. The residual family consists of r-sets on n points, and remains cosunflower-free.

If r>=n/2, put d=2r-n. Average instead over d-sets D avoided by the members. The same identity gives at least delta_q binom(n,r) members lying in the remaining n points. This restriction also preserves cosunflower-freeness. Since q is proportional to n,

    M_k(n,floor(alpha n)) >= binom(n,floor(alpha n)) exp(-o(n)).

For every fixed eta>0, log binom(n,floor(alpha n))=n H(alpha)+o(n) with H(alpha)>0. Hence the last bound is at least binom(n,floor(alpha n))^(1-eta) for all sufficiently large n. This proves exactly the consequence used by [TZ, Lemma 5.6] and [C, Proposition 5.4], including their all-large-n quantifier, without relying on the imprecisely stated H hypothesis. Fixed common additions/deletions and fixed-universe restrictions preserve distinctness, so the generalization to every fixed k needs no unsupported nonuniform product step.

### 9.4  Full-density consequences after repair

The repaired weighted product-measure lemma feeds [TZ, section 5.4]. With prime weights w_p=1/(p+1), division by the empty-set mass turns product-measure mass into harmonic sum exactly. The total reciprocal mass over its unrestricted squarefree family is at least a constant times (log T)^(1-(log 2)epsilon/2). Its discarded tail above N is at most O_epsilon((log T)^2/log N), using the first logarithmic moment of the squarefree Euler product. Choosing log T=(log N)^(1-3epsilon/5) gives a main exponent greater than 1-epsilon and an error exponent 1-6epsilon/5. For sufficiently small fixed epsilon this proves the desired lower bound; larger epsilon follows by weakening it. Thus the full-density equivalence survives the repair.

Alternatively, the density substitute directly verifies [C, Proposition 5.4]. Uniform layers of density beta have weighted n-th-root mass approaching z^beta exp(H(beta)). The maximum over beta in [0,1] is 1+z. Therefore Lambda(z)=1+z and Ltilde(z)=1+z if mu_k^S=2, and gamma_k=1. The converse follows from gamma_k<=mu_k^S-1. This route needs neither the dropped-factor calculation nor its tail estimate.

## 10  Acceptance boundaries and reproducibility

The accepted core is: existence of the fixed-k logarithmic exponent; the two weighted variational descriptions; their finite-block elimination; the elementary complete-layer bounds and monotonicity consequences. The independent reconstruction supplies every nontrivial combinatorial and arithmetic-transfer step in that core, with Mertens estimates as standard analytic inputs.

Ancillary status: Tang–Zhang's printed Lemma 5.6 calculation requires the explicit factor repair; its H hypothesis should be read in an asymptotic form, with the required consequence proved directly above. The sharper numerical interval retains the named external capacity theorems as dependencies. This audit does not attest to journal acceptance of any 2026 manuscript, execute AI- or author-supplied proof software, or characterize the entire original estimation problem as fully solved.

Authored finite checks exhaust all uniform families on at most four points for two-block products, all nonuniform index families on at most three points with two-element bucket blow-ups, endpoint arithmetic tuples for m<=500, and exact M_k(n,r) through n=5 for k=3,4,5. They also check negative controls for nonuniform tensor closure and the literal small-n hypothesis. Such tests supplement the proofs; they cannot establish asymptotic claims. The original audit manifest and verifier bound its exact files and detected modifications, deletions, additions, and symlinks. This edition distributes verification metadata in VERIFICATION.json and its own eight-file inventory in MANIFEST.json, but no executable verifier or raw finite-check outputs. Mathematical acceptance remains an argued conclusion, separate from byte-integrity success.
