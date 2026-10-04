# Failure ledger

- Initial extraction dependency pypdf was unavailable in the specified private Python runtime. Used installed Poppler pdftotext and pdftoppm; no installation performed. No candidate impact.

- The web renderer could not open the Numdam supplement. Direct primary PDF retrieval succeeded; its1,037,965 bytes and SHA256 match SOURCE_ADDITION_T2.json. The relevant primary pages were extracted/read locally.
- The first whole-repository tree requests used an unquoted question mark and were rejected by zsh globbing. Quoted retry worked for the head, but that GitHub recursive response explicitly has truncated=true. It is retained as failed_truncated_whole_head_tree_api.json.gz and is not accepted as scope evidence.
- A base whole-tree output and several small writes failed under transient disk-full pressure. The partial base response was discarded. Only this audit's own duplicate source copies and regenerable extracts/renders were removed; raw PDFs remain. Complete generated C++ streams and the head response were losslessly compressed. Parent independently freed its own storage; foreign files were untouched.
- The initial bindings verifier correctly rejected the truncated whole-tree API response. It was replaced by recursive comparison of untruncated direct tree requests, skipping only identical tree SHAs. This verifies every changed subtree without relying on a truncated root listing.
- A subsequent verifier run failed because this review's queue-column assertion used indexes9/10 instead of8/9 after splitting leading/trailing pipes. Corrected the local reviewer assertion; the actual candidate queue changes were always the same two target cells. All44 API blobs had already passed. Final rerun passed every binding, scope, history and raw replay comparison.
- Every candidate execution in both source modes returned0 with empty stderr. No candidate mathematics or program failure was encountered. No candidate file was corrected or rewritten.
