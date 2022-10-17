# SUEPNano

This is a [NanoAOD](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD) framework for the analysis of SUEPs - plain NanoAOD, extended by PF candidates and more track information + automatic crab submission. 

This format can be used with [fastjet](http://fastjet.fr) directly.

## Recipe

For UL data and MC **NanoAODv9** follow the PPD recommendations:

```
cmsrel  CMSSW_10_6_26
cd  CMSSW_10_6_26/src
cmsenv
git cms-addpkg PhysicsTools/NanoAOD
git clone -b autumn18 https://github.com/cericeci/SUEPNano.git PhysicsTools/SUEPNano
scram b -j 10
cd PhysicsTools/SUEPNano/test
```

Note: This configuration has been tested for this combination of CMSSW release, global tag, era and dataset. When running over a new dataset you should check with [the nanoAOD workbook twiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD#Running_on_various_datasets_from) to see if the era modifiers in the CRAB configuration files are correct. The jet correction versions are taken from the global tag.

## Local Usage. Please remember to test with a local file before proceeding without any submission:

2016 MC  

```
cmsRun nano16.py inputFiles=sample_name
```

2016APV MC        

```
cmsRun nano16APV.py inputFiles=sample_name
```

2017 MC        

```
cmsRun nano17.py inputFiles=sample_name
```

2018 MC        

```
cmsRun nano18.py inputFiles=sample_name
```

2016 data        

```
cmsRun nano16_data.py inputFiles=sample_name
```

2016APV data        

```
cmsRun nano16APV_data.py inputFiles=sample_name
```

2017 data        

```
cmsRun nano17_data.py inputFiles=sample_name
```

2018 data        

```
cmsRun nano18_datapy inputFiles=sample_name
```

## Crab submission

Examples are available in test/multicrab_year[data].py. For example, for the 2016 campaign:

```
source /cvmfs/cms.cern.ch/crab3/crab.csh
voms-proxy-init -voms cms
python multicrab_16.py
```

WARNING: this will submit 3k+ lengthy jobs to crab, so be careful that what you are sending is reasonable.


## Crab automating resubmission and reporting

First set up your proxy for a long time so it doesn't run out

``` 
voms-proxy-init -voms cms --valid 196:00:00
```

Then use to send automatic resubmission every 12 hours

```
python crabMonitoring.py
```

Alternatively for a one-off resubmission of all samples

```
python crabAutoTool.py
```

Warning: this will send you a mail every time you run it with a summary. Edit it out of the file if you don't want it
