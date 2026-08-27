# Execution and falsification record

Date: 2026-08-26 (America/Los_Angeles)

All commands below were run in the dedicated audit directory.  The supplied
packet was copied to `packet_copy/`; every substantive mutation was made in a
separate directory under ignored `packet_mutations/`.  No checksum was refreshed
and the packet orchestrator was deliberately bypassed for the negative controls,
so a manifest failure could not masquerade as mathematical detection.

## Environment

- macOS 26.5.2 (build 25F84), Darwin 25.5.0, arm64
- Python 3.14.6
- Tectonic 0.16.9 at `/opt/homebrew/bin/tectonic`
- Poppler `pdftotext` and `pdftoppm` 26.08.0
- SymPy 1.14 in the ignored audit-local virtual environment

## Packet integrity and provenance checks

- Independently checked all 37 entries in `PACKET_SHA256SUMS`: every digest
  matched, the listed path set was complete, and the original copy remained
  unchanged after execution.
- Compared all 32 `materials/` files byte-for-byte with the stated canonical
  commit `3d3e4abee9f4dab9f5f1b3ec9f73740aa04c565c`: all matched.
- The local annotated tag `k2p-k3p-theta-v1.2.3` resolves to that commit, but it
  is unsigned.  This corroborates provenance in this checkout; it is not an
  external cryptographic trust anchor.

## Complete replay

From `packet_copy/`:

```text
bash ./RUN_REFEREE_REPLAY.sh --with-pdf
```

Exit status: 0.  The normal and optimized complete outputs matched the supplied
complete transcript.  Normal/optimized four-leaf runs matched each other and
the supplied transcript.  The focused simple, displayed-tree, source-convention,
and four-leaf outputs matched their stored counterparts.  Every support entry
point exited successfully.  Regeneration of the compact K2P certificate was
byte-identical.  Tectonic rebuilt all three PDFs, and Poppler layout-preserving
text extraction matched each supplied PDF.  The orchestrator's pre- and
post-execution integrity checks passed.

This is a replay result, not by itself an independent validation; the static
code audit and clean-room reconstruction assess what was actually tested.

## Clean-room symbolic reconstruction

Command:

```text
tmp/sympy_env/bin/python notes/clean_room_symbolic_checks.py
```

Exit status: 0.  The program imports no packet module and reads no packet JSON.
It independently reconstructs the compact K2P and quartic K3P four-switching
maps, all 64 Fourier coordinates, all 64 ordinary-state probabilities via
literal retained-graph Markov pruning and comparison-star pruning, the compact
K2P probability minimum, the selected rank-9 and rank-15 determinants, and the
K3P fixed-output tangent identity.  Output ended with:

```text
compact K2P factorization, independent pruning, 64 coordinates, minimum, and rank-9 determinant: PASS
quartic K3P factorization, independent pruning, 64 coordinates, rank-15 determinant, and IFT tangent: PASS
ALL CLEAN-ROOM SYMBOLIC CHECKS PASSED
```

## Substantive negative controls

### NC-1: collision datum

Changed only the simple K2P `U` vector from
`(1,4/5,19/30,4/5)` to `(1,79/100,46/75,79/100)`.  This preserves K2P
symmetry, strict stochasticity, and the verifier's minimum transition entry
`1/120`, while breaking the certified factorization.

```text
PYTHONDONTWRITEBYTECODE=1 python3 materials/verify_k2p_simple.py
```

Exit status: 1.  Field, topology, parameter, and root-splitting checks passed;
the first relevant failure was `AssertionError: factor (0, 1)`.

### NC-2: graph assignment

Changed the literal rooted-arc assignment for `p -> r2` from vector `S` to
vector `T` in the graph-based displayed-tree verifier, leaving the expected
monomials unchanged.

```text
PYTHONDONTWRITEBYTECODE=1 python3 materials/verify_k2p_displayed_trees.py
```

Exit status: 1.  The source-convention prelude passed; graph reconstruction then
failed with `AssertionError: wrong graph-derived monomial for switch ('p', 'p')`.

### NC-3: rank certificate

Changed the stored compact K2P determinant numerator from
`-4126104359487341` to `-4126104359487342`, without changing primitive
parameters or the differentiator.

```text
PYTHONDONTWRITEBYTECODE=1 python3 materials/src/verify_k2p_rank_family.py
```

Exit status: 1.  Both number-field checks passed; exact differentiation and
elimination rejected the stored value with `AssertionError: simple determinant`.

### NC-4: K3P continuous-time tangent

Changed the constant coefficient of the pivot derivative `e_u_p.a_G` from
`-6/19` to `13/19` in both the embedded certificate and its sidecar, so the
sidecar-consistency check could not be the reason for rejection.

```text
PYTHONDONTWRITEBYTECODE=1 python3 materials/src/verify_k3p.py
```

Exit status: 1.  Sidecar equality, field/topology/construction, collision,
K3P-scope, and Jacobian/rank checks all passed.  The targeted fixed-output
check failed with
`AssertionError: linearized fixed-output identity in row 1: Alg(0, 0, 0, 1/128)`.

### NC-5: K3P Jacobian semantic-label cycle (surviving mutation)

In a fresh ignored copy, kept the first three displayed Jacobian names fixed as
`e_rho_1.a_C`, `e_rho_1.a_G`, and `e_rho_1.a_T`, but cycled their executable
`character` descriptors from `(C,G,T)` to `(G,T,C)`.  Applied the same even
three-cycle to the first three stored matrix columns and the corresponding
pivot values, and synchronized the embedded/sidecar sections.  No primitive
witness, graph, Fourier value, probability, determinant formula, later column,
or verifier source was changed.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 materials/src/verify_k3p.py
```

Exit status: 0.  The run printed the Jacobian, tangent, margin, and sidecar PASS
lines and ended with `ALL K3P CHECKS PASSED`, even though the three displayed
names no longer described the derivatives computed beneath them.  A three-cycle
preserves determinant sign, and cycling the pivot coefficients with the columns
preserves the assembled tangent vector.  This experimentally confirms the
semantic-binding blind spot; it does not alter or disprove the unmutated
determinant or tangent, both of which were separately reconstructed.

## PDF checks

The rebuilt PDFs were not expected to be byte-identical because the TeX engine
and metadata are environmental.  Their extracted text matched exactly under
the packet's `pdftotext -layout` comparison.  Separately, all 19 main-paper
pages and both pages of each support PDF were rendered and inspected at high
detail.  No missing figure, clipping, broken glyph/equation/table, unresolved
cross-reference, or content-changing rendering defect was found.
