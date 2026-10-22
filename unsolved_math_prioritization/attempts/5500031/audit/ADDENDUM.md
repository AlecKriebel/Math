# Non-destructive correction and clarifications

The frozen author package remains byte-for-byte unchanged. This addendum accompanies it.

## 1. Related-catalog completeness

The author's SOURCES.md identifies adjacent polygonal-room target 3900009. The complete catalog also contains **3100011**, a polygonal-room question about the existence of an illuminating source position. A safer replacement for the adjacent-target passage is:

> The complete catalog includes adjacent polygonal-room illumination entries 3900009 and 3100011. They concern illumination inside a room with connected boundary walls and differ from escape from pairwise-disjoint open segment mirrors. Neither is resolved by this note. No new proof-search attempt or current-status determination was made for either adjacent target.

This is a completeness correction, not a change to any segment-mirror theorem or the unsolved 5/5 disposition. Public source links: [Geometry Junkyard open problems](https://ics.uci.edu/~eppstein/junkyard/open.html) and [Cooper's combinatorial problems](https://people.math.sc.edu/cooper/combprob.html). These links identify source provenance; this audit does not certify those adjacent problems' current status.

## 2. Nonunit numerical clock

Both verifiers use exact rational velocity vectors without normalizing their speed. Their `elapsed` value is therefore an affine flight parameter. For the explicit velocity (2,1), the collision parameters are 1/2 and 3/2; unit-speed physical times are sqrt(5)/2 and 3sqrt(5)/2. The verifier's radial polynomial correctly includes the squared speed. The mathematical theorem uses unit speed, so this is only a reporting clarification.

## 3. Endpoint-sensitive test classification

In the author's 280 concurrent controls, the acute-wedge rays from (10,0) with directions (5,1) and (5,-1) pass through omitted endpoints and escape without reflection. They test the explicitly stated transparent-endpoint extension, not the regular-ray theorem alone. The independent 840-run suite contains the corresponding six cases under three rigid coordinate transforms and flags them as singular. The other 834 are regular in that suite. The author package describes concurrent examples without claiming that every tested ray is regular; no theorem correction is needed.

The four-mirror certificate at slope 1/2 is regular. The entire open slope interval in the proof is regular. Its boundary slopes pass through endpoints, which explains why they were excluded from the authored regular interval even though transparent continuation also escapes.

## Status

No mathematical correction required for the scoped claims. Unrestricted problem unsolved; approach count remains 5/5. The author's historical “independent review pending” fields describe its freeze-time state and are superseded only by the separate independent audit verdict, not silently rewritten.
