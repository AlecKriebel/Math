# Static adversarial audit of the referee-authored independent checks

Date: 2026-08-27
Scope: `independent_checks/README.md` and all seven Python checkers in
`independent_checks/`
Method: complete static reread only; no checker, package producer, package
verifier, imported package code, or Python byte-code compilation was run
during this audit.

## Disposition

After the repairs recorded below, I found no remaining concrete mathematical
or interval-soundness defect in the frozen source.  The primary referee's first
sandboxed attempt stopped at a checker-only class-ID assertion in the four-port
script (item 6).  Its corrected run passed the full four-port checker and then
stopped at a second checker-only schema error in the restoration census: a
legacy forest parent hash was incorrectly compared with an active K3P row hash
(item 8).  I did not execute or compile either run or either correction.  The
seven scripts are now statically suitable for another clean corrected run in
the documented offline, credential-free sandbox.  This is **not** a passing
computational result: the repaired restoration path and the still-later probe
assertions have not yet been observed to pass.

The checks are genuinely useful independent spot checks, but they do not by
themselves meet every exhaustive part of the neutral referee prompt.  In
particular, they do not redo the `405,216 -> 40` four-port filtering, the JC
primitive/completion census, all-row probe semantics, or topology discovery
for the Krawczyk witness.  Those are coverage boundaries, not defects in the
claims the scripts now make.

## Frozen files

The following SHA-256 values were reread after the final source edit.  The
seven Python files are frozen at these digests; the README digest is included
to bind the stated coverage boundary and commands.

| File | Lines | SHA-256 |
|---|---:|---|
| `check_three_leaf_geometry.py` | 345 | `eaf0c29e630f2e53da34544b9d03ccf6d163e350f38302d6ba9b41d91d209a29` |
| `check_bridge_gluing.py` | 155 | `1be1d2a43330ed709adb4618c5062dd80e42af2ea6256fbf368632a916472755` |
| `check_jc_endpoint_certificate.py` | 764 | `4541f41475ebe2299019c96727133b2fd729fdb9f538d4e2fab3640a6856c158` |
| `check_four_port_witnesses.py` | 881 | `54e83dc6442308c55524ca8246a4b643a3663abdce3cc97032fee8cea64296c6` |
| `check_restoration_probe_census.py` | 540 | `511c0d5832c38c2ee21eb8a82d1aad8a20f40d687364bf7121c83d0502c4119f` |
| `check_probe_semantic_samples.py` | 860 | `94b55315840d5bd631701e45ce1b273e6c8c419d9d90eda59a65cf0eeaa8e92f` |
| `check_krawczyk_box.py` | 491 | `d224151afd9bc9fc00833eb2d3a487bfe951d706eaa6e6683b028dbad07c95ba` |
| `README.md` | 81 | `0314091f40d1b503fe8b4d8421b8a2e5fac9975371b54d79ad64a103ce8b1db9` |

## Defects and hazards caught by static review or the first run and repaired

### 1. Four-port quotient originally used the wrong automorphism category

Severity: high for the referee spot checker; caught before any result was
generated.  The first draft computed automorphisms of the rooted DAG.  That is
exactly the historical H21-01 category error identified by the article at
`package_copy/proof_package/manuscript/sections/08_primitive_bounded.tex:273-278`:
the quotient requires root-suppressed semi-directed mixed-graph
automorphisms, with arrowheads preserved, and target automorphisms conjugated
into the displayed frame.

The final repair is at `check_four_port_witnesses.py:55-136`: it suppresses the
root, represents each mixed edge by a bipartite incidence vertex, records the
arrowhead flag on each incidence, pins leaf labels, and enumerates the induced
port group.  Lines 231-251 independently recover the base target group and
check `pi G pi^-1` in every displayed lock frame.  Lines 253-296 then form the
double cosets and compare the independently obtained fourteen-part partition
with the stored quotient only as a post-check.  Static comparison with the
package clean-room construction found the action and composition convention
consistent.

### 2. Four-port compiler silently had the wrong semantics if raw signatures repeated

Severity: potentially high but conditional; this was a latent fail-closed
hazard, not evidence that the six frozen literals actually contain a
duplicate.  `compile_variant` gives each effective edge signature one
coordinate.  If two raw edges had the same switching signature, merely mapping
both to that coordinate would add exponents and would not equal a
single-edge-coordinate compiler unless an explicit product-coordinate collapse
were implemented.

