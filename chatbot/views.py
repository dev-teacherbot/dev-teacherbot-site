from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from chatbot.models import  pandora_settings, cbot, aiml_config, aiml_file
from chatbot.forms import chatbot_form, twitterbot_form 
import chatbot.script.pandora_actions as pa
# -*- coding: utf-8 -*-
from chatbot.script.process_manager import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.messages import constants as messages
import os.path



################################################################
###################### CHATBOT PAGES ###########################

@login_required
def bot_hub(request):
    """ Display the bots owned by the viewing user """
    context = RequestContext(request)
    context['chatbots'] = cbot.chatbot_manager.user(request)
    context['twitterbots'] = cbot.twitterbot_manager.get_twitter_capable(request)
    return render_to_response('bot_hub.html', context)

@login_required
def add(request):
    """ Create a new chatbot """
    if request.method == 'POST':
        form = chatbot_form(request.POST)
        if form.is_valid():
            cbot = form.save(commit=False)
            cbot.author = request.user
            cbot.save()
            form.save_m2m()
            return HttpResponseRedirect('/')
    else:
        form = chatbot_form()
    return render(request, 'cbotforms/add_chatbot.html', {'form': form})

@login_required
def chatbot_to_twitterbot(request):
    """ Display chatbots to transform into twitterbot """
    context = RequestContext(request)
    context['chatbots'] = cbot.chatbot_manager.user(request)
    return render_to_response('chatbot_to_twitterbot.html', context)
    
    
@login_required
def add_twitterbot(request, cbot_id):
    """ Chatbot settings edit """
    chatbot = get_object_or_404(cbot, id=cbot_id)
    if request.method == "POST":
        form = twitterbot_form(request.POST, instance=chatbot, initial={'twit_capable': True})
        if form.is_valid():
            form.author = request.user
            chatbot = form.save(commit=False)
            chatbot.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('bot_hub'))
        else:
            return HttpResponse("Sorry - there was an error the system could not handle.")
            #messages.error(request, "Error")
    else:
        form = twitterbot_form(instance=chatbot, initial={'twit_capable': True})
    return render(request, 'cbotforms/add_twitterbot.html', {'form': form, 'chatbot_id' : cbot_id })

@login_required
def edit(request, cbot_id):
    """ Chatbot settings edit """
    chatbot = get_object_or_404(cbot, id=cbot_id)
    if request.method == "POST":
        form = chatbot_form(request.POST, instance=chatbot)
        if form.is_valid():
            form.author = request.user
            chatbot = form.save(commit=False)
            chatbot.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('bot_hub'))
        else:
            return HttpResponse("Sorry - there was an error the system could not handle.")
            #messages.error(request, "Error")
    else:
        form = chatbot_form(instance=chatbot)
    return render(request, 'cbotforms/edit_chatbot.html', {'form': form, 'chatbot_id' : cbot_id })

@login_required
def cbot_management(request, cbot_id):
    """ Displays the information page for a single chatbot """
    context = {'chatbot' : cbot.chatbot_manager.get(pk=cbot_id),
               'pandora' : pa,
               'aiml_configs' : aiml_config.config_manager.user(request)}
    return render(request, 'chatbot_management.html', context)

def tbot_management(request, cbot_id):
    """ Displays the information page for a twitterbot """
    context = {'twitterbot' : cbot.twitterbot_manager.get(pk=cbot_id),
               'pandora'    : pa,
               'aiml_configs' : aimml_config.config_manager.user(request)}
    return render(request, 'twitterbot_management.html', context)

@login_required
def chatbot_add_setup(request, cbot_id, setup_id):
    """ Add a setup to the specified chatbot and redirect to next page up tree """
    chatbot = cbot.chatbot_manager.get(id=cbot_id)
    setup = aiml_config.config_manager.get(id=setup_id)
    chatbot.aiml_config.add(setup)
    return HttpResponseRedirect(reverse('cbot_manage', args=[cbot_id]))  

@login_required
def chatbot_remove_setup(request, cbot_id, setup_id):
    """ Removes a setup to the specified chatbot and redirect to next page up tree """
    chatbot = cbot.chatbot_manager.get(id=cbot_id)
    setup = aiml_config.config_manager.get(id=setup_id)
    chatbot.aiml_config.remove(setup)
    return HttpResponseRedirect(reverse('cbot_manage', args=[cbot_id]))



