# Attempt 4: the logarithmic bound for every parallel family with rotating cubes

Date: 2026-10-20 UTC. Queue row 1825, ID 30002421.

## Result

If all positive-length supporting lines of A are mutually parallel, then the proposed lower bound holds for unrestricted-orientation cubes:

    D_rot(A) >= c log(L)/L,

with one universal positive c, for L>1. For 0<L<=1 the written right side is nonpositive. The constant is independent of the common direction, the line positions, and the number or lengths of their full chords.

This does not settle configurations with arbitrarily many directions. In combination with Attempt 2 it proves that test orientation genuinely changes the answer: the same oblique parallel line family has axis-parallel discrepancy O(1/L), but rotating-cube discrepancy at least c log(L)/L.

## 1. Weighted planar lemma

The companion authored note WEIGHTED_SQUARE_ROUTE.md supplies the following lemma, including closed-boundary cases:

For every set of m distinct points P⊆[0,1]^2 with m>=2,

    W_m(P) := sup_{closed squares S⊆[0,1]^2}
                    side(S) |#(P∩S) − m|S||
                 >= γ log m

for an absolute γ>0.

The nontrivial weight transfer is explicit. A small square is a signed combination of twelve squares of sides at least 1/10, with sum of coefficient magnitudes at most 6. This yields W>=ordinary-square-discrepancy/60 for interior points; boundary points are handled by a separate remove-and-compare argument. The ordinary planar square lower bound used is the established Halász/Ruzsa consequence of Schmidt's theorem, with an inspected proof in Matoušek §6.3.

A useful immediate extension is that for any T>=0,

    W_T(P) := sup_S side(S) |#(P∩S) − T|S|| >= W_m(P)/2.

Indeed the full square gives |m−T|<=W_T(P), while for every S of side s<=1,

    s |#(P∩S)−m s^2| <= W_T(P)+|m−T|s^3 <= 2W_T(P).

## 2. Inscribe an orientation-adapted cube

Discard repeated defining lines and lines with zero-length intersection with C before counting projections. This changes neither A up to an arclength-null set nor any discrepancy, and ensures that the subsequent line count uses distinct positive-length supporting lines.

Let u be the common unit direction. Choose an orthonormal frame whose third axis is u, and let P_box be the cube of side

    a = 1/(2 sqrt(3))

centered at (1/2,1/2,1/2), using that frame. Every vertex is at Euclidean distance sqrt(3)a/2=1/4 from the center. Thus P_box⊆C for every direction u, uniformly.

Identify its base square perpendicular to u with [0,a]^2. A supporting line intersects P_box exactly when its transverse projection belongs to that base square. Every such intersection is a full segment of length a, including lines on the side faces of the closed cube. Parallel distinct supporting lines have distinct transverse projections.

Let m be the number of these lines, and let P be their projections rescaled to [0,1]^2. Then

    H^1(A∩P_box)=am,
    |P_box|=a^3.

If D_rot(A)>=a^3/2, there is already a fixed positive discrepancy and the desired asymptotic lower bound follows, since log L/L<=1/e for L>1.

Otherwise, the test P_box gives

    |am/L−a^3| < a^3/2,

so in particular

    m > La^2/2.

Thus m grows proportionally to L when D is small. No estimate involving the original total number of chords is needed; short grazing chords elsewhere are irrelevant.

## 3. Reduce interior cubes to the weighted planar problem

Let S⊆[0,1]^2 be any closed square of side t. In P_box, choose a cube Q of side at whose transverse square is the scaled copy aS; any longitudinal interval of the same length inside the third coordinate range of P_box is admissible. Because the supporting lines are all parallel to the third axis,

    H^1(A∩Q)=at #(P∩S),
    |Q|=a^3 t^3.

Consequently

    |mu_A(Q)−|Q||
       = (a/L) t |#(P∩S)−La^2 t^2|.

Taking the supremum over S and applying the reference-coefficient variant of the weighted lemma yields

    D_rot(A) >= (a/L) W_{La^2}(P)
             >= (aγ/(2L)) log m.

For all sufficiently large L, the preceding lower bound m>La^2/2 gives log m >= (1/2)log L, and therefore

    D_rot(A) >= (aγ/4) log L/L.

All constants are universal because a is fixed. The finitely bounded regime 1<L<L_0 is covered by the unconditional bound of Attempt 3, reducing the universal c if necessary. For example, the ratio of that bound to log L/L is at least 1/(16 log L_0) on this interval.

## 4. Why oblique torus-flow examples do not contradict this theorem

Every A_n in Attempt 2 consists of parallel lines with direction α=(sqrt(2),sqrt(3),1). Here the test cube P_box is aligned with α, not with C's axes. Its side-face normals are perpendicular to α. Borda's bounded-error theorem specifically excludes such normals, and does not give a uniform bound as orientations approach them.

An explicit excluded algebraic normal is

    ν=(sqrt(3),−sqrt(2),0),   ν·α=0.

Thus the distinction is supported both by the elementary reduction and by the exact hypotheses of the continuous-flow theorem.

## 5. Remaining obstruction

For nonparallel lines, a line's length inside an orientation-adapted cube is no longer side(Q) times a planar point indicator. Projecting all lines onto a plane produces projected segments, not point masses, and taking an arbitrary cross-section assigns weights and geometric truncations that depend on the test cube. Those replacements would change the theorem.

Even isolating a subset of many almost-parallel lines does not automatically give a lower bound for the whole positive measure: its signed discrepancy relative to volume can be canceled by contributions of the other lines. The present proof avoids such cancellation only because every line has the same direction. No extension to a general finite union is claimed.

## Public references

- Original problem: https://ems.press/journals/owr/articles/12723
- Original report PDF: https://ems.press/content/serial-article-files/46480?nt=1
- Inspected planar square proof: https://people.fjfi.cvut.cz/vybirja2/TUM-IBC/Matousek_Geometric_Discrepancy.pdf
- Borda theorem: https://arxiv.org/html/1803.06968
