# Queue provenance correction

The frozen `artifacts/SOURCE_GATE.md` identifies `c87c275c638939b8008fd58db80657491d14971e` as the queue blob. That value was read from an already-existing line inside the queue file; it is not the actual Git blob identifier of the version used for this publication.

For base commit `f91b355fcee5465d8a942d142e1bad4eabdbb1db` in AlecKriebel/Math, the GitHub file tool reports the actual blob of `unsolved_math_prioritization/QUEUE.md` as `24545d98c2c211548377ed2f2555d6a129abfc69`. Decoding the tool's base64 response yields 383,256 bytes. Recomputing SHA-1 over the Git blob header and those exact bytes independently reproduces that identifier.

The rank-534 row in that version is `queued`, `0/5`. This branch changes only that row's Status to `unsolved` and Turns to `5/5`. All other queue bytes, including the pre-existing header line, are preserved. The original research files and their frozen SHA-256 manifest are also preserved.

This corrects repository-provenance metadata. It changes no mathematical statement, source-paper fingerprint, verification result, or unresolved classification. The independent mathematical audit remains the audit of the original frozen files.
