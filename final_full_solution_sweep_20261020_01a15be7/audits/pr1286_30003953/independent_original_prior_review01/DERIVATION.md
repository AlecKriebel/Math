# Independent derivation and attempted falsification

## Exact success criterion

For each closed oriented surface S of genus at least2, construct a projective1-Anosov representation of its group into some PGL(d,R) with a rectifiable limit circle which is not a C1 embedded submanifold, hence not C1,alpha for any positive alpha. Dimension4 suffices for the original existence question. No full-PGL Zariski density, fixed dimension or higher-root condition is required. Regularity must concern the embedded image, not a chosen parametrization.

## Construct the group and check the correct gap

Use an oriented pants decomposition. Choose marked hyperbolic structures m1,m2 with all cuff lengths1 and zero twists for m1, and with one cuff c changed to length2 in m2. Hyperbolic pants and orientation-compatible gluing give both cocompact Fuchsian holonomies j1,j2 with the same marking. The chosen element gamma has lengths ell1=1, ell2=2, so the holonomies cannot be conjugate. Their boundary actions are conjugated by an increasing homeomorphism h of RP1.

For arbitrary determinant-one representatives A_i of j_i(delta), define rho(delta)=[A_1 tensor A_2] in PGL4. Sign changes and multiplication discrepancies are scalars, so no coherent SL2 lifts are needed. In tensor-product Euclidean norms, if the factor singular logarithms are plus/minus a1 and plus/minus a2, the four tensor logarithms are

    a1+a2, |a1-a2|, -|a1-a2|, -a1-a2.

The leading logarithmic gap is exactly2min(a1,a2). Cocompact orbit quasi-isometries give displacement2a_i(delta)>=c_i|delta|-C_i for every group element in ordinary word length. Thus the singular-value ratio is at most exp(max C_i) exp(-min(c_i)|delta|). This is precisely the published PSW projective-Anosov definition/criterion for a word-hyperbolic group. Translation length was used to select one cuff, not to supply this uniform bound; it cannot bound ordinary word length on arbitrary conjugates.

A block direct sum would instead have gap|a1-a2|, zero at equal factors. That representation is not interchangeable with the tensor. The phrase direct sum in the PSW introduction is followed by the target PSL2 x PSL2: it denotes the product pair, not the block-matrix realization into PGL4.

## Boundary and hyperplanes

The smooth Segre embedding F:RP1 x RP1 -> RP3 sends([u],[v]) to[u tensor v]. It is injective and immersive; compactness gives an embedding. The map xi(x)=F(x,h(x)) is continuous, injective and equivariant. For a nontrivial element, the largest-modulus tensor eigenvalue is simple and its line is the tensor of the attracting factor lines. Thus xi identifies the Anosov attracting lines on the dense set of attracting fixed points and is the boundary map.

Let omega be the standard alternating form on R2. B=omega tensor omega is symmetric, nondegenerate, signature(2,2), and preserved by determinant-one tensor factors. A rank-one line is B-null. For distinct x,y,

    B(u_x tensor v_h(x), u_y tensor v_h(y))
       =omega(u_x,u_y) omega(v_h(x),v_h(y)) !=0.

Hence eta(x)=xi(x)^{perp_B} gives the transverse equivariant hyperplane map. It is the attracting hyperplane for the dual action at a positive fixed point; the original action's repelling hyperplane is eta(delta-minus), not eta(delta-plus). No ambient semisimplicity or full-PGL density is inferred from this pairing.

## Finite length of the actual image

Give RP1 circumference pi and lift the increasing h to H with H(t+pi)=H(t)+pi. For an ordered partition over one period, each product-distance increment is at most the sum of the nonnegative angular increments. Their sums telescope to pi+pi. Thus Graph(h) is rectifiable with length at most2pi; h need not be Lipschitz in its original coordinate.

For unit representatives u,v and orthogonal derivatives u',v', the differential of F is u' tensor v + u tensor v'. Its squared norm is ||u'||^2+||v'||^2, since the cross term vanishes. Thus F is an isometric immersion for these product/round quotient metrics. Applying the chain rule to an arclength parametrization of the rectifiable graph shows length preservation; a local Lipschitz bound would already suffice for finiteness. Consequently the projective image has length at most2pi. All smooth metrics on compact RP3 are uniformly comparable.

