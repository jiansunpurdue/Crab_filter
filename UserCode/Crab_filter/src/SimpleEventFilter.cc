#include "UserCode/Crab_filter/src/SimpleEventFilter.h" 
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include <iostream>
 
//
// -- Constructor
//
SimpleEventFilter::SimpleEventFilter( const edm::ParameterSet & pset ) {
   nInterval_ = pset.getUntrackedParameter<int>( "nInterval", 5 );
   nInterval_rest = pset.getUntrackedParameter<int>( "nInterval_rest", 0 );
   verbose_   = pset.getUntrackedParameter<bool>( "DebugOn", false );
   nEvent_    = 0;
}
//
// -- Destructor
//
SimpleEventFilter::~SimpleEventFilter() {
}
 
bool SimpleEventFilter::filter(edm::Event & iEvent, const edm::EventSetup &iSetup) {
  nEvent_++;
  int evtnumber = iEvent.id().event();
  bool ret = false;
//  std::cout << " nInterval: " << nInterval_ << std::endl;
  if (nEvent_ % nInterval_ == nInterval_rest) ret = true; 
  if ( verbose_ && !ret) std::cout << ">>> filtering event" << nEvent_ << std::endl; 
  return ret;
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(SimpleEventFilter);
