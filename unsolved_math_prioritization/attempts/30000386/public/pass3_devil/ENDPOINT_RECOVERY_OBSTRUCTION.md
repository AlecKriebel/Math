# Endpoint recovery obstructs small tracking repairs of interpolated random blocks

## Scope

This is an adversarial test of the current hidden-block coupling proposal. It does not defeat unrestricted Angel strategies. Its content is that linear interpolation of a fresh private endpoint, repaired only by a sub-square-root tracking error, cannot simultaneously guarantee survival against arbitrary short-lead announcements. The Devil strategy is constructed online from actual observed positions; it is not a preloaded-state argument.

## 1. General endpoint-covering principle

Suppose that after the Angel's move at a time m<T, the observed history determines a finite set C of at most T−m cells. Suppose every continuation satisfying a proposed tracking/transition guarantee has its time-T endpoint in C. Then the Devil can force either a violation of that guarantee or a collision by time T.

Indeed, enumerate C and announce its cells, one in each successive round beginning with m, all with time T. There are enough announcement rounds m,…,T−1. Every listed announcement is strictly earlier than T. The same list may instead be held until the final |C| rounds T−|C|,…,T−1, because C was already determined by time m. This version uses announcement leads at most |C|. Additional announcements, when needed, may be irrelevant. If the continuation keeps the guarantee, its terminal cell is bombed; otherwise the guarantee has failed. This construction uses neither future observations nor stored announcement credit.

The principle does not say that the Devil can force the Angel to keep the guarantee. An unrestricted Angel may escape C by violating the proposed transition rule.

## 2. A fresh random endpoint with linearly interpolated motion

Consider a block starting at time s, of even length L, ending at T=s+L. Let its reference path be

    b_(s+r)=b_s+(floor(r D_x/L), floor(r D_y/L)),
    0≤r≤L,

where D is any integer vector in [−L,L]². D may be sampled privately at the start of the block. The Devil does not need to know it. These reference increments are legal king steps, including for negative D.

Write m=s+L/2. The exact integer identity is

    b_T−2b_m+b_s ∈ {0,1}².                                  (1)

Suppose actual positions a_s,a_m,a_T satisfy

    ||a_u−b_u||_∞≤R    for u∈{s,m,T},                       (2)

where R is a nonnegative integer. No assumption is imposed on how the Angel reacts to bombs between these three times.

The Devil has observed a_s and a_m by round m. Combining (1) and (2) gives

    a_T ∈ (2a_m−a_s)+[−4R,4R+1]².                         (3)

The integer square in (3) contains exactly

    M=(8R+2)²

cells. Therefore, whenever

    (8R+2)²≤L/2,                                            (4)

the endpoint-covering principle supplies a legal adaptive Devil which forces either a tracking error exceeding R at one of s,m,T or a collision at T.

**Derivation of (3).** Put e_u=a_u−b_u. Then

    a_T−2a_m+a_s
       =(b_T−2b_m+b_s)+(e_T−2e_m+e_s).

The first term lies in {0,1}² and each coordinate of the second lies between −4R and 4R. The set in (3) thus covers every possible private D and every subsequent reaction that keeps (2).

If the reference block starts exactly at the actual position, so b_s=a_s, the sharper square is

    (2a_m−a_s)+[−3R,3R+1]²,

with M=(6R+2)². Its announcement capacity condition is correspondingly (6R+2)²≤L/2.

## 3. Consequence for tracking-based block transitions

For any family of block lengths tending to infinity, R=o(sqrt(L)) eventually satisfies (4). Thus no transition guarantee that simultaneously promises survival and an o(sqrt(L)) tracking error at the block's start, midpoint and endpoint can hold for every legal short-lead Devil, for these linearly interpolated reference blocks.

This conclusion allows arbitrary adaptive changes to the actual path between observation times. It allows D to remain private. The endpoint square is computed from actual positions, not by decoding the private vector exactly.

The Devil can compute the square at the midpoint and wait until rounds T−M,…,T−1 to announce it. Thus the attack uses only announcement leads at most M=(8R+2)², or M=(6R+2)² for actual-start anchoring. All these rounds lie in the second half of the block. In particular a fixed tracking radius is defeated with a fixed bounded lead, independently of the growing block length. There are no auxiliary lethal preloads. Before this attack the Devil may announce irrelevant pairs. If a tracking failure already occurred at an observation time, that is already a failure of the proposed transition guarantee; otherwise the terminal carpet is valid.

Spreading the reference motion across the whole block therefore does not by itself repair the move-then-hold construction's vulnerability. A successful coupling must avoid the endpoint-recovery implication, permit larger corrections while controlling them more finely, or change the reference/transition design.

## 4. Why the naive bounded-repair probability budget then fails

The following limitation concerns a common sufficient bound, not the actual probability of survival.

If a reference endpoint is X=D+Z, where D is uniform on [−L,L]² and independent of Z under the relevant earlier conditioning, and the actual endpoint Y obeys ||Y−X||_∞≤R, then

    P(Y=p) ≤ (2R+1)²/(2L+1)².                              (5)

The correction may depend on D, the observed path, and the bombs. To prove (5), the event Y=p implies X∈p+[−R,R]²; conditioning further on Z leaves at most (2R+1)² possible values of D. This argument concerns unconditional probabilities under the original conditioning; conditioning on a tracking-good event is not justified unless that conditioning is separately handled.

Without additional structure on the correction, the factor (2R+1)² is sharp: with Z=0, map every D∈[−R,R]² to Y=0 and leave all other D unchanged. The correction is bounded by R and gives exactly that point mass at zero, provided R≤L.

Now consider a block proof charging L_(j−1) earlier announcements using a fresh length-L_j endpoint and the bound (5). Its charged block cost is

    A_j=L_(j−1)(2R_j+1)²/(2L_j+1)².

To keep the interpolation tracking guarantee available against the attack above at arbitrarily large blocks, its necessary radius scale is R_j=Ω(sqrt(L_j)). For large L_j, this makes A_j bounded below by a positive constant times L_(j−1)/L_j. If adjacent block ratios are bounded above, these charged costs are not summable.

This applies in particular to the comparable-length blocks used in the accepted logarithmic-delay construction. It explains why that construction cannot simply add a universally small bounded tracking repair and reuse the same worst-case point-mass union bound unchanged.

The conclusion is only about this certificate. Large adaptive corrections might preserve spread through an injective or otherwise controlled transport map; a nonlinear or history-sensitive probability argument might charge far less than (5). Also, this argument does not assert a contradiction for every possible rapidly growing block schedule.

## 5. Exact boundary

What is proved is a legal adaptive endpoint-covering attack on a specific promised block property, and a corresponding obstruction to one generic probability-budget argument. No unrestricted finite-time Devil trap is established. In particular, the Angel can escape the announced terminal square by abandoning close tracking; the unresolved question is how to do so while retaining the spread needed to control older announcements.
