# Attempt 4: Fractional ownership and a quadratic dual

Verdict: a precise sufficient weighted inequality is isolated, but it is not proved in general. Unweighted face-incidence squaring is false. Fractional ownership repairs the displayed obstruction without resolving all hypergraphs.

## The square-counting approach and its failure

For each red hyperedge e, let d(e) be the number of successful r-sets containing it. One might try to combine T≤Σ_e d(e), Cauchy–Schwarz, and

Σ_e d(e)² ≤ 2GB.                                            (6)

Then T²≤RΣ_e d(e)²≤2RGB would follow. But (6) is false in the five-vertex example of Attempt 2. In the red-edge order 012,013,014,023,123,234, the degrees are (1,1,2,1,1,2), so Σ d(e)²=12, while 2GB=8. Each successful set has two red faces; this repeated accounting is consequential rather than cosmetic.

## Fractional ownership removes that overcount

Let S range over the successful r-sets, and let R(S) be the nonempty set of red faces of S. Choose numbers p(S,e)≥0 supported on e∈R(S), subject to

Σ_{e∈R(S)} p(S,e)=1  for every successful S.

Put x_e=Σ_S p(S,e). Then Σ_e x_e=T exactly, and therefore

T² ≤ R Σ_e x_e².                                           (7)

Consequently it would suffice to prove that there is always such an assignment with Σ_e x_e²≤2GB. This is explicitly a stronger, unproved sufficient statement, not an established equivalent of the original conjecture. The implication in (7) runs in only the indicated direction.

## Exact convex dual, proved directly

Define E_* as the minimum of Σ_e x_e² over all fractional ownership assignments. The feasible set is a finite product of simplices, so a minimum exists. For any real weights y_e, completing squares gives

Σ_e x_e² ≥ 2Σ_e y_e x_e − Σ_e y_e²
          ≥ 2Σ_S min_{e∈R(S)} y_e − Σ_e y_e².                (8)

In fact equality is attained in the dual:

E_* = max_y [2Σ_S min_{e∈R(S)} y_e − Σ_e y_e²].             (9)

To prove the reverse inequality without invoking a duality theorem, take a minimizing assignment p with load vector x. If p(S,e)>0 and x_e>x_f for another f∈R(S), moving a sufficiently small positive mass from e to f changes the objective by 2ε(x_f−x_e)+2ε²<0, a contradiction. Thus every positive entry p(S,e) sits on a minimum-load red face of S. With y=x we then have

Σ_S min_{e∈R(S)} x_e = Σ_{S,e} p(S,e)x_e = Σ_e x_e².

The right side of (8) equals E_* for this y, proving (9). The optimum weights may be taken nonnegative since x is nonnegative.

If R=0, then T=E_*=0, and this case is handled separately. For R>0, optimizing the scale of a nonzero nonnegative y in (9) also yields

E_* = sup_{y≥0,y≠0} (Σ_S min_{e∈R(S)} y_e)² / Σ_e y_e².    (10)

For the upper bound, write A=Σ_S min y_e and B=Σ_e y_e²; the optimal scale t≥0 maximizes 2tA−t²B at t=A/B. For the lower bound in the other direction, the optimizer y=x from (9) has A=B=E_*, unless T=0, which is trivial.

The missing sufficient inequality can therefore be stated precisely as

Σ_S min_{e∈R(S)} y_e ≤ √(2GB Σ_e y_e²)  for all y≥0.       (11)

Taking all y_e=1 already recovers the desired original bound, so this reformulation must not be mistaken for a solution. It identifies the additional local information an ownership-based proof would need to exploit.

## Exact repair of the five-vertex example

The four successful sets have red options

0124: {012,014}; 0134: {013,014};
0234: {023,234}; 1234: {123,234}.

Assign mass 2/3 to each private red face 012,013,023,123 and mass 1/3 to the respective shared face 014 or 234. Every red face then has load 2/3, giving E_*=6(2/3)²=8/3. This is optimal by (7), since T²/R=16/6=8/3. The dual constant vector y_e=2/3 supplies the matching certificate. Thus the raw-square failure 12>8 is fully removed for this example, but no universal control of (11) follows from it.

## Remaining obstruction

Color-pair uniqueness bounds the number of successful sets, but does not yet control the weighted minimum over their red faces in (11). Establishing that weighted estimate, or producing an obstruction to it, remains open in this attempt. The final attempt turns to complements, where successful sets become common faces of three colored families; this makes small complementary dimensions amenable to parity and trade arguments.
