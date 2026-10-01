param policyDefinitionId string
resource assignment 'Microsoft.Authorization/policyAssignments@2024-04-01' = {
  name: 'analytics-tag-audit'
  properties: { policyDefinitionId: policyDefinitionId, enforcementMode: 'Default' }
}
