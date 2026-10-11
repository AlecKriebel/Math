# Independent audit of conditional exact additive rigidity

## 1. Verdict and exact original audited

**ACCEPTED, with no mathematical correction required, at the stated conditional scope.**

Acceptance covers Lemmas 1–2, Theorem 3, Corollary 4, and the mathematical boundary examples. The original report SHA-256 is 36d97fbda23153404efb551edf1463df325d2164c1fd34eea16bb1b1cf043778 (16,567 bytes). The candidate manifest SHA-256 is f7b02329f535a23f44b2b9e6c5e7731f33c0aa3998767dc1f21bbbe384557011 (3,000 bytes), listing 17 payload members and excluding itself. The original audit SHA-256 is 3c9a8e965cab220dbb22aebe0528b658f820d9b47b0f9697699ee9b2bf8ccce6 (19,550 bytes); its manifest SHA-256 is 1dbc302782f085dba62915bdc5b3e2cfe86b25652ae8332782c2b52db1d0cee3, listing 24 payload members and excluding itself.

The unrestricted EP 1122 / 2503 problem remains unresolved by this work. The audit does not establish that density-zero decreases imply periodic residual approximation, the sufficient weighted prime-tail condition, or absolute vanishing-error approximation. No unrestricted counterexample or novelty is claimed.

The proofs below were independently reconstructed in the original audit and are retained in full. Candidate Python was not imported or executed; finite checks provided supporting arithmetic and integrity evidence only. This edited audit is bound to the original and to the distributed proof by ACCEPTANCE.json. Editorial removals concern workflow and accounting, not mathematical corrections.

## 2. Definitions and quantifiers

An ordinary real additive function is a map f from the positive integers to the finite real numbers such that f(ab)=f(a)+f(b) whenever gcd(a,b)=1. The identity f(1)=0 follows by setting a=b=1. Its values at different powers of one prime are not required to have any relation.

For a set E, write d*(E)=limsup as N tends to infinity of |E intersect [1,N]|/N. A sequence h converges in density to a finite real number a if d*({n: |h(n)-a|>t})=0 for every t>0.

Periodic approximation in density means that for each t>0 there is a finite-valued real periodic sequence a_t with d*({n: |h(n)-a_t(n)|>t})<t. The period and range may depend arbitrarily on t. Neither h nor the family of approximants is required to be uniformly bounded. Each fixed approximant is bounded because it has finitely many values.

The theorem concerns one **fixed** real c and the ordinary additive residual h(n)=f(n)-c log n. A different slope chosen at each N does not define this one residual and is not covered by the proof.

## 3. Independent proof of the lifting statements

### 3.1 Density convergence of an additive function lifts to exact zero

Suppose h is ordinary additive and converges in density to a finite a. Fix an integer m>=2 and a tolerance t>0. Let E_t={n: |h(n)-a|>t}. The number of n<=N/m coprime to m is

(phi(m)/m) floor(N/m) + O_m(1) = (phi(m)/m^2) N + O_m(1).

This is a positive constant times N for fixed m. At most |E_t intersect [1,N/m]|=o(N) such n have n in E_t. At most |E_t intersect [1,N]|=o(N) have mn in E_t, since n maps injectively to mn. Thus at least one coprime n satisfies both |h(n)-a|<=t and |h(mn)-a|<=t for all sufficiently large N. Additivity on this coprime pair gives

|h(m)| = |h(mn)-h(n)| <= 2t.

The number h(m) is independent of N and t, so h(m)=0. This applies separately to each m; it does not require uniform exceptional-set control for a growing collection of dilations. Together with h(1)=0 it gives h identically zero, and uniqueness of the finite density limit gives a=0.

This proof uses no assertion that a density-one set contains any predetermined integer m. It uses the positive density of suitable witnesses n instead. It also does not assume that h(mn)=h(m)+h(n) for noncoprime n.

### 3.2 Absolute vanishing error allows a changing slope and offset

Suppose E_N is a set of o(N) exceptions in [1,N], e_N tends to zero, and outside E_N,

