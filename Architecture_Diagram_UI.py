import streamlit as st
import os
import openai
import pydot
import re
import base64
from io import BytesIO
from pathlib import Path
from IPython.display import Image
from langchain.memory import ChatMessageHistory
from PIL import Image
from graphviz import Source
import time
from graphviz import Source
from graphviz import Digraph
import glob
all_prompts = []


MAX_CONTEXT_QUESTIONS = 10
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown(
        "![Alt Text](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAB+CAMAAADY4yX9AAAAilBMVEX///8AcK0Sq9sAbqwAqNoAZqgAaqoAaKkAptkAY6cAbKsSrt0ApNgAX6X7/f7O3erh6vLH2OcQn9GxyN7l8/qCyejy9/rp8PY1fbSqw9thk7+Z0eu23vBlv+Oq2u/L6PVNhriaudWOsNBUjr1tnMR4oscodbAHebQEgboSi8AOk8hPuOHa7/iCqczpSEsYAAAEkklEQVRoge2a2ZKiMBRAgbAviqIsbtBq49b+/+9NAu0ChCSQYFdNcV6m5qVP3TUBlKSRkZGRkf+byR95o3g1/RNvZujaIQj/wCvLMrDir8+qo9yWC4Cm7z+onnlAfgB06x59yLu35ArGZ6L2D5pcA2h5Mvh0JbJd9xZtls0G1YYrC6NF2NZxwFIHBi7cpzoZSOtnFmj3QqzMH0A72euEcEt0W3zQs1gjh1uircROVvStUcP9DRqIPDsSYLBpEeJ6zI8pTVXDOwrZJuG310kLMWIBhQ7yDll+YMu8cwUXc9dwS7PO12KJoffRyui05Njd/qFtMbOYjd7mL4txdFvQ+pn9uHHsdo65T50T+mKmm/XOB2V07NfMdXPXeZ7GPWYXh7HqtMMSzq56w/rq4D16orTIzNzaYcbbzRVAzthgvqjyPtBXTN5pLqy8D6yAJV5bxBRVAQa9s/1uBz4jxp3uHUAL8SiHsy++viX6kegNs75nLxWNeFocBc/RG8SQv4TujSoAtFd5qMYq0fat4lzwIAHE67952ywLTTSwT+fz5XI5n08PudayviJDXMD26TJXnAJFMa+lu21jfwvraCBfFSh84jjzE1oPGjbXvrBE26eKtnRfQduVU1jA9qWhRWYTLmxcX0eyoArbV5wX4sp2jBEngjKtt3lhtm0PU+RMzOEAWr3QfPaa+1rQ6Q+w9X1gYt4TBEIyDU4kr+Kcmt11FJNpkhZyba4QIWsazIkBQw717pqIuL/jB7iS60tdLORAPFG0KNf1B7iZgN7S53TxvC4W0NTgTEs0Tsy/twCtowvMhpj7hCCtrDeEi8GZRas49a7mr7HJJL7VxbxdTR/hAnVZ83LPMcMII8xdXcy5uXTqrixxF3Ux365mGmGE0/BKR56HNaAyZnrdFAcc89R6y2LItOT3j5hy+r9Qt00vvHP1LjJgOBxKMSZgjhXCnGhchSX0/btnvIwjrKiNrfXLvV972Wy7Eop/8F4p6nXBZe/oTYtXkvY9qvxcHdu1S/Y2luWLSfcqvybJCZckMyFeCf3OobP5WWA4Ku0xq0pK8sIn1Y5b5O0ejULaqfjV6W6xA/ye7LhTf72fScVW+rlhzKZDTHNJp0c3L7i9p7OYlo1TjVo1nR3TF4kpe2d7Sfg+SY9FnC4V13VVCPzHWVOK+2LG+MkHWIG0qewO8+kI090asmnbGC0xM2Vbl2eStK1WtHGD7IjP8K1YQz+5+Kl1UusyZiVcUQoNrDu6l2/rLazeeL+RBzppoDW5eJORNvcFdVHQg757Or7UwALle4ywObEK2hX8arv5jQ/oXhb8FhK3K8rBXacLrmKHyerkGajH0btfYOuWkd39x59sFPjNrSqOgr9tsBJN94c4znOQ53F2DPxn70wI3iLjjUeVHoSR7/tRJXmLljw/e4xhO/dhZxK99MOoH6lDvGu4N96+xrLYOKTLnereBsjyIl3fFJLWVbbpEL9T/FFcwgyZym0zTG3hEK1V3OVGVWGzLQezlmyW8Hw31QcmOuy364Glv0zgMb8sgGd9+hHlyMjIyMjIyED8Ax/ZVkQ3zARGAAAAAElFTkSuQmCC)")
with col2:
    st.title("Architecture Diagram")
    st.write("Generative AI")
output = None


# openai.api_type = "azure"
# openai.api_base = "https://capgeminiopenai.openai.azure.com/"
# openai.api_version = "2023-07-01-preview"
# openai.api_key = "bd1badfce950429ab2e42504ade5079c"
# MAX_CONTEXT_QUESTIONS = 10


