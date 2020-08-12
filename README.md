# computational-chemistry-toolbox

## generate executable output reader UI
generate .exe file with the below command in the directory with this repo
> pip install pyinstaller

*(deliberately excluded from spec_file.txt, many installations likely to not use it)*

> pyinstaller --onefile GaussianOutputReader.py

### Dependencies
Use the below command to generate a working environment:
> conda create --name --file spec-file.txt

The spec file can be found in the *other* directory.

### Credits and Licensing
Developer: Himaghna Bhattacharjee, Vlachos Research Lab. (www.linkedin.com/in/himaghna-bhattacharjee)

Developer: Jackson Burns, Don Watson Lab. ([Personal Site](https://www.jacksonwarnerburns.com/)) 

### TODO
- @JacksonBurns add custom icon to executable and tk window
