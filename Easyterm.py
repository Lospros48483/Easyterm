import os
from platform import system
import shutil
from pyttsx3 import init
from threading import Thread
from subprocess import Popen
from subprocess import run
from sys import executable
from qrcode import make
from cv2 import imread
from pyzbar.pyzbar import decode
from random import uniform, randint
from art import text2art
from pathlib import Path

ask = ""
count = 0
temp = ""
write = True
os_ver = system()
usurname = ""
history_list = []
try:
    usurname = os.environ.get('USER', os.environ.get('USERNAME'))
except:
    usurname = os.environ['USER']
dir = os.getcwd()
version = "1.4.0"
adb_dir = ""

def clear() -> None:
    if os_ver == "Windows":
        run("powershell clear", shell=True)
    else:
        run("clear", shell=True)

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
        engine = init()
        engine.setProperty('rate', 85) 
        engine.say(text)
        engine.runAndWait()

    Thread(target=speak).start()
    
def show_message(title, text, style=0):
    try:
        import tkinter as tk
        from tkinter import messagebox
    except:
        print("You don't have GUI, So this command can't run!")
        return
    root = None
    try:
        root = tk.Tk()
        root.withdraw()
        try:
            root.attributes("-topmost", True)
        except Exception:
            pass
        try:
            # Map style to the messagebox function name
            func_map = {
                0: 'showinfo',
                1: 'askokcancel',
                2: 'askretrycancel',
                3: 'askyesnocancel',
                4: 'askyesno',
                5: 'askretrycancel',
                6: 'askyesnocancel'
            }
            func_name = func_map.get(style, 'showinfo')

            dialog_code = (
                "import tkinter as tk\n"
                "from tkinter import messagebox\n"
                "root = tk.Tk()\n"
                "root.withdraw()\n"
                "try:\n"
                "    root.attributes(\"-topmost\", True)\n"
                "except Exception:\n"
                "    pass\n"
                f"messagebox.{func_name}({repr(title)}, {repr(text)})\n"
                "try:\n"
                "    root.destroy()\n"
                "except Exception:\n"
                "    pass\n"
            )

            Popen([executable, "-c", dialog_code], start_new_session=True)
            return
        except Exception:
            try:
                root = tk.Tk()
                root.withdraw()
                try:
                    root.attributes("-topmost", True)
                except Exception:
                    pass

                if style == 0:
                    messagebox.showinfo(title, text)
                elif style == 1:
                    messagebox.askokcancel(title, text)
                elif style == 2:
                    messagebox.askretrycancel(title, text)
                elif style == 3:
                    messagebox.askyesnocancel(title, text)
                elif style == 4:
                    messagebox.askyesno(title, text)
                elif style == 5:
                    messagebox.askretrycancel(title, text)
                elif style == 6:
                    messagebox.askyesnocancel(title, text)
                else:
                    messagebox.showinfo(title, text)
            except Exception:
                pass
            finally:
                try:
                    root.destroy()
                except Exception:
                    pass
    except tk.TclError:
        pass
    finally:
        if root is not None:
            try:
                root.destroy()
            except Exception:
                pass


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
            if os.path.exists(" ".join(ask.split()[1:])):
                dir = " ".join(ask.split()[1:])
            else:
                print("Please put a directory! If not, type help.")
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
                    run(rf"powershell ni {dir}\{file_name} -ItemType File", shell=True)
                else:
                    run(f"touch {dir}/{file_name}", shell=True)
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
exit -> To exit the program! Command: exit
go -> Goes into the directory that you say. Command: go [directory]
creat -> You can create a folder or file with this command with any name using the already directory. Command: creat [type] [name + file extension]
clear -> You can clear your screen with this command. Command: clear
edit -> You can edit files with this command (to get  in linux or MacOS press: esc + : + q. In windows: ctrl + q). Command: edit [optional directory]
list -> We you can see what files you have in a directory selected or a custom one. Command: list [optional directory]
delet -> You can delete files or folders with this command. Command: delet [type] [file or folder or directory]
rename -> You can rename files however you want. Command: rename [optional directory with original file name with extension] [optional directory with new file name with extension]
copy -> You can copy any file to another directory. Command: copy [directory with file with the extension] [directory where it is going to be]
ping -> Run test to see your network traffic. Command: ping [a website]
history -> If you put only history, it gives you a list of numbers of that you can choose from to do that command. Command: history [optional number command]
os -> Run this and tells what os you have. Command: os.
say -> Print's the text that you put. Command: say [text]
talk -> Says the text that you put. Command: talk [text]
python -> Activate python. Command: python
message -> Put's a massage but the styles are: 0 : OK, 1 : OK | Cancel, 2 : Abort | Retry | Ignore, 3 : Yes | No | Cancel, 4 : Yes | No, 5 : Retry | Cancel , 6 : Cancel | Try Again | Continue. Command: message ([title]) [text] [style]
download -> Let's you download anything from anyware. Command: download [URL] [file name]
remote -> To access someones computer with there ip adrres. Command: remote [ip adrres]
kill -> To kill a program that is running. Command: kill [name of the program]
unzip -> To unzip a .zip file. Command: unzip [File]
ver -> To see in what version is the program. Command: ver
open -> You can open websides and files! Command: open [file name or URL (with www.)]
credit -> Tell's you who did it! Command: credit
qr -> You can creat qr codes of any type, it will go to your selected dirrectory! Command: qr ([text or url])
qrscan -> You can scan qr codes to get it's info, it will go to your selected dirrectory to get the file! Command: qrscan [file name + extension]
random -> You can random any number but no text! Command: random [first number] [second number]
find -> You can look up the file name with extension and find the dirrectory it is! Command: find [file name + extension]
ascii -> You can have ascii art in seconds! Command: ascii (your text)
add -> So you can add numbers! Command: add (1 number to add) (2 number to add)
sub -> So you can substract numbers! Command: sub (1 number to substract) (2 number to substract)
mult -> So you can multiply numbers! Command: mult (1 number to multiply) (2 number to multiply)
div -> So you can divide numbers! Command: div (1 number to divide) (2 number to divide)
infoweb -> You can see the websides code (HTML). Command: infoweb [webside to get the code]
home -> Goes to the home directory. Command: home
which -> To see where a command is in the computer. Command: which [command]
pip -> To install or uninstall python libraries! Command: pip [install or uninstall] [Python libray name]
count -> Counts many numbers you want. Command: count [number to count, needs to be number]
adb -> Enables you to use android tools easily with normal commands! Command: adb [normal command]
createxe -> Lets you creat an file of the terminal, you will need to put your directory with go and put it in the directory with the python program and icon. Command: createxe
reboot -> reboot's your computer. Command: reboot
shutdown -> shutdown's your computer. Command: shutdown""")
    elif cmd == "clear":
        clear()
    elif cmd == "edit":
        if os_ver == "Windows":
            try:
                run(f"edit {ask.split()[1]}", shell=True)
            except IndexError:
                run("edit", shell=True) 
        else:
            try:
                run(f"vim {dir}/{ask.split()[1]}", shell=True)
            except OSError:
                run(f"vim {ask.split()[1]}", shell=True)
            except IndexError:
                run("vim")
    elif cmd == "list":
        if os_ver == "Windows":
            try:
                run(f'dir "{ask.split()[1]}"', shell=True)
            except IndexError:
                run(f'dir "{dir}"', shell=True)
            except OSError:
                print("Please put a valid directory. If not, type help.")
        else:
            try:
                run(f"ls {ask.split()[1]}", shell=True)
            except IndexError:
                run(f"ls {dir}")
    elif cmd == "delet":
        if os_ver == "Windows":
            if ask.split()[1] == "folder":
                try:
                    run(rf"rmdir /S /Q {dir}\{ask.split()[2]}", shell=True)
                except IndexError:
                    print("Please put a folder name. If not, type help.")
                except OSError:
                    run(f"rmdir /S /Q {ask.split()[2]}", shell=True)
            elif ask.split()[1] == "file":
                try:
                    run(rf"del /Q {dir}\{ask.split()[2]}", shell=True)
                except IndexError:
                    print("Please put a file name. If not, type help.")
                except OSError:
                    run(f"del /Q {ask.split()[2]}", shell=True)
            else:
                print("Put file or folder and then the file name or the folder name. If not, type help.")
        else:
            if ask.split()[1] == "file":
                try:
                    run(rf"rm {dir}/{ask.split()[2]}", shell=True)
                except IndexError:
                    print("Please put a file name. If not, type help.")
                except OSError:
                    run(f"rm {ask.split()[2]}", shell=True)
            elif ask.split()[1] == "folder":
                try:
                    run(rf"rm -r {dir}/{ask.split()[2]}", shell=True)
                except IndexError:
                    print("Please put a folder name. If not, type help.")
                except OSError:
                    run(f"rm -r {ask.split()[2]}", shell=True)
            else:
                print("Put file or folder and then the file name or the folder name. If not, type help.")
    elif cmd == "rename":
        try:
            try:
                os.rename(ask.split()[1], ask.split()[2])
            except OSError:
                if os_ver == "Windows":
                    os.rename(rf"{dir}\{ask.split()[1]}", rf"{dir}\{ask.split()[2]}")
                else:
                    os.rename(rf"{dir}/{ask.split()[1]}", rf"{dir}/{ask.split()[2]}")
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
        except FileNotFoundError:
            print("The file or directory you have put does not exist! If not, type help.")
    elif cmd == "ping":
        try:
            if os_ver == "Windows":
                run(f"ping -n 5 {ask.split()[1]}", shell=True)
            else:
                run(f"ping -c 5 {ask.split()[1]}", shell=True)
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
                run(f"python {ask.split()[1]}", shell=True)
            except IndexError:
                run("python", shell=True)
        else:
            try:
                run(f"python3 {ask.split()[1]}", shell=True)
            except IndexError:
                run("python3", shell=True)
    elif cmd == "message":
        length: int
        tokens = list(ask)
        token = ask.split()
        
        if len(tokens) < 8: pass
        else:
            title = ''
            try:
                clauses_start = tokens.index('(')
                clauses_end = tokens.index(')')
                length = clauses_end - clauses_start - 1
            except:
                title = ''
            
            if title == '':
                for i in range(length):
                    title = title + tokens[i + 9]
            else:
                title = ''
            
            style_token = token[-1]
            try:
                style = int(style_token)
            except ValueError:
                print("Style must be an integer. See help for valid styles. If not, type help.")
            else:
                text = "".join(tokens[clauses_end + 1:-1])
                show_message(title, text, style)
    elif cmd == "download":
        try:
            if os_ver == "Windows":
                try:
                    run(rf"curl -o {dir}\{ask.split()[2]} {ask.split()[1]}", shell=True)
                except OSError:
                    run(f"curl -o {ask.split()[2]} {ask.split()[1]}", shell=True)
            else:
                try:
                    run(f"curl -o {dir}/{ask.split()[2]} {ask.split()[1]}", shell=True)
                except OSError:
                    run(f"curl -o {ask.split()[2]} {ask.split()[1]}", shell=True)
        except IndexError:
            print("Please put a URL. If not, type help.")
    elif cmd == "remote":
        try:
            run(f"ssh {ask.split()[1]}", shell=True)
        except IndexError:
            print("Please put a ip addres. If not, type help.")
    elif cmd == "kill":
        try:
            if os_ver == "Windows":
                run(f"taskkill /F /IM {ask.split()[1]}.exe", shell=True)
            else:
                run(f"pkill {ask.split()[1]}", shell=True)
        except IndexError:
            print("Please put a running program. If not, type help.")
    elif cmd == "unzip":
        if os_ver == "Windows":
            os.mkdir(rf"{dir}\Unzip")
            try:
                run(rf"tar -xf {dir}\{ask.split()[1]} -C {dir}\Unzip", shell=True)
            except OSError:
                run(rf"tar -xf {ask.split()[1]} -C {ask.split()[1]}", shell=True)
            except IndexError:
                print("Please put a .zip file. If not, type help.")
        else:
            try:
                run(rf"unzip {dir}/{ask.split()[1]}", shell=True)
            except OSError:
                run(rf"unzip {ask.split()[1]}", shell=True)
            except IndexError:
                print("Please put a .zip file. If not, type help.")
    elif cmd == "ver":
        print(version)
    elif cmd == "open":
        try:
            if os_ver == "Windows":
                run(f"start {ask.split()[1]}", shell=True)
            elif os_ver == "Linux":
                run(f"xdg-open {ask.split()[1]}", shell=True)
            else:
                run(f"open {ask.split()[1]}", shell=True)
        except IndexError:
            print('Please put a file or a URL with "www.". If not, type help.')
    elif cmd == "qr":
        length: int
        data = ''
        tokens = list(ask)
        
        if len(tokens) < 3: pass
        else:
            data = ''
            try:
                clauses_start = tokens.index('(')
                clauses_end = tokens.index(')')
                length = clauses_end - clauses_start - 1
            except:
                data = ""
            
            if data == "":
                for i in range(length):
                    data = data + tokens[i + 4]
            else:
                data = ''
        
        img = make(data)
        
        if os_ver == "Windows":
            with open(rf"{dir}\qrcode.png", "wb") as f:
                img.save(f)
        else:
            with open(f"{dir}/qrcode.png", "wb") as f:
                img.save(f)
    elif cmd == "qrscan":
        token = ask.split()[1:]
        try:
            datas = " ".join(token)
        except IndexError:
            print("Please put a flie name and flie extension. if not, type help.")
        
        if os_ver == "Windows":
            image = imread(rf"{dir}\{datas}")
        else:
            image = imread(f"{dir}/{datas}")

        if image is None:
            print("Could not load image. Please provide a valid file or go to the directorry. If not, type help.")
        else:
            codes = decode(image)
            
            for code in codes:
                data = code.data.decode('utf-8')

            if data:
                print(f"The QR code has {data}")
            else:
                print("No QR code detected.")
    elif cmd == "random":
        randomNumInt: int
        randomNumFloat: float
        try:
            randomNumInt = randint(int(ask.split()[1]), int(ask.split()[2]))
            print(randomNumInt)
        except ValueError:
            try:
                randomNumFloat = uniform(float(ask.split()[1]), float(ask.split()[2]))
                print(randomNumFloat)
            except:
                print("Don't Put a text in the number's spot! if not, type help.")
        except:
            print("Please put 2 numbers to be able to do the randomaising! If not, type help.")
    elif cmd == "find":
        token = ask.split()[1:]
        try:
            datass = " ".join(token)
        except IndexError:
            print("Please put a flie name and flie extension. if not, type help.")
        
        if os_ver == "Windows":
            run(f'powershell "gdr -PSProvider FileSystem | % {{ Get-ChildItem -Path $_.Root -Filter {datass} -Recurse -ErrorAction SilentlyContinue }} | Select-Object FullName"', shell=True)
        else:
            run(f"sudo find / -name {datass} 2>/dev/null", shell=True)
    elif cmd == "ascii":
        token = ask.split()[1:]
        try:
            datasss = " ".join(token)
        except IndexError:
            print("Please put text. if not, type help.")
        
        word = text2art(datasss)
        print(word)
    elif cmd == "add":
        token = ask.split()[1:]
        if len(token) < 2:
            print("Please provide two numbers. If not, type help.")
        else:
            try:
                a = float(token[0])
                b = float(token[1])
            except ValueError:
                print("Please put a number, not text! If not, type help.")
            else:
                s = a + b
                if s.is_integer():
                    print(int(s))
                else:
                    print(s)
    elif cmd == "sub":
        token = ask.split()[1:]
        if len(token) < 2:
            print("Please provide two numbers. If not, type help.")
        else:
            try:
                a = float(token[0])
                b = float(token[1])
            except ValueError:
                print("Please put a number, not text! If not, type help.")
            else:
                s = a - b
                if s.is_integer():
                    print(int(s))
                else:
                    print(s)
    elif cmd == "mult":
        token = ask.split()[1:]
        if len(token) < 2:
            print("Please provide two numbers. If not, type help.")
        else:
            try:
                a = float(token[0])
                b = float(token[1])
            except ValueError:
                print("Please put a number, not text! If not, type help.")
            else:
                s = a * b
                if s.is_integer():
                    print(int(s))
                else:
                    print(s)
    elif cmd == "div":
        token = ask.split()[1:]
        if len(token) < 2:
            print("Please provide two numbers. If not, type help.")
        else:
            try:
                a = float(token[0])
                b = float(token[1])
            except ValueError:
                print("Please put a number, not text! If not, type help.")
            else:
                s = a / b
                if s.is_integer():
                    print(int(s))
                else:
                    print(s)
    elif cmd == "infoweb":
        try:
            run(f"curl {tokens[1]}", shell=True)
        except IndexError:
            print("Please put the webside link (URL). If not, type help.")
    elif cmd == "home":
        dir = str(Path.home())
    elif cmd == "which":
        try:
            if os_ver == "Windows":
                run(f"where {ask.split()[1]}", shell=True)
            else:
                run(f"which {ask.split()[1]}", shell=True)
        except IndexError:
            print("Please put what you want to find the command directory. If not, type help.")
    elif cmd == "pip":
        try:
            if os_ver == "Windows":
                run(f"py -m pip {ask.split()[1]} {ask.split()[2]}", shell=True)
            else:
                run(f"pip {ask.split()[1]} {ask.split()[2]}", shell=True)
        except IndexError:
            print("Please put install or unistall and the pakage name. If not, type help.")
    elif cmd == "count":
        try:
            count += int(ask.split()[1])
            print(count)
        except IndexError:
            print("Please put a number. If not, type help.")
        except ValueError:
            print("Please put a number and not text! If not, type help.")
    elif cmd == "adb":
        if adb_dir == "":
            adb_dir = input("What is the directory where is the adb tools: ")
            trying = False
            while not trying == True:
                try:
                    run(fr"{adb_dir}\adb.exe", shell=True)
                    trying = True
                except OSError:
                    adb_dir = input("The directory you gave was wronge. What is the directory where is the adb tools: ")
                    trying = False
        
        try:
            run(fr"{adb_dir}\adb.exe {" ".join(ask.split()[1:])}", shell=True)
        except IndexError:
            print("Here are some commands: ")
            run(fr"{adb_dir}\adb.exe")
    elif cmd == "rust":
        if os_ver == "Windows":
            rustc_path = shutil.which('rustc')
            if rustc_path is None:
                rustc_path = rf"{os.environ['USERPROFILE']}\.cargo\bin\rustc.exe"
            try:
                run(f'"{rustc_path}" {ask.split()[1]}', shell=True)
            except IndexError:
                run(f'"{rustc_path}"', shell=True)
        else:
            try:
                run(f"rustc {ask.split()[1]}", shell=True)
            except IndexError:
                run("rustc", shell=True)
    elif cmd == "createxe":
        if os_ver == "Windows":
            run(fr"python -m PyInstaller --onefile --icon={dir}\icon.png --collect-all pyzbar {dir}\Easyterm.py", shell=True)
            shutil.rmtree(fr"{dir}\build")
            os.remove(fr"{dir}\Easyterm.spec")
        else:
            run(f"python3 -m PyInstaller --onefile --icon={dir}/icon.png --collect-all pyzbar {dir}/Easyterm.py", shell=True)
            shutil.rmtree(fr"{dir}/build")
            os.remove(fr"{dir}/Easyterm.spec")
    elif cmd == "reboot":
        if os_ver == "Windows":
            run("shutdown /r /t 0")
        else:
            run("sudo reboot")
    elif cmd == "shutdown":
        if os_ver == "Windows":
            run("shutdown /s /t 0")
        else:
            run("sudo shutdown -h now")
    elif cmd == "credit":
        print("Created by Lospros48483 in Github")