The final repair is the guard at `check_four_port_witnesses.py:423-426`, which
requires `len(raw_signatures) == len(set(raw_signatures))` before the coordinate
map is built.  Thus the bounded suite either has the intended one-edge/one-
signature form or terminates.  The primary referee reports that the subsequent
corrected run passed the complete four-port checker, so this guard was observed
to hold for the six frozen literals.  I did not execute that run.

### 3. The Krawczyk interval slice did not originally bind every frozen coordinate

Severity: medium.  The first draft checked the pivot boxes but did not require
each nonpivot interval to be the point interval at its frozen parameter value.
A wrong nonpivot box could therefore fail to enclose the actual frozen slice
whose center residual and point Jacobian were used.

The final assertions at `check_krawczyk_box.py:371-389` now bind all 64 point,
scale, and interval entries: pivot boxes equal the scaled center-radius boxes,
every nonpivot point equals its frozen scale, every nonpivot interval is that
exact point interval, and every point lies in its interval.  Lines 445-447 also
require each rank-minor column list to contain 15 distinct in-range columns.

### 4. Restriction replay originally compared only node and edge sets

Severity: medium.  The first draft of the identity restriction check could
accept the same incidence sets with altered labels, roles, or arrowhead sets.
That would be insufficient for a labelled semi-directed restriction.

The final check at `check_probe_semantic_samples.py:397-401` requires full
attribute-dictionary and mixed-edge/arrowhead-dictionary equality.  The
two-port sample is additionally bound to the parent inventory and base anchor
at lines 777-786.

### 5. Census rows originally had weaker cross-reference bindings

Severity: low to medium.  The final census now binds each restoration
`proof_id` to its asserted proof kind, binds every active restoration row in
order to the sealed frozen-forest identity, and checks the corrected legacy
parent relation and exact `32 x 8` fanout
(`check_restoration_probe_census.py:112-276`).  In the probe path it validates
the compressed registry digests and payload hashes, reconstructs the exact
one-port anchor Cartesian order, binds every parent inventory row to its
one-port equality record and candidate profiles, reconstructs the exact
two-port Cartesian order and site IDs, and compares origin and reverse-relation
censuses to the coherence certificate (`:278-482`).  These repairs prevent
internally self-consistent but cross-category or cross-parent substitutions.

### 6. The first run exposed a source-local class-ID mistake in the referee quotient check

Severity: blocking for the referee checker, but not for the package theorem or
its exhaustive replay.  The original assertion at
`check_four_port_witnesses.py:158` required 40 distinct *bare* `class_id`
numbers among the 40 post-quadratic residue members.  Static inspection of the
registry and its producer/verifier shows that `class_id` is enumerated afresh
inside each source lane: the package verifier's class key is explicitly
`(source_index, class_id)` at
`package_copy/proof_package/four_port_atlas/full_universe_replay/verify_full_four_port_replay.py:330-355`,
and raw quotient members are keyed by
`(source_index, target_index, permutation)` at lines 400-410 and 496-505.

The frozen data contain 40 residue members and 40 distinct source-local class
keys, but only 34 distinct bare class-ID numerals: 28 occur once and 6 occur
twice across different source lanes.  All 40 raw
`(source,target,port-permutation)` keys are distinct, followed by the expected
38 ordinary members and 2 sink swaps.  Thus the observed stop was solely a
referee-checker schema error; it does not indicate a package census,
classification, or quotient defect.

The corrected fail-closed census is at
`check_four_port_witnesses.py:157-174`.  It checks all four facts separately:
40 members, the exact `34 = 28 singleton + 6 doubleton` bare-ID census, 40
distinct source-local class keys, and 40 distinct raw quotient keys.  No
package or README edit is implied.

### 7. The derived-quotient post-check originally dropped source and target IDs

Severity: low to medium checker-binding defect; found during the required full
reread of the affected quotient path.  The independent orbit construction used
the correct raw triple, but the first draft appended only each orbit's set of
port permutations and compared that to only `raw_members` in the derived
artifact.  That projection is not injective: the two L21a, two L21b, and two
L23 orbits occur in three repeated permutation-set groups.  Swapping their
stored source metadata could therefore evade the stated partition post-check.

