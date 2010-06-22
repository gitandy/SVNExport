#include <version.iss>
#define MyAppName "SVN-Export"
#define MyAppExeName "SVNExportGUI.exe"

[Files]
Source: dist\{#MyAppExeName}; DestDir: {app}
Source: dist\svnexport.exe; DestDir: {app}
Source: svnexport.ico; DestDir: {app}
Source: LICENSE; DestDir: {app}
[Setup]
AppCopyright=©2010, Andreas Schawo <andreas@schawo.de>
AppName={#MyAppName}
AppVerName={#MyAppVersion}
PrivilegesRequired=none
DefaultDirName={pf}\{#MyAppName}
AppID={{B11E4A7B-310E-46EF-92CC-52FF02EAF2D1}
LanguageDetectionMethod=locale
SetupIconFile=C:\Programme\Inno Setup 5\Examples\Setup.ico
WizardImageFile=C:\Programme\Inno Setup 5\WizModernImage-IS.bmp
WizardSmallImageFile=C:\Programme\Inno Setup 5\WizModernSmallImage-IS.bmp
OutputBaseFilename={#MyAppName}-{#MyAppVersion}-Setup
DefaultGroupName={#MyAppName}
UsePreviousGroup=false
AppendDefaultGroupName=false
DisableStartupPrompt=false
UsePreviousSetupType=false
ShowLanguageDialog=auto
LicenseFile=LICENSE
InfoAfterFile=
[LangOptions]
LanguageName=German
LanguageID=$0407
[Icons]
Name: {group}\{#MyAppName}; Filename: {app}\{#MyAppExeName}; IconFilename: {app}\{#MyAppExeName}; WorkingDir: {app}
Name: {commondesktop}\{#MyAppName}; Filename: {app}\{#MyAppExeName}; Tasks: desktopicon; WorkingDir: {app}; IconFilename: {app}\bug.ico; Comment: Game; IconIndex: 0
Name: {userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}; Filename: {app}\{#MyAppExeName}; Tasks: quicklaunchicon; WorkingDir: {app}; IconFilename: {app}\bug.ico; Comment: Game; IconIndex: 0
[Languages]
Name: German; MessagesFile: compiler:Languages\German.isl
[Tasks]
Name: desktopicon; Description: {cm:CreateDesktopIcon}; GroupDescription: {cm:AdditionalIcons}
Name: quicklaunchicon; Description: {cm:CreateQuickLaunchIcon}; GroupDescription: {cm:AdditionalIcons}; Flags: unchecked
[UninstallDelete]
Name: {app}\*.pyc; Type: files
Name: {app}\*.pyo; Type: files
Name: {app}\*.log; Type: files
