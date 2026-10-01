param prefix string
param suffix string
param location string
param tags object
param storageId string
param keyVaultId string
param logAnalyticsId string

resource insights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${prefix}-insights-${suffix}'
  location: location
  tags: tags
  kind: 'web'
  properties: { Application_Type: 'web', WorkspaceResourceId: logAnalyticsId }
}
resource ml 'Microsoft.MachineLearningServices/workspaces@2024-04-01' = {
  name: '${prefix}-ml-${suffix}'
  location: location
  tags: tags
  identity: { type: 'SystemAssigned' }
  properties: {
    friendlyName: 'Analytics ML'
    storageAccount: storageId
    keyVault: keyVaultId
    applicationInsights: insights.id
    publicNetworkAccess: 'Disabled'
  }
}
resource foundry 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: '${prefix}-ai-${suffix}'
  location: location
  tags: tags
  kind: 'AIServices'
  sku: { name: 'S0' }
  identity: { type: 'SystemAssigned' }
  properties: {
    customSubDomainName: '${prefix}-ai-${suffix}'
    allowProjectManagement: true
    disableLocalAuth: true
    publicNetworkAccess: 'Disabled'
  }
}
resource project 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' = {
  parent: foundry
  name: 'analytics'
  location: location
  tags: tags
  identity: { type: 'SystemAssigned' }
  properties: { displayName: 'Analytics enrichment', description: 'Connect a Fabric data agent after provisioning.' }
}
resource adx 'Microsoft.Kusto/clusters@2023-08-15' = {
  name: take('${prefix}adx${suffix}', 22)
  location: location
  tags: tags
  sku: { name: 'Dev(No SLA)_Standard_E2a_v4', tier: 'Basic', capacity: 1 }
  identity: { type: 'SystemAssigned' }
  properties: { enableStreamingIngest: true, publicNetworkAccess: 'Disabled' }
}
resource adxDatabase 'Microsoft.Kusto/clusters/databases@2023-08-15' = {
  parent: adx
  name: 'telemetry_source'
  location: location
  kind: 'ReadWrite'
  properties: { softDeletePeriod: 'P30D', hotCachePeriod: 'P7D' }
}
output foundryEndpoint string = foundry.properties.endpoint
