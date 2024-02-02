# ImageScrapper
ImageScrapper is part of a school project that requires images in order to 
test various types of machine learning algorithms. 
<br> It was required from us to build our own dataset and this script serves this purpose.

It's goal is to download a set of images in a given path by using a search key to query images
on Google Image.

## Requirements

This script requires Google Chrome Driver in order to work, using the selenium library, make sure that it is 
installed before. Other requirements are listed in the ``requirements.txt`` file.

## Usage

To use the script, you can do the following :
```shell
    python main.py --search_keyword "keyword" --dir_path "relative/absolute_path" -n <integer> --headless
```
**Required parameters :**

```--search_keyword``` is the word provided to the Google image query<br>
``--dir_path`` is the path where the images will be stored, if the folder does not exist it will be created<br>
``--num_images`` or ``-n`` is the number of images to download

**Optional parameters :**

``--headless`` is used to enable headless mode during the script execution (for selenium)
    
