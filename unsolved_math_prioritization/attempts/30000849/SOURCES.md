# Source and normalization audit

Checked 2026-10-01. This is a mathematical source reconstruction, not a claim
that no later work exists. PDF hashes are in source_manifest.json; full PDFs
remain outside the public packet.

1. F. P. da Costa, joint work with J. T. Pinto, R. Sasportes, H. van Roessel and
   J. A. D. Wattis, *Convergence to self-similarity in addition models with input
   of monomers*, OWR46/2007, printed2754–2756 (PDF28–30), DOI
   https://doi.org/10.4171/owr/2007/46.
   Full report: https://publications.mfo.de/bitstream/handle/mfo/3032/OWR_2007_46.pdf?isAllowed=y&sequence=1
   The complete contribution and the actual equation/conjecture images were
   inspected. Its equation(1) prints birth j^(p-1), whereas its immediately
   following p=0 triangular equation uses birth1. Conjecture1 explicitly
   defines the size scale as a positive constant times t^((2+omega)/(3-2p)),
   uses amplitude exponent r_p=[1-omega(1-p)]/[(2+omega)(1-p)], and gives
   eta^-p(1-eta^(1-p))^-r_p on0<eta<1. The eta^-p factor is outside the
   r_p power. The scale constant Q_p is not specified explicitly for general
   p; the bare r in the initial decay condition is not defined there.
   The tilde notation is introduced earlier as a time composition alone.
   The p=0 theorem is credited and not challenged. The nonconstant-rate
   formal extension cites unpublished2007 notes in reference8.

2. F. P. da Costa, *Mathematical Aspects of Coagulation-Fragmentation Equations*,
   published in *Mathematics of Energy and Climate Change*, Springer2015,
   pp.83–162, DOI https://doi.org/10.1007/978-3-319-16121-1_5.
   Complete author repository copy, internally numbered1–74:
   https://repositorioaberto.uab.pt/bitstreams/e7050fb6-aa7f-4674-a271-8b8b93d28c0f/download
   Repository metadata: https://repositorioaberto.uab.pt/entities/publication/4aa88b30-5b59-42fb-a453-5cb572019206
   Read the full relevant section, internal pp.57–60, and reference51 onp.68.
   Equation(123) uses birth a_(j-1), so a_j=j^p gives (j-1)^p. Theorem19
   concerns constant coefficients. The subsequent nonconstant-rate paragraph
   still presents formal rather than proved scaling and cites the OWR item.
   Its tau-versus-varsigma notation and exchanged labels for constants do not
   provide a clean alternative normalization theorem. We do not treat that
   paragraph as a proof, or assert that every edition has identical typography.
   The rendered repository PDF has missing Greek glyphs in this environment;
   its extracted text and the clear original OWR images were both checked.

3. R. Sasportes, *Dynamical Problems in Coagulation Equations*, complete thesis,
   repository record https://repositorioaberto.uab.pt/entities/publication/3213a56b-3308-4762-a7e7-27f8d71e0b19,
   handle http://hdl.handle.net/10400.2/1909, full PDF in source_manifest.
   This is relevant to the constant-coefficient/slow-input analysis. It was
   searched for the nonconstant-rate conjecture and does not supply a located
   proof of the displayed general-p statement. No claim to have audited every
   theorem of the thesis is made.

4. F. P. da Costa, J. T. Pinto and R. Sasportes, *Rates of convergence to scaling
   profiles in a submonolayer deposition model and the preservation of memory
   of the initial condition*, https://arxiv.org/abs/1508.03013,
   full author PDF https://arxiv.org/pdf/1508.03013. The equations and scope
   at pp.1–3 have constant aggregation rates with a critical cluster size;
   they do not resolve the displayed general-p normalization.

Current searches included the exact unpublished-note title, the authors'
publications, and size-dependent addition scaling. The 2008 AIP author-uploaded
abstract/full-text rendering (DOI10.1063/1.2991089) also treats constant
coefficients and cites the variable-rate work as unpublished. No source was
located that supplies a proved corrected version of the exact target. This
is a bounded literature check, not a priority certificate.

The imported record's clean version correctly recovers the profile's
parentheses, but its 'corrected_verified' label is not proof that its other
normalization conventions are mathematically consistent. Its original version
has a different malformed profile expression. The candidate uses the actual
OWR display and explicitly handles the standard physical equations as well.
