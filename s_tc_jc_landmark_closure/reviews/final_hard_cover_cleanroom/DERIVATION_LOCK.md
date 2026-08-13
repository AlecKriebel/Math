# Clean-room derivation lock

Status: active clean-room design, 2026-08-10.

This review may read only the frozen primitive/support encodings as
mathematical inputs.  Primary hard-cover JSON streams are comparison objects;
no primary Python module is imported or copied.

The independent construction is graph first:

1. Strip the labelled minimum-repair subdivision vertices from each permitted
   support presentation to recover its rooted directed cycle/theta skeleton.
2. Rebuild the selected boundary ports directly on that skeleton.  The n=3
   stratum has four selected boundaries; the theta-2 minimum-support n=4
   stratum has five and is never normalized down to n=3.  The structural
   incoming and reticulation-sink ports may be selected or hidden; every
   unoccupied segment of one minimum strong repair receives a hidden repair
   port.
3. Quotient only by an independently implemented coloured-graph canonical
   form.  After anchoring the source labels, enumerate all 24 target boundary
   permutations.  No incoming boundary is fixed across the relation.
4. Bind restoration to one immutable root relation.  Hidden incoming,
   repair, and sink ports are restored in a deterministic order.  At each
   step the same physical label is inserted in every source segment position,
   while each path record retains its root and parent binding.
5. Enumerate displayed trees from the rooted arcs, derive descendant masks,
   canonicalize every selected split as `min(S,S^c)` on the zero-sum Fourier
   slice, zip identical switching rows, and construct JC Fourier polynomials
   from those masks.  Quartet invariants are derived independently from the
   15 JC character orbits and arm-multihomogeneous nullspaces.  Primary
   invariant metadata supplies only the claimed quartet/index and arm degree
   to be audited; no primary coefficient body or classification flag is used
   to establish separation.
6. A source-nonzero/target-zero pullback is a generic polynomial separator.
   A source-zero/target-nonzero pullback is accepted only with an exact strict
   open-cube sign proof.  Everything else remains unresolved.

Primary commitments are comparison inputs only.  Any disagreement is
preserved, not patched to the expected bytes.  The active n=4 gate is locked
to its exact-rooted-graph schema and independently replays all 132 roots and
2,106 states.  The n=3 stream is a separate gate and cannot inherit the n=4
verdict.
