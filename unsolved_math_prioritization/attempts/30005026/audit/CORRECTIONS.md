# Exact source errata for the frozen author package

These are nonblocking source-accuracy corrections. They do not change any mathematical proposition, input hash, verification count, or the unresolved status. The frozen ZIP has not been modified. This addendum must accompany it; a later author revision may incorporate these two replacements.

## C1. Publication year versus workshop date

Location: RESULT.md, Section 1, final paragraph, sentence beginning "A catalog citation".

Old:

> A catalog citation calling the workshop itself a 2023 event conflates these dates.

New:

> The catalog's parenthetical 2023 is consistent with the report's publication year; it should not be read as the workshop date.

Reason: the full dataset contains a bibliographic parenthetical year, not an explicit assertion that the meeting occurred in 2023. The report's title page dates the workshop to 13–19 February 2022. EMS lists the issue as Volume 19 (2022), published 11 March 2023. The year 2023 in a publication citation is therefore not intrinsically erroneous. The author's adjacent statements that the workshop occurred in 2022 and the issue was published in 2023 are correct.

Evidence: https://ems.press/journals/owr/issues/2056 and the title page of https://ems.press/content/serial-article-files/46944 .

## C2. Markov-extension page range

Location: SOURCES.md, item 3, first paragraph.

Old substring:

> Section 5, printed pp.30--32.

New substring:

> Section 5, printed pp.28--31.

Reason: Section 5 begins at the bottom of printed p.28, continues through pp.29–30, and finishes at the top of p.31. Printed p.32 contains references. The cited Theorem 2 is correctly located on printed p.3.

Evidence: https://www.math.ucdavis.edu/~romik/data/uploads/papers/expoplms.pdf .

## Inspection-history handling

Do not rewrite the frozen provenance.json entries recording which pages the author inspected. Those are historical metadata, not a claim about the full extent of Section 5. The auditor additionally inspected pp.28–29; SOURCE_AUDIT.json records that separately.

No definitive false date, PDF hash, dataset hash, or verification result was found in frozen provenance.json. Neither correction requires changing that file. Theorem 1.2 on p.2 of the entropy-efficient preprint supplies the countable-output qualitative extension; the audit records this additional supporting location without treating it as a new mathematical input.