Diagram_Node = '''
<Cloud_Provider> <Resource_type> <Node>
gcp analytics Bigquery
gcp analytics BigQuery
gcp analytics Composer
gcp analytics DataCatalog
gcp analytics DataFusion
gcp analytics Dataflow
gcp analytics Datalab
gcp analytics Dataprep
gcp analytics Dataproc
gcp analytics Genomics
gcp analytics pubsub
gcp analytics PubSub
gcp api APIGateway
gcp api Endpoints
gcp compute GAE
gcp compute AppEngine
gcp compute ComputeEngine
gcp compute GCE
gcp compute ContainerOptimizedOS
gcp compute Functions
gcp compute GCF
gcp compute GKEOnPrem
gcp compute GPU
gcp compute KubernetesEngine
gcp compute GKE
gcp compute Run
gcp database Bigtable
gcp database BigTable
gcp database Datastore
gcp database Firestore
gcp database Memorystore
gcp database Spanner
gcp database SQL
gcp devtools Build
gcp devtools CodeForIntellij
gcp devtools Code
gcp devtools ContainerRegistry
gcp devtools GCR
gcp devtools GradleAppEnginePlugin
gcp devtools IdePlugins
gcp devtools MavenAppEnginePlugin
gcp devtools Scheduler
gcp devtools SDK
gcp devtools SourceRepositories
gcp devtools Tasks
gcp devtools TestLab
gcp devtools ToolsForEclipse
gcp devtools ToolsForPowershell
gcp devtools ToolsForVisualStudio
gcp iot IotCore
gcp migration TransferAppliance
gcp ml AdvancedSolutionsLab
gcp ml AIHub
gcp ml AIPlatformDataLabelingService
gcp ml AIPlatform
gcp ml AutomlNaturalLanguage
gcp ml AutomlTables
gcp ml AutomlTranslation
gcp ml AutomlVideoIntelligence
gcp ml AutomlVision
gcp ml Automl
gcp ml AutoML
gcp ml DialogFlowEnterpriseEdition
gcp ml InferenceAPI
gcp ml JobsAPI
gcp ml NaturalLanguageAPI
gcp ml NLAPI
gcp ml RecommendationsAI
gcp ml SpeechToText
gcp ml STT
gcp ml TextToSpeech
gcp ml TTS
gcp ml TPU
gcp ml TranslationAPI
gcp ml VideoIntelligenceAPI
gcp ml VisionAPI
gcp network Armor
gcp network CDN
gcp network DedicatedInterconnect
gcp network DNS
gcp network ExternalIpAddresses
gcp network FirewallRules
gcp network LoadBalancing
gcp network NAT
gcp network Network
gcp network PartnerInterconnect
gcp network PremiumNetworkTier
gcp network Router
gcp network Routes
gcp network StandardNetworkTier
gcp network TrafficDirector
gcp network VirtualPrivateCloud
gcp network VPC
gcp network VPN
gcp operations Monitoring
gcp security Iam
gcp security IAP
gcp security KeyManagementService
gcp security KMS
gcp security ResourceManager
gcp security SecurityCommandCenter
gcp security SCC
gcp security SecurityScanner
gcp storage Filestore
gcp storage PersistentDisk
gcp storage GCS
aws analytics Analytics
aws analytics Athena
aws analytics CloudsearchSearchDocuments
aws analytics Cloudsearch
aws analytics DataLakeResource
aws analytics DataPipeline
aws analytics ElasticsearchService
aws analytics ES
aws analytics EMRCluster
aws analytics EMREngineMaprM3
aws analytics EMREngineMaprM5
aws analytics EMREngineMaprM7
aws analytics EMREngine
aws analytics EMRHdfsCluster
aws analytics EMR
aws analytics GlueCrawlers
aws analytics GlueDataCatalog
aws analytics Glue
aws analytics KinesisDataAnalytics
aws analytics KinesisDataFirehose
aws analytics KinesisDataStreams
aws analytics KinesisVideoStreams
aws analytics Kinesis
aws analytics LakeFormation
aws analytics ManagedStreamingForKafka
aws analytics Quicksight
aws analytics RedshiftDenseComputeNode
aws analytics RedshiftDenseStorageNode
aws analytics Redshift
aws ar ArVr
aws ar Sumerian
aws blockchain BlockchainResource
aws blockchain Blockchain
aws blockchain ManagedBlockchain
aws blockchain QuantumLedgerDatabaseQldb
aws blockchain QLDB
aws business AlexaForBusiness
aws business A4B
aws business BusinessApplications
aws business Chime
aws business Workmail
aws compute AppRunner
aws compute ApplicationAutoScaling
aws compute AutoScaling
aws compute Batch
aws compute ComputeOptimizer
aws compute Compute
aws compute EC2Ami
aws compute AMI
aws compute EC2AutoScaling
aws compute EC2ContainerRegistryImage
aws compute EC2ContainerRegistryRegistry
aws compute EC2ContainerRegistry
aws compute ECR
aws compute EC2ElasticIpAddress
aws compute EC2ImageBuilder
aws compute EC2Instance
aws compute EC2Instances
aws compute EC2Rescue
aws compute EC2SpotInstance
aws compute EC2
aws compute ElasticBeanstalkApplication
aws compute ElasticBeanstalkDeployment
aws compute ElasticBeanstalk
aws compute EB
aws compute ElasticContainerServiceContainer
aws compute ElasticContainerServiceService
aws compute ElasticContainerService
aws compute ECS
aws compute ElasticKubernetesService
aws compute EKS
aws compute Fargate
aws compute LambdaFunction
aws compute Lambda
aws compute Lightsail
aws compute LocalZones
aws compute Outposts
aws compute ServerlessApplicationRepository
aws compute SAR
aws compute ThinkboxDeadline
aws compute ThinkboxDraft
aws compute ThinkboxFrost
aws compute ThinkboxKrakatoa
aws compute ThinkboxSequoia
aws compute ThinkboxStoke
aws compute ThinkboxXmesh
aws compute VmwareCloudOnAWS
aws compute Wavelength
aws cost Budgets
aws cost CostAndUsageReport
aws cost CostExplorer
aws cost CostManagement
aws cost ReservedInstanceReporting
aws cost SavingsPlans
aws database AuroraInstance
aws database Aurora
aws database DatabaseMigrationServiceDatabaseMigrationWorkflow
aws database DatabaseMigrationService
aws database DMS
aws database Database
aws database DB
aws database DocumentdbMongodbCompatibility
aws database DocumentDB
aws database DynamodbAttribute
aws database DynamodbAttributes
aws database DynamodbDax
aws database DAX
aws database DynamodbGlobalSecondaryIndex
aws database DynamodbGSI
aws database DynamodbItem
aws database DynamodbItems
aws database DynamodbTable
aws database Dynamodb
aws database DDB
aws database ElasticacheCacheNode
aws database ElasticacheForMemcached
aws database ElasticacheForRedis
aws database Elasticache
aws database ElastiCache
aws database KeyspacesManagedApacheCassandraService
aws database Neptune
aws database QuantumLedgerDatabaseQldb
aws database QLDB
aws database RDSInstance
aws database RDSMariadbInstance
aws database RDSMysqlInstance
aws database RDSOnVmware
aws database RDSOracleInstance
aws database RDSPostgresqlInstance
aws database RDSSqlServerInstance
aws database RDS
aws database RedshiftDenseComputeNode
aws database RedshiftDenseStorageNode
aws database Redshift
aws database Timestream
aws devtools CloudDevelopmentKit
aws devtools Cloud9Resource
aws devtools Cloud9
aws devtools Codebuild
aws devtools Codecommit
aws devtools Codedeploy
aws devtools Codepipeline
aws devtools Codestar
aws devtools CommandLineInterface
aws devtools CLI
aws devtools DeveloperTools
aws devtools DevTools
aws devtools ToolsAndSdks
aws devtools XRay
aws enablement CustomerEnablement
aws enablement Iq
aws enablement ManagedServices
aws enablement ProfessionalServices
aws enablement Support
aws enduser Appstream20
aws enduser DesktopAndAppStreaming
aws enduser Workdocs
aws enduser Worklink
aws enduser Workspaces
aws engagement Connect
aws engagement CustomerEngagement
aws engagement Pinpoint
aws engagement SimpleEmailServiceSesEmail
aws engagement SimpleEmailServiceSes
aws engagement SES
aws game GameTech
aws game Gamelift
aws general Client
aws general Disk
aws general Forums
aws general General
aws general GenericDatabase
aws general GenericFirewall
aws general GenericOfficeBuilding
aws general OfficeBuilding
aws general GenericSamlToken
aws general GenericSDK
aws general InternetAlt1
aws general InternetAlt2
aws general InternetGateway
aws general Marketplace
aws general MobileClient
aws general Multimedia
aws general OfficeBuilding
aws general SamlToken
aws general SDK
aws general SslPadlock
aws general TapeStorage
aws general Toolkit
aws general TraditionalServer
aws general User
aws general Users
aws integration ApplicationIntegration
aws integration Appsync
aws integration ConsoleMobileApplication
aws integration EventResource
aws integration EventbridgeCustomEventBusResource
aws integration EventbridgeDefaultEventBusResource
aws integration EventbridgeSaasPartnerEventBusResource
aws integration Eventbridge
aws integration ExpressWorkflows
aws integration MQ
aws integration SimpleNotificationServiceSnsEmailNotification
aws integration SimpleNotificationServiceSnsHttpNotification
aws integration SimpleNotificationServiceSnsTopic
aws integration SimpleNotificationServiceSns
aws integration SNS
aws integration SimpleQueueServiceSqsMessage
aws integration SimpleQueueServiceSqsQueue
aws integration SimpleQueueServiceSqs
aws integration SQS
aws integration StepFunctions
aws integration SF
aws iot Freertos
aws iot FreeRTOS
aws iot InternetOfThings
aws iot Iot1Click
aws iot IotAction
aws iot IotActuator
aws iot IotAlexaEcho
aws iot IotAlexaEnabledDevice
aws iot IotAlexaSkill
aws iot IotAlexaVoiceService
aws iot IotAnalyticsChannel
aws iot IotAnalyticsDataSet
aws iot IotAnalyticsDataStore
aws iot IotAnalyticsNotebook
aws iot IotAnalyticsPipeline
aws iot IotAnalytics
aws iot IotBank
aws iot IotBicycle
aws iot IotButton
aws iot IotCamera
aws iot IotCar
aws iot IotCart
aws iot IotCertificate
aws iot IotCoffeePot
aws iot IotCore
aws iot IotDesiredState
aws iot IotDeviceDefender
aws iot IotDeviceGateway
aws iot IotDeviceManagement
aws iot IotDoorLock
aws iot IotEvents
aws iot IotFactory
aws iot IotFireTvStick
aws iot IotFireTv
aws iot IotGeneric
aws iot IotGreengrassConnector
aws iot IotGreengrass
aws iot IotHardwareBoard
aws iot IotBoard
aws iot IotHouse
aws iot IotHttp
aws iot IotHttp2
aws iot IotJobs
aws iot IotLambda
aws iot IotLightbulb
aws iot IotMedicalEmergency
aws iot IotMqtt
aws iot IotOverTheAirUpdate
aws iot IotPolicyEmergency
aws iot IotPolicy
aws iot IotReportedState
aws iot IotRule
aws iot IotSensor
aws iot IotServo
aws iot IotShadow
aws iot IotSimulator
aws iot IotSitewise
aws iot IotThermostat
aws iot IotThingsGraph
aws iot IotTopic
aws iot IotTravel
aws iot IotUtility
aws iot IotWindfarm
aws management AutoScaling
aws management Chatbot
aws management CloudformationChangeSet
aws management CloudformationStack
aws management CloudformationTemplate
aws management Cloudformation
aws management Cloudtrail
aws management CloudwatchAlarm
aws management CloudwatchEventEventBased
aws management CloudwatchEventTimeBased
aws management CloudwatchRule
aws management Cloudwatch
aws management Codeguru
aws management CommandLineInterface
aws management Config
aws management ControlTower
aws management LicenseManager
aws management ManagedServices
aws management ManagementAndGovernance
aws management ManagementConsole
aws management OpsworksApps
aws management OpsworksDeployments
aws management OpsworksInstances
aws management OpsworksLayers
aws management OpsworksMonitoring
aws management OpsworksPermissions
aws management OpsworksResources
aws management OpsworksStack
aws management Opsworks
aws management OrganizationsAccount
aws management OrganizationsOrganizationalUnit
aws management Organizations
aws management PersonalHealthDashboard
aws management ServiceCatalog
aws management SystemsManagerAutomation
aws management SystemsManagerDocuments
aws management SystemsManagerInventory
aws management SystemsManagerMaintenanceWindows
aws management SystemsManagerOpscenter
aws management SystemsManagerParameterStore
aws management ParameterStore
aws management SystemsManagerPatchManager
aws management SystemsManagerRunCommand
aws management SystemsManagerStateManager
aws management SystemsManager
aws management SSM
aws management TrustedAdvisorChecklistCost
aws management TrustedAdvisorChecklistFaultTolerant
aws management TrustedAdvisorChecklistPerformance
aws management TrustedAdvisorChecklistSecurity
aws management TrustedAdvisorChecklist
aws management TrustedAdvisor
aws management WellArchitectedTool
aws media ElasticTranscoder
aws media ElementalConductor
aws media ElementalDelta
aws media ElementalLive
aws media ElementalMediaconnect
aws media ElementalMediaconvert
aws media ElementalMedialive
aws media ElementalMediapackage
aws media ElementalMediastore
aws media ElementalMediatailor
aws media ElementalServer
aws media KinesisVideoStreams
aws media MediaServices
aws migration ApplicationDiscoveryService
aws migration ADS
aws migration CloudendureMigration
aws migration CEM
aws migration DatabaseMigrationService
aws migration DMS
aws migration DatasyncAgent
aws migration Datasync
aws migration MigrationAndTransfer
aws migration MAT
aws migration MigrationHub
aws migration ServerMigrationService
aws migration SMS
aws migration SnowballEdge
aws migration Snowball
aws migration Snowmobile
aws migration TransferForSftp
aws ml ApacheMxnetOnAWS
aws ml AugmentedAi
aws ml Comprehend
aws ml DeepLearningAmis
aws ml DeepLearningContainers
aws ml DLC
aws ml Deepcomposer
aws ml Deeplens
aws ml Deepracer
aws ml ElasticInference
aws ml Forecast
aws ml FraudDetector
aws ml Kendra
aws ml Lex
aws ml MachineLearning
aws ml Personalize
aws ml Polly
aws ml RekognitionImage
aws ml RekognitionVideo
aws ml Rekognition
aws ml SagemakerGroundTruth
aws ml SagemakerModel
aws ml SagemakerNotebook
aws ml SagemakerTrainingJob
aws ml Sagemaker
aws ml TensorflowOnAWS
aws ml Textract
aws ml Transcribe
aws ml Translate
aws mobile Amplify
aws mobile APIGatewayEndpoint
aws mobile APIGateway
aws mobile Appsync
aws mobile DeviceFarm
aws mobile Mobile
aws mobile Pinpoint
aws network APIGatewayEndpoint
aws network APIGateway
aws network AppMesh
aws network ClientVpn
aws network CloudMap
aws network CloudFrontDownloadDistribution
aws network CloudFrontEdgeLocation
aws network CloudFrontStreamingDistribution
aws network CloudFront
aws network CF
aws network DirectConnect
aws network ElasticLoadBalancing
aws network ELB
aws network ElbApplicationLoadBalancer
aws network ALB
aws network ElbClassicLoadBalancer
aws network CLB
aws network ElbNetworkLoadBalancer
aws network NLB
aws network Endpoint
aws network GlobalAccelerator
aws network GAX
aws network InternetGateway
aws network Nacl
aws network NATGateway
aws network NetworkingAndContentDelivery
aws network PrivateSubnet
aws network Privatelink
aws network PublicSubnet
aws network Route53HostedZone
aws network Route53
aws network RouteTable
aws network SiteToSiteVpn
aws network TransitGateway
aws network VPCCustomerGateway
aws network VPCElasticNetworkAdapter
aws network VPCElasticNetworkInterface
aws network VPCFlowLogs
aws network VPCPeering
aws network VPCRouter
aws network VPCTrafficMirroring
aws network VPC
aws network VpnConnection
aws network VpnGateway
aws quantum Braket
aws quantum QuantumTechnologies
aws robotics RobomakerCloudExtensionRos
aws robotics RobomakerDevelopmentEnvironment
aws robotics RobomakerFleetManagement
aws robotics RobomakerSimulator
aws robotics Robomaker
aws robotics Robotics
aws satellite GroundStation
aws satellite Satellite
aws security AdConnector
aws security Artifact
aws security CertificateAuthority
aws security ACM
aws security CertificateManager
aws security CloudDirectory
aws security Cloudhsm
aws security CloudHSM
aws security Cognito
aws security Detective
aws security DS
aws security DirectoryService
aws security FMS
aws security FirewallManager
aws security Guardduty
aws security IdentityAndAccessManagementIamAccessAnalyzer
aws security IAMAccessAnalyzer
aws security IdentityAndAccessManagementIamAddOn
aws security IdentityAndAccessManagementIamAWSStsAlternate
aws security IAMAWSSts
aws security IdentityAndAccessManagementIamAWSSts
aws security IdentityAndAccessManagementIamDataEncryptionKey
aws security IdentityAndAccessManagementIamEncryptedData
aws security IdentityAndAccessManagementIamLongTermSecurityCredential
aws security IdentityAndAccessManagementIamMfaToken
aws security IAMPermissions
aws security IdentityAndAccessManagementIamPermissions
aws security IAMRole
aws security IdentityAndAccessManagementIamRole
aws security IdentityAndAccessManagementIamTemporarySecurityCredential
aws security IdentityAndAccessManagementIam
aws security IAM
aws security InspectorAgent
aws security Inspector
aws security KeyManagementService
aws security KMS
aws security Macie
aws security ManagedMicrosoftAd
aws security RAM
aws security ResourceAccessManager
aws security SecretsManager
aws security SecurityHubFinding
aws security SecurityHub
aws security SecurityIdentityAndCompliance
aws security ShieldAdvanced
aws security Shield
aws security SimpleAd
aws security SingleSignOn
aws security WAFFilteringRule
aws storage Backup
aws storage CDR
aws storage CloudendureDisasterRecovery
aws storage EFSInfrequentaccessPrimaryBg
aws storage EFSStandardPrimaryBg
aws storage ElasticBlockStoreEBSSnapshot
aws storage ElasticBlockStoreEBSVolume
aws storage EBS
aws storage ElasticBlockStoreEBS
aws storage ElasticFileSystemEFSFileSystem
aws storage EFS
aws storage ElasticFileSystemEFS
aws storage FsxForLustre
aws storage FsxForWindowsFileServer
aws storage Fsx
aws storage FSx
aws storage MultipleVolumesResource
aws storage S3GlacierArchive
aws storage S3GlacierVault
aws storage S3Glacier
aws storage SimpleStorageServiceS3BucketWithObjects
aws storage SimpleStorageServiceS3Bucket
aws storage SimpleStorageServiceS3Object
aws storage S3
aws storage SimpleStorageServiceS3
aws storage SnowFamilySnowball Export
aws storage SnowballEdge
aws storage Snowball
aws storage Snowmobile
aws storage StorageGatewayCachedVolume
aws storage StorageGatewayNonCachedVolume
aws storage StorageGatewayVirtualTapeLibrary
aws storage StorageGateway
aws storage Storage
azure analytics AnalysisServices
azure analytics DataExplorerClusters
azure analytics DataFactories
azure analytics DataLakeAnalytics
azure analytics DataLakeStoreGen1
azure analytics Databricks
azure analytics EventHubClusters
azure analytics impor tEventHubs
azure analytics Hdinsightclusters
azure analytics LogAnalyticsWorkspaces
azure analytics StreamAnalyticsJobs
azure analytics SynapseAnalytics
azure compute AppServices
azure compute AutomanagedVM
azure compute AvailabilitySets
azure compute BatchAccounts
azure compute CitrixVirtualDesktopsEssentials
azure compute CloudServicesClassic
azure compute CloudServices
azure compute CloudsimpleVirtualMachines
azure compute ContainerInstances
azure compute ContainerRegistries
azure compute ACR
azure compute DiskEncryptionSets
azure compute DiskSnapshots
azure compute Disks
azure compute FunctionApps
azure compute ImageDefinitions
azure compute ImageVersions
azure compute KubernetesServices
azure compute AKS
azure compute MeshApplications
azure compute OsImages
azure compute SAPHANAOnAzure
azure compute ServiceFabricClusters
azure compute SharedImageGalleries
azure compute SpringCloud
azure compute VMClassic
azure compute VMImages
azure compute VMLinux
azure compute VMScaleSet
azure compute VMSS
azure compute VMWindows
azure compute VM
azure compute Workspaces
azure database BlobStorage
azure database CacheForRedis
azure database CosmosDb
azure database DataExplorerClusters
azure database DataFactory
azure database DataLake
azure database DatabaseForMariadbServers
azure database DatabaseForMysqlServers
azure database DatabaseForPostgresqlServers
azure database ElasticDatabasePools
azure database ElasticJobAgents
azure database InstancePools
azure database ManagedDatabases
azure database SQLDatabases
azure database SQLDatawarehouse
azure database SQLManagedInstances
azure database SQLServerStretchDatabases
azure database SQLServers
azure database SQLVM
azure database SQL
azure database SsisLiftAndShiftIr
azure database SynapseAnalytics
azure database VirtualClusters
azure database VirtualDatacenter
azure devops azure.devops ApplicationInsights
azure devops Artifacts
azure devops Boards
azure devops Devops
azure devops DevtestLabs
azure devops LabServices
azure devops Pipelines
azure devops Repos
azure general Allresources
azure general Azurehome
azure general Developertools
azure general Helpsupport
azure general Information
azure general Managementgroups
azure general Marketplace
azure general Quickstartcenter
azure general Recent
azure general Reservations
azure general Resource
azure general Resourcegroups
azure general Servicehealth
azure general Shareddashboard
azure general Subscriptions
azure general Support
azure general Supportrequests
azure general Tag
azure general Tags
azure general Templates
azure general Twousericon
azure general Userhealthicon
azure general Usericon
azure general Userprivacy
azure general Userresource
azure general Whatsnew
azure identity AccessReview
azure identity ActiveDirectoryConnectHealth
azure identity ActiveDirectory
azure identity ADB2C
azure identity ADDomainServices
azure identity ADIdentityProtection
azure identity ADPrivilegedIdentityManagement
azure identity AppRegistrations
azure identity ConditionalAccess
azure identity EnterpriseApplications
azure identity Groups
azure identity IdentityGovernance
azure identity InformationProtection
azure identity ManagedIdentities
azure identity Users
azure integration APIForFhir
azure integration APIManagement
azure integration AppConfiguration
azure integration DataCatalog
azure integration EventGridDomains
azure integration EventGridSubscriptions
azure integration EventGridTopics
azure integration IntegrationAccounts
azure integration IntegrationServiceEnvironments
azure integration LogicAppsCustomConnector
azure integration LogicApps
azure integration PartnerTopic
azure integration SendgridAccounts
azure integration ServiceBusRelays
azure integration ServiceBus
azure integration ServiceCatalogManagedApplicationDefinitions
azure integration SoftwareAsAService
azure integration StorsimpleDeviceManagers
azure integration SystemTopic
azure iot DeviceProvisioningServices
azure iot DigitalTwins
azure iot IotCentralApplications
azure iot IotHubSecurity
azure iot IotHub
azure iot Maps
azure iot Sphere
azure iot TimeSeriesInsightsEnvironments
azure iot TimeSeriesInsightsEventsSources
azure iot Windows10IotCoreServices
azure migration DataBoxEdge
azure migration DataBox
azure migration DatabaseMigrationServices
azure migration MigrationProjects
azure migration RecoveryServicesVaults
azure ml BatchAI
azure ml BotServices
azure ml CognitiveServices
azure ml GenomicsAccounts
azure ml MachineLearningServiceWorkspaces
azure ml MachineLearningStudioWebServicePlans
azure ml MachineLearningStudioWebServices
azure ml MachineLearningStudioWorkspaces
azure mobile AppServiceMobile
azure mobile MobileEngagement
azure mobile NotificationHubs
azure network ApplicationGateway
azure network ApplicationSecurityGroups
azure network CDNProfiles
azure network Connections
azure network DDOSProtectionPlans
azure network DNSPrivateZones
azure network DNSZones
azure network ExpressrouteCircuits
azure network Firewall
azure network FrontDoors
azure network LoadBalancers
azure network LocalNetworkGateways
azure network NetworkInterfaces
azure network NetworkSecurityGroupsClassic
azure network NetworkWatcher
azure network OnPremisesDataGateways
azure network PublicIpAddresses
azure network ReservedIpAddressesClassic
azure network RouteFilters
azure network RouteTables
azure network ServiceEndpointPolicies
azure network Subnets
azure network TrafficManagerProfiles
azure network VirtualNetworkClassic
azure network VirtualNetworkGateways
azure network VirtualNetworks
azure network VirtualWans
azure security ApplicationSecurityGroups
azure security ConditionalAccess
azure security Defender
azure security ExtendedSecurityUpdates
azure security KeyVaults
azure security SecurityCenter
azure security Sentinel
azure storage ArchiveStorage
azure storage Azurefxtedgefiler
azure storage BlobStorage
azure storage DataBoxEdgeDataBoxGateway
azure storage DataBox
azure storage DataLakeStorage
azure storage GeneralStorage
azure storage NetappFiles
azure storage QueuesStorage
azure storage StorageAccountsClassic
azure storage StorageAccounts
azure storage StorageExplorer
azure storage StorageSyncServices
azure storage StorsimpleDataManagers
azure storage StorsimpleDeviceManagers
azure storage TableStorage
azure web APIConnections
azure web AppServiceCertificates
azure web AppServiceDomains
azure web AppServiceEnvironments
azure web AppServicePlans
azure web AppServices
azure web MediaServices
azure web NotificationHubNamespaces
azure web Search
azure web Signalr

'''

