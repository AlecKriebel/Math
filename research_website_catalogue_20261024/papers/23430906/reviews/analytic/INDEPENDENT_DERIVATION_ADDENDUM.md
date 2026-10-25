# Correction to one excluded-endpoint control; canonical input verified

2026-10-25 UTC (exact checkpoint time in RESEARCH_LOG.md). Preserve the original first seal and all sealed artifacts unchanged.

The first independent controls output and section 7 of the sealed derivation incorrectly described the H=1 polygonal half-correction variance as T^4/4. This is an error in this review's excluded-endpoint control, not in the submitted reader. Static inspection of the deposited original finite checker exposed the disagreement; direct exact recalculation resolves it:

    B_t^i=t Z_i,
    Delta_k B^i=(T/m)Z_i,
    Q_m=(1/2)m(T/m)^2 Z_1Z_2=T² Z_1Z_2/(2m),
    E Q_m²=T^4/(4m²) ->0.

The initial comment accidentally dropped m^(-2). The corrected exact controls are in `endpoint_correction.py` and its output. At H=1, **the correction does converge to zero**; failure of the claimed positive witness bound there is due to D_H divergence and endpoint recoverability X_T=B_T^1B_T^2/2. The statement about H=1 in the first output/derivation is superseded. All central open-interval tensor, Fourier, Gram and pairing steps, and all exact polynomial outputs, are unaffected. No theorem or source bytes were edited.

Primary canonical input now directly checked from fresh author-institution `sources/primary-cache/ntu_journal.pdf` (1211802 bytes; SHA256 3f7467eea58ebf6998981bf0337a579f45ad1db1c544273eb955507fe2e55c68): introduction fixes independent standard fBm and H∈(1/4,1); Proposition 6, printed p229, gives L^p convergence of analytic first and second levels and Chen's identity; Remark 10, printed p230, identifies the canonical linear-interpolation construction; Theorem 2, printed p226, bounds the actual trapezoid/polygonal error by C(H)T^(4H)n^(1-4H), and its full proof on printed pp237–240 uses diagonal/adjacent O(n) terms plus off-diagonal cancellation. For the lower theorem here only the existence and canonical identification are imported, and the independent Q_m argument already proves the needed left-sum convergence without exact Euler coefficients.

The same institutional source's equation (26), pp234–235, gives the positive separated-cell integral. Its equations (29),(30), pp236–237, retain all fixed positive lags in the leading coefficient and discard only the tail after log n. The pinned arXiv v1's equation (27), printed p12, discards all separated lags at the leading rough scale. The fixed lag-2 covariance lower bound H²(2H-1)²3^(4H-4)/4>0 (H≠1/2) contradicts that little-o assertion, as the reader states. This criticism is version-specific; no journal exact-coefficient theorem is certified by this review.
