# A bounded tracker for all announcement leads at most fifteen

Status: authored PASS3 partial theorem, submitted for independent audit. The unrestricted Time-Bomb game is not resolved. No novelty claim. The game and turn order are exactly those in `CONSTRUCTION_CONTRACT.md`.

## 1. Statement

A short announcement made after the Angel move in round r has target time t with 1 <= t-r <= 15. Other announcements can be present but are ignored by the controller below. They still consume their one-per-round announcement budget. For the purposes of this theorem the hypothetical path is continued through any collision with an ignored announcement.

Let z_0,z_1,... be any real-valued reference path in R^2 with z_0=(0,0) and

    ||z_n-z_(n-1)||_2 <= 1/100.

There is an online controller, using only the next reference point z_n and previously announced short bombs, which produces legal king moves a_n, avoids every short bomb, and satisfies

    ||a_n-z_n||_2 < 80  for every n>=0.

The reference points may be supplied successively. The result holds against every adaptive short-bomb stream, including one responding to all observed positions. No stochastic assumption is used in the tracking result.

## 2. A geometric guard

Write N(a)=a+{-1,0,1}^2. Before move n let A_n be the short-bomb sites at time n and B_n those at time n+1. Define m_n=|A_n intersect N(a_(n-1))| and b_n=|B_n|. Duplicates are counted once. All bombs in A_n or B_n were announced in rounds n-15,...,n-1, so

    m_n+b_n <= |A_n|+|B_n| <= 15.                 (1)

Negative or zero announcement rounds contribute nothing.

Maintain the invariant m_n<=8. It holds at the initial move. An admissible guard move q is a point of N(a_(n-1)) which is not in A_n and satisfies

    |B_n intersect N(q)| <= 7.                   (2)

Such a move exists whenever (1) and m_n<=8 hold. Indeed, the accepted geometric lemma says that for any nonempty Q subset N(a), if every q in Q has at least eight neighbors in a finite set B, then |B|>=|Q|+7. Apply this with Q=N(a) minus A_n. Failure of every Q move would give b_n>=9-m_n+7, contradicting (1).

After an admissible move the Devil adds at most one new short bomb at time n+1. Thus the next neighborhood contains at most eight such bombs and the invariant continues. This proves immediate short-bomb safety.

For completeness the geometric lemma follows from elementary expansion. If Q has k points, r occupied rows and c occupied columns, then |Q+{-1,0,1}^2|>=k+2r+2c+4>=2k+7, because k<=rc<=2r+2c-3 for 1<=r,c<=3. Each neighborhood has at most one point missing from B. Assign each missing point of the union to a containing neighborhood; these assignments are injective into Q. At most k points of the union are missing, giving |B|>=k+7.

The same lemma bounds the number r_n of moves excluded by failure of (2): if r_n>0, then b_n>=r_n+7. Therefore at most

    m_n + max(0,b_n-7)

moves are excluded. If b_n>=8 this quantity is at most eight by (1); if b_n<=7 it equals m_n<=8.

## 3. Directional reserve inequality

For a direction u with ||u||_1=1, let its nine king-step projections be sorted from largest to smallest. Their largest value is 1. If at most k of the moves are excluded, the loss from 1 in the largest remaining projection is at most D_k, where

    k:    0    1    2    3    4    5    6    7    8
    D_k:  0   1/2  2/3   1    1   4/3   2    2    2.

To verify the table, reflect and exchange coordinates so u=(u_1,u_2) with u_1>=u_2>=0 and u_1+u_2=1. The sorted projections are

    1, u_1, max(u_2,u_1-u_2), min(u_2,u_1-u_2), 0,
    -min(u_2,u_1-u_2), -max(u_2,u_1-u_2), -u_1, -1.

Taking the largest possible loss at each rank gives the displayed bounds, including the breakpoint u_1=2/3.

The table satisfies D_k<=k/2 and D_k<=2(k+7)/13 for 1<=k<=8. If r_n=0, the first bound applies with k=m_n. Otherwise put k=m_n+r_n and use b_n>=r_n+7:

    m_n/2 + 2b_n/13
      >= m_n/2 + 2(r_n+7)/13
       = 2(k+7)/13 + 9m_n/26
      >= D_k.

Consequently, for every Euclidean unit direction w, at least one guard-admissible displacement delta satisfies

    w dot delta >= 1 - alpha*m_n - beta*b_n,      (3)

where

    alpha = sqrt(2)/2,  beta = 2sqrt(2)/13,
    C = alpha+beta = 17sqrt(2)/26 < 93/100.

Indeed apply the preceding result to u=w/||w||_1, multiply by ||w||_1, and use 1<=||w||_1<=sqrt(2). This remains valid when the right side is negative.

## 4. Controller and radial drift

Before move n, put e=z_n-a_(n-1). If e is nonzero choose, among the guard-admissible moves, a displacement maximizing e dot delta. Use any fixed tie order. If e=0 choose any guard-admissible move. This is an online rule. Write d_n=||a_n-z_n||_2.

Suppose d_(n-1)>=60. Then r=||e||_2>=60-1/100. Since ||delta||_2<=sqrt(2), the norm Taylor bound gives

    ||e-delta||_2
       <= r - (e/r) dot delta + 1/(r-sqrt(2)).

For example, this follows by integrating the Euclidean norm Hessian along the segment, where its operator norm is at most 1/(r-sqrt(2)); the quadratic remainder is at most ||delta||_2^2/[2(r-sqrt(2))]. Here 1/(r-sqrt(2))<1/50. Using (3), r<=d_(n-1)+1/100 and the reference-speed assumption gives

    d_n <= d_(n-1) - 97/100 + alpha*m_n + beta*b_n.       (4)

## 5. Amortization and a uniform radius

For any interval of N consecutive move indices s,...,s+N-1, each distinct short bomb counted by sum m_n has an announcement witness between s-15 and s+N-2. There are at most N+14 such rounds, or fewer near the initial time. The same bound holds for sum b_n, with its witness interval shifted one round. It is enough to use

    sum m_n <= N+15,   sum b_n <= N+15.            (5)

A bomb is counted at most once in each sum, since each sum ranges over distinct target times. Over any interval on which all preceding errors are at least 60, (4)-(5) imply

    d_end <= d_start - (97/100-C)N + 15C
          <= d_start + 15C.                       (6)

The coefficient 97/100-C is strictly positive.

Initially d_0=0. Whenever the error crosses from below 60 to at least 60, its new value is less than 60+sqrt(2)+1/100<62. Apply (6) to the remaining portion of that excursion above 60. Its error is always less than

    62+15C < 62+15*(93/100) < 76.

Points below 60 already satisfy the claimed bound. Thus d_n<76<80 for every n, proving the theorem.

## 6. Why this can couple short and long threats

The tracker can ignore long bombs and stay within 80 of a reference path whose future random block displacements remain hidden. If a long bomb at (p,t) hits the actual path, then z_t lies in p+[-80,80]^2. A fresh completed reference displacement uniform on an integer square [-M,M]^2 therefore bounds the conditional hit probability by

    161^2/(2M+1)^2,

even if the tracking error depends on that displacement and on subsequent adaptive short announcements. Only the reference displacement, not the error, must be independent of the earlier announcement history. The exact block construction and deterministic extraction are stated separately in MIXED_LEAD_COROLLARY.md.

This does not handle unrestricted intermediate announcement leads. In particular, the short bound fifteen and the long block rule are genuine restrictions on the Devil.
