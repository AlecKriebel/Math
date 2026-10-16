"""Select the single assigned catalog key, preserving literal payload/report values."""
import datetime
import hashlib
import json
from pathlib import Path
import sqlite3
import sys

key=sys.argv[1]
assert key in ('30000166','30000167')
p=Path('/Users/alec/Documents/Math/unsolved_math_prioritization/cache/catalog.sqlite')
c=sqlite3.connect(p.as_uri()+'?mode=ro&immutable=1',uri=True)
rows=c.execute('SELECT key,payload,report FROM records WHERE key=?',(key,)).fetchall()
assert len(rows)==1, ('selected key count',key,len(rows))
k,payload,report=rows[0]
result={'schema':'pr51-selected-native-catalog-row/v1',
        'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'database_path':str(p),'database_bytes':p.stat().st_size,
        'readonly_immutable':True,'sql':'SELECT key,payload,report FROM records WHERE key=?',
        'parameters':[key],'selected_count':1,
        'raw_row':{'key':k,'payload':payload,'report':report},
        'payload_identity':{'utf8_bytes':len(payload.encode()),'sha256':hashlib.sha256(payload.encode()).hexdigest()},
        'report_sql_null':report is None,
        'parsed_payload':json.loads(payload)}
if report is not None:
    result['report_identity']={'utf8_bytes':len(report.encode()),'sha256':hashlib.sha256(report.encode()).hexdigest()}
    try:result['parsed_report']=json.loads(report)
    except json.JSONDecodeError:result['parsed_report']=None;result['report_parse']='non-JSON text'
print(json.dumps(result,indent=2,ensure_ascii=False))
c.close()
