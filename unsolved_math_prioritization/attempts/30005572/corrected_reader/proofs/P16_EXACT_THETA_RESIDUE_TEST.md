# Exact CM theta-symbol residues at the first admissible 2-power level

Shared PASS3/5, row 1777 / 30005572. 14 October 2026 UTC.

## Result and acceptance boundary

This lane computes an actual local Steinberg tame symbol of a specified, normalized rational CM theta function. It does **not** identify that symbol with the LSSW cocycle value in PASS2 equation (7.6), construct a relative map, or prove a nonzero absolute residue. The full construction and the actual surviving cocycle-residue identity remain open.

For F=Q(sqrt(-23)), w=(1+sqrt(-23))/2, q=(2,w), and level N=q², choose a CM elliptic curve E over a finite extension K of Q₂ unramified over Q₂, with good reduction, all O_F endomorphisms defined over K, and the chosen q-adic CM type. Such local models are supplied by the source's CM definition fields F(f), with f coprime to 2: these are unramified at q and have good reduction there. Let P be a primitive q²-torsion point. Write j̄ for the reduction of j(E).

For the standard fifth division polynomial ψ₅, put

  θ₅ = Δ²/ψ₅.

The exact conclusions are:

1. K(P)/K is totally ramified quadratic. Both A=θ₅(P) and B=θ₅(wP) belong to K, although P does not.
2. With τ{u,v}=(-1)^{v(u)v(v)} overline(u^{v(v)}/v^{v(u)}),

     τ_{K(P)}{A,B}=j̄,       τ_K{A,B}=j̄⁴.

   Each is a nonidentity element of order seven.
3. The coefficient-normalized symbol (1/24²){A,B}, which is unambiguously defined in K₂(K)⊗Z[1/6], has residue j̄². This is a specified symbol, **not an asserted value of the missing relative map**.
4. For admissible nonzero coordinates c,d modulo q², the raw theta-pair residue is exactly j̄^{4(ε(d)-ε(c))}, where ε is zero on units and one on q\q². Thus these nonzero edge residues have a simple potential on the represented cusp graph. This permits telescoping; it is not a counterexample to integral absolute values.

The field K can have residue field larger than F₈. The calculation retains the actual CM reduction: j̄ lies in its canonical F₈ subfield and is not in F₂. No claim that matrix coefficients in F₂ force theta constants into F₂ is made.

## 1. Source facts versus authored calculation

The following inputs are used at their source scope.

- LSSW, author manuscript §§3.1, 3.4 and 4.2: one may choose CM definition fields F(f) away from a given level; their CM curves have good reduction away from f. The auxiliary theta primitive has divisor Nc(0)-E[c] and is trace-fixed. The actual arithmetic map is constructed from the geometric Gersten cocycle, not by simply assigning a two-theta symbol to every path. The introduction expressly leaves relative formulas untreated.
- The usual Robert/Kato theta normalization for multiplication by an integer t prime to 6 is the analytic quotient Θ(z)^{t²}/Θ(tz). Its algebraic expression for t=5 is verified below rather than guessed from the divisor alone. Chida's account, §8, records the divisor, norm compatibility and analytic Robert prescription (with its root-of-unity normalization).
- The Hilbert class polynomial for discriminant -23 is

     H_{-23}(J)=J³+3491750J²-5151296875J+12771880859375.

  The displayed polynomial is independently recorded in the Sage/Kohel database documentation. We use this documented exact polynomial; the accompanying script verifies its reduction and finite-field consequences, not the Hilbert class polynomial algorithm itself.

Everything in §§2–6 below is an authored derivation from these facts and elementary formal-group/division-polynomial identities. It is not quoted as a theorem of the later paper.

Public references:

- https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf
- https://www.kurims.kyoto-u.ac.jp/~kenkyubu/bessatsu/open/B4/pdf/B04_014.pdf
- https://doc.sagemath.org/html/en/reference/databases/sage/databases/db_class_polynomials.html

These sources were inspected on 14 October 2026. No literature-exhaustiveness or novelty claim is made.

## 2. Theta normalization, including the constant

Use an integral Weierstrass equation

  y²+a₁xy+a₃y=x³+a₂x²+a₄x+a₆

with unit discriminant Δ, and parameter T=-x/y at the origin. The standard odd division polynomial ψ₅ is a polynomial of degree 12 in x, with leading term 5x¹². Consequently

  ψ₅(T)=5T^{-24}(1+O(T)),
  θ₅(T)=(Δ²/5)T²⁴(1+O(T)).                         (2.1)

