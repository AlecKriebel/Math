# Two explicitly repaired Sigma-neighborhood statements: exact counterexamples

Problem 2306113 / AMR-022-6113, Hayman–Lingham Problem 6.113, rank 1036.

**Historical problem status: unresolved; five of five substantive approaches used.** The accepted mathematical result is an exact degree-10 counterexample for each of two explicitly displayed repairs of a malformed neighborhood formula. Identifying either repaired formula with the historical primary definition remains unresolved. This packet does not claim full resolution of the historical problem.

For x=0, rho=1/1000 and gamma=1000000/1002001, an explicit normalized polynomial g lies in each specified neighborhood throughout the unit disk. An explicit globally normalized univalent function F has (g*F)(999/1000)=0 exactly. The symmetric formula has a rational all-circle certificate and a maximum-modulus argument; the inner-absolute-value formula has a genuinely two-dimensional disk certificate. S* here means the Hadamard dual, not the starlike class.

Start with [acceptance and limitations](ACCEPTANCE.md), the [main proof](candidate/PROOF.md), the [alternative repair](candidate/ALTERNATIVE_REPAIR.md), and the two independent AI-assisted audits: [mathematical scope](scope_audit/SCOPE_AUDIT.md) and [exact reconstruction/reproducibility](exact_audit/AUDIT.md). The [five-approach ledger](candidate/APPROACHES.md) distinguishes unsuccessful routes and partial results. No novelty, priority, complete literature search, journal peer review, or formal proof-assistant verification is claimed.

## Original and corrected slices

The original v2 manifest is pinned at `2f315877db00b3776fe55ab0e576012874078fd8e2df0fc61fec94ff7ac98c28`. Its complete thirteen-file identity is represented without duplicating shared bytes: its own manifest and main verifier are preserved in `original_v2/`, and its eleven other files are byte-identical to the files in `candidate/`. The wrapper checks every original entry through this lossless representation.

The separately corrected thirteen-file `candidate/` slice has manifest `d889cab7f0337d983b9bd352f61b6bdd5e330cd6d011927cb97949dd716471fb`. The sole code change is the [one-line ValueError catch](exact_audit/REJECT_LARGE_INTEGER.patch), changing oversized JSON-integer handling from an uncaught exception to structured rejection. Proofs, witness, successful outputs and the other checker are unchanged. Historical pending-review wording in frozen authored files is preserved; ACCEPTANCE.md gives the later accepted, qualified status.

## Source-free replay

Python's standard library suffices. Source documents, external datasets and the optional floating-point search are not needed. Independently authenticate `verify_publication.py`, `wrapper_controls.py`, and `PUBLIC_MANIFEST.json` using digests conveyed outside the packet before executing them. A mutable manifest cannot authenticate itself.

Make a fresh copy with directories mode 0555 and regular files mode 0444, then execute as genuine UID/EUID 1000. Use a writable working directory outside the packet. Run each of:

    python3 -I -B verify_publication.py --root /absolute/read-only/packet --manifest-sha256 EXTERNAL_MANIFEST_PIN
    python3 -I -B -O verify_publication.py --root /absolute/read-only/packet --manifest-sha256 EXTERNAL_MANIFEST_PIN
    python3 -I -B -OO verify_publication.py --root /absolute/read-only/packet --manifest-sha256 EXTERNAL_MANIFEST_PIN

Each full invocation freshly runs six candidate positives, 168 baseline input rejections, 228 expanded input rejections, seven trust-boundary rejections, independent coefficient reconstruction, all 32770 listed circle points, all 4050 adaptive disk nodes and 2026 leaves, and four exact partition mutation rejections. The baseline and expanded drivers themselves exercise normal, -O and -OO child modes. Independent algebra, complete-circle/disk reconstruction and partition checks inherit the outer optimization mode. All successful exact outputs and independently generated leaf bytes must match their frozen records. Two wrapper write probes and two baseline-driver write probes must actually fail with PermissionError. All packet bytes are revalidated afterward.

The original v2 execution reports are historical and hash-checked, not presented as fresh runs. The original checker is retained for provenance and comparison; fresh malformed-input acceptance is assessed on the separately corrected slice.

Run the wrapper's additional adversarial controls with:

    python3 -I -B wrapper_controls.py --root /absolute/read-only/packet --manifest-sha256 EXTERNAL_MANIFEST_PIN --wrapper-sha256 EXTERNAL_WRAPPER_PIN

That command tests three integrity-only positive runs and 37 rejection cases in each optimization mode (111 rejections total), including exact integer schema, duplicate keys, overflow, inventory/path/symlink attacks, writable files, wrong external pins and repinned changes to either preserved verifier. Tests mutate only disposable copies. Integrity-only PASS does not mean mathematical replay occurred.

Permission bits establish real process-level read-only behavior. They do not protect against root, a malicious owner changing permissions, concurrent substitution, or arbitrary resource exhaustion. Trusted interpreter, standard library, operating system and stable filesystem are assumed. This is computer-assisted verification, not a proof kernel or CI result.

## Public sources and scope

[Hayman–Lingham, arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2) is the inspected problem source; the historical record reports malformed delimiters in both its HTML and PDF. The full text of [Sheil-Small–Silvia, *Neighborhoods of analytic functions* (1989)](https://doi.org/10.1007/BF02820479) was not obtained. Its intended formula is therefore not attributed to an uninspected page. Public URLs, retrieval history, byte counts and PDF digests are retained in the original [source metadata](candidate/SOURCE_METADATA.json); source text and PDF bytes are excluded.

`PUBLIC_MANIFEST.json` is the exact source-free file allowlist and digest inventory, excluding only itself for external pinning. No private coordination record, downloaded scholarly document, external dataset content or personal data is part of this packet.
