#!/usr/bin/env python3
"""Final packaging only; generated record is not independent exit evidence."""
from datetime import datetime,timezone
import hashlib,json
from pathlib import Path
import stat

base=Path(__file__).resolve().parent
def pin(p):
    data=p.read_bytes()
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
            'mode':stat.S_IMODE(p.stat().st_mode)}
prepared=datetime.now(timezone.utc).isoformat()
record={'prepared_utc':prepared,'kind':'internally assembled manifest preparation',
        'program':pin(Path(__file__).resolve()),'excluded_file':'MANIFEST.json',
        'native_evidence_limit':'This generated record does not certify its own process exit,stdout or stderr. Named executions001-028 are actual separately captured child processes;root external replay/closure must capture its genuine outer process.',
        'status':'PREPARED;not externally closed'}
(base/'MANIFEST_PREPARATION.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
files={str(p.relative_to(base)):pin(p) for p in sorted(base.rglob('*'))
       if p.is_file() and p.name!='MANIFEST.json'}
manifest={'prepared_utc':prepared,'owned_namespace':str(base),'status':'UNSEALED;root external closure required',
          'candidate_head':'96395a4f506af6a6045e3cd59afcba2db6b7e2e7',
          'excluded_namespace_files':['MANIFEST.json'],
          'execution_environment':{'PATH':'/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin',
                                   'LANG':'C','LC_ALL':'C','TZ':'UTC','PYTHONHASHSEED':'0','PYTHONDONTWRITEBYTECODE':'1'},
          'files':files,'native_receipt_count':28,'portable_control':'check_arithmetic.py',
          'full_local_verifier':'verify_readonly.py','public_default':False}
(base/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print(json.dumps({'namespace_files_including_manifest':len(files)+1,
                  'manifest':pin(base/'MANIFEST.json'),'prepared_utc':prepared,
                  'status':'PREPARED;not a native process-certification record'},sort_keys=True))
