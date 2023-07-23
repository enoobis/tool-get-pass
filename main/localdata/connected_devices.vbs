Option Explicit

Dim colItems, objItem
Set colItems = GetObject("winmgmts:\\.\root\cimv2").ExecQuery("SELECT * FROM Win32_USBHub")

Dim strFilePath, objFSO, objTextFile
strFilePath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) & "\connected_devices.txt"
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objTextFile = objFSO.CreateTextFile(strFilePath, True)

objTextFile.WriteLine "Connected USB Devices:"
objTextFile.WriteLine "-----------------------"

For Each objItem in colItems
    objTextFile.WriteLine "Device Name: " & objItem.Description
    objTextFile.WriteLine "Device ID: " & objItem.DeviceID
    objTextFile.WriteLine "Device Status: " & objItem.Status
    objTextFile.WriteLine "--------------------------------------"
Next

objTextFile.Close