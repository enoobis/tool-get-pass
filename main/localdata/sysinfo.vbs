Option Explicit

On Error Resume Next

Dim objWMIService, colItems, objItem
Dim strOutput, objFSO, objFile

' Connect to the WMI service
Set objWMIService = GetObject("winmgmts:\\.\root\CIMV2")

' Retrieve operating system information
strOutput = "Operating System Information:" & vbCrLf & "-------------------------" & vbCrLf
Set colItems = objWMIService.ExecQuery("SELECT * FROM Win32_OperatingSystem")
For Each objItem In colItems
    strOutput = strOutput & "Name: " & objItem.Caption & vbCrLf
    strOutput = strOutput & "Version: " & objItem.Version & vbCrLf
    strOutput = strOutput & "Manufacturer: " & objItem.Manufacturer & vbCrLf
    strOutput = strOutput & "OS Architecture: " & objItem.OSArchitecture & vbCrLf
    strOutput = strOutput & "System Directory: " & objItem.SystemDirectory & vbCrLf
    strOutput = strOutput & "Windows Directory: " & objItem.WindowsDirectory & vbCrLf
    strOutput = strOutput & "Total Virtual Memory: " & FormatNumber(objItem.TotalVirtualMemorySize / (1024 * 1024), 0) & " MB" & vbCrLf
    strOutput = strOutput & "Free Virtual Memory: " & FormatNumber(objItem.FreeVirtualMemory / (1024 * 1024), 0) & " MB" & vbCrLf
Next

' Retrieve processor information
strOutput = strOutput & vbCrLf & "Processor Information:" & vbCrLf & "-------------------------" & vbCrLf
Set colItems = objWMIService.ExecQuery("SELECT * FROM Win32_Processor")
For Each objItem In colItems
    strOutput = strOutput & "Name: " & objItem.Name & vbCrLf
    strOutput = strOutput & "Manufacturer: " & objItem.Manufacturer & vbCrLf
    strOutput = strOutput & "Architecture: " & objItem.Architecture & vbCrLf
    strOutput = strOutput & "Max Clock Speed: " & objItem.MaxClockSpeed & " MHz" & vbCrLf
    strOutput = strOutput & "Number of Cores: " & objItem.NumberOfCores & vbCrLf
Next

' Retrieve memory information
strOutput = strOutput & vbCrLf & "Memory Information:" & vbCrLf & "-------------------------" & vbCrLf
Set colItems = objWMIService.ExecQuery("SELECT * FROM Win32_PhysicalMemory")
For Each objItem In colItems
    strOutput = strOutput & "BankLabel: " & objItem.BankLabel & vbCrLf
    strOutput = strOutput & "Capacity: " & FormatNumber(objItem.Capacity / (1024 * 1024 * 1024), 2) & " GB" & vbCrLf
    strOutput = strOutput & "Speed: " & objItem.Speed & " MHz" & vbCrLf
    strOutput = strOutput & "Memory Type: " & objItem.MemoryType & vbCrLf
Next

' Get the script's directory
Dim objShell, strScriptDir
Set objShell = CreateObject("Scripting.FileSystemObject")
strScriptDir = objShell.GetParentFolderName(WScript.ScriptFullName)

' Create the output file
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objFile = objFSO.CreateTextFile(strScriptDir & "\sysinfo.txt", True)

' Write the output to the file
objFile.Write strOutput

' Close the file
objFile.Close