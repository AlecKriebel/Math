# Mandatory source and output clarification

This additive qualification is part of the accepted public report. It does not change any mathematical proof. Read it together with author/REPORT.md and author/CORRECTIONS.md. The original report and independently reviewed audit are preserved byte-for-byte.

There are two separate qualifications. Hart (2003), page 2, summarizes the k-orientation bound as O(n log k+k²), whereas Kavitha–Varadarajan (2003), page 1, and the author bibliography state O(n+k²); the full 1999 paper's conventions have not been checked here. Input orientation grouping and output reporting are different costs. In particular, the expanded ordered edge output on unsorted two-direction input can require Ω(n log n) comparisons by Proposition 7, even though the length or compressed path in that elementary case is available in O(n). The imported bounds are therefore not asserted for every input/output convention.

The 1999 paper and full 2020 thesis remain uninspected. No linear or orientation-sensitive bound is asserted for every input/output convention.
