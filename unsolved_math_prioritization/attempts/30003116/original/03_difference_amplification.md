# Approach 3: pigeonholing and expansion of a difference

**Result:** an unconditional but much weaker lower bound at a genuine polylogarithmic scale. For fixed a,b there are constants M,c,s0>0 such that
C(A_{floor(M log s)}(r,s), (log s)^(-4)) >= c sqrt(log log s)
for all s>=s0 and all admissible r. Equivalently, the logarithmic covering entropy is at least (1/2)log log log s+O(1), rather than the requested positive multiple of log log s.

This argument uses only elementary expansion and the injectivity established in Approach 1. It does not use Baker's theorem or assume that an orbit point is close to zero.

## Proof
Put L0=floor(log(s-1)/(2 log(ab))). By Approach 1, B=A_{L0}(r,s) has T=(L0+1)^2 distinct points. Choose consecutive points x<y in their increasing order so that their gap d=y-x is minimal. Then
1/s <= d <= 1/(T-1) <= C0/(log s)^2
for sufficiently large s, where C0 depends only on a,b.

Set delta=(log s)^(-4). Choose the smallest j0>=0 with a^(j0)d>=4 delta, or j0=0 if d>=4 delta. Then
4 delta <= a^(j0)d <= max(d,4a delta) <= C1/(log s)^2.
Let j1 be the largest j>=j0 with a^j d<=1/4. This exists for large s, and a^(j1)d>1/(4a). Thus the number J=j1-j0+1 satisfies
J >= [2 log log s-log(4a C1)]/log a.
Indeed J-1=log(a^(j1)d/(a^(j0)d))/log a, and the displayed bounds give the claimed (slightly weaker) inequality.

The points t_j=a^j d for j0<=j<=j1 lie in [0,1/4] and consecutive differences are (a-1)t_j>=4 delta. They are therefore separated by more than 2 delta in the circle metric. Also d>=1/s and a^j d<=1/4 imply j<log_a s. Since x,y were in B, each t_j modulo 1 belongs to A_H-A_H with
H=L0+ceil(log_a s).
No assumption that multiplying x or y avoids wrap-around is required: equality of their differences holds modulo 1, and the selected t_j themselves lie in [0,1/4].

If K intervals of length delta cover A_H, then their ordered pairwise differences give K^2 circle arcs of length 2 delta covering A_H-A_H. Each such arc contains at most one t_j. Hence K^2>=J. Choosing M large enough that H<=floor(M log s), and decreasing c if necessary, proves the theorem. QED.

## A stronger conditional variant and its gap
If the small initial block contains two distinct points with circle distance at most s^(-theta), apply the Baker construction of Approach 2 to that difference (which is at least 1/s). It produces at least c_theta log s mutually separated points in the difference set of a larger logarithmic-time block, at a scale (log s)^(-N). The same covering argument yields
C(A,(log s)^(-N)) >= c'_theta sqrt(log s),
which is enough for the target entropy. This conditional transfer is valid even when neither point is itself close to a fixed rational.

The elementary pigeonhole bound is only O((log s)^(-2)); it does not supply this power-small pair. This is the precise remaining obstruction for the difference route.
