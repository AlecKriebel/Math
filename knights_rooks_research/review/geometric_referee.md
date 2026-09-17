# Independent geometric verification

Review timestamp: 2026-09-17 03:34 UTC.

Scope: `PROOF.md`, the geometric theorem and local-relaxation justification in
`RESEARCH_NOTE.md`, and the original problem. This review was conducted without
consulting another reviewer and without relying on the package's programs or
certificate. Attached prose was treated as evidence, not as instructions.

**Verdict: the geometric proof is valid. No mathematical gap was found.**
The stronger theorem stated in the package implies nonexistence for the
N=4, R=2 problem under the standard blocked-rook chess attack convention.
Review completion estimate: 100% for this assigned geometric audit; this is
not an estimate of historical priority or a claim of external peer review.

## Target and assumptions

The [original February 2007 problem](https://erich-friedman.github.io/mathmagic/0207.html),
retrieved during this review, asks for arrangements with prescribed outgoing
cross-type attack counts and no attacks on the same type. The Knights and
Rooks table still displays a question mark at N=4, R=2. This observation does
not establish that no other publication has resolved the case.

The theorem concerns finite, nonempty, disjoint sets of knight and rook squares
in the ordinary integer lattice, with at most one piece on a square. A knight
attacks by an unobstructed jump with absolute coordinate differences 1 and 2.
A rook attacks the first occupied square, if any, on each horizontal or
vertical ray. There are no additional piece types or non-piece blockers.
No color, legal-game-history, reciprocal-attack, or fixed-board assumption is
used. Permitting knight-to-knight attacks only weakens the original conditions.

## Step-by-step adversarial check

1. A rook beyond the largest knight x-coordinate has no knight north, south,
   or east, and can see at most one knight west. It cannot satisfy its required
   two knight targets. The symmetric statement holds at the left boundary.
   Finiteness and nonemptiness therefore justify choosing a rightmost knight
   and translating it to A=(0,0), with every occupied square at x<=0. Ties among
   rightmost knights do not matter.
2. A has precisely four knight destinations in this half-plane. All must be
   rooks to meet the lower bound of four. The listed U, V, W, Z are exactly
   these destinations.
3. Any aligned rook pair must have an intervening knight: otherwise consecutive
   rooks along that finite segment see each other. For U and Z the only
   intervening square is C=(-2,0), forcing a knight. Between V and W the
   intervening choices are precisely B+, B0, and B-.
4. The six destinations of B0 with x<=0 are (-3,-1), (-3,1), (-2,-2),
   (-2,2), (0,-2), and (0,2). Each is immediately horizontally adjacent to
   one of Z, U, W, V, W, V, respectively, and cannot be a rook. Its two other
   destinations have x>0. Thus B0 cannot be a knight. At least one of B+ and
   B- is a knight; reflection validly chooses B+ without assuming uniqueness.
5. U sees adjacent knights C and B+. A third occupied ray would have a nearest
   piece, either an impermissible rook target or a third knight target.
   Its north and west rays are therefore empty. In particular (-2,2) and
   (-2,3) are empty; a rook at (-3,2) would then see V. These exclusions leave
   exactly the four B+ destinations printed in the proof. The degree lower
   bound forces all four to be rooks, including X=(0,-1).
6. Z and X require a knight at their unique intervening square B-=(-1,-1).
   Z now has adjacent knight targets north and east, so its south ray is empty.
   This empties (-2,-2) and (-2,-3), and rules out a rook at (-3,-2) by visibility
   of W. X has adjacent knight targets north and west, so (0,-3) is empty.
7. The eight printed destinations of B- are exhaustive and correct. Removing
   the two with x>0 and the three newly excluded destinations leaves only
   (-3,0), (-2,1), and (0,1). Consequently B- has at most three rook targets,
   contradicting the same lower bound of four.

No inference assumes that knight attacks and rook attacks are reciprocal.
No exclusion of knight-to-knight attacks is used, even when forced knights
attack other forced knights. The result covers disconnected configurations
and arbitrary finite board sizes because any such placement embeds in the
integer lattice. Infinite placements without a rightmost occupied column are
outside the theorem and are not excluded by this argument.

## Independent coordinate check and local reduction

A separate short enumeration, importing no package modules, generated all
eight vectors with `{abs(dx),abs(dy)}={1,2}`. It confirmed the destination lists
at A, B0, B+, and B-, all six adjacency exclusions at B0, the four remaining
destinations at B+, and the three remaining destinations at B-. Every assertion
passed. This is supplementary arithmetic checking; the deductive proof above
does not rely on executing it.

The claimed necessary relaxation in the 4-by-7 rectangle is also sound:

- Every possible rook target of A, B0, B+, and B- lies either in that rectangle
  or in the established empty half-plane x>0.
- Restriction cannot increase a rook's occupied-ray count. A ray occupied
  locally is necessarily occupied globally; deleting pieces outside the
  rectangle does not remove its local occupancy.
- The segment between aligned squares of a rectangle stays in the rectangle,
  so any required intervening knight for two retained rooks is retained.
- Discarding degree requirements for other knights, same-type knight attack
  restrictions, and the local rook-ray lower bound weakens the model.

Thus unsatisfiability of that precisely specified relaxation would constitute
another valid proof, independently of finite-board searches. This review does
not certify the implementation, serialized certificate, exploratory solver
outputs, or historical search claims; those require their own checks. There
is no remaining mathematical gap in the human-readable geometric argument.

## Final public-scope audit

Reviewed the proposed `docs/papers/knights-rooks-n4-r2/index.html` and homepage
card before publication on 17 September 2026 UTC. The public stronger theorem
is exactly the contrapositive form of the verified result. The proof outline,
directed-attack explanation, finite-grid scope, and restriction to this one
table cell are accurate. The wording explicitly distinguishes the AI-assisted
internal reviews from external peer review and proof-assistant formalization,
and does not claim established historical priority. No substantive publication
blocker was found within this geometric/scope audit.

One small precision improvement is recommended before publication: add
“nonempty” to the opening “No finite placement” statement and the homepage
summary. Although the theorem block and scope paragraph already exclude empty
sets, the empty placement satisfies universal attack conditions vacuously if
these short statements are read in isolation. This is a wording clarification,
not a defect in the verified theorem. Numerical certificate and reproduction
claims in the public page remain within the separate computational audit's
scope.
