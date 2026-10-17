# Acceptance of the unrestricted deletion-monotonicity boundary

Reviewed statement: the Additional logical boundary section in
`pass5_devil/FIXED_POINT_AND_DEPTH_AUDIT.md`, SHA256
`96ddc663c7537b2f502d8996eb2552f590a7c9dcd0511111a7e09193176c10dc`.

Accepted. For the unrestricted announcement game, suppose a fixed finite
preloaded state B is k-move winning. From the same starting position with
fewer bombs, the Angel can run that policy while internally supplying the
missing fixed preload and processing every actual announcement normally.
The simulated play contains every actual lethal pair. A policy safe against
every adaptive continuation of the simulated game is therefore safe in the
real game. Translating the starting position gives empty-state k-move
survival. No legality of a preparation history for B is needed for this
monotonicity argument.

Thus unconditional W_k states for an unbounded set of k, even if accompanied
by W_(k+1) failure, imply empty-state survival at every finite horizon and
hence a full infinite winning strategy by the accepted compactness theorem.
The conclusion would already follow from W_k membership alone.

The unrestricted qualifier is essential. A statement only about bounded-lead
W_k^H with H smaller than k cannot automatically be interpreted as a statement
about all announcements affecting a k-move horizon. The reviewed statement
correctly specifies unrestricted W_k. Conditional carpet examples retaining
an empty-state W_k hypothesis do not incur an unproved positive conclusion.