Diagram_Library = '''
from diagrams import Diagram
from diagrams import Cluster
from diagrams.gcp.analytics import BigQuery
from diagrams.gcp.analytics import Bigquery
from diagrams.gcp.analytics import Composer
from diagrams.gcp.analytics import DataCatalog
from diagrams.gcp.analytics import DataFusion
from diagrams.gcp.analytics import Dataflow
from diagrams.gcp.analytics import Datalab
from diagrams.gcp.analytics import Dataprep
from diagrams.gcp.analytics import Dataproc
from diagrams.gcp.analytics import Genomics
from diagrams.gcp.analytics import PubSub
from diagrams.gcp.analytics import Pubsub
from diagrams.gcp.api import APIGateway
from diagrams.gcp.api import Endpoints
from diagrams.gcp.compute import GAE
from diagrams.gcp.compute import AppEngine
from diagrams.gcp.compute import GCE
from diagrams.gcp.compute import ComputeEngine
from diagrams.gcp.compute import ContainerOptimizedOS
from diagrams.gcp.compute import GCF
from diagrams.gcp.compute import Functions
from diagrams.gcp.compute import GKEOnPrem
from diagrams.gcp.compute import GPU
from diagrams.gcp.compute import GKE
from diagrams.gcp.compute import KubernetesEngine
from diagrams.gcp.compute import Run
from diagrams.gcp.database import BigTable
from diagrams.gcp.database import Bigtable
from diagrams.gcp.database import Datastore
from diagrams.gcp.database import Firestore
from diagrams.gcp.database import Memorystore
from diagrams.gcp.database import Spanner
from diagrams.gcp.database import SQL
from diagrams.gcp.devtools import Build
from diagrams.gcp.devtools import CodeForIntellij
from diagrams.gcp.devtools import Code
from diagrams.gcp.devtools import GCR
from diagrams.gcp.devtools import ContainerRegistry
from diagrams.gcp.devtools import GradleAppEnginePlugin
from diagrams.gcp.devtools import IdePlugins
from diagrams.gcp.devtools import MavenAppEnginePlugin
from diagrams.gcp.devtools import Scheduler
from diagrams.gcp.devtools import SDK
from diagrams.gcp.devtools import SourceRepositories
from diagrams.gcp.devtools import Tasks
from diagrams.gcp.devtools import TestLab
from diagrams.gcp.devtools import ToolsForEclipse
from diagrams.gcp.devtools import ToolsForPowershell
from diagrams.gcp.devtools import ToolsForVisualStudio
from diagrams.gcp.iot import IotCore
from diagrams.gcp.migration import TransferAppliance
from diagrams.gcp.ml import AdvancedSolutionsLab
from diagrams.gcp.ml import AIHub
from diagrams.gcp.ml import AIPlatformDataLabelingService
from diagrams.gcp.ml import AIPlatform
from diagrams.gcp.ml import AutomlNaturalLanguage
from diagrams.gcp.ml import AutomlTables
from diagrams.gcp.ml import AutomlTranslation
from diagrams.gcp.ml import AutomlVideoIntelligence
from diagrams.gcp.ml import AutomlVision
from diagrams.gcp.ml import AutoML
from diagrams.gcp.ml import Automl
from diagrams.gcp.ml import DialogFlowEnterpriseEdition
from diagrams.gcp.ml import InferenceAPI
from diagrams.gcp.ml import JobsAPI
from diagrams.gcp.ml import NLAPI
from diagrams.gcp.ml import NaturalLanguageAPI
from diagrams.gcp.ml import RecommendationsAI
from diagrams.gcp.ml import SpeechToText
from diagrams.gcp.ml import SpeechToText
from diagrams.gcp.ml import TextToSpeech
from diagrams.gcp.ml import TextToSpeech
from diagrams.gcp.ml import TPU
from diagrams.gcp.ml import TranslationAPI
from diagrams.gcp.ml import VideoIntelligenceAPI
from diagrams.gcp.ml import VisionAPI
from diagrams.gcp.network import Armor
from diagrams.gcp.network import CDN
from diagrams.gcp.network import DedicatedInterconnect
from diagrams.gcp.network import DNS
from diagrams.gcp.network import ExternalIpAddresses
from diagrams.gcp.network import FirewallRules
from diagrams.gcp.network import LoadBalancing
from diagrams.gcp.network import NAT
from diagrams.gcp.network import Network
from diagrams.gcp.network import PartnerInterconnect
from diagrams.gcp.network import PremiumNetworkTier
from diagrams.gcp.network import Router
from diagrams.gcp.network import Routes
from diagrams.gcp.network import StandardNetworkTier
from diagrams.gcp.network import TrafficDirector
from diagrams.gcp.network import VPC
from diagrams.gcp.network import VirtualPrivateCloud
from diagrams.gcp.network import VPN
from diagrams.gcp.operations import Monitoring
from diagrams.gcp.security import Iam
from diagrams.gcp.security import IAP
from diagrams.gcp.security import KMS
from diagrams.gcp.security import KeyManagementService
from diagrams.gcp.security import ResourceManager
from diagrams.gcp.security import SCC
from diagrams.gcp.security import SecurityCommandCenter
from diagrams.gcp.security import SecurityScanner
from diagrams.gcp.storage import Filestore
from diagrams.gcp.storage import PersistentDisk
from diagrams.gcp.storage import Storage
from diagrams.gcp.storage import GCS
from diagrams.aws.analytics import Analytics
from diagrams.aws.analytics import Athena
from diagrams.aws.analytics import CloudsearchSearchDocuments
from diagrams.aws.analytics import Cloudsearch
from diagrams.aws.analytics import DataLakeResource
from diagrams.aws.analytics import DataPipeline
from diagrams.aws.analytics import ElasticsearchService
from diagrams.aws.analytics import ES
from diagrams.aws.analytics import EMRCluster
from diagrams.aws.analytics import EMREngineMaprM3
from diagrams.aws.analytics import EMREngineMaprM5
from diagrams.aws.analytics import EMREngineMaprM7
from diagrams.aws.analytics import EMREngine
from diagrams.aws.analytics import EMRHdfsCluster
from diagrams.aws.analytics import EMR
from diagrams.aws.analytics import GlueCrawlers
from diagrams.aws.analytics import GlueDataCatalog
from diagrams.aws.analytics import Glue
from diagrams.aws.analytics import KinesisDataAnalytics
from diagrams.aws.analytics import KinesisDataFirehose
from diagrams.aws.analytics import KinesisDataStreams
from diagrams.aws.analytics import KinesisVideoStreams
from diagrams.aws.analytics import Kinesis
from diagrams.aws.analytics import LakeFormation
from diagrams.aws.analytics import ManagedStreamingForKafka
from diagrams.aws.analytics import Quicksight
from diagrams.aws.analytics import RedshiftDenseComputeNode
from diagrams.aws.analytics import RedshiftDenseStorageNode
from diagrams.aws.analytics import Redshift
from diagrams.aws.ar import ArVr
from diagrams.aws.ar import Sumerian
from diagrams.aws.blockchain import BlockchainResource
from diagrams.aws.blockchain import Blockchain
from diagrams.aws.blockchain import ManagedBlockchain
from diagrams.aws.blockchain import QLDB
from diagrams.aws.blockchain import QuantumLedgerDatabaseQldb
from diagrams.aws.blockchain import QLDB
from diagrams.aws.business import AlexaForBusiness
from diagrams.aws.business import A4B
from diagrams.aws.business import BusinessApplications
from diagrams.aws.business import Chime
from diagrams.aws.business import Workmail
from diagrams.aws.compute import AppRunner
from diagrams.aws.compute import ApplicationAutoScaling
from diagrams.aws.compute import AutoScaling
from diagrams.aws.compute import Batch
from diagrams.aws.compute import ComputeOptimizer
from diagrams.aws.compute import Compute
from diagrams.aws.compute import EC2Ami
from diagrams.aws.compute import AMI
from diagrams.aws.compute import EC2AutoScaling
from diagrams.aws.compute import EC2ContainerRegistryImage
from diagrams.aws.compute import EC2ContainerRegistryRegistry
from diagrams.aws.compute import EC2ContainerRegistry
from diagrams.aws.compute import ECR
from diagrams.aws.compute import EC2ElasticIpAddress
from diagrams.aws.compute import EC2ImageBuilder
from diagrams.aws.compute import EC2Instance
from diagrams.aws.compute import EC2Instances
from diagrams.aws.compute import EC2Rescue
from diagrams.aws.compute import EC2SpotInstance
from diagrams.aws.compute import EC2
from diagrams.aws.compute import ElasticBeanstalkApplication
from diagrams.aws.compute import ElasticBeanstalkDeployment
from diagrams.aws.compute import ElasticBeanstalk
from diagrams.aws.compute import EB
from diagrams.aws.compute import ElasticContainerServiceContainer
from diagrams.aws.compute import ElasticContainerServiceService
from diagrams.aws.compute import ElasticContainerService
from diagrams.aws.compute import ECS
from diagrams.aws.compute import ElasticKubernetesService
from diagrams.aws.compute import EKS
from diagrams.aws.compute import Fargate
from diagrams.aws.compute import LambdaFunction
from diagrams.aws.compute import Lambda
from diagrams.aws.compute import Lightsail
from diagrams.aws.compute import LocalZones
from diagrams.aws.compute import Outposts
from diagrams.aws.compute import ServerlessApplicationRepository
from diagrams.aws.compute import SAR
from diagrams.aws.compute import ThinkboxDeadline
from diagrams.aws.compute import ThinkboxDraft
from diagrams.aws.compute import ThinkboxFrost
from diagrams.aws.compute import ThinkboxKrakatoa
from diagrams.aws.compute import ThinkboxSequoia
from diagrams.aws.compute import ThinkboxStoke
from diagrams.aws.compute import ThinkboxXmesh
from diagrams.aws.compute import VmwareCloudOnAWS
from diagrams.aws.compute import Wavelength
from diagrams.aws.cost import Budgets
from diagrams.aws.cost import CostAndUsageReport
from diagrams.aws.cost import CostExplorer
from diagrams.aws.cost import CostManagement
from diagrams.aws.cost import ReservedInstanceReporting
from diagrams.aws.cost import SavingsPlans
from diagrams.aws.database import AuroraInstance
from diagrams.aws.database import Aurora
from diagrams.aws.database import DatabaseMigrationServiceDatabaseMigrationWorkflow
from diagrams.aws.database import DatabaseMigrationService
from diagrams.aws.database import DMS
from diagrams.aws.database import Database
from diagrams.aws.database import DB
from diagrams.aws.database import DocumentdbMongodbCompatibility
from diagrams.aws.database import DocumentDB
from diagrams.aws.database import DynamodbAttribute
from diagrams.aws.database import DynamodbAttributes
from diagrams.aws.database import DynamodbDax
from diagrams.aws.database import DAX
from diagrams.aws.database import DynamodbGlobalSecondaryIndex
from diagrams.aws.database import DynamodbGSI
from diagrams.aws.database import DynamodbItem
from diagrams.aws.database import DynamodbItems
from diagrams.aws.database import DynamodbTable
from diagrams.aws.database import Dynamodb
from diagrams.aws.database import DDB
from diagrams.aws.database import ElasticacheCacheNode
from diagrams.aws.database import ElasticacheForMemcached
from diagrams.aws.database import ElasticacheForRedis
from diagrams.aws.database import Elasticache
from diagrams.aws.database import ElastiCache
from diagrams.aws.database import KeyspacesManagedApacheCassandraService
from diagrams.aws.database import Neptune
from diagrams.aws.database import QuantumLedgerDatabaseQldb
from diagrams.aws.database import QLDB
from diagrams.aws.database import RDSInstance
from diagrams.aws.database import RDSMariadbInstance
from diagrams.aws.database import RDSMysqlInstance
from diagrams.aws.database import RDSOnVmware
from diagrams.aws.database import RDSOracleInstance
from diagrams.aws.database import RDSPostgresqlInstance
from diagrams.aws.database import RDSSqlServerInstance
from diagrams.aws.database import RDS
from diagrams.aws.database import RedshiftDenseComputeNode
from diagrams.aws.database import RedshiftDenseStorageNode
from diagrams.aws.database import Redshift
from diagrams.aws.database import Timestream
from diagrams.aws.devtools import CloudDevelopmentKit
from diagrams.aws.devtools import Cloud9Resource
from diagrams.aws.devtools import Cloud9
from diagrams.aws.devtools import Codebuild
from diagrams.aws.devtools import Codecommit
from diagrams.aws.devtools import Codedeploy
from diagrams.aws.devtools import Codepipeline
from diagrams.aws.devtools import Codestar
from diagrams.aws.devtools import CommandLineInterface
from diagrams.aws.devtools import CLI
from diagrams.aws.devtools import DeveloperTools
from diagrams.aws.devtools import DevTools
from diagrams.aws.devtools import ToolsAndSdks
from diagrams.aws.devtools import XRay
from diagrams.aws.enablement import CustomerEnablement
from diagrams.aws.enablement import Iq
from diagrams.aws.enablement import ManagedServices
from diagrams.aws.enablement import ProfessionalServices
from diagrams.aws.enablement import Support
from diagrams.aws.enduser import Appstream20
from diagrams.aws.enduser import DesktopAndAppStreaming
from diagrams.aws.enduser import Workdocs
from diagrams.aws.enduser import Worklink
from diagrams.aws.enduser import Workspaces
from diagrams.aws.engagement import Connect
from diagrams.aws.engagement import CustomerEngagement
from diagrams.aws.engagement import Pinpoint
from diagrams.aws.engagement import SimpleEmailServiceSesEmail
from diagrams.aws.engagement import SimpleEmailServiceSes
from diagrams.aws.engagement import SES
from diagrams.aws.game import GameTech
from diagrams.aws.game import Gamelift
from diagrams.aws.general import Client
from diagrams.aws.general import Disk
from diagrams.aws.general import Forums
from diagrams.aws.general import General
from diagrams.aws.general import GenericDatabase
from diagrams.aws.general import GenericFirewall
from diagrams.aws.general import GenericOfficeBuilding
from diagrams.aws.general import OfficeBuilding
from diagrams.aws.general import GenericSamlToken
from diagrams.aws.general import GenericSDK
from diagrams.aws.general import InternetAlt1
from diagrams.aws.general import InternetAlt2
from diagrams.aws.general import InternetGateway
from diagrams.aws.general import Marketplace
from diagrams.aws.general import MobileClient
from diagrams.aws.general import Multimedia
from diagrams.aws.general import OfficeBuilding
from diagrams.aws.general import SamlToken
from diagrams.aws.general import SDK
from diagrams.aws.general import SslPadlock
from diagrams.aws.general import TapeStorage
from diagrams.aws.general import Toolkit
from diagrams.aws.general import TraditionalServer
from diagrams.aws.general import User
from diagrams.aws.general import Users
from diagrams.aws.integration import ApplicationIntegration
from diagrams.aws.integration import Appsync
from diagrams.aws.integration import ConsoleMobileApplication
from diagrams.aws.integration import EventResource
from diagrams.aws.integration import EventbridgeCustomEventBusResource
from diagrams.aws.integration import EventbridgeDefaultEventBusResource
from diagrams.aws.integration import EventbridgeSaasPartnerEventBusResource
from diagrams.aws.integration import Eventbridge
from diagrams.aws.integration import ExpressWorkflows
from diagrams.aws.integration import MQ
from diagrams.aws.integration import SimpleNotificationServiceSnsEmailNotification
from diagrams.aws.integration import SimpleNotificationServiceSnsHttpNotification
from diagrams.aws.integration import SimpleNotificationServiceSnsTopic
from diagrams.aws.integration import SimpleNotificationServiceSns
from diagrams.aws.integration import SNS
from diagrams.aws.integration import SimpleQueueServiceSqsMessage
from diagrams.aws.integration import SimpleQueueServiceSqsQueue
from diagrams.aws.integration import SimpleQueueServiceSqs
from diagrams.aws.integration import SQS
from diagrams.aws.integration import StepFunctions
from diagrams.aws.integration import SF
from diagrams.aws.iot import Freertos
from diagrams.aws.iot import FreeRTOS
from diagrams.aws.iot import InternetOfThings
from diagrams.aws.iot import Iot1Click
from diagrams.aws.iot import IotAction
from diagrams.aws.iot import IotActuator
from diagrams.aws.iot import IotAlexaEcho
from diagrams.aws.iot import IotAlexaEnabledDevice
from diagrams.aws.iot import IotAlexaSkill
from diagrams.aws.iot import IotAlexaVoiceService
from diagrams.aws.iot import IotAnalyticsChannel
from diagrams.aws.iot import IotAnalyticsDataSet
from diagrams.aws.iot import IotAnalyticsDataStore
from diagrams.aws.iot import IotAnalyticsNotebook
from diagrams.aws.iot import IotAnalyticsPipeline
from diagrams.aws.iot import IotAnalytics
from diagrams.aws.iot import IotBank
from diagrams.aws.iot import IotBicycle
from diagrams.aws.iot import IotButton
from diagrams.aws.iot import IotCamera
from diagrams.aws.iot import IotCar
from diagrams.aws.iot import IotCart
from diagrams.aws.iot import IotCertificate
from diagrams.aws.iot import IotCoffeePot
from diagrams.aws.iot import IotCore
from diagrams.aws.iot import IotDesiredState
from diagrams.aws.iot import IotDeviceDefender
from diagrams.aws.iot import IotDeviceGateway
from diagrams.aws.iot import IotDeviceManagement
from diagrams.aws.iot import IotDoorLock
from diagrams.aws.iot import IotEvents
from diagrams.aws.iot import IotFactory
from diagrams.aws.iot import IotFireTvStick
from diagrams.aws.iot import IotFireTv
from diagrams.aws.iot import IotGeneric
from diagrams.aws.iot import IotGreengrassConnector
from diagrams.aws.iot import IotGreengrass
from diagrams.aws.iot import IotHardwareBoard
from diagrams.aws.iot import IotBoard
from diagrams.aws.iot import IotHouse
from diagrams.aws.iot import IotHttp
from diagrams.aws.iot import IotHttp2
from diagrams.aws.iot import IotJobs
from diagrams.aws.iot import IotLambda
from diagrams.aws.iot import IotLightbulb
from diagrams.aws.iot import IotMedicalEmergency
from diagrams.aws.iot import IotMqtt
from diagrams.aws.iot import IotOverTheAirUpdate
from diagrams.aws.iot import IotPolicyEmergency
from diagrams.aws.iot import IotPolicy
from diagrams.aws.iot import IotReportedState
from diagrams.aws.iot import IotRule
from diagrams.aws.iot import IotSensor
from diagrams.aws.iot import IotServo
from diagrams.aws.iot import IotShadow
from diagrams.aws.iot import IotSimulator
from diagrams.aws.iot import IotSitewise
from diagrams.aws.iot import IotThermostat
from diagrams.aws.iot import IotThingsGraph
from diagrams.aws.iot import IotTopic
from diagrams.aws.iot import IotTravel
from diagrams.aws.iot import IotUtility
from diagrams.aws.iot import IotWindfarm
from diagrams.aws.management import AutoScaling
from diagrams.aws.management import Chatbot
from diagrams.aws.management import CloudformationChangeSet
from diagrams.aws.management import CloudformationStack
from diagrams.aws.management import CloudformationTemplate
from diagrams.aws.management import Cloudformation
from diagrams.aws.management import Cloudtrail
from diagrams.aws.management import CloudwatchAlarm
from diagrams.aws.management import CloudwatchEventEventBased
from diagrams.aws.management import CloudwatchEventTimeBased
from diagrams.aws.management import CloudwatchRule
from diagrams.aws.management import Cloudwatch
from diagrams.aws.management import Codeguru
from diagrams.aws.management import CommandLineInterface
from diagrams.aws.management import Config
from diagrams.aws.management import ControlTower
from diagrams.aws.management import LicenseManager
from diagrams.aws.management import ManagedServices
from diagrams.aws.management import ManagementAndGovernance
from diagrams.aws.management import ManagementConsole
from diagrams.aws.management import OpsworksApps
from diagrams.aws.management import OpsworksDeployments
from diagrams.aws.management import OpsworksInstances
from diagrams.aws.management import OpsworksLayers
from diagrams.aws.management import OpsworksMonitoring
from diagrams.aws.management import OpsworksPermissions
from diagrams.aws.management import OpsworksResources
from diagrams.aws.management import OpsworksStack
from diagrams.aws.management import Opsworks
from diagrams.aws.management import OrganizationsAccount
from diagrams.aws.management import OrganizationsOrganizationalUnit
from diagrams.aws.management import Organizations
from diagrams.aws.management import PersonalHealthDashboard
from diagrams.aws.management import ServiceCatalog
from diagrams.aws.management import SystemsManagerAutomation
from diagrams.aws.management import SystemsManagerDocuments
from diagrams.aws.management import SystemsManagerInventory
from diagrams.aws.management import SystemsManagerMaintenanceWindows
from diagrams.aws.management import SystemsManagerOpscenter
from diagrams.aws.management import SystemsManagerParameterStore
from diagrams.aws.management import ParameterStore
from diagrams.aws.management import SystemsManagerPatchManager
from diagrams.aws.management import SystemsManagerRunCommand
from diagrams.aws.management import SystemsManagerStateManager
from diagrams.aws.management import SystemsManager
from diagrams.aws.management import SSM
from diagrams.aws.management import TrustedAdvisorChecklistCost
from diagrams.aws.management import TrustedAdvisorChecklistFaultTolerant
from diagrams.aws.management import TrustedAdvisorChecklistPerformance
from diagrams.aws.management import TrustedAdvisorChecklistSecurity
from diagrams.aws.management import TrustedAdvisorChecklist
from diagrams.aws.management import TrustedAdvisor
from diagrams.aws.management import WellArchitectedTool
from diagrams.aws.media import ElasticTranscoder
from diagrams.aws.media import ElementalConductor
from diagrams.aws.media import ElementalDelta
from diagrams.aws.media import ElementalLive
from diagrams.aws.media import ElementalMediaconnect
from diagrams.aws.media import ElementalMediaconvert
from diagrams.aws.media import ElementalMedialive
from diagrams.aws.media import ElementalMediapackage
from diagrams.aws.media import ElementalMediastore
from diagrams.aws.media import ElementalMediatailor
from diagrams.aws.media import ElementalServer
from diagrams.aws.media import KinesisVideoStreams
from diagrams.aws.media import MediaServices
from diagrams.aws.migration import ApplicationDiscoveryService
from diagrams.aws.migration import ADS
from diagrams.aws.migration import CloudendureMigration
from diagrams.aws.migration import CEM
from diagrams.aws.migration import DatabaseMigrationService
from diagrams.aws.migration import DMS
from diagrams.aws.migration import DatasyncAgent
from diagrams.aws.migration import Datasync
from diagrams.aws.migration import MigrationAndTransfer
from diagrams.aws.migration import MAT
from diagrams.aws.migration import MigrationHub
from diagrams.aws.migration import ServerMigrationService
from diagrams.aws.migration import SMS
from diagrams.aws.migration import SnowballEdge
from diagrams.aws.migration import Snowball
from diagrams.aws.migration import Snowmobile
from diagrams.aws.migration import TransferForSftp
from diagrams.aws.ml import ApacheMxnetOnAWS
from diagrams.aws.ml import AugmentedAi
from diagrams.aws.ml import Comprehend
from diagrams.aws.ml import DeepLearningAmis
from diagrams.aws.ml import DeepLearningContainers
from diagrams.aws.ml import DLC
from diagrams.aws.ml import Deepcomposer
from diagrams.aws.ml import Deeplens
from diagrams.aws.ml import Deepracer
from diagrams.aws.ml import ElasticInference
from diagrams.aws.ml import Forecast
from diagrams.aws.ml import FraudDetector
from diagrams.aws.ml import Kendra
from diagrams.aws.ml import Lex
from diagrams.aws.ml import MachineLearning
from diagrams.aws.ml import Personalize
from diagrams.aws.ml import Polly
from diagrams.aws.ml import RekognitionImage
from diagrams.aws.ml import RekognitionVideo
from diagrams.aws.ml import Rekognition
from diagrams.aws.ml import SagemakerGroundTruth
from diagrams.aws.ml import SagemakerModel
from diagrams.aws.ml import SagemakerNotebook
from diagrams.aws.ml import SagemakerTrainingJob
from diagrams.aws.ml import Sagemaker
from diagrams.aws.ml import TensorflowOnAWS
from diagrams.aws.ml import Textract
from diagrams.aws.ml import Transcribe
from diagrams.aws.ml import Translate
from diagrams.aws.mobile import Amplify
from diagrams.aws.mobile import APIGatewayEndpoint
from diagrams.aws.mobile import APIGateway
from diagrams.aws.mobile import Appsync
from diagrams.aws.mobile import DeviceFarm
from diagrams.aws.mobile import Mobile
from diagrams.aws.mobile import Pinpoint
from diagrams.aws.network import APIGatewayEndpoint
from diagrams.aws.network import APIGateway
from diagrams.aws.network import AppMesh
from diagrams.aws.network import ClientVpn
from diagrams.aws.network import CloudMap
from diagrams.aws.network import CloudFrontDownloadDistribution
from diagrams.aws.network import CloudFrontEdgeLocation
from diagrams.aws.network import CloudFrontStreamingDistribution
from diagrams.aws.network import CloudFront
from diagrams.aws.network import CF
from diagrams.aws.network import DirectConnect
from diagrams.aws.network import ElasticLoadBalancing
from diagrams.aws.network import ELB
from diagrams.aws.network import ElbApplicationLoadBalancer
from diagrams.aws.network import ALB
from diagrams.aws.network import ElbClassicLoadBalancer
from diagrams.aws.network import CLB
from diagrams.aws.network import ElbNetworkLoadBalancer
from diagrams.aws.network import NLB
from diagrams.aws.network import Endpoint
from diagrams.aws.network import GlobalAccelerator
from diagrams.aws.network import GAX
from diagrams.aws.network import InternetGateway
from diagrams.aws.network import Nacl
from diagrams.aws.network import NATGateway
from diagrams.aws.network import NetworkingAndContentDelivery
from diagrams.aws.network import PrivateSubnet
from diagrams.aws.network import Privatelink
from diagrams.aws.network import PublicSubnet
from diagrams.aws.network import Route53HostedZone
from diagrams.aws.network import Route53
from diagrams.aws.network import RouteTable
from diagrams.aws.network import SiteToSiteVpn
from diagrams.aws.network import TransitGateway
from diagrams.aws.network import VPCCustomerGateway
from diagrams.aws.network import VPCElasticNetworkAdapter
from diagrams.aws.network import VPCElasticNetworkInterface
from diagrams.aws.network import VPCFlowLogs
from diagrams.aws.network import VPCPeering
from diagrams.aws.network import VPCRouter
from diagrams.aws.network import VPCTrafficMirroring
from diagrams.aws.network import VPC
from diagrams.aws.network import VpnConnection
from diagrams.aws.network import VpnGateway
from diagrams.aws.quantum import Braket
from diagrams.aws.quantum import QuantumTechnologies
from diagrams.aws.robotics import RobomakerCloudExtensionRos
from diagrams.aws.robotics import RobomakerDevelopmentEnvironment
from diagrams.aws.robotics import RobomakerFleetManagement
from diagrams.aws.robotics import RobomakerSimulator
from diagrams.aws.robotics import Robomaker
from diagrams.aws.robotics import Robotics
from diagrams.aws.satellite import GroundStation
from diagrams.aws.satellite import Satellite
from diagrams.aws.security import AdConnector
from diagrams.aws.security import Artifact
from diagrams.aws.security import CertificateAuthority
from diagrams.aws.security import CertificateManager
from diagrams.aws.security import ACM
from diagrams.aws.security import CloudDirectory
from diagrams.aws.security import Cloudhsm
from diagrams.aws.security import CloudHSM
from diagrams.aws.security import Cognito
from diagrams.aws.security import Detective
from diagrams.aws.security import DirectoryService
from diagrams.aws.security import DS
from diagrams.aws.security import FirewallManager
from diagrams.aws.security import FMS
from diagrams.aws.security import Guardduty
from diagrams.aws.security import IdentityAndAccessManagementIamAccessAnalyzer
from diagrams.aws.security import IAMAccessAnalyzer
from diagrams.aws.security import IdentityAndAccessManagementIamAddOn
from diagrams.aws.security import IdentityAndAccessManagementIamAWSStsAlternate
from diagrams.aws.security import IdentityAndAccessManagementIamAWSSts
from diagrams.aws.security import IAMAWSSts
from diagrams.aws.security import IdentityAndAccessManagementIamDataEncryptionKey
from diagrams.aws.security import IdentityAndAccessManagementIamEncryptedData
from diagrams.aws.security import IdentityAndAccessManagementIamLongTermSecurityCredential
from diagrams.aws.security import IdentityAndAccessManagementIamMfaToken
from diagrams.aws.security import IdentityAndAccessManagementIamPermissions
from diagrams.aws.security import IAMPermissions
from diagrams.aws.security import IdentityAndAccessManagementIamRole
from diagrams.aws.security import IAMRole
from diagrams.aws.security import IdentityAndAccessManagementIamTemporarySecurityCredential
from diagrams.aws.security import IdentityAndAccessManagementIam
from diagrams.aws.security import IAM
from diagrams.aws.security import InspectorAgent
from diagrams.aws.security import Inspector
from diagrams.aws.security import KeyManagementService
from diagrams.aws.security import KMS
from diagrams.aws.security import Macie
from diagrams.aws.security import ManagedMicrosoftAd
from diagrams.aws.security import ResourceAccessManager
from diagrams.aws.security import RAM
from diagrams.aws.security import SecretsManager
from diagrams.aws.security import SecurityHubFinding
from diagrams.aws.security import SecurityHub
from diagrams.aws.security import SecurityIdentityAndCompliance
from diagrams.aws.security import ShieldAdvanced
from diagrams.aws.security import Shield
from diagrams.aws.security import SimpleAd
from diagrams.aws.security import SingleSignOn
from diagrams.aws.security import WAFFilteringRule
from diagrams.aws.storage import Backup
from diagrams.aws.storage import CDR
from diagrams.aws.storage import CloudendureDisasterRecovery
from diagrams.aws.storage import EFSInfrequentaccessPrimaryBg
from diagrams.aws.storage import EFSStandardPrimaryBg
from diagrams.aws.storage import ElasticBlockStoreEBSSnapshot
from diagrams.aws.storage import ElasticBlockStoreEBSVolume
from diagrams.aws.storage import ElasticBlockStoreEBS, EBS
from diagrams.aws.storage import ElasticFileSystemEFSFileSystem
from diagrams.aws.storage import EFS
from diagrams.aws.storage import ElasticFileSystemEFS
from diagrams.aws.storage import FsxForLustre
from diagrams.aws.storage import FsxForWindowsFileServer
from diagrams.aws.storage import FSx
from diagrams.aws.storage import Fsx
from diagrams.aws.storage import MultipleVolumesResource
from diagrams.aws.storage import S3GlacierArchive
from diagrams.aws.storage import S3GlacierVault
from diagrams.aws.storage import S3Glacier
from diagrams.aws.storage import SimpleStorageServiceS3BucketWithObjects
from diagrams.aws.storage import SimpleStorageServiceS3Bucket
from diagrams.aws.storage import SimpleStorageServiceS3Object
from diagrams.aws.storage import S3
from diagrams.aws.storage import SimpleStorageServiceS3
from diagrams.aws.storage import SnowFamilySnowballImportExport
from diagrams.aws.storage import SnowballEdge
from diagrams.aws.storage import Snowball
from diagrams.aws.storage import Snowmobile
from diagrams.aws.storage import StorageGatewayCachedVolume
from diagrams.aws.storage import StorageGatewayNonCachedVolume
from diagrams.aws.storage import StorageGatewayVirtualTapeLibrary
from diagrams.aws.storage import StorageGateway
from diagrams.aws.storage import Storage
from diagrams.azure.analytics import AnalysisServices
from diagrams.azure.analytics import DataExplorerClusters
from diagrams.azure.analytics import DataFactories
from diagrams.azure.analytics import DataLakeAnalytics
from diagrams.azure.analytics import DataLakeStoreGen1
from diagrams.azure.analytics import Databricks
from diagrams.azure.analytics import EventHubClusters
from diagrams.azure.analytics import EventHubs
from diagrams.azure.analytics import Hdinsightclusters
from diagrams.azure.analytics import LogAnalyticsWorkspaces
from diagrams.azure.analytics import StreamAnalyticsJobs
from diagrams.azure.analytics import SynapseAnalytics
from diagrams.azure.compute import AppServices
from diagrams.azure.compute import AutomanagedVM
from diagrams.azure.compute import AvailabilitySets
from diagrams.azure.compute import BatchAccounts
from diagrams.azure.compute import CitrixVirtualDesktopsEssentials
from diagrams.azure.compute import CloudServicesClassic
from diagrams.azure.compute import CloudServices
from diagrams.azure.compute import CloudsimpleVirtualMachines
from diagrams.azure.compute import ContainerInstances
from diagrams.azure.compute import ACR
from diagrams.azure.compute import ContainerRegistries
from diagrams.azure.compute import DiskEncryptionSets
from diagrams.azure.compute import DiskSnapshots
from diagrams.azure.compute import Disks
from diagrams.azure.compute import FunctionApps
from diagrams.azure.compute import ImageDefinitions
from diagrams.azure.compute import ImageVersions
from diagrams.azure.compute import AKS
from diagrams.azure.compute import KubernetesServices
from diagrams.azure.compute import MeshApplications
from diagrams.azure.compute import OsImages
from diagrams.azure.compute import SAPHANAOnAzure
from diagrams.azure.compute import ServiceFabricClusters
from diagrams.azure.compute import SharedImageGalleries
from diagrams.azure.compute import SpringCloud
from diagrams.azure.compute import VMClassic
from diagrams.azure.compute import VMImages
from diagrams.azure.compute import VMLinux
from diagrams.azure.compute import VMSS
from diagrams.azure.compute import VMScaleSet
from diagrams.azure.compute import VMWindows
from diagrams.azure.compute import VM
from diagrams.azure.compute import Workspaces
from diagrams.azure.database import BlobStorage
from diagrams.azure.database import CacheForRedis
from diagrams.azure.database import CosmosDb
from diagrams.azure.database import DataExplorerClusters
from diagrams.azure.database import DataFactory
from diagrams.azure.database import DataLake
from diagrams.azure.database import DatabaseForMariadbServers
from diagrams.azure.database import DatabaseForMysqlServers
from diagrams.azure.database import DatabaseForPostgresqlServers
from diagrams.azure.database import ElasticDatabasePools
from diagrams.azure.database import ElasticJobAgents
from diagrams.azure.database import InstancePools
from diagrams.azure.database import ManagedDatabases
from diagrams.azure.database import SQLDatabases
from diagrams.azure.database import SQLDatawarehouse
from diagrams.azure.database import SQLManagedInstances
from diagrams.azure.database import SQLServerStretchDatabases
from diagrams.azure.database import SQLServers
from diagrams.azure.database import SQLVM
from diagrams.azure.database import SQL
from diagrams.azure.database import SsisLiftAndShiftIr
from diagrams.azure.database import SynapseAnalytics
from diagrams.azure.database import VirtualClusters
from diagrams.azure.database import VirtualDatacenter
from diagrams.azure.devops import ApplicationInsights
from diagrams.azure.devops import Artifacts
from diagrams.azure.devops import Boards
from diagrams.azure.devops import Devops
from diagrams.azure.devops import DevtestLabs
from diagrams.azure.devops import LabServices
from diagrams.azure.devops import Pipelines
from diagrams.azure.devops import Repos
from diagrams.azure.general import Allresources
from diagrams.azure.general import Azurehome
from diagrams.azure.general import Developertools
from diagrams.azure.general import Helpsupport
from diagrams.azure.general import Information
from diagrams.azure.general import Managementgroups
from diagrams.azure.general import Marketplace
from diagrams.azure.general import Quickstartcenter
from diagrams.azure.general import Recent
from diagrams.azure.general import Reservations
from diagrams.azure.general import Resource
from diagrams.azure.general import Resourcegroups
from diagrams.azure.general import Servicehealth
from diagrams.azure.general import Shareddashboard
from diagrams.azure.general import Subscriptions
from diagrams.azure.general import Support
from diagrams.azure.general import Supportrequests
from diagrams.azure.general import Tag
from diagrams.azure.general import Tags
from diagrams.azure.general import Templates
from diagrams.azure.general import Twousericon
from diagrams.azure.general import Userhealthicon
from diagrams.azure.general import Usericon
from diagrams.azure.general import Userprivacy
from diagrams.azure.general import Userresource
from diagrams.azure.general import Whatsnew
from diagrams.azure.identity import AccessReview
from diagrams.azure.identity import ActiveDirectoryConnectHealth
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.identity import ADB2C
from diagrams.azure.identity import ADDomainServices
from diagrams.azure.identity import ADIdentityProtection
from diagrams.azure.identity import ADPrivilegedIdentityManagement
from diagrams.azure.identity import AppRegistrations
from diagrams.azure.identity import ConditionalAccess
from diagrams.azure.identity import EnterpriseApplications
from diagrams.azure.identity import Groups
from diagrams.azure.identity import IdentityGovernance
from diagrams.azure.identity import InformationProtection
from diagrams.azure.identity import ManagedIdentities
from diagrams.azure.identity import Users
from diagrams.azure.integration import APIForFhir
from diagrams.azure.integration import APIManagement
from diagrams.azure.integration import AppConfiguration
from diagrams.azure.integration import DataCatalog
from diagrams.azure.integration import EventGridDomains
from diagrams.azure.integration import EventGridSubscriptions
from diagrams.azure.integration import EventGridTopics
from diagrams.azure.integration import IntegrationAccounts
from diagrams.azure.integration import IntegrationServiceEnvironments
from diagrams.azure.integration import LogicAppsCustomConnector
from diagrams.azure.integration import LogicApps
from diagrams.azure.integration import PartnerTopic
from diagrams.azure.integration import SendgridAccounts
from diagrams.azure.integration import ServiceBusRelays
from diagrams.azure.integration import ServiceBus
from diagrams.azure.integration import ServiceCatalogManagedApplicationDefinitions
from diagrams.azure.integration import SoftwareAsAService
from diagrams.azure.integration import StorsimpleDeviceManagers
from diagrams.azure.integration import SystemTopic
from diagrams.azure.iot import DeviceProvisioningServices
from diagrams.azure.iot import DigitalTwins
from diagrams.azure.iot import IotCentralApplications
from diagrams.azure.iot import IotHubSecurity
from diagrams.azure.iot import IotHub
from diagrams.azure.iot import Maps
from diagrams.azure.iot import Sphere
from diagrams.azure.iot import TimeSeriesInsightsEnvironments
from diagrams.azure.iot import TimeSeriesInsightsEventsSources
from diagrams.azure.iot import Windows10IotCoreServices
from diagrams.azure.migration import DataBoxEdge
from diagrams.azure.migration import DataBox
from diagrams.azure.migration import DatabaseMigrationServices
from diagrams.azure.migration import MigrationProjects
from diagrams.azure.migration import RecoveryServicesVaults
from diagrams.azure.ml import BatchAI
from diagrams.azure.ml import BotServices
from diagrams.azure.ml import CognitiveServices
from diagrams.azure.ml import GenomicsAccounts
from diagrams.azure.ml import MachineLearningServiceWorkspaces
from diagrams.azure.ml import MachineLearningStudioWebServicePlans
from diagrams.azure.ml import MachineLearningStudioWebServices
from diagrams.azure.ml import MachineLearningStudioWorkspaces
from diagrams.azure.mobile import AppServiceMobile
from diagrams.azure.mobile import MobileEngagement
from diagrams.azure.mobile import NotificationHubs
from diagrams.azure.network import ApplicationGateway
from diagrams.azure.network import ApplicationSecurityGroups
from diagrams.azure.network import CDNProfiles
from diagrams.azure.network import Connections
from diagrams.azure.network import DDOSProtectionPlans
from diagrams.azure.network import DNSPrivateZones
from diagrams.azure.network import DNSZones
from diagrams.azure.network import ExpressrouteCircuits
from diagrams.azure.network import Firewall
from diagrams.azure.network import FrontDoors
from diagrams.azure.network import LoadBalancers
from diagrams.azure.network import LocalNetworkGateways
from diagrams.azure.network import NetworkInterfaces
from diagrams.azure.network import NetworkSecurityGroupsClassic
from diagrams.azure.network import NetworkWatcher
from diagrams.azure.network import OnPremisesDataGateways
from diagrams.azure.network import PublicIpAddresses
from diagrams.azure.network import ReservedIpAddressesClassic
from diagrams.azure.network import RouteFilters
from diagrams.azure.network import RouteTables
from diagrams.azure.network import ServiceEndpointPolicies
from diagrams.azure.network import Subnets
from diagrams.azure.network import TrafficManagerProfiles
from diagrams.azure.network import VirtualNetworkClassic
from diagrams.azure.network import VirtualNetworkGateways
from diagrams.azure.network import VirtualNetworks
from diagrams.azure.network import VirtualWans
from diagrams.azure.security import ApplicationSecurityGroups
from diagrams.azure.security import ConditionalAccess
from diagrams.azure.security import Defender
from diagrams.azure.security import ExtendedSecurityUpdates
from diagrams.azure.security import KeyVaults
from diagrams.azure.security import SecurityCenter
from diagrams.azure.security import Sentinel
from diagrams.azure.storage import ArchiveStorage
from diagrams.azure.storage import Azurefxtedgefiler
from diagrams.azure.storage import BlobStorage
from diagrams.azure.storage import DataBoxEdgeDataBoxGateway
from diagrams.azure.storage import DataBox
from diagrams.azure.storage import DataLakeStorage
from diagrams.azure.storage import GeneralStorage
from diagrams.azure.storage import NetappFiles
from diagrams.azure.storage import QueuesStorage
from diagrams.azure.storage import StorageAccountsClassic
from diagrams.azure.storage import StorageAccounts
from diagrams.azure.storage import StorageExplorer
from diagrams.azure.storage import StorageSyncServices
from diagrams.azure.storage import StorsimpleDataManagers
from diagrams.azure.storage import StorsimpleDeviceManagers
from diagrams.azure.storage import TableStorage
from diagrams.azure.web import APIConnections
from diagrams.azure.web import AppServiceCertificates
from diagrams.azure.web import AppServiceDomains
from diagrams.azure.web import AppServiceEnvironments
from diagrams.azure.web import AppServicePlans
from diagrams.azure.web import AppServices
from diagrams.azure.web import MediaServices
from diagrams.azure.web import NotificationHubNamespaces
from diagrams.azure.web import Search
from diagrams.azure.web import Signalr
'''

