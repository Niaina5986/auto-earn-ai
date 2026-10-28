import subprocess,sys
from config import ENABLE_EXECUTION

def execute_local_tasks(paths):
 result={'enabled':ENABLE_EXECUTION,'completed':[],'failed':[],'external_actions':'disabled'}
 if not ENABLE_EXECUTION:return result
 for p in paths:
  result['completed'].append({'task':'local_artifact_created','path':str(p)})
  if str(p).endswith('.py'):
   cp=subprocess.run([sys.executable,'-m','py_compile',str(p)],capture_output=True,text=True)
   (result['completed'] if cp.returncode==0 else result['failed']).append({'task':'python_syntax_check','path':str(p),'status':'passed' if cp.returncode==0 else cp.stderr[-1000:]})
 return result