|f(n)-lambda_N log n+eta_N| <= e_N.

For fixed m, the same coprime witness count supplies n,mn outside E_N. Subtracting the two displayed approximations cancels eta_N exactly and yields

|f(m)-lambda_N log m| <= 2 e_N.

With m=2, lambda_N tends to c=f(2)/log 2. For each other fixed m, passage to the limit gives f(m)=c log m. This proves the candidate's Lemma 2 without any monotonicity assumption. Under these absolute-error hypotheses, the offset is not an obstruction. The error's absolute scale is essential.

## 4. Independent proof of the conditional theorem

Assume ordinary additivity, d*(D)=0 for D={n: f(n+1)<f(n)}, and periodic approximation in density for h=f-c log with a fixed c.

### 4.1 The bounded transform has zero mean total variation

Set u(n)=arctan(h(n)). Then -pi/2<u(n)<pi/2. For n outside D,

h(n+1)-h(n) >= -c log(1+1/n) >= -|c|/n.

The second inequality is valid for either sign of c. Monotonicity and the 1-Lipschitz property of arctan give

(u(n)-u(n+1))_+ <= |c|/n outside D.

Every downward increment is at most pi, including on D, however large the untransformed residual is. Consequently the mean downward variation is at most

pi |D intersect [1,N]|/N + (|c|/N) sum_(n<=N) 1/n,

which tends to zero. The mean signed increment is (u(N+1)-u(1))/N, which also tends to zero by boundedness. The identity |x|=x+2(-x)_+ now gives

(1/N) sum_(n<=N) |u(n+1)-u(n)| -> 0.                         (A)

For any **fixed** integer j>=0, telescope u(n+j)-u(n) into j one-step increments and apply the triangle inequality. Shifting a bounded finite sum changes its normalized mean by O_j(1/N). Thus

(1/N) sum_(n<=N) |u(n+j)-u(n)| -> 0.                         (B)

There is no assertion here for j=j(N) tending to infinity. No integrability or boundedness assumption on h was used.

### 4.2 Periodic approximation removes all nonconstant transformed behavior

For bounded sequences w define the mean seminorm

||w|| = limsup_(N->infinity) (1/N) sum_(n<=N) |w(n)|.

The triangle inequality holds. For each fixed j, shifting w by j preserves this seminorm: the difference between the two finite means is at most 2j sup|w|/N.

Choose an approximant a to h at tolerance t and put v=arctan(a). The sequence v is bounded and periodic. On the good set |u-v|<=t; on the bad set |u-v|<=pi. Hence

||u-v|| <= t + pi d*({|h-a|>t}) <= (1+pi)t.                   (C)

Let q be the period of this one v, and let C_v be its average over a full period. Define T_q w(n)=q^(-1) sum_(j=0)^(q-1) w(n+j). Then T_q v=C_v exactly. Equation (B), used for only finitely many fixed shifts after v has been chosen, gives ||u-T_q u||=0. The seminorm triangle inequality and fixed-shift invariance give

||u-C_v|| <= ||u-T_q u|| + ||T_q(u-v)|| <= ||u-v||.           (D)

The bound has no factor growing with q. In particular, no assumption such as q(t)t tending to zero is hidden in the argument. The limiting procedure first fixes t and its period, then lets N tend to infinity.

Choose t_k tending to zero and obtain constants C_k with ||u-C_k|| tending to zero. For every k,l,

|C_k-C_l| <= ||u-C_k|| + ||u-C_l||.

Therefore C_k converges to a real C and ||u-C||=0. Markov's inequality for the nonnegative sequence |u-C| shows u tends to C in density. Since all C_k are averages of arctangents, initially C is known only to lie in the closed interval [-pi/2,pi/2].

### 4.3 Tightness excludes escape to either endpoint

Choose one approximant a at tolerance 1/4 and let M=max |a|. On a set of lower density greater than 3/4,

|h(n)| <= M+1/4, so |u(n)| <= b:=arctan(M+1/4)<pi/2.

