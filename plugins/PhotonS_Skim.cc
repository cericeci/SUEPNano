// user include files
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

//classes to extract Lepton information
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"

#include <vector>
#include <iostream>

//
// class declaration
//

class PhotonS_Skim : public edm::stream::EDFilter<> {
   public:
      explicit PhotonS_Skim(const edm::ParameterSet&);
      ~PhotonS_Skim();

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
  edm::EDGetTokenT<std::vector<pat::Photon>> photonInput;
  double pho_minpt_;
  double pho_etacut_;
};

// constructors and destructor
//
PhotonS_Skim::PhotonS_Skim(const edm::ParameterSet& iConfig)
{
   //now do what ever initialization is needed
  photonInput   = consumes<std::vector<pat::Photon>>(iConfig.getParameter<edm::InputTag>("srcphotons"));
  pho_minpt_   = iConfig.getParameter<double>("pho_minpt");
  pho_etacut_  = iConfig.getParameter<double>("pho_maxeta");
}


PhotonS_Skim::~PhotonS_Skim()
{
 
}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
PhotonS_Skim::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  // Get photons
  edm::Handle<std::vector<pat::Photon>> photons;
  iEvent.getByToken(photonInput, photons);

  // Loop over photons
  if(photons.isValid()){
    for (std::vector<pat::Photon>::const_iterator itphoton=photons->begin(); itphoton!=photons->end(); ++itphoton){
      if(abs(itphoton->eta())<pho_etacut_ && itphoton->pt()>pho_minpt_ && itphoton->photonID("mvaPhoID-RunIIFall17-v2-wp90")){
	return true;
      }
    }
  }

  return false;
}

// ------------ method called once each job just before starting event loop  ------------
void 
PhotonS_Skim::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
PhotonS_Skim::endJob() {
}

// ------------ method called when starting to processes a run  ------------
bool 
PhotonS_Skim::beginRun(edm::Run&, edm::EventSetup const&)
{ 
  return true;
}

// ------------ method called when ending the processing of a run  ------------
bool 
PhotonS_Skim::endRun(edm::Run&, edm::EventSetup const&)
{
  return true;
}

// ------------ method called when starting to processes a luminosity block  ------------
bool 
PhotonS_Skim::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}

// ------------ method called when ending the processing of a luminosity block  ------------
bool 
PhotonS_Skim::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
PhotonS_Skim::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(PhotonS_Skim);
