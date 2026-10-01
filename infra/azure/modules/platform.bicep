@minLength(3)
@maxLength(10)
param prefix string
@minLength(13)
@maxLength(13)
param suffix string
param location string
param fabricLocation string
param fabricSku string
param fabricAdministrators array
param operatorObjectId string
param tags object

resource capacity 'Microsoft.Fabric/capacities@2023-11-01' = {
  name: '${prefix}${suffix}'
  location: fabricLocation
  tags: tags
  sku: { name: fabricSku, tier: 'Fabric' }
  properties: { administration: { members: fabricAdministrators } }
}
resource lake 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: '${prefix}${suffix}'
  location: location
  tags: tags
  kind: 'StorageV2'
  sku: { name: 'Standard_LRS' }
  properties: {
    isHnsEnabled: true
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    allowBlobPublicAccess: false
    allowSharedKeyAccess: false
    publicNetworkAccess: 'Disabled'
  }
}
resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: lake
  name: 'default'
  properties: {
    deleteRetentionPolicy: { enabled: true, days: 7 }
    containerDeleteRetentionPolicy: { enabled: true, days: 7 }
  }
}
resource containers 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = [for name in ['landing', 'raw', 'curated', 'ml', 'archive']: {
  parent: blobService
  name: name
  properties: { publicAccess: 'None' }
}]
resource vault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: take('${prefix}-kv-${suffix}', 24)
  location: location
  tags: tags
  properties: {
    tenantId: tenant().tenantId
    sku: { family: 'A', name: 'standard' }
    enableRbacAuthorization: true
    enableSoftDelete: true
    enablePurgeProtection: true
    softDeleteRetentionInDays: 7
    publicNetworkAccess: 'Disabled'
    accessPolicies: []
  }
}
resource logs 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: '${prefix}-logs-${suffix}'
  location: location
  tags: tags
  properties: { sku: { name: 'PerGB2018' }, retentionInDays: 30 }
}
resource eventHubNs 'Microsoft.EventHub/namespaces@2024-01-01' = {
  name: '${prefix}-eh-${suffix}'
  location: location
  tags: tags
  sku: { name: 'Standard', tier: 'Standard', capacity: 1 }
  properties: { minimumTlsVersion: '1.2', publicNetworkAccess: 'Disabled', disableLocalAuth: true }
}
resource hub 'Microsoft.EventHub/namespaces/eventhubs@2024-01-01' = {
  parent: eventHubNs
  name: 'telemetry'
  properties: { messageRetentionInDays: 1, partitionCount: 2 }
}
resource consumer 'Microsoft.EventHub/namespaces/eventhubs/consumergroups@2024-01-01' = {
  parent: hub
  name: 'fabric'
  properties: {}
}
resource iot 'Microsoft.Devices/IotHubs@2023-06-30' = {
  name: '${prefix}-iot-${suffix}'
  location: location
  tags: tags
  sku: { name: 'S1', capacity: 1 }
  properties: { publicNetworkAccess: 'Disabled', minTlsVersion: '1.2' }
}
resource purview 'Microsoft.Purview/accounts@2021-12-01' = {
  name: '${prefix}-purview-${suffix}'
  location: location
  tags: tags
  identity: { type: 'SystemAssigned' }
  properties: { publicNetworkAccess: 'Disabled' }
}
resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${prefix}-workload-${suffix}'
  location: location
  tags: tags
}
resource storageReader 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(lake.id, operatorObjectId, 'blob-reader')
  scope: lake
  properties: {
    principalId: operatorObjectId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '2a2b9908-6ea1-4ae2-8e65-a410df84e7d1')
  }
}
resource ehDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'send-to-log-analytics'
  scope: eventHubNs
  properties: {
    workspaceId: logs.id
    logs: [{ categoryGroup: 'allLogs', enabled: true }]
    metrics: [{ category: 'AllMetrics', enabled: true }]
  }
}
output fabricCapacityId string = capacity.id
output storageId string = lake.id
output storageName string = lake.name
output keyVaultId string = vault.id
output keyVaultName string = vault.name
output logAnalyticsId string = logs.id
output eventHubNamespace string = '${eventHubNs.name}.servicebus.windows.net'
