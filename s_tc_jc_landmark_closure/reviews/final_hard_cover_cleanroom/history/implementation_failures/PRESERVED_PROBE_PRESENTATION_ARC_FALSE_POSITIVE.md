# Preserved presentation-sensitive arc-coverage false positive

Status: reviewer implementation failure; not a primary-stream failure.

An intermediate clean-room pass correctly found 100 observed and 100 expected
children for base path
`920a071edef4b626d93bd84232cc6e07f218bf14de15a514fd8a304fb68c813d`,
but compared raw insertion arcs after replacing the exact target rooted
presentation by an arbitrary isomorphic representative.  Raw vertex numbers,
and therefore raw arc pairs, changed.  The failure reinforced the schema-3
requirement: child coverage is indexed by the fixed root case and the exact
source/target rooted graph IDs, not just semi-directed or rooted-isomorphism
codes.

The corrected audit stores the exact primary graph IDs for every p and q
parent and computes the Cartesian arc set in those exact presentations.
