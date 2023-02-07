# CK2-history-extractor

This is a python script for extracting history about your characters from Crusader Kings 2, their titles and other misc info from save files into easily readable .html files.

## Usage

1. Ensure you have python3 installed
2. If you plan on using the full version install the [ClauseWizard](https://github.com/Shadark/ClauseWizard) library for python
3. Download the entire repository
4. Decompress the savefile if it's compressed
5. Run the version of the script you want to use
6. Follow the prompts

### Differences between the versions

Lite version of the script extracts less information and will work with the default python libraries. Good if you can't be bothered to wait or install necessary library to make the normal script work.
The normal one is slower, generally more reliable and extracts more information out of your savefile. Installation of  library is necessary to make the normal version work.

## Known Problems

Generally speaking there are going to be some small issues with the data that my program extracts. For example names might be different,missing entirely or it might not be able to extract everyting about a certain title. Those are minor bugs that despite my best efforts I couldn't eliminate. CK2 savefiles are very messy by their nature and as such some data about a certain title might be stored in a different way for seemingly no reason. When that occurs my script might simply return NA or unknown in a certain category. Perfect example of this is religion and culture of characters. My oldest dynasty member used to be a unreformed hellenic pagan. After reformation, data about his religion seems to be gone entirely out of the savefile. Why? idk, how ck2 still manages to display ingame his religion? idk.

## Other similar tools

- [CK2GED](https://github.com/faiuwle/CK2GED) is a tool for creating a GED file from your CK2 savefile
- [CK3-history-extractor](https://github.com/TCA166/CK3-history-extractor) is a tool like this for CK3

## Development Status

With CK3 now being out I will not add any new content to this tool, unless there is serious demand.  
Please check out my ck3 tool for all your chronicling needs.

## License

[![CCimg](https://i.creativecommons.org/l/by/4.0/88x31.png)](http://creativecommons.org/licenses/by/4.0/)  
This work (.py and .html files) is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).  
