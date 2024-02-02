from imageScrapper import ImageScrapper

scrapper = ImageScrapper(headless=True)
scrapper.find_urls("fps game", 200)
scrapper.download_images("./test")