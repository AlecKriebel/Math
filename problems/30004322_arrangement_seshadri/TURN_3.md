# Turn3: arbitrary two-line extensions of supersolvable arrangements

Third substantive turn. The general source conjecture remains unresolved. This turn proves an unbounded geometric subclass using the auxiliary-line certificate of turn2. Classical modular-point geometry and Bézout are credited ingredients; no historical novelty is asserted.

## 1. Geometric hypothesis

LetB be an arrangement of at least two distinct complex projective lines. Assume a pointP lies onm₀≥2 of its lines and that every singular point ofB lies on the union of those lines. For a rank-three arrangement this is the usual modular-point property underlying supersolvability. Pencils also satisfy the stated incidence condition.

Adjoin at most two arbitrary distinct lines, removing repetitions, to obtainA. PutZ=Sing(A), and letk=max_L |L∩Z| over all projective lines. Then

    epsilon(P²,O(1);Z)=1/k.                              (1)

The added lines need not be generic, may pass through old singular points and may pass throughP. No characteristic-specific incidence classification is used, although the source target and the Seshadri interpretation are overC.

## 2. Absorb the new pencil lines

Any added line throughP can be absorbed intoB while preserving the stated property: intersections with an old line lie on that added pencil line, and intersections among pencil lines areP. LetL₁,...,L_m be all final arrangement lines throughP. At mostt≤2 unabsorbed new linesA₁,...,A_t remain, none throughP.

All singular points outside the pencil unionU=∪L_i lie on at least oneA_j, because a pair of original/absorbed lines only meets inU. Call this finite outside setW=Z\U.

If the final arrangement is a pencil, Z={P} and epsilon=1, so assume there is a line not throughP. Such a line meets the m pencil lines in m distinct points; all are inZ. Thus the maximum over arrangement components,

    k_A=max_{L∈A}|L∩Z|,

satisfies k_A≥m. Of coursek≥k_A. It is important not to presumek=k_A: the assigned conjecture allows auxiliary lines to compute its value.

## 3. An explicit cover of degree at most k_A

If t=0, the m pencil lines already coverZ and m≤k_A.

If t=1 andk_A≥m+1, use the m pencil lines together withA₁. If insteadk_A=m, the m pencil intersections already account for every singular point onA₁. ThereforeW is empty and the pencil alone coversZ.

Now lett=2. Ifk_A≥m+2, the pencil together withA₁,A₂ is a cover of degree m+2≤k_A. Otherwise k_A≤m+1. EachA_j contains its m distinct pencil intersections, so it contains at mostone point ofW. Consequently

    |W|≤2.                                               (2)

IfW is empty, use the pencil. IfW is nonempty, at least oneA_j has an extra off-pencil singular point, sok_A≥m+1. Choose one projective lineH containingW (the joining line if there are two distinct points; any such line if only one). The m pencil lines andH coverZ, with total degree m+1≤k_A.

This is a complete case distinction, including concurrency between the added lines. An intersectionA₁∩A₂ outsideU is a single point ofW on both lines, not two different points. The argument does not require these points to be distinct or ordinary double points.

## 4. Bézout proves the exact Seshadri value

We have constructed a finite union of auxiliary lines coveringZ, of total degreec≤k_A≤k. For any integral curveC not one of these support lines, Bézout gives

    Σ_{p∈Z}mult_p(C)≤c degC≤k degC.

Any support line has at mostk points by definition and therefore ratio at least1/k. A line containingk points supplies the reverse inequality. This proves(1).

This is a genuine all-degree proof, not an inference from finite samples or from the degree bound of turn1. The arrangement may have arbitrarily many lines, arbitrary pencil sizes and continuous moduli.

There is also a finite way to determinek here without checking every projective line. Add all original component lines to the cover's support with weightzero, so its largest point-countk_support is at leastk_A≥c. The turn2 certificate then shows every line outside this finite support has at mostc points. Hencek=k_support, and a finite list of component lines plus at mostone joining line computes the constant.

No assertion that the computing line must belong to the input arrangement is made. Thus this theorem does not silently strengthen the OWR all-lines target to Pokora's possibly stronger original component-line formulation.

## 5. A high-multiplicity corollary

For any arrangement ofn≥3 lines, if it has a singular point of multiplicity

    m≥ceil(n/2)−1,

then the assigned conjecture holds.

If some arrangement line contains at leastceil(n/2) singular points, give every arrangement line weight1/2. Every singular point receives weight at least1, the total cost isn/2, and turn2 applies.

Otherwise every component has at mostceil(n/2)−1≤m singular points. If the arrangement is not a pencil, a line outside the pencil throughP meets its m members in m distinct singular points. It can contain no further singular point off the pencil union. Every off-pencil singular point would lie on such an external component, a contradiction. Thus all singular points lie in the m-line pencil union and the modular-point certificate applies. The pencil case has already been handled.

This corollary combines elementary certificates and is not claimed to be absent from prior literature. It does not resolve arrangements with smaller maximal multiplicity and without the two-line-extension structure.

## 6. Exact controls and remaining work

The checker constructs rational projective two-pencil base arrangements (including their common line at infinity), adds up to two arbitrary lines, enumerates all intersections, constructs the certificate by the proof's cases, and checks every line through pairs of singular points. This supplies exact finite controls of degeneracies and cover construction; the universal proof is Sections2–4.

The next turn will examine whether the same cover argument extends to three added lines, and distinguish a failure of that certificate from an actual Seshadri counterexample. Original status remains unresolved3/5.
