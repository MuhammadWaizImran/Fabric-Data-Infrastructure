targetScope = 'resourceGroup'

@minLength(3)
@maxLength(10)
param prefix string = 'analytics'
@allowed(['dev', 'test', 'prod'])
param environment string = 'dev'
param location string = resourceGroup().location
param fabricLocation string = location
param fabricSku string = 'F2'
@minLength(1)
param fabricAdministrators array
param sqlAdministrator string = 'analyticsadmin'
@secure()
param sqlAdministratorPassword string
@secure()
param postgresAdministratorPassword string
param operatorObjectId string
param monthlyBudget int = 250
param budgetStartDate string
param budgetEndDate string
param budgetContactEmails array = []

var suffix = uniqueString(resourceGroup().id)
var tags = { project: 'azure-fabric-analytics', environment: environment, managedBy: 'bicep' }

module platform './modules/platform.bicep' = {
  name: 'platform'
  params: {
    prefix: prefix
    suffix: suffix
    location: location
    fabricLocation: fabricLocation
    fabricSku: fabricSku
    fabricAdministrators: fabricAdministrators
    operatorObjectId: operatorObjectId
    tags: tags
  }
}
module sources './modules/sources.bicep' = {
  name: 'sources'
  params: {
    prefix: prefix
    suffix: suffix
    location: location
    tags: tags
    sqlAdministrator: sqlAdministrator
    sqlAdministratorPassword: sqlAdministratorPassword
    postgresAdministratorPassword: postgresAdministratorPassword
  }
}
module intelligence './modules/intelligence.bicep' = {
  name: 'intelligence'
  params: {
    prefix: prefix
    suffix: suffix
    location: location
    tags: tags
    storageId: platform.outputs.storageId
    keyVaultId: platform.outputs.keyVaultId
    logAnalyticsId: platform.outputs.logAnalyticsId
  }
}
resource budget 'Microsoft.Consumption/budgets@2023-11-01' = {
  name: '${prefix}-monthly'
  properties: {
    amount: monthlyBudget
    category: 'Cost'
    timeGrain: 'Monthly'
    timePeriod: { startDate: budgetStartDate, endDate: budgetEndDate }
    notifications: length(budgetContactEmails) > 0 ? {
      Actual80: {
        enabled: true
        operator: 'GreaterThanOrEqualTo'
        threshold: 80
        thresholdType: 'Actual'
        contactEmails: budgetContactEmails
      }
    } : {}
  }
}
output fabricCapacityResourceId string = platform.outputs.fabricCapacityId
output storageAccountName string = platform.outputs.storageName
output keyVaultName string = platform.outputs.keyVaultName
output eventHubNamespace string = platform.outputs.eventHubNamespace
output sqlServerFqdn string = sources.outputs.sqlServerFqdn
output postgresFqdn string = sources.outputs.postgresFqdn
output foundryEndpoint string = intelligence.outputs.foundryEndpoint
output deploymentNotice string = 'Resource shells only. Configure Fabric, RBAC, networking, source data and model deployments using docs/deployment.md.'
