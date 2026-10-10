# Disjoint equal-length interval LCMs: EP677 / 2249

This edition records complete general elementary reductions and an accepted,
computer-supported finite-gap theorem. Set

\[
M(n,k)=\operatorname{lcm}(n+1,\ldots,n+k).
\]

For all positive integers n, all 1<=k<=20, and every integer k<=d<=256,
M(n,k) differs from M(n+d,k). The starting point has no upper cutoff. The
boundary d=k is included and the comparison covers complete prime-power
exponents. Arbitrary lengths and gaps remain outside the accepted result.

The general divisor identity confines F_k(n)/M(n,k) to a fixed factor times
a divisor of L_k/k. Equality of two LCMs therefore implies one of finitely
many rational product equations for each fixed length and gap. A strictly
decreasing auxiliary product ratio gives uniqueness and an explicit upper
bound for any possible integer root. The full cross-difference divisibility
equivalence provides a second exact criterion. These proofs are supplied in
full, without assuming LCM monotonicity or replacing full LCM equality by
prime-support equality.

The separately audited exhaustive check covered 4,930 length-gap slices and
3,072,678 rational-product cases. No positive integer product root occurred,
so no equal-LCM pair occurred in that domain. All three Python optimization
modes passed the independent audit and ten adverse certificate controls.
Finite tests support the reported finite application and do not resolve the
unrestricted problem.

## Contents

- PROOF.md: the complete general proofs, finite reduction and reported result.
- AUDIT.md: the full independent mathematical audit and historical checks.
- ACCEPTANCE.md and ACCEPTANCE.json: exact accepted scope and review limits.
- VERIFICATION.json: aggregate/count/hash/byte and match metadata, without data.
- SOURCES.json: scholarly titles and public URLs, PDF identities, historical
  retrieval/inspection scope, source roles and access limitations.
- MANIFEST.json: exact membership and identities of the other seven files.

## Attribution and source limits

[Erdős (1979)](https://users.renyi.hu/~p_erdos/1979-23.pdf), printed page 78,
states the equal-length target with the inclusive separation m>=n+k. The
[1980 note](https://users.renyi.hu/~p_erdos/1980-11.pdf) uses strict separation
and does not replace the inclusive target. [Farhi and Kane's manuscript](https://cseweb.ucsd.edu/~dakane/lcm.pdf)
provides related valuation bookkeeping; its indexing uses one fewer than the
number of terms. Its exact-period theorem is not needed. [The author's
bibliography](https://cseweb.ucsd.edu/~dakane/cv.html) confirms publication in
Proceedings of the AMS 137 (2009), 1933-1939. No stronger small-length or
adjacent-block prior result was independently recovered, and no priority or
current literature-wide status assessment is claimed.

## Publication edition: finite numerical certificates omitted

This prose-and-verification-metadata edition preserves the complete general
divisor, ratio, monotonicity, root-bound and cross-difference proofs. It also
reports the accepted computational claim: for all integers n>=1, 1<=k<=20 and
k<=d<=256, the two complete LCMs M(n,k) and M(n+d,k) differ. The starting point
is unrestricted and the inclusive separation boundary is retained.

Raw certificates, individual brackets, numerical witness packages, executable
code and dataset contents are omitted. The finite verification cannot be
independently reproduced from this edition alone. This is not a complete
self-contained proof of the finite claim or a full computational reproduction
package. Published hashes, byte counts, aggregate counts and match results
identify separately audited evidence; hashes alone do not prove the omitted
arithmetic. The general proofs are written out in full and do not depend on
finite regression tests. Their application to the stated finite range relies
on the reported exhaustive numerical verification.


## Edition and review statement

This AI-assisted work is unrefereed. Acceptance refers to an independent
internal AI audit of the original report and its separate numerical evidence.
No external human peer review, journal acceptance or formal proof-assistant
certification is claimed. No mathematical correction was required. No novelty,
priority or full solution is claimed. The arbitrary-length, arbitrary-gap
problem remains unresolved by this work.

This edition preserves the general proofs, exact finite claim and substantive
scope qualifications. Historical verification and scholarly-source inspection
are reported as such. Edition preparation checks byte integrity, exact
editorial changes and publication structure only; it performs no new
mathematical computation or scholarly-source retrieval/inspection. The
original sealed candidate and audit packages are unchanged. Copied source
documents, source text, page images, dataset contents, raw certificates,
executable code and private coordination material are not distributed.
