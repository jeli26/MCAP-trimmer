# MCAP-trimmer
Script to trim MCAP files based on start and end time.

## Setup
Python 3.14 required:
```
git clone https://github.com/jeli26/MCAP-trimmer.git
cd MCAP-trimmer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage
```
python main.py -p /path/to/file.mcap -s START -e END
```
Flags:
- ```-s START```: Starting elapsed time in seconds, inclusive.
- ```-e END```: Ending elapsed time in seconds, inclusive.
- ```-ia```: Enables including attatchments and metadata to trimmed MCAP file.