# Corrected folding derivative: output records versus source coordinates

Final shared PASS5, 14 October 2026.

Reviewed derivative: `pass5_collective_windows/FOLDING_ENTROPY_OBSTRUCTION.md`, SHA-256 `0241b9c09b2a20390289479200a33fedadd2037e3751c0cb0ac03c90d798430c`.

**Accepted.** This supplements the preserved `FOLDING_ACCEPTANCE.md`, which reviewed the preceding version. The current derivative is the operative proof pin. Its clarification is important: the identical turnaround-location records are locations in the folded output. Original source coordinates may vary between source bit choices. The previous acceptance must not be read as asserting identical source coordinates.

All earlier exact orientation, path-validity, collision, size and entropy computations are unchanged. The derivative also supplies a valid stronger argument when full source coordinates are retained.

There are 2R+1 original turnaround cells including endpoints, each with pattern 12, hence m=4R+2 marked source points. Successive marked cells have cell-index distance at least W-1>=2. Their points therefore have the fixed induced pattern consisting of 2R+1 copies of 12 in skew order. A set of m positions and a set of m values determine every coordinate pair once that induced pattern is fixed. Thus at most binom(n,m)^2 source-coordinate records are possible; the fixed level walk already determines the relevant cell indices.

Pigeonholing the 2^(R*a) sources yields a recorded fiber of size at least 2^(R*a)/binom(n,4R+2)^2. For fixed W, the marked-point fraction tends to 4/(4W-4+a) as R tends to infinity. The binomial entropy bound gives precisely the rate in equation(12). As W subsequently tends to infinity, its entropy penalty 2h(4/(4W-4+a)) tends to zero, while its first term tends to log 2/9. Thus the strengthened lower bound is positive for all sufficiently large fixed W. No assertion of positivity for every small W is needed.

Retaining all listed source coordinates therefore still fails to make the map injective or its worst-case fiber entropy vanish with width. This remains an obstruction to the specified transformation and retained metadata, not to every conceivable encoding or to a uniform permuton limit.
