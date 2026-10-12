# Independent cubical reconstruction (sealed before historical comparison)

## Exact hypothesis and cell recipe

Only the raw ATTEMPT_1 construction is used here. The exact target is the free rank-three mapping torus with t a t^-1=a, t b t^-1=ab, t c t^-1=b c b. A finite NPC quotient suffices only after its fundamental group is identified with this exact group.

Use a one-vertex K with oriented x,y,b and oriented square cycles xyXY, bxBY. K has signed directions x±, y±, b±. For a boundary cycle h0 h1 h2 h3, the corner after hi contributes the pair (hi^-1, h(i+1)); this convention independently derives every link edge.

Use Q vertices A,B,C,D and oriented edges p:B→A (x), q:A→C (y), r:D→C (x), s:B→D (y), d:A→B (b), e:C→A (b). Its squares have edge cycles p q r^-1 s^-1 and d p e^-1 q^-1. Their vertex cycles are (B,A,C,D) and (A,B,A,C). In particular the second square has opposite corners identified at A; it is not an embedded square in Q. Its corner pairs at A are (b+,y+) and (x-,b-). The first square contributes (x-,y+) at A, connecting them to the claimed length-three path.

The involution exchanges x↔y and b↔b^-1. Its image of xyXY is yxYX (the reverse cycle); its image of bxBY is BybX (a cyclic rotation of the reverse cycle). It is therefore cubical on both K square cells, consistently with the edge map, and has square equal to identity.

For each Q vertex V, introduce the oriented vertical loop z_V from the j end to the lambda j end. For each oriented Q edge h:S→T with label ell, the product square has boundary ell z_T lambda(ell)^-1 z_S^-1. This yields the six explicit boundary cycles:

- p product: x z_A Y z_B^-1;
- q product: y z_C X z_A^-1;
- r product: x z_C Y z_D^-1;
- s product: y z_D X z_B^-1;
- d product: b z_B b z_A^-1;
- e product: b z_A b z_C^-1.

Attach one product cube for each Q square. Its four side faces are the corresponding four product squares, with orientation determined by the signed Q edge. Its bottom face is that Q square's j image and its top face is its lambda j image. Each restriction is a Euclidean face isometry to the designated K square or product square, and the restrictions agree along edges. The second cube repeats z_A at opposite vertical edges. Both cubes map their bottom and top to the same underlying K square. These global identifications must be retained, never simplified to embedded attaching maps.

## Independent link recipe and expected checks

For each K or product-square corner, derive the two oriented germs at its vertex from its actual boundary. Each product-cube corner contributes exactly the triangle consisting of the two horizontal Q-square germs at that corner, sent by j at the bottom or lambda j at the top, and z_V+ at the bottom or z_V- at the top. This is eight triangle incidences per cube, including both occurrences of V=A in the second cube.

Check endpoint closure in Q, all signed square corners, all six cube faces, consistency of horizontal corner-to-square mapping, injectivity of each Q vertex-link map, fullness of its image, simplicity of K and final links, and every clique against actual simplex incidences. Count link edges/triangles by incidences as well as distinct simplices, to detect duplicate edges/triangles that a set representation would otherwise hide. No edge joins two vertical directions. Thus any final-link clique can contain at most one vertical direction; fullness plus K flagness would then prove flagness, provided the actual corner data agree with this cone recipe.

## Local and global metric obligations

The quotient is constructed by face isometries of finitely many unit Euclidean cubes. Its nonembedded boundaries are permissible in the cubical CW quotient convention, just as a one-square torus is permissible. The link criterion must be applied to the actual direction-incidence complex; multiple edges, repeated triangles, or collapsed cube directions would be fatal to treating that link as a simple flag complex. Nonembeddedness cannot be dismissed by cell counts or presentation algebra.

A finite Euclidean cubical quotient has finitely many local shapes and is complete in its intrinsic length metric. A connected locally CAT(0) complete length space has CAT(0) universal cover under Cartan–Hadamard. The finite quotient and finite link incidences make the cover locally finite and its metric proper. Covering/deck-action theory then gives a free proper deck action and a compact quotient. A 3-dimensional uniform unit-cell structure gives no infinite small-cell accumulation. Global CAT(0) implies embedded cubes upstairs even though quotient boundaries identify corners/faces. Group identification must use the exact top relation z^-1(bx)z=b^-1y and the reversible substitution t=x, a=xy^-1, c=(zx)^-1; no nearby ab versus aba formula or finite-index/monodromy replacement is authorized.

## Planned meaningful negative controls

Delete the first Q square to break local fullness while preserving edge germs. Delete one product cube while keeping its side squares to create unfilled link triangles. Merge two vertical edges to test duplicate link incidences. Change r's x label to y to break square-cell compatibility. Change a Q endpoint to test nonclosed square boundaries. Each mutation must be rejected for its geometric defect, not merely by a changed cell count. Repeating signed derivations under orientation reversal should preserve the genuine link up to relabeling.

This document is the pre-historical reconstruction seal. No proof-search turns are added.
