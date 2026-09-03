$ErrorActionPreference = 'Stop'

$outputDirectory = (Resolve-Path -LiteralPath '.').Path
$pdf = Join-Path $outputDirectory 'word-minimal.pdf'
$log = Join-Path $outputDirectory 'word-minimal.log'
Remove-Item -LiteralPath $pdf -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $log -ErrorAction SilentlyContinue

function Write-Stage {
    param([string]$Message)
    Add-Content -LiteralPath $log -Value ("{0:o} {1}" -f (Get-Date), $Message)
}

$word = $null
$document = $null
try {
    Write-Stage 'Creating Word.Application'
    $word = New-Object -ComObject Word.Application
    Write-Stage 'Word.Application created'
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $document = $word.Documents.Add()
    Write-Stage 'Blank document created'
    $document.Content.Text = 'Local PDF conversion test'
    Write-Stage 'Exporting PDF'
    $document.ExportAsFixedFormat($pdf, 17)
    Write-Stage 'PDF exported'
    $document.Close(0)
    $document = $null
    $word.Quit(0)
    $word = $null
    Write-Stage 'Word quit'
}
finally {
    if ($null -ne $document) { try { $document.Close(0) } catch {} }
    if ($null -ne $word) { try { $word.Quit(0) } catch {} }
}
