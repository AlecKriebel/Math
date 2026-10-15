# Turn2: auxiliary-line certificates and an exact Hesse LP gap

Second substantive turn; the general arrangement conjecture remains unresolved. The Hesse value is already within the previously reported small-arrangement scope. The purpose here is an explicit certificate mechanism and an exact limitation of an arrangement-component-only relaxation, not a claim of first computing that value. Weighted Bézout arguments and the workshop LP strategy are credited prior methods.

## 1. A finite weighted-line certificate

LetZ be a finite nonempty point set. Choose distinct auxiliary linesL₁,...,L_t, which need not be components of its originating arrangement, and rational weightsw_i≥0. Suppose

    Σ_{i:p∈L_i} w_i≥1 for everyp∈Z.

Writeτ=Σw_i andk₀=max_i |L_i∩Z|, omitting zero-weight lines if desired. Ifτ≤k₀, then

    mpl(Z)=k₀,       epsilon(P²,O(1);Z)=1/k₀.             (1)

Indeed, for every integral curveC not among these support lines, Bézout gives

    τ deg C =Σw_i(C·L_i)≥Σ_{p∈Z} mult_p(C).              (2)

In particular a line outside the support contains at mostτ points. Therefore no line has more thank₀ points, and a support line realizesk₀. Every non-support curve has ratio≥1/τ≥1/k₀; every support line has ratio≥1/k₀. This proves(1). No general-position, multiplicity-one or irreducibility test on a sampled polynomial is involved; the test curve itself is integral as in the Seshadri definition.

This criterion extends the available Bézout inequalities beyond arrangement components. It is a sufficient certificate, not an equivalent formulation of the general source conjecture.

## 2. Exact configuration overQ(ζ)

Letζ²+ζ+1=0, ζ≠1, and letH be the twelve lines

    x=0, y=0, z=0,
    x+ζ^a y+ζ^b z=0,       a,b∈{0,1,2}.

Their singular setZ consists of two disjoint parts:

- Q: nine points obtained by putting one coordinate0 and taking the ratio of the other two to be−ζ^a
- D: the three coordinate vertices and the nine points[1:ζ^a:ζ^b].

EveryQ point lies on fourH lines, while everyD point lies on two. EachH line contains threeQ points and twoD points, hence five singular points. These claims follow directly from1+ζ+ζ²=0 and are also checked over the exact quadratic field.

They exhaust all pair intersections:9 binomial(4,2)+12 binomial(2,2)=66=binomial(12,2). The listed points are distinct and every incidence is explicitly verified, so no unlisted intersection is left over.

Take also the nine Fermat linesF:

    x−ζ^a y=0, y−ζ^a z=0, z−ζ^a x=0,    a∈{0,1,2}.

EachF line contains fourD points and noQ point. EveryD point lies on threeF lines. TheH andF line sets are disjoint.

## 3. Arrangement-only LP has exact optimum6

Consider the fractional-cover linear program that only permitsH lines:

    minimize Σ_{L∈H}w_L
    subject to w_L≥0 and Σ_{L∋p}w_L≥1 for everyp∈Z.

Sum the twelveD-point constraints. EachH line appears exactly twice, so

    2Σw_L≥12, hence Σw_L≥6.

The constant choicew_L=1/2 is feasible, including at theQ points, and has cost6. Thus the optimum is exactly6. Since the actual maximum collinearity will be5, this relaxation alone cannot certify the conjectured lower bound1/5 by(2). This is a failure of that restricted certificate, not a counterexample to the conjecture or to every possible LP formulation.

## 4. Auxiliary lines repair the certificate, optimally

Assign weight1/4 to eachH line and1/6 to eachF line. At aQ point the total is4/4=1; at aD point it is2/4+3/6=1. The total cost is

    12/4+9/6=9/2.

The support lines have at mostfive points, withH lines realizingfive, and9/2<5. Section1 therefore proves

    mpl(Z)=5,          epsilon(Z)=1/5.                   (3)

Every integral nonlinear curve has Seshadri ratio at least2/9. Every line outsideH has at mostfourZ points, since a non-support line has at mostfloor(9/2)=4 and everyF line hasfour. Consequently the only curves computing the value1/5 are the twelveH lines. The lower bound2/9 for nonlinear curves is not claimed to be attained.

The augmented fractional-cover optimum is exactly9/2, not merely bounded above by it. Put dual point weights

    y_p=1/6 forp∈Q,       y_p=1/4 forp∈D.

EachH line has point-weight3/6+2/4=1, and eachF line has4/4=1. The total point weight is9/6+12/4=9/2. Weak LP duality proves optimality onH∪F.

In fact this dual is feasible even if **all** projective lines are allowed: any line outsideH∪F contains at mostfourZ points by the already-proved certificate, and every point weight is at most1/4. Thus the unrestricted fractional line-cover optimum for this particular set is also9/2. There is no circularity: the primal certificate first bounds outside-line cardinalities without invoking LP optimality, and only then establishes feasibility of the global dual.

## 5. Relation to turn1 and to the open problem

Here r=21 andk=5. The turn1 degree bound isD=9, so a raw exact search could require many fat-point systems through degree9. The auxiliary-line certificate removes that computation entirely and gives an explicit gap between all nonlinear curves and the line minimum.

The example illustrates a concrete risk for the general approach: optimizing only over input arrangement lines can fail even when the conjecture is true and a short certificate exists after adding other lines. It does not prove that every arrangement has a finite weighted-line certificate of cost≤mpl(Z), nor that all relevant auxiliary lines can be found by a universally bounded search. Those remain unproved routes, not asserted equivalents.

The source's general conjecture remains unresolved2/5. The next direction is to characterize or construct certificates in an infinite genuinely geometric family, while retaining existing-family credit.
