# CK2-history-extractor

This is a python script for extracting history about your characters from Crusader Kings 2, their titles and other misc info from save files into easily readable .html files.

For each player in a save file it creates a folder that contains .html files, with the main one being "Player history.html", that contains links to other html files.
It essentialy creates this sort of a wikipedia for your save file.

There are two versions of the program available: Lite and normal.
Lite is faster and will run with just the basic python install.
The normal one is slower and is generally more reliable but requires installation of [ClauseWizard](https://github.com/Shadark/ClauseWizard) library


<ul> Requirements:
  <li>Python 3</li>
  <li>ClauseWizard (if you want to run the normal script)</li>
  <li>Decompressed ck2 save file</li>
</ul>

This script alongside the main game chronicle and [CK2GED](https://github.com/faiuwle/CK2GED) can easily immortalize characters from your campaigns.
It works with mods, but save games from older versions might cause trouble.

<ul> Instructions:
  <li>Install python</li>
  <li>Download the repo</li>
  <li>Put the repo in the directory of your choosing</li>
  <li>Decompress a ck2 savefile of your choosing and put the decompressed version next to the script</li>
  <li>If you want to run the normal version install ClauseWizard using pip</li>
  <li>Run the script version of your choosing</li>
  <li>Follow the prompts</li>
</ul>
