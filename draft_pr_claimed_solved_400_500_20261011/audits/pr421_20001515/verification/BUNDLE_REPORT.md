# Verification delivery preparation report

The PR421 / 20001515 standalone delivery passed all preparation checks. Bundle
preparation completion estimate: 100%; two fresh sequential whole-paper and
package adversaries remain required before publication. Original author budget
is 1/5 unchanged; zero new proof-search turns were used.

The delivery preserves the exact thirteen-file layout from source head
`d5bf8b5a25cabb177433338fae60af52ebfecf1c`, replacing only the three accepted
program paths. All other bytes, including the pinned written proof and saved
historical output baselines, are unchanged. Every original source receipt
length/hash was verified before copying and rechecked after execution. Original
unsafe checker programs and all peer checker programs are omitted. Their
historical source hashes appear only in provenance.

The standard-library driver has no bare assert gates, hard-pins all thirteen
current packet files, validates the manifest and positive whitelist, and rejects
unlisted files/directories and symlinks. It executes copied programs with
`-I -S -B`, in normal and `-O` modes, using an ordinary isolated standalone
namespace. The accepted scripts assume standard unshadowed builtin
`AssertionError`; universal equivalence under foreign embedding or builtin
rebinding is not claimed. Inputs to every launch retain the proof-relative
layout and writable output directory.

Two full driver runs, normal and optimized, returned PASS. Each run performed
six clean direct program launches; every saved result was deleted first.
Canonical stdout was compared to the correct author, geometry summary, or
algebra baseline. The geometry and algebra full result files had to be newly
written and match both the full JSON values and historical output bytes. Normal
and optimized output agreed. The author program prints checks.json's JSON but
does not write that file. Both driver modes produced identical baseline,
control, and relocation evidence.

Per full driver run, proof/script/baseline SHA tampering was rejected in three
copied bundles. Seven meaningful data controls each ran in both modes: a
duplicate K square, a nonclosed Q square, the wrong involution b sign, deletion
of an actual cube-corner triangle, the wrong cube-side vertical sign, a wrong
inverse monodromy, and changed copied proof bytes. All fourteen launches raised
AssertionError before successful stdout or a result file. Mutation targets were
required to occur exactly once. No syntax, import, or missing-dependency failure
was counted as mathematical rejection. The scripts' own seventeen geometric
controls remain part of the accepted baselines.

Each full run additionally relocated the entire delivery to a directory with
spaces, launched the relocated driver under -O from outside that directory,
and reproduced six clean normal/-O program outputs there. All execution and
corruption fixtures were disposable temporary copies. Delivery and frozen
source files remained unchanged by execution.

Verification used installed Homebrew Python 3.14.6 at
`/opt/homebrew/opt/python@3.14/bin/python3.14`, without a virtual environment or
third-party dependency. The Apple `/usr/bin/python3` launcher was unavailable
because this host's Xcode license has not been accepted; even its --version
command failed. No host license, setup, or configuration was changed, and no
successful Apple-launcher check is claimed.

EXECUTION_EVIDENCE.json preserves the reports and exact preparation snapshot
manifest/whitelist. Its run digest fields are explicitly historical: adding
execution evidence and the final log/report then regenerates the final
manifest/whitelist. This avoids self-hash cycles. A further fresh run of the
sealed final delivery and its independently computed final digests are supplied
to root outside this delivery. MANIFEST.json excludes itself and the whitelist;
the whitelist positively hashes MANIFEST.json and all other included files,
and omits its own self-hash. Authentication requires a separately trusted pin.

The dated PUBLICATION_ADDENDUM.md records the accepted current exact-source
observations, bounded qualified-priority decision, verified present route from
older tools, exact three-program optimization repair, and unavailable earlier
checker-provenance limit. It leaves frozen historical notes byte-identical.
The concrete mathematical claim is the explicit finite NPC construction for
the exact ab,bcb group. No firstness, minimum, virtual-specialness, external
human-review, or formal proof-assistant claim is made. Written proof remains
primary; the finite executable certificate is corroboration, not a global proof
or source/priority guarantee.

The positive public delivery inventory is confined to verification/ and listed
in PUBLIC_OUTPUT_WHITELIST.json. It contains no foreign PDFs/HTML, raw catalog,
private fixtures, tokens, bytecode, virtual environment, or other PR case.
Original content is licensed CC BY 4.0. Extensive AI assistance and unrefereed
status are disclosed. There were no Git/index/branch/remote mutations, releases,
sheet changes, or external communications by this delivery worker. No required
mathematical or publication claim repair was identified in this task.
