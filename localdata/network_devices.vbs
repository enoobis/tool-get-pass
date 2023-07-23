Option Explicit

Dim objShell, objExec, objStdOut, strCommand, strOutput
Dim arrLines, line, ipAddress, macAddress
Dim strFileName, objFSO, objStream

' Define the command to retrieve the ARP table
strCommand = "arp -a"

' Create a WScript Shell object
Set objShell = CreateObject("WScript.Shell")

' Run the command and capture the output
Set objExec = objShell.Exec(strCommand)
Set objStdOut = objExec.StdOut

' Read the output into a variable
strOutput = objStdOut.ReadAll

' Specify the output file name and location
strFileName = objShell.CurrentDirectory & "\network_devices.txt"

' Create a Stream object to work with files and set it to UTF-8 encoding
Set objStream = CreateObject("ADODB.Stream")
objStream.Type = 2 ' TextStream
objStream.Charset = "UTF-8"
objStream.Open

' Write the output to the Stream
objStream.WriteText strOutput

' Save the Stream to the file
objStream.SaveToFile strFileName, 2 ' adSaveCreateOverWrite

' Close the Stream
objStream.Close

' Clean up objects
Set objStdOut = Nothing
Set objExec = Nothing
Set objShell = Nothing
Set objStream = Nothing