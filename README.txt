1. cd into the application home directory
2. run "python manage.py syncdb"
3. When the following message is displayed:

	"You just installed Django's auth system, which means you don't have any superusers defined.
	Would you like to create one now? (yes/no)"

Write "yes" and create it with the following data:
	
	Username: toolshare.team.d@gmail.com
	Email address: toolshare.team.d@gmail.com
	Password: teamd

4. If you're on windows and you don't have it already, download the sqlite3 command line tool from http://www.sqlite.org/download.html.
   Be sure you pick the right version for your environment. Look for this one if you're on Windows:
   sqlite-shell-win32-x86-3080100.zip

5. run this:

	(your sqlite3 download directory)/sqlite3 toolshare.db < doc/inserts.sql

6. Create a schedule task with the file changestatus.py

Linux instructions:

Open the setup.sh file in the toolshare directory and modify the first line.
You should put your toolshare directory in the placeholder: (your toolshare directory).

Open your crontab file for editing running this command:
	
	crontab -e
	
Add this task to the crontab file:
	
	* * * * * (your toolshare directory)/setup.sh

Windows instructions:

Open the setup.bat file in the toolshare directory and modify the first line.
You should put your toolshare directory in the placeholder: (your toolshare directory).

Run the following on the command prompt:
	
	schtasks /Create /SC DAILY /MO 1 /ST 23:59 /TN ChangeStatusTask /TR "(your toolshare directory)\setup.bat"
	
Note: To delete the task on Windows:
	
	schtasks /Delete /tn ChangeStatusTask


