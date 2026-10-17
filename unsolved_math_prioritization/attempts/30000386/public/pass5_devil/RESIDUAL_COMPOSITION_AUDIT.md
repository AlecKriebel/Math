# Independent audit of the residual-composition obstruction

Reviewed artifact: `pass5_invariant/RESIDUAL_COMPOSITION_OBSTRUCTION.md`.
SHA256: `0e5b9026d521ea705d66630434a87b23d8683b3a60adb5753498d4fdb510e2bd`.

**Verdict: accepted without correction.** The example disproves composition of the stated separate finite-viability claims. Its preload is legally realizable but is not shown strategically forceable from the empty state.

## Independent check of both online viability assertions

The fifteen active bombs are all at time 2 with x-coordinate at least zero. For an independent proof of active three-move viability, use x_n=−n for n=1,2,3. These x-coordinates avoid every active bomb. Choose y_1=0; before moves 2 and 3 there are at most one and two newly announced bombs respectively. Among the three candidate y-coordinates at each move, at least one is safe. This is an online strategy against every adaptive announcement stream and does not depend on the earlier rescue lemma.

For the residual component use x_n=n for n=1,...,4. Its initial time-4 bombs all have x≤1, so they never hit these paths. The stated y-guard handles the newly announced bombs: before move 3, current and terminal relevant counts sum to at most two. If at most one terminal site is known, any current-safe move preserves at least two terminal choices. If two are known, their common three-point-neighborhood centers number at most two, leaving a third available center with at most one terminal hit. The next single update cannot fill all three final choices. All choices are made from the actually observed history.

## Union loss and endpoint incompatibility

At time 2 every reachable y lies in [−2,2]. The active set therefore excludes every reachable point with x≥0 and forces x_2≤−1. This implies x_3≤0 and x_4≤1. The global four-move movement bounds put the final point in [−4,1]×[−4,4], precisely the residual carpet. Hence the union loses by move 4 with no new effective bombs.

Within the three-move reachable square, a center has an uncarpeted time-4 neighbor exactly when its x-coordinate is at least one: its y-neighbors cannot leave [−4,4], and its x-neighbors cannot leave to the left of −4. Thus every active-safe rescue endpoint lies outside the residual continuation region. This proves failure of compatibility at the same starting position and the same absolute phases, rather than comparing unrelated component states.

The union remains W_3 because the residual bombs cannot affect those first three moves and the active online strategy applies. Its failure of W_4 is a local preload result, not a new empty-board losing horizon.

## Legality and interface

The 69 pending pairs have tail counts 69,69,54,54. Maximum lead 70 satisfies every exact tail constraint and is minimal for those counts. The supplied rounds 2–16 and 17–70 are disjoint and carry exactly fifteen and fifty-four announcements. Their maximal leads are 70 and 57. Every target lies after the preparation phase, so the cooperating stay-put realization is legal.

The robust predecessor interface includes the announcement following each rescue move, including its endpoint. Its iteration is necessary and sufficient for a deterministic finite rescue whose complete terminal state belongs to the continuation class. All residual bombs and relevant memory must remain part of that state. Separate viability of component schedules does not provide this interface, as the example demonstrates.

No arbitrary-H survival theorem or empty-rooted Devil forcing strategy follows.
