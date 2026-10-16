# Independent audit of polynomial lemniscate inradius

## Verdict and exact scope

**PASS for the stated ordinary-mathematics theorem. No mathematical correction is required.**

This audit independently checks the frozen EP1039 / database 2450 candidate, with 8,595 bytes and SHA-256 `08d83176c955246871b036d0adb77756c1c2e28adfd8bd8154b2a01269f35dd6`. Every step of its proof was read and rederived. The candidate was not edited.

For each integer n >= 1, let F_n consist of the monic degree-n polynomials whose roots, counted with multiplicity, lie in the closed unit disk. Put

rho(f) = sup {r > 0 : some open disk of radius r is contained in {z : |f(z)| < 1}},
R_n = inf {rho(f) : f in F_n}.

The verified assertions are

(log 2)/n <= R_n <= rho(z^n - 1) <= pi/(2n),
and sup {rho(f) : f in F_n} = 1.

In addition, every f in F_n has an open disk of radius (log 2)/n centered at one of its roots and contained in its strict lemniscate. The proof below is complete without assuming any theorem from a computer formalization. Its conventional analytic inputs are elementary Hilbert-space Cauchy-Schwarz, geometric series, Parseval for functions analytic past the circle, the maximum-modulus principle, and Cauchy's coefficient estimate; the precise uses are supplied below.

These conclusions settle the positive-uniform-constant-over-n question and the order of the worst-case inradius. They do not compute R_n, assert that n R_n converges, determine an exact limiting constant, or say rho(f) is O(1/n) for every individual polynomial. For example, rho(z^n) = 1 for every n. For the original strict inequality R_n > c/n, any fixed 0 < c < log 2 suffices.

This is a credited reconstruction of the Price/Kitamura 2026 method. It is not a novelty claim, a claim that a journal or problem website accepted the argument, or a certification that the Lean development compiles.

## Source inspection and provenance qualification

1. P. Erdos, F. Herzog, and G. Piranian, *Metric Properties of Polynomials* (1958), original scan: https://users.renyi.hu/~p_erdos/1958-05.pdf . I independently rendered and visually read physical pages 1 and 10, printed pages 125 and 134. Page 125 defines a monic product and E by the strict inequality |f| < 1, with the relevant roots in the closure of the unit disk. Page 134, Problem 3, asks the uniform c/n question and gives z^n - 1 as the pi/2 obstruction. This confirms that the candidate addresses the original problem's quantity, not just a different level set or a root-spacing problem. The scan has 24 physical pages; the complete paper was not read. The frozen PDF is 4,304,732 bytes, SHA-256 `5d20ad770563e425ac3343e31581859a24facabf744f10489b8f8d201b0ec12a`.

2. Kenta Kitamura, *Erdos Problem 1039 in Lean 4*, https://github.com/KitaKen1/erdos1039-lean . The public README and the frozen README were read. They credit a natural-language proof by Liam Price with GPT assistance and the EP1039 discussion. The README's problem-status statement is explicitly dated May 16, 2026; it is not evidence of current October 2026 status. The public repository page and code page were accessible in this audit. The frozen README is 1,459 bytes, SHA-256 `687f53ff5f928d5dd0746e5196c574badfce10e47f3c20764b224d123632ddd2`.

3. Relevant portions of the frozen `Erdos1039.lean` text were read statically: product/kernel definitions; one-coordinate boundary iteration; kernel and defect vectors; the norm and Cauchy-Schwarz chain; torus and quadratic-product bounds; the perturbed-product and contradiction bridge; inradius definitions; and final lower/upper theorem statements. The source's explicit definitions and chain match the mathematical mechanism reconstructed here. Selected inspected passages are near lines 133-260, 1919-2025, 2796-2868, 4243-4318, 4540-4828, 4980-5150, 6065-6224, 6330-6468, and 6940-7093 in the local capture. Not every tactic line or dependency was checked. The source file, its imports, its build system, its axiom-reporting commands, and Lean itself were never executed.

