# Literal Verdure discrepancy and the independent Fisher interface

Bounded finding, not a paper-wide PASS/DEFER. No current family report or ROOT_REVIEW was read. The actual cached primary pixels, fresh text from the supplied Fisher PDF and relevant native TeX were inspected independently. Root's hint was treated as a question.

## What the scan actually prints

Verdure, *Lagrange resolvents and torsion of elliptic curves*, International Journal of Pure and Applied Mathematics33(1)(2006),75–92: supplied raster10/printed84 gives

    α₅ = 8+5ζ₅+5ζ₅⁴,     β₅ = 3−5ζ₅−5ζ₅⁴.

These definitions occur both above and inside Theorem5. Raster13/printed87, immediately below the fifth-power resolvent identity, instead prints

    A₅ = 8+5z₅+5z₅⁴,     B₅ = 3−5z₅−3z₅⁴.

**The first coefficient is5, not3; the final coefficient is3, not5.** The supplied original and the native diagnostic crop/magnification were individually viewed. This is a real printed mismatch, not just OCR. Printed88/raster14 reverts to α₅,β₅ in the resolvent expression and the specialization criterion, and explicitly uses P₅(t)≠0.

With the native choice φ=1+ζ+ζ⁻¹=(1+√5)/2 and c=φ⁵=3+5φ, the theorem's values are α₅=c and β₅=8−5φ=−1/c. Their sum is11 and product−1, so they are exactly the roots of Q₅(T)=T²−11T−1, as required by Verdure's printed83 definition P₅=T⁵Q₅. The printed87 B₅ differs from the theorem value by2ζ⁴ in characteristic0. It is not fixed by ζ↦ζ⁻¹ and cannot be either of those real-quadratic roots. Thus capital/lowercase notation or a harmless conjugation does not reconcile the literal constants.

The locally supported explanation is a typographical slip in the printed87 definition. However, I have **not** re-expanded the very large preceding MAGMA-derived expressions to certify their entire polynomial identity. Literal printed87 cannot by itself be silently used to derive printed88 with the theorem's β₅. This finding qualifies the printed proof line; it does not establish that Theorem5's correctly stated criterion or the target note is false.

## Native Tate parameter: the correct theorem constants fit

The native TeX uses D_β: y²+(1−β)xy−βy=x³−βx², with β=c′λ/(λ+5r), r=√5, c′=(11−5r)/2=−1/c, and λ∉{0,−5r,−c}. Hand calculation gives

    β−c  = −5r(λ+c)/(λ+5r),
    β−c′ = −5rc′/(λ+5r),
    (β−c)/(β−c′) = −c(λ+c).

All displayed denominators and β(β−c)(β−c′) are nonzero on that stated base. Thus the native β satisfies the smoothness/specialization condition P₅(β)≠0 with the **theorem's** constants. Since −c=(−φ)⁵, Verdure's stated ratio has the fifth-power class of λ+c. The mixed5/3 constant from printed87 must not replace c′. This checks this particular convention/substitution; the plane normalization, twist descent, complete field degrees and Galois claims are outside this challenge.

## Fisher supplies an independent all-fiber route

Actual primary inspected: Fisher, *Some examples of5and7descent for elliptic curves over Q*, JEMS3(2001),169–201, DOI10.1007/s100970100030. Supplied505102-byte author/journal PDF was freshly text-extracted. Personally read Lemma1.1 and its cited-proof line, Tate equation(2), §2.1's full-level definitions and construction through the X(5) equations/cusps (printed179–182), and all Lemma3.4/proof (printed194). Critical printed172,179,194 pixels were independently rendered and viewed. Lemma1.1's external standard exercise is accepted at its stated interface, not newly re-proved here.

This is more than the headline of Lemma3.4, whose displayed rational-point classification is over Q. §2.1 states that Y(5) parametrizes triples(E,P,Q) with e₅(P,Q)=ζ, and gives the action Q↦Q+P with quotient X₁(5). It explicitly constructs X(5)≅P¹ and the universal elliptic-normal-curve family away from the cusps. Lemma1.1(iii) removes automorphisms of the marked pair, including at otherwise exceptional j-values. The relevant geometric full-level cover therefore has five distinct choices of Q over every smooth marked fiber, not only at a generic parameter.

Lemma3.4's actual proof supplies the marked-family map

    β = τ f(τ)/g(τ),
    f=τ⁴+3τ³+4τ²+2τ+1,  g=τ⁴−2τ³+4τ²−3τ+1,
    ε(τ)=(φτ+1)/(τ−φ),  η(v)=(cv+1)/(v−c),
    β=η(ε(τ)⁵).

The final identity can be checked without any scientific script: using φ²=φ+1 and c=φ⁵, its cleared numerator and denominator are respectively

    c(φτ+1)⁵+(τ−φ)⁵ = (1+c²)τ f(τ),
    (φτ+1)⁵−c(τ−φ)⁵ = (1+c²)g(τ).

The nonzero scalar1+c² cancels. Both ε and η are genuine Möbius involutions in characteristic0. Hence with u=ε(τ), the full-level map is u⁵=η(β). This uses Fisher's actual marked/full-level interpretation and the labeling choice, not an inference from equal j-invariants or from a rational-point statement alone.

Over a characteristic0 field containing ζ, restrict the β-line to U=P¹\{0,∞,c,c′}. Both the full-level cover and u⁵=η(β) are finite étale of degree5 there. In the latter, η(β) is an invertible regular function and5u⁴ is invertible, so split fibers remain reduced. The rational map above identifies their function-field covers; their normal finite models over the smooth baseU therefore agree throughout U. Equivalently this is the explicit forgetful cover on marked elliptic curves. There is no excluded smooth j=0/1728 fiber and no assertion that every specialized polynomial remains irreducible.

Finally η(β)=−1/(λ+c), by direct substitution. If θ⁵=λ+c then u=−1/θ, so the radical **fields** coincide. For fixed Kummer-group labeling the classes are inverse, [−1/(λ+c)]=[λ+c]⁻¹, rather than generally equal; this is already distinguished by the native TeX. Thus Fisher provides an independent all-smooth-fiber interface for the needed Kummer step, without relying on the inconsistent Verdure printed87 line. This does not certify the rest of the target paper.

## Access, exposure and limits

All nine supplied Verdure mathematical rasters6–14 and its supplied title raster were viewed; the long polynomial coefficients were read as printed, not re-computed. No new Verdure download was attempted: root's failed author-URL/timeouts are not repeated, and no fresh Verdure PDF/erratum is available in this lane. The finding applies to this exact cached2006scan. Fisher's relevant proof bodies above were read; unrelated descent-rank arguments and the whole paper were not re-audited. The native TeX was read only through the relevant Tate/full-level section; original author assertions are exposure, not independent verdicts.

An optional Pillow magnification attempt failed because PIL is absent in the current interpreter; an attempted view of its absent output also failed. Both literal errors remain in COMMANDS_AND_ERRORS.md. No install, interpreter switch, source repair or scientific run occurred. A distinct ordinary macOSsips crop/resample successfully provided diagnostic pixels while preserving the original. Poppler text/render operations succeeded. All eleven core primary/native inputs have before/after SHA256 evidence; original files were not edited. Source/title pin and complete finite output pins accompany this note. Bounded challenge100% complete; no extended repair or full-paper promotion.
