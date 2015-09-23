import pprint

pp = pprint.PrettyPrinter()

def delete_playlist_by_title(youtube, title):
    """ Delete all playlists with the given title. """
    named_playlists = get_playlist_id_by_title(youtube, title)
    for playlist in named_playlists:
        request_response = delete_playlist_by_id(youtube, playlist['id'])
    return
            
def get_playlist_id_by_title(youtube, title):
    """ Retrieve a list of playlists (ids and titles) that match the given title. """
    playlists = get_playlists(youtube)
    named_playlists = filter(lambda playlist: playlist['title'] == title, playlists)
    return named_playlists
        
def delete_playlist_by_id(youtube, id):
    """ Delete a playlist by id """
    request_response = youtube.playlists().delete(id=id).execute()
    return request_response

def add_playlist(youtube, title, description, privacy_status):
    """ Add a playlist """
    request_response = youtube.playlists().insert(part = "snippet,status",body = dict(snippet = dict(title = title, description = description), status = dict(privacyStatus=privacy_status))).execute()
    return request_response
    
def get_playlist_contents(youtube, desired_playlist_id):
    """ Given an authenticated youtube object and a playlist id, retrieve playlist contents as a list of [id, title, and videoId]. """

    fields_list = "items(id,snippet(title,resourceId(videoId))),nextPageToken"
    playlist_contents = []
    playlist_items = youtube.playlistItems().list(playlistId=desired_playlist_id, part='snippet', fields=fields_list, maxResults=50).execute()
    playlist_contents += [item for item in playlist_items['items']]
    
    while ('nextPageToken' in playlist_items):
        playlist_items = youtube.playlistItems().list(playlistId=desired_playlist_id, part='snippet', fields=fields_list, maxResults=50, pageToken=playlist_items['nextPageToken']).execute()
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
