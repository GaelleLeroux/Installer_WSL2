import ctypes
import sys
import os
import time
import subprocess
import urllib.request
import tempfile
from colorama import init, Fore

# Initialise colorama
init(autoreset=True)

# Check if the file is launch with admin right
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
# Write with a color in the terminal
def print_instruction(message):
    print(Fore.RED + message)
    
def print_command(message):
    print(Fore.GREEN + message)

# Check if ubuntu is installed on the computer
def is_ubuntu_installed():
    "Check if unbuntu install"
    result = subprocess.run(['wsl', '--list'], capture_output=True, text=True)
    output = result.stdout.encode('utf-16-le').decode('utf-8')
    clean_output = output.replace('\x00', '')  # Enlève tous les octets null
    return 'Ubuntu' in clean_output

def ask_for_restart():
    confirm = input("Do you want to restart now your computer (Yes/No) ? ")
    if confirm.lower() in ['yes', 'y', '']:
        # Restart the computer after 10s
        subprocess.run(["shutdown", "/r", "/t", "10"])
        print_command("Your computer will restart in 10s.")
    else:
        print_command("The restart is cancelled.")


def main():
    text = "When an interaction is requested, it is indicated in red. Press enter to continue."
    print_instruction(text)
    
    input("Press enter")
    
    text = "The executable needs admin rights, press enter to give them."
    print_instruction(text)
    input("Press enter to give admin right")

    exe_dir = os.path.dirname(sys.executable)
    exe_name = "secondaire.exe"
    exe_path = os.path.join(exe_dir,"utils", exe_name)
    temp_file_path = os.path.join(exe_dir, "utils","tempo.txt")

    with open(temp_file_path, 'a') as file:  # Ouverture du fichier en mode 'append'
        file.write("Start of the tempo file" + '\n')  # Écrire le message suivi d'une nouvelle ligne

    # L'argument que vous voulez passer à l'exécutable
    kernel_path = os.path.join(os.path.expanduser("~"),"Downloads", "wsl_update_x64.msi")

    if is_admin():
        # Launch with subprocess secondaire if already in admin
        subprocess.run([exe_path, kernel_path,temp_file_path])
    else:
        # Ask and launch secondaire.exe if not in admin
        ctypes.windll.shell32.ShellExecuteW(None, "runas", exe_path, f"\"{kernel_path}\" \"{temp_file_path}\"", None, 1)
    
    # Attendre que l'utilisateur ferme manuellement le terminal admin ou que le script se termine
    
    # Read the tempo.txt file
    text = "Wait for a new instruction"
    print_instruction(text)
    with open(temp_file_path, 'r') as file:
        output = file.read()
        while "LetsContinue" not in output :
            time.sleep(5)
            output = file.read()
            
    # Delete tempo file
    os.unlink(temp_file_path)
            
    if "restart" in output:
        text = "Restart your computer and run this executable again."
        print_instruction(text)
        ask_for_restart()
        input("Wait for it to restart, or press enter to quit if restart is cancelled.")
        
    if "errorKernel" in output:
        text = "An error occurred during installation of the linux kernel. Have you restarted the computer?"
        print_instruction(text)
        ask_for_restart()
        input("Wait for it to restart, or press enter to quit if restart is cancelled.")
        
    if "ready" in output:
        if not is_ubuntu_installed(): # check is ubuntu is install on wsl
                #define version of wsl at 2
                subprocess.run("wsl --set-default-version 2", shell=True)

                # Write a message for the user before installing
                text = "A new windows will open!\nYou will create an username with a password, please note that whilst entering the Password, nothing will appear on screen. This is called blind typing. You won't see what you are typing, this is completely normal.\nWhen the line starts with your username, please enter 'exit' to continue the installation on this window."
                print_instruction(text)
                input("Press enter to continue")
                # input("During the installation you will create an username with a password, please note that whilst entering the Password, nothing will appear on screen. This is called blind typing. You won't see what you are typing, this is completely normal.\nWhen the line will start by your username please enter 'exit' to continue the installation\nPress enter to start the installation, it may take a few minutes")
                subprocess.check_call(["wsl", "--install","-d","Ubuntu"])
                
                # Wait for Ubuntu to be installed on WSL
                while not is_ubuntu_installed():
                    time.sleep(10)
                    
        text = "Enter the password you created when installing wsl" 
        print_instruction(text)
        input("Press enter to write the password")
        exe_dir = os.path.dirname(sys.executable)
            
        bash_script = "install_libs.sh"

        full_bash_script_path = os.path.join(exe_dir,"utils", bash_script)

        # Path to the .sh with the command to install librairie on wsl
        wsl_path = "/mnt/" + full_bash_script_path[0].lower() + full_bash_script_path[2:].replace("\\", "/")
            
        # Once WSL is initialized, execute the bash script (to install the librairies)
        subprocess.run(["wsl", "bash","-c", wsl_path])
        
        print_instruction("Installation succesfull")
        input("Press enter to quit")
        
    
if __name__ == "__main__":
    main()