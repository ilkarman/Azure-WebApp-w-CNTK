import os
# CNTK path
os.environ['PATH'] = r'D:\home\site\wwwroot\cntk\cntk;' + os.environ['PATH']
import cntk
import pkg_resources
from flask import render_template
from WebApp import app

@app.route("/")
def index():
    message = "Hello World!"
    return render_template('index.html', **locals())
    
@app.route("/cntk")
def cntk_ver():
    message = "CNTK version: {}".format(pkg_resources.get_distribution("cntk").version)
    return render_template('index.html', **locals())