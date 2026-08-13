# Final manuscript rereview

Date: 2026-08-09
Scope: patched active sharpness manuscript, exact verifiers, certificates,
submission artifacts, and documented release commands
Verdict: **HOLD**

## Executive verdict

The patched mathematical submission passes rereview.  The manuscript repairs
are correct, the independent reducer now implements the narrow
`sd_0` convention literally, the final strict-reducer script and certificate
hashes are exact, both mathematical implementations pass, and the current
source rebuilds the submitted ten-page PDF byte for byte.

The release is not yet eligible for `SUBMISSION_READY_PENDING_MANIFEST`.
Beyond the intentionally pending root manifest, two P1 release defects and two
P2 supporting-record defects remain:

1. the release driver still fails after a valid manifest because its README
   scope check is whitespace-sensitive;
2. both submitted ZIP archives lag the active canonical files;
3. the sharpness gate review still states the deleted broad reduction
   convention; and
4. its nested historical manifest no longer hashes the current gate review.

The missing root `MANIFEST.sha256` is treated only as the requested procedural
pending item and is not scored as a mathematical or release finding here.
No manuscript, verifier, certificate, PDF, archive, metadata, or release file
was edited during this rereview.

## Audited snapshot

The final strict-reducer audit anchor supplied by the author matches the active
tree:

```text
93a29ea6fdd1eba1671cf720a3929c2e2cab6ef5882c89a355d7cef04406c639  reproducibility/independent/verify_sharpness.py
38266537a7966d83bdb94c6fb90fa68f93fbd227b82579f1bf311005925366d7  reproducibility/independent/expected_certificate.json
```

Other relevant active hashes at the final check were:

```text
d1a24039d0109151aaed5347c0e781c6f48fed486a2006496d3e2e29b1f89b87  source/paper/main.tex
b616673aede01f50d951e702b3727fbea2772e62ace9a5d4752a79608071c405  reproducibility/verify_release.py
65f5a54f6858b091546bc2221cb36d77bf5e24722bb79d6420b98f429dadc810  submission/Weakly_Tree_Child_Level2_JC_Ambiguity.pdf
c44d96db475a287dfeef1cd2d9ff8af4f7673acec4719e6509518c303a6e4dcc  submission/Weakly_Tree_Child_Level2_JC_Ambiguity_Source.zip
e8b5b568b53127665e790ad58ebcb4f75a5bb286957ca73a9e7d7b3aa3ce0be8  submission/Weakly_Tree_Child_Level2_JC_Ambiguity_Reproducibility.zip
65cfe9411bef9c89c7606f92879a39628c94347c9e11d297c11992c15b45e7ce  repair/reviews/SHARPNESS_GATE_REVIEW.md
```

## Exact replay evidence

- The independent verifier was run directly with `PYTHONHASHSEED=0`, `1`, and
  `987654`.  All three runs returned `PASS final_verdict=PROVED`, produced hash
  `38266537...66d7`, and were byte-identical to one another and to
  `expected_certificate.json`.
- `reproducibility/verify_math.py` passed with NetworkX 3.6.1 and SymPy 1.14.0.
  It replayed the primary symbolic implementation, checked the three active
  independent locks, regenerated the independent certificate, and ended with
  `VERIFIED: both exact mathematical implementations passed`.
- Removing the reducer cleanup changes no mathematical certificate field.
  After deleting `.implementation.script_sha256`, the old and new canonical
  certificates compare identically.  The active certificate records the
  correct new script hash `93a29ea6...c639`.
- The active release command fails first on the intentionally absent root
  manifest.  In an isolated copy, generating a valid manifest advances the
  driver to its scope gate, where it fails for the independent P1.1 reason
  below.
- The current canonical source rebuilds the submitted PDF byte for byte at
  SHA-256 `65f5a54f...c810`.  The public paper copy and its public checksum have
  the same hash.
- All ten PDF pages were rendered and visually inspected.  There are no
  undefined references, clipping, collisions, illegible formulas, or layout
  defects.  All twenty PDF font resources are embedded.  The build log has no
  substantive warning, overfull box, underfull box, or missing-character
  message.
