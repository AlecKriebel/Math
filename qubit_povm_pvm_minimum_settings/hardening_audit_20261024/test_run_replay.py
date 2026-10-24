#!/usr/bin/env python3
"""Temporary MOCK controls for replay wrapper; no result here verifies Lean."""
from pathlib import Path
import contextlib, io, json, subprocess, sys, tempfile, unittest
from unittest.mock import patch
import run_replay as runner

class ReplayWrapperTests(unittest.TestCase):
    def test_acceptance_and_fail_closed_paths(self):
        for scenario in ['valid','panic_zero_exit','error_zero_exit','missing_marker',
                         'nonzero_exit','source_changed','artifact_changed','inventory_changed','stale_baseline']:
            with self.subTest(scenario=scenario),tempfile.TemporaryDirectory(prefix='replay-wrapper-mock-') as td:
                base=Path(td);root=base/'source';out=base/'result';root.mkdir()
                for name in ['Bell.lean','lakefile.toml','lake-manifest.json','lean-toolchain','environment/pins.json','reports/declarations.json','reports/source_completion/source_inventory.json']:
                    f=root/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_text('mock source\n')
                artifact=root/'mock.olean';artifact.write_bytes(b'mock input')
                (root/'reports/runs/mock').mkdir(parents=True)
                runner.write(root/'reports/latest_run.json',{'run_id':'mock','directory':'reports/runs/mock'})
                runner.write(root/'reports/runs/mock/kernel_report.json',{'status':'passed','last_stage':'complete','run_id':'mock','source_snapshot':runner.snapshot(root) if scenario!='stale_baseline' else {}})
                inventory={'constants':['Toy.valid'],'modules':[{'module':'Toy','olean':'mock.olean'}]}
                def fake(args,**kwargs):
                    stream=kwargs['stdout'];code=0
                    if '--version' in args:stream.write('Lean (version 4.19.0, Release)\n')
                    elif '--githash' in args:stream.write(runner.EXPECTED_COMMIT+'\n')
                    elif 'controls' in args:stream.write('PASS positive, malformed-proof, retyped-axiom, and changed-core controls\n')
                    elif 'inventory' in args:
                        runner.write(Path(args[-1]),inventory);stream.write('PASS dependency inventory only;\n')
                    else:
                        obj=inventory if scenario!='inventory_changed' else dict(inventory,constants=['Toy.changed'])
                        runner.write(Path(args[-1]),obj)
                        if scenario!='missing_marker':stream.write('PASS main-endpoint empty-environment replay;\n')
                        if scenario=='panic_zero_exit':stream.write('PANIC recovered\n')
                        if scenario=='error_zero_exit':stream.write('error: recovered\n')
                        if scenario=='nonzero_exit':code=1
                        if scenario=='source_changed':(root/'Bell.lean').write_text('changed')
                        if scenario=='artifact_changed':artifact.write_bytes(b'changed')
                    return subprocess.CompletedProcess(args,code)
                with patch.object(sys,'argv',['run_replay.py','--root',str(root),'--output',str(out)]),patch.object(runner.subprocess,'run',fake),contextlib.redirect_stdout(io.StringIO()):
                    if scenario=='valid':runner.main()
                    else:
                        with self.assertRaises(RuntimeError):runner.main()
                self.assertEqual(runner.read(out/'receipt.json')['status'],'passed' if scenario=='valid' else 'failed')

if __name__=='__main__':unittest.main(verbosity=2)
