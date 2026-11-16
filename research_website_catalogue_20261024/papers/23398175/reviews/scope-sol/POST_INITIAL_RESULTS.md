# Post-INITIAL completed checks — row 162

This is post-freeze work. The 14 source-first files remain unchanged. The two native proof-comparison bodies were read in full after the independent reconstruction: EXACT_BICENTRIC_DN_BRIDGE.md (9,887 B, f3be45b2523bc9a5a81110a9a2063085502bb67016e74aa5f46f268049038785) and CHECKABLE_TRANSFER.md (8,120 B, 3411d18d1505df8de7c9ea133b9bef8fabb26d33ce9f3cc6d6082c6a354a2a9e). Their historical-review paragraphs were inevitably exposed; their opinions are not acceptance evidence. The following are actual mathematical/interface checks.

## Supplementary dn bridge

The actual original-tangent intersection is V(z)=(-a^2 sn(z)/alpha,b^2 cn(z)/beta), verified by the same addition substitutions frozen initially. Its projective denominator a^2+cx is positive, since c<alpha. For its image R, (R_x-d_b)/R_b=(k-sn z)/(1-k sn z), R_y/R_b=k'cn z/(1-k sn z), matching the independently derived dual circle.

Put A=sqrt((1-k)/(1+k)), f(z)=A dn(z)/(1-k sn z), m_b=4k/(1+k)^2. Differentiation gives
f'=A k cn(z)/(1-k sn z),
f''=A k dn(z)(k-sn z)/(1-k sn z)^2
=((1+k)^2/4)((2-m_b)f-2f^3).
At z=K, f=1 and f'=0. The dn second-order ODE and initial-value uniqueness therefore give f(z)=dn((1+k)(z-K)/2,m_b), with parameter convention explicit. The relative-circle angle has derivative k'dn(z)/(1-k sn z)=(1+k)f(z), and value pi at z=K; this verifies the native circle-phase formula.

The squared tangent length, as an affine fraction in sn z, agrees at sn z=+/-1 with the independently calculated t_M^2,t_m^2; hence it is t_M^2 f(z)^2 identically. Real tangent lengths are positive by the already frozen star-sign argument. The area ratio frozen initially gives B_+=r_b^3 t_M/(R_b^2-d_b^2) times the dn cyclic sum. The native u phase, step 2K_b tau/N and focus shift K_b are consequently consistent. The Gauss formulas and K_b=(1+k)K also agree with actual KS precursor formulas (9)-(11), which use PARAMETER m=k^2.

Actual NIST DLMF 22.11.3 supplies a uniformly absolutely convergent real dn Fourier series. Summing its N equally spaced shifts kills every Fourier mode not divisible by N. The surviving coefficients have nome q_b^N, scale C=N K_N/K_b and argument Cu. This directly proves the cyclic reduction in the native bridge, independently of any weakness in an older proof presentation. Actual published-body KS Eq. (7), p. 923 states the same arbitrary-integer-order identity in reciprocal normalization; complete section 2.1 was read through its end on p. 926 in the exact cached published text. For odd N the focus shift advances the reduced argument by N K_N, a half period modulo 2K_N. The classical dn half-period product, also in DLMF Table 22.4.3, gives the same invariant. This checks the full alternative route without treating a projectivity as area preserving.

## Inverse transfer and cited fixtures

The actual six-page F62 primary was read completely by reference, raw SHA c7fbcc7e5a7b7746ad102cb7cf0f5e9eb6aa149009d88c3654fdbcc3484126c0. Its Lemmas 2-3 prove the same possible inverse-area pole row: at first inverse vectors have double poles, their two negative Laurent coefficients are parallel by isotropy, area order is at most two, and cyclic reversal removes the even Laurent coefficient. This occurs before its odd-parity step. Its equation (7) is the required imaginary antiperiod and its section 4 supplies the primitive reduced real period. Thus the exact common-divisor/one-dimensional-space argument frozen initially applies to B_+ and D_-; the real inverse area is nonzero by positive oriented chord determinants. The additional outer-foot lemma, not an object-label switch, is what makes the transfer work.

