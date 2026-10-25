# Unresolved GHR edition binding

The published manuscript's §7 compares its active K against the GHR2013 Eq.(5.2) operator and asserts the latter has the same {-1,q} spectrum (multiplicities4+4) and residual squares(0,48) for shifts1,2. The submitted verify_exact.py lines452–481 explicitly calls its transcription literal and gives **both blocks** the prefactor −exp(−iπ/3)/√2.

The primary author preprint at https://people.tamu.edu/~rowell/GHRarx1.pdf, SHA256099639fe71b91addb538010127245d53db210676b66ae836f823acee8a40794b, printedp26 Eq.(5.2), has prefactor −exp(−iπ/3)/√2 for the first block and1/√2 for the second. This is confirmed visually in primary-sources/ghr-page-26.png. The same preprint's Remark5.29(1) instead gives the quaternionic expression with a common overall prefactor, indicating an internal typographical inconsistency in that preprint.

Let ζ=exp(iπ/4). Each displayed unscaled block has trace2(ζ+ζ^-1)=2√2. Thus the **literal preprint Eq.(5.2)** has trace2κ+2=2q, whereas the normalized common-prefactor matrix has trace4κ=4(q−1). Their difference is4−2q=3−i√3≠0. In particular the bare-spectrum similarity assertion cannot hold for the literal preprint formula. This observation does not challenge the new five-word R, its active K, or the intended quaternionic GHR operator.

The manuscript cites the final IMRN2013 edition, not merely this preprint. That edition's PDF URL was obtained from Crossref metadata: https://academic.oup.com/imrn/article-pdf/2013/3/693/19064415/rnr269.pdf . Direct retrieval returned HTTP403; the web tool redirected to an inaccessible OUP CDN. No final-edition bytes were available in this independent review. Therefore it is not established here whether the final edition corrects the prefactor. Do not report the discrepancy as a proven false statement about the final edition, and do not silently identify the preprint's literal formula with the submitted normalized comparator.

Resolution needs only the final Eq.(5.2) source or an explicit statement of the intended normalization in the comparison; no repair is attempted. The core construction and all later GR2026 comparisons are independent of this bounded source-version issue.
