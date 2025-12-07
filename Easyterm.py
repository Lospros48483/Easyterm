import os
import platform
import shutil
import pyttsx3
import threading
import ctypes

ask = ""
temp = ""
write = True
os_ver = platform.system()
usurname = ""
history_list = []
try:
    usurname = os.environ.get('USER', os.environ.get('USERNAME'))
except:
    usurname = os.environ['USER']
dir = os.getcwd()
version = "1.0.0"

def clear() -> None:
    if os_ver == "Windows":
        os.system("powershell clear")
    else:
        os.system("clear")

def history(num=None) -> None:
    global ask
    global write
    if num is None:
        print("History:")
        for i in range(len(history_list)):
            print(f"{i + 1}. {history_list[i]}")
    else:
        if 0 < num <= len(history_list):
            ask = history_list[num - 1]
            write = False
        else:
            print("Put the number correctly.")

def talk(text: str) -> None:
    def speak():
        engine = pyttsx3.init()
        engine.setProperty('rate', 85) 
        engine.say(text)
        engine.runAndWait()

    threading.Thread(target=speak).start()
    
def Message(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

print('If you need help, type "help".')
while not ask == "exit":
    if write:
        ask = input(f'{usurname} "{dir}" >>> ')
    write = True
    history_list.append(ask)

    tokens = ask.split()
    cmd = tokens[0] if tokens else ""

    if cmd == "go":
        try:
            dir = ask.split()[1]
        except IndexError:
            print("Can you put a directory? If not, type help.")
    elif cmd == "creat":
        file_type = ask.split()[1]
        try:
            file_name = ask.split()[2]
        except IndexError:
            print("You need to put first the file type and then the file. If not, type help.")
        if file_type == "file":
            try:
                if os_ver == "Windows":
                    os.system(rf"powershell ni {dir}\{file_name} -ItemType File")
                else:
                    os.system(f"touch {dir}/{file_name}")
            except OSError:
                print(f"Tried to create a file in {dir} but it went wrong. If not, type help.")
        elif file_type == "folder":
            try:
                if os_ver == "Windows":
                    os.mkdir(rf"{dir}\{file_name}")
                else:
                    os.mkdir(f"{dir}/{file_name}")
            except OSError:
                print(f"Tried to create a folder in {dir} but it went wrong. If not, type help.")
        else:
            print("Switch the order of the file and file type.")
    elif cmd == "help":
        print("""help -> See what commands exist and do. Command: help
go -> Goes into the directory that you say. Command: go [directory]
creat -> You can create a folder or file with this command with any name using the already directory. Command: creat [type] [name + file extension]
clear -> You can clear your screen with this command. Command: clear
edit -> You can edit files with this command (to get  in linux or MacOS press: esc + : + q. In windows: ctrl + q). Command: edit [optional directory]
list -> We you can see what files you have in a directory selected or a custom one. Command: list [optional directory]
delet -> You can delete files or folders with this command. Command: delet [type] [file or folder or directory]
rename -> You can rename files however you want. Command: rename [directory with original file name with extension] [new file name with extension]
copy -> You can copy any file to another directory. Command: copy [directory with file with the extension] [directory where it is going to be]
ping -> Run test to see your network traffic. Command: ping [a website]
history -> If you put only history, it gives you a list of numbers of that you can choose from to do that command. Command: history [optional number command]
os -> Run this and tells what os you have. Command: os.
say -> Print's the text that you put. Command: say [text]
talk -> Says the text that you put. Command: talk [text]
python -> Activate python. Command: python
message -> Put's a massage but the styles are: 0 : OK, 1 : OK | Cancel, 2 : Abort | Retry | Ignore, 3 : Yes | No | Cancel, 4 : Yes | No, 5 : Retry | Cancel , 6 : Cancel | Try Again | Continue. Command: message ( [title] ) [text] [style]
download -> Let's you download anything from anyware. Command: download [URL] [file name]
remote -> To access someones computer with there ip adrres. Command: remote [ip adrres]
kill -> To kill a program that is running. Command: kill [name of the program]
unzip -> To unzip a .zip file. Command: unzip [File]
ver -> To see in what version is the program. Command: ver
open -> You can open websides and files! Command: open [file name or URL (with www.)]
credit -> Tell's you who did it! Command: credit""")
    elif cmd == "clear":
        clear()
    elif cmd == "edit":
        if os_ver == "Windows":
            try:
                os.system(f"edit {ask.split()[1]}")
            except IndexError:
                os.system("edit") 
        else:
            try:
                os.system(f"vim {ask.split()[1]}")
            except IndexError:
                os.system("vim")
    elif cmd == "list":
        if os_ver == "Windows":
            try:
                os.system(f"dir {ask.split()[1]}")
            except IndexError:
                os.system(f"dir {dir}")
            except OSError:
                print("Please put a valid directory. If not, type help.")
        else:
            try:
                os.system(f"ls {ask.split()[1]}")
            except IndexError:
                os.system(f"ls {dir}")
    elif cmd == "delet":
        if os_ver == "Windows":
            if ask.split()[1] == "folder":
                try:
                    os.system(rf"rmdir /S /Q {dir}\{ask.split()[2]}")
                except IndexError:
                    print("Please put a folder name. If not, type help.")
                except OSError:
                    os.system(f"rmdir /S /Q {ask.split()[2]}")
            elif ask.split()[1] == "file":
                try:
                    os.system(rf"del /Q {dir}\{ask.split()[2]}")
                except IndexError:
                    print("Please put a file name. If not, type help.")
                except OSError:
                    os.system(f"del /Q {ask.split()[2]}")
            else:
                print("Put file or folder and then the file name or the folder name. If not, type help.")
        else:
            if ask.split()[1] == "file":
                try:
                    os.system(rf"rm {dir}/{ask.split()[2]}")
                except IndexError:
                    print("Please put a file name. If not, type help.")
                except OSError:
                    os.system(f"rm {ask.split()[2]}")
            elif ask.split()[1] == "folder":
                try:
                    os.system(rf"rm -r {dir}/{ask.split()[2]}")
                except IndexError:
                    print("Please put a folder name. If not, type help.")
                except OSError:
                    os.system(f"rm -r {ask.split()[2]}")
            else:
                print("Put file or folder and then the file name or the folder name. If not, type help.")
    elif cmd == "rename":
        try:
            os.rename(ask.split()[1], ask.split()[2])
        except IndexError:
            print("Please put a directory. If not, type help.")
        except FileNotFoundError:
            print("The file that you tried to rename didn't work. If not, type help.")
    elif cmd == "copy":
        try:
            src = ask.split()[1]
            dst = ask.split()[2]
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
        except IndexError:
            print("Please put the directories. If not, type help.")
        except shutil.SameFileError:
            print("This file already exists! If not, type help.")
        except FileExistsError:
            print("The destination already exists! If not, type help.")      
    elif cmd == "ping":
        try:
            if os_ver == "Windows":
                os.system(f"ping -n 5 {ask.split()[1]}")
            else:
                os.system(f"ping -c 5 {ask.split()[1]}")
        except IndexError:
                print("Please put a URL. If not, type help.")
    elif cmd == "os":
        print(f"Your OS is {os_ver}")
    elif cmd == "history":
        if len(ask.split()) >= 2:
            try:
                num = int(ask.split()[1])
                history(num)
            except ValueError:
                print("Please provide a valid number for history. If not, type help.")
        else:
            history(None)
    elif cmd == "say":
        temp = " ".join(ask.split()[1:])
        print(temp)
    elif cmd == "talk":
        temp = " ".join(ask.split()[1:]) 
        talk(temp)
    elif cmd == "python":
        if os_ver == "Windows":
            try:
                os.system(f"python {ask.split()[1]}")
            except IndexError:
                os.system("python")
        else:
            try:
                os.system(f"python3 {ask.split()[1]}")
            except IndexError:
                os.system("python3")
    elif cmd == "message":
        tokens = ask.split()
        
        if len(tokens) < 4: pass
        else:
            title = ""
            try:
                clauses_start = tokens.index('(')
                clauses_end = tokens.index(')')
                length = clauses_end - clauses_start - 1
            except:
                title = ""
                
            for i in range(length):
                title = title + " " +tokens[i + 2]
            
            style_token = tokens[-1]
            try:
                style = int(style_token)
            except ValueError:
                print("Style must be an integer. See help for valid styles. If not, type help.")
            else:
                text = " ".join(tokens[clauses_end + 1:-1])
                Message(title, text, style)
    elif cmd == "download":
        try:
            os.system(f"curl -o {dir}/{ask.split()[2]} {ask.split()[1]}")
        except IndexError:
            print("Please put a URL. If not, type help.")
    elif cmd == "remote":
        try:
            os.system(f"ssh {ask.split()[1]}")
        except IndexError:
            print("Please put a ip addres. If not, type help.")
    elif cmd == "kill":
        try:
            if os_ver == "Windows":
                os.system(f"taskkill /F /IM {ask.split()[1]}.exe")
            else:
                os.system(f"pkill {ask.split()[1]}")
        except IndexError:
            print("Please put a running program. If not, type help.")
    elif cmd == "unzip":
        if os_ver == "Windows":
            os.mkdir(rf"{dir}\Unzip")
            try:
                os.system(rf"tar -xf {dir}\{ask.split()[1]} -C {dir}\Unzip")
            except OSError:
                os.system(rf"tar -xf {ask.split()[1]} -C {ask.split()[1]}")
            except IndexError:
                print("Please put a .zip file. If not, type help.")
        else:
            try:
                os.system(rf"unzip {dir}/{ask.split()[1]}")
            except OSError:
                os.system(rf"unzip {ask.split()[1]}")
            except IndexError:
                print("Please put a .zip file. If not, type help.")
    elif cmd == "ver":
        print(version)
    elif cmd == "open":
        try:
            if os_ver == "Windows":
                os.system(f"start {ask.split()[1]}")
            elif os_ver == "Linux":
                os.system(f"xdg-open {ask.split()[1]}")
            else:
                os.system(f"open {ask.split()[1]}")
        except IndexError:
            print('Please put a file or a URL with "www.". If not, type help.')
    elif cmd == "credit":
        print("Created by Lospros48483 in Github")