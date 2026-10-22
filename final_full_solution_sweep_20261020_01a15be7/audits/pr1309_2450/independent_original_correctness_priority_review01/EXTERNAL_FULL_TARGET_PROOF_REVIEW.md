# Existing full public proof of the explicit uniform c/n subquestion

I independently retrieved Geng and Qiu, arXiv2609.06461v1, and read the complete
Section 2 argument, Lemmas 2.1–2.2, Proposition 2.3 and Corollary 2.4, including
the latter's proof on physical page 5. The relevant mathematical body spans
physical pages 2–5. Its definitions and source context on pages 1–2 and its
declarations/references on pages 16–17 were also read. The full PDF was retained.
This is not a claim to have independently audited Sections 3–7 or their stronger
sharp pi/2 limiting theorem, and no Lean package was built.

The checked Section 2 is a complete proof of the original explicitly stated
uniform c/n question, not merely a lemma conditional on the later asymptotic
theorem. Corollary 2.4 proves the stronger root-centered open radius
T_n=2^(1/n)−1>log(2)/n for every n≥1. It therefore supplies actual full-target
coverage for this subquestion in the identified preprint DOI.

I checked its kernel argument independently. The real-Hilbert-space conjugation
convention is consistent: with h_m=delta_(m,0)−conj(lambda)b_m,
H_m=conj(h_m), S_m=sum v_j^m, the stated real inner product equals
Re(sum S_m h_m)=n. Its Blaschke multiplication telescoping identity is correct;
the terminal d|t_N|² tends to zero, by first truncating the input in l² and
using the norm bound for the tail. Alternatively finite rational Blaschke
products give the same norm directly by Parseval as in my independent proof.
The logarithmic derivative sign and constants give the torus bound, and only
the off-diagonal product is extended coordinatewise.

The improvement over PR1309 uses weighted pairing. Let A=1+t, B=sqrt(A), and
a=A^(−1). Then
(XY+t²)²≤(X²+t²/A)(Y²+t² A), with difference
t²(sqrt(A)X−Y/sqrt(A))². The regularization lengths are t/B=B−B^(−1)
for the roots and tB=A(B−B^(−1)) for the w-points. If m=n(n−1)/2 and
J=(1−a^n)/(1−a), the two separation bounds have factors A^m J^n and
A^(3m) J^n. Together with the diagonal t^(2n), they yield
V²≤(t A^(n−1)J)^(2n)=(A^n−1)^(2n). Every cancellation is exact.

For the endpoint disk, if all finitely many open T_n disks failed, each supplies
a bad point. The maximum of the finitely many distances is t<T_n. The matched
bound then contradicts V≥1. If t=0 all bad values would be root values zero,
already impossible; the separate t=0 proposition also handles it. This avoids
any compactness/strict-endpoint ambiguity. The outward points 2^(1/n)z_j for
z^n−1 obstruct larger universal zero-centered radii. Repeated roots, n=1 and
boundary roots are allowed. No later theorem or computer code is needed.

The actual arXiv body credits Price's announcement, Sothanaphan's product
explanation, Bloom's matched inequality, and Kitamura's May public code. These
are not journal publications. The browser reader initially returned access
errors for the forum, but a later native GET succeeded: I read the entire current
problem body and all 16 forum comments, including Price's May 7 announcement,
Sothanaphan's May 8 explanation and Bloom's May 11 matched-product statement.
The advertised Price Overleaf PDF remains inaccessible and was not read.
The forum's linked Sothanaphan streamlined note was then retrieved through the
Google Drive plugin; its complete five-page body was read and checked, with
visual verification of conjugations and grouping on pages 2 and 3. That earlier
public conventional proof also establishes the entire c/n target. See
MAY_NOTE_REVIEW.md for the precise dates and attribution limits.
The registered Geng–Qiu preprint is the independently authenticated public
conventional proof used for the proposed DOI record.

No exclusive novelty, journal acceptance, formal Lean certification, current
tracker status or whole-paper sharp-asymptotic verdict follows from this review.
