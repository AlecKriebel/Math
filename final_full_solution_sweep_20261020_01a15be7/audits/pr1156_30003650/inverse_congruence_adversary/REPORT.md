# Independent inverse-congruence adversarial report

Audit completed: 2026-10-22 UTC. Candidate: PR 1156 / problem 30003650.
Immutable candidate head: `57c07523247d0de1a2fbb76f3243d0369caff682`.
Compared proof: `unsolved_math_prioritization/attempts/30003650/PROOF.md`,
11,301 bytes, SHA-256
`a2486250c2ddd7dc0e75cbf7275c59628a7b24f1f227e6432890369de96bacdb`.

## Disposition and exact scope

**No mathematical defect found in the inverse-congruence theorem or its
fixed-ordinary-rank consequence.** The universal written argument below verifies
that, for every integer n >= 1, the maximum finite CP-plus-rank equals the maximum
ordinary CP-rank, including singular matrices. It verifies the stronger equality
on every exact ordinary-rank stratum 1 <= r <= n. The existence and attainment
interfaces have been checked; they do not require compact rank strata or an
unattained infimum argument.

The exact remaining gap for the audited theorem is **none identified**. This
disposition is a correctness finding for this family, not a novelty finding or
permission to publish. The maximum finite difference between the two ranks is a
separate question and is not resolved by this argument. An explicit integer
formula for the ordinary maximum in every order is not required to settle the
binary choice between that maximum and one more.

## Independent reading and source interpretation

I read the complete immutable candidate proof and the original primary source
before any historical mathematical audit. No historical mathematical audit was
consulted in this family. Primary PDFs, extracts, rendered pages, response headers,
and the candidate capture remain in the private directory.

