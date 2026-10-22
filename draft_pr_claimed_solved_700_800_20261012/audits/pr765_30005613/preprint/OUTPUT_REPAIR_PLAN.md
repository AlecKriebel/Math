# Required output-preservation repair plan

2026-10-16T05:29:22.371445+00:00 — pending first-review closure; no input mutation.

1. Preserve the lexical absolute output path before resolve; inspect it and every existing ancestor for symlinks. All existing ancestors must be directories.
2. Resolve output root and reject portable output inside or equal to closed source root. For every planned destination, including PACKAGE_INVENTORY.json, inspect all existing ancestors and the destination before any mkdir or write. Reject symlinks, non-directory parents and nonregular final destinations. Reject any resolved destination inside closed source.
3. Capture the complete closed input inventory/bytes; verify outer manifest, fixed historical/review pins and downloaded PDF before building. Construct all output and inventory bytes in memory. Validate every destination as a batch before first mutation.
4. Write only approved destinations, then compare complete closed input inventory/bytes with the captured values. Root authoring mode intentionally writes into its own unfrozen output directory; portable closed mode must preserve all inputs.
5. Add physical regressions for external root and ancestor links, output/pdf ancestor to input, PDF destination link, inventory link, sourceZIP link, paper.tex link, output root regular-file, parent regular-file, final destination directory, FIFO destination, and lexical path containing a symlink. Rejection must occur before any output is written and source bytes/inventory must remain identical. Run under outer -O and environment optimization2.
6. Apply O1 initialization clarification to paper; compile, render and inspect all changed pages; rebuild source/metadata/kit; replay four modes and exact six-output rebuilds; freeze new pins; have a NEW fresh complete-package adversary review corrected inputs. Preserve the first report and input identities unchanged.

## 2026-10-16T05:35:35.147003+00:00 — hardlink extension from independent adversary

Regular hardlink destinations also overwrite closed inputs. Preflight must reject multiply linked destination files/inode aliases. All generated outputs and the inventory receipt must use fresh same-directory temporary regular files followed by atomic replacement, so final-file writes never truncate an existing inode. Add physical hardlink regressions for metadata, inventory and the remaining generated destinations. Post-preservation checks alone cannot repair already corrupted inputs. Frozen publication files are unchanged; these are planned repairs after first-review closure.

## 2026-10-16T05:37:02.675347+00:00 — external PDF alias edge independently reproduced by root

A normal single-link downloaded PDF at OUT/zenodo-metadata.json is overwritten by the generated metadata even though closed source bytes remain unchanged. In portable mode preflight must also forbid output aliases to the supplied PDF path/inode, and the final preservation check must cover that PDF identity. Seven separate ordinary-path PDF alias regressions are added to the root harness. No mathematical proof change follows from these package defects.
