#ifndef SimpleEventFilter_H
#define SimpleEventFilter_H

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
 
class SimpleEventFilter : public edm::EDFilter {
 public:
 SimpleEventFilter( const edm::ParameterSet & );
 ~SimpleEventFilter();
  private:
  bool filter( edm::Event & iEvent, const edm::EventSetup &iSetup);
  int nEvent_;
  int nInterval_;
  int nInterval_rest;
  bool verbose_;
};

#endif
