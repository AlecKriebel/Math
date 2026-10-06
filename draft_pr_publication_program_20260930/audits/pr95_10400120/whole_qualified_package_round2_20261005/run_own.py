from review_tools import *
for negative in [False,True]:
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
        label='own_final_'+('false_'if negative else'positive_')+mode
        r=run(label,[PY,'-E','-B']+flags+[A/'own_exact.py']+(['--false-target']if negative else[]),A,[A/'own_exact.py',A/'OWN_DERIVATION.md'])
        err=(A/'processes'/label/'stderr.bin').read_bytes();out=(A/'processes'/label/'stdout.bin').read_bytes()
        if negative:
            if r['exit_code']==0 or out or b'false normalized coefficient rejected'not in err:raise RuntimeError('own false target failed')
        elif r['exit_code']or err or json.loads(out)['status']!='PASS':raise RuntimeError('own exact check failed')
