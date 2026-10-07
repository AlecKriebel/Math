# Frozen native operator v2: case-boundary source FAIL

SOURCE-only FAIL for 52090 bytes SHA256 2dadb9419fd3d4a5946fbe15b77f09da5352ffaefe7164d8825c3fbef276cd67. The lifecycle fixes resolve N1/N2. A remaining admission-policy gap treats nonpublic/archive exclusions as case-sensitive although the host may resolve those physical paths case-insensitively.

Mandatory N3: own-audit members under PRIVATE, Private_Controls, CACHE or .GIT evade the lowercase private/cache/Git exclusion. A lower-case ignored directory can be absent from the Git tree, so sparse existing-tree alias detection does not guarantee rejection. Mandatory N4: Original/README.md and original17_manifest.JSON evade the frozen original destination exclusion. The tree constructor can independently reject aliases of existing tracked names; these probes establish the missing admission predicate, not actual successful publication.

All six source-admission counterexamples reproduced with in-memory records normally (PID 26471, 2026-10-07T18:48:06.900425+00:00) and optimized (PID 26479, 2026-10-07T18:48:07.010589+00:00). Custody/resource/archive helpers were stubbed to isolate the path-policy boundary. No actual data/plan approval or source operator was invoked. The genuine candidate member allowlist contains no such paths; no private input was published. A separate107-case kernel/custody/lifecycle suite passed in both modes but is limited control evidence and does not overturn this source FAIL.

Root and preparer agreed a distinct successor repair: casefold nonpublic path components and frozen original prefix/manifest; include the intended ignored private_* convention. Preserve this source/seal, counterexamples and prior v1 FAIL. Review the repaired exact source anew before any native/data action.

Sealed PID 28041, 2026-10-07T18:50:30.035865+00:00. Bounded source finding identification100%; overall native source clearance incomplete. No native/global/ref/index/remote mutation or actual publication/installation.
