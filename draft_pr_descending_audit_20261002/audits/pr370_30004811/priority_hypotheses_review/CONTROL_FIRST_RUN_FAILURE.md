# Preserved first distinct-control failure

2026-10-03 11:36:17 UTC: The first run exited1 in the auxiliary boundary-mean-curvature sign control. SymPy raised `TypeError: cannot determine truth value of Relational: 2*r*(r + 1)/(r - 1)**3 > 0`.

The script had declared only r>0, whereas the negative-mass Schwarzschild exterior requires r>1 in the m=−2 specialization. The mathematical reconstruction already imposed R₀>|m|/2; the control omitted that domain in its symbolic assumptions. The preceding14 controls (including the entire exact radial volume integration and the boundary flux identity) had passed. Correction: substitute r=1+t with t>0, then test positivity. This is an audit-control correction, not a discovered candidate defect. The failure has not been erased from the research record.
