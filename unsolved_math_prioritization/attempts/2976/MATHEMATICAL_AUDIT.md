# Independent mathematical audit: KP-4.100 / problem 2976, attempt 1

Date: 10 October 2026.

## Verdict and exact scope

**Accepted as a correct partial attempt.** The fixed-split-form theorem for `S^2 x Sigma_h`, the formal-immersion reduction, and the stated positive-genus `b2^+ > 1` basic-class consequence are justified. This is neither a proof nor a counterexample to the universal assertion, and no novelty is established or claimed. The unresolved outcome in [STATUS.json](STATUS.json) is appropriate. The distributed [mathematical report](MATHEMATICAL_REPORT.md) is 12,899 bytes, SHA-256 `a94ff0855005fcffa337b3de54888598f7d6137ce0d4c2a2c408b4e8d135d743`. This is an AI-assisted, unrefereed audit; it does not assert external human peer review, journal acceptance, or formal proof-assistant certification. Inspection and finite-check statements record the audit conducted on 10 October 2026, rather than new work during edition preparation.

The audited target keeps the original symplectic form, integral homology class, connectedness, and embeddedness. It asks for some representative, not an isotopy of the supplied smooth embedding. The genus equality is `2g-2 = c^2 + K(c)` with `K=-c1(TX,omega)`. I visually checked the original K3 Problem 4.100 on PDF pages 272–273; its displayed first-Chern formula agrees with this sign. The later use of the word canonical does not override the displayed equation.

In Section 1, it is the quotient Euler-number **difference** that vanishes. The quotient Euler number itself is `c^2`, which need not be zero. Exact public proof and audit byte counts and SHA-256 bindings are in [ACCEPTANCE.json](ACCEPTANCE.json).

## 1. Formal monomorphisms, immersion, and torsion

The complex monomorphism exists by transversality: the relevant complex rank-two Hom bundle is real rank four over a real two-dimensional surface, so a generic section avoids its zero section. Nonzero complex maps from a complex line are injective. Its quotient line has first Chern number `c1(TX)(c)-chi(S)=c^2`, equal to the oriented normal Euler number of the original embedding.

Li's Remark 2.5 explicitly classifies components of real monomorphisms over a closed oriented surface by quotient Euler number, with the required parity condition. This is exactly the comparison made in the attempt. Independently, the oriented real Stiefel fiber `V_2(R^4)` has `pi1=0` and `pi2=Z`: in the fibration `SO(2) -> SO(4) -> V_2(R^4)`, the map on fundamental groups is reduction modulo two. A generator of the obstruction therefore changes quotient Euler number by two. The connected structure group acts trivially on this integer, and `H^2(S;Z)=Z`; equality of Euler numbers kills the obstruction. No torsion obstruction has been discarded.

The pointwise square-root rescaling of the complex monomorphism is correct for a two-form. It yields the chosen positive area form `sigma`, and equality of total area gives the required de Rham cohomology equality on the closed connected domain. Li's Theorem 2.7 explicitly permits a closed domain and real codimension two; its domain remains the same surface. Theorem 2.6, for embeddings, instead requires real codimension at least four. The attempt uses these distinctions correctly.

The homotopy preserves the **integral** represented class, including any torsion component. Positivity of symplectic area rules out a wholly torsion input class. No step replaces integral homology with homology modulo torsion. Proposition 2.8's normal Euler formula is consistent with the attempt's sign convention.

For the resulting symplectic immersion, an almost-complex splitting of the pullback tangent bundle gives `e(N)=c1(TX)(c)-chi(S)=c^2`. This splitting is on the domain and does not require a single ambient almost-complex structure compatible with both branches at a double point. A sufficiently small generic smooth perturbation preserves symplecticity because it is C1-open; self-transversality and absence of triple points can therefore be arranged. The ordinary signed self-intersection formula then gives `d_plus=d_minus`.

The two-plane negative-intersection example is valid: both ordered plane bases have symplectic area one, whereas their concatenated determinant is minus one. Consequently the proof correctly refuses to infer positivity of all intersections, or removal of opposite-sign pairs. Balanced double points leave the essential four-dimensional embedding problem unresolved.

## 2. Fixed-form split product construction

### Homology and genus bookkeeping

