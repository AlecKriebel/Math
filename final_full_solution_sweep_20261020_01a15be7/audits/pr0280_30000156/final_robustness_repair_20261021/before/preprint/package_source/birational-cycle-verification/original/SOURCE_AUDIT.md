# Exact source, literature, and prior-attempt gate

Checked 2026-10-01. Target 30000156 / OWR-768-006, queue rank 303.

## Original target

The full primary report is *Finite Fields: Theory and Applications*, Oberwolfach Report 54/2004, DOI 10.4171/OWR/2004/54. The workshop ran December 5–11, 2004; the imported citation's 2005 label must not change the workshop or conjecture date. Vivaldi's contribution, joint work with John A. G. Roberts, is printed pp.2944–2945 (PDF pages 32–33). The entire contribution was read, and p.2944 visually inspected.

[Full institutional report PDF](https://publications.mfo.de/bitstream/handle/mfo/2873/OWR_2004_54.pdf?isAllowed=y&sequence=1)

[Author's complete two-page version](https://webspace.maths.qmul.ac.uk/f.vivaldi/research/Oberwolfach.pdf)

The source starts with rational invertibility and algebraic integrability, permits coefficients in a number field, fixes the finite-field extension degree and lets the characteristic grow through a suitable positive-density set of primes. It then takes q=p for its displayed definition. Its D_p is the probability for a uniformly selected **point**, normalized by p², with threshold px. Conjecture 1 asserts existence for every birational map. The later genus-one heuristic, single-reversing-family clause and separate p²-scaled prime average are not hypotheses of that universal statement.

The candidate uses a polynomial forward map with a rational inverse. On p≡3 mod4 the inverse denominator has no zero anywhere in F_p², so it supplies an actual full-plane permutation. I(u,v)=u is a nonconstant rational first integral with unchanged degree, and the map's degree does not drop. This prime class is a standard positive-density Chebotarev class for Q(i), not a thin set chosen to conceal exceptional points. The two incompatible subsequences both lie inside that fixed class. No projective exceptional-point convention is required for this polynomial forward map and the explicitly affine statistic.

The source does not require that the rational inverse be polynomial over C. The candidate does not satisfy that stronger condition and does not pretend otherwise. If a different intended conjecture adds it, that is outside the exact imported target.

## Arithmetic inputs actually used

Lorenzo Menici and Cihan Pehlivan, *Average r-rank Artin conjecture*, Acta Arithmetica 174(3) (2016), 255–276, DOI 10.4064/aa8258-4-2016. [Full published PDF](https://www.impan.pl/shop/en/publication/transaction/download/product/91625).

- Equation (1), printed p.255, explicitly states the unconditional prime-average totient asymptotic, with credit to Stephens; p.255 was visually checked.
- Lemma 2 and its full proof, pp.262–263, give the precise mean argument. With r=m=1 its Jordan totient is the ordinary φ and the Euler-product constant is Artin's constant. These pages were read in full.
- The proof explicitly states the uniform Siegel–Walfisz estimate for π(X;1,d). The candidate reproduces only its elementary truncation specialization and uses fixed d=4 for the progression split. No GRH assumption from other parts of the article is imported.
- Stephens's 1969 original paper was located bibliographically but its full text was not accessed. This is disclosed rather than representing a publisher preview as a full read.

Dirichlet infinitude in a reduced arithmetic progression, Euler's product over primes, finite-field multiplicative cyclicity, and elementary Gauss/Jacobi sums are classical inputs. The candidate proves the character identities, primitive-element indicator, crude ω bound and needed Euler-product lower bound explicitly, avoiding a hidden reliance on Artin's unproved fixed-base primitive-root conjecture.

## Nearby later literature

1. Roberts–Vivaldi, *A combinatorial model for reversible rational maps over finite fields*, Nonlinearity 22 (2009), 1965–1982, DOI 10.1088/0951-7715/22/8/011. [Complete arXiv v1](https://arxiv.org/pdf/0905.4135). The introduction and Theorems A/B were read for exact scope. Theorem A averages over **random pairs of involutions** on a finite set with prescribed fixed-point counts. It does not prove a prime-by-prime limit for each fixed birational map. The final publisher version was not accessed here.
2. Jogia–Roberts–Vivaldi, *An algebraic geometric approach to integrable maps of the plane*, J. Phys. A 39 (2006), 1133–1149, DOI 10.1088/0305-4470/39/5/008. [Complete author version](https://web.maths.unsw.edu.au/~jagr/IntegrabilityRS.pdf). Introduction and the full finite-field discussion on author pp.13–15 were read. Its foliation-of-elliptic-curves, fixed-orbit density, and normalized periodic-point discussions are more specialized. We neither replace the OWR target by one of these variants nor claim to refute the paper's proved theorems.
3. Targeted current searches for the numeric/source ID, exact conjecture, birational cycle nonconvergence and totient mechanism found no verified exact prior counterexample. This is a bounded literature check, not a historical novelty certificate. No external executable or outreach was used.

## Campaign gate

The full pinned record and empty upstream report were read. Pin: ulamai/UnsolvedMath revision 37e53eabe540fb458758e198be61634bd02ee008.

- Statement SHA256: d35548befccb38900fe4d2c6574ef4e42574050421b200153694adfc4f47d587.
- Sorted JSON [record, report] SHA256: 231b10daf3e6ef548a06a0a8a657cf2c0de0eaa82592300bdddd4ab0ac95f22b.
- Live all-state AlecKriebel/Math PR searches for the exact ID/source and broader birational/cycle phrase returned no prior attempt.
- Dedicated-branch search returned none; both possible target attempt-path commit histories were empty.
- Local all-ref target history and related-target groups had no entry; QUEUE row was queued 0/5.

Source work preceded the substantive turn. Turn 1 developed the single fiberwise-multiplication/totient-oscillation mechanism, replacing the initial (u,uv) probe by the everywhere-permutational (u,(u²+1)v) construction on the fixed admissible prime class. This is one substantive author turn, not several tool-call turns.

Downloaded PDFs, extracts, images and full imported records are reading copies and must not be published with the proof packet.
