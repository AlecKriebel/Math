# Complete minimality certificates through k=46

This independently extends the present project's minimality checks from k<=20 to k<=46. It does not extend the published computation frontier. All 46 minima match the existing public table, whose frozen byte hash is recorded separately. The remaining public witnesses through 400 have not acquired independent minimality certification from this run.

## Search and completeness

The authored search uses only integer arithmetic. For a fixed p<=k, let q=p^d be the smallest power of p greater than k. If a current candidate n violates Lucas's digit condition, find the most significant violating digit position j. Keep all higher digits, increase digit j to the corresponding digit of k, and replace all lower digits by those of k. The resulting next_p(n) is the smallest locally admissible integer >=n: all higher digits already dominate k, a smaller value with the same higher prefix still fails at j or below it, and increasing a higher digit is larger. If no digit violates the condition, next_p(n)=n.

Starting at n=k+2, compute these next values for every prime and move to their maximum. The interval from the old n up to but excluding that maximum is invalid for the prime that supplied the maximum. Record its two endpoints and that prime. At a fixed point all prime conditions hold. This partitions every integer in [k+2,g(k)) into explicitly rejected intervals; no candidate is skipped without a reason.

Termination is not an empirical assumption. For k>=3, M_k-1 is admissible and exceeds k+1, where M_k is the product of the local q values. Every jump is to a local next value, so cannot jump beyond any common admissible upper bound. A strictly increasing integer sequence bounded by M_k-1 terminates. The cases k=1,2 are directly covered by the same actual search, yielding 3 and 6.

## Independent verifier

The separately retained independent verifier neither imports nor calls the search's digit-raising code. For each p it constructs a complete local-period table by the unrelated exact test C(r,k) mod p for every 0<=r<q, with C(r,k)=0 for r<k. These are exact Python binomial integers.

The period proof is short. In F_p[x], (1+x)^q=1+x^q. Writing n=tq+r with 0<=r<q, every term of positive degree from (1+x^q)^t has degree >=q>k. Therefore C(n,k) is congruent to C(r,k) modulo p. Hence the local admissible count up to any X is exactly the number of whole q-periods times the local residue count, plus the prefix count in the last period.

For each recorded interval [lo,hi), the verifier independently subtracts these two periodic prefix counts and requires zero locally admissible points. It also requires contiguous, strictly positive intervals beginning at k+2 and ending exactly at the asserted minimum. It then checks the final witness with direct C(n,k) mod p for every p<=k. This proves both existence and exclusion of every smaller permitted n. The certificate byte counts and SHA-256 hashes are checked before verification.

All counters, powers, products, binomial values and endpoints are Python arbitrary-precision integers. No fixed-width wraparound or floating logarithm is used. Prime generation uses an independent Eratosthenes sieve. Verification checks use explicit exceptions, not assert statements, so optimization flags cannot remove them.

## Recorded scope

The retained minimality record contains exactly k=1,...,46. The certificates comprise 2,562,964 consecutive exclusion intervals. Normal, -O and -OO verifier executions return byte-identical PASS reports. A run initially configured to continue through 60 was interrupted during the still-incomplete k=47 search; no partial certificate for 47 is included, and no claim about minimality beyond 46 follows.

The certificates are separately retained authored arithmetic evidence, not source-author output. VERIFICATION.json records the aggregate source-table comparison. The original search code, independent verifier, raw minimum records and interval certificates are retained separately and are not distributed in this public prose edition; this edition alone is not an executable replay package. The analytical results do not depend on any finite computation.
