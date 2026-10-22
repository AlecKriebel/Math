# Actual canonical comb mountains defeat every macroscopic rectangle-allocation score

Final shared PASS5, row1778 /30005770, 14 October2026. This is a deterministic obstruction to the exact raw-allocation entropy test, not a counterexample under the uniform avoidance law. Earlier frozen proof files are unchanged.

## 1. A213-avoiding comb state

Fix integers k,L>=1. Form B_(k,L) on (L+1)k entries by writing

    1,H_1,2,H_2,...,k,H_k,                                 (1)

where every H_i is a decreasing block of L values from{k+1,...,(L+1)k}, and the entire sequence H_1,H_2,...,H_k is decreasing. Call1,...,k the low anchors and the other points high teeth.

Every descent starts at a high tooth. No later entry is larger than that tooth. Hence there is no213: a descending pair cannot be followed by a larger third entry. Thus B_(k,L) is a legal normalized state in Av(213), and it avoids1324. It has an ascent, beginning with1 and the first tooth.

Its longest increasing subsequence has length k+1: take all low anchors and one tooth from H_k; no increasing subsequence can use two high teeth. Its increasing-pair count is exactly

    inc(B_(k,L))
       =binom(k,2)+L k(k+1)/2
       =[(L+1)k^2+(L-1)k]/2.                              (2)

## 2. Two geometric counting facts inside a comb

A. Every point strictly southwest of a given comb point is a low anchor. Indeed, earlier high teeth are larger than the given point, whether the latter is low or high.

B. Restrict these southwest points further to an open position interval ending at that point. If there are r such points, all but possibly the last have their entire following block of L teeth inside the position interval and above the endpoint's value. Thus these r points force at least L(r-1)_+ entries in the same position strip but outside the endpoint's value interval. Additional interleaving points from other cells do not change this statement: relative position and value orders within the comb are retained.

For an increasing pair with BOTH endpoints in the same comb, there is a stronger bound. Its first endpoint must be a low anchor. If its open rectangle has r points, then r low anchors lie between the endpoints. If the last endpoint is low, each such interior anchor has all L following teeth before that endpoint. If the last endpoint is high, its last interior low anchor may have an incomplete following block, but the L teeth following the first low-anchor endpoint are inside the open position interval and above the last endpoint. These compensate for the possibly incomplete last block. In both cases there are at least Lr strip contaminants. The assertion includes r=0.

## 3. Actual canonical mountain realization

Use normalized states

    B_(2,L), B_(4,L), ..., B_(2^s,L),
        B_(2^(s-1),L), ..., B_(2,L),                       (3)

for s>=1. Every state has an ascent. Join each ordered neighboring pair by the deterministic ascent bridge from the accepted exact kernel theorem: for upper state U and lower pattern S(A), split the lower pattern at its maximum, insert the portion through the maximum in the chosen adjacent upper ascent, and place the remaining lower portion after all upper points. This supplies a genuine allowed directed edge. The accepted exact homogeneous reconstruction produces a unique1324-avoider pi_(s,L) whose canonical normalized states are exactly(3).

In the actual grid, odd cells have the comb pattern and even cells its reflection S. The first and last fixed numbers of cells have negligible mass as s grows. Neighboring cell-size ratios are1/2 or2, just as in the earlier geometric mountain. Its size and central-state fraction are

    n_(s,L)=(L+1)(3*2^s-4),
    central fraction=2^s/(3*2^s-4)>1/3.                   (4)

This therefore retains the earlier escaping-index and graded-profile obstructions. It is not an arbitrary noncanonical gridding.

## 4. Every increasing-pair rectangle has many strip contaminants

For any marked increasing pair in pi_(s,L), let m,p,q have exactly the meanings in RECTANGLE_DELETION_AND_ENTROPY.md: m is its open rectangle's interior count, p counts points in its open position interval but outside its open value interval, and q is the dual value-strip count.

Then

    p+q>=L(m-2)_+.                                         (5)

Proof. Nonadjacent staircase cells are northwest/southeast ordered, so the pair lies in one cell or two adjacent cells. The accepted rectangle-locality lemma places its entire open rectangle in that same cell or adjacent pair.

If both endpoints lie in one cell, the strengthened same-cell comb argument gives p>=Lm for an odd comb cell and q>=Lm for its reflected even cell.

