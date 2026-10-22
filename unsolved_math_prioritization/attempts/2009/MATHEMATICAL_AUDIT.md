# EP252: independent mathematical and static-source audit

Audit date: 10 October 2026. Attribution: the argument audited below is the prior public claim of Tokengrinder. This report does not claim a new proof or a new solution.

## Publication edition and historical evidence

This AI-assisted authored mathematical and static-source audit is unrefereed. No external human peer review, journal acceptance, or independent formal proof-assistant certification is claimed. All seven steps of the complete mathematical reconstruction are preserved without mathematical changes. Inspection and finite-test statements below describe the recorded audit, not new scholarly-source inspection or mathematical test execution during edition preparation. This prose-only edition distributes authored analysis and public verification metadata, with no copied source documents, source excerpts, Lean or library code, executable checks, detailed test outputs, or datasets.

**FORMAL REPRODUCIBILITY HOLD remains in force.** Mathematical PASS within the stated scope does not clear the independent Lean build, transitive compiler/dependency/kernel closure, or axiom-report requirements.

## Disposition

**Mathematical inspection: PASS within the stated scope. Formal reproducibility: HOLD.**

The inspected argument gives an unconditional proof for every positive integer exponent, and a separate proof for exponent zero. The complete manuscript and complete main Lean source were read. No mathematical gap was found in the argument reconstructed below. In particular, the crucial progressions are ordinary CRT progressions, not progressions required to contain simultaneous primes. The finite grid is fixed after choosing the exponent, so its very large size does not invalidate any limit or finite intersection.

This is not an independent compiled Lean verification. At the recorded audit, neither Lean nor Lake was installed in the audit environment. No external proof code or installation script was run. The author's reports of successful compilation, standard axiom dependencies, and fresh-kernel replay remain author reports. The transitive library and compiler closure was not rebuilt or independently kernel-checked. Those facts prohibit describing this audit as full formal acceptance or as external journal/referee acceptance. The formal reproducibility hold remains in force pending independent compiled verification and its required evidence.

## Exact object and historical scope

For integer k >= 0, write sigma_k(n) = sum of d^k over positive divisors d of n, for n >= 1. Define sigma_k(0)=0 solely to match the formal indexing. The target is

    alpha_k = sum_{n=1}^infinity sigma_k(n)/n!.

The inspected theorem quantifies over every natural k, with no extra mathematical hypothesis. Its sum starts at zero, but the zero summand vanishes. The independently fetched mathlib definition is the ordinary positive-divisor sum. Its definition of irrational means exclusion from the image of the rational numbers in the reals. Thus neither the summand nor the conclusion is a weakened substitute.

Convergence is elementary: 0 <= sigma_k(n) <= n^(k+1), and n^(k+1)/n! is summable, for example by the ratio test. This proves that the formal totalized infinite sum denotes the ordinary convergent series. Removing the zero term and shifting to n+1 preserves the sum. At k=0, sigma_0(n) is the number of positive divisors, not the identically-one function, and 0^0 never enters a positive-divisor summand.

Erdos's 1988 chapter poses the issue beyond the Erdos–Kac k=1,2 results. Schlage-Puchta and Friedlander–Luca–Stoiciu give unconditional k=3 results and conditional larger-degree results. Pratt's 2022 preprint explicitly proves k=4. These statements were read in full-source PDFs. They establish the inspected historical frontier, not a claim that no intervening paper exists. The present all-degree claim is attributed to Tokengrinder rather than credited to this audit.

## Independent reconstruction of the decisive mathematics

All constants below may depend on the fixed integer k. No uniformity in k is needed.

### 1. Integrality belongs to the actual convergent tail

For n >= 1, set

    T_k(n) = (n-1)! sum_{m=n}^infinity sigma_k(m)/m!.

This is exactly (n-1)! times alpha_k minus its prefix. If alpha_k=a/b is rational, then for n>b the multiple (n-1)! alpha_k is integral, because b divides (n-1)!. Every prefix term is integral after the same scaling because m! divides (n-1)! for m<n. Hence T_k(n) is eventually an integer.