4. There is a minor byte-level distinction worth preserving: the frozen local Lean capture has 282,106 bytes and 7,093 LF characters, SHA-256 `f53e12d1c52e6a28e89298eafed24b878f79b1a9c531425c87522a762c10719e`. Its literal Git-blob SHA-1 is `15f64ac6954408f2866cb82866da1673e64a3b2e`. Removing exactly one final LF, without changing any source line, gives 282,105 bytes, SHA-256 `0d643fc771036648cc05476ef1688eee02285b4cb7dbb092072a055e72d034d0`, and Git-blob SHA-1 `efc244f5d31674970b4ea0370b20c31955c779ea`, exactly the source identity stated in the candidate. This audit verified these hashes directly using the Git blob header formula, without invoking Git. The frozen capture must not be described as literally byte-identical to the stated upstream blob without this one-byte qualification. No change to the candidate's mathematical proof follows from it.

5. On October 11, 2026, direct read attempts to https://www.erdosproblems.com/1039 and https://www.erdosproblems.com/forum/thread/1039 returned HTTP 403. The linked Price Overleaf project, https://www.overleaf.com/project/69fba41e9e7830016040c90e , was inaccessible through the reading tool. Thus I did not independently read the live forum or the Overleaf proof PDF, and cannot certify their current contents or the problem website's current status. Attribution is supported here by the inspected Kitamura README/source and the frozen candidate, with this limitation made explicit.

The independently authored proof below is the basis of mathematical acceptance. Source inspection establishes scope and credit, rather than substituting a software claim for the proof.

## 1 The kernel estimate with all conjugations fixed

Let u_1,...,u_n satisfy |u_i| < 1. Define

S = sum over i,j of 1/(1 - u_i conjugate(u_j)),
P = product over i of |u_i|^2.

We prove S is real and S >= n^2/(1-P). Since n >= 1 and every |u_i| < 1, the denominator 1-P is strictly positive, including when a u_i is zero.

Use H^2 with inner product <a,b> = sum a_k conjugate(b_k), linear in the first variable. For k_u(w) = sum_{k>=0} conjugate(u)^k w^k, absolute convergence/Cauchy-Schwarz gives <h,k_u> = h(u). Set

B(w) = product_i (w-u_i)/(1-conjugate(u_i)w),
Lambda = B(0),
g = 1 - conjugate(Lambda) B,
h = sum_i k_(u_i).

Every denominator of B stays nonzero in a neighborhood of the closed unit disk. On |w|=1, each factor has modulus one, so Parseval gives ||B||^2 = 1. It also gives <B,1> = Lambda and <1,B> = conjugate(Lambda). Consequently

||g||^2 = 1 + |Lambda|^2 - |Lambda|^2 - |Lambda|^2 = 1-P.

The conjugate on Lambda is essential. Also B(u_i)=0 for every listed root, irrespective of repetitions, so <g,h> = sum_i g(u_i) = n. Finally,

||h||^2 = sum_{i,j} 1/(1 - conjugate(u_i)u_j) = S,

where the final equality just swaps the finite indices. In particular S is real and nonnegative. Cauchy-Schwarz proves n^2 <= (1-P)S and hence the claim. There is no singular Gram-matrix inversion or distinct-root assumption. Parseval here only concerns rational functions analytic beyond the unit circle, so no radial boundary-value theorem is being assumed.

## 2 The off-diagonal product on the entire polydisk

For 0<a<1 and |x_i|<=1, write

T(x,a) = product over i!=j of |1-a x_i conjugate(x_j)|.

We claim

T(x,a) <= (1+a+...+a^(n-1))^n.                                      (A)

First suppose |x_i|=1. Let

G(a)=n log(1-a^n)-sum_{i,j} log |1-a x_i conjugate(x_j)|.

