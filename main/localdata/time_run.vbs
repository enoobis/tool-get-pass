Option Explicit

' Function to retrieve system uptime
Function GetSystemUptime()
    Dim objWMIService, colOperatingSystems, objOperatingSystem
    Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")
    Set colOperatingSystems = objWMIService.ExecQuery("SELECT * FROM Win32_OperatingSystem")
    
    For Each objOperatingSystem In colOperatingSystems
        GetSystemUptime = objOperatingSystem.LastBootUpTime
        Exit Function
    Next
    
    GetSystemUptime = ""
End Function

' Function to convert WMI datetime to a VBScript Date type
Function ConvertWMIDateTime(wmiDate)
    Dim strDateTime
    strDateTime = CStr(wmiDate)
    ConvertWMIDateTime = DateSerial(Left(strDateTime, 4), Mid(strDateTime, 5, 2), Mid(strDateTime, 7, 2)) & " " & TimeSerial(Mid(strDateTime, 9, 2), Mid(strDateTime, 11, 2), Mid(strDateTime, 13, 2))
End Function

' Function to calculate PC awake time
Function CalculateAwakeTime()
    Dim lastBootTime, currentTime, awakeTimeInSeconds
    lastBootTime = GetSystemUptime()
    lastBootTime = ConvertWMIDateTime(lastBootTime) ' Convert WMI datetime to VBScript Date
    currentTime = Now()
    awakeTimeInSeconds = DateDiff("s", lastBootTime, currentTime)
    CalculateAwakeTime = awakeTimeInSeconds
End Function

' Function to format seconds into HH:MM:SS
Function FormatTime(seconds)
    Dim hours, minutes
    hours = Int(seconds / 3600)
    seconds = seconds Mod 3600
    minutes = Int(seconds / 60)
    seconds = seconds Mod 60
    FormatTime = Right("0" & hours, 2) & ":" & Right("0" & minutes, 2) & ":" & Right("0" & seconds, 2)
End Function

' Function to save awake time to a text file
Sub SaveAwakeTimeToFile(filePath, awakeTimeFormatted)
    Dim fso, file
    Set fso = CreateObject("Scripting.FileSystemObject")
    Set file = fso.CreateTextFile(filePath)
    file.WriteLine "PC Awake Time: " & awakeTimeFormatted
    file.Close
End Sub

' Main program
Dim awakeTimeInSeconds, awakeTimeFormatted
Dim scriptPath, txtFilePath

awakeTimeInSeconds = CalculateAwakeTime()
awakeTimeFormatted = FormatTime(awakeTimeInSeconds)

scriptPath = WScript.ScriptFullName
txtFilePath = Replace(scriptPath, WScript.ScriptName, "") & "time_run.txt"

SaveAwakeTimeToFile txtFilePath, awakeTimeFormatted