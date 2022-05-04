from WMCore.Configuration import Configuration
config = Configuration()

import datetime,os
cTime=datetime.datetime.now()
date_str='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)

relBase = os.environ['CMSSW_BASE']
home = os.environ['HOME']

####################
### SET YOUR STRINGS
####################
cmsRun_config  = 'crabConfigs_multiLep2017/run_FWLJMET_WWZ.py'
inputDataset   = '/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM'
requestName    = 'multiLep2017'
outputFolder   = 'FWLJMET102X_3lep2017_wywong_012020'
logFolder      = 'WWZ'
Json_for_data  = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
isMC           = True
isVLQsignal    = False
#isTTbar        = ISTTBAR

##############
### GENERAL
##############
config.section_("General")
config.General.requestName = requestName+"_"+logFolder
config.General.workArea = 'crabSubmitLogs/'+requestName+'/'
#config.General.workArea = home+'/nobackup/FWLJMET102X_crabSubmitLogs/'+requestName+'/'  #JH: crab stuff in nobackup
config.General.transferLogs = True
config.General.transferOutputs = True


##############
### JobType
##############
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = cmsRun_config

#cmsRun params
#config.JobType.pyCfgParams = ['dataset='+dataset]
#if(isMC):
#	config.JobType.pyCfgParams = ['isMC=True']
#else:
#	config.JobType.pyCfgParams = ['isMC=False']
#
#if(isTTbar):
#	config.JobType.pyCfgParams += ['isTTbar=True']

#for VLQ signal this will run using crab_script.sh which will reset the env var in order to access LHApdf outside of CMSSW
if(isVLQsignal):
	config.JobType.scriptExe = relBase+'/src/FWLJMET/LJMet/CRAB3/crab_script.sh'
#else:
#	config.JobType.pyCfgParams += ['isVLQsignal=False']
	
# runtime, memory, cores
if(isMC):
	config.JobType.maxJobRuntimeMin = 2750 #minutes
config.JobType.maxMemoryMB = 4000 #MB, believed to be per core based on CRAB3FAQ TWiki, evidently not based on tests
config.JobType.numCores = 4 #use wisely if turned on.

##############
### DATA
##############
config.section_("Data")
config.Data.inputDataset = inputDataset
config.Data.allowNonValidInputDataset = True
if(isMC):
	#config.Data.splitting = 'Automatic'
	#config.Data.unitsPerJob = 1440 # 24 hours
	if(isVLQsignal):
		config.Data.splitting = 'LumiBased'
		config.Data.unitsPerJob = 2
	else:
		config.Data.splitting = 'FileBased'
		config.Data.unitsPerJob = 1
else:
	config.Data.splitting = 'Automatic'
	config.Data.unitsPerJob = 1440 # 24 hours
	config.Data.lumiMask = Json_for_data
config.Data.inputDBS = 'global'
config.Data.ignoreLocality = False
config.Data.publication = False
# This string is used to construct the output dataset name : /store/user/lpcljm/<outputFolder>/<inpuDataset>/<requestName>/<someCRABgeneratedNumber>/<someCRABgeneratedNumber>/
config.Data.outputDatasetTag = requestName
config.Data.outLFNDirBase = '/store/group/lpcljm/'+outputFolder

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'
