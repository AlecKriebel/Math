# Numerical Construction Results

## Status

**NUMERICAL EVIDENCE ONLY — NOT A RESOLUTION OR CERTIFICATE.**

No 41-, 42-, 43-, or 44-point configuration with maximum inner product at
most \(1/2\) was found.  The best numerical candidates all exceed \(1/2\) by
large margins compared with binary64 rounding error.

The final benchmark coordinates came from the public
[table of spherical codes](https://www.spherical-codes.org/), and were
independently parsed, recomputed, locally refined, and perturbed here.  They
are comparison data, not newly discovered exact constructions.

## Best observed candidates

Contacts below mean pairs within \(10^{-8}\) of the recomputed maximum.
The five listed eigenvalues are the positive eigenvalues of the numerical
Gram matrix; the other \(N-5\) eigenvalues are zero only up to rounding.

| \(N\) | maximum inner product | gap above \(1/2\) | angle (degrees) | contacts | contact degree histogram | components |
|---:|---:|---:|---:|---:|---|---|
| 41 | 0.5149946525121679 | 0.0149946525121679 | 59.0029024465 | 153 | \(0^6,8^{18},9^{10},10^6,12^1\) | \(35,1^6\) |
| 42 | 0.5182411558622624 | 0.0182411558622624 | 58.7856545088 | 171 | \(0^2,2^1,6^4,7^4,8^7,9^{12},10^8,11^4\) | \(40,1^2\) |
| 43 | 0.5247096018290212 | 0.0247096018290212 | 58.3513041507 | 169 | \(5^8,6^{12},7^2,9^6,10^8,11^6,12^1\) | \(43\) |
| 44 | 0.5274577123235323 | 0.0274577123235323 | 58.1661569222 | 190 | \(6^4,7^2,8^8,9^{24},10^4,11^2\) | \(44\) |

Positive Gram eigenvalues:

```text
N=41  7.89209913338035  7.97875518966749  7.97875518966750
      8.18617330107148  8.96421718621319
N=42  7.89831714334427  8.01144078381209  8.49179767155605
      8.68033850452981  8.91810589675779
N=43  8.39791854096492  8.41114832150702  8.41211366797961
      8.41211366797962  9.36670580156883
N=44  8.59143245017048  8.63764920946916  8.63764920946918
      9.05949682198754  9.07377230890366
```

Maximum squared-norm error after the recorded refinements was at most
\(4.45\times10^{-16}\).  This is a diagnostic only: direct coordinate
rounding and ordinary eigensolvers do not provide directed error bounds.

The 41-point benchmark has a 35-vertex active core and six contact-free
rattlers.  Its first noncontact lies about \(0.00687\) below the maximum.
Thus the displayed active graph is well separated at tolerance \(10^{-8}\),
but its six isolated vertices also show why a blanket rigidity assumption
would be invalid.

## Independent search before importing benchmark coordinates

The best locally refined values found without initializing from the public
coordinates were:

| \(N\) | independent best |
|---:|---:|
| 41 | 0.5155570516153124 |
| 42 | 0.5182413529839812 |
| 43 | 0.5258965494698511 |
| 44 | 0.5274711925362536 |

The \(N=42\) basin was rediscovered both by deletion from a 43-point code and
by exact-hinge random starts (seeds 206, 216, and 220), within about
\(2\times10^{-7}\) of the public benchmark.  This was the strongest
independent calibration outcome.

## Start portfolio and seeds

For every \(N=41,42,43,44\):

- 5 random hybrid starts, seeds 0–4;
- 60 hybrid starts, seeds 10–29 for each of `random`, `d5plus`, and `delete`;
- 24 exact positive-part hinge starts, seeds 200–223;
- 36 \(D_5\)-surgery starts, seeds 300–335.

Further:

- 24 insertion starts, seeds 100–123, for \(N=42,43,44\);
- complete one-point deletion cascades from the best \(N+1\) candidates;
- for the public \(N=41\) benchmark, 96 core/all/rattler perturb-and-relax
  starts, seeds 400–495, followed by 32 direct-SQP perturbations, seeds
  600–631, with tangent scales \(10^{-8}\) through \(0.02\);
- for public \(N=42,43,44\), 48 continuation perturbations, seeds 500–547,
  and 32 direct-SQP perturbations, seeds 600–631.

All 32 direct-SQP perturbations of the 41-point benchmark returned
0.514994652512 within roughly \(10^{-14}\); none improved it.  The analogous
tests for \(N=42\) and \(N=44\) returned their benchmark values.  Most
\(N=43\) tests did likewise, while a few scale-\(0.02\) starts converged about
\(2.5\times10^{-7}\) above the benchmark.  No perturbation improved any
benchmark.  This is local numerical evidence only and says nothing about
global optimality.

## Exact replay commands

The following are the principal commands used, written from the repository
root.  Replace `python3` by the pinned discovery environment as desired.

```bash
python3 kissing_number_5/experiments/random_codes/search_spherical5.py \
  --n 41 --seeds 0 1 2 3 4 --kinds random --mode hybrid \
  --out kissing_number_5/experiments/output/n41_wave1

python3 kissing_number_5/experiments/random_codes/search_spherical5.py \
  --n 41 --seeds $(seq 10 29) --kinds random d5plus delete --mode hybrid \
  --out kissing_number_5/experiments/output/n41_broad

python3 kissing_number_5/experiments/random_codes/search_spherical5.py \
  --n 41 --seeds $(seq 200 223) --kinds random --mode exacthinge \
  --out kissing_number_5/experiments/output/n41_exact_hinge

python3 kissing_number_5/experiments/random_codes/search_spherical5.py \
  --n 41 --seeds $(seq 300 335) --kinds d5surgery --mode hybrid \
  --out kissing_number_5/experiments/output/n41_d5_surgery

python3 kissing_number_5/experiments/random_codes/refine_spherical5.py \
  --input kissing_number_5/experiments/output/n41_broad.npz \
  --out kissing_number_5/experiments/output/n41_broad_refined --slsqp
```

Repeat with `--n 42`, `--n 43`, and `--n 44`.

Fetch and analyze the public comparison inputs:

```bash
for n in 41 42 43 44; do
  curl -fsSL "https://www.spherical-codes.org/data/5/$n" \
    -o "kissing_number_5/experiments/input/spherical_codes_5_${n}.txt"
  python3 \
    kissing_number_5/experiments/random_codes/analyze_refine_coordinates.py \
    "kissing_number_5/experiments/input/spherical_codes_5_${n}.txt" \
    --refine smooth-slsqp \
    --output-json \
    "kissing_number_5/experiments/output/public_5_${n}_refined.json"
done
```

Challenge the 41-point basin:

```bash
python3 kissing_number_5/experiments/random_codes/perturb_benchmark.py \
  --input kissing_number_5/experiments/input/spherical_codes_5_41.txt \
  --seeds $(seq 400 495) \
  --out kissing_number_5/experiments/output/public_5_41_perturb

python3 kissing_number_5/experiments/random_codes/slsqp_perturb.py \
  --input kissing_number_5/experiments/input/spherical_codes_5_41.txt \
  --seeds $(seq 600 631) \
  --out kissing_number_5/experiments/output/public_5_41_local_sqp
```

## Public-input hashes

The exact downloaded response bodies used in this experiment had SHA-256:

```text
N=41 c54b38d8216bf76a79c57119fc46245811188e1de05c840c68a33cec9b7fe1b0
N=42 f941a50369a6a26ab4785216a9c5d544a861b7bd9546f0ac1e246d848281f865
N=43 bf6414a336bf9205c3ec0115f6f289ac2e40b57f9fac5d7f4223083665e9a768
N=44 d7ac84e95fa5d34b358da80920922f52ead9d932fec19250ac176d277f8999c2
```

These hashes identify floating-point discovery inputs, not exact certificates.