F62's printed p. 6 rectangle is actually (+/-2/sqrt(5),+/-2/sqrt(5)). It lies on x^2/4+y^2=1 but its first reflection residual is (9/17,-15/17), and its horizontal/vertical chord caustic parameters alternate 1/5 and 16/5. At its upper-right corner, incoming (0,1) reflected in normal (t/2,2t), t=1/sqrt(5), is (-8/17,-15/17), not outgoing (-1,0). The native current paper correctly distinguishes this source fixture error from the all-odd proof.

For the corrected native rectangle (+/-4t,+/-t), set c=sqrt(3), u=ct, u^2=3/5. In unit inversion its two vertical inverse sides have denominators d_R=4(1-u)^2, d_L=4(1+u)^2. Their reciprocal sum is 5 and their horizontal separation is 1/(4t). Their signed trapezoid area is t*5/(4t)=5/4 at either focus, so inverse product is 25/16. The axis diamond has each inverse area 1, product 1. These are the printed F62 inverse numbers for the corrected genuine controls. No source file was repaired or changed.

The actual complete nine-page F14 v1.1 body was read. Its arbitrary-point product is outer area times ONE pedal area for primitive N=2 mod 4, and its odd extension is the CENTER pedal with the separate repeated-list convention. It does not state the present original-two-focus product. Its parallel-residue cancellation and reversal method are directly relevant and properly credited.

## Canonical and attribution interfaces

Stachel's actual published Theorem 4.3/Eq. (4.9), printed 1614, with context 1613-1615, matches the caustic modulus and canonical shift/axes used here. Its preceding printed dn real-shift line at 1613 has the opposite sign; a cached actual page image confirms that typography. That line is not adopted: the reviewed manuscript uses the correct DLMF periods/characters, and the cited canonical theorem's actual formulas agree. No correction to this manuscript is required on that account.

Official DLMF 22.4 Tables 1/3 and 22.8.1-3 were actually read after INITIAL. The common-vector lattice and all quarter/half-period signs match the frozen derivation. The official interface observed version 1.2.8, release 2026-09-15. No exact raw-byte identity between this live rendered interface and a prior HTML cache is asserted.

RGK actual v11 pp. 1-3,6-9, journal printed 342-343 and 349, and v1 pp. 1-2,6 were read. The signed construction and primed outer-side definition match; v11 Table 7 has k605,a, journal Table 7 has k606 while its k605 is original-chord, and the actual 26 April 2020 v1 has Table 5 k604. Their dated experimental question marks establish no current openness or firstness.

## Access and execution limits

One ordinary fresh IAS GET returned HTTP 403/curl exit 22; exact 118-byte HTML, headers/stdout/stderr are retained. No PDF was acquired and no retry/bypass was made. Actual published-body text retained from an earlier IAS acquisition was read by reference: 45,347 B, c37d396f97527c5c488202c3a4e96e7fbbf2d9d68be88f7dac6b4e4643516b36. Its acquisition-only receipt records original PDF 155,501 B/b095489fbd2de419b945af14933cda159f34b42a775b9d212031b62e1682de4c, but that PDF is not retained or freshly authenticated here. The actual raw arXiv precursor's first four pages were separately read and pinned. This custody/access limit must stay explicit.

The two small exact-control source files, 119 and 79 lines, were completely read statically. After the full 79-line body was read, exactly one ordinary native attempt was made in the owned outdir with bytecode disabled. It stopped at missing Sympy import, exit 1, empty stdout, literal stderr retained; no mathematical native output or PASS is claimed. There was no install, retry, optimized run, self-test campaign, builder or source change. The completed independent analytic proof and hand controls remain the mathematical evidence.

This note records completed post-INITIAL work; the final full-original disposition/manifest still require closure after the requested programme checkpoint. No current peer/root scientific findings were opened or shared.