The final comparison at `check_four_port_witnesses.py:253-296` carries
`(source_index, target_index, sorted raw_members)` on both independently
computed and stored sides.  Orbit sizes are correspondingly taken from the
third tuple entry at lines 277 and 315.  This is additional checker hardening;
it does not diagnose a defect in the clean derived artifact.

### 8. The restoration census confused legacy forest hashes with active K3P hashes

Severity: blocking for the referee checker, but not for the restoration theorem
or package replay.  After the corrected suite passed the four-port checker, it
stopped at the old `check_restoration_probe_census.py:185`, which required each
depth-two `parent_first_row_sha256` to be an active layer-one `row_sha256`.
That is not the ledger schema.  The depth-two field deliberately retains the
parent row hash from the frozen model-independent forest, while the active K3P
layer-one `row_sha256` is recomputed only after K3P status, proof, and graph
bindings are added.

The producer makes this distinction explicitly: `forest_identity` copies the
frozen hash into `legacy_row_sha256` and retains the frozen depth-two parent at
`package_copy/proof_package/restoration/regenerate_k3p_restoration.py:422-440`;
the active status fields are added at `:687-710`; and only then is the active
row hash computed at `:711`.  The independent package verifier reconstructs
depth-two rows through the frozen first-row hash at
`package_copy/proof_package/restoration/verify_k3p_restoration.py:850-890`,
binds active records to the same frozen identity at `:1105-1149`, and requires
the exact 32-parent/eight-child relation at `:1201-1209`.  The manuscript says
the same thing: all 32 inherited continuations are already terminated by active
K3P quartics, while their 256 depth-two children are retained only as a
redundant legacy-forest replay
(`package_copy/proof_package/manuscript/sections/09_restoration_words.tex:10-15,36-54`).

Read-only inspection gives the expected disjoint semantics: 36,568 active
layer-one rows are all `separated`; among their frozen statuses, 36,536 are
`separated` and 32 are `continuation`; the 256 layer-two rows have legacy status
`separated`, active status `redundant_verified`, and
`legacy_full_forest_only=true`.  Each of the 32 frozen continuation hashes has
exactly the insertion-index set `{0,...,7}`.  Thus the observed stop is solely a
referee-checker schema error, not evidence of a producer, verifier, ledger, or
manuscript defect.

The repaired checker now hashes and reads the frozen forest, binds all 36,824
active rows to its exact ordered identities, keys depth-two parentage by the
layer-one `legacy_row_sha256`, checks both legacy and active status censuses,
requires the 32 early-termination quartics, and requires exactly eight distinct
source insertion indices for every continuation parent
(`check_restoration_probe_census.py:112-276`).  The required reread of the
previously unreached probe path also led to the all-row anchor, parent/profile,
site-index, origin, and reverse-relation bindings described in item 5.  The
README coverage row was updated accordingly.  No package-file change is
implied.

## Script-by-script mathematical and code review

### `check_three_leaf_geometry.py`

The inverse Fourier round trip and the identities converting the CT
composition inequalities into principal transition inequalities are exact
(`:149-165`).  The six tree/sunlet circuit pullbacks are checked
coefficientwise against the displayed factorizations (`:174-186`), and the
paired cancellation identities used for strict separation are exact
(`:188-205`).  The eight-term H14 polynomial is pulled back to zero under all
six leaf permutations; its primitive linear coefficient is coprime to the
remainder; the three cyclic images meet at the same strict CT point with rank
14; and the H14 gradient there is nonzero (`:227-292`).  Together with
irreducibility, containment, and dimension 14, those facts justify equality of
the three Zariski closures and their common smooth hypersurface germ.  The
six-dimensional cherry determinant and both positive-branch compositions are
checked exactly (`:294-335`).

Residual boundary: the 5,000 numerical separator trials at `:125-141` and
`:207` are empirical and ancillary.  The all-composition-margins-zero branch
records the exact product identity at `:203-205`, while the inference
`0 < p < 1` and hence `p != p^2` remains elementary handwritten reasoning.  An
optional further hardening would assert an explicit polynomial combination of
the three margins equal to `p^2-p`; this is not needed for the validity of the
displayed human argument.

### `check_bridge_gluing.py`

