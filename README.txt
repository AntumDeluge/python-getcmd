GetCMD is Python library that checks for available system command executables.

Usage:
  import getcmd
  
  CMD_bash = GetCMD('bash')
  
  if CMD_bash:
      print(CMD_bash)


Example output:
  /bin/bash


The output can then be used with modules, such os subprocess, for execution.
