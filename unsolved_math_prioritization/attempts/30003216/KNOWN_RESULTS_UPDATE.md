# Additional primary-source checks during turn2

The complete primary 2024 paper by Adhikari, Kim, Lee and Sheen, *An efficient flux-variable approximation scheme for Darcy's flow*, Numerical Methods for Partial Differential Equations40(6), e23120, DOI10.1002/num.23120, was obtained from the NSF Public Access Repository. Its section3.2 treats the hybrid method as one augmented-Lagrangian Uzawa step and analyzes a Schur-complement pressure update. Section4 studies parameter-dependent approximation errors. Thus the broad Schur/Uzawa interpretation and small-parameter strategy in TURN_2 are explicitly credited classical inputs. This paper's numerical section uses uniform meshes; it does not supply the missing OWR adaptive rule.

The primary publisher page for Adhikari, *A reduced mixed finite element method with a priori and a posteriori error analysis*, JCAM486 (November2026),117609, DOI10.1016/j.cam.2026.117609, was available on the research date. Its abstract/introduction describe an iteration and an adaptive Alonso-estimator construction. The full paper was not recovered. The visible material does not establish which convergence theorem or two-mesh coupling it proves, so neither a resolution nor a non-resolution of the exact OWR target is inferred. Its forthcoming issue date is retained rather than silently changed.

The institutional primary copy of Carstensen–Hoppe, *Error reduction and convergence for an adaptive mixed finite element method*, Math.Comp.75(2006),1033–1042, was recovered and read. Its error-reduction argument uses bulk marking together with a separate data-reduction requirement. Those hypotheses cannot be dropped when transferring the framework to a perturbed flux. The turn2 marking statement keeps a valid conservative mixed convergence theorem as an explicit conditional input, rather than assuming that every residual-based marking loop converges.

Primary links:
- https://par.nsf.gov/servlets/purl/10535958
- https://onlinelibrary.wiley.com/doi/10.1002/num.23120
- https://www.sciencedirect.com/science/article/abs/pii/S0377042726002529
- https://edoc.hu-berlin.de/bitstreams/b245c06f-a852-485c-bac4-20ffe662986c/download

Full source PDFs, extracted text and page images are local reading copies, excluded from the public research checkpoint. Source lookup itself was not counted as an additional substantive turn.
