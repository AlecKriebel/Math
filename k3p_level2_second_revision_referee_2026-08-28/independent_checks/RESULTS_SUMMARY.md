# Fresh selected-check results

Run status: **PASS (6/6)**.

The checks ran against `package_copy` at proof/package commit
`5a6d64cb2a76e890d7baaef3ba5ac9861c1d029f`.  Pre- and post-run verification
agreed on 622 sealed payload files and 160,506,893 payload bytes.  The package
manifest SHA-256 is
`090741f2cf6aa05ee5d9d65528e66980bb6eefd32c7cd25d49c8906fda83c1d0` and
the package checksum-ledger SHA-256 is
`627a644adc7ec55cd1f1780eedfa70ea5dfd956de538d28402285013f07cef14`.

The dependency-only runtime was Python 3.14.6, SymPy 1.14.0, and NetworkX 3.5.
The operating-system sandbox denied network and credential access and allowed
writes only below this directory's `results/` tree.  Each checker ran with
isolated imports and optimized Python disabled.  Static inspection found no
package-module import or dynamic execution primitive.  The obsolete JC
endpoint checker was neither copied nor run.

| Check | Exact result | Output SHA-256 |
|---|---|---|
| Three-leaf geometry | 5,000 strict-principal trials; all three orientations rank 14 at the common strict CT point; six nonzero gradient entries; cherry determinant `176/25` | `d0d4e05618098918dd6099e43556845fe46cffac0bd5509be7ec6135d3d92692` |
| Bridge gluing | degrees 3--16 have full three-sector exponent rank; 2,000 capped-gluing trials; minimum physical margin `4399/19360000` | `1dbe247eedbe88fe6f7ece27e47146cf0760a74a83f5cd8f44752633fa4969c6` |
| Four-port witnesses | final residue `40=38+2`; fourteen double cosets with sizes nine times 2 and five times 4; quartic source/target term counts `(1080,0)`, `(90,0)`, `(32,0)`; rank pairs `(11,10)`, `(14,12)`, `(11,10)` | `98209af0715f050156d0cba53cf4adc6904c19572c630b0de0bf02aba330ff9f` |
| Restoration/probe census | 36,824 restoration rows (`36,568+256`), 32 legacy continuation parents each with eight depth-two rows, all 574,535 probe rows (`29,964+544,571`), 2,107 equality parents | `60661eb2d0fb96d454eb33765c1bb355a6cf041d73c958ad0af60ca028dd8af5` |
| Probe semantics | five literal reconstructions: isomorphic, triangle, displayed-quartet mismatch, six-circuit tree/sunlet, and two-port equality/restriction | `0049dc034ee9693e4785f567ed97c74bcf97f73e29daab263f7227678623ec80` |
| Krawczyk box | strict self-inclusion; normalized distance `9.740999384091E-41`; contraction `8.077023076476E-47`; both rank-15 Neumann bounds below `5E-45`; all physical lower bounds positive | `bf3d48ccd044f16e3dd46f8fbaf730d02e086c9d2e910f925ae5cda2f7f6d307` |

All six output hashes equal the prior deterministic output hashes.  The fresh
suite report SHA-256 is
`30f51f6f35332d31182bbe7678a7b37a0bdab964c8e8c5ef2f50bfede0ddb13f`;
the audit-ledger SHA-256 is
`b06e97b29fc77a26e03bc65704ccc51dc328165aa18254ac686db40ade456af9`.

Scope limits remain material: the four-port check starts from the stored
40-row residue rather than redoing the 405,216-case reduction; the restoration
check streams and binds the stored forest rather than regenerating it; the
probe-semantic check covers five representative rows rather than all 574,535;
and Krawczyk uniqueness is confined to the supplied 15-dimensional pivot slice.
