Option Explicit

Const ForWriting = 2
Const strComputer = "."  ' "." represents the local computer

Dim objWMIService, colItems, objItem
Dim dicServers, strResult

Set dicServers = CreateObject("Scripting.Dictionary")
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2")
Set colItems = objWMIService.ExecQuery("SELECT * FROM Win32_NetworkConnection")

For Each objItem in colItems
    Dim serverAddress, localAddress
    serverAddress = objItem.RemoteName
    localAddress = objItem.LocalName

    If Left(serverAddress, 2) = "\\" Then
        ' Extract server name (strip the leading "\\" from UNC path)
        serverAddress = Mid(serverAddress, 3)
        
        ' Check if the connection is to the same server as the local computer
        If serverAddress <> "" And InStr(serverAddress, ".") > 0 Then
            If Not dicServers.Exists(serverAddress) Then
                dicServers.Add serverAddress, localAddress
            Else
                dicServers(serverAddress) = dicServers(serverAddress) & ", " & localAddress
            End If
        End If
    End If
Next

' Prepare the result string
If dicServers.Count > 0 Then
    For Each server In dicServers
        strResult = strResult & "Server: " & server & ", Connected Local Shares: " & dicServers(server) & vbCrLf
    Next
Else
    strResult = "No connections to other servers found."
End If

' Save the result to a file
Dim strScriptPath, strFileName, objFSO, objFile
strScriptPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
strFileName = strScriptPath & "\connected_servers.txt"

Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objFile = objFSO.OpenTextFile(strFileName, ForWriting, True)
objFile.Write strResult
objFile.Close