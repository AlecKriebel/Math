# Independent encoding and certificate audit

Checkpoint: 2026-09-17T03:37:13Z. Assigned audit completion estimate: 100%.

**Verdict: PASS.** No flaw was found in the stated necessary finite
relaxation, its CNF encoding, the supplied UNSAT certificate, or the proof
checking logic as applied to these artifacts. This is an independent agent
audit and independently written computation, not external human peer review.

## Exact claim and assumptions

The audited consequence is nonexistence of a finite placement on distinct
integer squares, with nonempty knight and rook sets, every knight attacking
at least four rooks, and every rook attacking exactly two knights and no
rooks. A rook attacks only the first occupied square on each orthogonal ray.
Knight-knight attacks are unrestricted. The original N=4, R=2 requirements
are a special case. The certificate does not establish a statement about
infinite placements or other chess attack conventions.

## Necessity of the local model

1. The finite, nonempty knight set has a greatest x-coordinate. A rook to
   its right has no knight north, south, or east, and at most one visible
   knight west. It cannot attack two knights. Thus after translating a
   rightmost knight to (0,0), all pieces have x <= 0.
2. Direct enumeration of all eight knight moves from the four distinguished
   locations confirms that every move lands in D or in x > 0. Their local
   rook-target counts are therefore their full target counts. The counts
   of potentially occupied targets are 4, 6, 6, and 6.
3. Every globally occupied rook ray ends first at a piece. No rook can be
   that first piece, so the first piece is a knight. Hence exactly two
   occupied global rays, and at most two occupied local rays, are necessary.
   Restricting a ray to D cannot create a new occupied direction. Pieces
   outside D cannot invalidate a local occupied-ray witness.
4. Two aligned rooks without an intervening knight cannot occur: among the
   rooks on their intervening segment, some consecutive pair has no piece
   between them and therefore attacks each other. Conversely, a knight
   between every pair of aligned rooks suffices to prevent any local
   rook-rook visibility. Since D is a rectangle, the entire segment between
   a pair in D lies in D; no required separator has been discarded.
5. Type exclusivity and occupancy/ray definitions faithfully describe the
   restriction of a real placement. All omitted degree and exterior
   constraints weaken the local model. No extension of an arbitrary local
   assignment to a global placement is claimed or needed.

These deductions establish the required implication from any hypothetical
finite counterexample to a satisfying local assignment. An UNSAT result for
that local model therefore proves nonexistence on every finite board and
for arbitrary finite placements. The 4-by-7 window is not being asserted to
contain an entire placement.

## Encoding checks

The independent script imports none of the supplied source files. It reads
the variable-name table and CNF, requires a bijective numbering of exactly
the independently expected variable names, and reconstructs clauses from
coordinates. Ray squares are enumerated by stepping, aligned pairs by row
and column sublists, and knight moves by eight explicit displacements.
Clause multisets agree exactly, including multiplicity:

| Family | Clauses |
|---|---:|
| Occupancy and disjoint types | 112 |
| Ray equivalences | 342 |
| Guarded ray upper bounds | 54 |
| Rook separators | 126 |
| Guarded knight lower bounds | 64 |
| Origin anchor | 1 |
| Total | 699 |

There are 174 variables. Every Boolean gadget type is also checked against
its direct mathematical predicate by exhaustive truth tables, totaling 728
assignments. In particular, the threshold clause size t-3 is correct: a
count below four has at least t-3 false target variables; conversely such a
false subset witnesses a count below four. The guard correctly disables
the requirement when the square is not a knight.

## Certificate checks and independently derived obstruction

The exact CNF SHA-256 is
`991d45763d7e62b35ddedc7af5040cf93ef5e83b9b7b02340bbdb53da6930f10`.

The independently implemented checker evaluates residual clauses under a
partial assignment. Each asserted inference must leave exactly its recorded
literal, each contradiction must leave an empty clause, and both values of
every fresh split are checked. It validates the supplied three-node tree,
one split on variable 19 = K(-1,1), two conflicts, and 151 unit steps.

The original checker was also inspected for soundness: consistent assignment
sets are preserved; unit steps must have all other clause literals false;
both split children are mandatory; and a conflict must falsify an original
clause. There is no acceptance path for an unverified proof leaf in this
certificate. Robustness against every conceivable malformed input is not
being claimed as part of this mathematical audit.

As a further check independent of the supplied inference sequence, the new
script assumes each sign of K(-1,1) and runs its own unit propagation in
reverse clause order. Both branches contradict an original clause. Its
fresh certificate has three nodes and 222 unit steps. Both the independent
checker and the supplied checker accept this new certificate.

Negative controls invert each of the supplied proof's 151 unit literals
individually and remove each of the two split branches individually. The
independent checker rejects all 153 corrupted certificates.

## Artifacts and reproduction

Run from the package root with Python 3.9 or later:

```sh
python3 review/encoding_independent.py
python3 src/verify_unsat.py certificates/local_relaxation.cnf review/encoding_fresh_proof.json
```

The first command reproduces `review/encoding_results.json` and
`review/encoding_fresh_proof.json`. No solver or optional dependency is used.
The strongest verified result is the stated necessary local obstruction and
its UNSAT consequence. No remaining mathematical gap was identified in this
assigned scope; historical novelty and source-page interpretation are
outside this encoding audit.
