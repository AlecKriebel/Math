# Hosting capacity and pending redirects checkpoint

2026-11-18 08:36:31 UTC

Scientific review is 100% complete (203 eligible papers reviewed). Preparation is 100% complete (194 passing papers). An estimated 70.0% of eligible papers have a final disposition for this project (133 live and nine deferred, with 61 awaiting deployment).

Firebase Cloud Monitoring's `storage/total_bytes` and `storage/limit` samples show 10,818,227,046 and 10,737,418,240 bytes respectively. The sample predates the check by less than two hours and matches the sum of reported sizes for the 86 finalized versions exactly. This confirms the 80,808,806-byte overage behind the existing deployment failures. The same live version is served and no deployment or cleanup was executed at this checkpoint. [Storage limits](https://firebase.google.com/docs/hosting/usage-quotas-pricing) · [Cloud Monitoring metrics](https://docs.cloud.google.com/monitoring/api/metrics_gcp_d_h#firebasehosting)

The earlier source checkpoint counted 995 deployable files using a separate filter. The Firebase CLI’s own file selector, applied to the checked-in hosting configuration, selects 1,029 files. All 1,029 match the unchanged website source commit `352763640a979bf407868c36ccfdd49a6e632e0a` by Git blob hash and byte length. The file total is 229,635,432 raw bytes and 188,871,194 bytes after the CLI's level-9 gzip setting, before Hosting metadata.

The measured storage usage and release inventory support seeking approval for three June 2023 rollback deletions. Each candidate differs from a nearby retained release only in its homepage file. Their reported release sizes would leave an estimated 53,436,885 bytes of headroom after the prepared deployment. Actual storage release must be checked after any approved cleanup. The approval proposal and exact release records are private.

Both legacy articles remain HTTP 200 and their live bytes match the corresponding pinned Math Git blobs. Their corresponding production replacement routes are HTTP 404. Each pending redirect passed a private Chrome preview with JavaScript enabled (preserving the query and fragment) and disabled (using meta refresh). The redirect drafts may be applied after the production replacements, DOIs and PDF bytes have been verified.

| Inventory row | Zenodo version DOI | Legacy route | Replacement URL | Tested redirect Git blob |
| --- | --- | --- | --- | --- |
| 200 | `10.5281/zenodo.22983161` | `docs/papers/odd-part-slow-variation/index.html` | [/research/odd-part-ratio-slow-variation/](https://aleckriebel.com/research/odd-part-ratio-slow-variation/) | `c894b94909455bb68c315ebcb25a0a2078723cea` |
| 209 | `10.5281/zenodo.22983147` | `docs/papers/gamma-supercyclicity/index.html` | [/research/gamma-supercyclicity/](https://aleckriebel.com/research/gamma-supercyclicity/) | `fb04e22535e4090d3a79aee55d3b4d25fa1f5b7f` |