The Kunneth decomposition has only the two displayed degree-two generators because `H1(S^2)=0`; thus `c=aF+bB` covers every integral class. The intersection matrix, canonical pairings, genus, and area in the attempt are correct. There is no omitted mixed homology summand. Neither coefficient is assumed primitive or positive at the start.

### Sign-controlled degree maps and negative sections

The collapsed-disc construction is smooth and exists in every genus. In polar coordinates on a disc, one explicit local model to the standard oriented sphere is

`(r,theta) -> (sin(alpha(r))*cos(theta), sin(alpha(r))*sin(theta), cos(alpha(r)))`,

where `alpha(r)=r` near zero, `alpha` increases monotonically to `pi`, and it is identically `pi` on a boundary collar, flat where that collar begins. At the center, `sin(r)/r` and `cos(r)` are smooth functions of Cartesian coordinates. At the collar all nonconstant derivatives vanish. The Jacobian sign is the sign of `sin(alpha)*alpha'`, hence nonnegative. A regular value away from the poles has one positively oriented preimage. Pullback of any other positive target area form has the same sign. Disjoint copies yield arbitrary nonnegative degree and extend by the same constant on the complement. Orientation reversal yields arbitrary negative degree with nonpositive pullback. Thus this construction does not require a holomorphic map, which would impose inappropriate restrictions.

For degree `-k`, the proof uses `rho=-f^*sigma`, not an assumed strictly positive form. Adding `t*tau`, with `t=(mu-k*lambda)/mu>0`, makes `tau_prime` strictly positive even on the collapsed region and gives it the same integral as `tau`. The straight-line path between these area forms is positive and cohomologous, so Moser supplies an identity-isotopic `phi` with `phi^*tau_prime=tau`. The displayed identity

`tau + (f composed with phi)^*sigma = t*phi^*tau > 0`

is exact. It changes the graph rather than the ambient form. The graph is embedded, connected, of genus `h`, and represents exactly `aF+B`. This proves every positive-area section case, including negative square and both sphere-factor choices when `h=0`.

### Connected cyclic multisections and smoothing

For `h>=1`, a primitive integral class in `H^1(Sigma_h;Z)` gives a smooth circle-valued map with surjective induced map to `Z`. Reduction modulo `b` remains surjective, so the covering defined by `z^b=epsilon^b*theta(x)` is connected. This also applies for `h=1` and every `b>=1`; no primitivity of `bB` is needed.

The roots never meet zero, so the equation defines a smooth embedded covering. Each local root has image in a circle and therefore pulls back the sphere area form to zero. The induced covering orientation makes the base-area pullback positive. The sphere-factor projection has degree zero, while the base projection has degree `b`, proving the exact class `bB`. Covering Euler characteristic gives genus `1+b(h-1)`.

The circle-valued map can be made constant on finitely many small base discs by local homotopies without changing its induced map on fundamental groups. The added sphere fibers then meet it at distinct positive product-orthogonal nodes. In product Darboux coordinates, these are the coordinate-axis symplectic nodes to which the usual local symplectic smoothing applies. The smoothing can be performed in disjoint neighborhoods, preserves the total class and the fixed form, and introduces no further intersections. Each fiber attaches to the existing connected multisection, so the result stays connected. Euler characteristic decreases by two per node; with `a` spheres and `ab` nodes this gives exactly `1+b(h-1)+a(b-1)`.

### Exhaustion, including h=0 and h=1

- For `h>=1, b<0`, positive area forces integer `a>=1`, and the claimed bound `g<=bh<0` follows because `b-1<0`.
- For `b=0`, area and nonnegative genus force `a=1`.
- For `b=1`, the section construction has no further sign restriction on `a` beyond area.
- For `b>=2`, projection of the supplied smooth surface has degree `b`. Kneser's inequality yields `g>=1+b(h-1)`, and then `a>=0`. The theorem also covers the torus target: it excludes degree-nonzero maps from a sphere to a torus. Ryabichev's statement is for geometric degree; for these oriented surfaces and positive cohomological degree it agrees with the degree used here. No negative-degree convention is being imported.
- For `h=0`, `(a-1)(b-1)>=0` means both coefficients are at least one or both at most one. In the latter case positive area forces at least one coefficient to equal one. These are exactly the two section families. In the former case the complete bipartite grid has connected component graph and smoothing genus `(a-1)(b-1)`.

