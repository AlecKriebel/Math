# Source gate: simpler proofs of infinite Toeplitz total positivity

Checked 21 October 2026. Queue row 1839; ID 30005048; source key OWR-9790364-002.

## Verdict

The mathematical object and the proof-simplification question are recovered. The classification itself is an established theorem, not a conjectural equivalence. No new resolution of the 2022 request for a more straightforward proof was verified. A non-Nevanlinna, representation-theoretic proof already existed and was explicitly mentioned by the question. Therefore neither “the theorem is open” nor “no proof avoiding complex function theory exists” is an accurate status. The exact permitted toolkit for “elementary” is unspecified in the primary question. This is a methodological open request with an imprecise success criterion, not an unrecoverable assertion.

## Primary provenance

Alexander Dyachenko, joint with Alan Sokal, “Total-positivity characterization of the Laguerre–Pólya class LP+,” printed pp.661–662 in *The Laguerre-Pólya Class and Combinatorics*, Oberwolfach Reports 19 (2022), no.1,657–681. Workshop 13–19 March 2022; publication 11 March 2023. [Official EMS record](https://ems.press/journals/owr/articles/9790364), [official PDF](https://ems.press/content/serial-article-files/46952?nt=1), DOI [10.4171/OWR/2022/13](https://doi.org/10.4171/OWR/2022/13). The relevant printed page661/PDF page5 was locally rendered and visually inspected, and pp.661–662 extracted text was read.

The question sits immediately after the Aissen–Edrei–Whitney–Schoenberg quotient classification. It asks whether the complex-analytic techniques of Edrei's 1952 and 1953 papers can be replaced by something “more straightforward,” and explicitly asks about Okounkov's proof. It is not attached to the later theorem that the speakers announce proving by real analysis.

## Exact object and quantifiers

1. The class is LP+, the nonnegative-coefficient, negative-zero branch of the Laguerre–Pólya type-I class, not the unrestricted real-zero/type-II class. The canonical form is

   F(z)=C z^m exp(γz) ∏(1+α_i z), with m≥0, C≥0, γ≥0, α_i≥0, and ∑α_i<∞.

   For nonzero F take C>0; the zero function is a degenerate member. Standard approximating polynomials have positive leading coefficient and all zeros nonpositive, with convergence locally uniform in the complex plane. The report's compressed language says uniform convergence and negative-real-rooted; its explicit z^m factor includes zero roots. The choice of sign, and γ≥0, matter. Functions such as exp(−z²), although in the larger LP class, are not the target.

2. For a real one-sided coefficient sequence a=(a_n)_{n≥0}, extend a_j=0 for j<0 and define T(a)=(a_{n−k})_{n,k≥0}. Its transpose is equally valid. These are ordinary Taylor coefficients A(z)=∑a_n z^n, not exponential-generating coefficients a_n/n!. Total positivity in this report means every finite square minor of every order is nonnegative, often called total nonnegativity or PF∞. It does not mean strictly positive minors; a triangular matrix necessarily has zero minors. There is no fixed maximum order r, no single finite Toeplitz section, and no continuous translation kernel being classified here.

3. The clean nondegenerate normalized statement takes a_0=1. Then T(a) is totally nonnegative if and only if, in a neighborhood of zero,

   A(z)=exp(γz) ∏_i(1+α_i z) / ∏_i(1−β_i z),

   γ,α_i,β_i≥0 and ∑_i(α_i+β_i)<∞.

   Products can terminate. For a general nonzero sequence, factor off its initial zero coefficients and positive leading coefficient, adding C z^m. The zero sequence is separate. This is the precise one-sided meaning of the report's compressed F(z)/G(−z), F,G∈LP+: the denominator must define an analytic nonzero germ at zero (take G(0)>0), and it is not the zero function. A denominator factor at zero cannot be allowed without first cancelling and checking the resulting ordinary power series. Any exponential factor of G contributes positively to γ after division by G(−z).

4. The report also gives the entire-function corollary: Toeplitz total nonnegativity together with coefficient-ratio limit a_{k−1}/a_k→∞ characterizes LP+. For an infinite-support nonzero PF∞ sequence the eventual coefficients are positive, so this ratio is meaningful and says the radius is infinite. Finite-support sequences/polynomials must be handled separately, rather than interpreting an eventual 0/0. For a given entire function A with nonnegative coefficients, the characterization is A∈LP+ iff T(a) is totally nonnegative. The general quotient theorem permits positive real poles; it is stronger than this entire case.

The normalized full formula and the finite/one-sided/two-sided distinctions are independently confirmed in Sokal's [13 March 2015 QMUL slides](https://www.qmul.ac.uk/maths/media/maths/research/sokal.pdf), slide6. Those slides ask for a more elementary proof of the infinite cases and identify Nevanlinna theory as the heavy analytic input. Their web crawl/upload date is not the talk's date. The two-sided extension in those slides is broader background, not a reason to replace the one-sided power series in the recovered report by a bilateral Laurent problem.

## Direction that needs simplification

The quotient/product ⇒ nonnegative minors direction follows from elementary totally nonnegative building blocks, multiplication of Toeplitz matrices/convolution, Cauchy–Binet, and coefficientwise limits. The difficult direction is arbitrary PF∞ sequence ⇒ the stated analytic product/quotient classification. In the standard approach the central remaining hurdle, after extracting zeros and poles while retaining positivity, is to prove that a zero-free entire PF∞ generating function is just exp(γz), not exp(h(z)) for a general entire h. Establishing both infinite extraction and this residual rigidity without importing an equivalent classification is necessary for a complete replacement proof. Simply citing Edrei, Thoma, or the complete LP+/PF∞ equivalence proves the known theorem, not the requested proof simplification.

This allocation of the hard direction is mathematical interpretation supported by the primary proofs, rather than a separately quantified one-direction problem in the question. The report asks about the proof techniques of the full theorem.

## Existing alternatives and circularity traps

**Okounkov is already part of the question.** [*On the representations of the infinite symmetric group*, arXiv:math/9803037v1](https://arxiv.org/abs/math/9803037v1), submitted11 March1998, contains two representation-theoretic approaches. Its introduction explicitly advertises avoidance of deep entire-function theory. Sections2.3–2.4 were inspected, especially Proposition5 and manuscript pp.27–31. Proposition5 links normalized PF∞ sequences to characters of the infinite symmetric group using symmetric-group character identities. The second proof extracts factors, then uses a positive spectral measure μ on [−1,1] with cycle quantities c_k=∫t^{k−1}dμ. For a zero-free entire residual H, H′/H is entire. Positive mass away from zero would give c_{2k+1}≥const·ε^{2k}, contradicting infinite convergence radius. Thus μ is supported at zero and the residual is exponential. The spectral-measure/representation-theoretic construction is substantive and cannot be silently treated as elementary algebra or as a consequence of the theorem being proved.

This existing argument means that the weak interpretation “avoid Nevanlinna theory by any method” already has an affirmative answer. It does not establish that the authors' stronger, informal request for a more straightforward proof has newly been met. The OWR citation conflates bibliographic data: its title and J.Math.Sci.96(5),1999 correspond to pp.3550–3589, not the printed100–107. The 1994 shorter paper *Thoma's theorem and representations of an infinite bisymmetric group* has pp.100–107. The manuscript above and the [2026 Rietsch survey bibliography](https://epubs.siam.org/doi/full/10.1137/25M1806727) disambiguate the two.

**The speakers' real-analysis theorem is different.** With θ=z d/dz, the report announces that T((α+θ)F) being totally nonnegative for an unbounded set of positive α implies F∈LP+. It is the (b)⇒(a) step in a list of equivalent multiplier conditions. This hypothesis tests a whole family of transformed sequences ((α+n)a_n), and is stronger than T(F) alone. The source calls this already obtained, not the open question. A proof of it cannot be substituted for Edrei's arbitrary PF∞ classification without proving the missing bridge.

**A recent elementary-looking restatement is not an independent proof.** Konstanze Rietsch, [*Totally positive Toeplitz matrices: classical and modern*, arXiv:2509.25163v3](https://arxiv.org/abs/2509.25163v3),13 October2025; [ICM2026 publication](https://epubs.siam.org/doi/full/10.1137/25M1806727),13 July2026. Its Introduction identifies zero-free exponential rigidity as the key classical step. Section2.6/Theorem2.17 gives a uniqueness statement for a divergence-free labeling of an infinite quiver by the multiplication table. It explicitly describes this as an application/equivalent restatement of Edrei, and its proof invokes Edrei's parameters. Using that uniqueness as an unexplained elementary lemma to reprove Edrei is circular. The newer asymptotic/quantum-cohomology and tropical parametrizations likewise are not presented there as a solution to the OWR request.

## Status, catalogue correction, and stopping boundary

The local corpus has exactly one matching problem record. Its cleaned statement drops the essential LP+ superscript and quotient/one-sided hypotheses; its title adds the stricter-sounding word “elementary.” Thus the field claiming preservation of all hypotheses should not be relied on literally. The original extracted passage puts the talk heading after the question due to extraction order, but the PDF fixes its placement. The catalogue's22 August2026 assessment says no later resolution was found; that is a dated search assessment, not evidence of a formally open equivalence. No matching research-results record was found.

A bounded fresh search checked the exact report, the existing Okounkov alternative, the dated Sokal slides, modern Edrei/Thoma proof searches, and the 2025/2026 Rietsch survey. No independently verified newer proof explicitly satisfying the report's request was located. This is not a proof that none exists. The appropriate working status is: **known characterization; proof-simplification request unresolved/criterion unspecified; non-complex-analytic alternatives already known**. Any future attempt should state its allowed toolkit, isolate the extraction and residual-rigidity lemmas, and audit their dependencies.

This gate is not a new proof. Only authored analysis and public-source verification metadata are included in this package.
