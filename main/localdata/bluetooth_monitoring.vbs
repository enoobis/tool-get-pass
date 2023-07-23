Option Explicit

Const BluetoothClassGUID = "{0ECEF634-6EF0-472A-8085-5AD023ECBCCD}"

Dim objWMIService, colItems, objItem
Dim strOutputPath, objFSO, objOutputFile

strOutputPath = GetScriptDirectory()
strOutputPath = strOutputPath & "\bluetooth_devices.txt"

Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")
Set colItems = objWMIService.ExecQuery("SELECT * FROM Win32_PnPEntity WHERE ClassGuid = '" & BluetoothClassGUID & "'")

If colItems.Count = 0 Then
    SaveOutput "No Bluetooth devices found."
Else
    Dim strOutput
    strOutput = "Bluetooth Device Information:" & vbCrLf & "--------------------------------------" & vbCrLf

    For Each objItem In colItems
        strOutput = strOutput & "Device Name: " & objItem.Name & vbCrLf
        strOutput = strOutput & "Device Description: " & objItem.Description & vbCrLf
        strOutput = strOutput & "Device Manufacturer: " & objItem.Manufacturer & vbCrLf
        strOutput = strOutput & "Device Status: " & objItem.Status & vbCrLf
        strOutput = strOutput & "--------------------------------------" & vbCrLf
    Next

    SaveOutput strOutput
End If

Sub SaveOutput(outputText)
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    Set objOutputFile = objFSO.CreateTextFile(strOutputPath, True)
    objOutputFile.Write outputText
    objOutputFile.Close
End Sub

Function GetScriptDirectory()
    Dim objFSO, strScriptPath
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
    Set objFSO = Nothing
    GetScriptDirectory = strScriptPath
End Function