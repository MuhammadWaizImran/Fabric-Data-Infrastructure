[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ResourceGroup,
    [Parameter(Mandatory=$true)][string]$SubscriptionId,
    [Parameter(Mandatory=$true)][string]$ParameterFile,
    [switch]$Apply
)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$resolvedParameters = (Resolve-Path -LiteralPath $ParameterFile).Path
$parameterText = Get-Content -Raw -LiteralPath $resolvedParameters
if ($parameterText -match 'REPLACE_') { throw 'Resolve all parameter placeholders before planning.' }
$command = if ($Apply) { 'create' } else { 'what-if' }
& az deployment group $command --subscription $SubscriptionId --resource-group $ResourceGroup --template-file (Join-Path $repoRoot 'infra/azure/main.bicep') --parameters "@$resolvedParameters"
if ($LASTEXITCODE -ne 0) { throw "Azure deployment $command failed." }
