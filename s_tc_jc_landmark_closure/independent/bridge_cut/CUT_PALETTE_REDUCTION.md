# Two-colour segment-word reduction

This note records the combinatorial reduction used by the one-active part of
the pointwise cut theorem.  It is independent of the Fourier calculations.

Consider a complete cycle or theta factor after the rigid support and at most
four additional actual labels have been retained.  Colour every selected port
by the side of the proposed split.  Each primitive directed core segment then
carries a binary word in path order; path-sink and incoming boundary ports are
fixed extra letters.  Both colours occur at least twice.

## Three-run obstruction

If one segment contains three consecutive monochromatic runs with colours
`c,d,c`, choose one actual port from each of those runs.  In every displayed
tree, the path between the two outer `c` attachment vertices contains the
attachment vertex of the middle `d` port.  Deleting the final incoming edge
of that core segment at a reticulation, when a switching does so, does not
alter this internal path order.

No displayed-tree edge realizes the colour split.  An edge on the segment
either separates the two outer `c` ports or keeps the middle `d` port with
them; a pendant edge isolates only one port; and an edge outside the segment
keeps all three together.  The pendant edge of the middle `d` port cannot
work because a second `d` port exists elsewhere.  Thus a three-run word is
already a direct all-switching obstruction and needs no Fourier census.

## Reduction to the finite palette

Otherwise every segment has at most two monochromatic runs.  Retain one
actual port from each nonempty run.  The word on every segment is then one of

```text
(), (0), (1), (0,1), (1,0).
```

This restriction preserves precisely which core segments are occupied and
retains every fixed path-sink or incoming boundary.  Hence it preserves the
minimum strong repair, simplicity, the primitive core, and standard-strong
validity.

If both colours still occur at least twice, this is a direct member of the
short palette.  If one colour has only one retained representative, all of
its original occurrences lay in the same monochromatic run.  Because the
original colouring was balanced, that run contains at least two actual
ports.  Retain a second adjacent actual port from the run.  This is exactly
the singleton-doubled case checked by `duplicate_singleton_colors` in
`verify_cut.py`.  A sole representative cannot be a fixed extra port, since
then the original colouring would also contain that colour only once.

Restriction of a displayed tree preserves every split displayed by that
tree.  Consequently, if an original colouring were displayed by every
switching, its direct or singleton-doubled palette restriction would also be
displayed by every switching.  The exact graph-to-switching compiler checks
the complete reduced palette and has no survivor.  Together with the
three-run obstruction, this proves exhaustiveness for arbitrary segment
words in the at-most-eight-port handoff.

`verify_palette_reduction.py` independently exhausts all 808,642 balanced
binary word distributions with four through eight active ports across the
five primitive arities and both root roles.  It verifies that every record
falls into exactly one of the two cases above, that segment occupancy is
unchanged, and that the historical `(1,0,1)` example is classified as a
three-run obstruction.  `verify_cut.py` reconstructs the rooted graphs and
displayed switchings for the resulting finite palette.  A further clean-room
implementation in `reviews/global_bridge/verify_palette_cleanroom.py`
transcribes only the five primitive arc templates and independently
implements rooted validity, fixed-mixed-graph strongness, switching, masks,
and split testing; its family-by-family counts agree and it also finds no
survivor.