If C=pi/2 or C=-pi/2, this positive-density set would have |u(n)-C|>=pi/2-b>0, contradicting convergence in density. Thus C lies strictly inside the arctangent range.

Continuity of tan at this one interior C supplies, for every epsilon>0, a delta>0 such that |u-C|<delta implies |h-tan C|<epsilon. It follows that h converges in density to the finite tan C. There is no global Lipschitz assertion for tan and no invalid inversion at infinity.

The residual h is ordinary additive because log is completely additive and c is fixed. Section 3.1 gives h identically zero. Therefore f(n)=c log n for every positive integer. If c<0, every n is a strict decrease, contrary to d*(D)=0. Hence c>=0. This proves the full candidate Theorem 3.

## 5. Independent proof of the prime-tail corollary

Assume, for the same fixed c,

sum over primes p of min(1,|h(p)|)/p < infinity.

No restriction is imposed on h(p^k), k>=2, beyond each being a finite real number. Ordinary additivity gives the exact finite decomposition h(n)=sum_(p^k exactly divides n) h(p^k).

Fix a target tolerance epsilon>0. For a prime cutoff P define

L(P)=sum_(p>P, |h(p)|>1) 1/p,
S(P)=sum_(p>P, |h(p)|<=1) |h(p)|/p,
Q(P)=sum_(p>P) 1/p^2.

All three tend to zero. For every N the proportion of n<=N divisible by any large prime in the first sum is at most L(P), using floor(N/p)/N<=1/p. The proportion divisible by p^2 for some p>P is at most Q(P). These estimates are uniform in N; for each finite N only finitely many primes can divide n or have p^2<=n. The convergent sums dominate the resulting finite union bounds.

Off these two exceptional sets, every omitted prime power has exponent exactly one and |h(p)|<=1. Its total absolute contribution is bounded by

T_P(n)=sum_(p>P, |h(p)|<=1, p divides n) |h(p)|.

For every N,

(1/N) sum_(n<=N) T_P(n) <= S(P).

Markov gives proportion at most S(P)/epsilon for T_P(n)>epsilon. This estimate requires no cancellation between primes and no moments of the higher prime-power values.

Choose P so that L(P)+Q(P)+S(P)/epsilon<epsilon/2. For the finitely many p<=P choose a common K>=2 with sum_(p<=P) p^(-K)<epsilon/2. Define a(n) by retaining the term h(p^k) precisely when p<=P and 1<=v_p(n)=k<K, and using zero for v_p(n)=0 or v_p(n)>=K. Each such contribution is determined by n modulo p^K. Thus a is periodic modulo the finite product of p^K for p<=P, and its finitely many values are finite even if the omitted prime-power values are arbitrarily large.

The untruncated small-prime sum differs from a only if p^K divides n for some p<=P, a set of upper density at most sum_(p<=P) p^(-K). Combining all the bounds gives

d*({n: |h(n)-a(n)|>epsilon}) < epsilon.

This proves periodic approximation in density and hence the candidate Corollary 4. The order of choices is epsilon, then P, then K, followed by the density limit. No bound on the approximant's amplitude, no simultaneous infinite truncation, and no complete additivity are smuggled in.

In particular, a residual may vanish at every prime while having nonzero values at infinitely many higher prime powers. It still satisfies the approximation lemma. Under the density-zero-decrease premise, the theorem then forces those higher values to vanish exactly. The large-prime square bound and the finite-small-prime valuation bound are both necessary parts of this reasoning.

## 6. Boundary examples and overclaiming controls

