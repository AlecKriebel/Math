#!/usr/bin/env python3
"""Deterministic complete unittest outcomes; the mathematical test source is unchanged."""
import hashlib,json,os,runpy,sys,unittest
from pathlib import Path
class Result(unittest.TestResult):
 def __init__(self):super().__init__();self.records=[]
 def addSuccess(self,test):super().addSuccess(test);self.records.append(dict(test=test._testMethodName,status='PASS'))
 def addFailure(self,test,err):super().addFailure(test,err);self.records.append(dict(test=test._testMethodName,status='FAIL',error_type=err[0].__name__,reason=str(err[1])))
 def addError(self,test,err):super().addError(test,err);self.records.append(dict(test=test._testMethodName,status='ERROR',error_type=err[0].__name__,reason=str(err[1])))
 def addSubTest(self,test,subtest,err):
  super().addSubTest(test,subtest,err)
  if err is not None:self.records.append(dict(test=test._testMethodName,status='FAIL' if issubclass(err[0],test.failureException) else 'ERROR',subtest=str(subtest),error_type=err[0].__name__,reason=str(err[1])))
 def addSkip(self,test,reason):super().addSkip(test,reason);self.records.append(dict(test=test._testMethodName,status='SKIP',reason=reason))
def main():
 if os.getuid()!=1000 or os.geteuid()!=1000:raise ValueError('UID=EUID=1000 required')
 if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise ValueError('require -I -S -B')
 root=Path(__file__).absolute().parent;p=root/'check_algebra.py'
 if len(sys.argv)==3 and sys.argv[1]=='--candidate':
  name=sys.argv[2]
  if Path(name).name!=name or not name.startswith('mutant_') or not name.endswith('.py'):raise ValueError('safe local mutation filename required')
  p=root/name
 elif len(sys.argv)!=1:raise ValueError('invalid arguments')
 raw=p.read_bytes();ns=runpy.run_path(str(p),run_name='finite_mathematics');suite=unittest.defaultTestLoader.loadTestsFromTestCase(ns['AlgebraChecks']);result=Result();suite.run(result)
 if p.read_bytes()!=raw:raise ValueError('checker changed')
 success=result.wasSuccessful() and not result.skipped and result.testsRun==9
 record=dict(schema=1,problem_id=30005199,status='PASS' if success else 'FAIL',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,script_sha256=hashlib.sha256(raw).hexdigest(),tests_run=result.testsRun,test_outcomes=result.records,failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),scope='Finite exact algebra and scope controls only; not analytic theorem certification')
 print(json.dumps(record,indent=2,sort_keys=True));return 0 if success else 1
if __name__=='__main__':
 try:sys.exit(main())
 except Exception as e:print(json.dumps(dict(status='ERROR',error_type=type(e).__name__,reason=str(e)),sort_keys=True));sys.exit(1)
