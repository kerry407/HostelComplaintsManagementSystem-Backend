from .base import *

DEBUG = True


ALLOWED_HOSTS = ["hostelcomplaintsmanagementsystem.onrender.com"]

# Whitenoise settings for static files in production 
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
