def display_playlist_list(youtube, detail, match):
    """ Display the list of playlists associated with the account """

    if detail is None:
        detail = ["title"]

    playlists = get_playlists(youtube)

    for playlist in playlists:
        if match is None or match in playlist['title']:
            for detail_item in detail:
                if detail_item == 'title':
                    detail_output = "\""
                    detail_output += playlist[detail_item]
                    detail_output += "\""
                else:
                    detail_output = playlist[detail_item]

                print detail_output,
            print
    return


def list_playlist_contents(youtube, playlist, detail):
    if detail is None:
        detail = ["title", "id"]

    playlist_ids = get_playlist_id_by_title(youtube, playlist)
    for playlist_id in playlist_ids:
        playlist_contents = get_playlist_contents(youtube, playlist_id['id'])
        for playlist_entry in playlist_contents:
            entry_output = ""
            if "title" in detail:
                entry_output += "\""
                entry_output += playlist_entry['snippet']['title']
                entry_output += "\" "
            if "id" in detail:
                entry_output += playlist_entry['snippet']['resourceId']['videoId']
            if "debug" in detail:
                entry_output += str(playlist_entry)
            print(entry_output)
    return


def delete_playlist_by_title(youtube, title):
    """ Delete all playlists with the given title. """
    named_playlists = get_playlist_id_by_title(youtube, title)
    for playlist in named_playlists:
        delete_playlist_by_id(youtube, playlist['id'])
    return


def get_playlist_id_by_title(youtube, title, create_missing_playlist=False):
    """ Retrieve a list of playlists (ids and titles) that match the given title. """
    playlists = get_playlists(youtube)
    named_playlists = filter(lambda playlist: playlist['title'] == title, playlists)
    if (not named_playlists and create_missing_playlist):
        request_response = add_playlist(youtube, title, title, "private")
        named_playlists = [dict(id=request_response['id'], title=title)]
    return named_playlists


def delete_playlist_by_id(youtube, id):
    """ Delete a playlist by id """
    request_response = youtube.playlists().delete(id=id).execute()
    return request_response


def add_playlist(youtube, title, description, privacy_status):
    """ Add a playlist """
    request_response = youtube.playlists().insert(part="snippet,status",
                                                  body=dict(
                                                      snippet=dict(title=title,
                                                                   description=description),
                                                      status=dict(privacyStatus=privacy_status)
                                                  )).execute()
    return request_response


def get_playlist_contents(youtube, desired_playlist_id):
    """ Given an authenticated youtube object and a playlist id,
    retrieve playlist contents as a list of [id, title, and videoId]. """

    fields_list = "items(id,snippet(title,resourceId(videoId))),nextPageToken"
    playlist_contents = []
    playlist_items = youtube.playlistItems().list(playlistId=desired_playlist_id,
                                                  part='snippet',
                                                  fields=fields_list,
                                                  maxResults=50).execute()
    playlist_contents += [item for item in playlist_items['items']]

    while ('nextPageToken' in playlist_items):
        playlist_items = youtube.playlistItems().list(playlistId=desired_playlist_id,
                                                      part='snippet',
                                                      fields=fields_list,
                                                      maxResults=50,
                                                      pageToken=playlist_items['nextPageToken']
                                                      ).execute()
        playlist_contents += [item for item in playlist_items['items']]

    return playlist_contents


def get_playlists(youtube):
    """ Given an authenticated youtube object, return a list of playlist ids and titles """

    playlists = []

    playlists_request = youtube.playlists().list(part='id,snippet', mine=True)

    while(playlists_request is not None):
        response = playlists_request.execute()
        playlists += [{'id': playlist['id'], 'title': playlist['snippet']['title']}
                      for playlist in response['items']]
        playlists_request = youtube.playlists().list_next(playlists_request, response)

    return playlists


def add_video_to_playlist(youtube, playlist_id, videoIdToAdd):
    """ Add a video to playlist """

    request_response = youtube.playlistItems().insert(part="snippet",
                                                      body=dict(
                                                          snippet=dict(
                                                              playlistId=playlist_id,
                                                              resourceId=dict(
                                                                  kind="youtube#video",
                                                                  videoId=videoIdToAdd
                                                                  )
                                                              )
                                                          )
                                                      ).execute()

    return request_response


def remove_video_from_playlist(youtube, playlist_id, videoIdToRM):
    """ Remove a video from playlist """
    playlistItems = get_playlist_contents(youtube, playlist_id)

    unwanted_playlistItems = filter(lambda item:
                                    item['snippet']['resourceId']['videoId'] == videoIdToRM,
                                    playlistItems)

    if unwanted_playlistItems:
        for item in unwanted_playlistItems:
            youtube.playlistItems().delete(id=item['id']).execute()


def copy_videos_from_playlist1_to_playlist2(youtube, playlist1_title, playlist2_title):
    playlist1_id = get_playlist_id_by_title(youtube, playlist1_title)
    playlist2_id = get_playlist_id_by_title(youtube, playlist2_title, True)[0]['id']

    playlist1_contents = get_playlist_contents(youtube, playlist1_id[0]['id'])

    for video in playlist1_contents:
        add_video_to_playlist(youtube, playlist2_id, video['snippet']['resourceId']['videoId'])

    return


def print_playlist_info(youtube):
    """ Print a "pretty" dump of a users playlists and their contents. """

    playlists = get_playlists(youtube)

    print("Play list ids:\n")
    for playlist in playlists:
        print "Title: ", playlist['title']
    print("\n\n")

    print("Playlist contents:\n")
    for playlist in playlists:
        print "Play list title: ", playlist['title'], " (", playlist['id'], ")"
        playlist_contents = get_playlist_contents(youtube, playlist['id'])
        print "Count is ", len(playlist_contents)
        for item in playlist_contents:
            print "\tVideo title: ", item['snippet']['title'].encode('ascii', 'ignore'),
            " (", item['id'], ")"
        print "\n"

    return
