# Source and readiness gate: 10400067 / AMR-103-0067

Checked 2026-10-03 UTC. This is rank 447, Ohtsuki Problem 3.17.

## Identity and prior-attempt gate

- The live default-branch `unsolved_math_prioritization/QUEUE.md` in
  `AlecKriebel/Math`, Git blob `c87c275c638939b8008fd58db80657491d14971e`,
  has the target row queued at 0/5.
- Exact-ID and code searches of branches, PRs, issues and default-branch code
  found no previous attempt. The target `attempts/10400067` path returned 404.
  A broader two-loop search found PR 249 on a *different* problem, Kirby 1.6;
  its use of Ohtsuki's formula does not constitute an attempt on Problem 3.17.
- The pinned catalogue revision is `37e53eabe540fb458758e198be61634bd02ee008`.
  SHA256 of `problems.json` is
  `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`;
  SHA256 of `research_results.json` is
  `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`.
  Both were recomputed and match. Imported OPEN-TRIAGE notes are literature
  metadata, not a previous proof attempt.
- The exact requested URL is
  <https://www.unsolvedmath.com/problems/10400067>.
  It could not be read live: the research tool reported inaccessible, HTTP
  retrieval returned 403, and the cloud browser displayed "This request was
  blocked", 403 FORBIDDEN. No verification challenge was completed. This is
  an access limitation, not evidence about mathematical status. The pinned
  item and original publisher PDF agree on the identity and statement.

## Exact source and conventions

Tomotada Ohtsuki (editor), *Problems on invariants of knots and 3-manifolds*,
Geometry & Topology Monographs 4 (2002), pp. 377–572,
<https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf>.
The target is printed p. 439, PDF page 67. Its statement is:

> Find a topological construction of the 2-loop polynomial P_K^theta.

Equations (25)–(26), pp. 438–439, specify the theta-diagram component of
the logarithm of the Kontsevich invariant with numerator P_K^theta and
denominator Delta_K(t1) Delta_K(t2) Delta_K(t3), with t1 t2 t3=1.
The source's loop degree 1 means a graph with first Betti number 2. The
symmetry is S3 together with **simultaneous** inversion of all three
variables. Independent inversions do not preserve t1 t2 t3=1 in general.
We use Delta(t)=Delta(t^-1), Delta(1)=1.

The printed trefoil expression `12 P = -t1^2 t2+t1^2` is not literally
S3-invariant. Thus it cannot, without an orbit/representative convention,
serve as a canonical symmetric polynomial identity. This was checked on
the actual PDF page, not just OCR. We do not silently repair that example
or use it to calibrate a candidate topological invariant.

Ohtsuki's 2007 paper defines a numerator by **summing** over the 12 theta
symmetries. Averaging the same diagram representative instead gives 1/12
of that numerator. A factor of 12 is therefore material. A complete answer
must also match the Kontsevich/PBW convention, knot/mirror convention and
any framing/normalization correction. None of the partial results below
asserts an unproved normalization bridge to a different invariant.

## Current literature audit and disposition

1. Ohtsuki, *On the 2-loop polynomial of knots*, Geometry & Topology 11
   (2007), 1357–1475,
   <https://msp.org/gt/2007/11-3/gt-v11-n3-p04-p.pdf>.
   Section 1.1 defines the 12-fold symmetrization. Theorem 4.4 gives a
   construction using degree-at-most-three finite-type data of a Seifert
   spine. Theorem 4.7 bounds each variable's Laurent degree by twice genus.
   This is important computational progress; simply reusing its
   Kontsevich-integral input is not an independently justified geometric
   construction of the invariant requested here.
2. Lescop, *On the cube of the equivariant linking pairing for knots and
   3-manifolds of rank one*, arXiv:1008.5026,
   <https://arxiv.org/abs/1008.5026>.
   Theorem 1.1 constructs Q by equivariant triple intersections with a
   Pontrjagin correction; the knot version Q-hat is defined in Section 1.8.
   Theorem 9.2 proves comparison with the primitive two-loop Kontsevich
   part for knots with trivial Alexander polynomial in integral homology
   spheres. The paper does not prove the comparison for arbitrary knots.
3. Audoux–Moussard, *A universal finite-type invariant of knots in homology
   3-spheres*, Journal of Topology 18 (2025), e70036,
   <https://doi.org/10.1112/topo.70036>.
   Introduction and Section 2.5 explicitly distinguish the unknown general
   comparison of Kricker and Lescop invariants from their graded equality.
   Proposition 6.12 proves equality on the associated graded space, not
   equality of the invariants themselves.
4. Bar-Natan–van der Veen, *A Fast, Strong, Topologically Meaningful and Fun
   Knot Invariant*, arXiv:2509.18456v4, 6 May 2026,
   <https://arxiv.org/html/2509.18456v4>.
   Conjecture 25 is the equality of their theta with Ohtsuki's two-loop
   polynomial. Theorem 24 identifies a one-variable specialization with
   the Rozansky–Overbay invariant; it does not establish Conjecture 25.
5. Garoufalidis–Kricker, *Finite type invariants of cyclic branched covers*,
   Topology 43 (2004), 1247–1283,
   <https://people.mpim-bonn.mpg.de/stavros/publications/printed/finite_type_invariants_of_cyclic_branched_covers.pdf>.
   Cyclic-cover Casson–Walker invariants give sums of two-loop rational
   functions at roots of unity, after the signature correction. We examine
   the information loss of this type of sum below; numerical agreement of
   such sums is not a proof of equality of two-variable invariants.

Marché's 2005 preprint *An equivariant Casson invariant of knots in homology
spheres* is cited by Lescop and Ohtsuki. A primary full text was not found
in the author's current preprint/publication/notes pages. It is not used as
an equality theorem. A bibliographic mention is insufficient for a
zero-turn already-solved certificate.

**Gate decision:** no complete literature resolution has been certified.
Proceed with substantive proof attempts. The source/current-status audit
is not charged as a proof turn. Source PDFs, full-text reading copies,
catalogue corpora, browser artifacts and private coordination are excluded
from the public packet.
