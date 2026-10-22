# Independent combinatorial-family audit of PR778 / 30001054

This audit checks the corrected finite counterexample, not priority, novelty, or PR disposition. The frozen head supplied at intake is c9a87710414d1d4ac5f21e84a81a7d3d40d4d094. The complete selected record has statement SHA256 220b900750d7fa3d7062a4aa1879d1b178ea11c5247cf7a28436feb39071820a and review SHA256 51710cccfe6bcd44ff5a8bd2b663db2387edbf19169806cfc0c1855f24822377. Prior research is empty. The exact imported target asks whether every allowable double-permutation sequence arises from connected sets with specified pseudoline separators/common tangents.

## Finding and scope

The witness is a valid counterexample to the universal realization statement when allowable means exactly the four printed state axioms. Its period is primitive, every transition is one adjacent cross-body swap, and all mixed event types are absent. The source geometry explicitly requires two internal and two external common tangents per pair; its encoding reads the eight directed tangent events. Thus it cannot encode this word. The witness does not refute a realization statement restricted to switch-once interval sequences or a fibration class. This family does not independently verify the Habert-Pocchiola theorem, and makes no claim about novelty or the complete normalized polygonal construction problem.

The source problem-session output clause mentions the fully separated term (1,1',...,n,n'). If that clause is interpreted as restricting the input class to sequences containing that term, the witness is outside that class. Neither the four numbered axioms themselves nor Goodman-Pollack Definition 12 includes such a restriction. Therefore the additional normalization must be distinguished explicitly; it cannot silently be used to reject this counterexample to the imported unqualified four-axiom target.

## Independent derivation

Use -i for i'. The six linear extensions of 1<-1 and 2<-2 are:

| Name | State | Adjacent cross-body neighbors | Reverse-toggle image |
| --- | --- | --- | --- |
| X | (1,-1,2,-2) | A | Y |
| A | (1,2,-1,-2) | X,B,D | C |
| B | (1,2,-2,-1) | A,C | B |
| C | (2,1,-2,-1) | B,D,Y | A |
| D | (2,1,-1,-2) | A,C | D |
| Y | (2,-2,1,-1) | C | X |

This list is exhaustive: choose the two positions for the endpoints of body 1 among four, then their internal order and that of body 2 are forced. The graph is a square A-B-C-D-A with leaves X at A and Y at C. Reversal followed by prime toggle is an involutive graph automorphism R.

For w=(A,B,A,B,C,B,C,B), w[k+4]=R(w[k]) at every cyclic phase. The closing B->A move is the same legal adjacent swap as the other B->A moves. The length is eight, exactly 8*C(2,2). A least period of an eight-periodic word divides eight. Since w[0]=A differs from w[4]=C, none of 1,2,4 is a period. This is a primitive period of length eight.

In the OWR/Goodman-Pollack after-switch convention the events are

(-2,-1), (-1,-2), (-2,-1), (2,1), (1,2), (2,1), (1,2), (-1,-2).

Each of the four supporting directed types appears twice. The four separating types (1,-2), (-2,1), (-1,2), (2,-1) appear zero times. In the interval manuscript convention, write each event before rather than after the move; this reverses each ordered pair. The same four missing mixed types and the same supporting multiplicities remain. A phase shift merely permutes event positions; reversal reverses the ordered pairs and event order; renaming bodies permutes types. These operations cannot supply a missing mixed event.

Goodman-Pollack Proposition 10 states a stronger necessary switch property before Corollary 11 lists the four weaker state properties. Definition 12 names only Corollary 11. In particular its required mixed switches are not consequences of those four state conditions, as the explicit word demonstrates. This establishes an actual definition gap, rather than a failure of the later representation theorem.

## Exhaustive finite check

The independent verifier derives transitions from changes of pairwise endpoint orientations (Kendall distance), not by comparing the two changed positions. It rejects anything other than exactly one adjacent cross-body inversion. A separate enumerator generates the six-state graph by direct adjacent swaps; all 36 ordered state-pair checks agree with the orientation validator.

One exhaustive method visits all four-move paths from s to R(s) and reflects the first half. A second independently loops through all 6^4=1296 half-tuples and validates their reflected eight-term words without path pruning. Both find exactly 48 indexed primitive weak words. Sixteen have a separated state and every directed type once; 32 have no mixed event at all. There are three orbits under phase shift, traversal reversal, and body-label exchange. All 32 transformations of every accepted word are verified, with event obstruction and switch-once status preserved. The complete machine-readable state graph, orbit representatives, events, and controls are in EXACT_RESULTS.json.

Seventeen negative controls cover malformed schema, bool-as-int inputs, degenerate n=1, duplicate/missing/zero endpoints, reversed same-body order, stationary transitions, simultaneous changes, nonadjacent changes, wraparound, broken half-period relation, wrong length, smaller least period, and direct helper-level same-body/nonadjacent exchanges. Some controls intentionally fail an earlier guard; their actual failure reason is recorded, so they do not pretend to isolate a later axiom. The primitive-period function is independently computed by testing every divisor. No check uses Python assert.

Normal and python -O exact runs pass and produce byte-identical output. Separated-start positive controls for n=2,...,7 also pass under both modes, with full lengths 8,24,48,80,120,168. These are validation examples, not evidence replacing the following general argument.

## Fully separated-start implication

Let a sequence satisfy the four axioms and contain a term consisting of adjacent endpoint blocks, in any body order. Its R-image reverses the order of the blocks, while retaining the order of each body's own endpoints. Every one of the four cross-body endpoint pairs for each pair of bodies reverses its relative order. The Kendall distance from this state to its R-image is therefore 4*C(n,2).

That is exactly the prescribed number of steps in a half-period. Each adjacent move changes exactly one pair's relative order. Every cross-body pair needs an odd number of changes, hence at least one, and there are precisely as many moves as such pairs. Consequently each changes once in the half. In the other half the reverse-toggle involution supplies the four complementary directed types. Every ordered cross-body switch occurs once in the full period. This proves separated-start implies switch-once for arbitrary n. No converse for n>=3 is claimed.

For n=2 this is also visible directly: the two separated leaves have distance four, so a four-step half-path between them must be X-A-(B or D)-C-Y, or its reverse. It cannot make any detour. The witness never visits either leaf. Requiring all terms to be different would not be a source-supported rescue: six states cannot fill the stipulated eight terms, and even the source's legitimate two-body switch-once patterns repeat states. Requiring simple moves is already satisfied by the witness; interval simplicity means one ordered pair per move.

## Source reading and limits

SOURCE_RETRIEVALS.json preserves retrieval URLs, redirects, byte counts, and PDF SHA256 values. SOURCE_READING.json records complete relevant page ranges and visual checks. Full bodies and temporary renders were removed after reading; no other family's material was accessed or cleaned. The initial position was sealed before historical opinions; no historical review implementation or other fresh family's findings were read. The source bodies themselves, not search-result fragments, support the definition comparison.

The local policy's five-attempt boundary is respected: this is a finite adversarial audit of an existing corrected candidate, not a new search extending an unfinished construction target. No outside person was contacted; no Git, index, queue, PR, sheet, release, or Zenodo action was taken.

ENOSPC intermittently prevented writes; failed operations and successful retries are recorded in RESEARCH_LOG.md. One cleanup command containing rm -f was rejected by automatic approval review. It was replaced with a scoped operation deleting only two specifically named own duplicate/empty scratch outputs. This did not drop any check: the optimized run is reproduced in memory by replicate.py.