No logarithm has a zero argument: |a x_i conjugate(x_j)|=a<1. For any fixed complex xi with |xi|=1,

a d/da log|1-a xi| = -Re(a xi/(1-a xi)).

The n^2 constant terms from a xi/(1-a xi) = 1/(1-a xi)-1 therefore give

a G'(a) = sum_{i,j} Re[1/(1-a x_i conjugate(x_j))] - n^2/(1-a^n).

Applying Section 1 with u_i=sqrt(a)x_i, so P=a^n, gives G'(a)>=0. All sums are finite, and G(a) tends to zero as a tends to zero from the right. For any 0<b<a, G(a)>=G(b); letting b decrease to zero proves G(a)>=0. Exponentiating yields

product_{i,j}|1-a x_i conjugate(x_j)| <= (1-a^n)^n.

The diagonal factors equal (1-a)^n on this torus; dividing gives (A).

For arbitrary points in the closed disk, pair conjugate factors to get

T(x,a) = product_{i<j}|1-a x_i conjugate(x_j)|^2.

With all coordinates except x_k fixed, this equals a fixed nonnegative number times

|product_{j!=k}(1-a x_k conjugate(x_j))|^2.

It is the squared modulus of a polynomial in x_k, not an unjustified holomorphic expression in x_k and conjugate(x_k). By the ordinary maximum-modulus principle and compactness, replace x_k by a boundary point without decreasing T. Iterating for k=1,...,n reaches the torus while keeping all coordinates in the disk. This proves (A).

The off-diagonal restriction is essential. The corresponding full-product bound on the entire polydisk would be false: with n=2 and x_1=x_2=0 its left side is 1 and its proposed right side would be (1-a^2)^2<1. The candidate correctly avoids this trap.

## 3 Exact quadratic separation estimate

For A>0, sigma>0, |v_i|<=A, define

Q(v,sigma)=product_{i<j} (|v_i-v_j|^2+sigma^2).

Let alpha=arsinh(sigma/(2A)) and a=exp(-2alpha), so 0<a<1 and

sigma^2/A^2 = (1-a)^2/a.

For |x|,|y|<=1, direct expansion, with the cross term -2 Re(x conjugate(y)) cancelling, gives

|1-a x conjugate(y)|^2/a - |x-y|^2 - (1-a)^2/a
= (1-a)(2-|x|^2-|y|^2) + a(1-|x|^2)(1-|y|^2) >= 0.     (B)

Set v_i=A x_i, multiply (B) over all unordered pairs, and use (A). The number of those pairs is m=n(n-1)/2. Thus

Q(v,sigma) <= A^(n(n-1)) a^(-m) ((1-a^n)/(1-a))^n.

Since

(1-a^n)/(1-a) = exp(-(n-1)alpha) sinh(n alpha)/sinh(alpha),

its exponential factor after the n-th power cancels a^(-m)=exp(n(n-1)alpha), exactly. We obtain

Q(v,sigma) <= A^(n(n-1)) [sinh(n alpha)/sinh(alpha)]^n.   (C)

There is no missing square in (A) or (B), and no missing A exponent. When n=1, both sides of (C) are 1; for sigma>0 the hyperbolic denominator is nonzero. Coincident and boundary points pose no issue. Neither a=1 nor sigma=0 is divided by in the proof.

## 4 Perturbing all listed roots

Let f(z)=product_i(z-z_i), |z_i|<=1, t>0, and |w_i-z_i|<=t. Put

V=product_i |f(w_i)|.

The diagonal factors in the distance matrix have product at most t^n. For i<j, expansion gives the exact complex identity

(w_i-z_j)(w_j-z_i)
= (w_i-z_i)(w_j-z_j) + (w_i-w_j)(z_j-z_i).

Let d=|w_i-w_j| and e=|z_i-z_j|. The triangle inequality and then the nonnegative identity

(d^2+t^2)(e^2+t^2)-(de+t^2)^2=t^2(d-e)^2

