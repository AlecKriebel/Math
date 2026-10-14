# Independent audit of the restricted terminal-time constructions

Audit date: 2026-10-14. Scope: mathematical checks within the same shared
PASS1, not an additional construction pass or historical-source audit.

Audited artifact: `../pass1_fixed_time/REPORT.md`.

SHA-256 at audit:
`dfb554c9156c7108ced1b169ae148b3d4dddfe970a2c8354d642994815128cda`.

## Result

No mathematical defect found in Sections 1–5. The weighted terminal
lemma, robust sole-deadline lemma, two-known-deadline theorem, and stated
sparse-deadline theorem are valid restricted results under the exact
king-move, Angel-first convention. The final three-time calculation is
correctly characterized as a failure of one sufficient estimate, not a
Devil win. These results do not establish unrestricted survival.

## Checks performed

1. **Ternary-square geometry.** A centered square of side `3q` partitions
   into nine disjoint squares of side `q`, whose centers have coordinate
   offsets in `{-q,0,q}`. The selected center is reached in exactly `q`
   legal king moves, including zero increments. Remaining time changes
   from `(3q-1)/2` to `(q-1)/2`. Thus each chosen endpoint square remains
   exactly reachable at the terminal time.

2. **Online information.** Least-density choices use the field already
   observed at each block boundary. The next block's updates need not be
   predicted; their total mass is charged at the declared rate. There
   are no unaccounted intermediate lethal times in this lemma.

3. **Terminal chronology.** If `L=3^k` and
   `w=T-(L-1)/2`, the nonfinal moves total
   `w+sum_{j=1}^{k-1}3^j=T-1`. Their corresponding Devil updates are all
   charged. The final choice is made after update `T-1`, and update `T`
   cannot retroactively kill it. When `w=0`, the initial observed field
   is simply zero; no round-zero Devil update is assumed.

4. **Strict weighted threshold.** The last average is at most
   `beta[w/L^2+1/2-3/(2L)]`. Here `0<=w<=L-1`, so for `beta<=2` it is at
   most `1-(L+2)/L^2<1`. The bracket is nonnegative. For `L=3` the sum
   over traversal scales is empty and the formula still agrees exactly.

5. **Preloaded reserve.** The robust lemma counts only already announced
   endpoint bombs in the initial square. All subsequently chosen
   terminal squares are nested inside it; outside bombs cannot affect
   the terminal endpoint. The criterion
   `m+w<(L^2+3L)/2` is precisely the strict inequality obtained from the
   final average. Its initial state is explicitly after the boundary
   announcement.

6. **Two-deadline smearing.** A later bomb contributes `1/D` at exactly
   `L^2` possible earlier centers. Because
   `D=C-w-1 >= (L^2+L)/2`, its total contribution is strictly less than
   two. Earlier bombs contribute at most one. Thus the weighted lemma
   applies to every adaptive mixed sequence. The earlier terminal
   inequality simultaneously ensures survival there and the integer
   reserve `b<=D-1` for the next time.

7. **Boundary announcement.** The announcement immediately after the
   first terminal move can add one later bomb, giving `m<=D`, hence
   `m+w<=C-1<C`. It has not been omitted or counted as visible before the
   earlier terminal move. For a one-round gap, `L=3,w=0,D=8`, so this
   reduces correctly to at most eight forbidden final neighbors.

8. **Infinite sparse-time strategy.** At a post-announcement time `s`,
   at most `s` distinct future bombs exist, so the robust lemma can be
   reset whenever `s+w<C`. Successive intervals contain no allowed
   intermediate lethal times. The prescribed infinite sequence and
   finite observed history determine every move, so no compactness or
   offline-path inference is involved.

9. **Numerical sufficient condition.** Substituting
   `L>(2r+1)/3` into `C-w=L^2/2+2L-r-1/2` gives the claimed strict lower
   bound `(2r+1)(r+2)/9`. For `T_j=2j^2`, the difference after substituting
   `s=2(j-1)^2,r=4j-2` is
   `(14j^2+24j-18)/9`, positive already at `j=1` and thereafter.

10. **Composition obstruction.** With weighted downstream rate `beta`,
    reserve and traversal accounting give
    `D_r(beta)=L^2-beta[w+1+(L^2-3L)/2]`. The stated update of `1/beta`
    follows algebraically. For gaps four, the rates are `81/53` and
    `81/25`; for first deadline thirteen the terminal coefficient is
    `4/9`, producing `36/25`. A bound exceeding one proves only that
    this estimate gives no certificate. The report preserves this
    distinction.

The accompanying `verify_bounds.py` also ran successfully: 20,000
remaining-time cases, 10,000 sparse-sequence cases, and the exact rational
three-time obstruction. These finite checks supplement the symbolic
proof; they are not evidence of general game solving.

## Limits

This audit does not authenticate the companion journal PDF or assert
novelty. It does not allow arbitrary detonation times, bombs at unlisted
intermediate times, or direct recursive composition beyond the proved
mass threshold. A resolution of the unrestricted conjecture still needs
a new simultaneous-time invariant or another complete strategy.