The [original Oberwolfach contribution](https://ems.press/content/serial-article-files/46715),
printed pp. 3082-3083, separately asks for the maximum finite rank difference and
the maximum finite CP-plus-rank. It records the latter between p_n and p_n+1.
Its displayed p-by-n factor accompanying BB^T is dimensionally inconsistent for
an n-by-n matrix. The intended vector-sum convention is confirmed by Definition
1.1 and Lemma 2.9 of the [complete author manuscript](https://api.newton.ac.uk/website/v0/events/preprints/NI14088):
column factors are n-by-p with A=BB^T; alternatively row factors are p-by-n with
A=B^TB. This audit uses the former throughout.

The author manuscript is dated November 4, 2014; the journal publication is
*Linear Algebra and its Applications* 482 (2015), 191-206,
[DOI 10.1016/j.laa.2015.05.021](https://doi.org/10.1016/j.laa.2015.05.021).
Its Theorem 4.9 has an interior hypothesis. Its Theorem 5.1 gives the interior
CP-plus maximum as p_n and the global finite maximum between p_n and p_n+1.
The proof below needs neither of those theorems; its singular conclusion is
derived directly. Relevant original pages and manuscript pages 1, 6, 7 were
visually inspected in addition to text extraction.

## Exact definitions and success criteria

Let CP_n consist of symmetric real matrices expressible as A=DD^T for a finite
entrywise nonnegative n-by-p matrix D. For nonzero A, let cp(A) be the least
number of such columns. Let cp+(A) be the least number of columns of a finite
entrywise strictly positive factor, or infinity if no such factor exists.
An infimum over admissible integer column counts, when finite, is a minimum by
well-ordering. No limiting matrix-factor argument is needed for this fact.

Write p_n for the maximum cp(A) among nonzero A in CP_n. For each r in
{1,...,n}, write P_(n,r) for the corresponding maximum restricted to rank(A)=r.
The required upper-bound claim is

    0 != A, cp+(A) < infinity, rank(A)=r
        implies cp+(A) <= P_(n,r) <= p_n.

To establish equality of maxima rather than an upper bound alone, the success
criterion also requires a matrix in each rank stratum whose finite cp+ equals
the attained ordinary maximum in that stratum.

## Universal upper-bound proof, independently reconstructed

Take any finite strictly positive factor B of A=BB^T, with q columns. This q
need not be minimal. Set e=(1,...,1)^T, J=ee^T, and

    s_j = sum_i B_ij,
    alpha = min_(i,j) B_ij/s_j,
    0 < t <= alpha/2,
    T = I-tJ.

The finite minimum alpha is positive. For each fixed column j, the ratios sum
to 1, so alpha <= 1/n. Consequently 0<t<1/n, and

    (TB)_ij = B_ij-t s_j >= B_ij/2 > 0.

Thus C=TAT^T=(TB)(TB)^T is a nonzero completely positive matrix. Because
J^2=nJ, multiplication gives

    M = T^(-1) = I + [t/(1-nt)]J,
    TM = MT = I.

The coefficient t/(1-nt) is strictly positive, so M is entrywise strictly
positive. If d>=0 is nonzero, then sum_i d_i>0 and every coordinate of Md is
at least [t/(1-nt)] sum_i d_i>0.

Let D be a minimal nonnegative factor of C, with k=cp(C) columns. Every
column is nonzero: deleting a zero column would yield a shorter factor. Hence
MD is strictly positive and

    A = MCM^T = (MD)(MD)^T.

It follows that cp+(A)<=k=cp(C). Invertibility gives rank(C)=rank(A)=r.
Therefore cp+(A)<=P_(n,r)<=p_n. There is no step assuming that T preserves
the entire CP cone: it is enough that the specifically chosen factor TB is
positive. There is no assumption that A is positive definite, an ambient
interior point, or even of full ordinary rank.

If B is chosen minimal positive, q=cp+(A), the same proof also gives

    q <= cp(C) <= cp+(C) <= q.

Thus all three counts are exactly q for **every** t in the displayed interval.
The positive interval is explicit for the chosen B. It is not a parameter bound
uniform over every possible A or every factor; the candidate does not need
such a bound.

## Finiteness, closedness, and the lower-bound interface

For completeness, p_n and P_(n,r) exist without assuming previously computed
CP-rank tables. Put N=n(n+1)/2. If a nonnegative factor has more than N nonzero
columns v_i, the symmetric matrices v_i v_i^T are linearly dependent. With
positive current weights w_i and a nonzero relation sum_i c_i v_i v_i^T=0,
reverse signs so some c_i>0 and take u=min_(c_i>0) w_i/c_i. Then
w_i-u c_i>=0 for all i, and at least one weight vanishes. Removing zero
weights and absorbing square roots into the retained columns yields the same
matrix with fewer terms. Repeating gives at most N terms. If the original
columns were strictly positive, retained columns remain strictly positive.

Consequently all realized ordinary CP-ranks lie in the finite set {1,...,N}.
The rank-r class is nonempty, using a diagonal matrix with r positive diagonal
entries. Each class therefore has a largest realized integer CP-rank. This
is attainment by a finite set of integer values, not by compactness of the
matrix class.

For every k>=0, the bounded CP-rank set F_k is closed, with F_0={0}. Indeed,
if A_m=D_m D_m^T converges and each D_m has at most k columns, pad with zero
columns to n-by-k. The identity ||D_m||_F^2=trace(A_m) bounds the factors, so
a subsequence converges to a nonnegative D and the limit matrix is DD^T.
The k=0 case is immediate. This includes singular limits.

Take an attained rank-r maximizer A_0 with p=cp(A_0)=P_(n,r), and a minimal
nonnegative factor D_0. For every t>0, S=I+tJ is invertible and strictly
positive. Because D_0 has no zero columns, SD_0 is strictly positive. Hence

    cp(SA_0S^T) <= cp+(SA_0S^T) <= p.

As t tends to zero, SA_0S^T tends to A_0, which is outside the closed set
F_(p-1). There is therefore a positive interval in which cp(SA_0S^T)>=p.
All inequalities are equalities on that interval; invertibility preserves rank
r. This supplies an actual finite positive-factor maximizer in every stratum.

An optional quantitative version makes the interval checkable. Let
delta=dist_F(A_0,F_(p-1))>0. With K=2n+n^2, every

    0 < t <= min(1, delta/(2 K ||A_0||_F))

satisfies

    ||SA_0S^T-A_0||_F
       <= (2nt+n^2t^2)||A_0||_F
       <= delta/2 < delta.

Here ||J||_2=n supplies the norm bound. Thus there is no unattained-limit
loophole. Combining this lower construction with the upper construction proves

    P_(n,r)^+ = P_(n,r)   (1 <= r <= n),
    p_n^+ = p_n          (n >= 1).

## Adversarial checks and boundary cases

| Attack or possible hidden premise | Resolution |
| --- | --- |
| Singular A might make the pullback fail | Only T and M must be invertible. A can have any nonzero ordinary rank. |
| T has negative off-diagonal entries | Full-cone preservation is not used; the displayed entrywise bound establishes TB>0 for this A. |
| A shortest nonnegative factor might have zero columns | A zero column can be removed. C is nonzero, so its shortest factor has positive length and no zero columns. |
| Infimum of positive column counts may fail to be attained | Counts are integers and the admissible set is nonempty when cp+ is finite. Its least element is admissible. |
| Maximum on a nonclosed rank stratum might be unattained | Possible CP-rank values form a nonempty finite set, so the largest realized value has a witness. |
| Lower construction might lose CP-rank as soon as t>0 | Closedness of F_(p-1) excludes this on a positive interval; the explicit delta bound above suffices. |
| Rank one or n=1 could violate strictness | For n=1, alpha=1 and 0<t<=1/2; the same inverse proof applies. Every positive rank-one matrix has a one-column positive factor. |
| Zero matrix or rank-zero stratum | Excluded by the stated nonzero scope; convention at zero does not affect any maximum. |
| t=1/n | Excluded: T is singular. |
| t=alpha without a margin | May lose strictness: B=(1,3)^T, alpha=1/4, gives TB=(0,2)^T. The stated bound t<=alpha/2 avoids this. |
| Positive-factor singular matrices might secretly be treated as interior | No such inference occurs. In fact rank<n means an ambient PSD boundary point. |
| Equality of maxima might imply equality of ranks pointwise | It does not. The proof changes the matrix by congruence; the original matrix can have cp<cp+. |

## Exact finite guards and limits of computation

`exact_guards.py` is authored for this audit and was inspected before execution.
Only new, read-only private copies were run, with ordinary Python, -O, and -OO.
Each run passed the same 36 exact rational rank-stratum cases for 1<=n<=8 and
1<=r<=n, with repeated positive columns and row scales ranging down to 10^-7.
The guards check both inverse identities, the half-margin, exact factor and
Gram round trips, rank preservation, sparse nonzero-column pullbacks, and the
two excluded parameter endpoints. All three outputs are byte-identical.
Source and copy hashes before and after are recorded in
`EXACT_GUARD_RECEIPT.json`; the copies remained read-only and unchanged.

These computations are supplementary algebra guards. They do not compute
minimal CP factorizations and are not the proof of the universal statement.
The written proof above is the basis for acceptance in this family.

## Remaining work outside this family's finding

No correction to the audited theorem is requested. The candidate correctly
leaves the general maximum-gap problem open and does not give a formula for
all p_n. Priority and duplication of the congruence mechanism require separate
literature work; this report makes no novelty or publication-readiness claim.
No external individual was contacted and no Git, candidate, PR, tracker, or
service mutation was performed by this family.
