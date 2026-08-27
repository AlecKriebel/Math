# Deterministic archive rebuild metadata

- Input archive: 214,930,375 bytes; SHA-256
  `86a286be82ce3c211f556eaa24cf1120aa42e41f716b46cb8752c1d2546053ba`.
- `rebuild_a.zip`: 214,930,375 bytes; same SHA-256; completed
  2026-08-26T20:25:42-0700; measured builder runtime 20.65 s.
- `rebuild_b.zip`: 214,930,375 bytes; same SHA-256; completed
  2026-08-26T20:26:03-0700; exact byte comparison with the input and rebuild A
  returned zero. Its runtime output was not retained because the combined
  shell invocation yielded while this second build was active.
- `rebuild_c.zip`: 214,930,375 bytes; same SHA-256; completed
  2026-08-26T20:26:43-0700; measured builder runtime 20.92 s.

All three disposable rebuilds were removed after hashing to conserve disk.
