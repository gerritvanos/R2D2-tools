# R2D2-tools
tools for R2D2 project note: this might not be in line with the R2D2 style guide
This script is made for personal use to verify or chceck the commits you've made. 
The use is at own risk and i strongly reccomend checking the links once in a wile.

# Compatibility:
At this point the "get commits.py" script will only work on windows due to some system calls, this might get fixed later.


# Dependencies:
- atleaste python 3.6 or higher
- gitpython library 

# How to use it:
- install gitpython if you don't have it already.
- Run the script either from commandline `python "get commits.py"`, or via pycharm.
- when promted type your author name*
- give a file name to which you want your commit information to be written.
- specify if you want to get commit information for [wiki,libraries,modules,other, or 1 repo]
- specify the date from wich you want to get commits in the following format MM-DD-YYYY or type all to get all commits.
- specify the date until** wich you want to get commits in the following format MM-DD-YYYY or type all to get all commits.
- if you chose 1 repo now specify the repo name.
- the script will now run and output the information to the screen and the .csv file created in the same folder the script is located.
- the .csv file can now be opened with excel and all commits will be visible. 
- **note:** the wiki commits have 2 links, 1 to the compare and 1 to how the page looked at that point. <br>
The compare links show the progress made in that commit just like a normal repo.

* I've noticed the author name is not always the same, try your username first this usualy gets the most results. <br>
If you are not sure first type `git log` in a repo you know you've made commits and check your name in the output.
** note if you input 04-29-2019 the commits on 04-29 are not visible you need to enter 04-30-2019 to see commits for 04-29