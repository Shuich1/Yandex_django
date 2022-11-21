"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

include(
    'components/common.py',
    'components/database.py',
    'components/internationalization.py',
    'components/static_files.py',
)