give

|w_i-z_j| |w_j-z_i| <= t^2+de <= sqrt((d^2+t^2)(e^2+t^2)).

All factors are nonnegative, so multiplication is legitimate even when some factor vanishes. It follows that

V <= t^n sqrt(Q(w,t)Q(z,t)).                            (D)

We have |w_i|<=1+t. Apply (C) with A=1 and A=1+t. Put alpha=arsinh(t/2), beta=arsinh(t/(2(1+t))). Taking the nonnegative n-th root in (D), then using sinh(alpha)=t/2 and sinh(beta)=t/(2(1+t)), gives exactly

V^(1/n) <= 2(1+t)^(n/2) sqrt(sinh(n alpha)sinh(n beta)). (E)

For s>=0, arsinh(s)<=s, since its derivative is 1/sqrt(1+s^2)<=1 and its value at zero is zero. Also log(1+t)<=t and sinh is increasing on the nonnegative real axis. In particular alpha<=t/2 and beta<=t/2. Thus

V^(1/n) <= 2 exp(nt/2)sinh(nt/2)=exp(nt)-1,
V <= (exp(nt)-1)^n.                                    (F)

This is valid for all real t>0, not just t of order 1/n. It introduces neither floating-point approximations nor a hidden small-parameter asymptotic. For n=1 the underlying product is simply |w_1-z_1|<=t<=exp(t)-1, in agreement with the formula.

## 5 Uniform disks and the strict endpoint

Take any 0<t<(log 2)/n. For each root index i the continuous function |f| attains a maximum M_i on the compact closed disk centered at z_i of radius t. Choose a maximizing w_i. If all M_i>=1, then V=product M_i>=1, contradicting (F), since exp(nt)-1<1. Hence some M_i<1, and the entire closed root-centered disk of radius t lies in the strict lemniscate. This proves rho(f)>=t for all such t and therefore rho(f)>=(log 2)/n.

For an actual open disk at endpoint R=(log 2)/n, choose an increasing sequence 0<t_j<R tending to R. Each t_j has a successful index from the finite set {1,...,n}. At least one index i occurs on an infinite subsequence; that subsequence still tends to R. If |w-z_i|<R, then |w-z_i|<=t_j for some successful j in the subsequence, so |f(w)|<1. Thus B(z_i,R) is contained in the strict lemniscate.

This does not use the false implication that a limit of strict inequalities is strict, and it does not assume that the successful root is initially independent of t. It also does not assert that the corresponding closed endpoint disk is contained in the strict lemniscate. The supremum definition needs only the preceding lower bound; the subsequence argument gives the stronger open-disk existence stated in the candidate.

## 6 The root-of-unity upper witness

Let p_n(z)=z^n-1. Its roots all lie on the unit circle. For w in E_n={|p_n|<1}, the triangle inequality gives |w|^n<2, and w is nonzero because |p_n(0)|=1.

If 0<|w|<=1, consider all 2n rays of arguments (2k+1)pi/(2n), for k=0,...,2n-1. Consecutive rays are separated by pi/n, so one is within angular distance delta<=pi/(2n) of w. Choose q on that ray with |q|=|w|. Then Re(q^n)=0, so |q^n-1|^2=1+|q|^(2n)>=1. Moreover

|q-w| = 2|w|sin(delta/2) <= |w|delta <= pi/(2n).

If |w|>1, choose q on the same radial ray with |q|=2^(1/n). By the reverse triangle inequality, |q^n-1|>=|q|^n-1=1. Also

|q-w|=2^(1/n)-|w|<2^(1/n)-1<=1/n<pi/(2n).

Here (1+1/n)^n>=2 follows from the first two binomial terms, proving 2^(1/n)<=1+1/n. This includes n=1, where the binomial comparison is an equality.