- The submitted reproducibility ZIP is internally hash-consistent and its old
  wrapper passes, but it certifies the superseded `389d1ec6...b04b` script and
  `c6478dab...bae1` certificate.  Internal validity does not make it the active
  final package.
- The deterministic archive builder passes in isolation.  Rebuilding from the
  audited snapshot changes both stale submission archives as described in
  P1.2.

## Disposition of the prior P1/P2 findings

The substantive repairs requested in `MANUSCRIPT_FINAL_REVIEW.md` are correct:

- **Prior P1.1:** the final root manifest remains intentionally pending.  This
  is not scored here, but the complete release command must pass after the
  rereview and all repairs are frozen.
- **Prior P1.2:** fixed at `source/paper/main.tex:578-611`.  The context now
  assumes nonempty `X`, restricts positivity to zero-total Fourier
  coordinates, and makes the analytic cherry inverse valid.
- **Prior P1.3:** fixed at `source/paper/main.tex:80-83,110-120,646-652`,
  `README.md:20-25`, and `docs/PRIOR_WORK_COMPARISON.md:27-32`.  The release now
  says explicitly that the example contains a triangle and does not settle
  the triangle-free weakly tree-child subclass.
- **Prior P2.1:** the active implementation is fixed at
  `reproducibility/independent/verify_sharpness.py:513-542`.  It suppresses the
  binary root once and performs no post-root cleanup.  Exact enumeration still
  gives five admissible LSA-valid rootings and two tree-child rootings for each
  network.  A supporting-review residue remains as new P2.1 below.
- **Prior P2.2:** fixed at `source/paper/main.tex:615-633`.  The manuscript and
  certificate both repeatedly replace labelled leaf 2 and preserve the
  labelled leaf-1 triangle separator.
- **Prior P2.3:** fixed at `source/paper/main.tex:547-558`; the proof now cites
  all five reconstruction formulas and names `J,K,M,N,O`.
- **Prior P2.4:** fixed at `source/paper/main.tex:127-130`.  The rendered PDF
  has `stacked-reticulation`, without an inserted space.
- **Prior P2.5:** fixed at `source/paper/main.tex:161-170` by an explicit stable
  ancestor definition.
- **Prior P2.6:** fixed at `repair/reviews/SHARPNESS_GATE_REVIEW.md:617-640` and
  `docs/PRIOR_WORK_COMPARISON.md:17`.  The active command and Sullivant dates
  are correct.
- **Prior P2.7:** fixed at `reproducibility/verify_primary.py:103-106`; the
  comment now says cycle rank two.

## P0 findings

None.

## P1 findings

### P1.1 — The post-manifest release command still fails its scope contract

**References:** `reproducibility/verify_release.py:85-103`;
`README.md:20-22`; `source/paper/main.tex:712-715`.

The release driver reads the README verbatim and tests

```python
if "unresolved, not refuted" not in readme:
```

The Markdown source wraps that phrase between `not` and `refuted`, so the
literal substring is absent.  In an isolated current-tree copy, a newly
generated valid manifest passes with `VERIFIED manifest`, after which the
driver raises:

```text
AssertionError: README does not preserve the positive theorem's unresolved status
```

This is independent of the missing active manifest: generating the manifest
does not make the documented release command executable.

**Exact repair:** normalize whitespace for both prose files before testing the
scope strings.  Replace the first two assignments in
`verify_scope_contract()` with:

```python
manuscript = " ".join(
    (ROOT / "source/paper/main.tex").read_text(encoding="utf-8").split()
)
readme = " ".join((ROOT / "README.md").read_text(encoding="utf-8").split())
```

The same repair was tested in an isolated copy: after manifest generation the
complete driver passed and ended with
`VERIFIED: all sharpness-release gates passed`.

### P1.2 — The submitted archives do not contain the active canonical files

**References:**
`submission/Weakly_Tree_Child_Level2_JC_Ambiguity_Source.zip`;
`submission/Weakly_Tree_Child_Level2_JC_Ambiguity_Reproducibility.zip`;
`reproducibility/build_archives.py:42-68`;
`docs/SUBMISSION_CHECKLIST.md:37-42`.

