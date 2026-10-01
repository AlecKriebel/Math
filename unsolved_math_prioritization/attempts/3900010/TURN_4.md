# Author turn4: an odd periodic lattice tiling and the missing boundary repair

**A positive periodic construction, not a positive rectangular witness.** 2026-10-01.

## 1. The exact lattice fundamental domain

Define the homomorphism

    chi:Z² -> Z/14Z,   chi(x,y)=x+4y mod14,
    L=ker chi.

The14 cells of P are a complete set of representatives for Z²/L. In row y=0 their residues are0,1,2,3; in row y=1 they are4,5,6,7; in row y=2 they are8,9,10,11,12,13. Hence each lattice cell z has a unique decomposition z=p+l with p∈P and l∈L: choose p by chi(z), then l=z-p. This proves that the translates P+L tile the whole plane without overlaps of cell interiors.

One basis of L is(14,0),(-4,1), with determinant14. Rectangular periods include(14,0) and(0,7). Passing to the14×7 torus yields exactly7 tiles. Explicit representatives for their translations are

    (0,0),(10,1),(6,2),(2,3),(12,4),(8,5),(4,6).

Each projected tile still has14 distinct cells, and the seven sets partition the98 torus cells. This is an exact odd tiling of a flat torus, using translations only. The certificate and standalone checker verify every cell and identify the wrapped placements.

## 2. Why this does not answer the source question

Four of the seven displayed placements cross a chosen rectangle seam. After taking their coordinates modulo14 or7, they become disconnected pieces in the Euclidean rectangle. They are congruent tiles on the torus, not congruent copies of P contained in a planar14×7 rectangle. Allowing such wrapping would change the problem.

In fact the planar14×7 rectangle is already excluded by turn2: its even side is not divisible by6. A periodic tiling need not preserve a coloring that fails to descend through its periods, so this is no contradiction.

For a stronger control, use the rectangular periods(42,0),(0,7). The same lattice tiling gives21 tiles on a42×7 torus. Its area, odd count and even-side character restriction all satisfy turn2. Yet the planar rectangle is excluded by the complete width7 graph in turn3. Thus even the combination of a positive odd torus tiling with every complex-character condition proved here is insufficient for a positive rectangular tiling.

More generally,14a×7b rectangular periods with a,b odd give7ab odd torus tiles. This infinite family is not an infinite family of positive planar rectangle solutions.

## 3. A precise obstruction to the simplest boundary-cut proposal

The particular plane lattice tiling uses only untranslated orientation P (plus translations). No finite rectangle can be tiled using only this orientation. To see this, align P with row lengths4,4,6 from bottom to top. Every tile meeting the bottom rectangle side must have its lowest row there. Its contribution to the bottom side has length4, while its top row protrudes two units farther to the right. The rightmost bottom-side tile ends at the rectangle's right side along its bottom row, so its top row would extend two units outside the rectangle. Contradiction.

This is a proof for the **translation-only fixed-orientation subclass**, not for the full D4 problem. It shows that simply selecting a finite rectangular union of whole tiles from this lattice tiling cannot work. Genuine boundary repair must change some tile orientations or alter the lattice pattern; wrapping or cutting tiles apart is not an allowed repair.

Similarly, rectangular juxtaposition of known even tilings cannot create an odd seed. If two tiled rectangles with a common side are joined, their tile counts add. Rotating/reflection or making an array preserves evenness. By induction every rectangle built by such operations from even seeds has even tile count. Thus the known396-tile rectangle, by itself and these operations, cannot supply the missing odd construction. This is a limitation of that closure route, not of every geometric construction.

## 4. Attempted extension and exact remaining gap

The lattice pattern suggests a finite boundary-correction search: retain a periodic interior and replace its wrapped seam pieces by complete rotated/reflected tiles, while checking all overlaps and the resulting odd total. This turn has not found such a correction. The torus construction only identifies an interior pattern and makes clear what must be repaired. It cannot be promoted by ignoring the boundary.

The final author attempt will test a separate finite-field coloring/overlap relaxation against admissible odd rectangles. Any modular or signed witness will be kept distinct from a positive exact cover, and any bounded obstruction will stay bounded.

Substantive author turns:4/5. Estimated completion35%. Original unresolved; no novelty claim.