Every point of E_n is therefore within distance pi/(2n) of its complement. If an open disk of radius r>pi/(2n) lay in E_n, its center w would lie in E_n and the constructed q would lie strictly inside that disk while outside E_n, a contradiction. Hence rho(p_n)<=pi/(2n), and R_n<=pi/(2n). No connectedness or radial convexity of E_n was assumed.

## 7 The exact maximum inradius

For any monic degree-n polynomial f, without a root-location condition, suppose an open disk centered at c of radius R>1 lies in {|f|<1}. Fix 1<r<R. The entire circle |z-c|=r is in that strict lemniscate. Compactness and continuity give M=max_{|z-c|=r}|f(z)|<1. The coefficient of (z-c)^n in f is 1 because translation preserves the leading coefficient. Cauchy's coefficient formula yields

1 <= M/r^n < 1,

which is impossible. Thus rho(f)<=1. The admissible polynomial z^n has {|f|<1} equal to the open unit disk and rho(f)=1, proving the maximum and hence the supremum are exactly 1. Every n>=1 is included.

## Adversarial coverage and bounded checks

The decisive proof obligations were checked independently in Sections 1-7. In particular:

- Repeated roots never require an invertible matrix, nonzero discriminant, or distinct kernel vectors.
- Boundary roots are allowed in every geometric/product step; only the auxiliary Hardy points are made strictly interior by multiplication by sqrt(a).
- n=1 is covered throughout, and n=0 is outside the theorem. Empty pair products equal 1.
- Parameters satisfy A>0, sigma>0, 0<a<1 at every division or logarithm. The only endpoint limit a->0 is of a continuous finite expression; no a->1 passage is required.
- The product maximum step uses independent maximizing points on all n disks, not an unjustified common maximizer.
- The original strict c/n wording follows with a smaller fixed c, while the candidate's non-strict log(2)/n bound and open endpoint disk are valid as written.
- The witness bounds distances to the actual complement of the strict sublevel set; equality |p_n(q)|=1 is sufficient.
- The leading coefficient estimate uses compact circles strictly inside an assumed disk, ensuring M<1.

The independently authored diagnostic checker uses only Python's standard library and exact rational Gaussian arithmetic. It checks the kernel inequality for every list of length 1 through 4 from six interior rational points; the off-diagonal inequality for every list of length 1 through 4 from eight closed-disk rational points at four a values, including a=1/1000 and 999/1000; the exact separation identity; the quadratic-product estimate; the squared perturbed-product chain for deterministic lists through n=6 with t from {1/1000,1/5,1,3}; the cross-factor identity; the scalar pairing identity; and the binomial upper-witness bound through n=256. Repetitions, zeros, and boundary roots are intentional. Hyperbolic expressions in the bounded checks are evaluated as exact rational polynomials after taking the indicated n-th power; exp, logarithms, and numerical tolerances are not used.

Three explicit negative controls reject an invalid full-product polydisk extension, a missing conjugation in the defect function, and a missing disk-radius scale. They are tests of the checker's discrimination, not defects in the candidate.

A successful run contains 39,357 exact checks. The proof covers all allowed inputs; these finite checks are corroboration, not a substitute for analytic arguments, a formal proof, or an exhaustive verification over the continuum. The diagnostic checker was run in normal Python mode and both optimization modes (-O and -OO), with JSON receipts. All three modes agreed, confirming that these checks do not disappear under optimization. The checker uses explicit exceptions and no Python assert statements.

## Acceptance and residual work

Accept the frozen candidate as a complete conventional proof of the stated positive c/n and sharp-order result, with the endpoint disk and maximum-inradius assertions included. No mathematical patch is needed. Carry forward the one-terminal-LF provenance clarification when describing exact source identities.

Keep the exact limiting constant, existence of a limit for n R_n, external acceptance/current website status, and compilation/axiom certification of the Lean development outside this acceptance. Those were not established here. All new mathematics and bounded diagnostic checks in this audit were independently authored; no source-author program was run.
