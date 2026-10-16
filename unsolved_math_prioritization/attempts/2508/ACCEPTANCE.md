# Acceptance and publication scope

## Exact mathematical disposition

The complete authored verification and separate complete mathematical audit accept the prior proof for **2508 / EP-1133**, relative to the explicitly imported Bernstein interpolation strict-density theorem and standard analytic/measure-theoretic results. No unresolved gap was found in the checked deduction, and no mathematical patch is required. The repository classification is **already_solved**, with **0/5 new substantive solution approaches**.

For every real C > 0, there are epsilon > 0 and n0, depending only on C, such that for every n >= n0 and every indexed list of n nodes in [-1,1], one can choose real labels in [-1,1] so that every complex polynomial of degree strictly below (1+epsilon)n and interval norm at most C agrees at strictly fewer than (1-epsilon)n indices. Equivalently, agreement on at least (1-epsilon)n indices forces norm strictly greater than C. Repeated nodes and indexed multiplicity are retained.

The accepted argument includes the C < 1 case, uniform separation, stationary configuration compactness, interpolation on every support configuration, passage from real to complex data, strict density, angular rescaling, and the floor/ceiling and bad-block estimates. Both the candidate's original ergodic extraction and the verification's reverse-Fatou alternative were checked. The latter is an alternative verification of a step, not a new solution approach. No effective constants in C are claimed.

The imported result is the necessity direction of Ortega-Cerdà and Seip, Theorem 1, in the real-line specialization: interpolation for bounded complex data in the Bernstein space of exponential type at most tau requires upper uniform density strictly below tau/pi. The strict inequality is indispensable. The imported theorem is not reproved or formally certified by this packet.

## Attribution and public status

The audited draft is *A Bernstein-density proof of Erdős’s robust interpolation obstruction*, dated April 29, 2026, publicly attributed through Przemek Chojecki's posting with GPT-5.5 Pro assistance. The PDF title page has no named author. Attribution is deliberately limited to that public posting. The exact manuscript and source identities are recorded in [SOURCES.json](author/public/SOURCES.json).

- [Prior draft](https://www.ulam.ai/research/erdos1133.pdf)
- [Public discussion](https://www.erdosproblems.com/forum/thread/1133)
- [Ortega-Cerdà–Seip article DOI](https://doi.org/10.1006/jfan.1998.3357)
- [Original Erdős survey](https://users.renyi.hu/~p_erdos/1967-20.pdf)
- [Dated AI-contributions index](https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems)

The available tracker snapshot calls the work a candidate and says updates ended June 30, 2026. This audit does not establish later tracker acceptance, current community consensus, journal acceptance, human expert certification, or proof-assistant formalization. The repository's accepted-audit classification must not be presented as external consensus. There is no new-discovery or historical-priority claim.

## Frozen evidence and verification boundary

The original author archive is 17,247 bytes, SHA-256 74b4b17367e5926f3fcf35307e8dff9c0d8cd37923b20066d31fe8bdfb1c9203. Its public manifest is 97185d9d301079510b35dcc78944f1f536c10e34f4de5222aadf474093b1b15d; the author verifier is 14733b9582625d2cdecc12312832a3af5b1f4737646088a54b7f4b9c8586af8d.

The independent supplement is 14,569 bytes, SHA-256 2fd59af57e01c38fc3a25b4a98f69c925eef917fb0840f2a784dd9a60c761783. Its manifest is aab77e1317076d4369cb0ba8b585773b95675e174f4dd22929c8f175ec9df9ce. All allowlisted members, both archives, and both final receipts retain the accepted bytes. Historical statements such as publication_performed=false describe their original time and are not silently rewritten.

Default fresh replay is source-free. The historical original 90 rejections comprise 84 bundle and six optional-source cases; only the 84 bundle cases are rerun. The historical additional 75 comprise 51 portable and 24 source-dependent cases; only the 51 portable cases are rerun. Fresh source-PDF checks, corpus checks, and the original independent full-source harness are NOT_RUN. Historical all-five-file matches and inspections remain historical evidence. Finite arithmetic and node-pattern controls do not prove the analytic theorem or compactness.

The wrapper authenticates exact bytes and performs bounded controls; it does not validate arbitrary newly repinned descriptive metadata as a generic semantic schema. Its external bootstrap pin is essential. Only the target QUEUE.md row's Status, Turns, and Findings cells are in scope; all unrelated bytes, including the inherited leading SHA text, Chat, and DOI cells, are preserved. The draft is for review, with no merge, release, DOI deposit, or outreach.