################################################################
###################### Pandora Actions #########################
### These views are referenced via an ajax call from specific templates

@login_required
def pandora_archive(request, cbot_id):
    """ Upload an archive file; normally accessed indirectly """
    pa_name = cbot.bot_manager.get(pk=cbot_id).pandora_name
    if request.method == 'POST':
        form = PandoraUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pa.upload_archive(pa_name, request.FILES['archivefile'])
            return HttpResponseRedirect('/chatbot/' + cbot_id)      ### Not correct
    else:
        form = PandoraUploadForm()
    return render(request, 'pandora_management.html', {'form': form})


def upload_pandora_config(request, cbot_id):
    """ Upload the attached aiml configurations from the internal Setup database """
    try:
        
        pa_name = cbot.bot_manager.get(pk=cbot_id).pandora_name
        configurations = cbot.bot_manager.get(pk=cbot_id).get_attached_configurations()
        file_list = []
        for n in configurations:
            file_list = file_list + [n.get_file_paths()]
        file_list = [i for inner in file_list for i in inner]
        if not file_list:
            return HttpResponse("No files were found")
        
        response = pa.pandora_upload_files_from_path(pa_name, file_list)
        return HttpResponse(response)
    except Exception, error:
        return HttpResponse("Error: " + str(error))

@login_required
def create_pandora_bot(request, cbot_id):
    """ Creates or compiles a pandorabot using the currently specified name """
    pa_name = cbot.bot_manager.get(pk=cbot_id).pandora_name
    return HttpResponse(pa.create_bot(pa_name))

@login_required
def download_pandora_bot(request, cbot_id):
    """ Downloads a copy of the files on pandora to a directory and outputs a link """
    pa_name = cbot.bot_manager.get(pk=cbot_id).pandora_name
    return HttpResponse(pa.pandora_download(pa_name))

@login_required
def file_list_pandora_bot(request, cbot_id):
    """ Returns a list of the current files for a specific bot on pandora """
    pa_name = cbot.bot_manager.get(pk=cbot_id).pandora_name
    return HttpResponse(pa.pandora_list_files_short(pa_name))

@login_required
def talk_pandora_bot(request, cbot_id):
    """ Query the pandora bot """
    pa_name = cbot.bot_manager.get(pk=cbot_id).pandora_name
    context_instance=RequestContext(request)
    if request.method == 'POST':
        return HttpResponse( pa.pandora_talkto_bot(pa_name, request.POST['askbot']) )
    return HttpResponse("A query was not correctly sent to the chatbot")

@login_required
def delete_pandora_file(request, cbot_id):
    """ Delete a specific file on the pandora bots system """
    pa_name = cbot.bot_manager.get(pk=cbot_id).pandora_name
    if request.method == 'POST':
        response = pa.pandora_delete_file(pa_name, request.POST['filename'])
        return HttpResponse( response ) ### Name of post variable required
    return HttpResponse("We weren't able to retrieve a file instance.")

@login_required
def delete_all_pandora_file(request, cbot_id):
    """ Delete a specific file on the pandora bots system """
    pa_name = cbot.bot_manager.get(pk=cbot_id).pandora_name
    response = pa.pandora_delete_all_files(pa_name)
    return HttpResponse(response)


@login_required
def compile_pandora_bot(request, cbot_id):
    """ Additional compilation method """
    pa_name = cbot.bot_manager.get(pk=cbot_id).pandora_name
    response = pa.pandora_compile_bot(pa_name)
    return HttpResponse(response)

################################################################
###################### Internal Actions ########################

@login_required
def chatbot_activate_toggle(request, cbot_id):
    """ Toggles the "Enabled" state of chatbot, i.e whether it should be run with cron """
    try:
        chatbot = cbot.twitterbot_manager.get(pk=cbot_id)
        chatbot.enabled = not cbot.twitterbot_manager.get(pk=cbot_id).enabled
        chatbot.save()
        active = cbot.twitterbot_manager.get(pk=cbot_id).enabled
        if active:
            response = "activated"
        else:
            response = "deactivated"
        # And we'll compile here also, just to reduce the onus of responsibility on the user
        pa_name = cbot.twitterbot_manager.get(pk=cbot_id).pandora_name
        pa.pandora_compile_bot(pa_name)
        return HttpResponse("Chatbot has been " + response)
    except Exception, e:
        return HttpResponse("The system was unable to toggle bot activity; please contact a system administrator with these details: " + str(e))

