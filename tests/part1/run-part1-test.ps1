param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('q2', 'q3', 'q4', 'q5', 'q6')]
    [string]$Query,

    [string]$Database = 'csc343'
)

$ErrorActionPreference = 'Stop'

$datasetMap = @{
    q2 = 'tests/part1/q2_helpfulness_core.sql'
    q3 = 'tests/part1/q3_curators_core.sql'
    q4 = 'tests/part1/q4_best_worst_core.sql'
    q5 = 'tests/part1/q5_hyperconsumers_core.sql'
    q6 = 'tests/part1/q6_yoy_core.sql'
}

$dataset = $datasetMap[$Query]
$queryFile = "part1/$Query.sql"
$tableName = "Recommender.$Query"

Write-Host "Loading schema, dataset, and $queryFile into $Database..."

psql -d $Database -v ON_ERROR_STOP=1 `
    -f schema.ddl `
    -f $dataset `
    -f $queryFile `
    -c "TABLE $tableName;"

if ($LASTEXITCODE -ne 0) {
    throw "psql returned exit code $LASTEXITCODE"
}
