# Independent audit packet: Calegari Question 6.1

Decision: **accepted only as an unsolved 5/5 scoped report**. Read `AUDIT_REPORT.md` for the full mathematical review, source applicability, correction history, and remaining gap. This is automated independent review, not human peer review or a formally checked proof.

The subject is the exact source-free `author_v1` distribution identified in `REVIEWED_SUBJECT.json`. Audit scripts never modify that distribution. They use disposable copies for rejection controls. `SOURCE_RECHECK.json` contains only public-source metadata and corpus/record hashes, not source documents or dataset contents. `REPLAY_RECEIPT.json` contains actual normal/-O/-OO subprocess outcomes.

## Authenticate before running

Obtain the audit manifest's SHA-256 from the independently delivered external pin. Hash `AUDIT_MANIFEST.json` with a trusted tool and compare it before trusting its contents. Then independently check every listed audit file's byte count and SHA-256 and reject missing, unexpected, nonregular, or symlink files. A manifest received beside untrusted files does not authenticate itself. Use a trusted Python interpreter and standard library on a quiescent filesystem.

Also externally authenticate the subject's manifest and bootstrap using the two pins in the review. The independent control script checks the subject's entire exact inventory before importing its verifier. Its reference inventory is itself covered by the audit manifest.

## Reproduce

Replace the example paths with local directories. Run from anywhere:

```sh
python -I -S -B /path/to/audit/independent_controls.py \
  --subject /path/to/author_v1
python -I -S -B /path/to/audit/independent_boundary_controls.py \
  --subject /path/to/author_v1
```

For the private, read-only source/corpus binding replay, supply the six source files named in the author source pins and both corpus files named in its corpus bindings:

```sh
python -I -S -B /path/to/audit/independent_controls.py \
  --subject /path/to/author_v1 \
  --sources-dir /path/to/sources \
  --corpora-dir /path/to/corpora
```

Repeat each command with `-O` and `-OO` before the script path. The recorded audit ran all three outer modes; each suite also exercises all three inner modes. It independently replayed the author's `author/controls.py` under all three outer modes.

With sources and corpora supplied, each independent-control invocation checks 94 labelled multigraphs, 1,422 retained subsets, 19 malformed graphs, and 99 surface genera, then obtains 9 successful and 60 rejected subprocesses. Without optional private inputs, there are 6 successful subprocesses. Every boundary invocation accepts 3 exact relocated copies and rejects 45 mutations. These are finite bookkeeping/integrity controls; the mathematical acceptance is justified separately in the report.

No frozen author correction was necessary. The positive-genus clarification was incorporated by the author before freezing the accepted version. Do not update historical author metadata inside that version merely because this separate acceptance report now exists.
