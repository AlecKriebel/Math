# Research log: hostile review of positive-rank full-list terminals

## 2026-07-28 PDT

- Froze the final theorem bytes at SHA-256
  `e25845bbf5e23886284f2046ac8c5c661b48176f4bef9fda5651f733d4a0edb0`
  and audited the final control implementation at commit `8f002f62`.
- Rechecked C-149, C-154, and C-157 at the exact dependency hashes in the
  candidate manifest.
- Audited the synchronous rank convention.  Rank \(h\) deletion means no
  response in \(\Omega_h\), so every dominating unbanned response has
  rank below \(h\); positive rank independently supplies a response in
  \(\Omega_0\).
- Audited every corridor occupancy, the direct-root retained restart,
  the nonroot private-witness exclusions, and the palette-free positive
  rank alternate.
- Audited minimum-rank descent and confirmed that it is invoked only
  after establishing unrestricted greatest-family membership.
- Audited anchor restoration.  Mover exhaustion forces the old terminal
  vertex to the attacked anchor; no missing palette entry is used as a
  graph nonedge.
- Rebuilt all three controls with an independent frozenset-based
  fixed-point implementation and an independent complement-coloring
  search.
- Exhaustively checked every terminal entry for each named
  root/target/color, not only the three selected records.
- Final verdict: unconditional pass at the stated strict scope.
