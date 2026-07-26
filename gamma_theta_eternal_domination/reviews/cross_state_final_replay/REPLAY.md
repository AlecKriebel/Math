# Root replay: cross-state and frozen-color probes

Date: 2026-07-26 16:26 PDT

The two bounded ordinary-set probes were rerun from their frozen sources into
fresh temporary directories.  Neither replay invoked a SAT solver or used an
order-14 instance.

## Cross-state response probe

Command:

```text
python3 math/working/cross_state_response_probe.py \
  --min-order 1 --max-order 8 --max-seconds 60 \
  --output <temporary>/out.json --log <temporary>/out.log
```

After deleting only the nondeterministic `resource_usage` object, the accepted
and replay JSON files were byte-identical.  Both normalized files had SHA-256

```text
b37e94d86f0ad4755a1dff4e6edf2f3f9b46bc23ca94fd212d0faa849d70653a
```

Frozen artifact hashes:

```text
e335e60e958a2520398a10b7614c346f81cc3dd000963c38678f4460d363a6ff  math/working/cross_state_response_probe.py
fcd56622c6d7d8c4a51a6c3a24be544d1e9e71c58b9fff9b6c452a4e2f02c066  results/cross_state_response_probe.json
72568679a222cda679797b4b3f134ac6c9615bd51e11a35c8499364b6ee5664c  results/cross_state_response_probe.log
```

## Frozen-color and residual-core probe

Command:

```text
python3 math/working/k3_full_list_residual_probe.py \
  --max-order 8 --max-seconds 60 \
  --output <temporary>/out.json --log <temporary>/out.log
```

After deleting only the nondeterministic `resource_usage` object, the accepted
and replay JSON files were byte-identical.  Both normalized files had SHA-256

```text
0c792c200c319c1c23ed8a314076ba4de066416185cf1fa2c6b5571fb7230b4c
```

Frozen artifact hashes:

```text
b7805ef0fa63744ea97060d72d2ef697d3dfca3ed4d06bddf9304f7bdee5a50a  math/working/k3_full_list_residual_probe.py
1455c6e7d802dde4cc907750bd7789119ef31bdf3ddd0a2b0d55ccf502e64fba  results/k3_full_list_residual_probe.json
e6fa36888421ebd8ea8acd5595f9fb89dbd56ea7f6365b56e440b04c80907287  results/k3_full_list_residual_probe.log
```

## Verdict

```text
PASS — BOTH NORMALIZED REPLAYS BYTE-IDENTICAL
```

The zero-violation finite outcomes are falsification evidence only.  The
campaign claims rest on the separately reviewed analytic proofs.
