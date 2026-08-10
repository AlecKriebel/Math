# Preserved failure: omitted target incoming boundary

Status: **INCOMPLETE UNIVERSE, QUARANTINED BEFORE ALGEBRA**

After correcting the relation action from the incoming-fixed subgroup to the
full boundary group `S_p`, the reviewer still required the target rooted
presentation's structural incoming boundary to be one of the `p` observed
boundaries.  The affected source hash was
`2ade3c25b95da412ee2d74ab43af6078088da8fcb6bd5230513ad5fee2d433fd`.

That condition is not preserved by an arbitrary selected support marginal.
A full target factor may be rooted through a boundary outside the selected
support.  In the selected Fourier tensor that structural incoming boundary
has character zero, while all `p` observed boundaries lie in outgoing roles.
The tensor still has exactly `p` observed boundary indices.

The corrected target grammar therefore has two nonroot provenance modes:

- `incoming_selected`: the structural incoming leaf is one observed boundary;
- `incoming_dummy`: the structural incoming leaf is restored as a distinct
  zero-character dummy and all observed boundaries occupy outgoing roles.

The incoming provenance is not a relation colour in either mode.  Certificates
and survivor counts are stratified by mode so that this repair cannot be
silently lost by canonical deduplication.
