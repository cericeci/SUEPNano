name = 'nanoSUEP2016data'  #Part of the name of your output directory, adapt as needed.  
running_options = []
runATCAF = False

dataset = {
"MET_F":"/MET/Run2016F-UL2016_MiniAODv2-v2/MINIAOD",
"MET_G":"/MET/Run2016G-UL2016_MiniAODv2-v2/MINIAOD",
"MET_H":"/MET/Run2016H-UL2016_MiniAODv2-v2/MINIAOD"
}


listOfSamples = [k for k in dataset.keys()]

""" # Just to check that these actually exist
import os
for k in dataset.keys():
 print("%s--->"%dataset[k])
 os.system("dasgoclient --query='file dataset=%s' | wc -l"%dataset[k])"""

if __name__ == '__main__':

   from CRABClient.UserUtilities import config
   config = config()

   from CRABAPI.RawCommand import crabCommand
   from multiprocessing import Process

   def submit(config):
       res = crabCommand('submit', config = config )

   config.General.workArea = 'crab_'+name
   config.General.transferOutputs = True
   config.General.transferLogs = True

   config.JobType.pluginName = 'Analysis'
   config.JobType.psetName = 'nano16_data.py' 
   config.JobType.maxMemoryMB = 2000

   config.JobType.pyCfgParams = running_options

   config.Data.inputDBS = 'global'
   config.Data.splitting = 'FileBased'
   config.Data.publication = False
   config.Data.unitsPerJob = 5
   config.Data.outLFNDirBase = '/store/group/phys_exotica/SUEPs/UL16/'
   config.Site.storageSite = 'T2_CH_CERN'

   for sample in listOfSamples:
      config.General.requestName = sample
      config.Data.inputDataset = dataset[sample]
      config.Data.outputDatasetTag = sample
      p = Process(target=submit, args=(config,))
      p.start()
      p.join()
