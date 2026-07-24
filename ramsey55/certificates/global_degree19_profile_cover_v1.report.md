# Exact degree-profile cover of the global minmax-degree-19 branch

Evidence status: **EXACT COVER AND UNION ENCODING VERIFIED; SOLVE
UNRESOLVED**

This branch consists of order-43 Ramsey models whose degrees lie in
\(\{19,20,21,22,23\}\) and which have at least one vertex of degree 19 or
23. Equivalently, its min/max parameter
\(\min(\delta(G),42-\Delta(G))\) is exactly 19.

The cover is a decomposition of this branch only. It is not an exclusion of
the branch and does not cover arbitrary order-43 graphs.

## Multiplicity cover and complement orientation

Write

\[
(a,b,c,d,e)=(n_{19},n_{20},n_{21},n_{22},n_{23}).
\]

The handshake lemma requires \(a+c+e\) to be even. Complementation sends the
profile to

\[
(e,d,c,b,a).
\]

This action has no fixed admissible profile. Indeed, a fixed profile would
have \(a=e\) and \(b=d\). Since
\(2a+2b+c=43\), \(c\) would be odd, making \(a+c+e=2a+c\) odd and
contradicting handshake parity.

Each two-element complement orbit is therefore oriented uniquely by

\[
(a,b)>(e,d)
\]

in lexicographic order. Vertices are then relabelled into nondecreasing
degree order. Direct exhaustive enumeration gives:

- 88,550 handshake-admissible exact-branch profiles before complement;
- zero complement-fixed profiles;
- 44,275 canonical profiles after orientation.

The independent checker enumerated the 88,550 profiles through a separate
loop structure, reconstructed every complement orbit, and found no missing,
duplicate, or invalid representative.

## Exact degrees from forward counters

The direct global CNF has forward threshold counters for the 42 edge
indicators and 42 nonedge indicators at every vertex. Only false final
thresholds are used:

| Exact degree \(q\) | Edge unit | Nonedge unit |
|---:|---:|---:|
| 19 | edge count \(<20\) | nonedge count \(<24\) |
| 20 | edge count \(<21\) | nonedge count \(<23\) |
| 21 | edge count \(<22\) | nonedge count \(<22\) |
| 22 | edge count \(<23\) | nonedge count \(<21\) |
| 23 | edge count \(<24\) | nonedge count \(<20\) |

A negative final threshold is sound in the one-directional counter because
reaching the threshold forces that variable true. Since edge and nonedge
counts sum to 42, the two upper bounds in each row force exact degree
\(q\). Canonical counter extensions establish completeness for every
primary assignment satisfying the intended degree.

The independent checker rebuilt all 86 counter final rows without importing
the generator and exhaustively checked the threshold semantics for every
requested degree and every possible observed count.

## Selector-union encoding

Every canonical profile has 86 distinct negative threshold units, two per
vertex. A fresh selector guards each profile, and one long clause requires
at least one selector.

- base variables / clauses: 65,403 / 2,052,132;
- selector variables: 44,275;
- appended implication clauses: 3,807,650;
- appended at-least-one clause: 1;
- union variables / clauses: 109,678 / 5,859,783;
- appended clause-stream SHA-256:
  `edae0bba35896250ea245a49ec31fc27a5f578e368b90ccb405d138e692eeea1`.

The 15,126,076-byte plan has SHA-256:

`63e385365ee787882a455d419460ec95cbee9f5b4207afc5b33093832ff4a9d5`.

The materialized union was retained only in temporary storage. It has
151,810,283 bytes and SHA-256:

`9d19c71875647f624e2b51f4803473ba5957a0e1fb125101123408b29dd266ef`.

The independent streaming checker matched all 2,052,132 copied base clauses
and all 3,807,651 appended clauses in order, with zero mismatches. It also
matched the union header, metadata, file hash, byte count, and appended
stream hash.

## Proof-free pilot

The resource preflight found more than 10 GiB free disk and 54% system memory
headroom. Pinned Python-SAT 1.9.dev7 MapleChrono then ran the checked union
with a 50,000-conflict budget and no proof output.

- status: `BUDGET_EXHAUSTED`;
- observed conflicts: 50,004;
- decisions: 561,762;
- propagations: 61,864,371;
- restarts: 275;
- solver runtime: 105.581548 seconds;
- peak resident set: 2,424,078,336 bytes;
- pilot-result SHA-256:
  `98ad122e356fe627490d884dd772cf1d2784fcaa320f675dca4e88495e3d1016`.

No model or proof was produced. The outcome is a resource-limited
computational observation only.

## Artifact hashes

- generator source:
  `9ab74cc717305d65f432fc653a2072bb65363a5f29d9228f2eeaae67b688b043`;
- independent checker source:
  `33273833a9f0b875a76aeb6f71d5e0c98729b2be7fe589afeaa1298acc8fee79`;
- test source:
  `80e18dd4694b7491c4e7f22e6193d6a12a95f4a051aca51110e859ccdf2482e2`;
- plan-only checker result:
  `316b4844c5b22b39695af8cc1cb68f6455e6264a53893a98815fc3345e5f8720`;
- generated metadata:
  `4a5cf3024b6819df29c5d1a3800ea7eff6bc3bac9f608b804a9121767d44e1d4`;
- materialized-union checker result:
  `6c6bfbbaddc8ea040f2d67a98ceb4a6c6d80da128d7ceeec008dce789bfa944d`;
- proof-free worker source:
  `4939d935e709fed3527d31858dc8854c3d8b7b84420e29197856b126e92dcbf3`.

Five structural tests pass.

## Claim boundary

The degree-profile census, complement orientation, threshold semantics, and
selector union are exact and independently checked. The MapleChrono timeout
has no proof and therefore excludes no profile, no union branch, and no
graph. The minmax-degree-19 branch remains unresolved, and the bound
\(43\le R(5,5)\le46\) is unchanged.
