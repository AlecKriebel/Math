"""Real local descriptor ordering and injected faults; no crash/provider simulation."""
from pathlib import Path
from datetime import datetime,timezone
from unittest.mock import patch
import hashlib,importlib.util,json,os,stat,tempfile
D=Path(__file__).resolve().parent;P=D.parent/'publication'
spec=importlib.util.spec_from_file_location('guard',P/'release_binding.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
rows=[];real=os.fsync
with tempfile.TemporaryDirectory(prefix='pr210-intent-durability-') as tmp:
    C=Path(tmp);leaf=C/'new_ancestor/new_leaf';events=[]
    def observe(fd):
        s=os.fstat(fd);events.append((s.st_dev,s.st_ino,stat.S_ISDIR(s.st_mode)));return real(fd)
    with patch.object(os,'fsync',observe):g.durable_mkdir(leaf)
    for path in [C,C/'new_ancestor']:
        s=path.stat();assert (s.st_dev,s.st_ino,True) in events
    rows.append(dict(test='Every newly created ancestor linkage is directory-synced',pass_result=True,directory_sync_count=len(events)))
    events=[]
    with patch.object(os,'fsync',observe):g.exclusive_json(leaf/'ok.json',{'fixture_only':True})
    assert [x[2] for x in events]==[False,True]
    rows.append(dict(test='Exclusive intent fsyncs regular file then parent directory',pass_result=True,descriptor_is_directory=[x[2] for x in events]))
    called=[]
    def fail_directory(fd):
        if stat.S_ISDIR(os.fstat(fd).st_mode):raise OSError('Injected directory-sync failure')
        return real(fd)
    try:
        with patch.object(os,'fsync',fail_directory):g.exclusive_json(leaf/'failed.json',{'fixture_only':True});called.append('provider-would-run')
    except OSError:pass
    else:raise AssertionError('Directory failure was ignored')
    assert not called and (leaf/'failed.json').exists()
    rows.append(dict(test='Directory sync failure retains intent and blocks associated effect',pass_result=True,provider_calls=0))
    def second_directory_fails(fd):
        if stat.S_ISDIR(os.fstat(fd).st_mode):
            second_directory_fails.n+=1
            if second_directory_fails.n==2:raise OSError('Injected new ancestor-link sync failure')
        return real(fd)
    second_directory_fails.n=0;other=C/'retry_ancestor/retry_leaf'
    try:
        with patch.object(os,'fsync',second_directory_fails):g.durable_mkdir(other)
    except OSError:pass
    else:raise AssertionError('Ancestor sync failure ignored')
    assert (C/'retry_ancestor').is_dir() and not other.exists()
    events=[]
    with patch.object(os,'fsync',observe):g.durable_mkdir(other)
    for path in [C,C/'retry_ancestor']:
        s=path.stat();assert (s.st_dev,s.st_ino,True) in events
    rows.append(dict(test='Retry syncs visible unconfirmed ancestor before creating descendants',pass_result=True))
r=dict(utc=datetime.now(timezone.utc).isoformat(),all_tests_passed=True,network_provider_calls=0,actual_power_failure_simulated=False,evidence='Descriptor ordering and injected errors only; relies on supported OS fsync semantics, no hardware durability certification',release_binding_sha256=hashlib.sha256((P/'release_binding.py').read_bytes()).hexdigest(),tests=rows)
(D/'ROOT_DURABLE_INTENT_TEST_RESULTS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
