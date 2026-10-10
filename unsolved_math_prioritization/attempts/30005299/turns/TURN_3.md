# Substantive turn 3: an intrinsic characterization of the smooth locus

2026-10-01 06:02–06:05 UTC. Status: complete candidate theorem for **smooth complex quartics only**, unreviewed; the original singular/nonreduced target remains unresolved. Estimated full-target completion: 55%. No novelty assertion. Classical Steinerian/polar-involution geometry and the determinantal–Ulrich correspondence are credited below.

Write H=O_X(1) for the given projective embedding of a smooth complex quartic X. All statements concern this polarization, not only the abstract K3 surface.

## Theorem

The following are equivalent:

1. X is the Weddle quartic of four independent quadratic forms in the given P^3.
2. X admits a fixed-point-free involution sigma such that L=sigma^*H is an H-Ulrich line bundle.
3. X admits a fixed-point-free involution sigma such that H·sigma^*H=6 and the divisor class 2H-sigma^*H is not effective.

Here an H-Ulrich line bundle means that all cohomology of L(-H) and L(-2H) vanishes. Equivalently its pushforward i_*L has the linear resolution

    0 -> O_P3(-1)^4 --M--> O_P3^4 -> i_*L -> 0.

This equivalence is a standard published input: Beauville, *An introduction to Ulrich bundles*, Propositions 2.1–2.2, https://arxiv.org/abs/1610.02771 and https://math.univ-cotedazur.fr/u/beauvill/pubs/UlrichIntro.pdf . It is not a new theorem claimed here.

## Proof that (1) implies (2)

Use q_j(x)=x^T A_j x/2 with A_j symmetric, and M(x)=[A_0x ... A_3x]. Since X={det M=0} is smooth, M(x) has rank exactly three at every point of X: corank at least two would make all cofactors and hence all first partials of its determinant vanish. Its cokernel is therefore a line bundle L on X, with the displayed linear resolution, so L is Ulrich.

For x in X define sigma(x) to be the unique projective vector y with M(x)^T y=0. This is a regular morphism because the kernel has constant rank one on X. The equations are y^T A_j x=0. Symmetry gives x^T A_j y=0, so y lies in X and sigma(y)=x. Thus sigma is an involution.

It has no fixed point. First, any common base point p of the four q_j is singular on X. Indeed p^T M(p)=0. In corank at least two this is immediate. In rank three write adj(M(p))=r p^T up to nonzero scalar, where M(p)r=0. The derivative of det M in direction z is then, up to that scalar,

    p^T M(z) r = z^T M(p) r = 0,

where symmetry of each A_j gives the middle equality. Thus p is singular, contradicting smoothness. A fixed point sigma(p)=p would be exactly such a common base point because p^T A_j p=0 for every j. Hence none exists.

The quotient C^4 -> L_x is evaluated by the row y^T. Consequently the morphism defined by the complete linear system |L| is exactly x -> sigma(x) followed by the given embedding X -> P^3. It is complete because the resolution gives h^0(L)=4. It follows that L=sigma^*H, as required.

## Proof that (2) implies (1)

Choose a basis s_0,...,s_3 of H^0(H). Use sigma^*s_0,...,sigma^*s_3 as the basis of H^0(L). The evaluation map of L gives its linear resolution. After twisting that resolution by O_P3(1), taking cohomology shows that the multiplication map

    mu: H^0(H) tensor H^0(L) -> H^0(H tensor L)

is surjective, its kernel K has dimension four, h^0(H tensor L)=12, and H^i(H tensor L)=0 for i>0. The four columns of its presentation matrix supply a basis of K. In coordinates x,y these are the four bilinear equations of the graph x -> sigma(x), namely y^T M(x)=0.

The canonical lift of sigma to H tensor sigma^*H exchanges its two factors. On H^0(H) tensor H^0(L), after the chosen identification, it acts by exchanging x and y. It preserves K, and mu is equivariant.

**The trace step is essential.** Since sigma is fixed-point-free, the holomorphic Lefschetz formula for the line bundle H tensor L gives alternating cohomological trace zero. Higher cohomology vanishes as just proved, so the trace on its 12-dimensional space of sections is zero. Its plus and minus eigenspaces therefore each have dimension six. This is the standard fixed-point-free case of the Atiyah–Bott holomorphic Lefschetz theorem, not a new result. Equivalently one may descend the canonically linearized line bundle to the etale double quotient: its two eigensheaves differ by the nontrivial torsion line bundle, hence have equal Euler characteristics by Riemann–Roch; their higher cohomology vanishes, giving the same dimensions.

On the 16-dimensional tensor product, the plus and minus eigenspaces have dimensions ten and six. Equivariant surjectivity of mu, and semisimplicity of an involution over C, therefore force

    dim K_plus=4,    dim K_minus=0.

Thus every bilinear relation in K is symmetric. Write its four basis elements as y^T A_j x with A_j symmetric. In these bases the presentation matrix has columns A_j x. Its determinant is a nonzero scalar multiple of the equation of X by the linear resolution. Therefore q_j=x^T A_j x/2 give the desired Weddle determinant. They are independent because a relation between q_j would give a constant relation between the columns of a matrix with nonzero determinant. This proves (1).

This implication does not assume that an arbitrary determinantal representation is symmetrizable: it selects the intrinsic Ulrich bundle sigma^*H and uses the involution to force symmetry of its entire bilinear relation space.

## Equivalence with the numerical/effectivity criterion (3)

The quartic is a K3 surface, so H^2=4, its canonical bundle is trivial, and chi(D)=2+D^2/2 for every divisor D. The Hilbert polynomial supplied by an Ulrich line bundle is 4 binomial(t+2,2)=2t^2+6t+4. Comparison with Riemann–Roch gives H·L=6 and L^2=4. Ulrich vanishing and Serre duality also give h^0(2H-L)=0. This proves (2) implies (3).

Conversely suppose (3), and set L=sigma^*H. Both H and L are ample, L^2=4 and H·L=6. D=L-H has square -4 and intersects the ample class H+L in zero. Since D is nontrivial, neither D nor -D is effective. Thus H^0(D)=H^2(D)=0, and chi(D)=0 forces H^1(D)=0.

The class L-2H also has square -4 and has H-degree -2, so it has no sections. Serre duality and the stipulated non-effectivity of 2H-L give H^2(L-2H)=0; Euler characteristic zero then gives H^1(L-2H)=0. Hence L is Ulrich. No unproved claim that the effectivity condition follows merely from the intersection number is used.

## Credit, scope and remaining gap

The polar involution on a smooth Steinerian quartic is classical. Modern primary accounts include Dolgachev–Kondo, *Enriques Surfaces II*, Chapter 7, especially Sections 7.2 and 7.4, https://sites.lsa.umich.edu/idolga/wp-content/uploads/sites/1334/2024/08/EnriquesTwo.pdf . The proof above spells out the smooth determinant-specific implications rather than importing a theorem restricted to six base points. Smooth Weddle quartics in fact have **no** base point in their defining web, as proved above, so the six-basepoint special-locus characterization cannot replace this argument.

The conclusion is intrinsic and necessary-and-sufficient for every smooth complex quartic in its given embedding. It is only a subcase of the source question. Singular surfaces can have base points, corank-two points and noninvertible cokernels; their polar correspondence can be rational or multivalued at the singular locus. Reducible and nonreduced determinant quartics also occur. Extending this criterion to them is not justified by specialization or by the smooth K3 argument. The full original target remains unresolved.
