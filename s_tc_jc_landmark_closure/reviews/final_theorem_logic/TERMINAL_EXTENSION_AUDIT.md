# Path-bound terminal-extension audit

## Verdict

**ACCEPTED AS THE CORRECT FINITE ARBITRARY-WORD IMPLEMENTATION, SUBJECT TO
THE CONTRACT BELOW.**

After a fixed-full restoration path terminates at
`A = Q_s union Q_t` in labelled isomorphism or ordinary `T`, it is sufficient
to extend that terminal directly by one label `p` and then one label `q`.
This realizes the safe twelve-tensor-port promotion and removes any need for
factorial full-target-boundary enumeration at outgoing sizes five and six.

It does not discharge the separate unequal-signature base relations.

## Exhaustiveness proof

The set `A` contains:

1. every source reticulation-sink boundary, through `Q_s`;
2. every target reticulation-sink boundary, through `Q_t`;
3. the independently selected incoming boundary of each rooted factor; and
4. a complete strong repair for each factor.

Consequently every boundary label outside `A` is an ordinary port attached at
one subdivision tree vertex of an internal blob arc on both sides.  Restrict a
fixed full relation to `A+p`.  All other ordinary subdivision vertices are
suppressed, so this restriction is obtained uniquely by subdividing one
internal arc of the `A` terminal graph and attaching the port `p`.  Enumerating
every such arc on both sides therefore includes the actual restriction.

Now restrict to `A+p+q`.  Relative to its exact `A+p` parent, the same argument
inserts `q` on one current internal arc.  If `p,q` lie in one anchor interval,
the arcs immediately before and after `p` produce both possible orders.  If
they lie in different intervals or segments, their independent placements are
also present.  Thus all one-port locations and all same-segment pair orders
are covered.  Pointwise rigidity of `A` forces every child transport to
restrict to the same base transport, and the pair comparisons reconstruct
each complete finite source word coherently.

No full symmetric-group action remains at these stages.  The labels of `A`
and their transport were fixed by the parent path, while `p` and `q` are fixed
physical labels of the same full relation.  The finite choices are arc
placements, not arbitrary relabellings.

## Required record schema

Every `A+p` or `A+p+q` relation must record and verify:

- the raw path-bound base-terminal identifier;
- restoration-root and parent-path identifiers;
- the fixed `Q_s`, `Q_t`, and role-to-physical-label maps;
- source and target parent graph identifiers;
- the subdivided source and target arc identifiers;
- the new physical label;
- raw-to-canonical vertex, edge, inheritance, and port transports;
- a deletion map whose normalized result is exactly the parent relation;
- locked standard-strong membership of both child graphs;
- regenerated switchings, descendant masks, complete JC tensors, pullbacks,
  strict signs, and generic-rank data; and
- one terminal classification: isomorphism, ordinary `T`, exact separation,
  lower-dimensional intersection, or proper one-sided containment.

Canonical child states and algebra may be content-addressed and shared, but
raw parent-child relation records may not be discarded or merged merely
because two children have the same target graph or polynomial hash.

## Mandatory mutations

The release verifier must reject at least:

- extending only one representative of a deduplicated terminal state;
- changing `Q_t` or a port transport between the base and a child;
- omitting one admissible source or target internal arc;
- inserting `p` or `q` on a pendant/cut arm and calling it a blob word;
- accepting a child whose deletion canonicalizes to a different parent;
- swapping the parent of an `A+p+q` relation;
- selecting a separator by topology id rather than regenerating its pullback;
- accepting a valid polynomial attached to the wrong decorated relation; and
- allowing probe-specific `T` maps that do not restrict to the base map.

## Separate unresolved gate

The equal-signature hard cover begins only after source and target invariant
decks agree.  The current bounded screens contain 110 and 776
unequal-but-necessary directed signature pairs at outgoing sizes three and
four.  These require pair-level graph-derived exact separators or rank
obstructions for every decorated presentation relation they represent.

No active `primary/certificates/bounded_relations_n*.jsonl.gz` stream exists.
Therefore the terminal-extension design is accepted, but Outcome P remains
unresolved until this pair-level gate, the n=4 theta-2 base cover, and the
independent normalized replay all close.
