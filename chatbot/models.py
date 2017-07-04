# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.core.files.base import ContentFile
import os
from teacherbot.settings import MEDIA_ROOT
from .managers import cbotManager, fileManager, configManager
import random, string
from django.contrib.auth.models import User
from tinymce.models import HTMLField

## This may not be ideal for longterm
def get_upload_directory(self, filename):
        """ Return a randomized folder name as an upload location """
        foldername = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        return os.path.join('aiml_files/%s/' % foldername, filename)

class aiml_file(models.Model):
    docfile = models.FileField(upload_to=get_upload_directory)
    text_file = models.TextField(default='', blank=True, verbose_name="File Contents")
    author = models.ForeignKey(User, default=1, related_name='aiml', blank=True)
    objects = fileManager()

    def get_path(self):
        """ Return full system path """
        return os.path.join(MEDIA_ROOT, self.docfile.name)

    def __str__(self):              # __unicode__ on Python 2
        return self.docfile.name

    def is_owner(self):
        return self.author

    @property
    def get_filetype(self):
        filename, file_extension = os.path.splitext(self.get_path())
        return file_extension[1:]

    @property
    def get_simplename(self):
        """ The pathless version of the filename """
        return self.docfile.name.split('/')[-1] 
    
    class Meta:
        verbose_name = 'File'

# To do for aiml_file type - on edit, text file should transfer it's content to the docfile.






### AIML Configurations for chatbot
class aiml_config(models.Model):
    title = models.CharField(max_length=100, default='', blank=False)
    last_modified = models.DateTimeField(auto_now_add=True)
    aiml_files = models.ManyToManyField(aiml_file, blank=True,  related_name='AIML_File', verbose_name="Current Setup Files")
    is_public = models.BooleanField('Should be public?', default=False)

    author = models.ForeignKey(User, default=1, related_name='configs', blank=True)
    objects = configManager()

    def __str__(self):              # __unicode__ on Python 2
        return self.title

    @property
    def file_counts(self):
        """ Returns a count of all active attached files"""
        return self.aiml_files.count()

    def get_files(self):
        """ Returns all attached files as arrays of files """
        files = self.aiml_files.all()
        return files

    def get_file_paths(self):
        """ Create an archive of the attached files and return the OS path """
        filelist = self.get_files()
        filepaths = []
        for n in range(len(filelist)):
            filepaths = filepaths +  [filelist[n].get_path()]
        return filepaths

    class Meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'Setups'


### The base chatbot model. 
class cbot(models.Model):
    created = models.DateTimeField('Date created',auto_now_add=True)
    title = models.CharField(max_length=100, blank=False, default='')
    pandora_name = models.CharField(max_length=70, default='', unique=True)
    aiml_config = models.ManyToManyField(aiml_config,related_name='mlconfig',blank=True  ,verbose_name="Active Chatbot Setups") 
    enabled = models.BooleanField('Is enabled?', default=False)
    active_process = False
    author = models.ForeignKey(User, default=1, related_name='chatbots', blank=True)
    twit_hashtags = models.CharField(max_length=200, blank=True, default='',  verbose_name="Hashtags and Keywords")       # Placeholder 
    twit_token = models.CharField(max_length=200, blank=False, default='',  verbose_name="Twitter Access Token", help_text="Stuff")
    twit_token_secret = models.CharField(max_length=200, blank=False, default='',  verbose_name="Twitter Access Token Secret")
    twit_c_key = models.CharField(max_length=200, blank=False, default='',  verbose_name="Twitter Consumer Key")
    twit_c_secret = models.CharField(max_length=200, blank=False, default='',  verbose_name="Twitter Consumer Secret")
    

    objects = cbotManager() # Custom Manager returning bot objects
    
    #twitterBots = tbotManager() # Manager returning all twitter-enabled bots
    
    def get_attached_configurations(self):
        """ Get config objects """
        return self.aiml_config.all()

    def get_attached_config_names(self, join=True):
        """ Get config object title """
        return self.aiml_config.all().values_list('title', flat=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Chatbot Instance'
        verbose_name_plural = 'Chatbots'

def validate_only_one_instance(obj):
    """ Raise validation error if more than one is created """
    model = obj.__class__
    if (model.objects.count() > 0 and
            obj.id != model.objects.get().id):
        raise ValidationError("Can only create 1 %s instance. Please edit the already existing entry. " % model.__name__)


### Singular connection configuration for pandorabots
class pandora_settings(models.Model):
    app_id = models.CharField(max_length=1000)
    user_key = models.CharField(max_length=1000)
    host = models.CharField(max_length=1000)
    def clean(self):
        validate_only_one_instance(self)
    class Meta:
        verbose_name = 'Pandora Settings'
        verbose_name_plural = 'Pandora Settings'

