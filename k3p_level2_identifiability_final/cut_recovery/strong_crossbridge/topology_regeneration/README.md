# Active graph-derived cut-topology regeneration

This directory contains a standalone graph-to-polynomial producer for the
finite cut-topology input.  It explicitly derives the five directed primitive
cycle/theta cores, constructs bounded rooted and incoming-port completions,
checks the standard strongly tree-child condition, enumerates switchings and
descendant masks, and produces the endpoint, one-active, two-active, and
switching-compression certificates.  It does not import the stored certificate.

Run from the repository root:

```sh
bash cut_recovery/strong_crossbridge/topology_regeneration/verify_all.sh
```

The wrapper writes the fresh 2.5 MB certificate only to a temporary directory,
verifies its graph witnesses and internal mask/hash relations, requires exact
byte equality with
`cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json`, and runs
coherent topology and mask mutations.  Optimized Python is rejected.

The producer was imported from the independently developed bridge-cut package
in the companion JC workstream.  Its role here is active regeneration, not a
trust in a frozen companion byte string: the K3P release gate executes the
producer and compares its fresh output to the exact input consumed downstream.
