# Installing CNTK w/ Demo Model on Azure Web Apps

[Demo](http://cntkwebappik.azurewebsites.net)

![Demo](readme_example.JPG)

## A - Prerequisites

1. Create a folder that will contain the data for your web-app and download all of the contents of this repo into it:
	```
	mkdir <YourWebAppFolderName>
	```

2. Go to https://github.com/Microsoft/CNTK/releases and download the latest version of the Windows CPU-only CNTK, which for me is "CNTK for Windows v.2.0 Beta 11 CPU only", rename this to "cntk.zip" and put this at the root of your directory

3. Go to http://www.lfd.uci.edu/~gohlke/pythonlibs/ and download the following python-wheels (assuming latest Python is v3.5 x64, adjust accordingly):
	```
	numpy-1.12.0+mkl-cp35-cp35m-win_amd64.whl
	Pillow-4.0.0-cp35-cp35m-win_amd64.whl
	scipy-0.19.0rc2-cp35-cp35m-win_amd64.whl
	```

	Put these into the "Wheels" folder, if you require additional wheels don't forget to also add them to "requirements.txt" at the root of the directory

4. At the end of this step you should have:
	```
	<YourWebAppFolderName>
	- logs
	-- init.txt
	- Model
	-- ResNet_18.model
	-- synset-1k.txt
	- Wheels
	-- init.txt
	-- numpy-1.12.0+mkl-cp35-cp35m-win_amd64.whl
	-- Pillow-4.0.0-cp35-cp35m-win_amd64.whl
	-- scipy-0.19.0rc2-cp35-cp35m-win_amd64.whl	
	- WebApp
	-- __init__.py
	-- model.py
	-- templates
	--- index.html
	- cntk.zip
	- .deployment
	- deploy.cmd
	- README.md
	- requirements.txt
	- runserver.py
	- web.xml
	```

## B - Create & Configure Web-App

1. Create a web-app and setup the git-credentials by running the following Azure CLI commands (or by using Azure Portal):
	```
	cd <YourWebAppFolderName>
	azure login
	azure account list
	azure account set <Subscription ID to become default>
	azure config mode asm
	azure site create --git <yourWebAppSiteName>
	```

	If you don't already have a git user-name configured for Azure then you will need to go to the "Deployment Credentials" blade to setup your credentials on Azure Portal.

2. Navigate to your web-app on Azure Portal and click on the "Scale up (App Service plan)" blade and select "S1" (or more powerful if needed, however S1 is the minimum for this guide)

3. Scroll down to the "Extensions" blade, click on "Add" and locate the latest version of Python, which for me is "Python 3.5.3 x64" and add it.

4. (Optional) Under the "Application settings" blade set "Always On" to "On"

## C - Deploy Demo

1. (Optional) Assuming you have used Python 3.5 (x64) and CNTK v2.0 Beta 11 you don't have to change anything in the deployment script. However if you are using Python 3.6 or CNTK v2.0 Beta 12+ then alter the below in the "deploy.cmd" script:
	```
	:: Adjust these
	SET PYTHON_RUNTIME=python-3.5
	SET PYTHON_VER=3.5
	SET CNTK_WHEEL=cntk-2.0.beta11.0-cp35-cp35m-win_amd64.whl
	SET PYTHON_EXE=%SYSTEMDRIVE%\home\Python35\python.exe
	:: Adjust these
	``` 

2. Deploy this demo by running:
	```
	cd <YourWebAppFolderName>
	git add -A
	git commit -m "init"
	git push azure master
	```

3. You should now be able to navigate to your web-app address and upload a photo that will be classified accroding to the CNN: ResNet-18

4. To modify this for your own needs, alter the "model.py" script as desired in the folder "WebApp", along with the HTMl template, "index.html" in "templates" and then push your changes to the repo:
	```
	git add -A
	git commit -m "modified some script"
	git push azure master
	```