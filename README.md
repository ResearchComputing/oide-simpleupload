# oide-simpleupload
Simple HTTP upload app for the OIDE.

**Installing OIDE Simple HTTP Upload**

The OIDE Simple HTTP Upload requires that you first install [The OIDE](https://github.com/ResearchComputing/OIDE)

Once the OIDE is installed, clone the OIDE Simple HTTP Upload repository and enter the project directory:
```
git clone https://github.com/ResearchComputing/oide-simpleupload.git
cd oide-simpleupload
```
Then, build the dependencies for the front-end components:
```
cd oidesupl
bower install
```

Now configure your local OIDE Simple HTTP Upload app settings, if they diverge from the defaults. The settings file may be modified directly, or be overridden with a `local_settings.py` file in the `oidesupl` directory:

Switch back to the project root and install the python package (a virtualenv is recommended):
```
python setup.py install
```
The OIDE, which will now include the OIDE Simple HTTP Upload app, can now be run with the following command:
```
oide
```
To use the OIDE, point your browser to `localhost:8888`.
