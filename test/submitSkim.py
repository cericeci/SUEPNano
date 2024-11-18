import os
import sys

inputFolder  = sys.argv[1]
outputFolder = sys.argv[2]
nFilesPerJob = int(sys.argv[3])
queue        = sys.argv[4]
tag          = sys.argv[5]
runFolder    = os.getcwd() + "/exec_" + tag
doSubmit     = True

print(runFolder)
if not os.path.isdir(runFolder):
    os.system("mkdir %s"%runFolder)
    os.system("mkdir %s/jobs"%runFolder)
    os.system("mkdir %s/batchlogs"%runFolder)

allFiles = [ inputFolder + "/" + f  for f in os.listdir(inputFolder)]

lastN = 0
iJob = 0
workdir = os.getcwd()

tmpFiles = []
for f in allFiles:
    if not ("output" in f): continue
    outFile = outputFolder + "/" + tag + "_" + f.split("/")[-1].replace("output_","")
    if os.path.isfile(outFile):
        if os.path.getsize(outFile) < 2000:
            os.system("rm %s"%outFile)
            tmpFiles.append((f,outFile))
        else:
            continue
    else:
        tmpFiles.append((f,outFile))

allFiles = tmpFiles

while lastN < len(allFiles):
    with open("%s/jobs/_%i.sh"%(runFolder,iJob), "w") as fout:
        fout.write("#!/bin/sh\n")
        fout.write("echo\n")
        fout.write("echo\n")
        fout.write("echo 'START---------------'\n")
        fout.write("export X509_USER_PROXY=%s/proxy/x509up_u222283\n"%workdir)
        fout.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
        fout.write("cd /eos/home-c/cericeci/Combine/CMSSW_14_1_0_pre4/src\n")
        fout.write("cmsenv\n")
        fout.write("cd %s\n"%workdir)
        for f in allFiles[lastN:min(len(allFiles)+1, lastN+nFilesPerJob)]:
            fout.write("python3 skimFile.py %s %s\n"%(f[0], f[1]))
    lastN += nFilesPerJob
    iJob  += 1

if iJob == 0:
    print("No new jobs to submit, closing in...")
    exit()
else:
    print("Will submit %s new jobs"%iJob)
#os.mkdir("%s/batchlogs"%tag)
with open('submit.sub', 'w') as fout:
    fout.write("executable              = $(filename)\n")
    fout.write("arguments               = $(ClusterId)$(ProcId)\n")
    fout.write("output                  = %s/batchlogs/$(ClusterId).$(ProcId).out\n"%runFolder)
    fout.write("error                   = %s/batchlogs/$(ClusterId).$(ProcId).err\n"%runFolder)
    fout.write("log                     = %s/batchlogs/$(ClusterId).log\n"%runFolder)
    fout.write('+JobFlavour = "%s"\n' %(queue))
    fout.write("\n")
    fout.write("queue filename matching (%s/jobs/_*sh)\n"%runFolder)

if doSubmit:
    ###### sends bjobs ######
    os.system("echo submit.sub")
    os.system("condor_submit -spool submit.sub")
