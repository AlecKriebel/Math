# Queue provenance correction

This note corrects one metadata assertion in the unchanged, frozen `../public/SOURCE_GATE.md`. It does not change the mathematics, source PDFs, independent mathematical audit, or reviewed-file hashes.

The frozen source gate calls `c87c275c638939b8008fd58db80657491d14971e` the fetched queue-file blob. That value occurs in a line already embedded in the repository file's body. It must not be treated as the connector's actual Git object metadata. The earlier blob attribution is therefore withdrawn as unverified.

At publication, the file was read at exact main commit `642e59ea2f6ad2e72920c4e6f57f23c600bfac35`. The connector returned Git blob SHA `59dba610d333684751e889818d21f66aba29cec9`. Decoding its full contents and independently calculating Git's blob hash agreed with that metadata. The file has 385282 bytes and SHA-256 `7444ffc4b78456cae98dc248946b9e6e665cd4e369ace163741c3da6b023f21e`.

Only rank 555 / ID 30006308's Status and Turns cells were changed, from `queued`, `0/5` to `unsolved`, `5/5`. Every other byte, including the pre-existing header line, Chat, Findings, DOI and other rows, was preserved. The resulting queue file has 385284 bytes, Git blob SHA `0ab36544a26f21c181a42e90ed85efdb8062e4cd`, and SHA-256 `063c13dfb0e500fe2549f551b93584df74f853201ae26c8ac28e69f7b02a903d`.

This publication-level correction is intentionally separate from the frozen research packet so that the original review binding remains reproducible. The recommended outcome remains unresolved after five substantive mathematical approaches.
