import sys
import os
import ROOT

def parse_das(f):
  outs = {}
  text = open(f, "r")
  for l in text.readlines():
    words = l.split(" ")
    fil = words[0]
    yields = sum(eval(words[3].replace("\n","")))
    outs[fil] = yields
  return outs

def getyields(f):
  #print("dasgoclient --query='file=%s | grep file.nevents' >> kk"%f)
  os.system("dasgoclient --query='file=%s | grep file.nevents' >> kk"%f)
  ff = open("kk", "r")
  yields = int(ff.read().replace("\n",""))
  #print(yields)
  os.system("rm kk")
  return yields

def parse_exec(f):
  text = open(f,"r")
  inputFiles = []
  outputFile = ""
  for line in text.readlines():
     if "cmsRun" in line:
       inputs = line.split(" ")[2]
       inputFiles += inputs.replace("inputFiles=","").split(",")
     if "mv" in line:
       outputFile = line.split(" ")[-1].replace("\n","")
  return inputFiles, outputFile

fold = sys.argv[1]
execs  = fold

execfiles = os.listdir(execs)

for ex in execfiles:
  bad = False
  iF, oF = parse_exec(execs + "/" + ex)
  if not(os.path.isfile(oF)):
    print("Missing output for %s"%ex)
    continue
  #print([getyields(iFF) for iFF in iF])
  expyields = sum([getyields(iFF) for iFF in iF])
  test = ROOT.TFile(oF, "READ")
  count = test.Get("Count")
  obsyields = count.Integral()
  if expyields != obsyields:
    print("Some files missing in %s, exp=%i, obs=%i, I will delete it"%(ex, expyields, obsyields))
    os.system("rm %s"%oF)
    continue
  print("File %s is good"%ex)
