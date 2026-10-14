# Restricted fixed-time and two-time online strategies

## Result and scope

This report gives independent, fully online proofs in the exact two-dimensional king-move model of the shared construction contract for:

1. One known common detonation time.
2. Two known allowed detonation times, with arbitrary separation.
3. A known infinite sequence of sufficiently separated allowed detonation times, including `T_j = 2 j^2`, `j >= 1`.

These are restrictions on the Devil's allowed time coordinates. They do **not** resolve the unrestricted Time-Bomb conjecture. The constructions tolerate adaptive announcements, repeated positions and times, and Devil announcements after observing the Angel's current move. No offline safe-path inference is used. The strategy only inspects finite, already observed announcements.

The single-time and two-time conclusions were already suggested by an unauthenticated third-party transcription of Bollobás–Leader, *The Angel and the Devil in three dimensions*, JCTA 113 (2006), 176–184, DOI `10.1016/j.jcta.2005.03.009`. It labels the first conclusion Proposition 6 and states the second without a proof. The publisher/author PDF was unavailable to this research pass. That transcription is a lead, not proof authentication. The arguments below are independently supplied; no novelty claim is made for any result.

## 1. Weighted terminal-hazard lemma

A nonnegative hazard field is a finitely supported function `f : Z^2 -> [0,infinity)`. Between Angel moves, an adaptive adversary may increase this field by a nonnegative function of total mass at most `beta`. There are no intermediate lethal times. The terminal goal, at a known time `T >= 1`, is to choose a position `a_T` with `f(a_T) < 1`, where `f` includes all updates through round `T-1` but not the update after move `T`.

**Lemma 1.** Starting with the zero field at time 0, the Angel has such an online strategy for every `0 <= beta <= 2`.

### Construction and proof

Let `L = 3^k` be the largest power of 3 satisfying `L <= 2T+1`, and put

- `R = (L-1)/2`,
- `w = T-R`.

Since `T >= 1`, `L >= 3`. Since `2T+1 < 3L`, integrality gives `0 <= w <= L-1`.

Stay at the initial position for `w` moves. This is safe because there are no intermediate lethal times. After the round-`w` update, consider the square `S` of side `L` centered at the current position. There are exactly `R` moves remaining. Its average hazard is at most `beta w / L^2`.

Whenever the current square has side `3q >= 9`, partition it into its nine disjoint, axis-aligned squares of side `q`. Choose one whose average hazard is no greater than the current square's average, breaking ties lexicographically. Its center differs from the current center by a vector with both coordinates in `{-q,0,q}`. Reach it in exactly `q` king moves, using the corresponding constant coordinate increments in `{-1,0,1}`. All these moves are legal, and there is no lethal intermediate time.

The remaining time changes from `(3q-1)/2` to `(q-1)/2`, exactly as required. During the `q` traversal rounds the total new hazard anywhere is at most `beta q`, so the average in the chosen square increases by at most `beta/q`. Changes outside it need not be counted.

Repeat until the current square has side 3 and exactly one move remains. Its average hazard is at most

`beta [ w/L^2 + 1/3 + 1/9 + ... + 3/L ]`

`= beta [ w/L^2 + 1/2 - 3/(2L) ]`.

For `L=3` the displayed geometric sum is empty and is zero, agreeing with the formula. Because `w <= L-1` and `beta <= 2`, the bound is at most

`1 - (L+2)/L^2 < 1`.

All nine squares are reachable on the final king move. At least one has hazard strictly below 1. Choose the lexicographically first such square. Its hazard is known before making that final move. This proves the lemma against every adaptive sequence of updates. Staying and the constant-increment traversals are legal moves under the contract.

**Timing check.** The first `w` moves and all block traversals occur strictly before `T`. The last current field is the field after round `T-1`. There is no assumed ability to observe or evade the announcement made after the terminal move.

**Corollary 1.** With all bombs restricted to a single known time `T`, the Angel wins. Let `f` be the indicator of positions already bombed for time `T`. Each announcement increases its total mass by at most 1, and `f(a_T)<1` means the terminal position is unbombed. All subsequent times are harmless.

