; ==== Dynamic Hotkey Loader (AHK v2) ====
; Path to settings.json (in same folder as script)
settingsPath := A_ScriptDir "\settings.json"

; Read settings.json
settingsData := FileRead(settingsPath, "UTF-8")

; Extract "activate_game_saver_key" value
if RegExMatch(settingsData, '"activate_game_saver_key"\s*:\s*"(.*?)"', &match) {
    gameSaverKey := match[1]
} else {
    MsgBox "Could not find 'activate_game_saver_key' in settings.json", "Error", 16
    ExitApp()
}

; Extract "re_calculate_after_saving" value
if RegExMatch(settingsData, '"re_calculate_after_saving"\s*:\s*(true|false)', &match) {
    reCalculateAfterSaving := (match[1] = "true")
} else {
    MsgBox "Could not find 're_calculate_after_saving' in settings.json", "Error", 16
    ExitApp()
}

; Build hotkey string (Ctrl + key)
hotkeyStr := "^" . gameSaverKey

; Dynamically assign hotkey
Hotkey(hotkeyStr, ActivateGameSaver)

; Show shortcut information to user
ShowShortcutInfo(gameSaverKey)
return

; Function to show shortcut information
ShowShortcutInfo(key)
{
    ; Format the key for display (capitalize it for better readability)
    displayKey := Format("Ctrl + {1}", StrUpper(key))
    
    MsgBox("SPC Saver is active!`n`nUse " displayKey " to save a round.", "SPC Saver", "OK")
}

; ==== End Dynamic Hotkey Loader ====

ActivateGameSaver(*)
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

    if reCalculateAfterSaving
    {
        Run(A_ScriptDir "/spc.exe", , "Min")
        MsgBox "Calculation running + Round saved as " FileName "`n`nPreview:`n" preview, "SPC Saver"
}
    else
    {
        MsgBox "Round saved as " FileName "`n`nPreview:`n" preview, "SPC Saver"
    }
}