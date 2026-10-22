# Acceptance of structural Pierce bounds and a separate source correction

## Decision and status

Accept the complete structural partials and scoped published-source correction without material mathematical correction. The CRT theorem's L>=1 hypothesis has been made explicit as the auditor recommended. The four sharp numerical orbits remain exact authored proof constructions. The original structural proof, separate correction, independent verdict, full logical review and full source review are all retained with recorded editorial changes.

This AI-assisted manuscript is unrefereed. Acceptance records an independent internal AI audit, not external human peer review, journal acceptance of this correction, or formal proof-assistant certification.

The original uniform O((log A)^2) question remains unresolved by this work. No novelty, priority, worldwide-openness, or main-theorem refutation claim is made.

This is not a computational reproduction package. Complete authored proofs, the four exact sharpness constructions, and the full independent logical and source review are retained. Raw scan and enumeration datasets, executable code, copied source PDFs and text, rendered source images, and private coordination material are omitted. Historical checks support the written proofs and cannot be reproduced from this edition alone.

All retrieval, inspection, computation and match statements below describe the historical candidate or independent audit of October 11, 2026 UTC. No new mathematical execution or scholarly-source inspection occurred during editorial preparation.

## Exact structural scope

A>B>0 are integers, A is fixed, and P(A,B) counts modulo operations to the first zero. Quotients strictly increase, gcd(A,b_i) divides gcd(A,b_(i+1)), and reduced denominators satisfy D_(i+1)=D_i/gcd(D_i,q_i), with terminal denominator 1. Removing the initial gcd preserves length, but counting gcd changes gives no bound on intervening stretches, including the prime-numerator case.

For a primitive positive k-member arithmetic progression, its LCM is at least k binom(k-1,floor((k-1)/2)), hence at least 2^(k-1). The proof retains the prime-valuation factorial divisibility, final-r-member argument, central-coefficient step, nonprimitive scaling and k=1 boundary.

For an r-periodic decrement block of L steps, phase j has k_j positive pre-transition states, decrement d_j, total-period decrement S and g_j=gcd(c_j,S). Their shared divisor relation gives g_j 2^(k_j-1)<=A+d_j. Consequently L<=sum_j[1+floor(log_2((A+d_j)/g_j))]<=r[1+floor(log_2(2A-1))]. Terminal zero is never an LCM modulus; incomplete final periods are included. The log-squared consequence requires total partition-period sum O(log A), which remains unproved for arbitrary orbits.

For a fixed positive word, S is its sum and G the nonnegative gcd of decrement differences. If k complete copies occur, M_k(S)=lcm{m<=k:gcd(m,S)=1} divides G. If the word is nonconstant, G>0 and the first forbidden modulus is K=min_(p prime,p not dividing S) p^(v_p(G)+1), so k<K. This is necessary, not sufficient for realization. The four exact sharpness constructions and their least numerators/CRT moduli remain in the proof and audit; they are mathematical certificates, not raw enumeration tables. Constant words are treated separately by the credited Erdős–Shallit construction A=lcm(1,...,m)-1, B=m for m>=3, with the complete dyadic logarithmic-size proof.

For L>=1, the prescribed chain c_0>...>c_L=0 is a complete orbit for some A>c_0 exactly when gcd(c_i,c_j) divides c_(i+1)-c_(j+1) for every pair 0<=i,j<L. For its compatible residue a modulo H=lcm(c_0,...,c_(L-1)), 0<=a<H, the least numerator is a+H max(0,floor((c_0-a)/H)+1). The full prime-power CRT proof, strict-start boundaries, adjacent-only counterexample and large-H/small-residue warning remain. The original question is equivalent, up to harmless finite small-input adjustments, to A_min>=exp(c sqrt(L)) uniformly. No such inequality is proved here.

## Exact source correction and full local repairs