For adjacent cells, normalize their geometry to an upper comb A and a lower reflected comb S(C). The lower endpoint of the increasing pair belongs to the lower cell; its upper endpoint belongs to the upper cell. Let m_A and m_C count interior points in the upper and lower cells, so m_A+m_C=m.

All m_A upper interior points are southwest of the upper endpoint and hence low anchors by Fact A. Fact B gives at least L(m_A-1)_+ upper teeth in the open position strip above the upper endpoint, so p>=L(m_A-1)_+.

Apply S to the two-cell picture. This reverses the pair's endpoints, interchanges its coordinate strips, and turns the lower reflected comb into an upper comb. The same argument gives q>=L(m_C-1)_+. The counted tooth sets belong to different cells, so they are disjoint. Summing yields(5). For a horizontal original pair, S supplies the normalized vertical representation; the final bound on p+q is invariant under the coordinate exchange. QED.

## 5. No occupied rectangle of size at least20 pays the allocation cost

For m,p,q>=0,

    e(m,p)+e(m,q)>=e(m,p+q).                               (6)

For m>0, this follows from concavity of H(t)=e(1,t) and H(0)=0, which imply H(x)+H(y)>=H(x+y). The zero case is immediate.

Now fix L=5. If m>=20, equation(5) gives p+q>=5(m-2)>=9m/2. Consequently

    E(m,p,q)>=m H(9/2)>m log(27/2)>=m log lambda.            (7)

The last comparison uses the credited upper bound lambda<=27/2. The strict middle comparison is exact:

    2[H(9/2)-log(27/2)]=log(11^11/3^24)>0,
    11^11=285311670611>282429536481=3^24.                   (8)

Thus every marked increasing pair in every pi_(s,5) whose open rectangle contains at least20 points has STRICTLY NEGATIVE raw deletion score

    m log lambda-E(m,p,q)<0.                               (9)

For every fixed epsilon>0, every rectangle of mass at least epsilon*n_(s,5) eventually has m>=20. Adaptive choices of endpoints, sizes, locations, or a bounded family of candidate rectangles cannot produce a favorable macroscopic score. In fact(9) covers all rectangle locations and sizes above this fixed threshold simultaneously.

## 6. The examples have genuine increasing-pair mass

The central state alone has an increasing subsequence of length2^s+1 and the increasing-pair count in(2). With L=5,

    liminf_s LIS(pi_(s,5))/n_(s,5)>=1/18,
    liminf_s Inc(pi_(s,5))/n_(s,5)^2>=1/108.                (10)

The normalized two-point increasing density therefore has liminf at least1/54, and these deterministic permutations do not approach the anti-diagonal permuton. At the same time, fixed initial and terminal cell prefixes have negligible mass, and the earlier graded-window barriers remain applicable because their cell-mass profile is unchanged by the common factor L+1.

None of these claims supplies a lower probability under exactly uniform Av_n(1324). The entire witness family can be exponentially negligible. Equation(9) obstructs only an upper bound that treats all position/value allocation records in the deletion fiber as admissible. The exact admissibility indicator or another counting mechanism may supply a substantially larger loss.

## 7. Consequence for the final rectangle route

The dense-interior probability theorem is valid, but positive increasing-pair density does not force one of its favorable rectangles. The obstruction persists in actual canonical avoiders with escaping-index heavy cells and holds for every macroscopic occupied rectangle, not merely for one chosen profile window.

This does not eliminate the point-pair route: it identifies the missing gain as a constraint on actual allocation admissibility or a joint completion estimate, rather than an uncharged choice of interior points. The sparse/empty-rectangle branch also remains necessary; two decreasing blocks in direct sum have quadratically many increasing pairs and zero occupied interiors.

## Inputs and source scope

The exact canonical kernel and rectangle locality are the accepted PASS2 EXACT_GREEDY_TRANSFER.md. The universal ascent bridge is in the accepted PASS3 REROOTING_ONE_POINT_BOUND.md. The primary bound lambda<=27/2 is Theorem8 of Bevan, Brignall, Elvey Price and Pantone, *A structural characterisation of Av(1324) and new bounds on its growth rate*, https://oro.open.ac.uk/68534/1/1324-staircase-els.pdf, already pinned and used in PASS4 FIXED_WIDTH_CALIBRATION.md. No source is newly copied or published here.
