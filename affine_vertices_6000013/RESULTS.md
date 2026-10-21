# Affine vertices: five scoped approaches and authored partial results

Problem 6000013 / AMR-059-0013, queue 1853. Research date 2026-10-21. No general resolution claimed. Throughout, curves are smooth regular and a vertex means a noninflectional sextactic point (osculating-conic contact at least six). This convention is natural but is not explicitly specified by the original question.

## Approach 1: source and scope recovery

The original 1998 item 4(b) inherits a closed curve on a Riemann surface with a projectively flat connection from 4(a). It does not state completeness, equiaffinity, global affine coordinates, simplicity, homotopy class, or nondegeneracy. The accompanying condition is isolated inflections, not simple inflections. A real oriented affine torus can be given a Riemann surface structure independently of its flat affine connection. If compatibility with that complex structure or a volume-preserving connection was intended, that must be added as a hypothesis; it is not silently assumed here.

Primary sources:
- Furuhata–Matsuzoe–Urakawa (1998), item 4(b): https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_pdf/-char/en
- Sasaki (1995), DOI https://doi.org/10.1007/BF03322277 . Publisher abstract only, rechecked 2026-10-21; full text not inspected. It distinguishes Euclidean from other affine tori in inflection-count questions and discusses affine vertices. No exact theorem is inferred from its incomplete abstract hypotheses.
- Thorbergsson–Umehara (2002): https://doi.org/10.1017/S0027763000025435 and author preprint https://arxiv.org/abs/math/0008137 . Simple closed curves in RP2, not arbitrary projective surfaces.

## Approach 2: literal-scope zero-count example with nontrivial holonomy

**Proposition A.** There exists a compact oriented smooth affine flat torus and a smooth embedded essential closed curve with no inflections and no affine vertices. Consequently the sharp universal nonnegative lower bound for vertices, in this unrestricted class with the stated contact convention, is zero. The condition that inflections are isolated is vacuously satisfied.

Let Q={(x,y):x>0,y>0}, and let the commuting affine transformations be
A(x,y)=(e x,e^3 y), B(x,y)=(x,e y).
In logarithmic coordinates u=log x, v=log y these are translations by (1,3) and (0,1). They generate a lattice, so Q/<A,B> is a compact oriented smooth torus, with the torsion-free flat connection descended from the ordinary affine plane. It is projectively flat. For example, the translation-invariant conformal structure in (u,v) supplies a Riemann surface structure.

