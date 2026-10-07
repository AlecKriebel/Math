# Separately credited presentation clarifications

The independent audit supplied these two optional clarifications. They are adopted as explanatory notes here; neither frozen packet nor any authored proof is edited.

1. The stationary positive result of Erath and Praetorius, *Optimal adaptivity for the SUPG finite element method*, CMAME 353 (2019), 308–327, is substantial. The optimal-rate assertion in Theorem 4.5 requires 0 < theta < (1+C_stb^2 C_drl^2)^-1. Its linear-convergence theorem has the broader range 0 < theta <= 1. These are eventual/asymptotic conclusions under the paper's other hypotheses, not parameter-uniform preasymptotic guarantees. See [primary manuscript](https://arxiv.org/abs/1806.11000) and [journal DOI](https://doi.org/10.1016/j.cma.2019.05.028).
2. Proposition 5.3 is read in the real Gelfand-triple setting of Proposition 5.1, with a time-independent bounded linear coercive operator A: V -> V'. Bounded linearity and the standing setting are inherited assumptions used in the existence argument. The proposition concerns an unrefined time grid and does not rule out successful time adaptivity.

Credit: the independent audit's CORRECTIONS.md and full AUDIT_REPORT.md; both are retained byte-for-byte in independent_audit/.
