// user include files
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

//classes to extract Lepton information
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"

#include <vector>
#include <iostream>

//
// class declaration
//

class ZS_Skim : public edm::EDFilter {
   public:
      explicit ZS_Skim(const edm::ParameterSet&);
      ~ZS_Skim();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual bool filter(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual bool beginRun(edm::Run&, edm::EventSetup const&);
      virtual bool endRun(edm::Run&, edm::EventSetup const&);
      virtual bool beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual bool endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      // ----------member data ---------------------------
  edm::EDGetTokenT<std::vector<pat::Muon>> muonInput;
  edm::EDGetTokenT<std::vector<pat::Electron>> elecInput;
  double mu_minpt_;
  double mu_etacut_;
  double el_minpt_;
  double el_etacut_;
  double mu_dxy_;
  double mu_dz_;
  double el_dxy_;
  double el_dz_;
  double leadlep_pt_;
};

// constructors and destructor
//
ZS_Skim::ZS_Skim(const edm::ParameterSet& iConfig)
{
   //now do what ever initialization is needed
  muonInput   = consumes<std::vector<pat::Muon>>(iConfig.getParameter<edm::InputTag>("srcmuons"));
  elecInput   = consumes<std::vector<pat::Electron>>(iConfig.getParameter<edm::InputTag>("srcelectrons"));
  mu_minpt_   = iConfig.getParameter<double>("mu_minpt");
  mu_etacut_  = iConfig.getParameter<double>("mu_maxeta");
  el_minpt_   = iConfig.getParameter<double>("el_minpt");
  el_etacut_  = iConfig.getParameter<double>("el_maxeta");
  mu_dxy_     = iConfig.getParameter<double>("mu_dxy");
  mu_dz_      = iConfig.getParameter<double>("mu_dz");
  el_dxy_     = iConfig.getParameter<double>("el_dxy");
  el_dz_      = iConfig.getParameter<double>("el_dz");
  leadlep_pt_ = iConfig.getParameter<double>("leadlep_pt"); 
}


ZS_Skim::~ZS_Skim()
{
 
}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
ZS_Skim::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  std::cout << "Starting filter..." << std::endl;
  // Get muons
  edm::Handle<std::vector<pat::Muon>> muons;
  iEvent.getByToken(muonInput, muons);

  // Get electrons
  edm::Handle<std::vector<pat::Electron>> electrons;
  iEvent.getByToken(elecInput, electrons);

  // All relevant flags
  bool isGoodDilep  =false;
  bool isGoodLeading=false;
  int nMuons = 0;
  int nElectrons = 0;

  // Loop over muons
  if(muons.isValid()){
    for (std::vector<pat::Muon>::const_iterator itmuon=muons->begin(); itmuon!=muons->end(); ++itmuon){
      if(abs(itmuon->eta())<mu_etacut_ && itmuon->pt()>mu_minpt_ && abs(itmuon->dB(pat::Muon::IPTYPE::PV2D))<mu_dxy_ && abs(itmuon->dB(pat::Muon::IPTYPE::PVDZ))<mu_dz_){
	nMuons += 1;
        if (itmuon->pt() > leadlep_pt_) isGoodLeading=true;
      }
    }
  }

  // Loop over electrons
  if(electrons.isValid()){
    for (std::vector<pat::Electron>::const_iterator itelectron=electrons->begin(); itelectron!=electrons->end(); ++itelectron){
      if(abs(itelectron->eta())<el_etacut_ && itelectron->pt()>el_minpt_ && abs(itelectron->dB(pat::Electron::IPTYPE::PV2D))<el_dxy_ && abs(itelectron->dB(pat::Electron::IPTYPE::PVDZ))<el_dz_){
        nElectrons += 1;
        if (itelectron->pt() > leadlep_pt_) isGoodLeading=true;
      }
    }
  }

  if (nMuons + nElectrons >=2) isGoodDilep = true;
  std::cout << "Event is " << isGoodDilep << " ; " << isGoodLeading << std::endl;
  return isGoodDilep && isGoodLeading;
}

// ------------ method called once each job just before starting event loop  ------------
void 
ZS_Skim::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
ZS_Skim::endJob() {
}

// ------------ method called when starting to processes a run  ------------
bool 
ZS_Skim::beginRun(edm::Run&, edm::EventSetup const&)
{ 
  return true;
}

// ------------ method called when ending the processing of a run  ------------
bool 
ZS_Skim::endRun(edm::Run&, edm::EventSetup const&)
{
  return true;
}

// ------------ method called when starting to processes a luminosity block  ------------
bool 
ZS_Skim::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}

// ------------ method called when ending the processing of a luminosity block  ------------
bool 
ZS_Skim::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
ZS_Skim::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(ZS_Skim);
