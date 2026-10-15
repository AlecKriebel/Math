#!/usr/bin/env python3
"""Intentional invalid source-contract assertions; each must fail."""
import sys
assert __debug__ and not sys.flags.optimize
kind=sys.argv[1]
if kind=='null_Git_source_as_helper':
    actual={'source':None,'source_unchanged':None,'argv':['git','show','fixed-head:fixed-path']}
    assert 'source' in actual
    assert type(actual['source']) is dict, 'Genuine Git source null cannot be validated as a helper source row'
elif kind=='nine_bit_mode':
    actual=0o4444
    assert actual & 0o777==0o444
    assert actual==0o444,'Nine-bit masking hides additional full permission bits'
elif kind=='null_absence_fallback':
    saved=None; upstream_key_present=False; fallback={}
    assert upstream_key_present is False
    assert type(saved) is type(fallback) and saved==fallback,'Saved null differs from absent-key object fallback'
elif kind=='future_current_approval':
    current={'current_verdict':None,'current_gate':'PENDING','future_acceptance_approved':False}
    assert current['future_acceptance_approved'] is True,'SOURCE preparation cannot approve a future whole-current or merge'
else: raise ValueError(kind)
