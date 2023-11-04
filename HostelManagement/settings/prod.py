from .base import *

DEBUG = True


ALLOWED_HOSTS = ["hostelcomplaintsmanagementsystem.onrender.com", "127.0.0.1"]

# Whitenoise settings for static files in production 
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
