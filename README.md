# CK2-history-extractor

This is a python script for extracting history about your characters from Crusader Kings 2, their titles and other misc info from save files into easily readable .html files.

For each player in a save file it creates a folder that contains .html files, with the main one being "Player history.html", that contains links to other html files.
It essentialy creates this sort of a wikipedia for your save file.

There are two versions of the program available: Lite and normal.
Lite version of the script extracts less information and will work with the default python libraries. Good if you can't be bothered to wait or install necessary library to make the normal script work.
The normal one is slower, generally more reliable and extracts more information out of your savefile. Installation of [ClauseWizard](https://github.com/Shadark/ClauseWizard) library is necessary to make the normal version work.

Lite version of the script takes aproximately 120 seconds to extract data out of my 400 year long campaign save file. The normal version takes about 600 seconds to do the same thing, but extracts more titles from the savefile.

Requirements:
<ul> 
  <li>Python 3</li>
  <li>ClauseWizard (if you want to run the normal script)</li>
  <li>Decompressed ck2 save file</li>
</ul>

This script alongside the main game chronicle and [CK2GED](https://github.com/faiuwle/CK2GED) can easily immortalize characters from your campaigns.
It works with mods, but save games from older versions might cause trouble.

Instructions:
<ul> 
  <li>Install python</li>
  <li>Download the repo</li>
  <li>Put the repo in the directory of your choosing</li>
  <li>Decompress a ck2 savefile of your choosing and put the decompressed version next to the script</li>
  <li>If you want to run the normal version install ClauseWizard using pip</li>
  <li>Run the script version of your choosing</li>
  <li>Follow the prompts</li>
</ul>

Known problems:<br>
Generally speaking there are going to be some small issues with the data that my program extracts. For example names might be different,missing entirely or it might not be able to extract everyting about a certain title. Those are minor bugs that despite my best efforts I couldn't eliminate. CK2 savefiles are very messy by their nature and as such some data about a certain title might be stored in a different way for seemingly no reason. When that occurs my script might simply return NA or unknown in a certain category. Perfect example of this is religion and culture of characters. My oldest dynasty member used to be a unreformed hellenic pagan. After reformation, data about his religion seems to be gone entirely out of the savefile. Why? idk, how ck2 still manages to display ingame his religion? idk.
<br>
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
