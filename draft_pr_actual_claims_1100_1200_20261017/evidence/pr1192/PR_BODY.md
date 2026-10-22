## Accepted partial fixed-scale result

This authored edition records exact two-sided saturation and a transposed
k=4 construction for the fixed integer seed in Section 2 of Sam Mausberg's
*Two Formalized Partial Results Related to Erdős Problem E885*, at commit
05c3837a998a6a71ed1f2ce05985bc67f8e1c35a. It also records that a k>=5
configuration cannot contain two of the original fixed differences or two
of the transposed fixed differences. The original S-pair third-difference
support bound is four, with a sharper bound of three for the second and
fourth elements. The T-pair exclusion uses three-support intersections:
third-difference supports of size five do occur.

The general square criterion, complete two-difference divisor reduction,
full factor-difference enumeration, transposition argument, support
implications and rational (k+1)-by-k square-sumset equivalence remain fully
proved. Zero differences, parity, positivity, injectivity and the absence
of an independent N cutoff are explicit. The result concerns the exact
source integers only. It is not an arbitrary-rescaling theorem.

## Separate finite premises and reproduction limit

The public proof defines the fixed sets through the pinned source without
copying the numerical seed lists. Premises P1–P4 explicitly identify the
separately checked seed identities, exact closures, S support bounds, and
T triple-support obstruction. Numerical seed lists, raw tables, individual
witnesses, certificate contents, executable code and copied sources are
omitted. The finite saturation and support claims cannot be independently
reproduced from this edition alone. This is not a complete self-contained
proof of the seed-specific computational claims or a complete computational
reproduction package. Hashes alone do not prove the omitted arithmetic.
The complete general arguments give the stated deductions from the
separately verified finite premises.

## Independent verification and source credit

An independently authored exact-integer rebuild matched all mathematical
certificate fields across 16 fixed pairs, 1,047 pair-indexed rows, 987 distinct
positive integers and 162,718 pair-indexed memberships. Deduplicating the
integers first gives 156,803 memberships. Both pairs of two-sided closures,
all 31 square identities, and all nine available T support triples were
checked. Every triple intersection has size at most one.

The independent verifier passed in normal, -O and -OO modes with byte-identical
substantive receipts, rejecting 24 malformed mathematical inputs per mode.
Separate direct checks covered 80,400 square-criterion cases and 136 small
pairs with 116,194 exhaustive N checks under a proved bound. Zero, positivity,
parity and empty-neighborhood cases were included. The auditor did not inspect
candidate programs as source, import or execute them. Candidate historical
receipts were byte-authenticated; the candidate verifier was not independently
rerun. No third-party mathematical code or Lean formalization was executed.
The independently serialized certificate differs in bytes from the candidate
certificate; exact mathematical agreement does not mean byte identity.

The finite-factorization method is credited to Erdős–Rosenfeld,
[*The factor-difference set of integers*](https://matwbn.icm.edu.pl/ksiazki/aa/aa79/aa7944.pdf),
Acta Arithmetica 79(4) (1997), Section 3, and is re-proved here.
The [pinned Mausberg note](https://github.com/SamMausberg/lean-formalizations/blob/05c3837a998a6a71ed1f2ce05985bc67f8e1c35a/FormalConjectures/Problems/Erdos/E885/ForumNote/erdos885_forum_note.tex)
identifies the exact seed and explicitly does not settle k=5. Its author's
Lean-backed description is attributed only. Historical reading and inspection
are distinguished from this edition preparation, which performed no new
scholarly-source retrieval or inspection and no new mathematical computation.
The full 1999 and 2019 papers were not audited and are not dependencies.

Unrestricted k=5 and the universal arbitrary-k target remain unresolved by
this work. No novelty, priority or exhaustive literature-status claim is made.
This AI-assisted work is unrefereed. Acceptance means an independent internal
AI audit of the original report and separate finite evidence. No external
human peer review, journal acceptance or formal proof-assistant certification
is claimed. No mathematical correction was required.

Only eight authored prose/public-verification-metadata files are added under
unsolved_math_prioritization/attempts/2364. QUEUE.md and all unrelated paths
are unchanged. Private coordination material is excluded.

Base commit: `4b27092a448d53b61408355ce44ec38d103a1ce4`.

## Exact public-file identities

- `ACCEPTANCE.json`: 3,195 bytes; SHA-256 `487e981727a123094f51a3cda86727d46948fa094434a0c1c89202b1b97ac2fc`.
- `ACCEPTANCE.md`: 4,061 bytes; SHA-256 `ef4fa6972e77c1d9caf2db3960fc2a4c03f0160ff4cacdb1ac54605d0df11373`.
- `AUDIT.md`: 11,044 bytes; SHA-256 `d56edc78f75097dacc578313f99b16e5646b5745ca6cc0f76e0914e73d69060b`.
- `MANIFEST.json`: 1,375 bytes; SHA-256 `ae559cb71742eb8d7349a973640fabb9b7d185b531465dba665af08955b7d7c1`.
- `PROOF.md`: 12,870 bytes; SHA-256 `b5491adc6481dbf66312d395da6371de9a697ae953c89dd2b6ce1096eb70a0c3`.
- `README.md`: 2,471 bytes; SHA-256 `37b1157ae2cba47bd77d2e70d76aee071e5edc2354d10b421215933e26acd192`.
- `SOURCES.json`: 3,913 bytes; SHA-256 `238f9df72e1a16d29583f1db883522c00b744f2620e30d6c7ed406c83a104f80`.
- `VERIFICATION.json`: 3,738 bytes; SHA-256 `3f7c50430bdeebab372e42ef31cae9c3bfb0a33ff33b9508acf967e40e06fe30`.

MANIFEST.json lists eight members and hashes the other seven; this body independently pins its digest.

