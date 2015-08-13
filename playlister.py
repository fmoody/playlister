#!./bin/python

import httplib2
import os
import sys

#TODO: REMOVE
import pprint
#TODO: REMOVE

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the {{ Cloud Console }}
{{ https://cloud.google.com/console }}

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def main():

    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    message=MISSING_CLIENT_SECRETS_MESSAGE,
    scope=YOUTUBE_READ_WRITE_SCOPE)
    
    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()
  
    if credentials is None or credentials.invalid:
        flags = argparser.parse_args()
        credentials = run_flow(flow, storage, flags)
    
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    #http=credentials.authorize(httplib2.Http()))
    http=credentials.authorize(httplib2.Http(cache=".playlister-cache"))) # trialling caching

    #print_playlist_info(youtube)
    #pp.pprint(get_playlist_contents(youtube,get_watchlater_playlist_id(youtube)))
    #add_playlist(youtube, "New Playlist Attempt", "Working the API all the live long day.", "private")
    #delete_playlist_by_id(youtube, "PLR21k8SuCtZcvTRh5jhkLMqFI6b_vuoF-")

def delete_playlist_by_id(youtube, id):
    """ Delete a playlist by id """
    request_response = youtube.playlists().delete(id=id).execute()
    #pp.pprint(request_response)
    return request_response

def add_playlist(youtube, title, description, privacy_status):
    """ Add a playlist """
    request_response = youtube.playlists().insert(part = "snippet,status",body = dict(snippet = dict(title = title, description = description), status = dict(privacyStatus=privacy_status))).execute()
    #pp.pprint(request_response)
    return request_response
    
def print_playlist_info(youtube):
    """ Print a "pretty" dump of a users playlists and their contents. """
    
    playlists = get_playlists(youtube)
    
    print("Play list ids:\n")
    for playlist in playlists:
        print "Title: ", playlist['title']
        #pp.pprint(playlists)
    print("\n\n")

    print("Playlist contents:\n")
    for playlist in playlists:
        print "Play list title: ", playlist['title'], " (", playlist['id'], ")"
        playlist_contents = get_playlist_contents(youtube, playlist['id'])
        #pp.pprint(playlist_contents)
        print "Count is ", len(playlist_contents)
        for item in playlist_contents:
            print "\tVideo title: ", item['snippet']['title'].encode('ascii', 'ignore'), " (", item['id'], ")"
            #print "\tVideo title: (", item['id'], ")"
        print "\n"

    #playlist_contents = get_playlist_contents(youtube, 'PLR21k8SuCtZdOJbTyeQ3vXy-y8Ipi3q_E')
    #pp.pprint(dir(youtube))
    return

def get_playlist_contents(youtube, desired_playlist_id):
    """ Given an authenticated youtube object and a playlist id, retrieve playlist contents as a list of [id, title, and videoId]. """

    fields_list = "items(id,snippet(title,resourceId(videoId)))"
    playlist_contents = []
    playlist_items = youtube.playlistItems().list(playlistId=desired_playlist_id, part='snippet', fields=fields_list, maxResults=50).execute()
    playlist_contents += [item for item in playlist_items['items']]
    
    while ('nextPageToken' in playlist_items):
        print "Page Token: ", playlist_items['nextPageToken']
        playlist_items = youtube.playlistItems().list(playlistId=id, part='snippet', fields=fields_list, maxResults=50, pageToken=playlist_items['nextPageToken']).execute()
        playlist_contents += [item for item in playlist_items['items']]

    return playlist_contents

def get_playlists(youtube):
    """ Given an authenticated youtube object, return a list of playlist ids and titles (including the 'watch later' playlist) """
    
    playlists_request = youtube.playlists().list(part='id,snippet',mine=True).execute()

    playlists = [{'id' : playlist['id'], 'title' : playlist['snippet']['title']} for playlist in playlists_request['items']]

    # Get watch later playlist via looking up the user's channel
    channels_listing = youtube.channels().list(part="contentDetails", mine=True).execute()
    playlists.append({'id':get_watchlater_playlist_id(youtube), 'title': u'Watch Later'})

    return playlists

def get_watchlater_playlist_id(youtube):
    """ Given an authenticate youtube object, retrieve the watch later playlist id from the user's channel info. """
    channels_listing = youtube.channels().list(part="contentDetails", mine=True).execute()
    return channels_listing['items'][0]['contentDetails']['relatedPlaylists']['watchLater']

if __name__ == '__main__':
    pp = pprint.PrettyPrinter()
    main()
    
