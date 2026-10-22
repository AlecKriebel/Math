import pathlib,hashlib,json,math,datetime
R=pathlib.Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';E=P/'audits/pr967_2616/closure_engineering_01'
for name,h in [('close_pr967.py','c6231a47758a6b037ed005883d39e374946e38bd9aec0c74eb33df3afe2d2a45'),('finalize_pr967_and_gate_next.py','47520f8f86889db8c5b85fc7000486773d2ca4e8601ad00531bad2fdce5143cb')]:
 raw=(E/('FINAL02_'+name)).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=h:raise RuntimeError('Externally pinned old helper changed before compile')
 n={'__name__':'_review_overflow_reproduction_','__file__':str(P/name)}
 exec(compile(raw,str(P/name),'exec',dont_inherit=True,optimize=0),n)
 value=n['strict'](b'{"extra":1e9999}')
 if not math.isinf(value['extra']):raise RuntimeError('Old optional issue no longer reproduced')
 print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'helper':name,'reviewed_old_sha256':h,'overflow_value_is_infinite':True,'scope':'Parser primitive only. No semantic authority bypass demonstrated.'}))
