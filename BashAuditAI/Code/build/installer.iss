#define MyAppName "ShellAnalyzer"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "YourCompany"
#define MyAppExeName "ShellAnalyzer.exe"

[Setup]
AppId={{8E07AE4B-8951-4B37-8BEE-1D49B6E46C25}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputBaseFilename=ShellAnalyzer-Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "..\dist\ShellAnalyzer.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Masaüstü kısayolu oluştur"; GroupDescription: "Ekstra seçenekler:"; Flags: unchecked
