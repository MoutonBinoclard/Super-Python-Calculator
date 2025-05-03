; AutoHotkey V2 script to launch with Ctrl+D, send commands, and save clipboard content

^r::
{
    Send "{Enter}"
    Sleep 50
    Send "/getplayers"
    Sleep 50
    Send "{Enter}"

    ClipWait 2
    if !A_Clipboard
    {
        MsgBox "Le presse-papier est vide."
        return
    }

    FileName := "00.txt"
    File := FileOpen(FileName, "w", "UTF-8")
    File.Write(A_Clipboard)
    File.Close()
}