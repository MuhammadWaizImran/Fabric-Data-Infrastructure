targetScope = 'subscription'
param resourceGroupName string
resource group 'Microsoft.Resources/resourceGroups@2024-03-01' existing = { name: resourceGroupName }
resource definition 'Microsoft.Authorization/policyDefinitions@2023-04-01' = {
  name: 'analytics-environment-tag-audit'
  properties: {
    policyType: 'Custom'
    mode: 'Indexed'
    displayName: 'Audit analytics resources missing an environment tag'
    policyRule: {
      if: { field: 'tags[environment]', exists: 'false' }
      then: { effect: 'audit' }
    }
  }
}
module assignment './modules/policy-assignment.bicep' = {
  name: 'analytics-tag-audit'
  scope: group
  params: { policyDefinitionId: definition.id }
}
