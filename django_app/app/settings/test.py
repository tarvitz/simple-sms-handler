from .dist import *


import warnings
warnings.filterwarnings(
    'error', r"DateTimeField .* received a naive datetime",
    RuntimeWarning, r'django\.db\.models\.fields')

DEBUG = True

# internal apps
MIGRATION_MODULES = {
    app: "apps.%s.migrations_not_used_in_tests" % app
    for app in ["sms", ]
}
# django apps
MIGRATION_MODULES.update({
    app: "django.contrib.%s.migrations_not_used_in_tests" % app
    for app in ["sites", "admin", "auth", "contenttypes", "sessions"]
})