Instructions = f"""You are an expert AI assistant designed to generate components, data flow, and node class of the components in a specific format to assist in building an architecture
diagram based on problem statements. Provide solutions using AWS, GCP, Azure cloud technologies.

Please follow these formats:

1.  Components:
    Each step should clearly identify the two interacting components of the IT product or service for creating architecture diagram, along with the reason and purpose of their connection.
    Use descriptive language to explain the role of each component and how it interacts with others.
    Clearly indicate the direction of data flow between components.
2. Identify Nodes and Resource_type for the required components:
    Strictly take Nodes, Resource_type and cloud provider from {Diagram_Node} only for the components which are required.
    For each required component, provide the following information:
   Cloud_provider: (e.g., AWS, GCP, Azure)
   Resource_type: (as identified in the given data)
   Node: (as identified in the given data)
3. Data Flow:
   Describe how components will interact with each other in the data flow, and illustrate the end-to-end data flow.

"""

node_ins = f"""You're expert in developing python code using diagrams library for generating an architecture diagram for various cloud providers like AWS, GCP, Azure.
You'll receive components and data flow for creating an architecture diagram.
Your Task:
You are a python chatbot.You have to provide a python code using diagrams library to create an Architecture Digram for IT solution.
Strictly Import all the packages require to generate code should be taking from {Diagram_Library} only.
output:
Your final output should only the python code, do not answer anything else.
"""

