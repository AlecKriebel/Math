# Literal query and retrieval ledger

These are authored statuses, not raw source excerpts. Raw primary PDFs, extracted text, rendered pages and fetch headers are confined to `_local/`. No general web search, candidate search, repository search, author contact, or external messaging was undertaken.

| Literal request | Authored status |
| --- | --- |
| `open https://ems.press/content/serial-article-files/46706` | Web provider opened the publisher PDF; confirmed report identity and independently inspected its page 21 / printed page 2621 after a direct download. |
| `open https://arxiv.org/abs/1708.08258v3` | Web provider returned the version-specific primary arXiv abstract record. |
| `open https://arxiv.org/pdf/1708.08258v3` | Web provider opened the version-specific primary PDF; direct bytes independently downloaded and relevant complete pages rendered and inspected. |
| Direct HTTPS GET `https://ems.press/content/serial-article-files/46706` | Successful HTTP 200; primary PDF bytes and fetch record persisted only under `_local/`. |
| Direct HTTPS GET `https://arxiv.org/pdf/1708.08258v3` | Successful HTTP 200; version-specific primary PDF bytes and fetch record persisted only under `_local/`. |
| Direct HTTPS GET `https://www.maths.tcd.ie/pub/ims/bull61/S6101.pdf` | Successful HTTP 200; primary Renault body, extract and rendered printed pages 58-59 inspected and persisted only under `_local/`. |

The web provider's displayed open responses were read but not persisted as separate raw response files. The direct downloads preserve the primary evidence actually used for the source assertions; their exact bytes, SHA-256 values, final URLs, headers and retrieval times are in `_local/FETCH_RECORDS.json`. No raw third-party snippets or excerpts are reproduced in this public ledger.
