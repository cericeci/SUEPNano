name = 'nanoSUEP2018data'  #Part of the name of your output directory, adapt as needed.  
running_options = []
runATCAF = False

dataset = {
"MET_A":"/MET/Run2018A-UL2018_MiniAODv2-v2/MINIAOD",
"MET_B":"/MET/Run2018B-UL2018_MiniAODv2-v2/MINIAOD",
"MET_C":"/MET/Run2018C-UL2018_MiniAODv2-v1/MINIAOD",
"MET_D":"/MET/Run2018D-UL2018_MiniAODv2-v1/MINIAOD"
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
   config.JobType.psetName = 'nano18_data.py' 
   config.JobType.maxMemoryMB = 2000

   config.JobType.pyCfgParams = running_options

   config.Data.inputDBS = 'global'
   config.Data.splitting = 'FileBased'
   config.Data.publication = False
   config.Data.unitsPerJob = 5
   config.Data.outLFNDirBase = '/store/group/phys_exotica/SUEPs/UL18/'
   config.Site.storageSite = 'T2_CH_CERN'

   for sample in listOfSamples:
      config.General.requestName = sample
      config.Data.inputDataset = dataset[sample]
      config.Data.outputDatasetTag = sample
      p = Process(target=submit, args=(config,))
      p.start()
      p.join()
