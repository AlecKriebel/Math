# Attempt 4: signed interval-orbit dimensions and compressed reconstruction

Date: 20 October 2026. This attempt closes the apparent exponential jump/spike-variable obstruction using a dimension cutoff, rather than assuming all orbits have original-breakpoint anchors.

## Signed orbit lemma

Consider variables z_i, 0≤i<N, with polynomially many interval-pairing equations z_{g(i)}=epsilon z_i, epsilon in {+1,−1}, and forced-zero integer ranges. Each g is an order-preserving or order-reversing bijection between integer intervals. The geometric orientation of g is independent of epsilon.

Form an underlying interval-pairing graph on N indices. Form its two-sheet lift on (i,+),(i,−), with edges

(i,sigma) ~ (g(i),epsilon sigma).

The two sheets are consecutive integer blocks, so every lifted edge family is again an interval pairing. Add sheet-flip pairings (i,+)~(i,−) on all forced-zero ranges. Such flips do not change the underlying graph.

For each underlying connected component:

- if no negative cycle or forced zero exists, the lift has two components, and the signed equations have one free scalar;
- otherwise the lift has one component, and the signed equations force every variable to zero.

Therefore the solution-space dimension is exactly

D = orbit_count(lift) − orbit_count(underlying).

Basic AHT computes both counts in polynomial bit time. Counts may be exponentially large, but their binary lengths are O(log N).

## Why exponentially many orbits need not be listed

Let K be the number of residual homogeneous equations after the local slope/jump/spike relations are imposed. If the total free dimension D_s+D_J+D_P exceeds K, a nonzero solution necessarily remains. For the extremality decision this already proves nonextremality. It is unnecessary to construct or enumerate all free variables.

Otherwise all three free dimensions total at most K, which is polynomial in the sparse input size. Their representatives can be found without traversing orbits.

## Polynomial representative extraction

Maintain the original forced-zero set plus singleton flips at previously selected representatives. Let its current dimension be d>0. Temporarily add sheet flips on the prefix [0,t] and recompute the dimension. The dimension decreases precisely by the number of currently free signed components meeting that prefix.

Binary-search the least t causing a decrease. Adding the single vertex t can affect only one component, so this least t lies in a new free component and the drop is exactly one. Record t, permanently add its singleton flip to the SEARCH graph, and repeat. There are at most K iterations and O(K log N) AHT calls, with only polynomially many new pairings.

IMPORTANT: the graph modified for representative extraction is not the graph used for coefficient reconstruction. Those added singleton flips deliberately kill the selected components. Reconstruct on the ORIGINAL signed graph with only its original forced zeros.

## Weighted reconstruction

Give the lifted positive representative of each free component its own marker coordinate. Add indicator coordinates for each required prefix and singleton on each sheet. These weights are nonnegative and piecewise constant on a polynomial-size interval partition. The original AHT weighted algorithm applies directly.

For the lifted component containing representative (r,+), the difference between its positive-sheet and negative-sheet prefix counts is the signed sum of the basis variable over that prefix. Singleton versions give the basis value at a required coordinate. A marker occurs at one node only, so its component is unambiguously identified in AHT's output and has multiplicity one. Exponentially many unmarked forced-zero orbit groups can be ignored without expansion.

Using separate nonnegative sheet indicators avoids needing any extension of AHT to signed input weights. All output coefficients have magnitude at most N and hence O(log N) bits.

## Application to Attempt 3

Apply this lemma independently to slope, jump, and spike families. Slopes and jumps use character +1 even for geometrically reversing pairings; spikes use character −1 on reflection edges. The required reconstruction queries include all projected coarse arrangement zero vertices, not only original input breakpoints, as well as f, 0, full sums, and adjacent prefixes needed for one-sided traces.

The finitely many reconstructed endpoint-sector, f-normalization, and periodic-compatibility equations give an ordinary rational matrix with at most K variables. Exact rank is computable in polynomial bit time.

## Reproducibility and independent checks

`structural/SIGNED_ORBIT_COMPRESSION_LEMMA.md` gives an independent derivation. `checks/audit_signed_reconstruction.py` checks 204 random signed graphs against direct equation-space construction and 230 rational trace-reconstruction instances. These finite tests validate the reduction formulas; AHT's asymptotic guarantee is imported from its published theorem, not inferred from those tests.
