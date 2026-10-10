# Additive queue-provenance correction

Publication preflight, 2026-10-04 UTC.

The frozen author files `public/SOURCE_GATE.md` and `public/SOURCES.json` identify `c87c275c638939b8008fd58db80657491d14971e` as an observed queue blob. That identifier was taken from a literal line already present inside the queue file and must not be treated as the authoritative GitHub object identity for the publication base.

At base commit `fab787f7df8b481cc95df2be593b6f64a4818585`, the GitHub contents tool reports the actual blob for `unsolved_math_prioritization/QUEUE.md` as:

`59dba610d333684751e889818d21f66aba29cec9`

The downloaded content is 385,282 bytes. Independent Git blob hashing of those exact bytes reproduces that identifier. Its SHA-256 is `7444ffc4b78456cae98dc248946b9e6e665cd4e369ace163741c3da6b023f21e`.

The file's literal first line is:

    sha: c87c275c638939b8008fd58db80657491d14971e size: 363342

That line is existing file content, not current tool metadata. It is preserved unchanged, along with every other queue byte outside rank 549's authorized Status, Turns and formerly blank Findings cells. No attempt is made here to repair or reinterpret the queue's historical header.

This note supersedes only the author package's identification of the queue blob. It does not alter the frozen author files or independent audit, the mathematical proof, the source-PDF hashes, the published attribution, or the accepted disposition `already_solved`, `1/5`.
