# Correlation-model and appendix continuation contract

Status: source-writing only; no Lean invocation or accepted axiom report.
Established before the new proof scripts on 2026-09-14.

## Exact goals

The primary new endpoints are the actual suprema of the first and second,
reduced and augmented, Bell functionals on Q_q, Q_qa and Q_qc at every d>=2.
The behavioral array consists of REAL Born probabilities; the plus-sign
first-harmonic correlator is derived from that array. A functional is not
redefined by its desired optimum or by a strategy's claimed score.

Q_q consists of the actual finite-coordinate, positive trace-one mixed-state,
tensor-product PVM behaviors. Arbitrary finite local index types and zero
measurement effects are allowed. Q_qa is the closure of this set in the
finite product topology. Q_qc consists of vector-state PVM behaviors on an
arbitrary complete complex Hilbert space, with all cross-party effects
commuting. No finite-dimensional or same-party-commutation condition is
added. Lean universe levels describe carriers, not dimension restrictions.

The finite-to-commuting embedding must be explicit: vectorize a positive
square-root factor of the density, adjoin an identity environment, and map
coordinate matrices into continuous operators on the Euclidean Hilbert
space. Prove normalization, PVM identities and the Born equality. Do not
postulate a behavior embedding or use a selected entangled witness in place
of the arbitrary input state.

The three-model value proof may avoid Q_qa subset Q_qc: continuity of a
finite Bell functional makes its sublevel set closed, transferring the
universal Q_q bound directly to Q_qa. This is enough for value equalities
with a common attained finite witness, without claiming the omitted general
closure inclusion or that Q_qc is closed. Prove nonemptiness and boundedness
before using the conditionally complete real supremum.

Reduced functionals use their actual reduced input alphabets, not an
augmented scenario renamed as reduced. Input restriction of the complete
witness provides attainment; a direct reduced operator bound handles all
competitors.

Additional goals, after that chain is written: the binary C*-algebra SOS and
arbitrary-Hilbert upper bound; binary model value wrappers; simple exact-value
appendix identities; honest party-swap transport. Each additional source
endpoint must have a corresponding expanded statement and generated axiom
query in the default build.

## Boundaries

All incoming mathematical proof files remain unchanged unless an explicit
repair is recorded. The canonical manuscript and qubit project are not
modified. The latest archive is the baseline, SHA-256
093043d7db11aea7d45c5896c4d16ae071184c92d4085757ef1d552b3c6f9255.
No source count or exact Python check constitutes kernel verification.
Independent review is not claimed: no subagent facility is available here.
The earlier GitHub integration denied writes; no alternative authentication
or access-control bypass is attempted.
