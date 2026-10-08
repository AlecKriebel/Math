# Short geodesics and taut foliations: accepted scoped partials

Problem **10300043 / AMR-102-0043**, rank **1008**, Calegari Question 10.5. Disposition: **unsolved, 5/5 approaches used**. The independent audit accepts the original seven propositions unchanged. No universal threshold, universal isotopy or homotopy solution, or geodesic counterexample is claimed. This is an unrefereed, AI-assisted mathematical investigation, not formal proof verification or a novelty certificate.

## Mathematical scope

The accepted deductions are a homotopy bad-leaf-space length-gap reduction, a normalized fiber-period bound and norm countercontrol, a meridional calibration, a disk-filling transverse-core lemma, and an arbitrarily small **non-geodesic** trefoil countercontrol. Primitive free homotopy classes are not thereby embedded knots. Homotopy is not isotopy. Foliation-dependent and genus-dependent sufficient bounds do not supply a universal bound. The closed, orientable, cooriented restrictions are explicit rather than silently removed.

Read the complete [original proof](author_original/packet/PROOF.md), [independent mathematical audit](audit_original/payload/MATHEMATICAL_AUDIT.md), and [machine-readable acceptance](audit_original/payload/ACCEPTANCE.json). The complete original freezes and their ZIPs are byte-preserved, including the author's historical independent-review-pending label. The separate later audit supplies acceptance; no correction patch was needed.

## Public sources and limits

- Danny Calegari, [Problems in foliations and laminations of 3-manifolds](https://arxiv.org/pdf/math/0209081v1), printed Question 10.5, p.24.
- Yosuke Kano, [Taut foliations and the actions of fundamental groups on leaf spaces and universal circles](https://arxiv.org/pdf/1203.2413v1), Proposition 6.1 with its global hypotheses.
- William Breslin, [Short geodesics in hyperbolic 3-manifolds](https://arxiv.org/pdf/0912.3496v2). Otal's fiber-genus-dependent theorem is credited **through Breslin**; the original Otal proof was not obtained or certified.
- Danny Calegari, [The Gromov norm and foliations](https://arxiv.org/pdf/math/0007120v2), Section 3.2. Its length is a homotopy/foliation subdivision invariant, not ambient geodesic length.

[Source pins](author_original/packet/SOURCE_PINS.json) and [corpus bindings](author_original/packet/CORPUS_BINDINGS.json) contain public verification metadata only. No PDFs, source extracts, dataset contents, or private coordination files are included. The audit's retrieval and inspection accounts are dated historical evidence, not a fresh literature search by the publication replay.

## Reproduction and trust boundary

Python 3 standard library only, no network operations. Before execution, independently compare the hashes and byte counts of BOOTSTRAP.py and PUBLICATION_MANIFEST.json against the publication's external receipt or draft-PR description. BOOTSTRAP.py pins the verifier and manifest; the manifest authenticates the complete exact file and directory inventory before payload code runs. Coordinated replacement of all external anchors and concurrent filesystem mutation are outside the threat model.

Run from the packet directory:

    python -I -S -B BOOTSTRAP.py
    python -I -S -B -O BOOTSTRAP.py
    python -I -S -B -OO BOOTSTRAP.py
    python -I -S -B TEST_MUTATIONS.py

The default source-free replay authenticates both freezes and exact ZIP members, runs the original author's 84 controls, authenticates the later audit, and reruns the audit's independent finite algebraic diagnostics. The historical 111-scenario full audit suite is **authenticated recorded evidence, not claimed as rerun** by this wrapper. Its full original script requires separately supplied source and corpus inputs. Neither finite diagnostics nor integrity hashes mechanically prove the topology.

Default source and corpus rehash statuses are explicitly NOT_RUN. Optional rehashing reads only actual supplied inputs:

    python -I -S -B BOOTSTRAP.py --sources /path/to/source-pdfs
    python -I -S -B BOOTSTRAP.py --corpora /path/to/full-corpora

Either option may be supplied independently or together. It verifies the pinned PDF or full-corpus bytes, and for corpora checks the unique selected record pair. It emits only match metadata. It does not retrieve missing files, distribute their contents, or certify external source proofs. Requested absent, changed, malformed, or symlinked inputs fail closed. The integrity-only option executes no mathematical payload.

TEST_MUTATIONS.py tests separate-trusted-launcher rejection, every member's corruption and absence, repinned forgeries, malformed manifests, hostile code, symlinks, special files, extra paths, relocation, actual non-root read-only permission enforcement, and hostile import isolation. Optimized-mode and downloaded-copy results belong to the external publication verification receipt. Local replay success is not GitHub CI success; zero workflow runs or checks mean NOT_RUN.
