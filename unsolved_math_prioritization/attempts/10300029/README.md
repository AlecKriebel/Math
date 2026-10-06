# Finite-radius left-orderability: audited partial

Problem 10300029 / AMR-102-0029, catalog rank 845, Calegari Question 8.6.

**Overall status: unsolved. Three substantive approaches of five used.**
The exact frozen author version is accepted as a credited, scoped partial after
an independent AI-assisted audit. No correction was required. Start with the
[author's result](author/RESULT.md), [full audit](audit/AUDIT.md), and
[acceptance report](audit/ACCEPTANCE.json).

## What is established

- A fixed two-generator marking of the P(-2,3,7) knot group and its sufficiently
  long integer fillings refute a universal finite positive-cone radius: the
  filled closed hyperbolic groups are non-left-orderable but pass each prescribed
  local test once the filling is sufficiently long.
- Infinite girth of the Weeks group refutes a manifold-only bound required to
  work uniformly over every finite marking. This does not settle a separately
  prescribed preferred-marking convention.
- A computable sufficient radius for a supplied marking is equivalent to
  left-orderability decidability on the promised effective input class.
  Uniform word-problem solving is available for promised finite 3-manifold-group
  presentations by the cited Aschenbrenner--Friedl--Wilton result.

The exact local multiplication condition requires kernel exclusion through
length 3r. A finite positive cone is not a certificate of global left-orderability.
A complete positive semidecision procedure, effective marked radius, preferred
marking formulation, and the full compound question remain unresolved by this
work. The deductions are credited to existing literature; no novelty or exhaustive
present-day openness is claimed. No human specialist review or formal verification
is claimed.

## Preserved records

Both original ZIP archives, their receipts, and all 13 archive members are
preserved byte-for-byte. Historical author fields saying independent review was
pending remain untouched; the separate acceptance record supplies the later
verdict for those exact bytes. The audit receipt's statement that no publication
had yet occurred is likewise historical.

The author archive contains five inert text/JSON files. Audit programs verify
bytes and metadata, never mathematical truth. No copied source PDF, extracted
source text, raw dataset content, or private coordination file is included.
Source titles, URLs, hashes, and inspection history are in the preserved source
metadata. Complete-corpus binding can be replayed against separately supplied,
byte-pinned inputs without publishing those inputs.

## Reproduction and trust boundary

Use Python 3's standard library with `-I -S -B`; optimized checks add `-O`.
Before executing any package code, authenticate `publication_bootstrap.py` against
its externally recorded SHA-256 and size, and obtain the external SHA-256 for
`PUBLICATION_MANIFEST.json` from the draft PR verification receipt. Neither a
self-consistent replacement manifest nor a hash supplied by the untrusted package
establishes authenticity.

After external authentication, the bootstrap accepts an absolute package path and
the external manifest digest, verifies the exact tree (including symlink rejection),
all files, both original archives, every member, and all manifest/receipt links.
The `--replay` option executes only authenticated audit code in a temporary relocated
tree, runs normal and optimized modes, and checks 46 rejected command-line cases
and 22 structural/JSON cases per audit-suite run. The suite also exercises original
and relocated positives and hostile import paths.

The `--corpus CATALOG PROBLEMS REPORTS` option runs complete-record source binding
in both interpreter modes. It emits only hashes, counts, and match results.
`publication_controls.py ROOT MANIFEST_SHA256 BOOTSTRAP_SHA256` separately tests
publication boundary failures after authenticating its own bytes externally.

Successful integrity checks are not mathematical proof checks. CI status is
reported separately for the exact PR head; no workflow runs or status checks is
not a passing CI result.
