# Complete-package review 1: arithmetic, integrity and formalization scope

Review checkpoint: 2026-10-06 22:22 PDT (2026-10-07 05:22 UTC). Assigned arithmetic/integrity audit completion: 100%; this does not estimate discovery, novelty or full upstream-proof validation. No manuscript, source, receipt or Git state was edited. No external individual was contacted.

## Verdict

**No substantive defect found in this scope.** Frozen hashes and upstream pin agree. Exact arithmetic checks pass and match pinned formulas. Density, volume threshold and CM coefficient arithmetic are correct. Lean certification is expressly disclaimed, consistently with the checked catalog. This review does not certify geometric, semigroup, global-minimization or moduli arguments.

## Integrity

All 18 entries in `receipts/review_snapshot_v1.json` matched byte count and SHA256, including `main.tex`, `paper.pdf`, both reproduction scripts and frozen notes. This review file is added after that snapshot.

All 21 `sources/PINNED_MANIFEST.json` entries matched three representations: filesystem contents under `/Users/alec/Desktop/math`, actual Git blobs at commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, and project-local copies in `sources/pinned/`. Clone HEAD equals that full commit.

All seven PDF records in `agent_notes/spotti_sun_source_hashes.json` matched local sources in byte count and SHA256. Built PDFs in both pinned manuscripts' `build/` directories match their build receipts. Rebuilt PDFs intentionally differ from the originally pinned published PDFs. Receipt matching checks artifact consistency; no LaTeX build was rerun or treated as mathematical proof.

## Exact arithmetic and reproduction

`python3 reproducibility/verify_constants.py` exited successfully using the standard library. Its relative-to-file call of the fourfold checker is sound. Both scripts accurately limit themselves to arithmetic. Their assertions require ordinary Python execution, as documented, rather than assertion-disabling `-O`.

The upstream Section 4 exponential certificate matches lines 741–749. Retain degrees 0 through 8 of `exp(4/3)`; the tail starts at degree 9 and each subsequent ratio is at most `(4/3)/10=2/15`. The valid geometric tail bound equals `917330371/241805655`, below `1897/500` by `8028407/24180565500`. The lower series for `e` through degree 6 is `1957/720`, above `1359/500` by `1/18000`. The negative coefficient of `e` gives the correct direction:

    C*=(3/4)exp(4/3)-e/3 < 3879/2000 < 2.

The fourfold checker matches the companion's three-mode formula at lines 535–548: `M0=13/16`, `M2=61/64`, `M4=685/256`, `M6=11101/1024`. With `l=35/12`, the positive coefficient of `c` is `50065/9216`; substitution at `c=-1` gives `26581/4096`. Multiplication by `432/625` gives `717687/160000`; subtraction of `625/144` gives positive margin `209183/1440000`.

Independent substitution of `p=5/4` in `2p(l^2-p^2)/4` recovers `625/144`. The shifted transform gives coefficient `32/35+32/1155=1088/1155` multiplying `sqrt(2)/pi`, matching `g(p)`. Lower-dimensional values `19/324`, `5/27` and coefficient `1/3` match companion lines 582–619. The fourfold bound is `162=2*3^4`.

The companion and all-dimensional introduction theorem, lines 33–51, state the unrestricted singular complex algebraic klt boundary-zero scopes used in the note. Equality classification is not needed.

## Local manuscript constants and dimensions

For `b_k=2(1-1/k)^k`, the derivative is correct: `u=1/(t-1)` gives `u-log(1+u)>0`. The endpoint `b_2=1/2` makes finite-cover density `1/d<=1/2` adequate in every transverse dimension. The range `k=2,...,n` matches Spotti–Sun's flat-factor definition of `A'(n)`.

Cached primary Theorem 5.2 requires precisely `V>(1/2)A'(n)(n+1)^n` and concludes `-K_Z=rL_Z` with Cartier `L_Z`. Cubic adjunction gives `r=n-1`, `H^n=3`, `V=3(n-1)^n`. Substitution gives threshold `(n-1)^n(1+1/n)^n`, strictly smaller than the cubic volume by the valid `(<e<3)` argument. Exact rational spot checks at 2, 3, 4, 5, 6, 10 and 100 agreed, supplementing the uniform argument.

The coefficient of `h^(n+1)s` in `(rh-s)^(n+1)(3h+s)` is `r^(n+1)-3(n+1)r^n`. Negative pushforward and `r=n-1` yield exactly `2(n+2)(n-1)^n s`, positively signed. This checks CM arithmetic, not descent or moduli continuity.

## Lean scope and limitations

`main.tex`, README, CURRENT_THEOREM and DEPENDENCY_LEDGER consistently separate arithmetic, compilation, scoped review and formal certification. The pinned Lean README says only that some repository results are formalized. No ODP-gap/fourfold-gap entry occurs in the catalog, and `/Users/alec/Desktop/math/lean/docs/037.md` is absent. Searching the Lean tree found unrelated normalized-volume uses, not formalization of this singularity bound. No Lean build was run.

The upstream input is correctly treated as a cited theorem, not independently formalized or reproved by these checkers. The exact remaining limitation is mathematical substance outside the stated constants, source-scope matching and integrity checks. No scoped repair is required.