The active source is SHA-256 `d1a24039...b87`, but the source ZIP contains the
previous `main.tex`, SHA-256 `e27f5b93...734c`.  The reflow is PDF-neutral—the
current source still rebuilds the submitted PDF exactly—but the submitted
source archive is not the canonical source.

The active independent pair is script `93a29ea6...c639` and certificate
`38266537...66d7`, while the reproducibility ZIP contains script
`389d1ec6...b04b` and certificate `c6478dab...bae1`, together with the matching
superseded wrapper.  Thus a reader of the submitted supplement does not receive
the final audited implementation and locks.

**Required repair:** after P1.1 and both P2 items are final, run from the
release root:

```text
python3 reproducibility/build_archives.py
```

Then extract both rebuilt archives into clean temporary directories, check
their internal `SHA256SUMS.txt`, confirm every archived canonical file is
byte-identical to its active counterpart, run
`python3 reproducibility/verify_math.py` from the extracted reproducibility
archive, and rebuild the PDF from the extracted source.  Only then generate
the final root manifest.

## P2 findings

### P2.1 — The gate review still states the deleted broad reduction convention

**References:** `repair/reviews/SHARPNESS_GATE_REVIEW.md:61-76`, especially
lines 69-72; `reproducibility/independent/verify_sharpness.py:513-542`.

The review's “Locked conventions” section says that the standard reduction
suppresses unlabelled ordinary degree-two vertices after suppressing the root.
The manuscript and final strict reducer expressly forbid that step.  The note
at lines 642-647 acknowledges deletion of the old loop but does not correct the
earlier operational definition, so the same active report asserts both
conventions.

**Exact replacement for item 2 at lines 69-72:**

> The standard semi-directed reduction retains arrowheads precisely on edges
> entering reticulations, makes ordinary edges undirected, and suppresses the
> binary root once.  It performs no further degree-two cleanup or broad
> deletion of reticulation artifacts.

### P2.2 — The nested repair manifest has a stale hash for the gate review

**References:** `repair/reviews/SHARPNESS_GATE_REVIEW.md:659-660`;
`repair/independent/sharpness/MANIFEST.sha256:7`.

The gate review says that the nested manifest records its final hash.  That
manifest records `de5bd231...`, whereas the audited gate review is currently
`65cfe941...` and will change again when P2.1 is fixed.  The root release
manifest generator treats this inner manifest as an ordinary file and does not
validate its internal entries, so the stale assertion can survive a successful
root release gate.

**Required repair:** after applying P2.1, recompute the gate-review SHA-256 and
replace line 7 of `repair/independent/sharpness/MANIFEST.sha256` with that exact
digest.  Recheck every line of the nested manifest before rebuilding the
reproducibility ZIP.

## Mathematical and manuscript findings that pass

No mathematical regression was found.  The rereview reconfirms:

- the exact LSA, compatible retained-edge root insertion, `W_TC \ S_TC`,
  nonisomorphism, and non-ordinary-`T` certificates;
- strict root suppression and the effective root multiplier;
- Klein-four group law, orbit completeness, all six equations, localized
  irreducibility, dimension eight, and the positive physical sheet;
- the exact beta point, every strict `Theta_0` inequality, all Fourier and
  inverse-Fourier coordinates, and strict pattern positivity;
- both rank-eight Jacobian certificates and the inverse-function overlap
  argument;
- the meaning of full-dimensional regular overlap and the non-algebraic-
  exceptional genericity conclusion;
- the repaired cherry inverse, exact `+2` dimension increment, explicit
  leaf-2 all-taxa family, and persistence of topology classes and non-`T`;
- the narrowed scope and restrained bibliographic comparison; and
- the patched manuscript's notation, references, typesetting, and rendered
  ten-page PDF.

## Final binary verdict

**HOLD**

The theorem and manuscript are mathematically ready, and the absent final root
manifest remains only a procedural pending item.  The active release as a
whole is not submission-ready, however, because P1.1 and P1.2 prevent the
advertised command and submitted archives from representing the final audited
state, while P2.1 and P2.2 leave contradictory convention and hash records.
After those four repairs, regenerate both archives, write the root manifest,
and require the unmodified active command to end with
`VERIFIED: all sharpness-release gates passed`.
