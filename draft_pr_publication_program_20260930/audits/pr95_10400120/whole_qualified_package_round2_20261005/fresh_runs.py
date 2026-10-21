from review_tools import *
import zipfile
root=A/'archive_unpacked';root.mkdir()
with zipfile.ZipFile(Q/'publicfiles/pr95_support.zip')as z:z.extractall(root)
receipts=[]
for mode,flags in [('normal',[]),('optimized',['-O'])]:
    receipts.append(run('fresh_runner_'+mode,[PY,'-E','-B']+flags+[root/'verification/run_all.py','--output-dir',A/('fresh_'+mode)],root,[root/'verification/run_all.py',root/'PAYLOAD_MANIFEST.json',Q/'publicfiles/pr95_support.zip']))
    if receipts[-1]['exit_code']:raise RuntimeError('fresh reproduction failed')
dump(A/'FRESH_OUTER_RECEIPTS.json',receipts)