The unmarked one-sector exponent matrices have exact determinant `-2`, and
the three-sector blocks determinant `-8`, for the tested degrees 3 through 16
(`:29-64`).  The positive pair-anchor inverse, degree-two stabilizer, and
sectorwise gauge cancellation are exact (`:66-103`).  The capped-gluing trials
use `Fraction` arithmetic, and the central CT lower-bound decomposition is
symbolically checked (`:105-143`).

Residual boundary: the marked case at `:79-83` constructs an identity matrix
after adopting the manuscript's one-character-anchor interpretation; it does
not independently derive that marked exponent matrix from a topology.  The
topological marked-or-degree-at-least-three dichotomy is expressly conditional
(`:144-146`).  The 2,000 cap cases and degrees through 16 are representative;
the general inequalities and arbitrary-degree extension still consume the
short handwritten pattern argument.

### `check_jc_endpoint_certificate.py`

The checker locally expands the JC switching mixture as sparse rational
polynomials (`:152-185`).  Its multivariate power-to-Bernstein conversion
`b_beta = sum_{alpha<=beta} c_alpha binom(beta,alpha)/binom(n,alpha)` is correct,
and strict open-cube positivity follows because every Bernstein basis function
is positive in the open cube (`:193-376`).  Every supplied record is normalized
and rebuilt, with Delta/Gamma reconstructed rather than accepted from a stored
Boolean (`:387-525`).  The four 4-by-4 blocks, all nonzero 2-by-2 minors up to
sign, four manuscript minors, three identities, and the strict `f1`
decomposition are rebuilt exactly (`:558-675`).  The stored factor strings and
Bernstein extrema are not used.

Residual boundary: the checker begins with the 77 stored switching-signature
records and retains their normalization and case labels, which it then checks.
It does not regenerate witness graphs, the primitive completion grammar, the
808,642 binary-word census, or the 204 one-active minors (`:737-755`).  It also
uses the same factor/Bernstein proof family as the producer, although in a
separate implementation.  Thus it is a strong independent algebraic replay,
not an independent completeness proof for the graph census.

### `check_four_port_witnesses.py`

After the automorphism repair, the quotient uses the required
root-suppressed, arrowhead-preserving mixed-graph category (`:55-136`), verifies
displayed-frame conjugation (`:231-251`), and independently obtains 14 double
cosets of sizes nine times 2 and five times 4 from the 38 ordinary records,
with the two sink swaps kept separate (`:139-324`).  The local switching
compiler expands inheritance factors and literal Fourier monomials exactly
(`:335-473`).  Three quartics have coefficientwise-zero target pullback,
nonzero source pullback, and a fresh strict rational source witness
(`:798-812`).  The H21 identities express the eleven selected outputs through
ten rational generators after saturation by factors nonzero on strict
`D_+` (`:645-683`); the two ordinary-sunlet compressions give the stated 12-
and 10-generator upper bounds (`:686-779`, `:851-854`).

Residual boundary: the quotient starts from the stored flat 40-row
post-quadratic residue.  It does not reconstruct the preceding 405,216 cases
or prove that the lock literals arose from the complete grammar; sink swaps are
checked and separated but not re-derived from the full universe.  The fresh
sample ranks are lower bounds only, as the script itself says at `:868-872`;
the target upper bounds come from the exact rational/sunlet factorizations.
The primary referee's corrected run subsequently passed this complete checker,
including the raw-signature uniqueness assertion; I did not run it myself.

### `check_restoration_probe_census.py`

Every ledger row is streamed.  Ledger bytes, canonical row/record hashes,
ordered roots, counts, proof/reference membership, exact frozen-forest identity,
the legacy/active status split, the 32-by-8 legacy parent fanout, anchor and
parent-profile cross-references, full one-/two-port Cartesian order, site IDs,
origin counts, endpoint-map compatibility, and exact rational parameter margins
are checked (`:112-276`, `:278-482`).  No package module is imported.

Residual boundary: this is deliberately a binding/census audit.  It does not
regenerate the restoration forest or recompute the stored quartet, tree-
sunlet, or quartic polynomial semantics (`:526-531`).  In particular,
`validate_transport_binding` at `:75-102` verifies an injective endpoint map
and triangle bookkeeping, not full role/label/arrowhead isomorphism; the latter
is exercised only by the companion five-row sample.  The strict-witness check
recomputes the physical CT/inheritance margins exactly and requires the stored
evaluation to be nonzero, but it does not independently reevaluate every stored
polynomial.  The checker now validates the top-level manifest/certificate
self-hashes and binds the frozen forest, restoration proof registry, separation
registry, and all ledger bytes to their advertised hashes.  The outer
sealed-package audit remains responsible for the initial byte identity of those
self-hashed top-level documents.  These are disclosed coverage boundaries, not
defects in the binding claims made here.