INSTRUCTIONS_GRAPHVIZ = """Hello, you are an AI assistant tasked with generating components and their connections of flow diagrams based on problem statements.
You should provide solutions using AWS,GCP,AZURE cloud technologies or general IT solutions. Your output should follow this format:
Numbered steps
1.Each step should clearly identify the two interacting components of the IT product or service, along with the reason and purpose of their connection.
2.Use descriptive language to explain the role of each component and how it interacts with others.
3.Clearly indicate the direction of data flow between components.
4.For horizontal flow diagrams, draw the components from left to right.

Here are few examples:
Example 1.Create an architecture diagram for Three-tier web application.
Solution:
A three-tier web application architecture consists of three main components: the presentation layer, the application layer, and the data layer. Each layer has its own specific role and interacts with the other layers to provide a complete web application.
1. Presentation Layer:
   - User Interface (UI): This component is responsible for presenting the web application to the user and handling user interactions.
   - Web Server: The web server receives HTTP requests from the user's browser and forwards them to the application layer. It also serves static content, such as HTML, CSS, and JavaScript files, to the user's browser.
   - Load Balancer: The load balancer distributes incoming requests across multiple web servers to ensure scalability and high availability.
2. Application Layer:
   - Application Server: This component hosts the business logic of the web application. It processes requests received from the web server, interacts with the data layer, and generates dynamic content to be sent back to the user.
   - API Gateway: The API gateway acts as a single entry point for all API requests. It handles authentication, authorization, and request routing to the appropriate application server.
   - Caching Layer: The caching layer stores frequently accessed data to improve performance and reduce the load on the application servers. It can be implemented using technologies like Redis or Memcached.
3. Data Layer:
   - Database Server: This component stores and manages the web application's data. It can be a relational database (e.g., MySQL, PostgreSQL) or a NoSQL database (e.g., MongoDB, DynamoDB).
   - File Storage: The file storage component is used to store and retrieve files uploaded by users, such as images or documents. It can be implemented using services like Amazon S3 or Google Cloud Storage.
Data flow:
- User requests are sent from the browser to the web server through HTTP.
- The web server forwards the requests to the application server(s) through the load balancer.
- The application server processes the requests, interacts with the database server and caching layer if necessary, and generates dynamic content.
- The dynamic content is sent back to the user's browser through the web server.
- The application server also interacts with the file storage component when handling file uploads or retrievals.

Example 2.Create an architecture diagram for Azure Batch for parallel processing
Solution:
Here is an architecture diagram for Azure Batch for parallel processing:
1. User Interface:
   - Web Browser or Application: This is the user-facing component that interacts with the Azure Batch service.
2. Azure Batch Service:
   - Batch Account: This component provides the management and orchestration of parallel processing workloads.
   - Batch Pools: A pool of virtual machines (VMs) that are used to execute the parallel processing tasks. The pool can be dynamically scaled based on the workload demand.
   - Batch Jobs: Represents a collection of tasks that need to be processed in parallel. It defines the input data, processing logic, and output requirements.
   - Batch Tasks: Represents an individual unit of work within a job. It can be a script, executable, or Docker container that performs a specific processing task.
3. Azure Storage:
   - Blob Storage: Stores input data, output data, and application binaries required for processing.
   - File Storage: Provides shared file storage for the parallel processing tasks.
4. Azure Virtual Machine Scale Sets:
   - Virtual Machine Scale Sets: This component automatically scales the number of VM instances based on the workload demand. It ensures that there are enough resources available to process the tasks in parallel.
5. Azure Batch Task Dependencies:
   - Task Dependencies: Allows defining dependencies between tasks. It ensures that certain tasks are executed only after their dependent tasks have completed successfully.
6. Azure Batch Job Manager:
   - Job Manager: Monitors the progress of the job, manages task execution, and handles task failures or retries.
7. Azure Batch Task Output:
   - Task Output: The processed data or results generated by each task are stored in Azure Storage for further analysis or retrieval.
Data Flow:
- The user submits a job request through the user interface.
- The Batch Account receives the job request and creates a job with the specified parameters.
- The input data and application binaries are stored in Azure Storage.
- The Batch Account creates a pool of VM instances based on the job requirements.
- The job manager distributes the tasks across the VM instances in the pool.
- Each VM instance executes the assigned tasks in parallel.
- The processed data or results are stored in Azure Storage.
- The job manager monitors the progress of the job and handles any failures or retries.
- Once all tasks are completed, the job manager notifies the user or triggers further actions based on the job output.
Please note that this is a high-level architecture diagram, and the specific components and configurations may vary depending on the requirements of the Azure Batch application for parallel processing.

Example 3.Create an architecture diagram for Serverless architecture of AWS cloud
Solution:
Here is an architecture diagram for a serverless application in AWS cloud:
1. User Interface:
   - Web Browser or Mobile App: This is the user-facing component that interacts with the serverless application.
2. Amazon API Gateway:
   - API Gateway: Acts as a single entry point for all API requests. It handles authentication, authorization, and request routing to the appropriate serverless functions.
3. AWS Lambda Functions:
   - Lambda Functions: This component hosts the business logic of the application. It consists of individual functions that are triggered by events or API requests.
4. Event Sources:
   - AWS S3: Triggers a Lambda function when a file is uploaded or modified.
   - AWS DynamoDB: Triggers a Lambda function when a new record is inserted or updated.
   - AWS SNS: Triggers a Lambda function when a new message is published to a topic.
   - AWS CloudWatch Events: Triggers a Lambda function at a specific time or interval.
5. AWS Serverless Databases and Storage:
   - Amazon DynamoDB: A serverless NoSQL database that can be used to store and retrieve data.
   - Amazon S3: Serverless object storage service that can be used to store files and other unstructured data.
6. AWS Cognito:
   - Cognito: Handles user authentication and authorization. It provides secure access to the serverless application.
7. AWS Step Functions:
   - Step Functions: This service allows you to coordinate multiple Lambda functions as a workflow. It provides visual representation and control flow for complex serverless applications.
8. AWS EventBridge:
   - EventBridge: This service enables you to route events between different AWS services and Lambda functions. It acts as a central event bus for your serverless architecture.
9. AWS CloudWatch:
   - CloudWatch: Monitors and logs the performance of your serverless application. It provides metrics, logs, and alarms for monitoring and troubleshooting.
10. AWS SNS:
    - SNS: Sends notifications to subscribed endpoints or Lambda functions. It can be used to trigger actions based on specific events.
Data Flow:
- User requests are sent from the browser or mobile app to the API Gateway.
- The API Gateway routes the requests to the appropriate Lambda function.
- The Lambda function is triggered by an event source or an API request.
- The function processes the request, interacts with the serverless database or storage, and performs the necessary business logic.
- The function can also interact with other AWS services or external services if required.
- The response is sent back to the API Gateway, which then returns the response to the user.
Please note that this is a high-level architecture diagram, and the specific services and components used may vary depending on the requirements of the serverless application in AWS cloud.

"""

