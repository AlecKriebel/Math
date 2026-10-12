#!/usr/bin/env python3
"""Disclosed replays of sealed earlier sources, with only private output redirects."""
import contextlib,hashlib,importlib.util,io,json,socket,sys,tempfile
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
sys.path.insert(0,str(AUDIT/'operations'))
import common as c

def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
    selections=[('PREPARER',AUDIT/'operations/check_operations.py',158),('ROUND2',AUDIT/'reviews/operations_adversary2/independent_controls.py',160),('ROUND3',AUDIT/'reviews/operations_adversary3/independent_controls.py',84)]
    private=HERE/'private_cases';private.mkdir(exist_ok=True);suffix='NORMAL' if __debug__ else 'OPTIMIZED';outputs=[]
    def deny(*a,**k):raise RuntimeError('Actual service denied in historical replay')
    for label,source,count in selections:
        before=hashlib.sha256(source.read_bytes()).hexdigest();m=load(source,'ops4_replay_'+label)
        with tempfile.TemporaryDirectory(prefix='historical_',dir=private) as tmp:
            target=Path(tmp).resolve()
            if label=='PREPARER':m.OPERATIONS=target
            else:m.HERE=target
            with contextlib.redirect_stdout(io.StringIO()),patch.object(c.subprocess,'run',side_effect=deny),patch.object(socket,'create_connection',deny):m.main()
            produced=target/('OFFLINE_CONTROLS_'+suffix+'.json' if label=='PREPARER' else 'INDEPENDENT_CONTROLS_'+suffix+'.json');data=produced.read_bytes();result=json.loads(data)
            require(result['case_count']==count and result['all_passed'] is True and type(result['real_external_calls']) is int and result['real_external_calls']==0,'Historical replay failed')
            require(all(row['passed'] is True and row['real_external_calls']==0 for row in result['cases']),'Actual historical row failed')
            (HERE/(label+'_REPLAY_'+suffix+'.json')).write_bytes(data)
            outputs.append({'label':label,'count':count,'sha256':hashlib.sha256(data).hexdigest(),'reviewed_source_sha256':before,'all_passed':True,'real_external_calls':0})
        require(hashlib.sha256(source.read_bytes()).hexdigest()==before,'Sealed source changed')
    (HERE/('HISTORICAL_REPLAY_RECEIPT_'+suffix+'.json')).write_bytes(c.json_bytes({'scope':'Disclosed replay, not fresh case definitions. Previous failed results remain untouched.','sources':outputs,'case_count':sum(x['count'] for x in outputs),'all_passed':True,'real_external_calls':0}));print(json.dumps(outputs,indent=2))
if __name__=='__main__':main()
