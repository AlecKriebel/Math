# Source and scope checks

Checked 2026-10-04 UTC.

## Authoritative target and prior solution

1. W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)* (2018), [arXiv:1809.07200](https://arxiv.org/abs/1809.07200). Printed p. 134 (PDF page 135) contains Problem 6.44 and Update 6.44. The exact target is closure of `S_R` under `sum a_n b_n z^n/n`. The update explicitly identifies a negative solution by Bshouty and cites a Jenkins result through Pommerenke's book. Both the equation and update were read in extracted text and visually checked on the rendered page.
2. D. Bshouty, *A note on Hadamard products of univalent functions*, Proceedings of the American Mathematical Society **80** (1980), no. 2, 271–272. [DOI:10.1090/S0002-9939-1980-0577757-X](https://doi.org/10.1090/S0002-9939-1980-0577757-X). The publisher-deposited Crossref metadata confirms author, title, date, pagination and abstract: a modified Hadamard product of normalized real-coefficient univalent functions need not be univalent. The full paper was **not read**: AMS requests returned 403, the cloud browser reported a client block, and JSTOR did not yield the PDF. An Internet Archive copy was identified but marked access-restricted, so its private files were not requested. The exact matching of Bshouty's published result to the target relies on Hayman–Lingham's explicit Update 6.44, not on an inference from the title.

## The coefficient theorem actually used

3. A. Pfluger, *The Fekete–Szegö inequality by a variational method*, Annales Academiae Scientiarum Fennicae, Series A I Mathematica **10** (1985), 447–454. [DOI:10.5186/aasfm.1985.1049](https://doi.org/10.5186/aasfm.1985.1049); [publisher PDF](https://www.acadsci.fi/mathematica/Vol10/vol10pp447-454.pdf). Equation (1), p. 447, gives the sharp bound for the full normalized univalent class, with parameter `0 <= lambda < 1`; substituting `lambda=1/2` yields `1+2/e^2`. The page was visually inspected. This is a primary research paper furnishing a proof of the classical theorem, not just a database citation.
4. M. Fekete and G. Szegő, *Eine Bemerkung über ungerade schlichte Funktionen*, Journal of the London Mathematical Society **s1-8** (1933), no. 2, 85–89. [DOI:10.1112/jlms/s1-8.2.85](https://doi.org/10.1112/jlms/s1-8.2.85). Original theorem attribution; bibliographic metadata verified on the journal page. The 1933 full text was not needed or read.
5. A. Vasudevarao, *Fekete–Szegö inequality for certain spiral-like functions*, C. R. Acad. Sci. Paris, Ser. I **354** (2016), 1065–1070. [DOI:10.1016/j.crma.2016.09.008](https://doi.org/10.1016/j.crma.2016.09.008). Equation (2.1), p. 1067, independently states the same full-class classical inequality. Its definition of `S` and equation were visually checked. This corroboration is not needed once reference 3 is used.

## Catalogue and repository checks

- [Catalogue target](https://www.unsolvedmath.com/problems/2306044): the live page returned 403 and could not be used as the source of the mathematical statement.
- The recovered dataset record and prior report describe the exact weighted-convolution problem but incorrectly say no resolution was found in Hayman's 2018 edition. The explicit Update 6.44 overrides that obsolete triage claim.
- Live `AlecKriebel/Math` main was checked for its repository instructions, queue, state and related-target groups. The row was rank 584, queued, 0/5; it had no state record. No existing `attempts/2306044` directory was returned. Searches found no matching branch or pull request. No related-target group listed this ID.
- Problem 6.45 concerns strongly starlike subclasses and Problem 6.56 concerns quasiconformal extensions. Neither is settled by this counterexample; no other row is changed.

## Provenance fingerprints

Private reading copies were not included in the public deliverables.

| Source | SHA-256 |
|---|---|
| Hayman–Lingham PDF | `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0` |
| Pfluger PDF | `6da2e2921429ccd17256868cbc8c8dba2937e987af9068aaf4129bfc49c20adb` |
| Vasudevarao PDF | `2058aa43e4de490edbeb4ac91c39fa9f82879e8c80003895e868e35695e2016c` |

The proof does not depend on a numerical search, the dataset's classification, the inaccessible Bshouty proof, or an assertion of novelty. Its external mathematical dependency is the verified Fekete–Szegő theorem in reference 3.