### `check_probe_semantic_samples.py`

The script reconstructs rooted graphs from public site profiles, suppresses the
root into a mixed graph, preserves arrowheads, checks labelled isomorphism or
the precisely localized ordinary-triangle ambiguity, reconstructs displayed
quartet sets, compiles literal three-leaf Fourier maps and all six circuits,
and validates parent restrictions (`:149-434`, `:437-617`).  The selected
tree/sunlet row has coefficientwise-zero tree circuits, six nonzero sunlet
polynomials, and a fresh exact isotropic point with positive sum of squares
(`:732-775`).  The two-port sample reconstructs its parent and child, checks
both restrictions, and checks that the child transport restricts to the parent
transport (`:777-834`).  `ast.literal_eval`, not `eval`, is used for frozen
tuple encodings.

Residual boundary: the five row indices, public candidate profiles, and stored
witness records are retained.  Five semantic rows exercise all four one-port
statuses and one two-port equality, but cannot establish the claimed semantics
of all 574,535 rows (`:836-852`).  The selected two-port sample does not also
rebuild its reverse-order parent certificate.

### `check_krawczyk_box.py`

All interval endpoints and arithmetic decisions use `Fraction`; the decimal
module is used only to render summaries (`:52-127`, `:335-352`).  Interval
multiplication considers all four endpoint products, and division rejects an
interval containing zero.  Both literal maps and analytic Jacobians are
rebuilt directly from the two DAGs (`:205-298`).  The final full slice binding
is at `:355-389`.  The Krawczyk image at `:421-438` is the standard
`x0-CF(x0) + (I-CJ(X))(X-x0)` enclosure; strict self-inclusion and an infinity-
norm contraction below one prove existence and uniqueness inside the supplied
15-dimensional scaled pivot slice.  The two interval rank certificates use
exact Neumann bounds (`:440-460`), and all physical margins are exact and
strict (`:313-332`, `:462-466`).

Residual boundary: the certificate still supplies the rational center,
pivots, scales, radius, selected rank columns, and literal DAGs.  This check
does not discover the witness topology or prove uniqueness outside the frozen
15-dimensional slice; the output states that scope correctly at `:476-482`.

## Fail-closed behavior, independence, and write confinement

- Every checker rejects optimized Python before relying on assertions.  The JC
  checker additionally uses an explicit `CheckFailure` path for sign failures.
  The only caught `AssertionError` is the bounded H21 parameter-convention
  search at `check_four_port_witnesses.py:843-850`; the script still fails if
  no convention satisfies all identities.
- No checker imports a producer, verifier, atlas module, or another referee
  checker.  There is no subprocess, network, shell, socket, dynamic code
  execution, or unsafe `eval` call.
- Inputs are read only beneath the supplied `--package-root` (or no package
  input for the two self-contained symbolic scripts).  Outputs are the seven
  named JSON files beneath the supplied `--output-dir`; the JC checker uses an
  atomic temporary file in that same directory.  The programs do not enforce
  that an arbitrary caller-supplied output directory is inside the copied
  workspace, so the documented OS sandbox remains the confinement mechanism.
- Except for the independently rebuilt formulae, the principal retained inputs
  are accurately disclosed in `README.md:16-24`.  A matching content hash is
  treated as a binding check, not mathematical proof.

## Static recommendation and unresolved execution item

Run the corrected frozen suite cleanly with the README commands in the isolated
copy, preserve the complete transcript and output hashes, and treat any
exception or assertion failure as a failed check.  A clean rerun is justified:
both observed stops have been traced to referee-checker schema mistakes, not
package failures.  The four-port correction was subsequently observed to pass.
The restoration correction matches the producer, independent verifier,
manuscript, frozen forest, and active ledger semantics, and now checks exact
legacy parentage rather than weakening the gate.  The remainder of the census,
especially the newly strengthened one-/two-port Cartesian and parent/profile
bindings, is still unobserved.  No passing claim should be made from this static
correction alone.