The exact block formula is

    T_k(n+1) = sum_{j>=0} sigma_k(n+j+1)/[(n+1)...(n+j+1)].

All terms are nonnegative and the series converges. Thus splitting it after k+1 terms is legitimate. The construction never replaces this tail by an unrelated sequence that merely has similar formal coefficients.

### 2. The error is small enough after multiplication by n

Put D_h(x)=1/[x(x-1)...(x-h+1)] and S(i,j) for a Stirling number of the second kind. For 0<=j<=k,

    D_{j+1}(x) = sum_{i=0}^k S(i,j)/x^(i+1) + E_j(x).

For x >= k+1, the source's elementary recurrence yields

    0 <= E_j(x) <= (k+1)^(k+1)/x^(k+2).

To check the estimate without appealing to an infinite asymptotic expansion, let P_{j,L}(x)=sum_{i<L}S(i,j)/x^(i+1) and E_{j,L}=D_{j+1}-P_{j,L}. Their exact recurrence is

    E_{j+1,L+1}(x) = [E_{j,L}(x)+(j+1)E_{j+1,L}(x)]/x.

For any H with j+1<=H<=x, induction in L proves 0<=E_{j,L}<=H^L/x^(L+1). The L=0 case uses D_{j+1}<=1/x; the j=0 step is exact; for other j the recurrence has nonnegative coefficients whose sum is at most H. The denominators cleared here are positive in the range used in the theorem.

Pairing complementary divisors gives d(n)<=2 sqrt(n), so sigma_k(n)<=2 n^k sqrt(n). The manuscript uses the harmless weaker constant 64. With x=n+j+1 and j<=k, multiplying the finite remainder sigma_k(x)E_j(x) by n+1 gives O_k(n^(-1/2)). There are only k+1 such terms.

The omitted infinite tail starts at j=k+1. Put d=k+1 and j=r+d. For n>=1, m=n+1+r+d satisfies

    sigma_k(m) <= 64 m^(k+1)/sqrt(n+1),
    m^d (n+1)^(r+1) <= d^d (n+1)^(ascending r+d+1).

The second inequality follows from m<=d(n+r+2), then bounding the first r+1 ascending factors below by n+1 and the last d factors below by n+r+2. Dividing and summing a geometric series bounds the omitted tail by

    64 (k+1)^(k+1) / [n sqrt(n+1)].

Consequently the exact expansion can be written

    T_k(n+1) = M_k(n) + R_k(n),
    M_k(n) = sum_{j=0}^k sum_{i=0}^k S(i,j) sigma_k(n+j+1)/(n+j+1)^(i+1),
    (n+1) R_k(n) -> 0.

This last scaled estimate, rather than just R_k(n)->0, is essential later and is proved with an explicit summable majorant. No unproved exchange of an infinite expansion with a divisor sum is needed.

### 3. Exact progression means, including the k=1 edge

For n>=1 define rho_k(n)=sigma_k(n)/n^k=sum_{d|n}d^(-k). For fixed k>=1 and Q,A>=1, consider the averages along Qj+A. For each positive d, let g=gcd(d,Q). The congruence d|(Qj+A) has no solution if g does not divide A; otherwise it is one class modulo d/g, with density g/d. Therefore the average contribution of divisor d tends to

    m_k(Q,A,d) = 1_{g|A} g/d^(k+1).

An important point is domination of the averages themselves. If C_d(N) counts the relevant j<N, injectivity of j -> Qj+A gives C_d(N)<=floor((QN+A)/d). Hence for N>=1,

    C_d(N)/(N d^k) <= (Q+A)/d^(k+1).

The right side is summable for every k>=1, including k=1. Dominated convergence for series, after interchanging a finite j-sum with the finite divisor supports, establishes

    (1/N) sum_{j<N}rho_k(Qj+A) -> mu_k(Q,A),
    mu_k(Q,A)=sum_{d>=1}m_k(Q,A,d).

This does not use the divergent pointwise majorant sum 1/d at k=1. Also, mu_k(Q,A)>=1 because the d=1 term is one.

