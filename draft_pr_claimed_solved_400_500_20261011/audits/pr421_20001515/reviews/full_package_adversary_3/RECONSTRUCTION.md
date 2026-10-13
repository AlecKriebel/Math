# Independent reconstruction and global proof audit

This is independent of all root/peer gates and reports, but not author-blind: the candidate proof and preprint source were read before the criteria artifact, as disclosed in CRITERIA.md. The checks below take definitions from the proposed construction and independently derive consequences. No candidate checker was imported or read before this seal.

## Incidence mechanism

At each oriented square word w, corner i contributes the unordered pair (inverse of w[i-1], w[i]) at the initial vertex of w[i]. The implementation retains all eight Q corner occurrences before merging link simplices. Its second square has vertex cycle A,B,A,C; the two A contributions are d+/q+ and p-/e-. Together with the first square's p-/q+, these are three distinct edges. K's eight corner pairs are distinct and bipartite. Q images at A,B,C,D have respectively 4,3,3,2 vertices and 3,2,2,1 edges; comparing every potential edge with K establishes induced fullness. Lambda swaps x/y and reverses b; the square words map to yxYX and BybX, in their dihedral orbits, and the chosen isometries square to identity.

The genuine product has six edge cylinders and two cube cylinders; cube boundaries agree because both end maps are isometries on each domain square agreeing on its edges. Every product corner has two Q directions and one interval direction. There is no corner with two interval directions. For each of eight distinct signed interval germs, the link is exactly the cone on the appropriate full Q link. The code assembles 32 edges and 16 triangles as occurrence lists, then checks uniqueness. The 14-vertex graph has exactly those 16 three-cliques and no four-clique. Therefore the actual link is simplicial and flag, not merely a clique-count surrogate. Deleting one A triangle breaks flagness; duplicating a corner breaks incidence uniqueness.

## Reversible algebra

The six side-square words are x z_A Y Z_B, y z_C X Z_A, x z_C Y Z_D, y z_D X Z_B, b z_B b Z_A, b z_A b Z_C. The p,q,s equations uniquely solve z_B=x z_A Y, z_C=Y z_A x, z_D=Y x z_A Y x. Eliminating these is reversible; adding the definitions reverses the operation. The r equation follows by commuting x and y. Substitution into d gives z^-1 (bx)z=By. Substitution into e gives z^-1(yb)z=xB. Base bxB=y implies yb=bx and By=xB, so these are identical equations, not two distinct HNN restrictions. The three-dimensional cells add no pi_1 relations.

Thus P=<x,y,b,z | xy=yx, bxB=y, Z bx z=By>. Introduce a=xy^-1,t=x,c=(zx)^-1. Inverse substitutions are x=t,y=a^-1t,z=c^-1t^-1. Substitution into xy=yx gives at=ta. The base equation becomes btb^-1=a^-1t; multiplying gives tbt^-1=ab, with exact converse. The HNN equation is Z(bx)z=x(Bx)X. Multiplication by z and x gives (zx)(Bx)(zx)^-1=bx; hence c^-1(Bt)c=bt. Left multiply by c, then by b, and right multiply by t^-1 to obtain tct^-1=bcb. These multiplications reverse, so this is an isomorphism to the full target presentation, not one-way relator evidence.

As a separate falsification check, the script implements exact free-word/height multiplication (u,n)(v,m)=(u phi^n(v),n+m) in F(a,b,c) semidirect Z and independently verifies the inverse automorphism, the three HNN relators, and all six side squares. The inverse automorphism is a->a,b->Ab,c->BacBa. Wrong HNN conjugation and changing the final b to B give nonidentity normal forms. These are controls, not substitutes for the reversible Tietze argument.

## Global metric and action

The quotient is a finite cube complex in the face-identification convention. Its cells are unit Euclidean cubes with genuine face isometries; the only vertex link is the actual flag simplicial link just reconstructed. Leary v3 Theorem C.9 applies explicitly to general cube complexes and arbitrary vertex links, so the universal cover with lifted metric is CAT(0). Theorem C.4 proves that a CAT(0) cube complex is cubical with embedded cubes and single-face intersections; it is not assumed that a nonembedded quotient automatically has a strict cover. The cover inherits dimension three and finite links. Its metric is complete: finite-dimensional cubical complexes have no infinite ascending chain of cubes, meeting Leary Theorem A.6 after strictness. Finite links ensure local compactness, so the complete geodesic CAT(0) space is proper by metric Hopf-Rinow.

The full deck group acts freely and cubically. Properness of the action has a direct compactness argument: if infinitely many distinct h_i translate a compact C to meet itself, choose p_i,q_i in C with h_i p_i=q_i and convergent subsequences. Covering neighborhoods at the limits identify one sheet for p_i and one sheet for q_i for large i; a deck transformation between fixed sheets is unique. This contradicts distinct h_i. The quotient is finite and hence compact, proving cocompactness. P is the full pi_1, already reversibly identified with G. No finite-index restriction, virtual specialness, minimality or historical firstness follows.

## Theoretical gaps

No remaining gap was found in this explicit-model proof. Finite computations certify only its finite incidence/algebra checks; the global assertions are deductions from the cited primary cubical theorems and the covering-space argument. The older-tools route and source/publication claims are still to be audited after this seal.