@login_required 
def chatbot_get_chatlog(request, cbot_id):
    try:
        file_location = os.path.join(os.path.dirname(__file__),"script", "chatlogs" , cbot_id,'queriestobot.txt')
        queryfile = open(file_location)
        lines = queryfile.read().replace('\n','<br />')
        return HttpResponse( str( lines) ) 
    except Exception, e:
        return HttpResponse("Chatlog for this bot wasn't found. Check that the chatbot has had active conversations.")


################################################################
###################### Twitter Actions #########################
### Most actions executed in subprocess

@login_required
def check_twitter_auth(request, cbot_id):
    """ Return a user readable response on whether twitter details are active """
    twitter_tk = cbot.twitterbot_manager.get(pk=cbot_id).twit_token
    twitter_tk_s = cbot.twitterbot_manager.get(pk=cbot_id).twit_token_secret
    twitter_c_k = cbot.twitterbot_manager.get(pk=cbot_id).twit_c_key
    twitter_c_s = cbot.twitterbot_manager.get(pk=cbot_id).twit_c_secret
    try:
        import tweepy
        auth = tweepy.OAuthHandler(twitter_c_k, twitter_c_s)
        auth.set_access_token(twitter_tk, twitter_tk_s)
        twitter_api = tweepy.API(auth)
        twitter_api.me()
        return HttpResponse("Success: Your twitter details are valid")
    except Exception,e:
        return HttpResponse("There was a problem; please check the twitter access details. The following may help: \n" + str(e))


################################################################
###################### File Manager ############################

@login_required
def file_manager(request):
    """ Loads the file management page for deleting/viewing files """
    userFiles =  aiml_file.file_manager.user(request)
    context = { 'aimls' : userFiles ,
                'setup_files' : aiml_config.config_manager.user(request) }
    return render(request, "filemanagement/file_manager.html", context)

@login_required
def file_delete(request, file_id):
    """ Deletes a file """
    try:
        filename = aiml_file.file_manager.get(id=file_id).get_simplename
        file = aiml_file.file_manager.filter(id=file_id).delete()
        return HttpResponse("File Deleted: " + filename)
    except Exception,e: 
        return HttpResponse("We were unable to delete the file due to an error: " + str(e))

@login_required
def file_delete_all(request):
    """ Deletes all files """
    try:
        file = aiml_file.file_manager.user(request).delete()
        return HttpResponse("All files deleted")
    except Exception,e: 
        return HttpResponse("We were unable to delete the files due to an error: " + str(e))


# Not Currently Needed as file management done through admin pages
@login_required
def file_add_new(request):
    """ Adds a new file via text entry """
    if request.method == 'POST':
        form = addFileForm(request.POST)
        if form.is_valid():
            #cbot = form.save(commit=False)
            #cbot.author = request.user
            #cbot.save()
            #form.save_m2m()
            return HttpResponseRedirect('/')
    else:
        form = addFileForm()
    return render(request, 'filemanagement/add_file.html', {'form': form})

################################################################
###################### AIML Wizard #############################
def aiml_wizard(request):
    context = RequestContext(request)
    context['aiml_configs'] = aiml_config.config_manager.user(request)
    return render_to_response('aimlwizard/aiml_wizard_home.html', context)


################################################################
###################### STATIC PAGES ############################

def index(request):
    return render(request, 'index.html')

def twitter_guide(request):
    return render(request, 'information/twitter_guide.html')

def pandora_guide(request):
    return render(request, 'information/what_is_pandora.html')

def playground_guide(request):
    return render(request, 'information/playground_editor.html')

def first_setup_guide(request):
    return render(request, 'information/teacherbot_for_dummies.html')

def get_started(request):
    return render(request, 'information/getting_started.html')

