# Inno Setup gerektirir (iscc.exe PATH'te olmali)
$iss = Join-Path -Path "build" -ChildPath "installer.iss"
& iscc.exe $iss
