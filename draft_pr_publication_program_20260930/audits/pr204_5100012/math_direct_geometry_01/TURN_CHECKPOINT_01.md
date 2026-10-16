# Early independent checkpoint

2026-10-16T09:50:08Z.

Primary source independently read in memory: arXiv v11 pp.1-6 and journal pp.343-346. Both define signed shoelace areas, original-side feet, proper confocal ellipse billiard context and target table k203,b with N not congruent 2 modulo 4. Neither table literally says least/primitive. No other target proof or favorable report read.

Elementary chord reduction, with outer vertices p_i=(a cos t_i,b sin t_i), m_i=(t_i+t_{i+1})/2, d_i=(t_{i+1}-t_i)/2, D_i=cos²(m_i)/a²+sin²(m_i)/b²:

- Confocal tangency gives sin²(d_i)=lambda D_i.
- Side length l_i=2ab sin²(d_i)/sqrt(lambda).
- Original area A=ab sum sin(d_i) cos(d_i).
- Original-line foot q_i=(cos(d_i)/D_i)(cos(m_i)/a,sin(m_i)/b).
- Hence B=lambda²/(2ab) sum u_i u_(i+1)(u_i+u_(i+1)), u_i=cot(d_i).

The universal route is PARTIAL: it still requires proving phase constancy of (lambda²/2)[sum u_i/(1+u_i²)] [sum u_i u_(i+1)(u_i+u_(i+1))] under the physical Poncelet correspondence, with the parity restriction. This is an exact remaining scalar identity, not yet a telescoping argument.

For a centrally symmetric 4-orbit P,Q,-P,-Q the elementary formulas give A B=8 lambda², and adjacent caustic tangencies force lambda=a²b²/(a²+b²). Work continues to make the full period-4 coverage and exact checks explicit.

Bounded audit estimate 25%; universal direct-geometry discovery 15%. No universal proof claimed.
