# EbscoPackageScraper
Scrapes EBSCO Holdings Management site looking for fuzzy matching package names

This tool works by retrieving a list of package names (in my case from SerialsSolutions) and then opening the EBSCO Holdings Management tool.

It then checks for the package names and uses fuzzy matching to report back any matches that are 80% or better.

The input list should be like this:

DatabaseCode,DatabaseName,DatabaseVendor
I4X,Gothenburg University Publications Electronic Archive (GUPEA),Gothenburg University Library
BVY,GPO Monthly Catalog,OCLC
QZ5,Graphic Novels Core Collection (H.W. Wilson),EBSCOhost
EP7,Griffith University DSpace,Griffith University
MG7,Handbook of Latin American Studies (HLAS Web),Library of Congress
BWP,HarpWeek,Harpweek
I59,Harvard University Library DASH,Harvard University
J3O,HathiTrust (Public Domain within US only),HathiTrust
IGY,Health & Psychosocial Instruments (HAPI),EBSCOhost
7T2,Health and Safety Science Abstracts (Full archive),ProQuest
FTE,Historical Abstracts (EBSCO),EBSCOhost
BYJ,Historical Statistics of the United States,Cambridge University Press
MUTSD,History of Black Achievement in America,"Ambrose Video Publishing, Inc."
UW7,"History of Science, Technology and Medicine",EBSCOhost

Libraries used are:
BeautifulSoup
urllib
tk
codecs
time
requess
re
fuzzywuzzy

Please note that in searching, I exclude any of the most commonly used English words from this site:
http://www.ef.edu/english-resources/english-vocabulary/top-1000-words/

I also only search approximatley the first 3 words of the package name

I also replace out the following characters:
':','-','&',',',')','('

Finally, the script expects a userNamePassword.txt file in the same directory as the script that has only the username on the first line and the password on the second.
eg:

username
password

