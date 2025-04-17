# DarknetDiaries

A Python-based script for downloading episodes from darknetdiaries.com, including their associated transcripts. The script organizes downloads into separate folders with episode titles and sets appropriate metadata, perfectly suited for media system like Jellyfin. Also, with the automate.py script you can automate the download of the new episodes every first Tuesday of the month. 

![DarknetDiaries](https://github.com/ifayost/DarknetDiaries/blob/c33c7ed85a1c2e756badba8c6bb0348064ba6765/darknetdiaries-throwing.jpg "DarknetDiaries")

## Features

- Downloads both audio episodes and transcripts (if specified)
- Organizes episodes in dedicated folders
- Sets mp3 tags including:
  - Artist: Darknet Diaries
  - Album: Episode title
  - Genre: True Crime
  - Description: Episode summary and details
  - Track number
  - Cover art
- Automates the download of new episodes every first Tuesday of the month.

## Installation

```bash
git clone https://github.com/ifayost/DarknetDiaries.git
cd DarknetDiaries
python3 -m venv .venv
source ./.venv/bin/activate
pip3 install -r ./requirements.txt
```

## Usage

### DarknetDiaries.py

Run the script from the command line with optional arguments:

```bash
python3 DarknetDiaries.py [OPTIONS]
```

#### Options

- `--episodes <EPISODE_NUMBERS>`: Specific episode numbers to download (multiple can be specified)
- `--path <DESTINATION_PATH>`: Path where episodes should be saved (default: ./Darknet\ Diaries)
- `--transcript`: Download and save transcripts alongside audio files
- No arguments: Downloads all available episodes

#### Examples

1. Download all episodes:
```bash
python3 DarknetDiaries.py
```

2. Download specific episodes #42 and #57:
```bash
python3 DarknetDiaries.py --episodes 42 57
```

3. Save episodes to a custom location:
```bash
python DarknetDiaries.py --path /my/custom/path
```

4. Download episodes to a custom location with transcripts:
```bash
python3 DarknetDiaries.py --path /my/custom/path --transcript
```

### automate.py

This script will generate a bash script and will link it to /usr/local/bin/DarknetDiaries so every time you run "DarknetDiaries" on your terminal it will search automatically for new episodes and will download it with options specified (--path and/or --transcript). If /usr/local/bin is not in your PATH the script will automatically ask you to choose one of the folders on your PATH. 

Also, it will add a cron job so it will be executed the first Tuesday of the month at 08:00.
 
Run the script from the command line with optional arguments:

```bash
python3 automate.py [OPTIONS]
```

#### Options

- `--path <DESTINATION_PATH>`: Path where episodes should be saved (default: ./Darknet\ Diaries)
- `--transcript`: Download and save transcripts alongside audio files

#### Examples

1. Save episodes to a custom location:
```bash
python automate.py --path /my/custom/path
```

2. Download episodes to a custom location with transcripts:
```bash
python3 automate.py --path /my/custom/path --transcript
```

## File Structure

By default, episodes are downloaded to `./Darknet\ Diaries/` and organized as follows:
```
./Darknet\ Diaries/
├── Episode_Title_1/
│   ├── episode.mp3
│   └── transcript.txt (if downloaded)
├── Episode_Title_2/
│   ├── episode.mp3
│   └── transcript.txt (if downloaded)
└── ...
```

## Troubleshooting

### ExFAT Filesystem Issues
If you encounter issues with special characters in filenames when using an exFAT-formatted storage device, you can modify the exfat_illegal_chars dictionary in DarknetDiaries.py to replace illegal characters.

1. Open DarknetDiaries.py and locate this section:
```python
# If you are experiencing problems with the filenames on exfat
# formated hard drives uncomment the contents of this dictionary:
exfat_illegal_chars = {
        # '"': "'",
        # '*': '',
        # '/': '.',
        # ':': '.',
        # '<': '_',
        # '>': '_',
        # '?': '¿',
        # '\\': '.',
        # '|': '.'
        } 
```

2. Uncomment the desired replacements by removing the `#` symbols:
```python
exfat_illegal_chars = {
        '"': "'",
        '*': '',
        '/': '.',
        ':': '.',
        '<': '_',
        '>': '_',
        '?': '¿',
        '\\': '.',
        '|': '.'
}
```

3. Save your changes and run again the script.

The script will now replace illegal characters with the specified alternatives when saving files:

## Contributing

Contributions are welcome! If you'd like to improve this script, feel free to:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request
