; AutoHotkey V2 script to launch with Ctrl+D, send commands, and save clipboard content

^0::
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
}