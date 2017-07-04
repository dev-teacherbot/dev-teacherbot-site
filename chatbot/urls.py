from django.conf.urls import include, url
from chatbot import views
from django.contrib import admin


## The naming conventions here could definitely be improved
urlpatterns = [
	url(r'^(?P<cbot_id>[0-9]+)/$', views.cbot_management, name='cbot_manage'),
	url(r'^$', views.index, name='index'),
	url(r'^index/', views.index, name='index'),

	#Chatbot Forms
	url(r'^add/', views.add, name='add_chatbot'),
	url(r'^(?P<cbot_id>[0-9]+)/edit/$', views.edit, name='edit_chatbot'),
    url(r'^choose_bot/$', views.chatbot_to_twitterbot, name='chatbot_to_twitterbot'),
    url(r'^add_twitterbot/', views.add_twitterbot, name='add_twitterbot'),
	
	# Static pages
	url(r'^twitter-guide/$', views.twitter_guide, name='twitter_guide'),
	url(r'^pandora-guide/$', views.pandora_guide, name='pandora_guide'),
	url(r'^playground-guide/$', views.playground_guide, name='playground_guide'),
	url(r'^first-setup-guide/$', views.first_setup_guide, name='first_setup_guide'),
	url(r'^get-started/$', views.get_started, name='get_started'),
    url(r'^bot-hub/$', views.bot_hub, name='bot_hub'),
    
	# File Manager 
	url(r'^file-manager/$', views.file_manager, name='file_manager'),
	url(r'^(?P<file_id>[0-9]+)/file-delete/$', views.file_delete, name='file_delete'),
	url(r'^file-manager/file-delete-all/$', views.file_delete_all, name='file_delete'),

	# File Pages
	url(r'^add-file/$', views.file_add_new, name='file_add_new'),

	# Twitter Actions
	url(r'^(?P<cbot_id>[0-9]+)/twit-check/$', views.check_twitter_auth, name='twit_check'),
    
    # AIML Wizard
    url(r'^aiml_wizard/$', views.aiml_wizard, name='aiml_wizard'),
    
	# Internal Actions 
	url(r'^(?P<cbot_id>[0-9]+)/bot-enabled/$', views.chatbot_activate_toggle, name='chatbot_toggle'),
	url(r'^(?P<cbot_id>[0-9]+)/get-chatlog/$', views.chatbot_get_chatlog, name='chatbot_get_chatlog'),
	url(r'^(?P<cbot_id>[0-9]+)/add-setup/(?P<setup_id>[0-9]+)/$', views.chatbot_add_setup, name='add_setup_to_chatbot'),
	url(r'^(?P<cbot_id>[0-9]+)/remove-setup/(?P<setup_id>[0-9]+)/$', views.chatbot_remove_setup, name='remove_setup_from_chatbot'),

	# Pandora API actions
	url(r'^(?P<cbot_id>[0-9]+)/pa-create/$', views.create_pandora_bot, name='pa_create'), 
	url(r'^(?P<cbot_id>[0-9]+)/pa-download/$', views.download_pandora_bot, name='pa_download'),
	url(r'^(?P<cbot_id>[0-9]+)/pa-compile/$', views.compile_pandora_bot, name='pa_compile'),
	url(r'^(?P<cbot_id>[0-9]+)/pa-talk/$', views.talk_pandora_bot, name='pa_talk'),
	url(r'^(?P<cbot_id>[0-9]+)/pa-list/$', views.file_list_pandora_bot, name='pa_list'),
	url(r'^(?P<cbot_id>[0-9]+)/pa-archive/$', views.pandora_archive, name='panda-test'),
	url(r'^(?P<cbot_id>[0-9]+)/pa-delete/$', views.delete_pandora_file, name='panda-delete'),
	url(r'^(?P<cbot_id>[0-9]+)/pa-delete-all/$', views.delete_all_pandora_file, name='panda-delete-all'),
	url(r'^(?P<cbot_id>[0-9]+)/pa-upload/$', views.upload_pandora_config, name='panda-upload'),
]