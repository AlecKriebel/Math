# Turn 3: a precise canonical gleam criterion and the failure of sign-only tests

**Scoped partial result; original Problem 12.11 remains unresolved after three substantive author turns.** This route leaves the long-filling approach and tests a direct combinatorial condition on the actual canonical gleamed knot shadow. It identifies exactly what the canonical gleams detect, recovers the credited alternating-diagram volume bound, and gives a knot-diagram countercontrol to a tempting weaker condition. The missing extension to more general or moved shadows is kept explicit.

## 1. Marked canonical shadows and the sign convention

Let D be a connected link diagram in a disk, with n>=1 ordinary crossings and its canonical shadow-cylinder data as in Thurston, printed p.351. Retain the planar support and its annulus attachments. The boundary marking identifies the actual link exterior; the auxiliary outer boundary is treated as in the source construction, not as an extra component of the target link.

Checkerboard-color the spherical complementary faces, choosing the outside face white. All black faces are then bounded disk regions whose gleams are part of the canonical data. At a crossing c, the two opposite black corners have the same half-corner sign; define epsilon_c in {+1,-1} to be twice this contribution. The white corners have the opposite sign. This is the checkerboard/Tait sign, up to one global convention change. It is **not** the oriented positive/negative crossing sign of a knot diagram.

For a black face B, let v_B be its number of corner incidences, with repetitions, and let p_B and m_B count its positive and negative corner incidences. Then

    2g_B = p_B-m_B,    v_B=p_B+m_B.                      (1)

A loop of the black Tait graph contributes twice to the corresponding black face's incidence counts. No step assumes a simple graph.

## 2. Saturation exactly detects alternation in this class

**Proposition.** For this marked canonical shadow, the following conditions are equivalent:

1. D is an alternating diagram.
2. All crossing signs epsilon_c agree.
3. Every black region satisfies |2g_B|=v_B.
4. The black gleams satisfy sum_B |g_B|=n.

### Proof

The signed Tait construction puts a vertex in each black face and an edge at each crossing. It is a connected plane graph because the projection is connected. Its signed medial graph reconstructs D. This standard construction is recorded explicitly in Moffatt, Section 3.1, properties T1–T3, printed p.1107.

For completeness, the local sign/alternation assertion can be seen without an oriented-link sign convention. Around a vertex of the Tait graph, label the two corners adjoining each incident edge as preceding and following in the planar cyclic order. At the corresponding medial crossing, the following corners at the two ends of that edge lie on one branch, while the preceding corners lie on the other. Choose one of these branches as over for epsilon=+1, and reverse the choice for epsilon=-1. A medial edge joins a following corner at one crossing to a preceding corner at the next. It therefore joins an overpass to an underpass exactly when the two signs agree. Since the medial projection is connected, alternation on every link arc is equivalent to all signs agreeing. A global reversal gives the same conclusion. This proves 1 iff 2.

Equation (1) gives |2g_B|=v_B if and only if all signs incident to B agree. If this holds for every black vertex, each Tait edge carries the common sign at both of its endpoints. Connectivity propagates that sign throughout the graph. Loops present no exception. Thus 3 implies 2, and the reverse implication is immediate.

Finally sum_B v_B=2n, because every crossing has two black corners. Each |2g_B|<=v_B. Equality in the sum occurs precisely when equality holds in each term, proving 3 iff 4. QED.

Define the nonnegative integer canonical gleam defect

    d_g(D)=n-sum_B |g_B|=sum_B min(p_B,m_B).              (2)

The second expression proves integrality and shows exactly how cancellation of corner contributions enters. It vanishes precisely for alternating diagrams. This is a statement about the retained canonical presentation, not a link invariant under arbitrary diagram or shadow moves.

## 3. The resulting genuine, but already-known, lower-bound subcase

Suppose in addition that the recovered diagram is prime and represents a hyperbolic link. Its twist number t(D) can be read from the marked planar support: join two crossings when they bound a bigon and take the maximal twist chains, with isolated crossings also counted. These are the same data as the degree-two planar regions in the canonical shadow, with the original source's twist-region convention.

If d_g(D)=0, the proposition proves that D is alternating. Lackenby's Theorem 1 therefore yields

    vol(S^3 minus L) >= (v_3/2)(t(D)-2).                 (3)

This is a valid shadow-data test on the stated canonical subclass, with an actual link-exterior identification. It makes no short-filling transfer and does not appeal to a volume bound for a different drilled manifold. The primeness and hyperbolicity conditions remain present. The formula can be zero for small twist number, exactly as in the credited original theorem; its useful growth parameter is twist count, not the raw crossing count.

Equation (3) recovers the alternating-diagram theorem already motivating Problem 12.11. It is not promoted to a solution of the intended general-shadow extension. The planar support, its checkerboard regions and the crossing-wise half-corner interpretation are additional structure. General efficient shadows or shadows after moves need not retain them, and their face gleams may no longer be sums of these particular corner signs.

## 4. All black gleams positive and all white gleams negative is too weak

Here is an exact knot-diagram countercontrol to replacing saturation by the signs of the total gleams.

Take the wheel plane graph with center 0 and rim 1,2,3,4. Its edges are

    a=01, b=02, c=03, d=04, e=12, f=23, g=34, h=14.

Use the planar cyclic orders

    0:(1,2,3,4), 1:(2,0,4), 2:(3,0,1),
    3:(4,0,2), 4:(1,0,3).

Give edge a sign -1 and every other edge sign +1. The black twice-gleams, in vertex order 0,1,2,3,4, are

    (2,1,3,3,3).

The four triangular white faces and the outer quadrilateral have twice-gleams

    (-1,-1,-3,-3,-4),

up to the order of the triangular faces. Thus every black total gleam is strictly positive and every white total gleam is strictly negative, including the outside face if it is recorded. Nevertheless the crossing signs are not uniform, so this diagram is not alternating. Its defect is 8-(2+1+3+3+3)/2=2.

This is a knot diagram, not merely a multi-component link example. The straight-through traversal of the medial graph, using the specified rotation system, has the single unoriented component whose crossing-visit word is

    a b f g d a e f c d h e b c g h.

Each crossing is visited twice. The two directed traversal cycles are reversals and exhaust all 32 directed medial half-edge states. Assigning all signs +1 makes the over/under visits alternate; changing only a breaks alternation at its adjacent arcs while keeping the same one-component projection. The exact checker constructs these permutations from the cyclic orders and verifies the statement without relying on a pictorial knot-name identification.

The claim is about this **diagram**. It does not assert that its underlying knot has no other alternating diagram, and it is not a counterexample to Problem 12.11. It shows that a coarse checkerboard sign test on aggregate gleams cannot replace the saturated local data even before generalizing away from planar canonical shadows.

## 5. What survives, and what is missing

The new mechanism gives an exact cancellation-sensitive criterion and a valid lower bound for the actual canonical presentation. Unlike a long-slope test, it really does include all prime hyperbolic alternating canonical diagrams. Its theorem is elementary and its volume input is credited prior work.

The original extension still requires a structure that makes sense after the planar support is lost, together with a theorem converting that structure into an essential-surface, guts, angle or other geometric lower bound. Simply asking for signs of face gleams loses necessary information, as the wheel control proves. Simply retaining the planar marking returns to Lackenby's original special case. Neither supplies the general efficient-shadow criterion asked for by the surrounding source motivation.

No sixth or uncounted proof route is hidden here: this is substantive turn 3, with the original general target unresolved. No novelty is claimed for the Tait construction, alternation criterion or known volume theorem.