For a prime L coprime to Q and B congruent to A modulo Q, direct gcd algebra gives

    mu_k(QL,B) = mu_k(Q,A) [1-L^(-k-1)+1_{L|B}L^(-k)].

Indeed the old summands with L|d have total mu_k(Q,A)/L^(k+1), by the bijection d=Le and gcd(Le,Q)=gcd(e,Q). Upon refining the modulus to QL, those summands are multiplied by L when L|B and deleted otherwise. The remaining terms do not change. Absolute convergence justifies these operations.

Now suppose a finite weighted sum sum_i c_i rho_k(Qn+A+r_i) tended to zero, where all r_i>0 and one shift r_* occurs exactly once with c_* nonzero. Choose a prime L exceeding Q and all the shifts. A residue v_0 with Qv_0+A=0 modulo L misses every shifted argument. A residue v_1 with Qv_1+A+r_*=0 modulo L hits exactly r_*: all the shifts lie strictly between 0 and L, so congruence to r_* is equality. Both subsequences n=Lt+v_h must still tend to zero, hence so must their Cesaro averages. Applying the displayed mean formula and subtracting their limits gives

    c_* mu_k(Q,A+r_*) L^(-k) = 0,

which is impossible. Only the infinitude of ordinary primes is used. Neither simultaneous prime values nor a prime-tuples conjecture appears.

### 4. A fixed grid with coprime multipliers

For k>=1 put b=k+2, F=b^k-1, D=F!, B=1+kDF. Let a vertex e have k digits e_a in {0,...,k+1}, with a=0,...,k-1. Define

    I_e=sum_a e_a b^a,     J_e=sum_a (a+1)e_a b^a,
    p_e=B+D I_e,           t_e=D J_e,
    s_{e,j}=(j+1)p_e-t_e,
    w_e=product_a (-1)^(k+1-e_a) choose(k+1,e_a).

Radix uniqueness gives distinct I_e between 0 and F, and J_e<=kI_e. Thus t_e<B and every s_{e,j}>0; natural subtraction in the formal definition agrees with ordinary subtraction.

Every p_e is 1 modulo D. If a prime divided both p_e and p_f, it would divide D(I_f-I_e). Being coprime to D, it would divide the nonzero difference of indices, which has absolute value at most F. That prime would then divide F!=D, a contradiction. Thus the p_e are pairwise coprime; they need not be prime.

For j<k,

    s_{e,j}=(j+1)B+D sum_a (j-a)e_a b^a

does not depend on the jth digit. Holding all other digits fixed, p_e^ell is a polynomial of degree at most ell in that digit. The binomial weight is a (k+1)st finite difference. It follows, for ell<=k and every function g on the shifts, that

    sum_e w_e p_e^ell g(s_{e,j})=0.

There is also exactly one occurrence of shift (k+1)B among j<=k. If j<k then s_{e,j}<=k(B+DF)=(k+1)B-1. For j=k,

    s_{e,k}=(k+1)B+D[(k+1)I_e-J_e],

and the bracket is at least I_e. Equality therefore forces I_e=0, hence e=0. At e=0,j=k the coefficient w_e p_e^(k+1)S(k,k) is nonzero. In fact w_0=(-1)^(k(k+1))=1 and S(k,k)=1.

### 5. Squared CRT moduli make the divisor rescaling valid

Choose A satisfying A=t_e modulo p_e^2 for every vertex and put Q=product_e p_e^2. The finite CRT applies because these squares are positive and pairwise coprime. For sufficiently large N=A+Qt, set n_e=(N-t_e)/p_e. This is a nonnegative integer divisible by p_e and tends to infinity. Directly,

    p_e(n_e+j+1)=N+s_{e,j}.

Because j+1<=k+1<=F, the number j+1 divides D and is coprime to p_e. Since p_e divides n_e, the same is true of n_e+j+1. Multiplicativity of sigma_k therefore proves, for every i,

    sigma_k(p_e) sigma_k(n_e+j+1)/(n_e+j+1)^(i+1)
       = p_e^(i+1) sigma_k(N+s_{e,j})/(N+s_{e,j})^(i+1).

