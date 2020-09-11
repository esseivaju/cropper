# Photoworkshop cropper

## Installation on macOS

You'll need to setup a virtual env to install the script and its dependencies. Download [Miniconda3 MacOSX 64-bit bash](https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh) on the [mininconda website](https://docs.conda.io/en/latest/miniconda.html) then open a terminal and execute the following commands:
```bash
# cd to another directory if you downloaded the file somewhere else
cd ~/Downloads
chmod +x Miniconda3-latest-MacOSX-x86_64.sh
./Miniconda3-latest-MacOSX-x86_64.sh -b

# !!IMPORTANT!! -> Close the current terminal window and reopen a new window for the changes to take effect otherwise you'll get errors when executing the next commands.

conda create -y -nphotoworkshop python=3.7
conda activate photoworkshop
pip install git+https://github.com/esseivaju/photoworkshop_cropper

# You can now use the photoworkshop script:
photoworkshop_cropper --help
```

Whenever you want to use the script, you'll first need to activate the virtual env you created:
```bash
conda activate photoworkshop # Activate the virtualenv whenever you open a terminal window to use the photoworkshop script
photoworkshop_cropper --help # You have access to cli command again
```

 ## Usage
```
usage: photoworkshop_cropper [-h] --src SRC --dst DST [--uniform-size]
                             [--padding-size PADDING_SIZE] [--ignore-realign]
                             [--min-box WIDTH HEIGHT] [--max-box WIDTH HEIGHT]
                             [--workers WORKERS]

optional arguments:
  -h, --help            show this help message and exit
  --src SRC             Source directory containing tif data
  --dst DST             Destination director where cropped image are saved
  --uniform-size        If set, performs a 1st pass across data to find the
                        largest crop region and apply the same crop box to
                        each picture
  --padding-size PADDING_SIZE
                        Padding area added to the bounding box. Avoid cutting
                        text close to the edge of the box
  --ignore-realign      If set, do not try to rotate picture to deskew the
                        text
  --min-box WIDTH HEIGHT
                        Restricts the detected page area to have a larger
                        width/height
  --max-box WIDTH HEIGHT
                        Restricts te detected page area to have a smaller
                        width/heigt. The resulting images will never be larger
                        than the box specified here, even taking into account
                        the padding size
  --workers WORKERS     Number of workers to use. Default to the number of cpu
                        cores
```