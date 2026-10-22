import json,runpy
from pathlib import Path
ns=runpy.run_path(str(Path(__file__).resolve().parent.parent/'diagnose_geometry.py'),run_name='verification_import')
mp=ns['mp']
tests=[('nan_modulus',lambda:ns['geometry'](mp.nan,8,1),'nonfinite scalar'),
       ('degenerate_modulus',lambda:ns['geometry'](mp.mpf(1),8,1),'strictly between'),
       ('repeated_label',lambda:ns['geometry'](mp.mpf('0.8'),12,2),'least period'),
       ('wrong_parity_as_target',lambda:ns['family'](mp.mpf('0.8'),6,1,['0'],mp.mpf('1e-20'),True),'divisible by four')]
records=[]
for name,call,message in tests:
    try:
        call()
    except ns['VerificationError'] as error:
        if message not in str(error):
            raise RuntimeError(name+': wrong rejection')
        records.append(name)
    else:
        raise RuntimeError(name+': invalid physical input accepted')
print(json.dumps({'status':'PASS','rejected_cases':records}))
