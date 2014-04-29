import FWCore.ParameterSet.Config as cms

#-----------------------------------
#  Simple Event Filter
#-----------------------------------
simpleEventFilter = cms.EDFilter("SimpleEventFilter",
           nInterval = cms.untracked.int32(2),
		   nInterval_rest = cms.untracked.int32(0),
           DebugOn      = cms.untracked.bool(True)                                               
                                      
)
