# Superseded n=4 theta-2 base and probe review

Status: **HISTORICAL — NOT AN ACTIVE CERTIFICATE**

This directory preserves the clean-room result produced before the primary
descriptor-cache provenance correction.  The replay was internally exact for
the bytes it read, but those bytes are no longer the active theorem inputs.

The superseded base inputs had the following physical SHA-256 commitments:

- graph stream:
  `9fd26a4e4f01e931fcfd1906a41576867f86299925d47adb41c06cf89241f492`;
- relation stream:
  `be741d4032028a683f0d49f827bc66d4067ca81cfc99c000a877086955923d08`;
- root stream:
  `330c4b4cee816bb67aaf6070775669c98eb0a1a17a6bc355d8af91eb935ea3ac`.

The superseded p/q summary had physical SHA-256
`e9f68bfb7333e25d0cb9dd2851fba4c88e032052c0a3664f46f3c640640a870b`
and explicitly bound those old base inputs.  Its clean-room structure,
algebra, mutation, and 168,582-record evidence artifacts are retained here
only to preserve the audit trail.

An intermediate primary n=4 summary then had physical SHA-256
`fd3b7a6a180a5569bf6d1f3056d8c31756d4b14eec8bf19805f37706748e9342`
and reports descriptor caching keyed by selected-port count and exact rooted
graph ID.  It too was superseded when admissible rootings exposed quartet
masks differing by split complement.  The next producer canonicalizes each
zero-sum quartet mask as `min(S,S^c)` to zip root-edge factors and recover
root-location invariance.  The clean-room audit of the intermediate bytes was
terminated before emitting a certificate.

No p/q stream currently committed to the primary package binds the pending
final base summary.  Therefore current base and p/q probe closure are both
**UNRESOLVED** until the final summary SHA is locked and replayed.

Nothing in this historical directory may be consumed by the active
`verify_all.sh` entry point or cited as evidence for the corrected base run.
