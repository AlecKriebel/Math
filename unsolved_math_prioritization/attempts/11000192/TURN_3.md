# Author turn 3: the angle is a simple-curve trace square

**Outcome: scoped partial, original problem unresolved 3/5.** The source's particular angle invariant has a stronger obstruction than the failed three-chain word: its entire mapping-class stabilizer is a simple-curve stabilizer. This is an unreviewed, convention-bound deduction requiring independent review before any public source critique. It does not disprove Goldman's requested measurable nonergodicity example or assert that every possible rational invariant has the same property.

## 1. Exact quaternion simplification

Retain precisely the four-square relations and pullback conventions of Turns 1–2. This calculation works without fixing the tree gauge. Put

 δ=A2−A3, V=A4δ, P=A1δ, A=A1 A4^(-1), b=B1, s=|δ|².

The source's two vectors are V and b^(-1)Pb, and its projective-angle function is

 F=<V,b^(-1)Pb>²/(|V|²|P|²).

The square relations give

 A4 A3=b3(A4 A2)b3^(-1),
 A1 A2=b(A1 A3)b^(-1).

Consequently V and P are pure imaginary quaternions. Moreover P is orthogonal to the imaginary part of b, since it is the difference of a quaternion and its conjugate by b. Thus

 P b=b^(-1)P.

We also have P=AV and |P|²=|V|²=s. Since AV is imaginary, quaternion conjugation gives V A^(-1)=A V, equivalently V A=A^(-1)V. Therefore

 V P=V A V=A^(-1)V²=−s A^(-1).

For imaginary quaternions the Euclidean inner product is minus the real part of their product. Combining these identities,

 <V,b^(-1)Pb>
 =−Re(V b^(-1)P b)
 =−Re(V P b²)
 =s Re(A^(-1)b²).

Hence, everywhere the original angle is defined,

 **F=(Re(A^(-1)b²))² = (tr ρ(q))²/4,**

where the based loop is

 q=(a1 a4^(-1))^(-1) b1².

This is an identity on the whole source representation space, not an inference from a rational sample or a generic rank assumption. The original angle still has no value when δ=0. Its trace-square expression provides a continuous regular extension across that set; it does not retroactively make the original quotient defined there. The two irreducible nonconstancy witnesses from Turn 1 remain valid.

## 2. The loop q is essential and simple

This step uses the actual source Figure 3, rather than interpreting a group word as simple merely from its abelianization. The edges a1 and a4 are distinct embedded edges joining the two distinct vertices, with disjoint interiors. The two-edge cycle a=a1 a4^(-1) is therefore an embedded circle in the quotient square complex. Each valence-two corner can be smoothed in the surface, including at its cone-metric vertices. No edge interiors are collapsed or identified with one another.

The square gluing can also be reconstructed from four unit squares with horizontal permutation (1)(23)(4) and vertical permutation (12)(34). It has exactly two vertex classes. The a1 and a4 edges connect those classes, and the cellular integral one-cochain that is 1 on a1 and 0 on all other edge labels is closed. It pairs with a to give 1. Thus a is homologically nonzero, in particular essential and nonseparating. The checker reconstructs these corner identifications and the cellular pairing directly.

Let A denote the source's Dehn twist, now as an automorphism rather than a quaternion. Its recorded action and first square relation give

 A(a)=A(a1 a4^(-1))=a1 b2 a4^(-1)=b1 a,
 A(b1)=b1.

It follows that A^(-2)(a)=b1^(-2)a, whose inverse is exactly q. Thus q is the inverse of a Dehn-twist image of the essential simple nonseparating curve a. This proves its geometric type without any assertion that every primitive homology class is represented by its given word as a simple curve.

## 3. The full stabilizer of this function

The complete primary paper of Charles–Marché, arXiv:0901.3064v1, has now been retrieved. Its Theorem 1.1 (PDF p. 4), proved by Theorem 5.3 (pp. 19–20), states that the products of negative trace functions indexed by isotopy classes of essential multicurves are linearly independent on the SU(2) character space of a compact oriented surface of negative Euler characteristic. Parallel components are permitted. We use this published theorem with credit; no Zariski-density or complex-component argument is needed.

Let 2q denote two disjoint parallel copies of the unoriented simple curve q, not a twice-traversed loop. Its multicurve trace function is

 f_(2q)=(-tr ρ(q))²=4F.

For any orientation-preserving mapping class f, pullback sends this function to the trace function of the image multicurve 2f(q), with the inverse convention making no difference to the stabilizer conclusion. If f preserves F, Charles–Marché linear independence implies that 2f(q) is isotopic to 2q. Therefore f(q) is isotopic to q as an unoriented curve. Conversely, a mapping class fixing q preserves its trace square. We obtain the exact equality

 **Stab(F)=Stab([q]).**

The same conclusion holds if preservation is only almost everywhere for Goldman measure. The trace-square extensions are continuous. The irreducible locus is dense, smooth, and every nonempty open subset there has positive symplectic volume. A continuous difference vanishing almost everywhere vanishes on that locus and then everywhere. Preservation of the source's rational angle on its invariant conull domain therefore suffices.

Every element of this stabilizer preserves an essential simple curve and hence is not pseudo-Anosov on the closed genus-two surface. This conclusion is about the entire stabilizer of the specific F, not just <C,D,R>. In particular, if the lifted intersection in the source preserves the two projective lines as established under the recorded conventions, its projection is contained in Stab([q]) and cannot supply the sought pseudo-Anosov.

This advances the earlier displayed-word diagnosis to a function-level obstruction. It remains tied to the exact source lifts and angle formula. It is not a statement that every group vaguely described as an intersection in the unbased mapping class group is reducible; forgetting the chosen lifts changes the problem.

## 4. A credited general consequence for the next route

The same multicurve-basis theorem has an elementary useful consequence. A finite trace-algebra function has a unique finite expansion

 H=Σ c_γ f_γ.

The mapping class group permutes the multicurve basis. If a pseudo-Anosov f preserved H, its finite nonzero support would be permuted by f. Each supported nonempty multicurve would therefore be fixed by a positive power of f. Its finite collection of essential simple components would then have finite orbit, contradicting pseudo-Anosov type. Only the empty multicurve, whose function is constant, can occur. Hence:

 **A pseudo-Anosov has no nonconstant invariant in the finite trace algebra.**

This is a direct consequence of the credited Charles–Marché theorem and the definition of pseudo-Anosov irreducibility. It is not a new theorem claimed on their behalf. In particular, a prospective nonergodicity example cannot be certified by a nonconstant regular trace-polynomial invariant. An arbitrary rational quotient or a measurable invariant need not have finite multicurve support, so this argument does not settle either category. It does not establish ergodicity, even when every regular invariant is constant.

## 5. Exact diagnostics and remaining problem

The checker evaluates the unsquared numerator identity and trace-square formula on exact unit-quaternion representations from both earlier families, transformed by source generators in both directions. These transformations include nontrivial A4, so the nongauged A1 A4^(-1) placement is tested. It also checks source-subgroup controls, simultaneous conjugation, the two explicit δ=0 irreducible cases, the distinction between a double multicurve and the trace of a twice-traversed loop, and the square-complex/cellular certificate for a.

Finite controls do not prove Charles–Marché's theorem or pseudo-Anosov irreducibility; the proof uses the cited exact theorem and the geometric argument above. No new pseudo-Anosov example has been found in this turn. The next turn must move beyond this now-blocked regular invariant or supply a materially different mechanism, such as a genuinely nonregular invariant or dynamical obstruction to ergodicity. The original full Goldman target remains unresolved after **3/5** substantive author turns.
