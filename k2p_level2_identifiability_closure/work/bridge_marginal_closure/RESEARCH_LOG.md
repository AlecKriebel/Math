# Research log

## 2026-08-21 — reconstruction started

- Recovered the one-sector bridge architecture from the graph-only JC proof
  and rebuilt it for the two observable K2P character sectors.
- Kept the paired characters `C,T` under one incidence scale and the singleton
  character `G` under an independent scale.
- Derived an explicit serial-edge section on `D_plus`: for an effective edge
  `(S,G)` and chain length `m`, choose `r` with
  `r^(m-1) > max(S,G,2S-G,0)`, use `(r,r)` on the first `m-1` edges, and
  `(S/r^(m-1),G/r^(m-1))` on the last.
- Derived simultaneous physical gluing for arbitrary positive incidence
  products by choosing the source bridge coordinates sufficiently small.
- No mixed-sign claim is made.
