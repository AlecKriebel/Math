# Scoped mathematical review of the symbolic threshold argument

Date: 2026-10-21 (UTC)

## Conclusion and scope

I accept the corrected mathematical argument in `UNIFORM_THEOREM.md`, Sections 3–11, as a symbolic proof of the stated lower-window capacity bounds for every integer r >= 378, conditional on the standard canonical Kruskal–Katona shadow framework and prescribed-profile criterion. I also accept the symbolic argument in `L4_PROOF.md` for every integer r >= 29 under those foundations. This is a reasoned mathematical assessment, not merely a report that sampled cases passed. One shadow-index notation error in Section 6 requires the explicit repair below; the proof of the full-state supersolution step survives that repair.

This review does not, by itself, accept the complete threshold theorem. It does not certify the finite bases, the prescribed-profile foundations, Sections 14–17, correspondence to the original problem, or a Lean build. No source programs were executed for this review, and no Lean compilation or axiom audit was performed by this reviewer. Separate arithmetic or CI evidence obtained elsewhere must retain its own provenance and limitations.

The reviewed source files are bound by these SHA-256 hashes:

- `UNIFORM_THEOREM.md`: `722c8c77c325806b25498c40e0e65f9d9c83b0f13ca26b733d818a7441255731`
- `L4_PROOF.md`: `85c2d5ffc0a5e67a0b9d31ccb16bc75872b1d4f3970539b9d964166f53af3312`

Public source context supplied for this review: https://github.com/mthiim/erdos_776/tree/v0.4.1-proof-claim . The hashes identify the actual local texts reviewed; they do not independently establish a remote commit identity.

## Required correction: shadowing the isolated active run

In the worked ordinary-extension calculation of Section 6, the isolated integer R_(j,L) is displayed as a cascade beginning at position u_j-L. The printed expression applies the shadow operator with index b_j-L to that integer and then shadows the displayed digits termwise. Those indices differ: b_j-u_j=h+j-1 > 0.

The correct isolated-run calculation is:

    shadow_(u_j-L)(R_(j,L))
      = sum_(p=0..L) C(s_j-1-p, u_j-L-p-1).

The next appended term is

    Q_(j,L) = C(s_j-L-2, u_j-2L-2).

Consequently,

    r + shadow_(u_j-L)(R_(j,L)) <= R_(j,L+1).

To justify the required full-state statement, let P_(j,L) denote the preceding anchor and completed-stone terms, and let V_(j,L)=P_(j,L)+R_(j,L). Their concatenation is canonical at index b_j-L. Shadow the entire list termwise. The prefix contributes its own shifted terms, while the suffix contribution is exactly shadow_(u_j-L)(R_(j,L)). The next prefix is the shifted old prefix, and Q_(j,L) >= r. Therefore

    r + shadow_(b_j-L)(V_(j,L)) <= V_(j,L+1).

This avoids assuming additivity of a fixed-index shadow operator on arbitrary sums. The repair is local to the displayed worked calculation. It does not require changing parameters, states, capacity bounds, or the theorem's range. The mathematical reason it works is canonical concatenation, not arbitrary linearity of shadows.

## Lower-window audit

### 1. Exact anchors and entry into the phased construction

At the top level, r-6 unary terms occupy positions 8 through r+1. Their shadow is C(r+2,2)-28. After adding r, the level-r state is C(r+2,r)+(r-28), with the residual represented by unary positions 28 through r-1.

At anchor q, write N=r-2q and B_q=T_q-2q. The unary block shadows to C(N,2)-C(B_q,2). Adding r gives C(N,2)+(r-T_(q+1)). Whenever r >= T_(q+1), this is the next anchor plus exactly the stated unary remainder. The anchor digits decrease by two; the unary block begins below the final anchor digit and occupies the remaining consecutive positions. Thus the termwise-shadow induction is justified canonically.

For the maximal t with T_t <= r < T_(t+1), the next residual is nonnegative and less than C(N,2), where N=r-2t. Rounding it to that binomial therefore gives a supersolution step by monotonicity. At the following level, the two initial active terms have value 2N-7, at least r under the stated growth bound.

The bound T_t >= 128t+250 holds at t=1 and is preserved by T_(t+1)=C(T_t-2t,2). It gives r >= 64(2t+3), with room to spare. It also ensures all anchor indices used before the phased region are positive.

### 2. Phase indices and paying the prescribed load

Put c=2t+3, h=t+2. The chosen K satisfies c*2^(K-1) <= r/4 < c*2^K and K >= 5. For ordinary phases, s_j=r+1-c*2^(j-1). Thus s_j >= 3r/4+1 for j<=K and s_(K+1)>=r/2+1.

The first active position is u_1=r-c-1. The exceptional first update gives u_2=floor(u_1/2)+1. Every subsequent ordinary update is u_(j+1)=ceil(u_j/2). These yield

    u_1/2^(j-1) <= u_j <= u_1/2^(j-1)+2,
    3c <= u_K <= 8c+2 <= r/8+2.

For later phases the birth invariant b_j-u_j=h+j-1 is preserved because a harvest lowers the level by ell_j+1 and lowers the new active position by ell_j+2. The preceding anchors and stones therefore end immediately above the active run. The active digits decrease by one and are strictly below the preceding completed stone.

During phase 1 an appended term has lower index at least 4, complementary index at least 2, and upper digit at least (N-1)/2. During later ordinary extensions the corresponding bounds are 4, 2, and r/2-3. Each appended binomial consequently exceeds r for r>=378. At harvest, completion of the shadowed run to its single binomial is an upper bound by the finite hockey-stick sum; the new active term separately exceeds r. Thus every extension and harvest pays the new load, using the full-state interpretation established in the correction above.