1. Let h(n)=1 when n is even, and h(n)=0 otherwise. It is ordinary additive: at most one factor in a coprime product is even. It is not completely additive because h(4)=1 whereas 2h(2)=2. For g(n)=log n+h(n), the absolute residual is bounded by 1 and its prime-power squared residual sum is sum_(2^k<=N) 2^(-k)<1. Yet g is not a logarithm.

   Also B_g(N)^2=sum_(p^k<=N) |g(p^k)|^2/p^k tends to infinity, since its prime terms dominate (log 2)^2 sum_(p<=N) 1/p. The reciprocal-prime sum diverges: if it converged, the finite Euler products product_(p<=y)(1-1/p)^(-1) would stay bounded, whereas their expansions include every term 1/n for n<=y. Thus the bounded residual and bounded squared residual sum are negligible at the source's respective normalized scales. This establishes the claimed obstruction to upgrading normalized error alone.

   The decrease set of g is exactly the even integers: the logarithmic increment is in (0,1), while h changes by -1 on even n and by +1 on odd n. Its density is 1/2. It is explicitly not a counterexample to the target or to the conditional theorem.

2. For h(n)=A 1_(v_p(n)=k), with k>=1 and A=+1 or -1, the residual is ordinary additive. If A=+1, decreases of log+h occur exactly when v_p(n)=k. If A=-1, they occur exactly when v_p(n+1)=k. In a full period p^(k+1), there are exactly p-1 such residues. The density is (p-1)/p^(k+1), positive however small it can be made. The candidate's distinction between exact exponent k and arbitrary divisibility by p is correct.

3. The scalar function lambda(X)=log log log X diverges, but for each fixed u>0,

   lambda(X^u)-lambda(X)=log(1+log(u)/log log X) -> 0.

   Thus even an absolute slow-variation statement of this kind does not imply a fixed limiting slope. This is a scalar control, not an additive-function example.

4. The residual h(n)=log n has transformed variation tending to zero in mean and u(n)=arctan(log n) tending to pi/2. It cannot be periodically approximable in density: for every real periodic a and every fixed tolerance, all sufficiently large n lie outside that tolerance. It therefore tests exactly the endpoint/tightness issue, and cannot be used to drop the periodic approximation premise.

None of these examples proves that the unrestricted conjecture is false. They instead identify invalid implications a proof must avoid.

## 7. Historical source comparison and dependency boundary

During the original audit, the two retained complete PDFs and their text extractions were byte-pinned. The auditor independently re-extracted the PDFs with the installed pdftotext layout mode, reproducing both retained text files byte for byte. Visual inspection of Erdős's printed page 3 verified the target's density-zero and ordinary-additive scope; visual inspection of Mangerel's printed page 6 verified Theorem 1.9's normalization and scale-dependent parameters. Further reading of the retained text covered the definitions, relevant introductory statements, Lemma 7.5 and formula (25), Proposition 7.1's statement and relevant proof, and the complete concluding proofs of Corollary 1.7 and Theorem 1.9, including Corollary 7.8.

- Paul Erdős, *On the distribution function of additive functions*, Annals of Mathematics 47(1) (1946), 1–20. Public source: https://users.renyi.hu/~p_erdos/1946-06.pdf. Page 1 defines additivity for coprime arguments; page 3 distinguishes the almost-everywhere monotonicity conjecture from the neighboring density-one small-difference conjecture. The candidate identifies the correct one.
- Alexander P. Mangerel, *Additive functions in short intervals, gaps and a conjecture of Erdős*, arXiv:2108.12351v1, 27 August 2021. Public source: https://arxiv.org/abs/2108.12351v1. The version is pinned; this audit makes no assertion about later revisions or present literature status.
- Corollary 1.7 uses complete additivity, a normalized large-prime-value variance-tail condition, and |B(X)| bounded by a constant times X/(log X)^(2+delta). Its concluding proof reaches absolute averaged gap o(1) and invokes the separately quoted Kátai–Wirsing characterization. It does not establish the unrestricted statement audited here.
- Theorem 1.8 is restricted to A_s, whose definition includes divergent B_g, negligible higher-prime-power contribution relative to B_g squared, and the stated normalized prime-tail condition. Its conclusion is variance-relative prime-power approximation, with scale-dependent slowly varying slope. These restrictions are not removed by the candidate.
- Theorem 1.9 allows ordinary additivity and density-zero decreases, but gives a scale-dependent slope and offset, with an error o(B_g(X)) on all but o(X) integers. Its final proof does not turn that error into o(1).
- Formula (25) bounds the mean absolute gap by a constant times B_g(X) multiplied by sqrt(|B(X)|/X)+log X/sqrt X. Density zero makes the multiplier tend to zero; it does not by itself show that the entire product tends to zero.

