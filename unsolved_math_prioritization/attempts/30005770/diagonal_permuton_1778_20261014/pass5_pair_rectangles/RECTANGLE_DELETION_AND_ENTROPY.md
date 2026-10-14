# Exact occupied-to-empty rectangle reduction and a uniform entropy tail

Final shared PASS5, row1778 /30005770, 14 October2026. This is a genuine exact counting reduction and partial concentration estimate. It does not establish vanishing expected increasing-pair density.

## 1. Rectangle statistics

Let pi be a1324-avoider of size n. Mark an increasing pair of entries at positions i<j and values u=pi(i)<v=pi(j). Its open rectangle consists of the entries

    i<t<j,       u<pi(t)<v.

Let m be the number of these entries. They form an increasing sequence: otherwise the marked endpoints and an interior decreasing pair form1324. Define the two strip-contamination counts

    p=j-i-1-m,
    q=v-u-1-m.                                             (1)

Thus p counts entries in the open position interval but outside the open value interval; q counts entries in the open value interval but outside the open position interval. These sets are disjoint. Both are nonnegative. They count actual entries, not rectangle area or an independently sampled grid.

Write e(x,y)=(x+y)log(x+y)-x log x-y log y, with0 log0=0. The exact allocation entropy used below is

    E(m,p,q)=e(m,p)+e(m,q).                                 (2)

## 2. Exact deletion data

Delete all m interior entries and standardize, retaining the marked endpoints. The result sigma is a1324-avoider of size N=n-m, its marked increasing pair has EMPTY open rectangle, and its open position and value intervals have respectively p and q entries.

Given this marked sigma, reconstruction requires:

- choosing m positions among the m+p positions between the two retained endpoint positions;
- choosing m values among the m+q values between the two retained endpoint values;
- matching the chosen positions and values increasingly.

There are exactly

    binom(m+p,m) binom(m+q,m)                               (3)

such allocation records before imposing1324-avoidance. The other entries keep their relative orders, so the record reconstructs at most one permutation. The interior of the reconstructed marked rectangle contains exactly the chosen entries: each surviving point was outside one of its endpoint intervals and stays outside it after order-preserving insertion.

Let B_N(p,q) be the number of1324-avoiders of size N with a marked EMPTY increasing pair having these two interval counts. Let Z_n(m,p,q) count marked pairs with the statistics(1). If A_m(sigma,a,b) denotes the number of allocations in(3) whose reconstructed permutation avoids1324, then the exact identity is

    Z_n(m,p,q)
      =sum_(sigma,a,b counted by B_(n-m)(p,q)) A_m(sigma,a,b),
    0<=A_m(sigma,a,b)<=binom(m+p,m)binom(m+q,m).              (4)

Consequently,

    Z_n(m,p,q)
      <=B_(n-m)(p,q) binom(m+p,m)binom(m+q,m)
      <=(n-m)^2 a_(n-m) exp(E(m,p,q)),                      (5)

where a_N=|Av_N(1324)|. The crude square factor merely bounds the number of marked pairs. Equation(4) retains the entire actual completion law in the marked skeleton sigma and its admissibility indicator; no conditional uniformity or independent shuffle law is introduced.

### The admissibility indicator cannot be omitted

The permutation31524 avoids1324. Its entries3 at position1 and5 at position3 form an empty increasing pair, with p=q=1. Insert one new rank4 between the old positions2 and3, increasing old ranks4,5 to5,6. The resulting314625 has the increasing marked endpoints3,6 and the inserted interior4, but contains1324 on entries1,4,2,5. Thus not all allocation records preserve avoidance. Replacing A_m by the full product in(3) is an upper bound, not an exact identity or a new random generator.

## 3. Exponential suppression when interior loss pays both allocations

Let lambda=lim a_n^(1/n). Skew-sum closure gives a_N<=lambda^N and log a_n=n log lambda+o(n).

For every fixed c>0,

    P(exists an increasing pair with
          m log lambda-E(m,p,q)>=c n)
       <=exp(-c n+o(n)).                                   (6)

Proof. For each admissible m,p,q, equation(5) is at most n^2 lambda^(n-m) exp(m log lambda-cn)=n^2 lambda^n exp(-cn). There are at most(n+1)^3 statistic triples. Divide their sum by the exact a_n. The polynomial factors are absorbed into o(n). This proves(6) uniformly over locations, interval lengths and all choices of the marked pair. No fixed-cell-index restriction is used. QED.

In particular, for fixed epsilon,eta>0, a pair with

    m>=epsilon n,
    E(m,p,q)<=m(log lambda-eta)

has exponentially small existence probability, with exponent at most-epsilon eta on the n scale.

## 4. A usable dense-interior corollary

If p+q<=m, concavity of e(m,.) gives

    E(m,p,q)<=2e(m,m/2)=m log(27/4).                        (7)

The accepted exact two-cell calibration gives g_2=27/4, while the accepted strict fixed-width gap gives g_2<lambda. Therefore, for every fixed epsilon>0,

    P(exists an increasing pair with m>=epsilon n,
                                      p+q<=m)
       <=exp[-epsilon log(lambda/(27/4)) n+o(n)].            (8)

More generally any fixed contamination ratio t satisfying2H(t/2)<log lambda works, where H(r)=e(1,r). This eliminates macroscopic occupied rectangles with sufficiently little strip contamination.

The original increasing-cell mountain is a useful target for such a shape-sensitive loss: its cell mass alone defeated weak window certificates, whereas its increasing interior has only one possible order. However, the companion comb construction shows that no adaptive choice of an occupied rectangle forces the favorable allocation inequality in general, even inside actual canonical avoiders with escaping-index heavy cells.

## 5. Remaining obstacle

Equation(4) reduces occupied rectangles to empty marked skeletons, but estimating their total weighted allocation sum is still substantive. The dense-interior tail(8) does not control occupied rectangles with large strip contamination or the m=0 branch. The comb witnesses defeat the displayed allocation entropy test, and two decreasing blocks in direct sum have quadratically many increasing pairs with m=0.

Thus this note proves neither E Inc(Pi_n)=o(n^2) nor a counterexample under the uniform law. It supplies an exact skeleton transformation, a valid probability estimate, and the specific missing admissibility/counting information.

## Inputs

Only hereditary avoidance, skew-sum closure, the finite growth limit and the accepted PASS4 exact g_2 calibration are used. The latter is in pass4_window_gaps/FIXED_WIDTH_CALIBRATION.md, SHA-256 f831a975f8757858a6ad2a875d135011068047f49154ec426c66e262e5e3705c. No new outside source is required.