node_ins_graphviz=""" You'll receive an IT solution with components and their connection, and your task is to construct a graph using the DOT language—a plain text graph description format.
 Here's the process for defining a fundamental graph using DOT language:

Define the Graph:

1.Define the graph type, either "digraph" (directed graph) or "graph" (undirected graph).

Here's a simple example of a directed graph in DOT language:

"digraph MyGraph {
    A -> B;
    A -> C;
    B -> C;
    C -> D;
}"

In this example, we've defined a directed graph with nodes A, B, C, and D, and directed edges between them.

Here are some key components of the DOT language:

digraph: Indicates that we are creating a directed graph. If you want an undirected graph, use graph instead.
MyGraph: This is an name for your graph. You can choose any name you like.
The lines that follow define the edges between nodes. In the example, we have four edges:

A -> B: A points to B
A -> C: A points to C
B -> C: B points to C
C -> D: C points to D

Your Task:
You will be creating a graph for the given IT solution, where each component will be a single node and directed edges between
them should denote the dataflow between the nodes. Your final output format should only contain the graph written in DOT
language, do not answer anything else, just the graph written in DOT language.Place each component on the diagram in its designated role.
Ensure that components are positioned logically and intuitively.
"""


def get_response(instructions, previous_questions_and_answers, new_question):  #to get component and data flow
    """Get a response from ChatCompletion

    Args:
        instructions: The instructions for the chat bot - this determines how it will behave
        previous_questions_and_answers: Chat history
        new_question: The new question to ask the bot

    Returns:
        The response text
    """

    # build the messages
    messages = [
        { "role": "system", "content": instructions },
    ]
    # add the previous questions and answers
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question
    messages.append({ "role": "user", "content": new_question })

    completion = openai.ChatCompletion.create(
       engine="gpt-4-32k",
        messages=messages,
        temperature=0.7,
        top_p=0.95
    )
    return completion.choices[0].message.content

