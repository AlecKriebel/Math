# Turn 5: the moduli parameter and the specialization obstruction

Attempt: turn the generic calculations into an answer about fibers over Q by identifying the moduli parameter and testing a smooth exceptional member.

Takei's 2014 thesis, Proposition 4.1.1, computes the Igusa--Clebsch invariants of this same quintic family after the parameter change t=2-4s. In his normalization they become

A=350, B=2500, C=295000-11250t^2, D=3125(t^2-4)^2.

This also agrees with the discriminant in Turn 1. These credited formulas yield a short exact moduli argument. For two fibers with weighted-projectively equal invariants, the nonzero constant A forces the weight-two scaling factor to be one. The weight-six invariant therefore agrees, and t'^2=t^2. Conversely C_t and C_{-t} are isomorphic over Q(i), by (x,y)->(-x,iy). Thus the coarse geometric moduli map is generically two-to-one, and its image has rational parameter t^2. It is a nonconstant curve inside the RM surface of discriminant five. This dimensional statement alone is not a claim that it is a Shimura subvariety or a complete description of every moduli-theoretic level structure.

The smooth fiber t=0 proves that generic images cannot be assigned uniformly to all rational parameters. Its defining polynomial is x(x^4-5x^2+5). Put alpha=sqrt((5+sqrt(5))/2) and beta=sqrt((5-sqrt(5))/2), choosing their real positive values. Since alpha beta=sqrt(5) and sqrt(5)=2alpha^2-5, every root 0,+/-alpha,+/-beta belongs to Q(alpha). The polynomial x^4-5x^2+5 is Eisenstein at 5, so this field has degree four and is the splitting field. The automorphism alpha->beta sends sqrt(5) to -sqrt(5), and hence beta to -alpha. It has order four. Therefore the root group, and by faithful action on hyperelliptic two-torsion the group Im(G_Q on J_0[2]), is C_4. This is strictly smaller than the generic arithmetic F_20. In this fiber [(0,0)-infinity] is a rational nonzero two-torsion point, in contrast to the generic fiber.

Outcome: the all-fibers shortcut fails for a proved reason. The generic local conclusions in Turns 1--4 remain valid, but do not compute any unspecified fiber's complete Tate image. Exact integral images at 2,3,5, cross-prime adelic compatibility, and a parameter-dependent classification of arithmetic fiber images remain unproved in this packet. The broad original problem is therefore unresolved here after five substantive mathematical approaches.

Citation: Luiz Kazuo Takei, *Arithmetic aspects of Triangle Groups*, Ph.D. thesis, McGill University, March 2014, Proposition 4.1.1, printed pp. 124--125; https://www.math.mcgill.ca/darmon/theses/takei/thesis.pdf .
