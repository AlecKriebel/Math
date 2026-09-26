# Bulletin of the Australian Mathematical Society: verified submission requirements

Checkpoint: 2026-09-26T04:13:03+00:00 (2026-09-25 America/Los_Angeles). Requirements audit **95% complete**: current public journal, publisher and template requirements are checked; account-only interface fields remain unverified. No account, agreement, communication or submission was created.

## Target decision and actual AI-policy compatibility

**The Bulletin is a supportable replacement target for this package.** Its own OJS preparation checklist expressly covers AI-generated text, images and data analysis and requires suitable acknowledgement and description. This provides positive policy evidence; the choice does not rely merely on the absence of a prohibition. [Bulletin checklist](https://journal.austms.org.au/ojs/index.php/Bulletin/about/submissions)

The journal-specific Cambridge page likewise explains how to disclose generated manuscript text, analysis and images. The disclosure should identify the tool/version, use dates as far as possible, access information and a full account of its use. Text generation belongs in acknowledgements or a footnote; analytical use belongs with methodology. For this paper, state the real scope: mathematical exploration/argument development, manuscript drafting/revision, verification code and AI-agent audits as applicable. Do not reduce it to language editing. This same page requires prior consultation for publisher-hosted supplements; repository publication is separately encouraged. We recommend a cited public reproduction repository with a referee ZIP only if the form permits. No external consultation was initiated. [Journal preparation and AI policy](https://www.cambridge.org/core/journals/bulletin-of-the-australian-mathematical-society/information/author-instructions/preparing-your-materials)

Cambridge's broader policy requires human accountability for accuracy, integrity and originality; AI cannot be named as an author. It also requires appropriate credit for third-party material. Human author criteria include substantive intellectual involvement or critical revision/final approval and accountability. There is no corresponding prohibition on an article largely written by AI in the reviewed journal-specific and publisher provisions. This supports preparing an honestly disclosed submission, not an editorial promise: Alec must personally approve the final work and be able to accept responsibility before submission. [Cambridge authorship and AI contributions](https://www.cambridge.org/core/services/publishing-ethics/authorship-and-contributorship-journals)

## Fit and length

The Bulletin welcomes original research across mathematics, emphasizing clear, attractive exposition and relatively short articles, approximately twelve pages or fewer. It screens for a manuscript already in publishable form and makes many quick editorial decisions, often within a month. It reports receiving over five times available publication capacity; quick processing does not mean easy acceptance. A sharp counterexample to a named finite-group problem with a self-contained proof fits the format, but novelty and strength remain editorial judgments. [Scope and review criteria](https://journal.austms.org.au/ojs/index.php/Bulletin/about)

## Initial upload and metadata

Use [OJS submissions](https://journal.austms.org.au/ojs/index.php/Bulletin/about/submissions), then login or register as both reader and author. Choose the **Articles** section for this research paper. Initial manuscript format is PDF prepared with AMS-LaTeX; the society encourages its `baustms` class. Source may be requested after acceptance or before review. Metadata must include every author and ORCID, keywords and MSC codes. Abstract maximum: 200 words, self-contained and without numbered cross-references. Include one primary and at least one secondary MSC2020 code. References are alphabetic and numerically cited, and only cited works belong in the list. Inaccessible cited material should accompany submission. Do not invent exact logged-in upload labels or imply a source ZIP or cover letter is a verified mandatory initial field. [OJS instructions](https://journal.austms.org.au/ojs/index.php/Bulletin/about/submissions)

Recommended metadata: author Alec Kriebel; ORCID https://orcid.org/0009-0001-9320-500X; affiliation Independent researcher; primary 20B05; secondary 20D30, 20D60. Keywords: finite permutation group; minimal base; independent set; subgroup lattice; Kourovka Notebook. Email and complete contact/address details must come from the author, not be inferred. Codes checked against [AMS MSC2020](https://mathscinet.ams.org/msc/msc2020.html?t=20-08).

## Template and formatting

Official, unchanged files have been downloaded to `sources/bulletin/`:

- [baustms.cls](https://archive.austms.org.au/Publ/Bulletin/baustms.cls), LPPL 1.3c or later.
- [srtnumbered.bst](https://archive.austms.org.au/Publ/Bulletin/srtnumbered.bst), LPPL 1 or later.
- [bamstemplate.tex](https://archive.austms.org.au/Publ/Bulletin/bamstemplate.tex).

See `sources/bulletin/TEMPLATE_PROVENANCE.md` for hashes and license notices. Use `\documentclass{baustms}`. The class already loads AMS packages, Times mathematics, hyperref and geometry. It provides `cupthm`, `cupdefn`, `cuprem`; `\runningtitle`; `\author[1]`; `\address[1]`; `\authorheadline`; and `\classification[2020]`. Do not load duplicate/conflicting packages or modify margins to force a page count. The official class's optional `[2020]` argument updates the otherwise stale classification heading without editing the class. Keep the abstract within 150 words if convenient, satisfying both its old template and the current 200-word rule.

## Fees, preprints and rights

Recommend the ordinary **Green Open Access** route; OJS states it has no publication charges. Do not select paid Gold OA merely to submit. [Journal licence terms](https://journal.austms.org.au/ojs/index.php/Bulletin/about/submissions)

Cambridge confirms that this hybrid journal's Gold route is optional and its APC does not apply to articles published under the ordinary route. Preprints may be posted anywhere at any time, including before submission. For the accepted manuscript, a six-month embargo applies to non-commercial repositories from first publication of the version of record; distinguish this from the freely shareable submitted preprint. [Journal open-access policy](https://www.cambridge.org/core/journals/bulletin-of-the-australian-mathematical-society/information/journal-policies/open-access-options)

A licence to publish is required before publication; copyright ownership remains with the author. [Publishing agreement requirement](https://www.cambridge.org/core/journals/bulletin-of-the-australian-mathematical-society/information/author-instructions/submitting-your-materials)

## Reproducibility and declarations

The journal encourages evidence, data and code access, data-availability statements and citations to archived material, ideally preserved with permanent identifiers. A compact availability paragraph should identify the exact public repository version/commit and the package containing the exact verifiers; avoid describing private audits as external peer review. [Research transparency](https://www.cambridge.org/core/journals/bulletin-of-the-australian-mathematical-society/information/journal-policies/research-transparency)

Cambridge requires disclosure of potential competing interests, including financial and nonfinancial interests. Confirm real funding and conflict status with the author; do not silently manufacture negative declarations. [Competing interests and funding](https://www.cambridge.org/core/services/publishing-ethics/competing-interests-and-funding-journals)

## Editor handling

The current Cambridge board identifies **John Loxton** as editor-in-chief and **John Cossey** as associate editor for **Group theory**. If an optional editor preference appears, Cossey is the direct subject match, assuming no personal conflict. No editor selection is established as mandatory by the public instructions. Do not contact anyone or nominate unverified reviewers. [Current board](https://www.cambridge.org/core/journals/bulletin-of-the-australian-mathematical-society/information/about-this-journal/editorial-board)

## Remaining author actions and limits

1. Read the final proof and explicitly own the intellectual content and accountability; verify the detailed AI-use dates and versions from the research record.
2. Provide/confirm email, address, funding/conflict information, and originality/exclusivity. Keep the legitimate existing preprint disclosed.
3. Check the compiled PDF, including all disclosures/references, remains comfortably within the approximately twelve-page target.
4. Login to OJS and follow its actual upload controls. Main PDF is confirmed; upload the optional reproduction archive only through an appropriate supporting-file control if offered. Otherwise the manuscript's repository citation provides access. Source files remain ready if requested.
5. Read any changed policy or additional logged-in author declaration before accepting it; this audit does not purport to certify unseen fields.

No guarantee of peer review or acceptance is made. No manuscript edits or submissions were performed by this requirements audit.