In a local increasing affine chart, s=x+h(x), t=h(x)-x satisfy |Delta t|<=Delta s. The strictly increasing s coordinate makes the graph locally1-Lipschitz after rotation, without requiring that x itself be a regular parameter.

## Intrinsic obstruction to C1

Conjugate the factor actions so gamma's attracting/repelling points are0/infinity. The boundary conjugacy fixes them and satisfies

    h(lambda1 x)=lambda2 h(x),
    lambda_i=exp(-ell_i), 0<lambda2<lambda1<1.

Write r=ell2/ell1>1, so lambda2=lambda1^r. On the compact two-sided fundamental annulus1<=|u|<=lambda1^(-1), h is finite and continuous. Let M=max|h(u)|/|u|^r. Every sufficiently small x!=0 has x=lambda1^n u there. Equivariance gives |h(x)|<=M|x|^r, and h(x)/x tends to0 from both sides. This is a statement about all secants approaching(0,0), not just one geometric subsequence.

Suppose Graph(h) were a C1 embedded curve. Its tangent at(0,0) is horizontal by that secant limit. The global horizontal line distribution is preserved by every product group transformation, so the tangent is horizontal on the whole orbit of this point. The cocompact Fuchsian boundary action is minimal; that orbit is dense in the graph. Continuity of a C1 tangent-line field makes it horizontal everywhere. The second projection then has zero differential on the connected C1 curve, so is locally and globally constant, contradicting its surjectivity onto RP1.

If the projective image were C1, it would be C1 within its smooth Segre surface, and smooth local surface charts followed by F inverse would make the graph C1. Thus the contradiction concerns embedded-submanifold regularity in RP3. It cannot be evaded by reparametrizing the curve.

One fixed-point flatness estimate alone would not suffice: h(x)=x|x| has a C1 graph, tangent horizontal at0 but nonhorizontal at1. Minimality and continuous tangents are essential. Likewise a dense zero-derivative statement for a merely monotone map would not by itself imply constancy. The proof assumes a C1 embedded curve precisely when using tangent continuity.

## Boundary cases and prior-source relation

For identical/conjugate factors, the diagonal/projectively conjugate graph is smooth. The chosen unequal cuff lengths rule out that exception; with equal lengths the exponent test would only give r=1 and no decay. Reversing the strict length ordering changes the flat direction; factors can be exchanged, and the construction already chooses the required order.

The image preserves signature(2,2). That does not violate the question, and no result for all dimensions or all higher roots is claimed. In optional AdS terminology, choosing Q=-B makes pairings of distinct increasing graph lifts negative. The zero-diagonal Gram matrix of a distinct triple has negative determinant and trace zero, hence signature(2,1). Together with the established projective gap this matches the PSW convex-cocompact criterion. The chosen gamma has tensor eigenvalue-modulus logarithms plus/minus(ell1+ell2)/2 and plus/minus(ell2-ell1)/2, none zero; a timelike fixed line in the AdS-Fuchsian case would force a modulus-one eigenvalue. This also excludes that case. These extra checks are not needed for the direct non-C1 argument.

The published PSW introduction describes the same product-Fuchsian graph as Lipschitz and non-C1 except for conjugate factors. The independent tensor/Segre calculation here identifies its projective realization and verifies the exact1-Anosov condition needed by the original question. The older GM arXivv2 theorem gives C1 rigidity specifically for AdS quasi-Fuchsian groups under its definitions. It is not a theorem about every projective-Anosov representation, and it is not required by this explicit proof. Its typeset journal theorem numbering has not been inspected.

## Verdict and verification limits

No substantive mathematical gap was found in the pinned PR construction. It provides the complete literal existence answer in dimension4, by an established example, without a novelty claim. The independent rational diagnostics check finite singular-log identities, forms, transversality, monotone increments, metric differentials, scale models and source fingerprints. They do not prove cocompact quasi-isometries, arbitrary-group domination, minimality or the universal tangent argument. Those are the written deductions and cited standard background above. Historical checks were not reexecuted. AI assistance is extensive; no external human review or proof-assistant certification is claimed.
