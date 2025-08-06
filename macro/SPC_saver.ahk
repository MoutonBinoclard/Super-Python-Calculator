; AutoHotkey V2 script to launch with Ctrl+M, send commands, and save clipboard content

^m::
{
    Send "{Enter}"
    Sleep 150
    Send "/getplayers"
    Sleep 150
    Send "{Enter}"
    Sleep 700

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


    ; Read the first 5 lines of the saved file for preview
    preview := ""
    File := FileOpen(FileName, "r", "UTF-8")
    Loop 5
    {
        line := File.ReadLine()
        if line = ""
            break
        preview .= line "`n"
    }
    File.Close()
    MsgBox "Round saved as " FileName "`n`nPreview:`n" preview, "SPC Saver"
}