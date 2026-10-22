## Accepted finite-gap result with general reductions

For M(n,k)=lcm(n+1,...,n+k), the independently audited original evidence
establishes M(n,k) != M(n+d,k) for every integer n>=1, every 1<=k<=20 and
every k<=d<=256. The starting point has no upper cutoff. The inclusive
disjoint boundary d=k and all prime-power exponents are included.

The complete general proofs show that F_k(n)/M(n,k)=T_k h_k(n), with
h_k(n) dividing C_k=L_k/k, where F_k(x)=product(i=1,...,k)(x+i),
L_k=lcm(1,...,k) and T_k=k!/L_k. Equal LCMs imply a reduced product ratio
a/b>1 with gcd(a,b)=1 and ab dividing C_k. Strict decrease of the auxiliary
product ratio gives uniqueness and the strict bounds
n+1<k*d*a/(a-b)<=k*d*(1+floor(sqrt(C_k))). The exact candidate-ratio count,
consecutive-integer sign logic, and two-sided cross-difference divisibility
equivalence are also proved in full. No monotonicity of the LCM itself or
of the cross-multiplied polynomial is assumed; prime support does not replace
full LCM equality. The cross-difference criterion alone does not prove
universal nonexistence.

The arbitrary-length, arbitrary-gap problem remains unresolved by this work.
No novelty, priority, stronger prior small-length result or full solution is
claimed. No mathematical correction to the accepted original was required.

## Finite verification and reproduction limit

The independent audit checked all 4,930 length-gap slices and 3,072,678
rational-product cases with exact consecutive-integer and analytic
upper-endpoint sign checks. There were zero positive integer product roots
and therefore zero equal full-LCM pairs in that domain. Lengths one and two
have no candidate ratios and are included by the general reduction.

The independently authored implementation enumerated reduced quotients of
trial-enumerated divisors and evaluated integer polynomials with Horner's
method. The candidate used signed exponents/binomial evaluation and a
separate divisor-pair/rising-product verifier. The independent auditor did
not inspect, import or execute the candidate programs; it read those files
as bytes only for integrity. Normal, -O and -OO runs passed and agreed after
removing timing and optimization fields. Ten adverse certificate controls
were rejected in each mode. Further controls covered 40,000 ordinary and 60
large starting-point divisor checks, 16,400 disjoint triples, 344,400 termwise
divisibility conditions, and 150 independently regenerated brackets.

This edition omits raw certificates, individual brackets, numeric witness
packages, executable code and dataset contents. The finite verification
cannot be independently reproduced from this edition alone. It is not a
complete self-contained proof of the finite claim or a full computational
reproduction package. Hashes, byte counts, aggregate counts and match results
identify separately audited evidence; hashes alone do not prove the omitted
arithmetic. The complete general proofs are included, while the finite
application relies on the reported exhaustive numerical verification.

## Sources and review status

[Erdős (1979)](https://users.renyi.hu/~p_erdos/1979-23.pdf), printed page 78,
provides the inclusive equal-length target. The
[1980 note](https://users.renyi.hu/~p_erdos/1980-11.pdf) uses strict separation
and does not narrow that target. [Farhi and Kane's author-hosted manuscript](https://cseweb.ucsd.edu/~dakane/lcm.pdf)
is credited for related valuation bookkeeping and its one-fewer-term index
convention; no exact-period theorem is used. [The author bibliography](https://cseweb.ucsd.edu/~dakane/cv.html)
confirms Proceedings of the AMS 137 (2009), 1933-1939. Retrievals, PDF identities,
actual page inspection scopes and unavailable reads are recorded as historical
audit evidence in SOURCES.json. No new scholarly-source retrieval/inspection
or current global-status assessment was performed for this edition.

This AI-assisted work is unrefereed. Acceptance means an independent internal
AI audit of the original report and separate numerical evidence. No external
human peer review, journal acceptance or formal proof-assistant certification
is claimed.

Only eight authored-prose/public-verification-metadata files are additions
under unsolved_math_prioritization/attempts/2249. Copied source documents,
source bodies and images, numerical proof payloads and private coordination
material are excluded. Original sealed packages, QUEUE.md and unrelated
repository paths remain unchanged. Edition preparation checks byte integrity,
exact editorial replay and publication structure without new mathematical
computation. This packet is prepared for a draft PR; no remote mutation has
been made during preparation.

Base commit: `4b27092a448d53b61408355ce44ec38d103a1ce4`.

## Exact public-file identities

- `ACCEPTANCE.json`: 5,291 bytes; SHA-256 `c01c46871c7a704fde4b0e18e7c7f2612e3418220c3e69b897d127d1c44ab2ff`.
- `ACCEPTANCE.md`: 4,993 bytes; SHA-256 `bd8b0fd5ab33cb3abc8604f8d982855946152b8cd9184fa484d0d9aec6b91825`.
- `AUDIT.md`: 13,795 bytes; SHA-256 `7d8ad86606e90695eee4a141e371873d97b92d9e20bff24bd07b7e5cfee8b4c8`.
- `MANIFEST.json`: 1,658 bytes; SHA-256 `e1b32e2508fb33647ebc3216f2b7357332d219d1c36ea5b19299631f1fa1f3ad`.
- `PROOF.md`: 11,630 bytes; SHA-256 `2fd04c00bce0dda1b8730187e1a7f7507f711028525bab95eef8b1ebcc59273a`.
- `README.md`: 4,967 bytes; SHA-256 `570d214c57ecd1cb08990ff5ccf41af6d2f7a1e510f829f6fa11c1f92a713696`.
- `SOURCES.json`: 4,469 bytes; SHA-256 `16fae11e44adb69d09f5e9912cdc7d3077e119f2916ac51ee4a79ec086146249`.
- `VERIFICATION.json`: 15,554 bytes; SHA-256 `e3bf6227f53d1b2839b6cdbe4bfdcf126b543299dff24392fc03c9409bf884c5`.

MANIFEST.json lists eight members and hashes the other seven; this body independently pins its digest.