## 2. Robust terminal lemma with preloaded bombs

The relevant number of preloaded bombs is local, not the total number on the board.

**Lemma 2.** Suppose the Angel has just observed the announcement at a time `s`, is at `a`, and the sole lethal time strictly after `s` under consideration is `s+r`, where `r >= 1`. Let

- `L = 3^k <= 2r+1 < 3^(k+1)`,
- `R = (L-1)/2`,
- `w = r-R`,
- `S_a = a + [-R,R]^2`,
- `C = (L^2+3L)/2`.

If the number `m` of already announced bombs for time `s+r` at distinct positions in `S_a` satisfies

`m + w < C`,

then the Angel has an online strategy surviving `s+r`, provided there are no other lethal times in `(s,s+r)`.

**Proof.** Use the same wait and nested-square construction. Bombs outside `S_a` never affect this construction. At the end of the wait, the initial square has at most `m+w` relevant bombs. The final side-3 square has marked density at most

`(m+w)/L^2 + 1/2 - 3/(2L) < 1`.

The final move is therefore safe. Every later announcement during the construction is already accounted for at rate one. The count `m` is taken after the round-`s` announcement; there is no omitted announcement at the boundary. Repeated pairs only reduce the rate of increase.

## 3. Two arbitrary known detonation times

**Theorem 1.** If the Devil may announce only bombs whose time coordinates are two fixed known integers `U < V`, then the speed-one Angel wins in two dimensions.

### Proof

Set `r = V-U` and define `L,R,w,C` as in Lemma 2 for this gap. Define the positive integer

`D = C-w-1`.

The elementary bound `w <= L-1` gives

`D >= (L^2+L)/2 > L^2/2`.

For the first phase, before time `U`, maintain the observed sets `B_U` and `B_V` of positions already bombed at those two times. Define a hazard field on all positions `a` by

`f(a) = 1_{B_U}(a) + |B_V intersect (a+[-R,R]^2)| / D`.

This field is nonnegative, finitely supported, and initially zero. A new time-`U` bomb adds mass at most 1. A new time-`V` bomb belongs to exactly `L^2` of the translated squares, so it adds total mass at most

`L^2/D < 2`.

An already announced duplicate adds no mass. Consequently every announcement adds total hazard mass at most 2, regardless of which of the two time coordinates the Devil chooses. Apply Lemma 1 with terminal time `U`. It produces a position `a_U` with `f(a_U)<1`, based on announcements only through round `U-1`.

First, `a_U` is not in `B_U`, so the Angel survives time `U`. Second, if `b` is the current number of time-`V` bomb positions in `S_{a_U}`, then `b < D`. Since `b,D` are integers, `b <= D-1`.

The Devil now makes its round-`U` announcement. It can increase the number of time-`V` bombs in that square by at most one, giving `m <= D`. Thus

`m+w <= D+w = C-1 < C`.

Lemma 2 now applies from the post-announcement time-`U` state and guarantees survival at `V`. There is no other lethal time strictly between `U` and `V`. After `V`, every allowed bomb time is past, so the Angel survives forever. This is one perfect-information strategy, not a trajectory chosen after the announcements.

## 4. A valid infinite sparse-time extension

**Theorem 2.** Let `0=T_0<T_1<T_2<...` be a known increasing sequence. For each `j`, put `s=T_(j-1)`, `r=T_j-s`, and define `L,w,C` as in Lemma 2. If

`s+w < C`

for every `j`, then the Angel wins against every adaptive Devil whose bomb times lie in this sequence.

**Proof.** At the post-announcement state at time `s`, at most `s` bombs have been announced in total. In particular, the number for `T_j` in the relevant square is at most `s`. There is no allowed lethal time strictly between successive sequence elements. Lemma 2 therefore guarantees survival at the next sequence element. Reset there, after its announcement, and continue. Each decision uses only the prescribed sequence and the finite history. The intervals cover all nonnegative times, so this constructs a single infinite online strategy.

