#define MyAppName "Quick Photo Viewer Pro"
#define MyAppVersion "2.9.0"
#define MyAppPublisher "BANG Tools"
#define MyAppExeName "QuickPhotoViewer.exe"
#define MyAppRegisteredName "Quick Photo Viewer"
#define MyAppProgId "BANGTools.QuickPhotoViewer.Image"
; Same AppId as previous Inno installations. Keep it stable across upgrades.
#ifndef BuildOutput
  #define BuildOutput GetEnv("USERPROFILE") + "\Documents\QuickPhotoViewerBuild\dist\QuickPhotoViewer"
#endif

[Setup]
AppId={{7DA76AE7-5982-47E6-A011-F87A49E5C03E}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\Quick Photo Viewer
DefaultGroupName=Quick Photo Viewer
UsePreviousAppDir=yes
UsePreviousGroup=yes
OutputDir=output
OutputBaseFilename=QuickPhotoViewer-Setup-2.9.0
SetupIconFile=..\icons\quick_photo_viewer.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
ChangesAssociations=yes
CloseApplications=yes
RestartApplications=no
DisableProgramGroupPage=yes
DisableWelcomePage=no
VersionInfoProductName={#MyAppName}
VersionInfoDescription=Quick Photo Viewer - Windows installer
VersionInfoProductVersion={#MyAppVersion}

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Shortcuts:"; Flags: unchecked
Name: "fileassoc"; Description: "Make Quick Photo Viewer available in Open with and Windows Default Apps (does not change your current defaults)"; GroupDescription: "Windows image associations:"; Flags: checkedonce
Name: "selectdefaults"; Description: "After installation, open Windows settings so I can choose my default photo app"; GroupDescription: "Windows image associations:"; Flags: unchecked

[Files]
Source: "..\maintenance.ps1"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\maintenance.ps1"; DestName: "Setup-Maintenance.ps1"; Flags: dontcopy
; Bundled onedir distribution includes the Python runtime, Qt DLLs and icon assets.
Source: "{#BuildOutput}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\QuickPhotoViewer maintenance"; Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -File ""{app}\maintenance.ps1"" -App QuickPhotoViewer -ProtectPath ""{app}"""; IconFilename: "{app}\QuickPhotoViewer.exe"
Name: "{autoprograms}\Quick Photo Viewer"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Quick Photo Viewer"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
; Register executable location without replacing Windows per-user UserChoice.
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\App Paths\{#MyAppExeName}"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName}"; Flags: uninsdeletekey
; Open-with application registration (independent of choosing the default app).
Root: HKLM; Subkey: "Software\Classes\Applications\{#MyAppExeName}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Flags: uninsdeletekey; Tasks: fileassoc
; Version-neutral, app-specific ProgID.
Root: HKLM; Subkey: "Software\Classes\{#MyAppProgId}"; ValueType: string; ValueName: ""; ValueData: "Quick Photo Viewer image"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Classes\{#MyAppProgId}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Classes\{#MyAppProgId}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Tasks: fileassoc
; Windows Default Apps listing; user chooses default types in Settings.
Root: HKLM; Subkey: "Software\Quick Photo Viewer\Capabilities"; ValueType: string; ValueName: "ApplicationName"; ValueData: "{#MyAppRegisteredName}"; Flags: uninsdeletekey; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Quick Photo Viewer\Capabilities"; ValueType: string; ValueName: "ApplicationDescription"; ValueData: "Fast, lightweight Windows image viewer. Photos remain on your computer."; Tasks: fileassoc
Root: HKLM; Subkey: "Software\RegisteredApplications"; ValueType: string; ValueName: "{#MyAppRegisteredName}"; ValueData: "Software\Quick Photo Viewer\Capabilities"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Quick Photo Viewer\Capabilities\FileAssociations"; ValueType: string; ValueName: ".jpg"; ValueData: "{#MyAppProgId}"; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Classes\.jpg\OpenWithProgids"; ValueType: none; ValueName: "{#MyAppProgId}"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Quick Photo Viewer\Capabilities\FileAssociations"; ValueType: string; ValueName: ".jpeg"; ValueData: "{#MyAppProgId}"; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Classes\.jpeg\OpenWithProgids"; ValueType: none; ValueName: "{#MyAppProgId}"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Quick Photo Viewer\Capabilities\FileAssociations"; ValueType: string; ValueName: ".png"; ValueData: "{#MyAppProgId}"; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Classes\.png\OpenWithProgids"; ValueType: none; ValueName: "{#MyAppProgId}"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Quick Photo Viewer\Capabilities\FileAssociations"; ValueType: string; ValueName: ".bmp"; ValueData: "{#MyAppProgId}"; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Classes\.bmp\OpenWithProgids"; ValueType: none; ValueName: "{#MyAppProgId}"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Quick Photo Viewer\Capabilities\FileAssociations"; ValueType: string; ValueName: ".gif"; ValueData: "{#MyAppProgId}"; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Classes\.gif\OpenWithProgids"; ValueType: none; ValueName: "{#MyAppProgId}"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Quick Photo Viewer\Capabilities\FileAssociations"; ValueType: string; ValueName: ".webp"; ValueData: "{#MyAppProgId}"; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Classes\.webp\OpenWithProgids"; ValueType: none; ValueName: "{#MyAppProgId}"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Quick Photo Viewer\Capabilities\FileAssociations"; ValueType: string; ValueName: ".tif"; ValueData: "{#MyAppProgId}"; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Classes\.tif\OpenWithProgids"; ValueType: none; ValueName: "{#MyAppProgId}"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Quick Photo Viewer\Capabilities\FileAssociations"; ValueType: string; ValueName: ".tiff"; ValueData: "{#MyAppProgId}"; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Classes\.tiff\OpenWithProgids"; ValueType: none; ValueName: "{#MyAppProgId}"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Quick Photo Viewer\Capabilities\FileAssociations"; ValueType: string; ValueName: ".ico"; ValueData: "{#MyAppProgId}"; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Classes\.ico\OpenWithProgids"; ValueType: none; ValueName: "{#MyAppProgId}"; Flags: uninsdeletevalue; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Quick Photo Viewer\Capabilities\FileAssociations"; ValueType: string; ValueName: ".svg"; ValueData: "{#MyAppProgId}"; Tasks: fileassoc
Root: HKLM; Subkey: "Software\Classes\.svg\OpenWithProgids"; ValueType: none; ValueName: "{#MyAppProgId}"; Flags: uninsdeletevalue; Tasks: fileassoc

[Run]
; Optional, user-initiated assignment of file defaults. Windows 11 requires approval.
Filename: "ms-settings:defaultapps?registeredAppMachine=Quick%20Photo%20Viewer"; Description: "Choose Quick Photo Viewer as my default image app in Windows Settings"; Flags: shellexec nowait postinstall skipifsilent runasoriginaluser; Tasks: selectdefaults
Filename: "{app}\{#MyAppExeName}"; Description: "Launch Quick Photo Viewer"; Flags: nowait postinstall skipifsilent

[Code]
var MaintenanceButton: TNewButton;
procedure OpenMaintenance(Sender: TObject);
var ResultCode: Integer;
begin
  ExtractTemporaryFile('Setup-Maintenance.ps1');
  if not Exec(ExpandConstant('{sys}\WindowsPowerShell\v1.0\powershell.exe'), '-NoProfile -ExecutionPolicy Bypass -File "' + ExpandConstant('{tmp}\Setup-Maintenance.ps1') + '" -App QuickPhotoViewer -ProtectPath "' + WizardDirValue + '"', '', SW_SHOWNORMAL, ewWaitUntilTerminated, ResultCode) then
    MsgBox('Maintenance tool could not be opened.', mbError, MB_OK);
end;
procedure InitializeWizard;
var Page: TWizardPage; Info: TNewStaticText;
begin
  Page := CreateCustomPage(wpSelectDir, 'Review previous builds', 'Optional maintenance before installation');
  Info := TNewStaticText.Create(Page); Info.Parent := Page.Surface; Info.Width := Page.SurfaceWidth; Info.WordWrap := True; Info.Caption := 'Find old builds, running copies and startup registrations. Nothing is removed automatically. Review matches and keep your project files and settings.';
  MaintenanceButton := TNewButton.Create(Page); MaintenanceButton.Parent := Page.Surface; MaintenanceButton.Top := ScaleY(56); MaintenanceButton.Width := ScaleX(235); MaintenanceButton.Caption := 'Scan and review old builds...'; MaintenanceButton.OnClick := @OpenMaintenance;
end;
