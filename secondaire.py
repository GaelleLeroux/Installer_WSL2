# -*- coding: utf-8 -*-cd D
import ctypes
import sys
import os
import time
import subprocess
import urllib.request
import re
import argparse
from colorama import init, Fore

# Initialiser colorama
init(autoreset=True)

# Check if ubuntu is installed on the computer
def is_ubuntu_installed():
    result = subprocess.run(['wsl', '--list'], capture_output=True, text=True)
    output = result.stdout.encode('utf-16-le').decode('utf-8')
    clean_output = output.replace('\x00', '')  # Enlève tous les octets null
    return 'Ubuntu' in clean_output

# check if the code is running in administrator
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
def download_wsl2_kernel(kernel_path):
    kernel_url = "https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi"
    urllib.request.urlretrieve(kernel_url, kernel_path)
    return kernel_path 

# Install the kernel of linux
def install_wsl2_kernel(kernel_path):
    subprocess.run(["msiexec", "/i", kernel_path, "/quiet"], check=True)

def check_wsl2_kernel_installed():
    try:
        # Run the WSL status command to get information about the WSL installations
        result = subprocess.run("wsl --status", stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
        
        # If the command was successful, process the output
        if result.returncode == 0:
            # output = result.stdout
            output_nclean = result.stdout.encode('utf-16-le').decode('utf-8')
            output = output_nclean.replace('\x00', '')  # Enlève tous les octets null
            
            # Look for a line that indicates the WSL version
            kernel_version_search = re.search(r'Kernel version: (\d+\.\d+\.\d+)', output)
            
            if kernel_version_search:
                kernel_version = kernel_version_search.group(1)
                return True
            else:
                return False
        else:
            return None
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        print(f"Error output: {e.stderr}")
        return None
    
def print_command(message):
    '''
    print in green in the terminal
    '''
    print(Fore.GREEN + message)

def write_output(file_path,message):
    '''
    write in the temprary file
    '''
    with open(file_path, 'a') as file:  # Ouverture du fichier en mode 'append'
        file.write(message + '\n')  # Écrire le message suivi d'une nouvelle ligne
        
def main(kernel_path,file_path):
    print_command("This windows will be close automatically, please wait")

    # Check is WSL activate in parameters of windows
    wsl_status = subprocess.run("dism.exe /online /get-featureinfo /featurename:Microsoft-Windows-Subsystem-Linux",
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    
    write_output(file_path,f"wsl_status : {wsl_status}")
    
    virtual_machine_status = subprocess.run("dism.exe /online /get-featureinfo /featurename:VirtualMachinePlatform",
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    
    write_output(file_path,f"virtual_machine_status : {virtual_machine_status}")

    
    activate_wsl = False
    if "Enabled" not in wsl_status.stdout:
            # Activate WSL and virtual machine platform for wsl2
            print("want to enable wsl")
            write_output(file_path,"want to enable wsl")
            subprocess.run("dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart", shell=True)
            print("Enabled wsl")
            # need to restart the computer
            activate_wsl = True
            write_output(file_path,"restart")

    if "Enabled" not in virtual_machine_status.stdout:
            print("want to enable virtual machine")
            write_output(file_path,"want to enable virtual machine")
            subprocess.run("dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart", shell=True)
            activate_wsl = True
            write_output(file_path,"restart")
       
    test_kernel=False
    if not activate_wsl :     
        test_kernel = check_wsl2_kernel_installed()
        if test_kernel!=True:
            try : 
                kernel_path = download_wsl2_kernel(kernel_path)
                install_wsl2_kernel(kernel_path)
                test_kernel=True
            except:
                write_output(file_path,"errorKernel")  
        
    if test_kernel==True:
        write_output(file_path,"ready")
    write_output(file_path,"LetsContinue")
        
        
        
if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print(f"Error this script need 2 arguments. You have {len(sys.argv)} arguments")
        print(f"The arguments you enter are : \n{sys.argv}")
        time.sleep(10)
        
        