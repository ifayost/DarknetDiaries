import argparse
import os
import subprocess 

from pathlib import Path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            prog='DarknetDiaries',
            description='Automate the download of Darknet Diaries episodes.',
            )
    parser.add_argument('--path', type=str, default=None,
                       help='Path to save episodes (default: ./Darknet Diaries)')
    parser.add_argument('--transcript', action='store_true', default=False, 
                        help='Download the transcript.')
    args = parser.parse_args()
    
    cwd = Path(os.getcwd())

    print('\n\n[*] Generating the bash script to call the programm with the parameters.')
    call = '#!/bin/bash\n'
    call += str(cwd / '.venv/bin/python3') + ' ' + str(cwd / 'main.py')
    if args.path is not None:
        call += f' --path {args.path}'
    if args.transcript:
        call += ' --transcript'
    call += '\n'
    bash_script = cwd / 'DarknetDiaries.sh' 
    with bash_script.open('w') as f:
        f.write(call)
    os.system('chmod +x ' + str(bash_script))
    print('    [+] Ok.')

    print('\n\n[*] Creating a symbolic link into /usr/local/bin ...')
    bin_path = Path('/usr/local/bin') 
    if str(bin_path) not in os.environ['PATH']:
        print('    [!] /usr/local/bin not in PATH.')
        print('\n\n[*] Choose a folder from your PATH to put link to DarkentDiaries script:\n')
        path = os.environ['PATH'].split(':')
        for i, p in enumerate(path):
            print('    ' + str(i) + '. ' + p)
        bin_path = input('> ')
        bin_path = Path(path[int(bin_path)])
        print(f'\n\n[*] Creating a symbolic link into {bin_path} ...')
    link = bin_path / 'DarknetDiaries'
    if link.exists():
        os.system('sudo rm ' + str(link))
    else:
        os.system(f'sudo ln -s {cwd}/DarknetDiaries.sh {link}')
    print('    [+] Ok.')

    print('\n\n[*] Adding a cron job to the users crontab to execute the script every first Tuesday of the month.')
    crontab = '0 9 1-7 * * [ "$(date \'+\%u\')" = "2" ] && DarknetDiaries'
    output = subprocess.check_output(['crontab', '-l']).decode()
    if crontab not in output:
        crontab = '0 9 1-7 * * [ \\\"\$(date \'+\%u\')\\\" = \\\"2\\\" ] && DarknetDiaries'
        command = f'(crontab -l 2>/dev/null; echo "{crontab}") | crontab -'
        os.system(command)
    else:
        print('    [!] Process already in users crontab.')
    print('    [+] Ok.\n')
