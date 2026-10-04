# Independent Nencka priority-source audit

Scope: source validation for existing PR50/target 10600042; no new problem proof attempt. Fixed eligible head supplied by parent: `7260315f8b8b193020c09d4ef6df9d943a3a13ff`. Only this audit folder may be written. No Git/index/ref/remote/PR/Zenodo/Sheets mutations or human outreach.

## 2026-10-04 01:02 UTC — initial source checkpoint (30% of bounded priority audit)

Read root and queue AGENTS instructions, current priority finding, publication source qualifications, and existing theorem. Independently viewed the original scan of both Nencka contribution pages, printed pp. 147–148. The printed signed tails are present; a positive-only objection is invalid. The text introduces a new braid representation and calls its target relation a generalized Markov equivalence, without a definition or proof on these two pages. That does not yet establish whether an exact ordinary-closure result was proved elsewhere.

Read-only commands: `pwd`; `rg --files -g 'AGENTS.md' -g 'nencka*' -g '*even_strand_markov*' ...`; `cat AGENTS.md unsolved_math_prioritization/AGENTS.md`; `cat .../PRIORITY_FINDING.md .../SOURCE_QUALIFICATIONS.md`; `sed -n '1,300p' .../even_strand_markov.tex`; `rg --files --hidden --no-ignore .../private`. Viewed `nencka_scan_153.webp` and `nencka_scan_154.webp` with the image tool. Internet searches for the exact author/title and extensions title led to an AMS 1999 contents advertisement and an institutional 1996 preprint catalog entry, to be authenticated next.

Evidence status: actual 1996 body read; 1999 follow-up and 1996 full preprint body not yet accessed. Central remaining gap is identification and validation of the generalized relation, not merely existence of powers-of-two braid counts.

## 2026-10-04 01:06 UTC — authenticated follow-up checkpoint (70% of bounded priority audit)

Authenticated additional primary records: Nencka's 1996 12-page institutional preprint `CNRS CPT 96/P.3381`, *Cantorian Braid Groups*, in the JINR library new-preprints catalog; *Cantorian braid groups*, Methods Funct. Anal. Topology 4 (1998), no. 2, 66–75, MR1770817, from the official journal article page; and *On some extensions of Artin’s braid relations*, Contemporary Mathematics 233 (1999), 221–233, DOI `10.1090/conm/233/03432`, MR1701686, from the actual AMS volume contents and Crossref publisher-deposited metadata. The relation among these texts is plausible by topic but unverified: they are not silently treated as identical versions.

The official 1998 article page currently labels the item open access, but its full-text section is `Coming Soon` and its PDF metadata URL is empty. The actual AMS 1999 Chapter PDF link redirects to an institutional access selector. Neither body was accessed; no access barrier was bypassed. HAL exact-title searches and INSPIRE exact-title search returned zero records, a bounded access result that supplies no absence or novelty evidence. Independently viewed the 1996 volume copyright/ISBN page, confirming PHASIS 1996 and ISBN 5-7036-0017-0; printed papers are presented as supplied by their authors.

HTTP commands captured with start/end UTC, URL, final URL, status/error, byte count and SHA256 under ignored `private/commands/source_access_*.json`. Exact command form: `python3 .../private/access_sources.py '<JSON of source names and URLs>'`. That local script uses ordinary unauthenticated HTTPS requests and stores third-party responses only in ignored `private/`. Read-only extraction command examined Crossref title/DOI/page/author data and AMS TOC context; another inspected `Full Text`, `Coming Soon`, `citation_pdf_url`, and issue references with `rg`.

No new theorem proof attempt was made. Source scope remains unresolved, although the additional access gaps are now concrete and independently reproducible.

## 2026-10-04 01:10 UTC — final bounded-audit checkpoint (85% of exact priority-resolution goal)

Saved `PRIORITY_DISPOSITION.md` with the authenticated source/access ledger, precise conditional double-move comparison, n=0/B1 caveat, and concrete fair manuscript wording. Added `INPUT_BINDINGS.json` with SHA256 hashes of the three original scanned inputs and the existing v1 theorem input, without republishing third-party bodies. Verified artifact existence and that this folder's `.gitignore` declares `private/`; the earlier `git check-ignore` confirmed its private path is ignored.

Further bounded legitimate access checks: AMS's actual chapter link was institutional-login gated; no bypass. OpenAlex exposed only the DOI landing location and no open PDF for that chapter, a locator result only. Semantic Scholar DOI lookup returned404. HAL/INSPIRE exact-title searches returned no records; CERN's search endpoint did not provide a usable article body. A Toulouse Fiedler webpage contained only an image; World Scientific ordinary access returned403. None is evidence that a full proof does not exist. No full Nencka follow-up body or Fiedler proof was acquired.

Independent pixel reading corrected a detail in the prior review: Theorem 3 says `natural induction map`, not an explicit zeroth induction map. The n=0 caveat rests on unspecified natural-number convention. Reported this correction to the parent before finalizing.

Strongest verified conclusion: the 1996 earlier related announcement exists and is directly pertinent; two further published source identities and a full preprint identity are authenticated. Exact earlier ordinary-closure completeness/priority remains UNRESOLVED. The remaining 15% represents the decisive inaccessible full-source/model/proof validation, not routine editorial work. The bounded access/reporting assignment is complete; retain the broader priority hold.

No new proof search, human outreach, or Git/index/ref/remote/PR/queue/Zenodo/Sheets mutation occurred. All writes are confined to this audit folder. The local binding/validation command was `python3 - <<'PY' ...` using `pathlib`, `hashlib`, `datetime`, and `json` to read the specified inputs, write `INPUT_BINDINGS.json`, and assert artifact existence/private-ignore declaration; its UTC timestamp is in the saved JSON.
