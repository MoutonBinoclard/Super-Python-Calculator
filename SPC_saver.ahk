; AutoHotkey V2 script to launch with Ctrl+M, send commands, and save clipboard content

^m::
{
    Send "{Enter}"
    Sleep 100
    Send "/getplayers"
    Sleep 100
    Send "{Enter}"
    Sleep 300

    ClipWait 2
    if !A_Clipboard
    {
        MsgBox "Le presse-papier est vide."
        return
    }

    ; Find the highest numbered file
    highestNum := 0
    Loop Files, "*.txt"
    {
        ; Extract numbers from filenames (like "01.txt", "02.txt", etc.)
        if RegExMatch(A_LoopFileName, "^(\d+)\.txt$", &match)
        {
            fileNum := Integer(match[1])
            if (fileNum > highestNum)
                highestNum := fileNum
        }
    }
    
    ; Create new filename with next number
    nextNum := highestNum + 1
    FileName := Format("{:02d}.txt", nextNum)  ; Format as 01, 02, etc.
    
    File := FileOpen(FileName, "w", "UTF-8")
    File.Write(A_Clipboard)
    File.Close()

    ; Notify the user with a tray tip
    TrayTip "SPC Saver", "Fichier enregistré : " FileName, 5
}