import os
import sys
import site

VIRTUAL_ENV_PATH = os.path.abspath(os.path.join(
	__file__, '..', '..', '..', 'env', 'lib', 'python2.6', 'site-packages'))

# Add virtualenv
site.addsitedir(VIRTUAL_ENV_PATH)

# Add project path.
project_path = os.path.abspath(os.path.join(__file__, '..', '..'))
if project_path not in sys.path:
    sys.path.append(project_path)

# Add local apps path.
apps_path = os.path.abspath(os.path.join(__file__, '..', '..', 'sapling'))
if apps_path not in sys.path:
    sys.path.append(apps_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'sapling.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
