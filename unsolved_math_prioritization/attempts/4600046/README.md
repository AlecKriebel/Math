# Cellular periodicity: accepted restricted partials

Problem 4600046 / AMR-045-0046 remains unresolved for unrestricted full-shift cellular automata. The shared five-route budget stays exhausted at 5/5. This packet adds zero proof-search routes. It publishes six restricted propositions accepted, after the empty-routing-set radius repair, by an AI-assisted independent mathematical audit. No novelty, exhaustive worldwide literature status, conventional human peer review, journal acceptance or formal proof-assistant verification is claimed.

Read current/REPORT.md and the complete byte-preserved current/AUDIT_REPORT.md. The model is a nonempty finite alphabet, dimension d >= 2, the full shift over Z^d, and one finite translation-invariant local rule. Periodic means finite shift orbit, equivalently membership in the union of Fix(n Z^d). One nonzero period vector alone is insufficient. A and B use the actual specified fixed quiescent symbol q; C has no such assumption.

- A asks whether injectivity on periodic configurations implies surjectivity on q-finite configurations.
- B asks whether surjectivity on q-finite configurations implies surjectivity on periodic configurations.
- C asks whether global surjectivity implies surjectivity on periodic configurations.

All three remain unresolved here in their unrestricted forms. Onto periodic configurations allows enlarged preimage periods and does not require onto each same-period torus.

## Exact accepted mathematical scope

1. The exact torus-collar criterion characterizes when a q-finite target has a finite preimage, assuming periodic injectivity. It does not prove that the required collar exists.
2. The ternary marker rule is bijective on F_2. Its inverse is continuous at every point of F_2 but not uniformly continuous and has no continuous extension to the full shift. The same rule is not onto F_0. This is not a counterexample to B.
3. The fixed-fibre 2r boundary bound follows from global surjectivity via the declared Garden-of-Eden pre-injectivity theorem. It gives zero entropy for a grouped periodic fibre, not a periodic point.
4. In the fixed-control, one-successor XOR family, global surjectivity is equivalent to exclusion of finite directed cycles for every control configuration. For an n-periodic target and R = max({1} union {infinity norm(s): s in S}), every power of two m > R n^(d-1) gives an mn-periodic lift. Control preservation, exact XOR equations, strict inequality and period enlargement are retained.
5. Periodic injectivity gives q-finite surjectivity in that same family at the actual q = (c_0, beta_0), including beta_0 = 1. Together with the preceding result this proves A/B/C only within the stated family.
6. Exposed-vertex permutivity gives periodic lifts with transverse period n and longitudinal T divisible by n, with T <= n |A|^(w n^(d-1)), in unimodular coordinates. This settles B and C in that subclass; it does not assert A. The singleton-neighborhood and singleton-alphabet cases are included.

Every universal statement relies on its written mathematical argument. Finite enumeration certifies no arbitrary full-shift antecedent, no infinite-graph existence theorem, no unrestricted A/B/C implication and no literature-openness claim.

## Correction, provenance and exclusions

current/CORRECTION.patch is the exact contextual mathematical repair. It replaces an undefined inner maximum when S is empty by a maximum of a set containing 1. An empty S gives the identity signal rule. Locally, the patch applied to the original authored report with zero fuzz and no offset and produced the audit's accepted corrected bytes. Publication-only prose edits then removed nonmathematical bookkeeping and updated acceptance status without changing mathematical content; current/PUBLICATION_EDITS.md explains this without repeating excluded details.

The full audit is historical evidence and is preserved byte for byte. Its references to the original checker, input snapshots, manifests and historical run files describe the original audit; those files are not dependencies of public reproduction. The old assertion-based checker was unsafe under -O and -OO and is omitted. Superseded full reports, original private-input manifests, unsafe input/audit harnesses and historical run receipts are omitted. Their replay stages are explicitly NOT_RUN. Frozen originals remain unchanged locally.

