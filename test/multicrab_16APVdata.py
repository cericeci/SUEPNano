name = 'nanoSUEP2016APVdata'  #Part of the name of your output directory, adapt as needed.  
running_options = []
runATCAF = False

dataset = {
"MET_B1":"/MET/Run2016B-ver1_HIPM_UL2016_MiniAODv2-v2/MINIAOD",
"MET_B2":"/MET/Run2016B-ver2_HIPM_UL2016_MiniAODv2-v2/MINIAOD",
"MET_C":"/MET/Run2016C-HIPM_UL2016_MiniAODv2-v2/MINIAOD",
"MET_D":"/MET/Run2016D-HIPM_UL2016_MiniAODv2-v2/MINIAOD",
"MET_E":"/MET/Run2016E-HIPM_UL2016_MiniAODv2-v2/MINIAOD",
"MET_F":"/MET/Run2016F-HIPM_UL2016_MiniAODv2-v2/MINIAOD",
}


listOfSamples = [k for k in dataset.keys()]


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
   config.JobType.psetName = 'nano16APV_data.py' 
   config.JobType.maxMemoryMB = 2000

   config.JobType.pyCfgParams = running_options

   config.Data.inputDBS = 'global'
   config.Data.splitting = 'FileBased'
   config.Data.publication = False
   config.Data.unitsPerJob = 5
   config.Data.outLFNDirBase = '/store/group/phys_exotica/SUEPs/UL16APV/'
   config.Site.storageSite = 'T2_CH_CERN'

   for sample in listOfSamples:
      config.General.requestName = sample
      config.Data.inputDataset = dataset[sample]
      config.Data.outputDatasetTag = sample
      p = Process(target=submit, args=(config,))
      p.start()
      p.join()