These are universal algebraic case splits, not extrapolations from a finite computation. They prove the stated product theorem and nothing about nonsplit forms on general four-manifolds.

## 3. Basic-class inequalities, including negative square

I visually checked Ozsvath–Szabo Corollary 1.7 on PDF page 5 (printed page 97). It requires an embedded oriented closed positive-genus surface of **negative square**, Seiberg–Witten simple type, and `b2^+>1`. It imposes no lower bound on the negative square and no primitivity condition. The conclusion is precisely `|L(c)|+c^2 <= 2g-2`. Their Section 3, Remark 3.3 on PDF page 13, explicitly recalls Taubes' simple-type theorem for symplectic four-manifolds with `b2^+>1`. Thus all these hypotheses are available here, including when `g=1`.

For nonnegative square, the usual positive-genus adjunction inequality also applies; the nonzero nontorsion requirement is ensured by positive symplectic area. Canonical basic classes are available by Taubes' theorem (the canonical Spin-c convention gives `-K`, and conjugation gives `K`; the absolute-value conclusion is unaffected). Consequently cancellation of `c^2` is legitimate in both ranges. The interval `0<=A.c<=K(c)` is exactly equivalent to the inequality for `L=K-2PD(A)`. Torsion pairings vanish but are not confused with integral equality of classes.

The exclusions in the attempt are essential and correct: this argument supplies no genus-zero claim, no arbitrary stable-class claim, and no chamber-independent `b2^+=1` claim. It blocks the specified counterexample strategy only when all its hypotheses hold.

## 4. Prior work, scope controls, and evidence

The credit to existing rational/ruled work is retained. I checked the pertinent Li–Li introduction and theorem statements and Li–Usher Section 2; they support the literature context, not an exact general sufficiency theorem.

I visually checked Dorfmeister–Li–Wu Theorem 1.3 and the statements on PDF pages 6–7. Theorem 1.3 starts with a preexisting symplectic configuration, so cannot create the arbitrary target representative from the smooth hypothesis alone. Theorem 1.8 supplies the stated rational square-minus-four sphere sufficiency. Theorem 1.9 supplies the stated irrational-ruled sphere sufficiency. Their Speculation 1.10 is aligned with the universal question, but its historical status is not a current-resolution certificate.

Sources and public landing pages:

- K3 problem list, Problem 4.100: https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- Li, *Existence of symplectic surfaces*: https://arxiv.org/abs/0812.4929
- Ozsvath–Szabo, *The symplectic Thom conjecture*: https://arxiv.org/abs/math/9811087
- Ryabichev, *Short proof of the Kneser–Edmonds theorem on the degree of a map between closed surfaces*: https://arxiv.org/abs/2401.01041
- Li–Li, *Symplectic genus, minimal genus and diffeomorphisms*: https://arxiv.org/abs/math/0108227
- Dorfmeister–Li–Wu, *Stability and existence of surfaces in symplectic 4-manifolds with b^+=1*: https://arxiv.org/abs/1407.1089
- Li–Usher, *Symplectic forms and surfaces of negative square*: https://arxiv.org/abs/math/0601540

The recorded audit independently verified all seven source PDF hashes and byte counts and visually inspected relevant pages rather than relying on extracted signs alone. The recorded authored arithmetic check passed and reproduced its prior result byte-for-byte, covering 40,931 adjunction triples and auxiliary identities. The recorded independent checks passed on 33,750 parameter tuples and five explicit boundary or negative controls. These are finite sanity checks only; the geometric and all-integral-class arguments are the written proofs above and in the mathematical report. Public source identities and inspection history are in [SOURCE_METADATA.json](SOURCE_METADATA.json). Programs and raw generated outputs are not distributed, and no excluded file is a mathematical premise. Edition preparation did not rerun these checks, retrieve or rehash source PDFs, or conduct new scholarly inspection.

The precise remaining task is to construct an embedded connected representative for an arbitrary fixed symplectic four-manifold, or supply a concrete sharp positive-area smooth class for which every same-class symplectic embedding is obstructed. This audit establishes neither. The proof-only edition preserves this partial verdict; it changes no QUEUE entry and adds no substantive proof-attempt response.