The adapted current/verify_partials.py retains the independent mathematical solvers and eleven actual mathematical mutations. Only public authored-input paths/pins, isolated runtime requirements and scope reporting were changed. It verifies four public authored/provenance inputs. The adapted current/verify_correction.py checks the unique mathematical patch context after editorial edits, reverses and reapplies that substitution in memory, and recovers the current clean proof exactly. It does not need the omitted original report. Both adaptations have authored code patches.

historical/SOURCE_REVIEW.json records Jarkko Kari's Cellular Automata, Spring 2026, public URL https://users.utu.fi/jkari/wp-content/uploads/sites/1251/2026/02/fullnotes.pdf, PDF size 1,332,765 bytes and SHA-256 f75bb1abe3102afe2d2e3e32fb6a2a69d441034c0b8224e9c40b2e4793e22bb9. It records reuse of the source retrieved 2026-10-09T00:42:31.183721+00:00 and the actual visual/text inspection scope. This publication performs no new download or literature search. The Garden-of-Eden dependency and the independent justification of the elementary counting inequality remain explicit in the full audit. Other mentioned literature is not silently treated as a proof dependency.

No source PDFs, images, extracted source text, external dataset contents, private sources, private coordination, identifying metadata for excluded private files, QUEUE or unrelated repository changes are delivered. The fixed examples are authored mathematical examples.

## Public reproduction and trust

Authenticate BOOTSTRAP.py against the independently reviewed SHA-256 in the draft PR description, then copy the authenticated bootstrap outside this packet. Use trusted CPython and its standard library, actual UID=EUID=1000, all delivered directories mode 0555 and files mode 0444:

    python -I -S -B /trusted/BOOTSTRAP.py --controls /path/to/packet
    python -I -S -B -O /trusted/BOOTSTRAP.py --controls /path/to/packet
    python -I -S -B -OO /trusted/BOOTSTRAP.py --controls /path/to/packet

Omit --controls for baseline verification. The external bootstrap authenticates the manifest, verifier and controls before execution. The exact recursive inventory rejects missing/extra members, special files, symbolic paths and hard links. The noncircular manifest binds every other delivered byte, excluding itself and the bootstrap; the independently reviewed external bootstrap binds the manifest. A hash learned solely from an untrusted packet is not independent authentication. Final replay receipts are kept outside the delivery and independently pinned in the PR description.

Each mode runs two positive checkers and eleven actual algorithm/hypothesis mutants: ignoring loops; ignoring cycle parity; odd or arbitrary-even cover multipliers; nonstrict radius bound; ignoring zero winding; a falsely uniform inverse radius; replacing the specified q; a thin fibre collar; omitting target phase; and dropping strict exposedness. Three-mode totals are six positive checker runs and 33 intended mathematical rejections. Their exact reasons are checked. Publication-integrity/schema/comparator controls are counted separately.

Each positive independent check covers 700 functional graphs and 10,552 binary targets; 1,296 routing patterns with 425 accepted and 871 rejected, 6,800 verified lifts and 1,632 odd base parities at m=4; stress covers up to 4,096 vertices; 729 marker targets with independently brute-forced unique support fibres; four expanding-window inverse witnesses; specified beta_0=1; 7,928 collar incidences; and 239 exposed-vertex lifts, including exact absolute phase and a nontrivial unimodular basis. The second checker adds 274 empty-routing identity targets and six singleton-alphabet cases. Repeated hostile and integrity runs add no mathematical coverage.

The verifier requires complete raw mode-specific stdout/stderr equality without normalization, exact recursive JSON types, exact exits, identities, counts and rejection reasons. It rejects empty, skipped, altered and malformed suites. Hostile imports must leave full baseline bytes unchanged. UID1000 create, append-open and unlink probes must physically fail. Every delivered byte must remain unchanged before/after. POSIX modes protect against accidental writes, not deliberate owner chmod or root. CPython and its standard library are execution trust dependencies. Local staging additionally uses GNU patch and Git; public verification uses neither.
