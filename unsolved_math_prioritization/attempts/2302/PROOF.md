# A finite exact counterexample to the descending-prime greedy rule

This is an AI-assisted, unrefereed authored mathematical audit edition. Acceptance means an independent internal AI audit of the precisely scoped written arguments and their explicitly retained classical dependencies. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete substantive ten-section audit and the full authored finite counterexample are retained, including every mathematical set, fraction, inequality, count, correction, dependency and limitation. Executable code, raw calculation outputs or datasets, copied source documents or text, source images and private coordination material are not distributed.

Retrieval, inspection and mathematical-check statements describe the original audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. Historical finite checks concern one finite witness only; they do not establish an eventual optimizer or the general harmonic-rigidity claim.

This is an independently checked finite witness. It does not refute an assertion quantified only over all sufficiently large N at fixed C, and it does not refute asymptotic optimality or harmonic rigidity.

Take N = 100 and C = 1/2. For a finite set A of pairwise coprime integers at least 2, put μ(A) = Σ(a in A) 1/a and U(A;100) = #{1 ≤ m ≤ 100 : a does not divide m for every a in A}.

The descending-prime greedy set is

A = {17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97}.

Its exact reciprocal sum is

μ(A) = 35224176913494639959138427813071 / 76775489974875738420016721522869 < 1/2.

Indeed twice the numerator minus the denominator is

−6327136147886458501739865896727 < 0.

The next prime in descending order is 13, and

μ(A) + 1/13 = 534689789850306057888816283092792 / 998081369673384599460217379797297 > 1/2,

because twice the numerator minus the denominator is

71298210027227516317415186388287 > 0.

All partial sums along the descending list are increasing, so these two exact inequalities certify that A is precisely the greedy set specified in the question.

Now replace 17 and 23 by 7:

B = {7,19,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97}.

Every member is prime, hence B is pairwise coprime. Its exact budget is

μ(B) = μ(A) − 1/17 − 1/23 + 1/7
     = 686355084015973446882109176506 / 1374497262977315010077025705013 < 1/2,

because twice the numerator minus the denominator is

−1787094945368116312807352001 < 0.

For A, the product of any two distinct members is at least 17·19 = 323 > 100. For B, it is at least 7·19 = 133 > 100. Thus no positive integer up to 100 is divisible by two distinct members of either set. Consequently the covered counts are exact sums of floors, with no inclusion-exclusion corrections.

For A the counts are 5,5,4,3,3,2,2,2,2, followed by ten 1s, summing to 38. Hence U(A;100) = 62.

The replacement deletes floor(100/17) + floor(100/23) = 5 + 4 = 9 covered integers and adds floor(100/7) = 14. Because B is overlap-free, its covered count is 38 − 9 + 14 = 43. Thus U(B;100) = 57 < 62.

This proves that the literal greedy set is not always the exact finite minimizer, even at C = 1/2 < log 2. It does not claim B is itself globally optimal. The gap is five integers at this one N, not a positive asymptotic density gap.

The original 1973 problem, printed page 135, asks for an extremal sequence while also permitting a near-minimum interpretation. The imported modern statement says N is large. Accordingly this witness must not be promoted to a disproof of a fixed-C eventual statement. It does rule out reading the January 2026 asymptotic result as an all-N exact-greedy theorem.

Public source for the historical question: https://users.renyi.hu/~p_erdos/1973-21.pdf .

Historical verification: an independent Python-standard-library calculation used exact rational arithmetic, trial-division primality checks, direct counting, and a separate floor-sum verification. It executed no code from any source author. The code and raw calculation output are not distributed in this edition; VERIFICATION.json records their byte identities and the original execution scope. The complete exact mathematical witness above is retained.
