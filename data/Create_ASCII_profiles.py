from glob import glob
from os import system

files = glob("*.calibP")

RMs = [102708,102708,102708,102708,102708,102708,102708,102708,102708,102708,102521,102521,102521,102521,102521,103039]

ii = 0
for burst in files:

    command = "pam -R %f -e calibP.RM %s"%(RMs[ii],burst)
    print command
    system(command)

    command = "pam -F -R %f -e calibP.RM.F %s"%(RMs[ii],burst)
    print command
    system(command)

    command = "psrtxt %s.RM > %s.RM.ASCII"%(burst,burst)
    print command
    system(command)

    command = "psrtxt %s.RM.F > %s.RM.F.ASCII"%(burst,burst)
    print command
    system(command)

    ii = ii+1
