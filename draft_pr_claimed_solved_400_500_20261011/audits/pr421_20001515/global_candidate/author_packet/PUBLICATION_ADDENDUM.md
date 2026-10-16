# Current publication and verification addendum

Dated 2026-10-12 UTC. Scope: PR421 / problem 20001515, exact source head
`d5bf8b5a25cabb177433338fae60af52ebfecf1c`. This addendum clarifies the current
accepted scope while preserving every frozen proof and historical note byte.
It supersedes dated pending-review, provisional-source, and portability-only
interpretations in the included notes; it does not silently rewrite their
history. The author budget remains `1/5`, with zero new proof-search turns.

The accepted mathematical result is a finite locally CAT(0) unit cube complex
with cells `(1,7,8,2)`, whose fundamental group is exactly
`<a,b,c,t | tat^-1=a, tbt^-1=ab, tct^-1=bcb>`. Its CAT(0) universal cover gives
a free, proper, cocompact cubical action of that group in dimension three. The
positive final `b` is essential. The actual cube-corner incidence and reversible
presentation argument have been independently reconstructed and accepted.
This is the general cube-complex convention permitting boundary-face
identifications: the repeated vertex A in the second Q-square is retained.
Leary, *A metric Kan–Thurston theorem*, Appendix C, Theorem C.9 (printed p.33)
provides the general flag criterion; C.4 concerns strict cubical covers and
C.11 permits second subdivision of the quotient under a stricter convention.
The original proof remains pinned and primary. No minimum dimension or cell
count, virtual specialness, formal proof-assistant verification, or external
human peer review is claimed.

The accepted exact-source review successfully read the current
[HTTP www AIM entry](http://www.aimpl.org/freebycyclic/5/), together with the
[28 August 2024 archive](https://web.archive.org/web/20240828224508id_/http://aimpl.org/freebycyclic/5/)
and [10 March 2026 archive](https://web.archive.org/web/20260310215532id_/http://www.aimpl.org/freebycyclic/5/).
All three responses were byte-identical: 25,734 bytes, SHA-256
`9dfa1624c5743d114c671ea69201a9ea46fe577e707239e245cc7f22b30b8121`.
Both the displayed AIM 5.2 question and embedded record identify
`a->a,b->ab,c->bcb`, attributed to Rylee Lyman, and ask for the geometric
cubical action. Record ID `0df1011a6fa8a3c46e2c977b7e12c66f`, revision
`6-d5a22eda9ed96ccdc8327e2e9395bb3e`. The HTTP observation has no TLS
authentication; HTTPS endpoint certificate failures were preserved, with no
warning bypass. Earlier failed live-page checks remain historical observations.
The empty source status field is not interpreted as evidence of current
openness. The workshop's `b->aba,c->bcb` example is a different group formula.
The driver does not fetch or newly certify these external sources.

The bounded priority review found no recorded earlier exact/equivalent
resolution or directly covering geometric-cubulation theorem in the inspected
sources. This is bounded absence evidence with acquisition/indexing limits,
not proof of firstness or absolute novelty. The accepted concrete contribution
is the explicit finite NPC quotient and its exact group identification.

The review also accepted a present qualitative existence deduction using older
tools. For `H=<x,y,b | [x,y]=1,bxb^-1=y>`, the consecutive stabilizers of the
`bx` Bass–Serre axis have trivial intersection. Corrected Minasyan–Osin
Corollary 4.3 gives WPD; Dahmani–Guirardel–Osin Theorem 6.8/Corollary 2.9 gives
a virtually cyclic hyperbolically embedded subgroup, and Sisto Theorem 1 gives
Morse behavior and word-metric quasiconvexity. Ben-Zvi–Kropholler–Lyman
Theorems 1.1 and 5.1 supply a finite local-isometry completion preserving the
cyclic subgroup exactly. The cubical involution `x<->y,b->b^-1` supplies two
compatible end maps on the same domain. A finite double mapping cylinder has
flag links, and reversible substitutions `t=x,a=xy^-1,c=(zx)^-1` identify its
group with the target. This yields a dimension-at-most-three existence route
without the explicit small Q or a cell-count bound. These mechanisms are
credited prior tools; this presently assembled exact application does not
establish a historical earlier answer or that those tools were unavailable.
The research note must explain that route alongside the explicit model.

All 62 essential historical validation gates in the three author-packet
programs were replaced by the accepted explicit `if not ...: raise
AssertionError(...)` forms, and a fresh independent repair audit verified the
one-to-one structural preservation and ordinary standalone normal/`-O`
behavior. Only these exact three accepted programs are current entry points.
The original scripts used bare assertions that disappear under optimized
Python; they are not included as runnable historical duplicates. This repair
has not certified any peer reviewer script. It requires unshadowed standard
builtin `AssertionError` and the copied proof/output layout; arbitrary foreign
embedding or builtin rebinding is outside its scope.

Earlier unpublished independent-checker bytes from before the historical
portability edit are unavailable and are not certified. The exact historical
source/checker bytes at the pinned head and the accepted current scripts have
independent proof and reproduction audits. No portability-only assertion is
promoted into proof of missing historical provenance. Source receipts label
historical and delivered hashes separately.

Evidence consists of written deductions, exact finite computation, and internal
AI-assisted adversarial audits. The saved historical outputs are expected
baselines, not successful current runs; the driver deletes them and verifies
fresh stdout and freshly written full results. Extensive AI assistance and
unrefereed status are disclosed. Preparation acceptance does not complete the
two required fresh sequential whole-paper and package reviews or certify readiness for a
Zenodo release, sheet registration, or merge. No outside individual was
contacted, and this packet includes no foreign PDFs, HTML, corpus, private
fixtures, tokens, bytecode, or virtual environment.
