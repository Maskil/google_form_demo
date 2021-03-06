# Thank you for using Form Filler!
Thank you for downloading Form Filler and I hope you have a good time using it.
Since this program is all coded by Python but mainly tested on a Windows device, running on Linux or mobile devices is not recommended.<br>Check [Privacy Policies](#privacy-policies) if you are concerned about your datas.<br>Check [How to use it](#how-to-use-it) if you are ready!<br></brCheck>Check [FAQ](#faq) if you are confused. <br> Check [Cautions](#cautions) to check cautions.<br>**Note: FAQ in this page is only for initializing the evironment and will not be updated. New and more detailed FAQs will be uploaded on GitHub.**<br/><br/>

# Privacy Policies
All your responses will **only** be saved **locally** . You can always check your data in the txt files saved in the folder.  <br/><br/>

# How to use it
## #1 Step: Setup Python. 
1. Install Python from [here](https://www.python.org/downloads/). Make sure the Python version is above **3.8**. Duing the installation, make sure to check the box for Python being in PATH.
2. module pip should be in your system's PATH, you can type pip(Windows) or pip3(Mac OS) in cmd(Windows) or Terminal(Mac OS) to check.
```
// an example for Mac users
someone'sMacBook:~ username$ pip3
Usage:
	pip3 <command> [options]
Commands:
	etc...
```
- #### For Windows
```
pip install bs4
pip install lxml
pip install selenium
```

- #### For Mac
```
pip3 install bs4
pip3 install lxml
pip3 install selenium
```

## #2 Step: Setup chromedriver
1. Install Chrome from [here](https://www.google.com/chrome/?brand=CHBD&brand=SZLF&gclid=Cj0KCQiA7NKBBhDBARIsAHbXCB6VQeMaSJShxbmZNnXguG7wwkxQgbd_ZItio2ECsqL4e46A0NwwX7AaAmb4EALw_wcB&gclsrc=aw.ds). In Chrome, go to `Settings -> About Chrome` and check the Chrome version *(Ex: 88)*. 
2. Install chromedriver from [here](https://chromedriver.chromium.org/downloads). Make sure to download the chromedriver accordingly to your Chrome version. Since the program requires the location of the chromedriver, please be aware where the chromedriver is.
## #3 Step: Run the script
1. Note: There are various ways to run a Python script. The method below is just an example.
2. Open `formfiller.py` by `IDLE`. Noting that `IDLE` is a basic IDE automatically installed while installing Python. The script of the `formfiller.py` should be readable.
3. Press F5 from the keyboard button to run the script.
After successfully running the script, there will be a few more instructions inside the program. If you meet any issue not listed in [FAQ](#faq), please contact the author by [email](#about-the-author) so the problem can be fixed ASAP. <br>
4. There are many alternative ways to open a python file. Google if you are confused. **Make sure the python file is in a independent folder because it will create some other files to save your responses!**<br/><br/>

# Cautions
**Sometimes the program will ask you to type your chromedriver location even after you could successfully start the form-filling process. In such cases, simply restart the program and it will be fine.**
## Input two information at the same time
![Screenshot 2021-03-06 230627](https://user-images.githubusercontent.com/45069462/110209561-9d29ed00-7ed0-11eb-82fb-5b4de8489c92.png)
If you type the nickname and the URL address of the form at the same time, you will be creating a new response even if the nickname is already saved. In other words, typing the nickname and URL the same times always creating a new response.
## Nickname rule
Users cannot use name `tmp`.
## Make Chrome visible
Delete the line  `option.add_argument("-headless")`.<br>


# FAQ
## Q: I messed up with the first three steps!
- ### A: Use Google.
## Q: I'm using Windows and the chromedriver location does not work!
- ### A: For Windows, you need to put `.exe` at the end of the chromedriver file. For instance, `C:\user\Downloads\chromedriver\chromedriver.exe`<br/>For Mac or Linux, `.formatname` is not required.<br/><br/>

# About the Author
### email: hg5180028@hiroogakuen.com or makigo613@gmail.com
### 