The square on the modulus is indispensable: a congruence modulo p_e alone does not force n_e divisible by p_e. For example p=5,N=15,t=0,j=1 would instead multiply sigma_1(5) by itself; 36 differs from sigma_1(25)=31. The actual proof uses p_e^2 and does not make this mistake.

### 6. Rationality forces the forbidden limit

Assume alpha_k rational and form the fixed integer-weighted tail

    W(N)=sum_e w_e sigma_k(p_e) T_k(n_e+1).

It is eventually integral. Apply the exact expansion from Step 2 to each n_e and use Step 5 to rescale each term. For i<k, every j<k term vanishes under the grid identity with ell=i+1<=k. The j=k term has S(i,k)=0. Hence only i=k survives:

    W(N)=S(N)+E(N),
    S(N)=sum_{e,j<=k} c_{e,j}rho_k(N+s_{e,j})/(N+s_{e,j}),
    c_{e,j}=w_e p_e^(k+1) S(k,j).

Since n_e grows like N/p_e, the exact identity N=p_e(n_e+1)-s_{e,0}, together with (n+1)R_k(n)->0, gives N E(N)->0. The sum is finite; signed or large coefficients do not change this limit.

The divisor-pairing bound also gives rho_k(n)<=64 sqrt(n). It follows that S(N)->0, so W(N)->0. An eventually integral real sequence tending to zero is eventually zero. Therefore N S(N)=-N E(N)->0 along this CRT progression.

Finally, for a fixed positive shift s,

    N rho_k(N+s)/(N+s)-rho_k(N+s)=-s rho_k(N+s)/(N+s)->0.

Consequently V(N)=sum_{e,j<=k}c_{e,j}rho_k(N+s_{e,j}) tends to zero. Step 4 supplied an isolated shift with nonzero coefficient, while Step 3 prohibits this zero limit on any positive-step arithmetic progression. This is the required contradiction for each k>=1.

### 7. Zero is covered without an invalid harmonic-series mean

At k=0 the exact tail expansion reduces to

    T_0(n+1)=sigma_0(n+1)/(n+1)+R_0(n).

The first term tends to zero by divisor pairing, and the second tends to zero by Step 2. Yet every T_0(n)>0 for n>=1, because its first block term is sigma_0(n)/n>0. Rationality would make this positive sequence eventually integral and thus eventually zero, a contradiction. The progression-mean argument is deliberately not applied at k=0, where the relevant p-series exponent would be one.

## Static Lean and dependency boundary

The complete main source is 60,831 bytes, 1,074 lines, and 89 theorem declarations. Its SHA256 is 784303a58ba3361669a236f5f7c5d38c68c352df8ccd3df9e46cc66149d42569. A fresh fetch at commit 46b9fd26361faf669bcd7e4495e63678bfa6a735 exactly matches the earlier retained bytes. The statement-audit source also matches exactly.

The main source imports ten Mathlib modules and no project-local generalization modules. All ten directly imported source files were independently retrieved at official mathlib revision 0df444a360eaa60ab8c11dca51a86af692955474. Key definitions and theorem interfaces inspected include sigma, Irrational, divisor complement pairing and multiplicativity, p-series summability, dominated convergence for series, finite differences, the Stirling recurrence, residue counts, and finite CRT. Ordinary dependencies are not mathematical assumptions such as Schinzel H.

The main source has no lexical sorry/admit/native_decide occurrences and no custom axiom, opaque, unsafe, elaborator, macro, syntax, or run_cmd declarations. This screen is only a static observation. It does not compute the transitive theorem axiom closure and cannot certify tactic elaboration. The file includes an axiom-print command; its presence does not itself establish what a fresh run would print.

The pin is Lean 4.33.1, and the official mathlib pin's own toolchain agrees. The project manifest fixes mathlib and eight inherited package revisions; all eight exactly match the official mathlib manifest at that revision. Its TOML disables automatic implicit parameters and enables sorry warnings. The manifest and direct source pins were inspected, but all transitive source files, compiler binaries, generated artifacts and imported oleans were not audited. The unrelated Generalizations library is outside this acceptance scope.

