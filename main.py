from imageScrapper import ImageScrapper

import argparse

parser = argparse.ArgumentParser(description="A tool to scrap images from google images")
parser.add_argument("--search_keyword", type=str, required=True, help="The keyword used to query google images (ex: cat)")
parser.add_argument("--dir_path", type=str, required=True, help="The path to the directory where images will be downloaded")
parser.add_argument("--num_images", '-n', type=int, required=True, help="The maximum number of images that")
parser.add_argument("--headless", action='store_true', help="Run in headless mode")
args = parser.parse_args()

scrapper = ImageScrapper(headless=args.headless)
scrapper.find_urls(args.search_keyword, args.num_images)
scrapper.download_images(args.dir_path)
scrapper.destroy()