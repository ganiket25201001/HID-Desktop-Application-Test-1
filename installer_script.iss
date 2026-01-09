; Inno Setup Script for Device Monitor Pro
; This creates a professional Windows installer with Start Menu integration
; Download Inno Setup from: https://jrsoftware.org/isdl.php

#define MyAppName "Device Monitor Pro"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Aniket Ganguly"
#define MyAppURL "https://github.com/ganiket25201001/HID-Desktop-Application-Test-1"
#define MyAppExeName "DeviceMonitorPro.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
AppId={{B3C4D5E6-F7A8-4B9C-8D7E-6F5A4B3C2D1E}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableDirPage=no
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=no
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=installer
OutputBaseFilename=DeviceMonitorPro_Setup_v{#MyAppVersion}
SetupIconFile=app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\{#MyAppExeName}
; Installation info
AppReadmeFile=https://github.com/ganiket25201001/HID-Desktop-Application-Test-1
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=Hardware Device Monitoring Tool
VersionInfoCopyright=Copyright (C) 2026 {#MyAppPublisher}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "startmenuicon"; Description: "Create Start Menu shortcuts"; GroupDescription: "{cm:AdditionalIcons}"
Name: "quicklaunchicon"; Description: "Create a &Quick Launch icon"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu - Main entry (searchable as "Device Monitor Pro"); Tasks: startmenuicon
; Start Menu - Short name (searchable as "DMP")
Name: "{group}\DMP"; Filename: "{app}\{#MyAppExeName}"; Comment: "Device Monitor Pro - Quick Access"; Tasks: startmenuicon
; Desktop icon
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
; Quick Launch
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon
; Uninstall
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"; Tasks: startmenuicon
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Registry]
; Add to Windows Search Index for better searchability
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\App Paths\{#MyAppExeName}"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName}"; Flags: uninsdeletekey

[Code]
procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpFinished then
  begin
    // Show completion message
  end;
end;

function InitializeSetup(): Boolean;
begin
  Result := True;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Post-installation tasks can go here
  end;
end;
