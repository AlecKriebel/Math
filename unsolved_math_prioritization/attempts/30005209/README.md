# Planar crystalline Wulff partial results

Problem **30005209**, queue rank **949**. Status: **unsolved**, **5/5** substantive approaches. The full geometric classification remains unresolved.

## Accepted scope

For each fixed exponent $0<\alpha<2$, a nondegenerate unit-area planar convex polygon containing the origin in its interior is a unique small-positive-coefficient global minimizer, up to translations and null sets, for its support-function anisotropy if and only if its side-average Riesz potentials are equal. The coefficient threshold depends on the polygon and exponent. Evenness of the anisotropy is not assumed.

The accepted consequences and obstruction are:

1. Every nondegenerate triangle qualifies. Automatic sliding stationarity is already in Bonacini–Cristoferi–Topaloglu (2022), Remark 4.1; no novelty is asserted.
2. Among parallelograms, exactly the rhombi qualify.
3. A local implicit-function construction produces sliding-stationary non-parallelogram quadrilaterals near the square, for sufficiently nearby normal configurations.
4. Vertex-truncation signs obstruct a particular strategy for excluding boundaries of normal-fan families. The thin-obtuse negative example is limited to $0<\alpha<1$.

This is an implicit planar criterion and partial geometric information. It does not classify all polygons, all normal fans, remote stationary branches, or higher-dimensional polytopes. Sliding and tilting variations are different: results imposing both do not classify the sliding-only problem.

## Reading order and byte provenance

- [Corrected reading copies](review/readable/README.md): the five full manuscripts, self-audit, and source/scope notes.
- [Complete independent analytical audit](review/AUDIT_REPORT.md) and [acceptance report](review/ACCEPTANCE.json). This is an AI-assisted audit, not human peer review or formal verification.
- [Frozen originals](authored/README.md), unchanged from the [original manifest](authored/AUTHORED_MANIFEST.json).
- [Typography-only patch](review/TYPOGRAPHY_ONLY.patch) and [typography manifest](review/TYPOGRAPHY_MANIFEST.json). Eight reading copies differ only by 171 inserted backslashes, with no deletions or substitutions. Their [separate corrected-copy manifest](review/readable/CORRECTED_COPY_MANIFEST.json) does not replace the original manifest.
- [Public source metadata](authored/SOURCE_MANIFEST.json): seven public scholarly PDF URLs, byte counts, SHA-256 values, retrieval date, and inspection scope. Source documents and extracted source text are not distributed here.

The analytic arguments rely on the explicitly cited small-parameter existence theorem of Choksi–Neumayer–Topaloglu, planar crystalline quasiminimizer rigidity of Figalli–Maggi, and quantitative Wulff stability. The packet does not reprove those external inputs. The relevant polytopal source authors are **Marco Bonacini, Riccardo Cristoferi, and Ihsan Topaloglu**.

The dated literature search found no full classification, but was bounded rather than exhaustive. No novelty or priority claim is made.

## Source-free verification

From the repository root, run:

```sh
python3 unsolved_math_prioritization/attempts/30005209/verify_packet.py
python3 unsolved_math_prioritization/attempts/30005209/verify_packet.py --sanity
```

The first command uses only Python 3.10+ standard-library modules. It checks the exact packet allowlist, all file hashes and byte counts, frozen original and audit anchors, acceptance scope, corrected-copy manifest, and exact correspondence of the insertion-only typography patch and reading copies. `PACKET_MANIFEST.json` pins every other packet file; like any ordinary manifest, it cannot cryptographically authenticate itself. Compare the pinned Git commit and externally reported manifest hash for publication identity.

The optional second command additionally requires SciPy. It runs a temporary copy of the unchanged authored verification script, leaving retained originals untouched. There are **19 floating-point sanity checks**: 12 parallelogram cases, four square-Hessian cases, and three thin-triangle convolution cases. The driver reports whether replay output is byte-identical to the retained JSON and also compares numerical fields with absolute and relative tolerances of $10^{-10}$ for cross-environment variation. These are not exact proof certificates. The analytical arguments and cited rigidity/existence inputs carry the proofs.

No verification command retrieves or inspects source PDFs, proves external theorems, establishes the full classification, or certifies novelty. The audit's source-inspection findings describe the dated analytical review, not an action performed by this replay driver.

## Publication boundary

This packet contains authored mathematical exposition and audits, insertion-only correction material, public scholarly metadata, and verification code/results. It excludes source PDFs, extracted source text, screenshots, source datasets, private sources, personal data, and coordination records. The only proposed existing-file change is the current problem's Status, Turns, and Findings cells in `unsolved_math_prioritization/QUEUE.md`; all other cells and bytes are preserved.