VERIFICATION.md says a clean-machine dependency download was not separately tested. README advertises SHA256SUMS, but the pinned repository fetch for that path returned 404. This is a documentation/reproducibility defect, not a counterexample to any mathematical lemma. The source hash printed on PDF page 20 agrees with the retrieved main Lean module regardless of this missing file.

## Historically recorded finite controls and their limits

The independently authored standard-library-only control program historically checked exact rational/integer identities and passed under normal Python, -O and -OO. Its recorded results include fixed-input byte-identity checks, exact equality of the then-fresh pinned Lean and statement-audit bytes, 630 divisor/phase cases, 972 Stirling-error cases, 819 polynomial-tail cases, 7,200 affine-count cases, 16,200 prime-refinement cases, 7,873 pairwise-coprimality checks, and 326 grouped cancellation checks. The complete grids at k=1,2,3 have 3,16,125 vertices. Four negative controls detect removing factorial spacing, squared moduli, signed finite-difference weights, or the prime hypothesis in the refinement identity.

For an easily reviewable instance, k=1 gives multipliers 5,7,9, offsets 0,2,4 and weights 1,-2,1. One CRT progression is N=47875+99225t, and the final phase sum is

    25 rho_1(N+10)-98 rho_1(N+12)+81 rho_1(N+14).

These controls detect implementation/indexing mistakes in bounded instances. They do not prove the universal theorem and do not substitute for a Lean build. The general argument is the mathematical reasoning in Steps 1–7.

## Required evidence to clear the formal hold

In an explicitly authorized isolated environment, obtain the pinned official toolchain and exact dependency revisions; inspect any build hooks before running them. Rebuild the main source from those bytes with no inherited project artifacts and with trust zero, then compile the six statement-audit results against the newly built module. Preserve complete output, tool versions, all relevant source/artifact hashes, and the final theorem's axiom report. The allowed axiom list advertised by the author is propext, Classical.choice, Quot.sound; this audit has not independently obtained that report. A fresh leanchecker replay uses Lean's own kernel and must not be called a second kernel implementation.

No source changes are proposed because no mathematical defect was identified. This is an audit of a credited prior claim, with no new-proof or novelty claim. Edition preparation did not run a new mathematical test, execute Lean or other external proof code, or install software.

## Public primary sources

- P. Erdos, "On the irrationality of certain series: problems and results" (1988), printed p.102: https://renyi.hu/~p_erdos/1988-22.pdf
- J.-C. Schlage-Puchta, "The irrationality of a number theoretical series": https://arxiv.org/abs/1105.1452
- J. B. Friedlander, F. Luca, M. Stoiciu, "On the irrationality of a divisor function series," INTEGERS 7 (2007), A31: https://math.colgate.edu/~integers/h31/h31.pdf
- K. Pratt, "The irrationality of a divisor function series of Erdos and Kac": https://arxiv.org/abs/2209.11124
- Tokengrinder, full proof at the audited commit: https://github.com/tokengr1nder/Erdos252/blob/46b9fd26361faf669bcd7e4495e63678bfa6a735/PROOF.pdf
- Main Lean source: https://github.com/tokengr1nder/Erdos252/blob/46b9fd26361faf669bcd7e4495e63678bfa6a735/Erdos252/Solution.lean
- Statement audit: https://github.com/tokengr1nder/Erdos252/blob/46b9fd26361faf669bcd7e4495e63678bfa6a735/audit/Statement.lean
- Author verification boundary: https://github.com/tokengr1nder/Erdos252/blob/46b9fd26361faf669bcd7e4495e63678bfa6a735/VERIFICATION.md
- Pinned dependency manifest: https://github.com/tokengr1nder/Erdos252/blob/46b9fd26361faf669bcd7e4495e63678bfa6a735/lake-manifest.json
- Official mathlib source revision: https://github.com/leanprover-community/mathlib4/tree/0df444a360eaa60ab8c11dca51a86af692955474
