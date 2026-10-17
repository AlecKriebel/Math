# Checking the authored small board certificate

[EXACT_AUTHORED_CERTIFICATE.json](EXACT_AUTHORED_CERTIFICATE.json) contains only the authored examples from this pass. It contains no transcription of a source paper's board or routes. Its numbers are exact integers; no numerical tolerance or random seed is needed to inspect it.

## Face and coordinate conventions

Every orientation is ordered `(top,bottom,north,south,east,west)`. The reference state is `(1,6,2,5,3,4)`. The permitted die states are its 24 rotations, not both chirality classes. For `q=(t,b,n,s,e,w)`, rolling gives

    N(q) = (s,n,t,b,e,w)
    S(q) = (n,s,b,t,e,w)
    E(q) = (w,e,n,s,t,b)
    W(q) = (e,w,n,s,b,t).

The certificate uses `x` increasing rightward and row `r` increasing downward from the top. Thus `N` changes `(x,r)` to `(x,r-1)`. A cell index is `width*r+x`. This agrees with the two obstruction proofs. The orientation theorem uses a north-increasing coordinate `y`; for a displayed height-5 board the conversion is `y=4-r`. It does not reflect the die or exchange its north and south faces. In general the certificate phase uses `y=height-1-r`. For height 5, this preserves the checkerboard parity; for height 2 it reverses the phase naming relative to a convention that uses `x+r`.

A route record includes every visited cell, every full orientation, the top labels encountered, and its move word. Consecutive entries must obey both the coordinate move and the corresponding tuple permutation. The initial top counts as a required label match. A cycle word has a final closing roll; its route record lists the ten distinct cells plus a separate closing state, not eleven distinct cells.

## The 4 by 5 global connectivity obstruction

The certificate lists the board, all 20 induced cell states, each of the two ten-cell cycle routes, all 25 possible physical state edges, and the partition of those edges into 20 cycle edges, one bridge, and four excluded edges. An edge record contains its ordered endpoints and the unique full state required at each endpoint. Checking these records does not require trusting their category names.

For every physical adjacency, examine its two labels. Equal or opposite labels forbid a legal edge. Otherwise the top and the side that rolls to the new top uniquely determine the source orientation of this chirality. This procedure reproduces the 25 edge records, and no others. Every listed transition belongs to phase 0; phase 1 is empty. The certificate also records the degree of each endpoint state in the full legal state graph.

The four excluded edges have state-degree one at both endpoints, none at the prescribed start `s=(0,4)`. If used in a complete path, both incident cells would have to be global endpoints. This conflicts with the different prescribed starting endpoint. Removing them leaves two ten-cycles and only their middle bridge. The start is not adjacent on its left cycle to the bridge attachment. A path cannot cover the left cycle from the start to that attachment, so there is no complete path. The proof is in [CONNECTIVITY_OBSTRUCTION.md](CONNECTIVITY_OBSTRUCTION.md).

The local feasible selection omits `s—t`, where `t=(0,3)`, from the left cycle and keeps the right cycle. The certificate lists all 19 selected edges, degrees at all 20 cells, and the two selected components. Every chosen transition respects the induced full orientation. This selection has the required endpoint and interior degrees but is disconnected. Its candidate graph, including the bridge, is connected.

## The 2 by 5 cap

Two ten-cell routes start at the bottom-left in the same reference state. The intended word `NNNNESSSS` ends at the bottom-right; its terminal orientation equals a single east roll for every initial orientation because each fourfold north or south roll is the identity. The alternate word `ENNNNWSSS` ends at the left cell one row above the start. Both match the same displayed board and cover all ten cells exactly once. The alternate route alone disproves compulsory exit at the intended port when the endpoint is unrestricted.

The certificate includes both complete state sequences. The stated boundary identity in [FILLER_OBSTRUCTION.md](FILLER_OBSTRUCTION.md) follows separately by summing path degrees over a cell set; the finite example does not replace that general argument.

## The projected six cycle

The certificate includes the authored 3 by 2 pair-label pattern, a representative choice of actual labels, and its six perimeter cells. The lower row is `1 3 1` and the upper row is `2 3 2` in north-increasing coordinates. The certificate displays top-first rows `2 3 2` and `1 3 1`, while retaining the theorem's checkerboard origin at the lower-left. Its phase is computed with `y=1-r`.

Each perimeter edge lies in phase 0, but the full states required by consecutive edges are incompatible somewhere on the perimeter. Trying the four top-compatible starting orientations confirms that none rolls around this particular perimeter with all required labels. This witnesses the distinction between the projection and physical state continuity; it is not a puzzle solution or a complexity reduction.

## Review and integrity

The finite outcomes in [VERIFICATION_SUMMARY.json](VERIFICATION_SUMMARY.json) summarize the accepted source, producer, and independent checks. The [independent structural review](INDEPENDENT_STRUCTURE_REVIEW.md) supplies the general proof challenge. The certificate was assembled from the accepted examples using the displayed permutations, then rechecked for coverage, full states, complete edge enumeration, degrees, components, and all four possible starting orientations. That assembly check adds no new mathematical pass.

The public manifest records byte lengths and SHA-256 values for every file other than the manifest. Those values detect changed bytes; the complete arguments and exact certificate data establish the mathematics.
