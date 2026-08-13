# Quarantined schema-2 hard-cover run

Status: **FALSE AS A RELATION CERTIFICATE**

The primary theta-2 run completed with 132 fixed roots and 1,518 canonical
states, but `primary/verify_hard_cover_artifacts.py` rejected it.  A state was
identified only by the two standard semi-directed mixed codes and remaining
roles.  Distinct rooted presentations of the same mixed graph could therefore
merge, while the state retained only the first rooted graph, polynomial
witness, and child set.  At least one raw coverage record had a different
`target_graph_id` from its canonical state.

The contained bytes are preserved solely as a regression fixture.  They are
not consumed by any active theorem verifier.  Schema 3 additionally binds a
state to its fixed-full root case and exact source/target rooted graph IDs.

The interrupted schema-2 n=3 run emitted no final streams and was stopped as
soon as this failure was reproduced.
