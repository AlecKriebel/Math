# Package identity audit

Status: independently verified on 2026-08-22.

## Delivered identity

- Scientific source commit claimed by the delivery:
  `3652cfda20a3edad1b4e9ca75a4e5536f6f7f5ba`.
- Source archive SHA-256:
  `b1b7b7c4c9393ee4fa85eeacd54cefc4bcc94a3eca759d500c9ee6a362eddd2b`.
- Manuscript PDF SHA-256:
  `a6bda621b764ca8ee86658f6b68de0245790b84315eb77a6cc7ca45f7953bd2d`.
- Archive contains 70 regular-file members, as claimed.

The source-commit provenance was also checked against the locally available
Git object. The object exists and is a commit; all 68 archive payload files
claimed to come from it match the corresponding blobs byte-for-byte. The two
archive-only metadata members are separately bound by the package checks.

## Independent checks

1. `shasum -a 256 -c PACKAGE_MANIFEST.sha256`: exit 0; every listed package
   member matched.
2. Detached archive checksum: exit 0 and matched the value above.
3. Delivered extraction's internal `MANIFEST.sha256`: exit 0; every listed
   archive payload file matched.
4. Fresh extraction of the archive to `work/archive_extraction`: exit 0.
5. Recursive byte/name comparison between the fresh and convenience
   extractions: exit 0 with no differences.
6. Fresh extraction's internal manifest: exit 0 for every listed payload
   file.
7. Byte comparison of `complete_graph_extremality_db.pdf` with the PDF inside
   the archive payload: exit 0 with no difference.
8. Independent `git show COMMIT:PATH` comparison for all 68 source-derived
   payload files: exit 0; every SHA-256 matched.

The complete transcripts and exit statuses are in `records/COMMANDS.log`.

## PDF inspection

- 30 letter-size pages, unencrypted, no forms or JavaScript.
- Poppler 26.08.0 extracted and rendered every page successfully.
- Visual inspection of all 30 rendered pages found no clipping, overlap,
  missing glyphs, illegible tables, or broken figures.