def get_nodes(instructions, previous_questions_and_answers, new_question):  # to get the code
    """Get a response from ChatCompletion

    Args:
        instructions: The instructions for the chat bot - this determines how it will behave
        previous_questions_and_answers: Chat history
        new_question: The new question to ask the bot

    Returns:
        The response text
    """
    # build the messages
    messages = [
        { "role": "system", "content": instructions },
    ]
    # add the previous questions and answers
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question
    messages.append({ "role": "user", "content": new_question })

    completion = openai.ChatCompletion.create(
        engine="gpt-4-32k",
        messages=messages,
        temperature=0.7,
        top_p=0.95,
    )
    return completion.choices[0].message.content

def save_prompts(prompts, filename):
# Read existing prompts (if any)
    existing_prompts = []
    if os.path.exists(filename):
        with open(filename, "r") as file:
            existing_prompts = file.readlines()

    # Combine new and existing prompts (deduplication optional)
    all_prompts = list(existing_prompts + prompts)

    # Write all prompts back to the file
    with open(filename, "w") as file:
        for prompt in all_prompts:
            file.write(prompt.strip() + "\n")

    with st.sidebar:

        for prompt in reversed(all_prompts):
            st.text(prompt)

def extract_code(cell_output):
    """
    Extracts the Python code for generating an architecture diagram from the cell output.

    Args:
        cell_output: The string containing the cell output.

    Returns:
        str: The extracted Python code or None if no code is found.
    """
    # Regex pattern to extract Python code blocks
    code_pattern = r"`python\n(.*?)`"

    # Find the first code block
    code_match = re.findall(code_pattern, cell_output, re.DOTALL)

    # Extract and return the code
    return code_match[0] if code_match else None




