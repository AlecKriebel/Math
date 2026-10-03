# Source and scope check

## Exact question

The authoritative source is Daniela Cadamuro, “The massive modular Hamiltonian
for a double cone,” in *Mini-Workshop: Standard Subspaces in Quantum Field Theory
and Representation Theory*, Oberwolfach Report 50/2023, printed pp. 2861–2864,
[DOI 10.4171/owr/2023/50](https://doi.org/10.4171/owr/2023/50).
The question is on printed p. 2862, immediately after equation (7):

> Is M− mass independent? Is M− a multiplication operator?

The passage concerns a real free scalar field of positive mass, the vacuum, and
a double cone. Its displayed Cauchy-data formula is a continuum spectral-calculus
formula, with closures/domain conditions. The next page reports numerical
evidence; the preceding page explicitly disclaims rigorous approximation bounds.
The source discusses one and three spatial dimensions. This investigation fixes
the unit interval/ball and never silently replaces the full operator by a
finite matrix or an angular-momentum sector.

The problem page [30005723](https://www.unsolvedmath.com/problems/30005723) could
not be accessed by the web tool. The pinned catalogue record was read locally;
the above statement and equations were independently checked in the official
MFO PDF, including an image of printed p. 2862. The catalogue’s original fragment
mentions p. 2863, whereas the two questions actually appear on p. 2862. No matching
prior report was found in the pinned research-results file by ID, code, or title.

## Primary literature checked

1. H. Bostelmann, D. Cadamuro, C. Minz, *On the mass dependence of the modular
   operator for a double cone*, Ann. Henri Poincaré 24 (2023), 3031–3054,
   [arXiv:2209.04681v3](https://arxiv.org/abs/2209.04681), especially Proposition
   2.3 and Sections 3 and 7. Their computations suggest mass and angular-momentum
   dependence but provide no convergence theorem for the finite approximations.
   Small off-diagonal contributions remain inconclusive. Their formula, not
   their plots, supplies the operator notation used here.
2. R. Longo, G. Morsella, *The massless modular Hamiltonian*,
   [arXiv:2012.00565v4](https://arxiv.org/abs/2012.00565), introduction and final
   Errata. The massless formula is retained; the authors explicitly withdraw the
   earlier positive-mass analysis after a gap was identified. It is not a valid
   proof of the massive assertion.
3. F. Figliolini, D. Guido, *The Tomita operator for the free scalar field*,
   Ann. Inst. H. Poincaré Phys. Théor. 51 (1989), 419–435,
   [primary archive](https://www.numdam.org/item/AIHPA_1989__51_4_419_0/),
   Theorems 4.1 and 4.4. Mass-continuity of modular operators/groups is available
   in their common one-particle realization. This is not, without further work,
   convergence of the unbounded time-zero block on prescribed test vectors.
4. M. B. Fröb, *Relating the modular Hamiltonian to two-point functions*,
   [arXiv:2501.09669](https://arxiv.org/abs/2501.09669), equations (1.7)–(1.9),
   Section 2. This gives another spectral representation, including precise
   restricted-region constructions. It does not evaluate the massive-ball
   spectrum or answer the present two questions.
5. S. Hollands, R. Longo, G. Morsella, *Bekenstein’s bound for wave packets*,
   [arXiv:2602.03606v1](https://arxiv.org/abs/2602.03606), introduction and
   Section 3.1. This recent primary source still describes the explicit massive
   ball generator as unavailable and proves bounds, not a multiplication formula.
6. R. Arias, D. Blanco, H. Casini, M. Huerta, *Local temperatures and local terms
   in modular Hamiltonians*, [arXiv:1611.08517](https://arxiv.org/abs/1611.08517),
   Section 4, especially the scalar discussion around (80)–(81). Its high-energy
   reasoning and numerical evidence concern the leading local part. They cannot
   be substituted for an exact theorem about the entire scalar block. The
   explicitly worked small-mass appendices concern fermions.
7. C. Minz, E. Tonni, *Modular Hamiltonian for the massive scalar field on the
   half line: a numerical approach*, [arXiv:2512.04659](https://arxiv.org/abs/2512.04659),
   [published record](https://repo.scoap3.org/records/110290). The boundary geometry
   and numerical status differ from the present continuum full-space problem.

Searches were made on 3 October 2026. No verified resolution of the full target
was located. This is a dated search conclusion, not proof that no such work exists.

## Duplicate and normalization checks

The main queue still listed this target at rank 491, 0/5, when read. Repository
code search, the attempt-directory listing, and related-target groups returned
no mathematically identical earlier attempt. A catalogue search located related
QFT questions 30000341, 30002834, and 30002835; they concern nontriviality of local
observables, minimal-length nets, and Bisognano–Wichmann covariance respectively,
not either question here.

We use spatial dimension n and radius 1 throughout. Some source prose writes a
general-radius parabola without a radius denominator. Rather than import that
normalization ambiguity, the scaling relation is derived directly in Attempt 3.
The unit-radius identities used in this package are unaffected.