The source uses {n: g(n)<g(n-1)} after defining g(0)=0; the candidate uses {n: f(n+1)<f(n)}. These are shifted versions, up to a harmless initial term, and have the same asymptotic density condition.

These are source-scope comparisons, not independent certifications of the external papers' complete proof chains. In particular, neither Kátai–Wirsing nor the analytic machinery cited by Mangerel is a dependency of Sections 3–5 above. No inference is made about whether an earlier author truly inspected every source passage their historical report says they inspected. The audit independently verifies the mathematical scope relevant here.

No new source inspection occurred during edition preparation. The complete PDFs and extracted text are excluded from this edition. Source hashes and history identify the material considered earlier; they do not assert a full audit of the external papers or a new assessment of later literature.

## 8. Independent computational checks and limitations

The audit's own standard-library code performs:

- Exact verification of all 17 candidate members against the externally supplied manifest hash, including file-set equality.
- Independent residue-congruence reconstruction of all 24 candidate isolated-prime-power examples and their exact rational densities, plus independent recomputation of the candidate's stated numerical pair, cycle, and dilation certificate fields in all three retained modes. It does not execute the candidate checker or certify its historical run merely because its output says PASS.
- 729 exact rational bounded-sequence variation checks, including fixed-shift triangle bounds.
- 1,364 exact period-average contraction checks.
- 16,388 exhaustive small finite bad-set/coprime-dilation checks.
- 555 coprime-pair checks for a genuinely non-completely-additive function with large freely assigned prime-power values.
- 512 valuation-truncation periodicity and error-support checks.
- 27 exact finite tail-mean and Markov checks.
- Eight rejected mathematical overclaiming controls.
- Fifteen adversarial inventory controls, including wrong pins, altered members, added/missing files, duplicate/unsafe paths, member/ancestor/unlisted symlinks, malformed metadata, and incorrect counts.

The independent checks run under normal Python, -O, and -OO. They use explicit exceptions rather than assert statements. Candidate Python is parsed only as inert text to inspect its use of assertions; it is never imported or run. All arithmetic supporting checks are integral or rational. The logarithmic increment sign is justified mathematically, not estimated in floating point.

The complete acceptance is based on the self-contained proofs, not on extrapolation from these finite tests. Hashes establish identity and integrity, not mathematical truth. A passing control verifies the audited checker behavior for that adversarial case, not every possible malicious program or filesystem.

## 9. Disposition

No mathematical amendment was required. The correct status is accepted conditional partial result; unrestricted EP 1122 / 2503 unresolved by this work. The full written proofs and examples are retained, while executable programs, raw certificates, copied third-party sources, and private coordination are excluded. Historical mathematical checks are summarized rather than rerun or distributed here. The publication manifest names exactly eight authored files and hashes the other seven, excluding its own hash; its digest is separately pinned by the proposed publication body.

## Publication and review boundary

This AI-assisted work is unrefereed. Acceptance means an independent internal AI audit of the original report and its separately retained supporting checks. No external human peer review, journal acceptance, or formal proof-assistant certification is claimed. No mathematical correction was required.

The authored conditional theorem, lifting lemmas, prime-tail corollary, and boundary examples are fully proved in this edition. Their proofs are self-contained and do not depend on omitted computational certificates or external analytic theorems. Finite checks are supporting tests, not proofs of asymptotic implications. The edition omits executable code, raw computational certificates, copied source text and PDFs, and private coordination material. Hashes establish identity and integrity, not mathematical truth.

The unrestricted EP 1122 / 2503 problem remains unresolved by this work. No counterexample to that unrestricted problem, novelty, priority, or exhaustive current literature-status claim is made. Historical source inspection and independent audit are distinguished from edition preparation: no new scholarly-source retrieval or inspection and no new mathematical computation were performed for this edition. Local packaging checks establish the identities and scope of the distributed files only.
