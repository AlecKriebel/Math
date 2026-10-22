# Classical elliptic / conic priority audit of PR200 k115

Audit date: 2026-10-16 UTC. Scope: a bounded independent classical-family audit, not novelty clearance. The approach was frozen before the permitted candidate proof was read. No Git, refs, PR, publication, or external communication action was performed.

## Result

**No exact classical prior statement or fully specified classical theorem implying the complete k115 claim was located in this search.** This negative finding is limited to the inspected sources and queries. It does not establish firstness, independence, worldwide openness, or permission to publish.

There is definite older partial coverage, including a genuine focal-distance product theorem. It must be distinguished from the full phase-product:

- Chasles (1838), p. 108, proves the focal alternating-ratio relation for a circumscribed quadrilateral. An anonymous 1853 note, §2 p. 219, gives the corresponding result for every even circumscribed polygon. Its §5 p. 220 gives a related vertex/contact-point product ratio for odd polygons. These are exact classical focal-product statements, but they do not assert that the full product is constant as a Poncelet family moves. [Chasles primary source](https://www.numdam.org/item/JMPA_1838_1_3__102_0/); [1853 primary source](https://www.numdam.org/item/NAM_1853_1_12__218_1/).
- The outer tangent-intersection polygon and its conic locus are routine polar reciprocity. Fouché (1915), §4 pp. 149–150, explicitly records the Poncelet conic chain under polarity, attributing the observation to Poncelet. The precise translation gives the outer locus semiaxes `a²/alpha, b²/beta`, exactly the candidate's `A_o, B_o`. The locus itself should not be described as a new contribution. [Primary source](https://www.numdam.org/item/BSMF_1915__43__146_1/).
- Jacobi's 1828 paper, Darboux's 1880 note and 1917 exposition, and Greenhill's 1892 treatment contain the classical elliptic translation, torsion closure, transformation, and product-factor machinery. None of the inspected passages identifies the k115 focal observable and its divisor. Precise locations and inspection levels are in the source ledger.

## Exact claim checked against the literature

Let `E` have semiaxes `a>b>0` and foci `F±=(±c,0)`, where `c²=a²-b²`. A proper nested nondegenerate confocal elliptical caustic has semiaxes `alpha>beta>0`. For a primitive billiard orbit of least period `N` and any coprime admissible turning number, `Q_i` is the intersection of the tangents to `E` at successive billiard vertices. The main claim is constancy in the phase of

`R± = product_i |Q_i-F±|`

for `4 | N`, with `R+=R-`. This audit concerns these ordinary positive Euclidean distances. Products to original billiard vertices, products of focal altitudes to sides, alternating products, and foci of the *outer locus* are different observables.

The optional claim is that, in this strict noncircular model, phase constancy holds **if and only if `4 | N`**. This audit found no exact classical classification statement. It also found no basis for treating that classification as a separate novelty claim.

## What the old focal theorem actually gives

Writing `r_i±=|Q_i-F±|`, the 1853 §2 theorem gives

`(product_odd r_i+)/(product_even r_i+) = (product_odd r_i-)/(product_even r_i-)`.

It is a relation between the foci for one circumscribed polygon. The common ratio may depend on that polygon. It is not the full product `product_i r_i±`, and it gives no phase-constant value. The technical addendum provides two exact parallelograms circumscribed about the same ellipse, satisfying this older identity, whose full products are `16` and `52/3`. This only demonstrates the insufficiency of that old theorem alone; it is **not** a counterexample to k115.

Polarity turns the original confocal Poncelet polygon into a polygon inscribed in a new conic and circumscribed about `E`. A general projective transformation can further turn suitable pairs into circles, but it does not preserve the Euclidean distances to `F±`. Pulling back a circular statement requires the actual metric factors. Invoking Poncelet/Jacobi duality without those factors transfers the central difficulty.

## Standard norm method versus an exact prior result

For a finite translation subgroup `G` of an elliptic curve, the product of a meromorphic function over `G` is its cyclic norm. Its divisor is the sum of the translated divisors. A zero divisor on the compact torus forces the norm to be constant. This is standard elliptic-function machinery. Classical product and multiplication formulas implement the same mechanism.

For the present observable, the substantive missing historical implication is an older identification of

`H(u) = (|Q(u)-F+| |Q(u)-F-|)²`

with the specific meromorphic divisor

`2[p+K] + [p+K+delta] + [p+K-delta] - 4[p]`,

including the degree drop at `N=4`. Once this divisor is supplied, the norm cancellation is a short torsion calculation. An old multiplication formula or a general result that elliptic functions with matching zeros and poles are proportional is not by itself an exact prior k115 theorem. The candidate must still not claim invention of the norm method, the elliptic parametrization, the polar outer locus, or the general divisor principle.

The generic assertion “classical algebra already proves k115” is **blocked at this exact observable-identification gap** in the inspected literature. Reopening it would require an older source that gives the metric factorization/divisor, or a different complete specialization that bypasses that calculation. Merely restating the norm criterion does not supply that evidence.

## Optional converse

The technical addendum independently checks the arithmetic consequence of the candidate's divisor. On the paired torus, the step has order `m=N/gcd(N,2)`. Its orbit subgroup contains the real half-period `K` exactly when `m` is even, equivalently `4 | N`. When `m` is odd, the norm has a nonzero divisor.

For odd `N`, this norm is `(R+ R-)²`, not `R+²`. The identity `R-(u)=R+(u+2K)` nevertheless shows that constancy of either one-focus product would force constancy of both, contradicting the nonzero norm divisor. Thus the full parity classification follows from the same candidate divisor, with no antipodal pairing inserted into an odd orbit. This is a mathematical deduction conditional on the candidate's geometric factorization, not a classical priority discovery.

## Search bounds and residual uncertainty

The search covered English, French, and German focal/product terminology; primary scans in Numdam and Internet Archive; author collections; and targeted passages of classical elliptic/conic treatises. The source ledger distinguishes rendered-page verification, extracted full-article reading, targeted book reading, and unresolved bibliographic leads. Poncelet's entire 1822 treatise and all nineteenth-century problem journals were not exhaustively searched. Loria 1889 was located bibliographically but not obtained in full. No external person was contacted.

A contemporary exact-match source was supplied by the root audit during this work. I did not open it, inspect sibling priority verdicts, or use its conclusions; its chronology and attribution are outside this classical family.

This audit is complete as a bounded evidence package. Editorial and publication decisions remain with the root/human process.
