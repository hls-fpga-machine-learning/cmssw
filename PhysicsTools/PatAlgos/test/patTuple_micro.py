## import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import cms, process
## switch to uncheduled mode
process.options.allowUnscheduled = cms.untracked.bool(True)
#process.Tracer = cms.Service("Tracer")

process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
process.load("PhysicsTools.PatAlgos.selectionLayer1.selectedPatCandidates_cff")

## ------------------------------------------------------
#  In addition you usually want to change the following
#  parameters:
## ------------------------------------------------------
#
#   process.GlobalTag.globaltag =  ...    ##  (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#                                         ##
#process.source.fileNames = {'/store/relval/CMSSW_7_0_0/RelValTTbar_13/GEN-SIM-RECO/PU25ns_POSTLS170_V3-v2/00000/5A98DF7C-C998-E311-8FF8-003048FEADBC.root'}
process.source.fileNames = {
'/store/relval/CMSSW_7_0_0/RelValTTbar_13/GEN-SIM-RECO/PU50ns_POSTLS170_V4-v2/00000/265B9219-FF98-E311-BF4A-02163E00EA95.root',
'/store/relval/CMSSW_7_0_0/RelValTTbar_13/GEN-SIM-RECO/PU50ns_POSTLS170_V4-v2/00000/36598DF8-D098-E311-972E-02163E00E744.root',
'/store/relval/CMSSW_7_0_0/RelValTTbar_13/GEN-SIM-RECO/PU50ns_POSTLS170_V4-v2/00000/542AC938-CA98-E311-8928-02163E00E5F5.root',
'/store/relval/CMSSW_7_0_0/RelValTTbar_13/GEN-SIM-RECO/PU50ns_POSTLS170_V4-v2/00000/6A95EE20-CD98-E311-8FAE-02163E00A1F2.root',
'/store/relval/CMSSW_7_0_0/RelValTTbar_13/GEN-SIM-RECO/PU50ns_POSTLS170_V4-v2/00000/822E181D-D898-E311-8A29-02163E00E928.root',
'/store/relval/CMSSW_7_0_0/RelValTTbar_13/GEN-SIM-RECO/PU50ns_POSTLS170_V4-v2/00000/E00EF5A1-CE98-E311-B221-02163E00E8AE.root',
'/store/relval/CMSSW_7_0_0/RelValTTbar_13/GEN-SIM-RECO/PU50ns_POSTLS170_V4-v2/00000/F60ED2AC-CB98-E311-ACBA-02163E00E62F.root'
}

##'/store/relval/CMSSW_7_0_0/RelValTTbar_13/GEN-SIM-RECO/PU50ns_POSTLS170_V4-v2/00000/36598DF8-D098-E311-972E-02163E00E744.root'}
#                                         ##
process.maxEvents.input = -1

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.prunedGenParticles = cms.EDProducer("GenParticlePruner",
    src = cms.InputTag("genParticles"),
    select = cms.vstring(
        "drop  *", # this is the default
        "keep status == 3",  #keep event summary status3 (for pythia)
        "++keep abs(pdgId) == 11 || abs(pdgId) == 13 || abs(pdgId) == 15", # keep leptons, with history
        "++keep pdgId == 22 && status == 1 && pt > 10",                    # keep gamma above 10 GeV
        "drop   status == 2",                                              # drop the shower part of the history
        "keep++ abs(pdgId) == 15",                                         # but keep keep taus with decays
        "++keep  4 <= abs(pdgId) <= 6 ",                                   # keep also heavy quarks
        "++keep  (400 < abs(pdgId) < 600) || (4000 < abs(pdgId) < 6000)",  # and their hadrons 
        "drop   status == 2 && abs(pdgId) == 22",                          # but remove again gluons in the inheritance chain
    )
)
#### FIXME here we should change all mcMatchers to use these genParticles,
#### and then turn OFF the embedding of the genParticle in the PAT Objects

process.packedPFCandidates = cms.EDProducer("PATPackedCandidateProducer",
    inputCollection = cms.InputTag("particleFlow"),
    inputCollectionFromPV = cms.InputTag("pfNoPileUp"), ## or ForIso? or JME?
)

process.offlineSlimmedPrimaryVertices = cms.EDProducer("PATVertexSlimmer",
    src = cms.InputTag("offlinePrimaryVertices"),
)

process.patMuons.isoDeposits = cms.PSet()
process.patElectrons.isoDeposits = cms.PSet()
process.patTaus.isoDeposits = cms.PSet()
process.patPhotons.isoDeposits = cms.PSet()

process.patMuons.embedTrack         = True  # used for IDs
process.patMuons.embedCombinedMuon  = True  # used for IDs
process.patMuons.embedMuonBestTrack = True  # used for IDs
process.patMuons.embedStandAloneMuon = True # maybe?
process.patMuons.embedPickyMuon = False   # no, use best track
process.patMuons.embedTpfmsMuon = False   # no, use best track
process.patMuons.embedDytMuon   = False   # no, use best track

process.selectedPatJets.cut = cms.string("pt > 10")
process.selectedPatMuons.cut = cms.string("pt > 3") 
process.selectedPatElectrons.cut = cms.string("pt > 5") 
process.selectedPatTaus.cut = cms.string("pt > 20")

from PhysicsTools.PatAlgos.tools.trigTools import switchOnTriggerStandAlone
switchOnTriggerStandAlone( process )
process.patTrigger.packTriggerPathNames = cms.bool(True)
process.selectedPatTrigger = cms.EDFilter("PATTriggerObjectStandAloneSelector",
    src = cms.InputTag("patTrigger"),
    cut = cms.string("!filterLabels.empty()")
)

#                                         ##
#   process.options.wantSummary = False   ##  (to suppress the long output at the end of the job)
#                                         ##

#   process.out.outputCommands = [ ... ]  ##  (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#                                         ##
process.out.fileName = 'patTuple_micro.root'
process.out.outputCommands = [
    'drop *',
    'keep *_selectedPatPhotons*_*_*',
    'keep *_selectedPatElectrons*_*_*',
    'keep *_selectedPatMuons*_*_*',
    'keep *_selectedPatTaus*_*_*',
    'keep *_selectedPatJets*_*_*',
    'keep *_patMETs*_*_*',
    ## add extra METs

    'drop *_*_caloTowers_*',
    'drop *_*_pfCandidates_*',
    'keep *_*_genJets_*',

    'keep *_offlineSlimmedPrimaryVertices_*_*',
    'keep *_packedPFCandidates_*_*',

    #'keep double_*_rho_*', ## need to understand what are the rho's in 70X

    'keep *_selectedPatTrigger_*_PAT',
    'keep *_l1extraParticles_*_HLT',
    'keep *_TriggerResults_*_HLT',

    #'keep *_TriggerResults_*_PAT', # this will be needed for MET filters

    'keep *_prunedGenParticles_*_*',
    'keep LHEEventProduct_source_*_*',
    'keep PileupSummaryInfos_*_*_*',
    'keep GenRunInfoProduct_*_*_*',
    'keep GenFilterInfo_*_*_*',

]
process.out.dropMetaData = cms.untracked.string('ALL')

