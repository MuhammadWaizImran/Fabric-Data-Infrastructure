param prefix string
param suffix string
param location string
param tags object
param sqlAdministrator string
@secure()
param sqlAdministratorPassword string
@secure()
param postgresAdministratorPassword string

resource sql 'Microsoft.Sql/servers@2023-08-01' = {
  name: '${prefix}-sql-${suffix}'
  location: location
  tags: tags
  properties: {
    administratorLogin: sqlAdministrator
    administratorLoginPassword: sqlAdministratorPassword
    version: '12.0'
    minimalTlsVersion: '1.2'
    publicNetworkAccess: 'Disabled'
  }
}
resource database 'Microsoft.Sql/servers/databases@2023-08-01' = {
  parent: sql
  name: 'operations'
  location: location
  tags: tags
  sku: { name: 'S0', tier: 'Standard' }
  properties: { collation: 'SQL_Latin1_General_CP1_CI_AS', maxSizeBytes: 268435456000 }
}
resource postgres 'Microsoft.DBforPostgreSQL/flexibleServers@2024-08-01' = {
  name: '${prefix}-pg-${suffix}'
  location: location
  tags: tags
  sku: { name: 'Standard_D2s_v3', tier: 'GeneralPurpose' }
  properties: {
    version: '16'
    administratorLogin: 'pgadmin'
    administratorLoginPassword: postgresAdministratorPassword
    storage: { storageSizeGB: 32 }
    backup: { backupRetentionDays: 7, geoRedundantBackup: 'Disabled' }
    highAvailability: { mode: 'Disabled' }
    network: { publicNetworkAccess: 'Disabled' }
  }
}
resource pgDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2024-08-01' = {
  parent: postgres
  name: 'operations'
  properties: { charset: 'UTF8', collation: 'en_US.utf8' }
}
resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {
  name: '${prefix}-cosmos-${suffix}'
  location: location
  tags: tags
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [{ locationName: location, failoverPriority: 0, isZoneRedundant: false }]
    consistencyPolicy: { defaultConsistencyLevel: 'Session' }
    publicNetworkAccess: 'Disabled'
    backupPolicy: { type: 'Continuous', continuousModeProperties: { tier: 'Continuous7Days' } }
  }
}
resource cosmosDatabase 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-05-15' = {
  parent: cosmos
  name: 'operations'
  properties: { resource: { id: 'operations' } }
}
resource cosmosContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = {
  parent: cosmosDatabase
  name: 'orders'
  properties: {
    resource: { id: 'orders', partitionKey: { paths: ['/customer_id'], kind: 'Hash' } }
    options: { throughput: 400 }
  }
}
resource databricks 'Microsoft.Databricks/workspaces@2024-05-01' = {
  name: '${prefix}-dbx-${suffix}'
  location: location
  tags: tags
  sku: { name: 'premium' }
  properties: {
    managedResourceGroupId: subscriptionResourceId('Microsoft.Resources/resourceGroups', '${prefix}-dbx-managed-${suffix}')
    parameters: { enableNoPublicIp: { value: true } }
  }
}
output sqlServerFqdn string = sql.properties.fullyQualifiedDomainName
output postgresFqdn string = postgres.properties.fullyQualifiedDomainName
