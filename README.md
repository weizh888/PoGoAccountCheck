# PoGoAccountCheck
PoGoAccountCheck is a python script which reads PTC accounts from a file and checks if they are banned. If they __are__ banned, the program will save them to a file, banned.txt.

# Installation
To Install PoGoAccountCheck run:

	git clone https://github.com/sebastienvercammen/PoGoAccountCheck.git

Then:

	cd PoGoAccountCheck

After you are in the directory, make sure to install all the requirements by running:

	pip install -r requirements.txt

# Usage

To use the program run the following command:

	python banned.py -f accounts.csv

Where accounts.csv is the file of accounts to check. See "Formatting" to see how the file should be formatted.

You can also use an additional -l argument which allows you to specify your own location for the program to use.
ie:

	python banned.py -f accounts.csv -l "40.7127837 -74.005941"


The -hk argument is also required ever since API 0.45 has stopped working.
ie.

	python banned.py -f accounts.csv -l "40.7127837 -74.005941" -hk your_hash_key




# Formatting
Your file of accounts should be structured as follows:

	ptc,username1,password1
	ptc,username2,password2
	google,username3,password3

# Output
The program will display a message in the terminal if the account is banned. Additionally, it will output all banned accounts to a new file named banned.txt, all accounts that failed login to failed.txt, and all working accounts to working.csv.
