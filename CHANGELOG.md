## v0.1.2 (2022-01-12)

### Fix

- **forced_update**: fixing a forced update because I made a mistake lol
- **__main__.py**: moved api code into __main__.py
- **poetry.lock**: updated poetry lock file
- **pysign**: changed repo name in order to upload to pypi

## v0.1.1 (2022-01-11)

### Refactor

- **pysign**: preparing pysign for packaging

## v0.1.0 (2022-01-11)

### Fix

- **api.py**: added unique port for anki integration and to avoid conflict with other services
- **.gitignore**: include python files after making the move from coco to py
- **remote.py**: working through some issues with errors found from the python lsp
- **__main__-.coco**: weird thing but I guess I had a space in the .coco file

### Feat

- **api.py**: rewrote api using quart as a mimicked api
- **api.py**: added video fetch
- **api**: tweaking api for better readability and integration with flask
- **json**: moving project in a new direction towards a restful api
- **anki.py**: used ankiconnect to integrate anki into the module
- **pysign**: massive cleanup of the source code after moving from coconut to python
- **pysign/*.py**: converted coco to py
- ***.coco**: rename coco to py
- **remote.coco**: added more specific logic behind scraping for table values
- **remote.coco**: started flesching out remote file to pull from signingsavvy.com
- **db.coco**: turned all table structures into class equivalents
- **db.coco**: shifting sqlalchemy constructions for migration to 2.0 release
- **db,start**: refactored a lot of code as well as rewriting some code as I added more structure
- **github**: github integration and ci
- **api**: some project set up as well as refactoring and database/api work
- **tests**: added pytest testing
- **github**: github integration and ci
- **stuff**: this is a bad commit because riley just got here lol
- **module**: implemented module-like structure with additional support for customization of variants and videos
- **init**: initial commit

### Refactor

- **db.coco**: remove useless uri table
- **db.coco**: prefixed word attributes with word_
- **tests**: refactored my test
- ***.coco**: using coconut and did some refactoring but committing now so that i can switch over to work on the database some more

### Perf

- **html/videos**: added html and mp4 files to .gitignore
