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
</ul>

This script alongside the main game chronicle and [CK2GED](https://github.com/faiuwle/CK2GED) can easily immortalize characters from your campaigns.
It works with mods, but save games from older versions might cause trouble.