The error series in (2.1) has coefficients in the integral base ring. In particular its value at a point reducing to zero is congruent to one.

Under a Weierstrass change x=u²x'+r, y=u³y'+su²x'+t, ψ₅ scales by u²⁴ and Δ by u¹². Thus Δ²/ψ₅ is invariant. Polynomial degree 12 is not Weierstrass weight 12; the weight of ψ₅ is 24. Its divisor is 25(0)-E[5].

To check the constant in the theta prescription, write the normalized analytic theta as a scalar C times the Weierstrass sigma function times its exponential quadratic correction. Its leading scalar satisfies C¹²=Δ. In the quotient Θ(z)²⁵/Θ(5z) the quadratic correction cancels. The classical odd division-polynomial identity ψ₅(z)=σ(5z)/σ(z)²⁵ then gives

  Θ(z)²⁵/Θ(5z)=C²⁴/ψ₅(z)=Δ²/ψ₅(z).

An alternative convention differing by a twelfth root of unity has no effect on the seven-primary conclusion: the resulting changes to tame symbols are of order dividing 12. The exact formula in this report fixes θ₅=Δ²/ψ₅, so its displayed tame symbols have no unspecified constant. The proof therefore does not infer a normalization merely from matching divisors.

The function θ₅ is even, since ψ₅ is a polynomial in x.

## 3. CM formal group and the marked-point extension

The element w satisfies w²-w+6=0 and has q-adic valuation one. Reduction modulo q² identifies O_F/q² with Z/4Z, and w with 2. Hence a primitive q²-point has fourfold additive order, wP is the unique nonzero q-point, and the possible O_F-linear Galois actions on P are P and -P.

Modulo 2, H_{-23} is J³+J+1. It has no root in F₂ and is irreducible of degree three. Therefore j̄ has degree three over F₂ and order seven in F₈×. In particular j̄≠0, so the good characteristic-two reduction is ordinary and ā₁≠0.

We use the formal parameter T of §2 and normalize the valuation v₀ on K by v₀(2)=1. Let

  [w](T)=wT+A₂T²+O(T³).

The coefficient A₂ reduces to ā₁. Here is a check that does not pretend q is principal. The identity [w]∘[1-w]=[6], together with w≡0 and 1-w≡1 modulo q, shows that the quadratic coefficient of [w] modulo q equals that of [6]. The standard formal doubling law has [2](T)=2T-a₁T²+O(T³), and [3]'(0)=3 reduces to one. Thus the quadratic coefficient of [6] modulo q is ā₁. All higher formal coefficients are integral.

The q-primary subgroup is the connected ordinary branch: [w] has inseparable degree two on reduction, while its prime-to-two kernel contributes no nonidentity point reducing to zero. The Newton polygon of [w](T)/T starts with a constant of valuation one and a unit linear coefficient. Its one nonzero formal q-torsion point R has v₀(T(R))=1.

Now R=wP. The primitive q²-point also reduces to zero. If s=v₀(T(P)), then s≥1 would give v₀(T(wP))≥2, impossible. For 0<s<1, the quadratic term is strictly smaller in valuation than the linear and higher terms. Therefore 2s=1 and

  v₀(T(P))=1/2,
  T(wP)/T(P)² ≡ ā₁.                                  (3.1)

The Galois orbit of P has size at most two, because O_F/q² has only two generators. The half-integral valuation forces a ramified quadratic extension. Thus K'=K(P) has ramification index two, no residue extension, and its normalized integer valuation v' satisfies

  v'(T(P))=1,      v'(T(wP))=2.                         (3.2)

The nontrivial automorphism carries P to -P. Evenness of θ₅ proves A,B∈K. In fact wP is already K-rational.

This explicitly distinguishes the marked-point field from the ray field: the admissible q² ray field is H, since the local-unit group has order two and is the image of {±1}. The good-model marked torsion can still require the ramified quadratic extension K'/K. Nothing here identifies K' with H at q.

## 4. Exact tame-symbol calculation

Set t=T(P), U=Δ²/5. Equations (2.1) and (3.1) give in K'

  A=U t²⁴(1+o(1)),
  B=U A₂²⁴ t⁴⁸(1+o(1)),

