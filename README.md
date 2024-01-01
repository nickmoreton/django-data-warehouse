# A Data Warehouse with Django and Scrapy

A Django app to store scraped website data with the intention to use the data as a source to import from.

**It's a work in progress and not ready for use in a production environment.**

Many parts of this project are based on previous work I have done. See the credits section below.

It's highly likely that this project will change significantly over time 💥

## How it works so far

1. Initial command to obtain links to all pages to scrape: `scrapy crawl sitemap`
2. Collect the page content for each site map page: `scrapy crawl pages`
3. Run command `python manage.py build_blocks` to "build the blocks" from the scraped data (page content)

## Setup

You'll need a wordpress site running from which you can scrape data. I used a local install of wordpress with default theme and sample content.

1. Clone this repo
2. Create a virtualenv and install requirements `poetry install then poetry shell`
3. Create a database and user for the project `python manage.py migrate then python manage.py createsuperuser`
4. Run the initial command to obtain links to all pages to scrape: `scrapy crawl sitemap from the warehouse/sitemap/spiders directory`
5. Collect the page content for each site map page: `scrapy crawl pages from the warehouse/pages/spiders directory`
6. Run command `python manage.py build_blocks` to "build the blocks" from the scraped data (page content). Run from the root directory of the project.

## TODO

- [ ] Add tests
- [ ] Refine the django admin interface
- [ ] Add a JSON API to access the data from a wagtail site for import
- [ ] and more...

## Dependencies

### Production

- [Poetry](https://python-poetry.org/) for dependency management
- [Scrapy](https://scrapy.org/) for scraping
- [Django](https://www.djangoproject.com/) for the web app
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for parsing html

### Development

- [Pre-commit](https://pre-commit.com/) for code linting
- [Black](https://black.readthedocs.io/en/stable/) for code formatting
- [Flake8](https://flake8.pycqa.org/en/latest/) for code linting
- [Isort](https://pycqa.github.io/isort/) for import sorting

## License

MIT

## Credits

### Previous work I have done and where I have pulled ideas from

- <https://github.com/rkhleics/nhs-ei.scrapy-poc>
- <https://github.com/nickmoreton/wagtail-toolbox/tree/main/wagtail_toolbox/wordpress>
- <https://github.com/import-experiments/scrape-wordpress-html>
- <https://github.com/wagtail-packages/django-wordpress-import>
- <https://github.com/import-experiments/wordpress-docker>