The source is Baraskar and Vukusic, Bounds for Sets of Remainders, Journal of Integer Sequences 29 (2026), Article 26.1.4, published January 26, 2026. The exact journal PDF is 377174 bytes, SHA-256 3cd27f6994d93ad35711bbeee2f2389a7d5350427aa222af9626794a70c99be3. Its Lemma 19 on p. 13 has t+1 where the corrected extinction equivalence needs t-1. The same issue appears as Lemma 11 in arXiv:2508.20853v1, p. 10. Citations and separate source-inspection scopes are retained in SOURCES.json.

Use S_0(N)={1,...,floor(N/2)}, S_(j+1)(N)={N mod b:b in S_j(N),b!=0}, and P(N)=max_(1<=b<=N) P(N,b). For N>=3 and t>=1, P(N)=t if and only if S_(t-1)(N)={0}, equivalently a singleton followed only by empty iterates. The proof identifies the unique zero stage Q among lower-half starts and proves P(N)=Q+1, with the even-midpoint Q=1 case handled by a different start. For N=1 all sets are empty although P(1)=1. For N=2, P(2)=1 and the sequence is {1},{0},empty,... . Neither boundary obeys the N>=3 formula.

AUDIT.md retains the full independent local repairs, not only summaries:

- The upper-half image endpoint issue in Lemma 18 is explained, including its N=2 failure.
- Lemma 21 is replaced by the domain-safe containment S_j(N) subset {nonnegative integers <=N/(j+2)}. The complete induction works for empty sets and gives s_j(N)<=N/(j+2)+1.
- For Lemma 23, x_0=0 and x_(j+1)=N-(j+2)x_j. The corrected inclusion contains every integer r with max(1,j)<=r<=(N-j-1)/(j+2) and r congruent to x_j modulo (j+1)!. The complete all-N induction reconstructs k=(N-r)/(j+2), proves its membership and checks 0<=r<k. Empty intervals are allowed.

For fixed j, this progression has N/(j+2)!+O_j(1) members. Together with the safe upper estimate this recovers Theorem 3's fixed-j cardinality bounds. Theorem 3 uses Lemmas 21 and 23, not the defective Lemma 19. Nothing here refutes the main theorem, the distinct s(N) asymptotic formula or the consecutive-difference theorems; the latter results were not independently audited.

## Independent evidence and exact limits

The historical independent audit checked 719,400 complete orbits through A=1200 and 3,782,774 transitions against a separate dynamic-programming calculation; 188,170 sub-block/period instances through A=180; 96,000 APs; all 1,023 nonempty subset chains on states 1..10, with 516,031 candidate residues and 250 compatible chains; and 43,680 word/tail templates, of which 3,047 were realizable and 32,382 were excluded by the word obstruction. It also checked the four sharp constructions, 127,535 complete orbits for selected larger numerators and 4,000 deterministic larger pairs.

The independent source-recurrence checks cover N=1..3000, 5,622 upper-half comparisons through N=600 and 39,000 repaired-inclusion/upper-bound cases for j=0..12. Constant-word checks cover m=3..150, binomial divisibility u=1..2000 and dyadic sizes through m=2048. Twelve mathematical negative controls and seventeen inventory controls were rejected in each Python mode. These computations support the universal proofs, not an asymptotic conclusion.

The saved independent exact outputs are literally byte-identical under normal Python, -O and -OO: 72026 bytes, SHA-256 0b732fc2788d94a08f02144533d4300b85887b04a2c2f2ac7f29c9a47eb16e65. The complete 49,995,000-pair candidate scan was not independently repeated; only its exact receipt was authenticated and selected larger cases were independently checked. Its claimed range-wide maximum is not independently certified. Candidate or source-author code was not imported or executed by the auditor. No mathematical program was rerun during editorial preparation.

Nine historical independent public retrievals succeeded; eight resources with candidate counterparts matched exactly, including five PDFs. The source-inspection claim is limited to recorded pages and arguments. The 3/10 announcement was described publicly as unpublished; bounded searches did not retrieve its supporting manuscript or a journal erratum, which does not prove nonexistence. No source novelty, global current-best or complete literature-survey certificate is given.