A convenient sufficient numerical condition is

`s <= (2r+1)(r+2)/9`.

Indeed,

`C-w = L^2/2 + 2L-r-1/2 > (2r+1)(r+2)/9`,

where strict inequality follows from `L > (2r+1)/3` and monotonicity of the expression in `L`. Thus the sufficient condition implies `s+w<C`.

**Example.** The known allowed times `T_j=2j^2` satisfy the sufficient condition. Here `s=2(j-1)^2`, `r=4j-2`, and the right side minus `s` is

`(14j^2+24j-18)/9 > 0` for `j>=1`.

This infinite family remains a proper restriction of the Devil's legal time coordinates. It neither covers arbitrary times nor handles intermediate lethal times omitted from the prescribed sequence.

## 5. Exact obstruction to the simplest further composition

The two-time proof uses the spare mass budget in Lemma 1. A future terminal bomb is converted into a spatial hazard of total mass below 2. Repeating this smoothing can exhaust that budget; “below 2” cannot simply be carried through another stage unchanged.

For a gap `r`, let `L,w` have the usual meanings and define

`A_r = w+1+(L^2-3L)/2`.

Suppose a downstream terminal hazard receives at most `beta` total new mass per round. A direct application of the same uniform-square construction, reserving `beta` for the boundary announcement, allows initial local hazard mass strictly below

`D_r(beta) = L^2-beta A_r`.

When this denominator is positive, converting that local-mass condition into a new hazard multiplies each downstream update's total mass by `L^2/D_r(beta)`. Its new worst-case mass bound is

`beta' = beta L^2 / [L^2-beta A_r]`,

or equivalently

`1/beta' = 1/beta - A_r/L^2`.

This is an exact accounting identity for this particular sufficient-condition construction, not a lower bound on every strategy.

**Concrete failure of the bound.** For a gap of 4, `L=9`, `w=0`, and `A_r=28`. Starting from unit bomb mass, two such smoothing stages give

`beta_1=81/53`, then `beta_2=81/25 > 2`.

For a first deadline of 13, its ternary-square estimate has coefficient `1/2-3/(2*27)=4/9`. Thus the composed terminal hazard bound becomes

`(81/25)(4/9)=36/25 > 1`.

Accordingly, this direct composition does not certify the three known allowed times `{13,17,21}`. This is **not** a Devil strategy, not a loss result for three times, and not evidence that the full conjecture is false. It pinpoints a failure of the proposed invariant's estimate.

The other obstruction is even more basic: in a multi-time game, one cannot execute a terminal-only block traversal while ignoring bombs at intervening times. The two-time construction explicitly avoids that problem by making the first terminal choice a certified safe starting state for the second phase. A proposed full-game extension must supply comparable simultaneous protection for every intermediate time; the terminal lemma alone does not do so.

## 6. Source and audit boundary

- Exact game conventions: the shared `CONSTRUCTION_CONTRACT.md`, independently recovered from Leader's OWR 1/2006 contribution, printed page 22 / PDF page 18, Conjecture 1.
- Public historical source: Imre Leader (joint with Béla Bollobás), in *Combinatorics*, Oberwolfach Reports 3 (2006), no. 1, DOI https://doi.org/10.4171/OWR/2006/01 ; official report https://ems.press/content/serial-article-files/46029?nt=1 .
- Companion bibliographic lead: Béla Bollobás and Imre Leader, JCTA 113 (2006), 176–184, DOI https://doi.org/10.1016/j.jcta.2005.03.009 . The unauthenticated Scribd transcription was used only to identify restricted propositions worth reconstructing. Its source text is not reproduced here.
- All arguments in Sections 1–5 are authored derivations. No publisher-PDF proof verification, exhaustive strategy search, novelty assertion, or resolution of the unrestricted conjecture is claimed.
- Supplementary exact-arithmetic checks in `verify_bounds.py` test the formulas and boundaries; they are not substitutes for the proofs above.