def get_latest_image(folder_path):
    images = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not images:
        return None
    latest_image = max(images, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
    return latest_image



def handle_download_button(img_bytes, image_path, placeholder):
    # Download the image
    st.markdown(f"[Download Image](data:application/octet-stream;base64,{base64.b64encode(img_bytes.getvalue()).decode()})", unsafe_allow_html=True)
    # Display the image again after the download button is clicked
    placeholder.image(Image.open(image_path), caption="Generated Image", use_column_width=True)

def remove_all_png_files(folder_path):
    """
    Remove all PNG files from the given folder.
 
    Parameters:
    - folder_path (str): Path to the folder containing PNG files.
    """
    try:
        # Ensure the folder path is valid
        if not os.path.isdir(folder_path):
            raise ValueError("Invalid folder path")
 
        # Create a glob pattern for PNG files in the folder
        png_files_pattern = os.path.join(folder_path, '*.png')
 
        # Get a list of PNG files in the folder
        png_files = glob.glob(png_files_pattern)
 
        # Iterate through each PNG file and remove it
        for png_file in png_files:
            os.remove(png_file)
            # print(f"Removed: {png_file}")
 
        print("Removal process completed.")
 
    except Exception as e:
        print(f"Error: {e}")

# Clear History
def clear_history(filename):
    # Clear the contents of the text file
    with open(filename, "w") as file:
        file.write("")


def Diagrams():
    openai.api_type = "azure"
    openai.api_base = "https://capgeminiopenai.openai.azure.com/"
    openai.api_version = "2023-07-01-preview"
    openai.api_key = "bd1badfce950429ab2e42504ade5079c"
    MAX_CONTEXT_QUESTIONS = 10
    saved_prompts = []

    # image_folder_path = "C:/Users/GALONE/Downloads/Architecture_Diagram_UI"  # Replace with your actual image folder path

    new_question = st.text_area("Enter your prompt:", height=10) #14
    if new_question:
        saved_prompts.append(new_question)
    generate_button = st.button("Generate Architecture Diagram")

    with st.sidebar:
        st.markdown('<h1 style="font-size:24px;">History</h1>', unsafe_allow_html=True)


    if generate_button:
        folder_path = os.getcwd()
        remove_all_png_files(folder_path)
        # Save updated prompts to the file
        save_prompts(saved_prompts, "prompts.txt")
        previous_questions_and_answers = []
        response = get_response(Instructions, previous_questions_and_answers, new_question)
        # add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((new_question, response))



        node_response = get_nodes(node_ins, previous_questions_and_answers, response)
        # add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((new_question, node_response))



        extracted_code = extract_code(node_response)

        if extracted_code:
            print(extracted_code)
            extracted_code = str(extracted_code)
        else:
            print("No code found in the cell output.")


        file = open('text_response.txt', 'w')
        file.write(extracted_code)
        file.close()
        file_path = 'text_response.txt'
        # Read the code from the file
        with open(file_path, 'r') as file:
            python_code = file.read()
        # Execute the code
        try:
            exec(python_code)
            print("Executed in 1st occurance")
        except Exception as e:
            print(f"An error occurred: {e}")
            error_variable = str(e)
            print(error_variable)
            ###################    FEEDBACK LOOP     ####################################################################
            count = 0
            while True:
                count=count+1
                error_msg=False
                def extract_error_line(code):
                    try:
                        exec(code)
                    except Exception as e:
                        # Extract the error message and line number
                        error_message = str(e)
                        error_line = e.__traceback__.tb_lineno
                        error_info = f" line {error_line}"

                    # You can store the error information in a variable or print it
                    # For example, storing in a variable named 'error_info'
                    return error_info
                Error_line = extract_error_line(extracted_code)
                print(Error_line)
                Feedback_code_instruction = f"""
                You are an expert in Python and your task involves reviewing and correcting a Python code snippet. This code utilizes the Diagrams library to create an architecture diagram.
                Instructions:
                1.Error Identification: You will be provided with an error message stored in the variable {error_variable} for the following code {extracted_code}. Your first task is to understand this error.
                2.Code Correction: Use the error information to correct the mistakes in the code snippet provided in {extracted_code}.
                3.Handling Import Errors: If the error is related to an import issue or if a node is not available:
                Refer to the documentation or the list of available nodes and imports in diagrams library that is: {Diagram_Library}.
                Replace any incorrect imports or node names with the correct ones from the Diagrams library.
                4.Code Review: Thoroughly review the entire code snippet to identify and fix any additional errors.
                5.Maintain Original Structure: While correcting the code, ensure that you keep the original structure and logic intact, except for the lines where errors are identified and corrected.
                Output Requirements:
                1.Present the corrected version of the Python code.
                2.Your response should exclusively contain the revised code without any additional commentary or explanation"""
                previous_questions_and_answers = []
                new_question = f'''Correct error {error_variable} from {Error_line} in {extracted_code} referring to {Diagram_Library}.'''

                new_code = get_nodes(Feedback_code_instruction,previous_questions_and_answers,new_question)
                # add the new question and answer to the list of previous questions and answers
                previous_questions_and_answers.append((new_question, node_response))
                # Only Extract the code from new_code
                extracted_code = extract_code(new_code)
                if extracted_code:
                    print(extracted_code)

                else:
                    print("No code found in the cell output.")

                extracted_code = str(extracted_code)
                file = open('text_response.txt', 'w')
                file.write(extracted_code)
                file.close()
                file_path = 'text_response.txt'
                # Read the code from the file
                with open(file_path, 'r') as file:
                    python_code = file.read()
                # Execute the code
                try:
                    exec(python_code)
                    print(f"Executed in feedback loop for {count} iteration.")
                except Exception as e:
                    print(f"An error occurred: {e}")
                    error_variable =str(e)
                    error_msg=True

                if error_msg==False:
                    break
        
        image_folder_path = os.getcwd()  # Replace with your actual image folder path
        latest_image = get_latest_image(image_folder_path)
        image_path = os.path.join(image_folder_path, latest_image)

        # Display the image in Streamlit
        img = Image.open(image_path)
        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG")

        st.image(img, caption="Generated Image", use_column_width=True)


        download_button = st.download_button(
            label="Download Image",
            data=img_bytes.getvalue(),  # Convert BytesIO to bytes
            file_name=os.path.basename(image_path),
            mime="image/png"
        )
        if download_button:
            st.image(img, caption="Generated Image", use_column_width=True)
            # Handle the download button click
            handle_download_button(img_bytes, image_path)

    with st.sidebar:
        main_container = st.container()
        with main_container:
            # Create two columns for the layout
            col1, col2 = st.columns([2, 2])
            # Add elements to the left column (History tab)
            with col2:
                clear_button = st.button("Clear History")

                if clear_button:
                    # Clear history button clicked, clear the contents of the text file
                    clear_history("prompts.txt")


def get_response_graphviz(instructions, previous_questions_and_answers, new_question):
    """Get a response from ChatCompletion

    Args:
        instructions: The instructions for the chat bot - this determines how it will behave
        previous_questions_and_answers: Chat history
        new_question: The new question to ask the bot

    Returns:
        The response text
    """
    # build the messages
    messages = [
        { "role": "system", "content": instructions },
    ]
    # add the previous questions and answers
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question
    messages.append({ "role": "user", "content": new_question })

    completion = openai.ChatCompletion.create(
       engine="gpt-4-32k",
        messages=messages,
        temperature=0.7,
        top_p=0.95
    )
    return completion.choices[0].message.content

def get_nodes_graphviz(instructions, previous_questions_and_answers, new_question):
    """Get a response from ChatCompletion

    Args:
        instructions: The instructions for the chat bot - this determines how it will behave
        previous_questions_and_answers: Chat history
        new_question: The new question to ask the bot

    Returns:
        The response text
    """
    # build the messages
    messages = [
        { "role": "system", "content": instructions },
    ]
    # add the previous questions and answers
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question


    completion = openai.ChatCompletion.create(
        engine="gpt-4-32k",
        messages=messages,
        temperature=0.7,
        top_p=0.95
    )
    return completion.choices[0].message.content

def extract_code_graphviz(text):
  """Removes starting and ending double quotes, slashes, and backslashes from a string.
 
  Args:
    text: The string to process.
 
  Returns:
    The cleaned string.
  """
 
  text = text.strip()  # Remove leading/trailing whitespace
 
  if text.startswith('"') and text.endswith('"'):
    text = text[1:-1]  # Remove only starting and ending quotes
 
  text = text.replace('/', '')  # Remove slashes
  text = text.replace('\\', '')  # Remove backslashes
  return text


def Graphviz():
    image_state = False
    openai.api_type = "azure"
    openai.api_base = "https://capgeminiopenai.openai.azure.com/"
    openai.api_version = "2023-07-01-preview"
    openai.api_key = "bd1badfce950429ab2e42504ade5079c"
    MAX_CONTEXT_QUESTIONS = 10

    saved_prompts = []

    new_prompt = st.text_area("Enter your prompt:", height=10) #14
    if new_prompt:
        saved_prompts.append(new_prompt)
    generate_button = st.button("Generate Flow Diagram")

    with st.sidebar:
        st.markdown('<h1 style="font-size:24px;">History</h1>', unsafe_allow_html=True)


    if generate_button:

        # Save updated prompts to the file
        save_prompts(saved_prompts, "prompts_graphiz.txt")
        #Run this cell to remove the previous conversation from the history
        previous_questions_and_answers = []




        response = get_response_graphviz(INSTRUCTIONS_GRAPHVIZ, previous_questions_and_answers, new_prompt)

        # add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((new_prompt, response))
        time.sleep(7)
        node_response = get_nodes_graphviz(node_ins_graphviz, previous_questions_and_answers, response)
    
        #st.write(f"node_response: {node_response}")
        # add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((new_prompt, node_response))
        extract_text = extract_code_graphviz(node_response)
        extracted_code = str(extract_text)

        file_path = "output.dot"


        # st.write(f"extracted_code: {extracted_code}")
        # if extracted_code:
        #     print(extracted_code)
        # else:
        #     print("No code found in the cell output.")

        # Write the DOT content to the file
        try:
          #  st.write("Executed in try Block")
            with open(file_path, "w") as dot_file:
                dot_file.write(extracted_code)

            print(f"DOT content has been saved to {file_path}")


            # Read the DOT file
            dot_file_path = 'output.dot'  # Replace with the actual path to your DOT file
            with open(dot_file_path, 'r') as dot_file:
                dot_code = dot_file.read()

            # Convert DOT code to a graph image
            graph = Source(dot_code, format='png')
            graph_path = 'graph'  # Replace with the desired path to save the graph image
            graph.render(graph_path, cleanup=True)

        except Exception as e:
            print("Executed in Exception Block")
            


        # time.sleep(3)
        image_folder_path = os.getcwd()  # Replace with your actual image folder path
        latest_image = get_latest_image(image_folder_path)
        # st.write(f"latest_image: {latest_image}")
        image_path = os.path.join(image_folder_path, latest_image)
        image_path = image_path.replace('\\', '/')
        # st.write(f"image_path: {image_path}")
        #


        # Read the graph image
        image = Image.open(image_path)

        # Display the initial image
        placeholder = st.empty()
        placeholder.image(image, caption='Architecture Diagram', use_column_width=True)

        # st.image(image, caption='Architecture Diagram', use_column_width=True)
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")

        download_button = st.download_button(
                    label="Download Image",
                    data=image_bytes.getvalue(),  # Convert BytesIO to bytes
                    file_name=os.path.basename(image_path),
                    mime="image/png"
                )
        if download_button:
            # st.image(image, caption="Generated Image", use_column_width=True)
            # Handle the download button click
            # handle_download_button(image_bytes, image_path)
            handle_download_button(image_bytes, image_path, placeholder)
            image_state = True

        if image_state:
            st.image(image, caption='Architecture Diagram', use_column_width=True)








    with st.sidebar:
        main_container = st.container()
        with main_container:
            # Create two columns for the layout
            col1, col2 = st.columns([2, 2])
            # Add elements to the left column (History tab)
            with col2:
                clear_button = st.button("Clear History")

                if clear_button:
                    # Clear history button clicked, clear the contents of the text file
                    clear_history("prompts_graphiz.txt")


#--------------------Code Start--------------------------------------------

tabs = ["Architecture Diagram", "Flow Diagram"]
selected_tab = st.sidebar.radio("Select Type", tabs)

if selected_tab == "Architecture Diagram":
    Diagrams()

elif selected_tab == "Flow Diagram":
    Graphviz()









