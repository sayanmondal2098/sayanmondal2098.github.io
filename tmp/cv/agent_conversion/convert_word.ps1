$ErrorActionPreference = 'Stop'

$source = (Resolve-Path -LiteralPath '..\Sayan-Mondal-CV.docx').Path
$outputDirectory = (Resolve-Path -LiteralPath '.').Path
$pdf = Join-Path $outputDirectory 'word-export.pdf'
$log = Join-Path $outputDirectory 'word-export.log'

function Write-Stage {
    param([string]$Message)
    Add-Content -LiteralPath $log -Value ("{0:o} {1}" -f (Get-Date), $Message)
}

Remove-Item -LiteralPath $log -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $pdf -ErrorAction SilentlyContinue

$word = $null
$document = $null
try {
    Write-Stage 'Creating Word.Application'
    $word = New-Object -ComObject Word.Application
    Write-Stage 'Word.Application created'
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $word.AutomationSecurity = 3
    $word.Options.ConfirmConversions = $false
    $word.Options.SaveNormalPrompt = $false
    $word.Options.UpdateLinksAtOpen = $false
    Write-Stage 'Opening document'
    $document = $word.Documents.Open($source, $false, $true, $false)
    Write-Stage 'Document opened'
    $document.SaveAs2($pdf, 17)
    Write-Stage 'PDF exported'
    $document.Close(0)
    $document = $null
    Write-Stage 'Document closed'
    $word.Quit(0)
    $word = $null
    Write-Stage 'Word quit'
}
catch {
    Write-Stage ("ERROR: " + $_.Exception.ToString())
    throw
}
finally {
    if ($null -ne $document) {
        try { $document.Close(0) } catch {}
    }
    if ($null -ne $word) {
        try { $word.Quit(0) } catch {}
    }
    if ($null -ne $document) {
        [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($document)
    }
    if ($null -ne $word) {
        [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($word)
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
