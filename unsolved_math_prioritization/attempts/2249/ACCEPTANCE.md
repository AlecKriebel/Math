# Acceptance of the finite-gap result for EP677 / 2249

The independently audited original report is accepted as a partial,
computer-supported finite-gap theorem. With

\[
M(n,k)=\operatorname{lcm}(n+1,\ldots,n+k),
\]

the accepted claim is

\[
M(n,k)\ne M(n+d,k)
\quad(n\ge1,\;1\le k\le20,\;k\le d\le256),
\]

where every variable is an integer. There is no upper cutoff on n. The
boundary d=k is included and full prime-power exponents are compared. This
acceptance does not extend to arbitrary k or d and makes no novelty or
priority claim. No mathematical correction to the original argument was
required.

## General arguments accepted

- The prime-by-prime divisor identity F_k(n)/M(n,k)=T_k h_k(n), h_k(n)|C_k,
  where F_k(x)=product from i=1 to k of (x+i), L_k=lcm(1,...,k), T_k=k!/L_k
  and C_k=L_k/k.
- Completeness of the reduced candidate ratios a/b>1 with gcd(a,b)=1 and
  ab|C_k, and the exact signed-exponent cardinality formula.
- Strict decrease of the auxiliary product ratio F_k(x+d)/F_k(x), uniqueness
  of any positive-integer product root, and both strict root bounds. No
  monotonicity of M(n,k) or of the cross-multiplied polynomial is assumed.
- Completeness of the consecutive-integer sign test, including the
  negative-at-one branch and the need to check actual LCMs if an integer
  product root occurs.
- The two-sided cross-difference divisibility equivalence for full LCMs,
  including the inclusive d=k boundary. This criterion alone does not prove
  universal nonexistence.

PROOF.md and AUDIT.md contain the full general derivations. The infinite
starting-point quantifier follows from those arguments, rather than from a
finite scan of n.

## Reported numerical verification

The original independent audit checked all 4,930 length-gap slices and all
3,072,678 rational-product cases, with consecutive-integer signs and the
proved upper-endpoint sign checked exactly. It found zero positive integer
product roots and therefore zero equal full-LCM pairs in this domain. Lengths
one and two have no candidate ratios and are included by the general argument.

An independently authored implementation enumerated reduced quotients of
trial-enumerated divisors and used integer polynomial coefficients with Horner
evaluation. It did not inspect, import or execute the candidate programs;
those files were read as bytes only to check integrity. The audit passed
normal, -O and -OO Python modes, with outputs agreeing after excluding timing
and optimization fields. Ten malformed or false certificate controls were
rejected in every mode. Further controls tested 40,000 ordinary and 60 large
starting-point divisor cases, 16,400 disjoint triples and 344,400 termwise
conditions, 150 independently regenerated brackets, and relevant scope traps.
These are historical verification results, not newly executed edition tests.

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