The lift c(t)=(e^t,e^{3t}) satisfies c(t+1)=A c(t). In log coordinates it is t -> (t,3t). If two parameters differ by a lattice vector, their difference is an integer, so it descends to an embedded essential circle. Its affine determinant det(c',c'')=6e^{4t} never vanishes.

Locally its graph is y=x^3. The exact vertex numerator in Approach 3 is N=8640, so it has no sextactic point. All conclusions are local and unchanged on affine-chart overlap. This torus is not claimed geodesically complete or equiaffine: det A=e^4, det B=e, so no parallel area form descends. These are explicit limitations of this example, not claims of necessity.

Alternative contact-only check: restricting the six conic monomials 1,x,y,x²,xy,y² to y=x³ gives 1,x,x³,x²,x⁴,x⁶. Their Wronskian of derivative orders 0 through 5 is a nonzero constant times x (the exponents are distinct and sum to 16). Thus no nonzero conic can vanish to order six at any x>0. At a noninflection, the usual osculating conic exists, so no vertex exists. This check avoids relying on an affine-curvature normalization.

A closed straight line on a Euclidean flat torus would instead have every point inflectional and would violate the isolated-inflection condition. It is therefore not used as the counterexample.

## Approach 3: local contact equation, with guards

For a graph y=f(x) at q=f'' != 0, affine curvature is
k=(3 q q''-5(q')²)/(9 |q|^(8/3)),
up to the conventional harmless choice of orientation. Direct differentiation shows k'=0 iff
N=9q²q'''-45q q'q''+40(q')³=0.
Here prime denotes x derivative; change to affine arclength multiplies the derivative by a nowhere-zero factor. The formula is used only on q != 0; evaluating N at an inflection does not define a vertex.

For a self-contained derivation of the contact criterion, translate the point to (0,0), subtract its tangent, and write f=a2 x²+a3 x³+a4 x⁴+a5 x⁵+O(x⁶), a2 != 0. Normalize the conic as y+A x²+Bxy+C y²=0. Killing terms x²,x³,x⁴ gives A=-a2, B=-a3/a2, C=a3²/a2³-a4/a2². The x⁵ coefficient is a5-3a3a4/a2+2a3³/a2². Thus contact at least six is equivalent to a2²a5-3a2a3a4+2a3³=0, exactly N=0 after substituting Taylor factorials. The conic is nonsingular: its homogeneous symmetric matrix has determinant a2/4 != 0. This verifies the convention directly.

For f=x^a on x>0,
N=2 a³(a-1)³(a-2)(a+1)(2a-1) x^(3a-9).
Guard a != 0,1 for noninflectionality. Exceptional exponents -1,1/2,2 give conics, with every point sextactic; they must not be counted as having finitely many isolated vertices. Exponent 3 gives N=8640.

## Approach 4: a sharp vertex–inflection inequality for periodic graphs, including degenerate isolated inflections

**Lemma.** Let f be smooth on a neighborhood of [a,b], with q=f'' nonzero on (a,b) and zero at a,b. Then the open graph arc has at least one sextactic point. No finite-order assumption is required at either zero.

Proof. Put h=|q|^(-2/3)>0 on (a,b). Then h tends to positive infinity at both endpoints, and k=-h''/2. On either end, h'' is unbounded above. Indeed, if h'' <= M on an end interval, Taylor's formula with integral remainder, based at any fixed interior point, bounds h above throughout that finite interval, contradicting h -> infinity. Choose a<x1<x0<x2<b with h''(x1),h''(x2)>h''(x0). The continuous h'' has a minimum on [x1,x2], necessarily at an interior point. Smoothness gives h'''=0 there, hence k'=0 and N=0. This is a noninflection by hypothesis. QED.

**Proposition B.** On the ordinary translation torus R²/(2pi Z x Z), consider c(t)=(t,f(t)) for a smooth 2pi-periodic f. If its inflections are isolated and their number is I, its number V of distinct noninflectional sextactic points satisfies V >= I. Infinite V is permitted. The bound is sharp for every positive even I.

Proof. The inflections are the zeros of the periodic continuous f''. An isolated closed subset of a compact circle is finite. There are at least two zeros unless f'' is identically zero, which is excluded by isolation. Apply the lemma to each cyclic interval between successive zeros, using the graph lift also across the period seam. Their interiors are disjoint, yielding at least I distinct vertices. For f(t)=epsilon sin(nt), n a positive integer and epsilon != 0,
N=-epsilon³ n^9 cos(nt)(36 sin²(nt)+40 cos²(nt)).
The inflections are sin(nt)=0 and the vertices are cos(nt)=0, each giving 2n distinct points. The two sets are disjoint, and every zero is simple. The curve is embedded because its first torus coordinate parametrizes the base circle once. QED.

This is a theorem for periodic graphs on a translation torus, NOT a theorem for arbitrary closed curves or for projective holonomy. It handles isolated infinitely flat zeros as well as nondegenerate ones. The argument requires a single graph coordinate over every inter-inflection arc; there is no claim such coordinates exist globally in the original question.

## Approach 5: sharp projective-plane results and limits of index arguments

Thorbergsson–Umehara's verified projective-plane results require smooth regular simple closed curves. Their lower bounds include at least three sextactics for non-nullhomotopic curves, six for nullhomotopic strictly convex curves, three for nonconvex curves, and two for convex curves; the last two classes use their precise definitions of convexity. Their combined bound for nullhomotopic curves is at least four inflections plus sextactics. Those results must be used with their stated definitions and scope, not transported to the affine torus without a global developed closed simple curve in RP2.

The developing map of a closed curve on an affine/projective surface need not be periodic: it closes only up to holonomy. Proposition A demonstrates the obstruction concretely. An extrema-of-curvature argument on a closed parameter circle also fails because curvature can transform by a nontrivial scale under holonomy. No universal V-I identity has been proved here or supported by the inspected literature. The rigorous results are instead (i) the zero lower bound in the unrestricted affine-torus subclass, (ii) the sharp inequality V>=I for translation-torus periodic graphs, and (iii) the cited, differently scoped projective-plane inequalities.

## Status and remaining question

Substantive partial progress, not a resolution of every possible intended version of item 4(b). The broadest literal positive-lower-bound hope fails under the explicit contact convention. A general relation with isolated inflections on arbitrary projectively flat surfaces remains unestablished. Resolve intended compatibility, equiaffinity/completeness, global convexity, and vertex conventions before any acceptance claim. Sasaki's full paper remains an uninspected source, not a source-access denial and not a proof gap in the authored propositions above.

## Strengthening A: complex-compatible logarithmic spiral (independent reviewer construction)

The zero-count example can also preserve a complex structure. Let M=C*/<z -> e^(1+i) z>. The exponential covering identifies M with C/<1+i,2pi i>, a compact complex torus. The ordinary flat real connection on C* descends because multiplication by e^(1+i) is real linear; it preserves the ordinary complex structure. The curve c(t)=[e^((1+i)t)], t mod 1, is embedded: equality of two points implies (1+i)(t-s-k)=2pi i m, whose real part forces t-s=k and then m=0.

The real-plane lift r(t)=(e^t cos t,e^t sin t) has det(r',r'')=2e^(2t)>0. Restricting a complexified real conic to this lift gives a linear combination of exponentials with distinct exponents 0,1+i,1-i,2,2+2i,2-2i. The transformation from real conic monomials to these complex exponential monomials is invertible. The order-0-through-5 evaluation matrix has nonzero Vandermonde determinant times a nonzero exponential. Therefore no nonzero conic has contact order six. This proves I=V=0 without the complex-compatibility caveat in the quadrant construction. It remains incomplete and does not carry a descended parallel area form for this connection; no claim about complete/equiaffine cases follows.

## Same-surface count obstruction: finite strictly convex ovals

**Proposition C.** In an arbitrarily small affine coordinate disk, for each integer n>=3 there exists a smooth strictly convex embedded oval with I=0 and exactly V=2n. Hence even on one fixed affine torus, V is not determined by I alone. Moreover V-I is not determined by ambient topology and curve homotopy class alone: take n=3 and n=4 contractible ovals on that same torus.

Proof. Let p(theta)=1+epsilon cos(n theta), n>=3, and let N=(cos theta,sin theta), T=(-sin theta,cos theta). Define r=pN+p'T. Then r'=rho T, where rho=p+p''=1+(1-n²)epsilon cos(n theta). For |epsilon|<1/(n²-1), rho>0. This is an embedded strictly convex oval: for any fixed direction N(theta0), r(theta) dot N(theta0) has derivative rho sin(theta0-theta), hence a unique maximum at theta0. In particular distinct parameters cannot give the same point (the supporting maximum is unique). Its determinant det(r',r'')=rho²>0.

Using ds=rho^(2/3)dtheta gives affine curvature
k=rho^(-4/3) -(1/3)rho''rho^(-7/3)+(4/9)(rho')²rho^(-10/3).
Consequently, as epsilon -> 0,
(1/epsilon) dk/dtheta -> [n(n²-1)(n²-4)/3] sin(n theta)
in C1 on the parameter circle. The coefficient is positive for n>=3. The limiting function has precisely 2n simple zeros. Uniform C1 convergence ensures that, for every sufficiently small nonzero epsilon, each zero has exactly one nearby zero (strict derivative sign on small disjoint neighborhoods), while the compact complement has none. The zeros of dk/dtheta are exactly the noninflectional sextactics, so V=2n. A translation and sufficiently small positive homothety put the oval into any chosen affine coordinate disk without changing either count. QED.

This disproves only identities determined by the stated topological/count data. It does not disprove general inequalities, signed or multiplicity-weighted index formulas, formulas including additional data, or holonomy-dependent relations.

## Final five-approach disposition

1. Source recovery: completed; original scope underspecified, historical general resolution not verified.
2. Holonomy counterexamples: accepted scoped constructions; universal positive lower bound is impossible under the stated sextactic interpretation without further restrictions.
3. Local differential/contact calculation: accepted exact derivation; used only away from inflections.
4. Isolated-inflection relation: accepted sharp periodic-graph theorem, not generalized to arbitrary projective surfaces.
5. Plane results and index/count tests: primary special-case bounds retained with scope; accepted exact-count ovals rule out unweighted count identities determined solely by the indicated topology/homotopy/count data.

Final disposition: scoped results accepted after independent adversarial review; general historical question unresolved/underspecified in this research. No novelty asserted. Symbolic checks are sanity checks of algebraic identities and are not presented as proofs of the global geometric statements. The authored proofs supply those statements under their explicit hypotheses.