No interval is omitted: the extension states cover the levels from b_j to b_j-ell_j, and the harvest occurs at b_j-ell_j-1=b_(j+1).

### 3. Final rising tail and envelope seam

At the final harvest, the old phase-(K-1) run is completed, and the additional term C(s_K,u_K) alone exceeds r. The new tail lies immediately below it. Write u=u_K and D=s_(K+1)+2. Then

    s_K-D=c*2^(K-1)-2 > 0,
    D >= r/2+3,
    u <= r/8+2.

These imply validity of the initial tail digit D-u+2 at position u-1 and strict separation below s_K. The tail remains valid as its position decreases and its digit rises.

For p>=4, the gain in the tail when descending one position and raising its digit by one is C(d_p,p-2). Here d_p>=3r/8 and both indices are at least 2, so the gain exceeds r. For the last step, from position 3 to 2, raising the digit by two produces gain 2D-3 >= r.

After u-3 steps the final stone is at position 3 and the tail is at position 2. Since b_K-u_K=h+K-1, the level is L=h+K+2. Every earlier stone s_q occupies position L-h-q+1, agreeing with the envelope formula. The anchor block ends directly above the first stone. The terminal envelope digit lies below the preceding stone because the stone gaps exceed two. The bound L<r/4, while all tower digits are at least r/2+1, establishes digit-versus-position validity.

### 4. Exact envelope and anchor collision

Let m=i-h-1 at an envelope step. The changing bottom portion has difference

    C(s_(m-1)+2,2) - C(s_(m-1),2) - (s_m+2)
      = 2*s_(m-1)-s_m-1
      = r.

All earlier terms simply shadow. This proves the exact envelope recurrence, not merely an inequality.

At level t+5, the last anchor has digit N at position 4, followed by N-2 at position 3 and s_2+2 at position 2. After shadowing and adding r, the portion below C(N,3) becomes C(N,2), because

    (s_2+2)+r=2N-3=C(N,2)-C(N-2,2).

Pascal's identity merges these two terms to C(N+1,3), giving the advertised scalar state F_t(0).

### 5. Scalar collapse and terminal capacities

At scalar index q, the final ordinary anchor has digit a=r-2q+2 at position 4, followed by a-1 at position 3. After shadowing, completing C(a-1,2) to C(a,2) costs a-1. The incoming load and residual shadow leave

    z_(q-1)=r+shadow_2(z_q)-(a-1)
           =2q-1+shadow_2(z_q).

Pascal merging produces the next special position-3 digit. The residual remains canonical beneath it: for q>=6 the invariant z_q<=q^2 bounds its leading digit by 2q; for smaller q the explicit bounds make it at most 6, whereas the preceding digit is much larger for r>=378.

For q>=7 the shadow bound shadow_2(z_q)<=2q gives z_(q-1)<=4q-1<=(q-1)^2. From z_6<=36 one obtains successively z_5<=20, z_4<=16, z_3<=14, and z_2<=11. For t>=3 there is also z_2>=5, hence 7<=z_1<=9. Every integer in that last interval has 2-shadow 5, proving z_0=6. The direct t=1,2 cases give z_0=1,4.

At level 4 the state is C(r+2,4)+C(r+1,3)+z_0. One step gives C(r+3,3)+shadow_2(z_0)-1. This residual equals 1 when t=1 and 3 when t>=2. The next step gives C(r+4,2)-1 or C(r+4,2), respectively.

All preceding states have canonical leading digit r+2. Their canonical tail is strictly below C(r+2,i-1), making the full state less than C(r+3,i), and therefore below C(r+4,i). The level-3 and level-2 computations finish the remaining capacities. Monotonicity transfers all these upper bounds to the exact lower-window recurrence.

## L4 audit

The reverse bounding sequence is canonical throughout its specified range. The fifth large digit r-5 exceeds the corrector digit 23 when r>=29. The corrector disappears above its valid positions; the separately treated transition at i=29 supplies the appropriate new unary term rather than shadowing a zero binomial incorrectly.

For the reverse implication, it is essential to evaluate the shadow at G_i+1, not merely G_i. Appending the specified unary term makes the reverse-step margins exactly:

- 1 at i=3,4,5,6,7;
- r+135 at i=8;
- r+i-6 for 9<=i<=28, when these indices occur;
- r+23 at i=29, when this index occurs;
- r+i-5 for 30<=i<=r-2.

Each follows by termwise canonical shadowing and Pascal subtraction. Thus c_(i-1)<=G_(i-1) excludes c_i>=G_i+1 by monotonicity. Starting from the alleged bottom capacity, induction forces c_i<=G_i through i=r-2.

Independently descending the actual top chain gives

    c_r = C(r+2,2)+(r-1),
    c_(r-1) = C(r+2,r-1)+C(r,2)+r,
    c_(r-2) = C(r+2,4)+C(r,3)+C(r-2,2)+(3r-9).

The middle residual r has the canonical expansion (r-2)+1+1 in the stated consecutive positions; its shadow accounts for the final linear contribution. At level r-2 the reverse bound has the same first three terms, linear contribution 2r-9, and corrector C(23,r-7). Therefore

    c_(r-2)-G_(r-2)=r-C(23,r-7).

This is 6 for r=29, 29 for r=30, and r for every r>=31. All are positive, contradicting the reverse bound. This establishes symbolic L4 without using a finite stress test or assuming any intermediate capacity beyond the initial bottom-capacity hypothesis.

## Acceptance boundary

The accepted objects are the repaired lower-window symbolic proof for r>=378 and the L4 symbolic proof for r>=29. The Section 6 correction should accompany any acceptance claim about the human proof. This document does not assert that the entire source manuscript is error-free, independently peer-reviewed, or formally compiled. A complete threshold acceptance requires the separately audited foundations, finite certificates, final assembly, and original-statement correspondence.
