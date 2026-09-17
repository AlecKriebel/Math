# General obstruction — proof checkpoint, 14 September 2026

Suppose m>=3 and all row sums and all column products are N>0. Write
x_j=A[1,j], y_j=A[2,j], z_j=A[3,j]. Since all other entries are positive
integers, N >= x_j*y_j*z_j. Therefore

3 = sum_j (x_j+y_j+z_j)/N
  <= sum_j (1/(x_j*y_j)+1/(x_j*z_j)+1/(y_j*z_j))
  <= sum_j (1/x_j^2+1/y_j^2+1/z_j^2)
  < 2.

The second inequality follows because its per-column gap is
((1/x_j-1/y_j)^2+(1/x_j-1/z_j)^2+(1/y_j-1/z_j)^2)/2.
For the last inequality, the selected entries are globally distinct
positive integers. If M is their maximum, their reciprocal-square sum is
at most sum_{k=1}^M 1/k^2 <= 1+sum_{k=2}^M 1/(k(k-1)) = 2-1/M < 2.

This is a contradiction. The argument covers every m>=3, every n>=1,
and every N>=1; there is no finite-search assumption. No AM-GM theorem,
infinite series evaluation, computational search, or numerical estimate is
needed. This checkpoint is a written mathematical proof, not a proof-assistant
certificate or a record of an external review.
