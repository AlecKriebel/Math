# Source-question-only reconstruction: ordinary triangle counts

Author metadata: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X. This is an independent mathematical reconstruction, not an originality or priority determination.

## 1. Independence, exact target, and result

This family read the original source question and the primary standard result identified below. It did not read any candidate PR, submitted proof/audit, another family's work, root mathematical notes, or outcome records before this initial seal. No outreach, delegation, Git/index/ref mutation, PR mutation, or publication was performed. All durable authored outputs are at this folder root. Downloaded third-party bodies and page renders are in ignored `_local/`.

Fix one constant p in (0,1). Let G be G(n,p), with independent edges, and let

T = sum over unordered 3-vertex sets S of 1{all three edges on S occur}.

Thus T counts ordinary triangles, not labeled embeddings (which would give 6T). Write mu=E T, sigma²=Var T, and phi(x)=(2pi)^(-1/2) exp(-x²/2). For every positive integer q define

D_n(q) = max_{0<=a<q} |q P(T=a mod q)-1|.

The exact answer, for every positive integer modulus sequence q_n without a monotonicity or primality condition, is

**D_n(q_n) -> 0 if and only if q_n=o(sigma_n), equivalently q_n=o(n²).**

Here q=1 is permitted and has D_n(1)=0. The claim is for fixed p, not an assertion about p approaching 0 or 1. The ordinary LLT holds uniformly over all integer values k, with the quantitative error in Section 3. The complete modular extension is the following stronger statement. Put

g_n(k) = sigma^(-1) phi((k-mu)/sigma),

G_{n,q}(a) = sum_{j in Z} g_n(a+jq),

r_n = C_p n^(-3/8) sqrt(log n) + O_p(n^(-10)).

Then

sup over all positive integers q and 0<=a<q of
min(q,sigma) |P(T=a mod q)-G_{n,q}(a)| <= r_n -> 0.       (F)

The power 3/8 is a convenient choice from the published theorem, not a claimed best rate. The full modular Gaussian approximation (F) includes all critical and supercritical moduli. Uniformity itself ends at q=o(n²).

Success criteria were: identify the authentic source's count and LLT convention; justify the imported theorem's hypotheses and normalization; prove sufficiency and necessity in the stated relative metric for every modulus sequence; give checkable boundary behavior; and distinguish the adjacent fixed-H conjecture. These are met below, using the explicitly identified deep LLT. That deep theorem is imported, not reproved.

## 2. What the original source actually says

