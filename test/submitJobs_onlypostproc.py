#!/usr/bin/env python
import os, re
import commands
import math, time
import sys

print 
print 'START'
print 
########   YOU ONLY NEED TO FILL THE AREA BELOW   #########
########   customization  area #########
interval = 1 # number files to be processed in a single job, take care to split your file so that you run on all files. The last job might be with smaller number of files (the ones that remain).
FileList        = sys.argv[1]                            # list with all the file directoriequeue = "workday" 
queue           = sys.argv[2] 
tag             = sys.argv[3]
NumberOfJobs    = int(sys.argv[4])
interval        = int(sys.argv[5])
year            = sys.argv[6]
ScriptName = "./nano%s.py"%year
extraIsData  = ""
if len(sys.argv) > 7: # Then it is data
  dataPD = sys.argv[7]
  extraIsData = "-d --pd %s"%dataPD
if extraIsData != "":
  ScriptName = "./nano%s_data.py"%year 
########   customization end   #########
tag = tag + year
path = os.getcwd()
print
print 'do not worry about folder creation:'
os.system("rm -rf tmp%s"%tag)
os.system("rm -rf exec%s"%tag)
os.system("rm -rf batchlogs%s"%tag)
os.system("mkdir tmp%s"%tag)
os.system("mkdir exec%s"%tag)
print

files = open(FileList,"r").readlines()
files = [f.replace("\n","") for f in files]
if NumberOfJobs == -1: 
  NumberOfJobs = (len(files)+ interval)/interval
##### loop for creating and sending jobs #####
for x in range(1, int(NumberOfJobs)+1):
    ##### creates directory and file list for job #######
    jobFiles = files[max(0,(x-1)*interval):min(x*interval, len(files))]
    ##### creates jobs #######
    #print(FullOutputDir+OutputFileNames+"_"+str(x)+".root")
    if len(jobFiles) < 1: continue
    with open('exec%s/job_'%tag+str(x)+'.sh', 'w') as fout:
        jobFiles = jobFiles[0].split(":") 
        fout.write("#!/bin/sh\n")
        fout.write("export X509_USER_PROXY=$1\n")
        fout.write("voms-proxy-info -all\n")
        fout.write("voms-proxy-info -all -file $1\n")
        fout.write("echo\n")
        fout.write("echo\n")
        fout.write("echo 'START---------------'\n")
        fout.write("echo 'WORKDIR ' ${PWD}\n")
        fout.write("export HOME=$PWD\n")
        fout.write("source /afs/cern.ch/cms/cmsset_default.sh\n")
        fout.write("cd "+str(path)+"\n")
        fout.write("cmsenv\n")
        fout.write("cd -\n")
        #fout.write("cmsRun /afs/cern.ch/work/c/cericeci/private/SUEP/CMSSW_10_6_26/src/PhysicsTools/SUEPNano/test/"+ScriptName+ " inputFiles=" + ",".join(jobFiles) + " outputFile='"+OutputFileNames+"_"+str(x)+".root'\n") 
        fout.write("python /afs/cern.ch/work/c/cericeci/private/SUEP/CMSSW_10_6_26/src/PhysicsTools/NanoAODTools/local/runLocalFile.py -c /afs/cern.ch/work/c/cericeci/private/SUEP/CMSSW_10_6_26/src/PhysicsTools/NanoAODTools/python/postprocessing/modules/SUEP/SUEPpostProcessor_20%s.py "%(year) + extraIsData + " -f %s\n"%jobFiles[0])
        fout.write("mv *Skim.root %s\n"%jobFiles[1])
        fout.write("echo 'STOP---------------'\n")
        fout.write("echo\n")
        fout.write("echo\n")
    os.system("chmod 755 exec%s/job_"%tag+str(x)+".sh")
    
###### create submit.sub file ####
    
os.mkdir("batchlogs%s"%tag)
with open('submit.sub', 'w') as fout:
    fout.write("executable              = $(filename)\n")
    fout.write("arguments               = $(Proxy_path) $(ClusterId)$(ProcId)\n")
    fout.write("output                  = batchlogs%s/$(ClusterId).$(ProcId).out\n"%tag)
    fout.write("error                   = batchlogs%s/$(ClusterId).$(ProcId).err\n"%tag)
    fout.write("log                     = batchlogs%s/$(ClusterId).log\n"%tag)
    fout.write("Proxy_path              = /afs/cern.ch/user/c/cericeci/private/x509up_u88688\n")
    fout.write('+JobFlavour = "%s"\n' %(queue))
    fout.write("\n")
    fout.write("queue filename matching (exec%s/job_*sh)\n"%tag)
    
###### sends bjobs ######
os.system("echo submit.sub")
os.system("condor_submit submit.sub")
  
print
print "your jobs:"
os.system("condor_q")
print
print 'END'
print
