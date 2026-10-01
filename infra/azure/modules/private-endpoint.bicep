// Reusable endpoint building block. Confirm groupId and DNS zone for each service.
param location string = resourceGroup().location
param name string
param targetResourceId string
param groupId string
param subnetId string
param privateDnsZoneId string
resource endpoint 'Microsoft.Network/privateEndpoints@2024-05-01' = {
  name: name
  location: location
  properties: {
    subnet: { id: subnetId }
    privateLinkServiceConnections: [{ name: name, properties: { privateLinkServiceId: targetResourceId, groupIds: [groupId] } }]
  }
}
resource zoneGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2024-05-01' = {
  parent: endpoint
  name: 'default'
  properties: { privateDnsZoneConfigs: [{ name: 'service-zone', properties: { privateDnsZoneId: privateDnsZoneId } }] }
}
