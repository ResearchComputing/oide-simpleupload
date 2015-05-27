import os

APP_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

APP_SPECIFICATION = {
    'APP_DESCRIPTION': {
        'name': 'Upload',
        'link': '/#/supl',
        'description': 'Simple HTTP Upload'
    },
    'NG_MODULE_NAME': 'supl',
    'NG_MODULE_STYLESHEETS': (
        'supl.css',
    ),
    'NG_MODULE_SCRIPTS': (
        'bower_components/es5-shim/es5-shim.min.js',
        'bower_components/angular-file-upload/angular-file-upload.min.js',
        'supl.js',
    ),
}

PYRO_UPLDMODULE_URI = 'upld.userd.%(username)s'

POST_AUTH_COMMANDS = (
    "(python -m oidesupl.oideupld &)",
)
