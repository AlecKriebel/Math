# Access failures and limits

Recorded 2026-10-16T20:51:56.455084+00:00. Direct-fetch failures below retain their actual attempt UTC in ACCESS_RECEIPTS.jsonl. They are access gaps, not evidence that a theorem does not exist.

- 2026-10-16T20:40:01.080750+00:00 — https://www.nzdr.ru/data/media/biblio/kolxoz/M/MD/MDgt/Zelenyuk%20Y.%20Ultrafilters%20and%20topologies%20on%20groups%20%28De%20Gruyter%2C%202011%29%28ISBN%203110204223%29%28O%29%28229s%29_MDgt_.pdf — <HTTPError 404: 'Not Found'>
- 2026-10-16T20:40:54.702687+00:00 — https://www.iris.unict.it/retrieve/dfe4d226-fa7c-bb0a-e053-d805fe0a78d9/bbm.pdf — <HTTPError 403: 'Forbidden'>
- 2026-10-16T20:41:19.671182+00:00 — http://www.nzdr.ru/data/media/biblio/kolxoz/M/MD/MDgt/Zelenyuk%20Y.%20Ultrafilters%20and%20topologies%20on%20groups%20%28De%20Gruyter%2C%202011%29%28ISBN%203110204223%29%28O%29%28229s%29_MDgt_.pdf — <HTTPError 404: 'Not Found'>
- 2026-10-16T20:41:19.671466+00:00 — https://nzdr.ru/data/media/biblio/kolxoz/M/MD/MDgt/Zelenyuk%20Y.%20Ultrafilters%20and%20topologies%20on%20groups%20%28De%20Gruyter%2C%202011%29%28ISBN%203110204223%29%28O%29%28229s%29_MDgt_.pdf — <HTTPError 404: 'Not Found'>
- 2026-10-16T20:41:19.671534+00:00 — https://degruyterbrill.com/document/doi/10.1515/9783110213225/pdf — Returned zero-byte HTML rather than a readable book/PDF.
- 2026-10-16T20:41:19.671581+00:00 — https://www.degruyterbrill.com/document/doi/10.1515/9783110213225/pdf — Returned zero-byte HTML rather than a readable book/PDF.
- 2026-10-16T20:44:21.207760+00:00 — https://dokumen.pub/ultrafilters-and-topologies-on-groups-9783110204223-9783110213225.html — <HTTPError 403: 'Forbidden'>
- 2026-10-16T20:44:21.207829+00:00 — https://www.sciencedirect.com/science/article/pii/016686419290021Q — <HTTPError 403: 'Forbidden'>
- 2026-10-16T20:44:21.207875+00:00 — https://www.sciencedirect.com/science/article/pii/S0166864102000937 — <HTTPError 403: 'Forbidden'>
- 2026-10-16T20:45:44.830235+00:00 — https://www.iris.unict.it/bitstream/20.500.11769/6655/1/bbm.pdf — <HTTPError 403: 'Forbidden'>
- 2026-10-16T20:47:22.971254+00:00 — https://iris.unict.it/bitstream/20.500.11769/6655/1/bbm.pdf — URLError(SSLError(1, '[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] ssl/tls alert handshake failure (_ssl.c:1082)'))

Additional web-service outcomes observed during the active UTC window 2026-10-16 20:39–20:48:

- Publisher book HTML and PDF routes for DOI10.1515/9783110213225 returned internal/empty results. The indexed nzdr book URL returned an internal web error and repeated direct404. Scribd exposed only the beginning of the book; it did not expose Cor12.21.
- The primary DOI for the2013 separability paper intermittently gave an internal web error, while the immutable arXivv1 was obtained in full.
- EU DML Talagrand landing page returned403. The actual IMPAN original PDF was subsequently obtained, rendered and inspected successfully.
- An initially guessed Talagrand article locator was incorrect; following the publisher contents links recovered the correct product102871. A mistaken link-id click returned an internal error and was corrected. Neither was used as evidence.
- An initially guessed2002 article DOI and a DML item locator did not identify the intended source. The actual2002 DOI was recovered from the paper metadata; only its primary abstract was inspected. No mathematical content from the unrelated DML item was used.
- MDPI original survey URL gave an internal error on open; relevant primary text was independently available in the arXiv2016 revision. The2015 journal date was not used as the conservative date bound for the topology passage.
- Web opening of Protasov2009 PDF failed once; direct retrieval later succeeded and the entire five-page text was read.
- Googlewithin-volume book queries for12.21, absolutely, finite and expansive returned zero hits even for common words. These are weak access/search outcomes and are not evidence about book contents.

No attempt used credentials, bypassed a paywall, installed software, contacted a human, purchased a source, or prepared outreach. External library access could resolve the older-book/paper gaps, but only the human may communicate externally.
