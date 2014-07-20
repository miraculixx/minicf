# configure minimongo 
from minimongo.options import configure
import minicf.settings as settings
# LOAD MODEL CLASSES ONLY AFTER configure() has run !!
if True:
    # if True is here to stop Eclipse/Pydev from rearranging the imports
    # ***
    # CONFIGURE MUST BE RUN BEFORE LOADING MODEL CLASSES !!
    # **
    configure(module=settings, prefix='MONGODB_')
    # now load model classes
    from app import App
    from service import Service