where each parenthesized factor reduces to one, and A₂ reduces to ā₁. Therefore v'(A)=24 and v'(B)=48. The tame-symbol sign is one, and

  τ_{K'}{A,B}
     = Ū²⁴ ā₁^{-576}
     = Δ̄⁴⁸ ā₁^{-576}.

For a general Weierstrass equation in characteristic two, c̄₄=ā₁⁴, so j̄=ā₁¹²/Δ̄. It follows, with no assumption that ā₁ lies in F₈, that

  Δ̄⁴⁸ ā₁^{-576}=j̄^{-48}=j̄,                       (4.1)

because -48≡1 modulo seven.

Restriction of K₂ along K'/K raises a tame symbol to the ramification index, after the residue inclusion. Thus

  (τ_K{A,B})²=τ_{K'}{A,B}=j̄.

The residue field has characteristic two, so its multiplicative group has odd order and squaring is an automorphism. The unique square root of j̄ is j̄⁴. This proves

  τ_K{A,B}=j̄⁴.                                       (4.2)

This calculation is algebraic and exact; it is not a floating-point theta approximation.

## 5. Legitimate coefficient normalization and the smoothing warning

Let R=Z[1/6]. Since 24 is a unit in R, the symbol

  Z(P,wP)=(1/576){θ₅(P),θ₅(wP)} ∈ K₂(K)⊗R

is well-defined. Its seven-primary residue is

  τ_K Z(P,wP)=j̄^{4/576}=j̄²,                         (5.1)

where division in the exponent means multiplication by the inverse of 576 modulo seven; 576≡2 and 2^{-1}≡4.

At N=q², 5≡1 modulo N, so the smoothing ideal c=(5) is ray-trivial and Nc=25. The formal calibration scalar for an unaugmented two-theta class is 25²-1=624, not 24². Thus the correctly scaled *candidate* smoothed class would be

  (624/576){A,B}=(13/12){A,B},

whose residue is again j̄², since 624≡1 modulo seven. The report does not assert that this candidate equals cΘ(γ), or that an arbitrary pair (1,w) is an absolute class. PASS1 already rules out replacing the geometric cocycle by a generic two-auxiliary-theta formula without its mixed terms and relations.

The coefficient normalization is safe because the denominator uses only two and three. No division by seven, no choice of a root in a finite K₂ group, and no exception to source p≥7 is hidden here. Nevertheless the canonical comparison, global relative relations, and full class-component assembly are separate missing obligations.

## 6. The exact local endpoint-potential pattern

For c∉q², define ε(c)=0 when c∉q and ε(c)=1 when c∈q\q². Because O_F/q²≅Z/4Z, we have exact equalities

  θ₅(cP)=A if ε(c)=0,
  θ₅(cP)=B if ε(c)=1.

For (c,d,q²)=O_F, at least one coordinate is a unit. Hence the only possibilities are (A,A), (A,B), and (B,A). Their residues are respectively 1, j̄⁴ and j̄^{-4}. Thus

  τ_K{θ₅(cP),θ₅(dP)}=j̄^{4(ε(d)-ε(c))}.               (6.1)

After the 1/576 normalization the exponent 4 becomes 2.

On the graph of genuine unimodular cusp edges in a fixed same-curve component whose endpoint denominators are nonzero modulo q², attach the potential j̄^{4ε(c)} to an endpoint with denominator c. This is independent of scaling a primitive O_F-vector by a unit. It is preserved by the strict Γ₁(q²) action, whose lower row is (0,1) modulo q²; adding the central unit action does not change ε. Equation (6.1) is exactly the ratio of endpoint potentials. Therefore every endpoint-balanced chain in this represented graph has product of these residues equal to one.

This last conclusion does not assume all Bianchi cusps admit global unimodular representatives, does not generate full compactified homology, and does not compare different CM components. It is the precise graph test of PASS2 §7.2 applied to the displayed local symbols, with all those limitations retained.

## 7. What is still needed for equation (7.6)

The new calculation isolates rather than bypasses the missing bridge. It shows that the theta constants can retain nontrivial F₈ dependence, and that individual admissible theta-symbol values need not be integral. It simultaneously exhibits exact local cancellation on represented cycles.

To turn this into integrality of the actual LSSW map, one still needs a proved comparison between these normalized/smoothed theta symbols and the specialized Gersten cocycle, with the correct moving primitive and all class-group components. Alternatively one could compute the geometric cocycle directly on an actual homology generating set. Neither has been done here. In particular, no nonzero evaluated residue of cΘ_{(r,1),N}(γ) is claimed.

The calculations give no unrestricted bad-U identity, no five-primary arithmetic construction, and no full relative or compactified integer-ring map. The original row remains UNSOLVED.
