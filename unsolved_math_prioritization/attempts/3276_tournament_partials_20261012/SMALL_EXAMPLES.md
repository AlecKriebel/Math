# Small authored examples

These illustrative examples are mathematical constructions, not copies of a searched dataset. They clarify direction, color and relaxation boundaries.

## A transitive rainbow triple is permitted

Take arcs 0→1 in color 0, 1→2 in color 1, and 0→2 in color 2. The three colors are different, but the triangle is transitive. Vertex 0 reaches each other vertex directly; the two chosen paths have different colors. Thus requiring one fixed path color would change the target.

## A cyclic rainbow triple satisfies the other alternative

Take 0→1 in color 0, 1→2 in color 1, and 2→0 in color 2. No vertex reaches its predecessor monochromatically. The directed triangle is rainbow, so this is not a counterexample to the disjunction.

Add vertex 3 and all arcs i→3 in color 0 for i=0,1,2. Vertex 3 is an incoming universal sink. There is still no outgoing monochromatic universal source. Reversing all arcs makes vertex 3 an outgoing source. This distinguishes directionality rather than providing a counterexample, since the rainbow cycle remains.

## Multistep paths matter

In an all-color-0 directed triangle, every vertex reaches every other vertex by a monochromatic path of length at most two. A direct-edge-only test would miss the paths to predecessors.

## Relaxation survivors are not counterexamples

The word 012 survives the switch-reachability relaxation, as does 012012. The first already has a cyclic rainbow triangle; the second is among the actual-completion exclusions of the finite search. Every even strictly alternating binary word of length at least four survives this relaxation although the stronger source proposition rules it out as an obstruction cycle.

The odd binary word 01010 has one nonswitch and fails. The word 00011 has nonswitch positions {1,2,4}; in cyclic step-minus-two order its three gaps are 2,1,2. All are at most (5+1)/2=3, so it passes the relaxation. This establishes neither tournament completion nor target failure.

For every odd n=2k+1 at least seven, 000 followed by k−1 copies of 10 has nonswitch positions {0,1,2} and step-minus-two gaps k,k,1. It shows that three nonswitches are sharp for this relaxation alone.

## A canonical residual set

On vertices modulo seven, orient i→i+d for d=1,2,3 and give that arc color d−1. Each vertex has all three incoming and all three outgoing colors, so its residual set is all seven vertices. Its color-0 directed cycle already gives every vertex universal monochromatic reachability.

Add a new source and a new sink, coloring their arcs to and from the original vertices, and the source-to-sink arc, with color 0. Both new vertices are deficient and are deleted; the original seven-vertex stable set survives. This illustrates why the proof uses retention of witnesses for old vertices, not the false claim that every superset of a stable set is stable.

A singleton has empty residual set. An empty tournament may be used in the residual-set definition, but is outside the target's nonempty universe and has no claimed universal source.
