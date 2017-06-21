# Memory File Extractor
Memory File Extractor extracts specific file in Memory dumped files.

* Python 2.7
* All Platform (Windows, Linux, Unix, OSX)

## Usage
```
-h, --help       show this help message and exit
-p, --pdf        Extract PDF file
-i, --image      Extract image file (jpg, gif, png)
-d, --directory  Select_directory
```

*ex)<br>
python extract_tool.py -i (memory.dump)<br>
python extract_tool.py -i -d (memory_dump_directory)*