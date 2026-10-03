# Author turn 1: finite rooted models and a first deficit-gap construction

2026-10-03 UTC. Status: partial; original target not solved. Best-guess full-target completion: 10%, a subjective planning estimate rather than a probability.

## Finite-model route
`FINITE_MODELS.md` gives the complete rooted representation, the 2(c−1)-vertex bound, the 2(m−1)-vertex verification bound and minimal crossing-core restrictions. General finite equivalence is credited to Stacey–Weidl p3. The elementary refinements have explicit proofs; originality is unclaimed. The independent approach worker contributed to this author turn, not to the final independent audit. Its checker passed12 explicit examples,3 negative/validation controls and 315 random bounded-versus-full comparisons.

The finite decision procedure does not make the recent asymptotic theorem's enormous/unspecified residue practical. A small crossing core can use fewer than c colors, and no safe arbitrary-palette extension was found.

## Properly colored K5 blocks
Inside K_n, take b vertex-disjoint K5 blocks. In each block, label vertices0,...,4 and color ij by i+j modulo 5. Give different blocks disjoint five-color palettes; give every other core edge a globally fresh color. Use one common fresh spoke color and another fresh infinite-tail color. This uses c=binom(n,2)+2−5b colors.

For an induced subset of a block of size s=0,...,5, the deficit (number of edges minus number of colors) is respectively 0,0,0,0,1,5. For s=3 properness makes the triangle rainbow. For s=4 every one of the five matching colors remains; for s=5 there are10 edges and 5 colors. Thus a block's deficit loss relative to its full deficit 5 lies in{0,4,5}. A sum of such losses cannot equal6.

Consequently if b≥2, k≥max(7,5b−4) and n≥max(k+1,5b), this coloring avoids
m=binom(k,2)+8−5b.
For nonempty core subsets S of size t the full infinite palette has size 2+binom(t,2)−D(S). If t<k this is at most2+binom(k−1,2)<m. If t=k equality would require D=5b−6, whose deficit loss is6, impossible. If t>k the count is at least2+binom(k+1,2)−5b>m because k>6. Empty core yields just one color. Also c>m because n≥k+1 and k>6.

The explicit instance b=2,k=10,n=16 yields (c,m)=(112,43). `deficit_blocks.py` exhaustively verified all 65536 core subsets, saved their complete spectrum and a full labeled witness. Additional block checks cover32+1024+32768 subsets. The instance is outside the explicit baseline sufficient conditions read in Stacey–Weidl Theorem 2 and p16, but this is not proof it was absent from all prior literature.

## Outcome and exact gap
We have a rigorous construction family and finite verification tools, not all c>m≥3. The next route is to assemble richer deficit-gap gadgets, seeking coverage of the modular-diagonal residue. All literature results retain credit and no novelty claim is made.
