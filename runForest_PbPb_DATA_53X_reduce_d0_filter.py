import FWCore.ParameterSet.Config as cms
process = cms.Process('HiForest')
process.options = cms.untracked.PSet(
    # wantSummary = cms.untracked.bool(True)
    #SkipEvent = cms.untracked.vstring('ProductNotFound')
)

#####################################################################################
# Input source
#####################################################################################

process.source = cms.Source("PoolSource",
                            duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
                            fileNames = cms.untracked.vstring("file:/uscms_data/d3/jiansun/data/1CC46C43-99B9-E311-B9CF-FA163E4A10E1_highpt_rereco_run181913.root")
 #                           fileNames = cms.untracked.vstring("file:hiReco_RAW2DIGI_L1Reco_RECO_1001_2_8Ow.root")
                            )

# Number of events we want to process, -1 = all events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(50))


#####################################################################################
# Load Global Tag, Geometry, etc.
#####################################################################################

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.ReconstructionHeavyIons_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

# PbPb 53X MC
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'GR_R_53_LV6::All', '')

from HeavyIonsAnalysis.Configuration.CommonFunctions_cff import *
overrideGT_PbPb2760(process)
overrideJEC_pp2760(process)

process.HeavyIonGlobalParameters = cms.PSet(
    centralityVariable = cms.string("HFtowers"),
    nonDefaultGlauberModel = cms.string(""),
    centralitySrc = cms.InputTag("hiCentrality")
    )

#####################################################################################
# Define tree output
#####################################################################################

process.TFileService = cms.Service("TFileService",
                                   fileName=cms.string("HiForest_reduce_d0_filter.root"))


#####################################################################################
######################

process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_data_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.EventSelection_cff')

#Filtering
# Minimum bias trigger selection (later runs)
process.load("HLTrigger.HLTfilters.hltHighLevel_cfi")
process.hltMinBiasHFOrBSC = process.hltHighLevel.clone()
process.hltMinBiasHFOrBSC.HLTPaths = ["HLT_HIMinBiasHfOrBSC_v1"]
process.load("HeavyIonsAnalysis.Configuration.collisionEventSelection_cff")

process.skimanalysis.superFilters = cms.vstring("ana_step")

process.reducedEcalRecHitsEB = cms.EDProducer("ReducedRecHitCollectionProducer",
    interestingDetIdCollections = cms.VInputTag(cms.InputTag("interestingEcalDetIdEB"), cms.InputTag("interestingEcalDetIdEBU")),
    recHitsLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
    reducedHitsCollection = cms.string('')
)
process.reducedEcalRecHitsEE = cms.EDProducer("ReducedRecHitCollectionProducer",
    interestingDetIdCollections = cms.VInputTag(cms.InputTag("interestingEcalDetIdEE")),
    recHitsLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
    reducedHitsCollection = cms.string('')
)

process.pcollisionEventSelection = cms.Path(process.collisionEventSelection)
process.pHBHENoiseFilter = cms.Path( process.HBHENoiseFilter )
process.phfCoincFilter = cms.Path(process.hfCoincFilter )
process.phfCoincFilter3 = cms.Path(process.hfCoincFilter3 )
process.pprimaryVertexFilter = cms.Path(process.primaryVertexFilter )
process.phltPixelClusterShapeFilter = cms.Path(process.siPixelRecHits*process.hltPixelClusterShapeFilter )
process.phiEcalRecHitSpikeFilter = cms.Path(process.hiEcalRecHitSpikeFilter )


process.ana_step = cms.Path(process.hltanalysis *
                            process.hiEvtAnalyzer
#                            process.HiForest                             
                            )

process.pAna = cms.EndPath(process.skimanalysis)

process.tree = cms.EDAnalyzer(
    "HFTree",
    verbose      = cms.untracked.int32(1),
    printFrequency = cms.untracked.int32(1000),
    requireCand  =  cms.untracked.bool(False)
    )

# ----------------------------------------------------------------------
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("UserCode.OpenHF.HFRecoStuff_cff")
process.load("UserCode.OpenHF.HFCharm_cff")

process.d0Dump.trackPt = cms.untracked.double(2.0)
# ----------------------------------------------------------------------
process.dmeson = cms.Path(
    process.recoStuffSequence*
    process.d0Sequence*
    process.tree
)

process.load("UserCode.Crab_filter.EventFilter_cff")

process.simpleEventFilter.nInterval = cms.untracked.int32(6)
process.simpleEventFilter.nInterval_rest = cms.untracked.int32(0)
process.simpleEventFilter.DebugOn      = cms.untracked.bool(True)

for path in process.paths:
	        getattr(process,path)._seq = process.simpleEventFilter*getattr(process,path)._seq

process.schedule = cms.Schedule(process.pcollisionEventSelection, process.pHBHENoiseFilter,process.phfCoincFilter, process.phfCoincFilter3, process.pprimaryVertexFilter, process.phltPixelClusterShapeFilter, process.phiEcalRecHitSpikeFilter, process.ana_step,process.pAna, process.dmeson)
