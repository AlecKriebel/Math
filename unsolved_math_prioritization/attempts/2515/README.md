# Kourovka 21.6: full negative candidate for p = 2

**Current status: claimed solved; independent AI audit PASS. External specialist review and novelty assessment remain pending.** No human verification, editorial acceptance, originality or priority is claimed.

This is a complete candidate counterexample to the literal October 2026 formulation, rather than a finite-only obstruction. A countably infinite transitive finitary 2-group has no transitive subgroup whose individual cycle supports are all blocks. Taking the ambient group as its own Sylow 2-subgroup meets the stated hypothesis.

## Read the mathematics

1. [Authored proof](author/PROOFS.md), especially the unrestricted block-obstruction transfer and infinite construction
2. [Independent proof audit](audit/INFINITE_PROOF_AUDIT.md), including a separate Frattini argument and explicit adversarial checks
3. [Current verdict](VERDICT.json), [author limitations](author/LIMITATIONS.md) and [source audit](audit/SOURCE_AUDIT.json)
4. [Three-approach research log](author/RESEARCH_LOG.md)

The author files and original archive were frozen before the audit, so they retain the historical “audit pending” wording. This later wrapper records the resulting PASS without rewriting that history. The frozen audit and original receipts likewise retain their accurate pre-publication no-remote-write statements. No mathematical correction was required.

## Exact verification

From this directory, run:

```sh
python3 verify_package.py
```

The runner resolves paths relative to itself, so it also works when invoked from another directory or after moving this complete folder. It checks recursive inventory, all publication hashes, both original ZIPs and their extracted-file equality, both frozen manifests, the author finite verifier and the separate independent verifier. It never writes the frozen artifacts.

Author checks use the Python standard library. The independent check additionally uses SymPy. The recorded exact-output replay was tested with Python 3.12.14 and SymPy 1.14.0; its frozen output records those versions. A different interpreter/library version may cause an exact-output metadata mismatch and should be recorded explicitly rather than silently rewriting the freeze.

The finite checks cover the order-32 group, every one of its 50 subgroups and 22 cyclic subgroups, all 255 nonempty point subsets, every one of 64 quotient-lift pairs, the complete order-2,048 first wreath stage, and all 1,024 pairs of witness lifts at that stage. The infinite theorem is a deductive proof, not an inference from these finite tests.

## Preserved archives

- [Original author safe freeze](archives/KOUROVKA_2515_AUTHOR_SAFE_FREEZE.zip), 19,561 bytes, SHA256 af960c341c4595486aef5a5376b1f596053da606ce2b25611a7d624779beff6b
- [Original independent audit](archives/KOUROVKA_2515_INDEPENDENT_AUDIT.zip), 20,066 bytes, SHA256 b5fe0726ef6533e38846f380d5ad3ec67811e4bd317b397c1f3481f7d435be76

Their original receipts are adjacent. The publication manifest covers every file in this folder except itself. The queue update changes only this target's Status, Turns and Findings, preserving all other bytes and the existing header.

## Scope and provenance

The controlling [October 2026 primary Notebook](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt.pdf) is printed page 177, Problem 21.6, A. O. Asar. It permits arbitrary transitive ambient G; maximality in the entire finitary symmetric group is not required. Literature access limitations are disclosed in the reports and do not enter the proof.

Only authored mathematics, code, computed certificates and public verification metadata are included. Source PDFs, extracts, source images, raw corpora and private coordination are excluded. This remains a draft research record with no merge, release, DOI or outreach action.