The original is Alex Scott, joint work with Atsushi Tateno, “On the Number of Triangles in a Random Graph,” printed pages 1279–1280, PDF pages 55–56, in Oberwolfach Report 23/2009. The publication and DOI are [EMS Press, OWR 23/2009](https://ems.press/journals/owr/articles/3473), [DOI 10.4171/OWR/2009/23](https://doi.org/10.4171/OWR/2009/23).

The contribution starts with the ordinary number of triangles at constant p. It recalls a prime-modulus logarithmic range, explicitly asks how far this extends, states the necessary q=o(n²) scale, and announces equidistribution for every integer-valued q=o(n²/log n). Its Theorem 3 already announces a uniform ordinary triangle LLT with error o(n^(-2)). Its reference Gaussian is the centered unit-cell mass

c_n(k) = integral from (k-mu-1/2)/sigma to (k-mu+1/2)/sigma of phi(x) dx.

The separate last sentence conjectures analogous results for any fixed subgraph H. The triangle question is therefore distinct from this broader assertion, whose disconnected-H LLT part is false; see Section 9. No labeled-embedding interpretation is justified here. The source pages and Sah–Sawhney's theorem page were read as text and also visually inspected to verify absolute values, integration endpoints, and standard-deviation conventions.

## 3. Exact imported premise and its application

The deep input is Ashwin Sah and Mehtaab Sawhney, *Local limit theorems for subgraph counts*, [arXiv:2006.11369v1](https://arxiv.org/abs/2006.11369v1), [PDF v1](https://arxiv.org/pdf/2006.11369v1), journal DOI [10.1112/jlms.12523](https://doi.org/10.1112/jlms.12523). The inspected version has 47 pages. Theorem 1.1 is on printed/PDF page 3; the ordinary-copy definition is made explicit in §4.1, page 23; §5, pages 28–31, transfers from the fixed-edge model to G(n,p).

Specialized exactly to H=K3, Theorem 1.1 supplies, for every epsilon>0,

sup_{k in Z} |sigma P(T=k)-phi((k-mu)/sigma)|
    <= C_{p,epsilon} n^(epsilon-1/2).                    (LLT)

It also supplies an L1 bound of the same order for the density lattice; we do not need that second bound. The theorem is about connected non-induced subgraph counts in G(n,p), p in (lambda,1-lambda). Choose lambda=min(p,1-p)/2. K3 is connected. No induced-count exceptional-density condition is applicable. The sigma is the actual standard deviation in G(n,p), not its variance or the smaller conditional standard deviation in G(n,m).

The summation defining W in §4.1 is over subgraphs H' of the edge set of K_n isomorphic to H, once each, with a product of their edge indicators. Its constant term is binom(n,v(H)) v(H)!/aut(H) times p^(e(H)). For K3 this is binom(n,3)p³, so its random variable is precisely ordinary T. It is not 6T. The lattice in Theorem 1.1 is (Z-mu)/sigma and its Gaussian N is the standard normal density; this yields (LLT) directly.

The imported proof is Fourier analytic and deep. We inspected its theorem, count definition, normalization, and relevant transfer/counterexample passages, not every lemma or line of its proof. In particular, the bound in its Lemma 4.1 uses the fixed-size-model quantities from §3.1; transplanting it unchanged as a G(n,p) characteristic-function estimate with sigma~n² would require an additional argument. We do not make that transplant. This family uses the authentic quantitative LLT plus a fully proved Gaussian folding step; it does not claim a new independent proof of the deep LLT or pretend that changing the postprocessing alone is a different LLT mechanism. The later arXiv:2412.09535v1 is not needed and was not retrieved.

For concreteness choose epsilon=1/8, and set delta_n=C_p n^(-3/8). Then (LLT) says |P(T=k)-g_n(k)|<=delta_n/sigma for all integers k. This quantitative decay, together with the tail estimate below, prevents an unsupported summation of a pointwise o(1/sigma) error over arbitrarily many values.

## 4. Moments, primitive count lattice, and elementary concentration

Let N=binom(n,2), C=binom(n,3), xi_e=X_e-p, and v=p(1-p). Expand each triangle product. Orthogonality of distinct products of independent centered edge variables gives

T-mu = L+R,

L=p²(n-2) sum_e xi_e,

R=p sum_{unordered adjacent edge pairs {e,f}} xi_e xi_f
  + sum_{triangles {e,f,g}} xi_e xi_f xi_g.

There are 3C adjacent unordered edge pairs, each occurring in one triangle. All monomials appearing in this expansion are distinct, hence mutually orthogonal. Consequently

mu=C p³,

Var L=N(n-2)² p^5(1-p),

Var R=3C p^4(1-p)²+C p³(1-p)³=O_p(n³),

sigma²=Var L+Var R
      =C p³(1-p³)+12 binom(n,4) p^5(1-p)
      ~ [p^5(1-p)/2] n^4.                              (V)

The equivalent covariance formula counts unordered triangle pairs sharing an edge; disjoint edge sets, even with one shared vertex, have zero covariance. The empty graph and a graph consisting of one triangle and isolated vertices have T=0 and T=1 with positive probability at n>=3. The ordinary statistic therefore has primitive lattice span 1. This observation does not assert that every intermediate integer is attained.

Changing one edge changes T by at most n-2. The bounded-differences inequality, proved by the independent-edge Doob martingale and the bounded-range exponential-moment bound, gives

P(|T-mu|>x) <= 2 exp[-2x²/(N(n-2)²)].                  (BD)

This is the standard elementary bounded-differences inequality, imported as a standard probability inequality rather than as a graph-count theorem. By the projection variance in (V), kappa=p^5(1-p)>0 satisfies sigma²>=kappa N(n-2)², so

P(|T-mu|>Lsigma) <= 2 exp(-2kappa L²).                 (T)

Take L=A_p sqrt(log n), with A_p sufficiently large that both sigma times the right side of (T) and exp(-L²/2) are O_p(n^(-10)). This is possible since sigma=O_p(n²).

## 5. Proof of the universal modular Gaussian LLT

Fix any positive integer q and residue a. Put m=min(q,sigma), h=q/sigma. Within I=[mu-Lsigma,mu+Lsigma], the progression a+qZ has at most 2Lsigma/q+1 points. Thus its central contribution to the approximation error, multiplied by m, is at most

(m delta_n/sigma)(2Lsigma/q+1)
    =delta_n(2L m/q+m/sigma) <= delta_n(2L+1).          (C)

The actual probability omitted outside I is at most P(T outside I). After multiplication by m<=sigma, (T) makes this O_p(n^(-10)), uniformly in q,a.

It remains to control the Gaussian progression tail uniformly in q, including huge q. Write the normalized progression as u+jh. Its positive points beyond L have a first point x0>L and spacing h. Since phi decreases on the positive half-line,

sum_{x in u+hZ, x>L} phi(x)
    <= phi(L)+h^(-1) integral_L^infinity phi(x) dx.

Indeed the first point contributes at most phi(L), and each later point is bounded by the integral over its preceding interval of length h divided by h. The same argument applies to the negative tail. Multiplying by m/sigma=min(h,1) shows

m sum_{k=a mod q, |k-mu|>Lsigma} g_n(k)
 <=2[phi(L)+integral_L^infinity phi(x) dx]
 <=C exp(-L²/2).                                      (G)

The last inequality is valid for L>=1; only large n are relevant. Combining (C), (T), and (G) proves (F), uniformly over every q>=1. There is no omitted q factor in this argument. Uniformity over q is a proved conclusion, not an added assumption on the source theorem.

## 6. Poisson folding, sufficiency, and the critical/supercritical regimes

The Gaussian is a Schwartz function, so the classical Poisson summation identity applies with absolutely convergent sums. If theta=(a-mu)/q modulo 1, then exactly

q G_{n,q}(a) = W_h(theta),

W_h(theta)=h sum_{j in Z} phi(h(j+theta))
 =1+2 sum_{ell>=1} exp(-2pi²ell²/h²) cos(2pi ell theta). (P)

This also follows by computing the Fourier coefficients of the smooth periodic Gaussian sum; its ell-th coefficient is exp(-2pi²ell²/h²). Thus (P) need not be accepted as a graph-specific imported estimate.

If q=o(sigma), eventually q<=sigma and (F), (P) yield

D_n(q) <= r_n + 2 sum_{ell>=1} exp[-2pi²ell²(sigma/q)²]
        -> 0.                                        (S)

For example, with B=2pi²(sigma/q)², the sum is at most exp(-B)/(1-exp(-B)) because ell²>=ell. This proves sufficiency without requiring q to be prime, increasing, unbounded, or a power of n. It includes q=n²/f(n) for every positive f(n)->infinity, even much slower than log n.

For completeness, the following finer regimes also follow from (F).

* If q/sigma->c in (0,infinity), then

  D_n(q) -> F(c):=2 sum_{ell>=1} exp(-2pi²ell²/c²)>0.  (K)

  To verify this limit, multiply (F) by q/min(q,sigma), which stays bounded. The phase grid {(a-mu)/q mod 1:0<=a<q} has mesh 1/q->0. The Fourier series in (P) converges uniformly in theta and for h in a compact neighborhood of c. Finally, |W_c(theta)-1| is bounded by the sum of its positive Fourier coefficients, with equality at theta=0. This proves (K), including arbitrary drifting phases of mu relative to q.

* If h=q/sigma->infinity, then

  max_a sigma P(T=a mod q) -> phi(0),

  D_n(q)/h -> phi(0)=1/sqrt(2pi), so D_n(q)->infinity. (U)

  For the Gaussian progression, choose its point nearest 0 in [-h/2,h/2]. That point contributes at most phi(0); the others contribute at most 2 sum_{j>=1} phi((j-1/2)h)=o(1). Conversely, the residue containing an integer nearest mu has a term tending to phi(0). Formula (F), with m=sigma, transfers these bounds to the actual probabilities. Since q max_a P(T=a mod q) tends to infinity, it eventually dominates the negative-deviation bound 1-q min_a P(T=a mod q)<=1, proving (U). This proof also covers q larger than the entire support of T.

These regimes are assertions along whichever subsequences satisfy their displayed limits. Arbitrary oscillating sequences are governed by the exact iff statement; a limit for q/sigma is never required for that statement.

## 7. Necessity independently of the deep LLT

Necessity does not need (LLT) or (F). For q>=2, the uniform residue distribution has first Fourier coefficient zero, so

|E exp(2pi i T/q)|
 = |sum_{a=0}^{q-1} [P(T=a mod q)-1/q] exp(2pi i a/q)|
 <= sum_a |P(T=a mod q)-1/q| <= D_n(q).               (N1)

We independently derive the ordinary CLT in a form uniform for characteristic-function arguments in a fixed compact interval. The expansion in Section 4 has R with Var R=O_p(n³), while sigma~c_p n². Hence E|R|/sigma=O_p(n^(-1/2)). Let b=p²(n-2). The characteristic function of b sum_e xi_e /sigma is a product of N identical Bernoulli factors. Uniformly for |t|<=B, its logarithm is

-t² N b² v/(2sigma²)+O_{p,B}(N |b/sigma|³)
 =-t²/2+O_{p,B}(1/n),

because N b²v=Var L=sigma²[1+O_p(1/n)] and b/sigma=O_p(1/n). The logarithm uses the branch continuous near 1; the factors lie uniformly near 1 for bounded t and large n. The inequality |exp(ix)-exp(iy)|<=|x-y| controls the remainder R. Therefore

sup_{|t|<=B} |E exp[it(T-mu)/sigma]-exp(-t²/2)|
    =O_{p,B}(n^(-1/2)).                               (N2)

Suppose q_n is not o(sigma_n). There is an epsilon>0 and an infinite subsequence with q_n/sigma_n>=epsilon, and eventually q_n>=2 on it. Set t_n=2pi sigma_n/q_n, so |t_n|<=2pi/epsilon. The centering phase does not affect modulus. From (N1)–(N2), along this subsequence,

D_n(q_n) >= exp[-2pi²(sigma_n/q_n)²]-o(1)
          >= exp(-2pi²/epsilon²)-o(1)>0.               (N3)

This contradicts convergence to zero. It treats bounded-away-from-zero, unbounded, and oscillating q/sigma in one argument. Together with (S) and (V), this proves the exact full range.

## 8. Density versus centered Gaussian cells

The source's ordinary LLT uses c_n(k), the centered unit-cell probability in Section 2. Taylor expansion of phi about z=(k-mu)/sigma, integrating over [-1/(2sigma),1/(2sigma)], cancels the odd term and gives, uniformly in k,

|c_n(k)-g_n(k)| <= ||phi''||_infinity /(24 sigma³).

Since sigma~c_p n², the difference is O_p(n^(-6)). Combining with (LLT) proves, for every epsilon>0,

sup_{k in Z} |P(T=k)-c_n(k)| = O_{p,epsilon}(n^(-5/2+epsilon)).

The same bound holds with g_n(k). Taking any epsilon<1/2 recovers the 2009 o(n^(-2)) LLT in its actual cell convention. Centered unit cells partition the real line; density samples g_n(k) instead have total mass 1+O(exp(-2pi²sigma²)) by Poisson summation. This exponentially tiny mass discrepancy has no effect on (F) or the iff result. No statement is made that an unquantified pointwise LLT by itself automatically gives a relative modular LLT at every subcritical q.

## 9. Adjacent fixed-H issue: an ordinary-copy obstruction already known

Sah–Sawhney Theorem 1.3 explicitly treats ordinary copies of H=2K2 and proves max_x P(X_H=x) >= c_p n^(1/2)/sigma_H, contradicting a Gaussian LLT at scale sigma_H. The following elementary reconstruction shows why the ordinary-copy version, rather than merely a homomorphism-square observation, obstructs that part of the 2009 broader conjecture. It is credited as a reconstruction of an existing obstruction, not a new discovery.

Let M be the edge count and W=sum_v binom(d_v,2) the number of wedges. The ordinary number X of unordered pairs of vertex-disjoint edges satisfies the exact identity

X=binom(M,2)-W.                                      (H1)

No assumption about induced copies is involved: extra edges between the four vertices do not exclude a copy. Conditional on M=m, define N=binom(n,2), s=3binom(n,3), d=2(n-2), A=Nbinom(d,2), B=binom(s,2)-A, and r_j=(m)_j/(N)_j. W is the sum of s indicators for adjacent edge pairs. Two distinct wedges either share one edge (A unordered pairs) or have four distinct edges (B pairs). Thus

E(W|M=m)=s r_2,

Var(W|M=m)=s(r_2-r_4)+2A(r_3-r_4)+s²(r_4-r_2²).       (H2)

Take m=floor(pN), and f=m/N. For fixed j<=4,

r_j=f^j-binom(j,2) f^(j-1)(1-f)/N+O_p(N^(-2)).

Consequently r_3-r_4=f³(1-f)+O_p(N^(-1)) and r_4-r_2²=-4f³(1-f)/N+O_p(N^(-2)). The apparent n^4 terms in (H2) cancel because s=Nd/2 and

2A-4s²/N=-2s.

It follows that Var(W|M=m)=O_p(s+A/N+s²/N²)=O_p(n³). Chebyshev puts a fixed positive conditional probability in an interval of O_p(n^(3/2)) integers. Stirling's formula gives P(M=floor(pN))>=c_p/n. Using (H1) and pigeonholing, some integer x has

P(X=x)>=c_p n^(-5/2).                                (H3)

For comparison, with D=binom(n-2,2), the centered expansion of X is

X-E X=pD sum_e xi_e + sum_{unordered disjoint edge pairs {e,f}} xi_e xi_f,

so orthogonality gives

E X=3binom(n,4)p²,

sigma_X²=N D² p³(1-p)+3binom(n,4)p²(1-p)²
        ~p³(1-p)n^6/8.                               (H4)

Thus sigma_X P(X=x)>=c_p n^(1/2), whereas a uniform normal LLT would keep those scaled masses bounded. This proves the ordinary-copy obstruction without claiming that every modular assertion for every disconnected H has been classified. It does not undermine the K3 result, and is not counted as new research progress toward an original discovery.

## 10. Fresh checks, limitations, and status

Run `python3 finite_checks.py` in this folder to reproduce `finite_checks.json`. The script uses only the Python standard library. It exhaustively enumerated all labeled host graphs for n=3,4,5,6 (33,864 graph configurations, reused across three p values 1/3,1/2,2/3). It verifies exact rational first and second moments, projection/remainder variance decomposition, primitive T=1 support, the ordinary 2K2 identity (H1), its exact variance (H4), the conditional wedge variance (H2), and its cancellation identity. It checks all moduli 1 through binom(n,3)+3, the Fourier-coefficient lower bound, and finite Fourier inversion. It separately compares direct Gaussian folding and its Poisson dual over 21 (h,theta) pairs, including h=50. The maximum finite Fourier-inversion error in this execution was 2.05e-15. These numerical identities corroborate conventions and algebra; they do not establish an asymptotic theorem or replace any proof above.

The original source was read only in the contribution relevant to this question; Sah–Sawhney was read in the theorem/count/transfer/counterexample passages recorded in `source_receipts.json`. Retrieval, text reading, visual inspection, and independent proof work are separately recorded there. No assertion is made to have independently validated the entire 47-page source proof. No whole-literature priority search was performed. The imported LLT already dates to 2020, and the original triangle LLT is announced in 2009. This report proves an explicit deduction from that established input; it supplies no basis for claiming that the threshold, its proof, or the adjacent obstruction is a novel contribution.

Strongest verified result: the exact iff range, universal modular folding approximation (F), critical profile (K), supercritical behavior (U), source-free necessity (N3), correct ordinary density/cell conventions, and an elementary reconstruction of the established ordinary 2K2 LLT obstruction. Remaining mathematical gap relative to the stated target: none once the authentic published LLT is admitted as a standard theorem. Deep premise not reproved: Sah–Sawhney Theorem 1.1. Novelty/priority status: not determined, with substantial explicit prior credit already identified. Initial independent reconstruction completion estimate: 100% for this source-question task; 0% asserted progress toward a newly established original discovery.
