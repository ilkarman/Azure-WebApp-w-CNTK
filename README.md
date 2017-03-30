# Installing CNTK w/ Demo Model on Azure Web Apps

[Check out step-by-step YouTube](https://youtu.be/nMZ8lTo-96k)

[Demo](http://cntkwebappik.azurewebsites.net)

![Demo](readme_example.JPG)

**For this guide to work without modifications you must install the "Python 3.5.3 x64" extension** For modifications please see the section below.

![Demo](requirement.JPG)

## Replicate Demo in 7 steps

1. Create a folder that will contain the data for your web-app and download all of the contents of this repo into it:
	```
	mkdir <YourWebAppFolderName>
	```
	You should have the following structure:
	```
	<YourWebAppFolderName>
	- logs
	-- __init__.txt
	- Model
	-- ResNet_18.model
	-- synset-1k.txt
	- Wheels
	-- Pillow-4.0.0-cp35-cp35m-win_amd64.whl
	- WebApp
	-- runserver.py
	-- model.py
	-- templates
	--- index.html
	- .deployment
	- deploy.cmd
	- README.md
	- requirements.txt
	- web.config
	```

2. Create a web-app and setup the git-credentials by running the following Azure CLI **(note: this currently uses the old version v1 of Azure CLI and will soon be updated to use azure-cli v2.0)** commands (or by using Azure Portal):
	```
	cd <YourWebAppFolderName>
	azure login
	azure account list
	azure account set <Subscription ID to become default>
	azure config mode asm
	azure site create --git <yourWebAppSiteName>
	```

	If you don't already have a git user-name configured for Azure then you will need to go to the "Deployment Credentials" blade to setup your credentials on Azure Portal.

3. Navigate to your web-app on Azure Portal and click on the "Scale up (App Service plan)" blade and select "S1" (or more powerful if needed, however S1 is the minimum for this guide)

4. Scroll down to the "Extensions" blade, click on "Add", locate "Python 3.5.3 x64" and add it (*you must use this extension*)

5. (Optional) Under the "Application settings" blade set "Always On" to "On" to reduce the response time (since your model will be kept loaded)

6. Deploy this demo by running:
	```
	cd <YourWebAppFolderName>
	git add -A
	git commit -m "init"
	git push azure master
	```
7. You should now be able to navigate to your web-app address and upload a photo that will be classified according to the CNN: ResNet-18

## Advanced extensions (run your own)

1. You can include references to other modules (e.g. pandas or opencv) in your model.py file, however you must add the module to the "requirements.txt" file so that python installs the module. If the module needs to be built you can you can go to http://www.lfd.uci.edu/~gohlke/pythonlibs/ to download the pre-built wheel file (to the wheels folder). Don't forget to add the wheel path to the  "requirements.txt" file at the root of the directory. **Note: [Numpy](https://azurewebappcntk.blob.core.windows.net/wheels/numpy-1.12.1+mkl-cp35-cp35m-win_amd64.whl), [Scipy](https://azurewebappcntk.blob.core.windows.net/wheels/scipy-0.19.0-cp35-cp35m-win_amd64.whl), and [CNTK](https://azurewebappcntk.blob.core.windows.net/wheels/cntk-2.0.beta11.0-cp35-cp35m-win_amd64.whl) wheels are automatically installed inside the "deploy.cmd" script; to change this you can edit the deploy.cmd file to point to whichever numpy wheel you require**	

2. **Editing deploy.cmd** -  the install script automatically adds the binaries for [CNTK v2.0 Beta11](https://azurewebappcntk.blob.core.windows.net/cntk2beta11win/cntk.zip). However if you want to use **Python 3.6 or CNTK v2.0 Beta 12+** then alter the below in the "deploy.cmd" script:
	```
	SET PYTHON_EXE=%SYSTEMDRIVE%\home\python353x64\python.exe
	SET NUMPY_WHEEL=https://azurewebappcntk.blob.core.windows.net/wheels/numpy-1.12.1+mkl-cp35-cp35m-win_amd64.whl
	SET SCIPY_WHEEL=https://azurewebappcntk.blob.core.windows.net/wheels/scipy-0.19.0-cp35-cp35m-win_amd64.whl
	SET CNTK_WHEEL=https://azurewebappcntk.blob.core.windows.net/wheels/cntk-2.0.beta11.0-cp35-cp35m-win_amd64.whl
	SET CNTK_BIN=https://azurewebappcntk.blob.core.windows.net/cntk2beta11win/cntk.zip
	echo "Installed python extension installed here:"
	``` 
	To create the 'cntk.zip' file you just need to extract the cntk/cntk folder (i.e. the folder that contains 'CNTK.exe' and DLLs; you can remove the python sub-folder which contains the wheels) and then reference it with the %CTNK_BIN% environmental variable above (assuming you have also extracted the relevant wheel from the cntk/cntk/python first).

3. Finally, alter the "model.py" script as desired in the folder "WebApp", along with the HTMl template, "index.html" in "templates" and then push your changes to the repo:
	```
	git add -A
	git commit -m "modified some script"
	git push azure master
	```