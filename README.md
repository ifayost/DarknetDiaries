# DarknetDiaries

A Python-based script for downloading episodes from darknetdiaries.com, including their associated transcripts. The script organizes downloads into separate folders with episode titles and sets appropriate metadata, perfectly suited for media system like Jellyfin.

![DarknetDiaries](https://github.com/ifayost/DarknetDiaries/blob/main/darknetdiaries-throwin.jpg?raw=true "DarknetDiaries")

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

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/DarknetDiaries.git
```

2. Install required Python packages:
```bash
pip install requests beautifulsoup4 pathlib eyed3
```

Note: You may need to use `sudo` depending on your system setup.

## Usage

Run the script from the command line with optional arguments:

```bash
python main.py [OPTIONS]
```

### Options

- `--episodes <EPISODE_NUMBERS>`: Specific episode numbers to download (multiple can be specified)
- `--path <DESTINATION_PATH>`: Path where episodes should be saved (default: ./Darknet\ Diaries)
- `--transcript`: Download and save transcripts alongside audio files
- No arguments: Downloads all available episodes

### Examples

1. Download all episodes:
```bash
python main.py
```

2. Download specific episodes #42 and #57:
```bash
python main.py --episodes 42 57
```

3. Save episodes to a custom location:
```bash
python main.py --path /my/custom/path
```

4. Download episodes with transcripts:
```bash
python main.py --transcript
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

## License

MIT License

## Contributing

Contributions are welcome! If you'd like to improve this script, feel free to:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

Please ensure any code modifications follow PEP8 style guidelines and maintain existing functionality.
```

