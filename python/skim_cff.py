import FWCore.ParameterSet.Config as cms


ZS_skim = cms.EDFilter("ZS_Skim",
                        srcmuons     = cms.InputTag("slimmedMuons"),
                        srcelectrons = cms.InputTag("slimmedElectrons"),
                        mu_minpt     = cms.double(10),
                        mu_maxeta    = cms.double(2.5),
                        mu_dxy       = cms.double(0.2),
                        mu_dz        = cms.double(0.2),
                        el_minpt     = cms.double(10),
                        el_maxeta    = cms.double(2.5),
                        el_dxy       = cms.double(0.2),
                        el_dz        = cms.double(0.2),
			            leadlep_pt   = cms.double(20)
                        )
