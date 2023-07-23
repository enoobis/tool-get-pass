Option Explicit

On Error Resume Next

Dim objWMIService, colItems, objItem
Dim strOutput, objFSO, objFile

Set objWMIService = GetObject("winmgmts:\\.\root\CIMV2")
Set colItems = objWMIService.ExecQuery("SELECT * FROM Win32_PnPEntity WHERE Name LIKE '%Bluetooth%'",,48)

If colItems.Count > 0 Then
    strOutput = "Bluetooth Devices:" & vbCrLf & "-------------------------" & vbCrLf
    For Each objItem In colItems
        strOutput = strOutput & "Name: " & objItem.Name & vbCrLf
        strOutput = strOutput & "DeviceID: " & objItem.DeviceID & vbCrLf
        strOutput = strOutput & "-------------------------" & vbCrLf
    Next
Else
    strOutput = "No Bluetooth devices found."
End If

' Get the script's directory
Dim objShell, strScriptDir
Set objShell = CreateObject("Scripting.FileSystemObject")
strScriptDir = objShell.GetParentFolderName(WScript.ScriptFullName)

' Create the output file
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objFile = objFSO.CreateTextFile(strScriptDir & "\bluetooth_connections.txt", True)

' Write the output to the file
objFile.Write strOutput

' Close the file
objFile.Close