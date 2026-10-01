// Deploy separately in the resource group containing the platform resources.
// This secures Azure-side connectivity; it does not enable Fabric outbound access.
targetScope = 'resourceGroup'
param location string = resourceGroup().location
param storageAccountName string
param keyVaultName string
param eventHubNamespaceName string

resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: 'analytics-vnet'
  location: location
  properties: {
    addressSpace: { addressPrefixes: ['10.42.0.0/16'] }
    subnets: [{ name: 'private-endpoints', properties: { addressPrefix: '10.42.1.0/24', privateEndpointNetworkPolicies: 'Disabled' } }]
  }
}
var services = [
  { name: 'storage-dfs', id: resourceId('Microsoft.Storage/storageAccounts', storageAccountName), group: 'dfs', zone: 'privatelink.dfs.${environment().suffixes.storage}' }
  { name: 'storage-blob', id: resourceId('Microsoft.Storage/storageAccounts', storageAccountName), group: 'blob', zone: 'privatelink.blob.${environment().suffixes.storage}' }
  { name: 'vault', id: resourceId('Microsoft.KeyVault/vaults', keyVaultName), group: 'vault', zone: 'privatelink.vaultcore.azure.net' }
  { name: 'eventhubs', id: resourceId('Microsoft.EventHub/namespaces', eventHubNamespaceName), group: 'namespace', zone: 'privatelink.servicebus.windows.net' }
]
resource zones 'Microsoft.Network/privateDnsZones@2020-06-01' = [for service in services: {
  name: service.zone
  location: 'global'
}]
resource links 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = [for (service, index) in services: {
  parent: zones[index]
  name: 'analytics-link'
  location: 'global'
  properties: { virtualNetwork: { id: vnet.id }, registrationEnabled: false }
}]
resource endpoints 'Microsoft.Network/privateEndpoints@2024-05-01' = [for service in services: {
  name: '${service.name}-pe'
  location: location
  properties: {
    subnet: { id: '${vnet.id}/subnets/private-endpoints' }
    privateLinkServiceConnections: [{ name: service.name, properties: { privateLinkServiceId: service.id, groupIds: [service.group] } }]
  }
}]
resource zoneGroups 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2024-05-01' = [for (service, index) in services: {
  parent: endpoints[index]
  name: 'default'
  properties: { privateDnsZoneConfigs: [{ name: service.name, properties: { privateDnsZoneId: zones[index].id } }] }
}]
