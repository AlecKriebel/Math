# Locked K3P fourteen-orbit table

The 40 post-filter relations reduce to **14 canonical directed relation orbits** and **10 algebraically distinct comparisons** after exact graph, port, inverse, and identical-source-map symmetries. Every row below is reconstructed from its literal rooted graph.

| Orbit | Family | Source | Target | Ranks | Port permutation | Raw members | Source/target map hashes |
|---|---|---|---|---:|---|---:|---|
| `H21-01` | rank21_nonautomorphic_relabelling | `S1:theta0:repair1` | `T80:theta0:repair1:perm0132` | 21→21 | `(0, 1, 3, 2)` | 4 | `5a9dcb458d3d` / `8736f9de4e6f` |
| `H21-02` | rank21_nonautomorphic_relabelling | `S1:theta0:repair1` | `T80:theta0:repair1:perm0213` | 21→21 | `(0, 2, 1, 3)` | 4 | `5a9dcb458d3d` / `d012985f5a0c` |
| `H21-03` | rank21_nonautomorphic_relabelling | `S1:theta0:repair1` | `T80:theta0:repair1:perm0231` | 21→21 | `(0, 2, 3, 1)` | 4 | `5a9dcb458d3d` / `a78194e93f0d` |
| `H21-04` | rank21_nonautomorphic_relabelling | `S1:theta0:repair1` | `T80:theta0:repair1:perm0312` | 21→21 | `(0, 3, 1, 2)` | 4 | `5a9dcb458d3d` / `e44a2aaecc42` |
| `H21-05` | rank21_nonautomorphic_relabelling | `S1:theta0:repair1` | `T80:theta0:repair1:perm0321` | 21→21 | `(0, 3, 2, 1)` | 2 | `5a9dcb458d3d` / `fd04bd5c1287` |
| `H21-06` | rank21_nonautomorphic_relabelling | `S1:theta0:repair1` | `T80:theta0:repair1:perm1032` | 21→21 | `(1, 0, 3, 2)` | 4 | `5a9dcb458d3d` / `394b68dbe68b` |
| `L20-01` | lower_to_rank24 | `S0:theta0:repair0` | `T822:theta3:repair1:perm1203` | 20→24 | `(1, 2, 0, 3)` | 2 | `631bc9fbcc40` / `c26c11b81283` |
| `L20-02` | lower_to_rank24 | `S0:theta0:repair0` | `T822:theta3:repair1:perm1230` | 20→24 | `(1, 2, 3, 0)` | 2 | `631bc9fbcc40` / `3ccb3fd24f85` |
| `L21a-01` | lower_to_rank24 | `S2:theta1:repair0` | `T822:theta3:repair1:perm0123` | 21→24 | `(0, 1, 2, 3)` | 2 | `3369199bc298` / `92a68687918e` |
| `L21a-02` | lower_to_rank24 | `S2:theta1:repair0` | `T822:theta3:repair1:perm0132` | 21→24 | `(0, 1, 3, 2)` | 2 | `3369199bc298` / `af3502889424` |
| `L21b-01` | lower_to_rank24 | `S3:theta1:repair1` | `T822:theta3:repair1:perm0123` | 21→24 | `(0, 1, 2, 3)` | 2 | `3369199bc298` / `92a68687918e` |
| `L21b-02` | lower_to_rank24 | `S3:theta1:repair1` | `T822:theta3:repair1:perm0132` | 21→24 | `(0, 1, 3, 2)` | 2 | `3369199bc298` / `af3502889424` |
| `L23-01` | lower_to_rank24 | `S4:theta3:repair0` | `T822:theta3:repair1:perm0123` | 23→24 | `(0, 1, 2, 3)` | 2 | `a768d785ab8c` / `92a68687918e` |
| `L23-02` | lower_to_rank24 | `S4:theta3:repair0` | `T822:theta3:repair1:perm0132` | 23→24 | `(0, 1, 3, 2)` | 2 | `a768d785ab8c` / `af3502889424` |

## Exact algebraic quotient

- `A-H21-01`: `H21-01`
- `A-H21-02`: `H21-02`
- `A-H21-03INV`: `H21-03`, `H21-04`
- `A-H21-05`: `H21-05`
- `A-H21-06`: `H21-06`
- `B-L20-01`: `L20-01`
- `B-L20-02`: `L20-02`
- `B-L21-01`: `L21a-01`, `L21b-01`
- `B-L21-02`: `L21a-02`, `L21b-02`
- `B-L23`: `L23-01`, `L23-02`

## Two pre-lock integrity separations

Two of the 40 post-quadratic raw presentations are nonautomorphic source-5/target-822 sink swaps. They are not graph terminals. The integrity replay assigns both an exact characteristic-zero quartic separator in `software/certificates/k3p_prelock_source5_quartic.json`; the remaining 38 raw presentations form the 14 locked orbits.

## Integrity fields

Each JSON record additionally contains the source and target incoming roles, repair tags, literal graph nodes and arcs, complete output and parameter orders, edge-signature hashes, exact rank points, and an automorphism witness for every raw member.
