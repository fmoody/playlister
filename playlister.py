#!./bin/python

#TODO: REMOVE
import pprint
#TODO: REMOVE

from google_auth_code import *
from tooling import *


def main():

    youtube = get_youtube_connection()
    
    ## Work Area ##
    print_playlist_info(youtube)
    #request_response = add_playlist(youtube, "Test Playlist", "Working the API all the live long day.", "private")
    #pp.pprint("Add Playlist response is:\n")
    #pp.pprint(request_response)
    #request_response = get_playlist_id_by_title(youtube, "Watch Later")
    #pp.pprint("Get Playlist Id by Name response is:\n")
    #pp.pprint(request_response)
    #delete_playlist_by_title(youtube, "Test Playlist")
    #pp.pprint(get_playlist_contents(youtube,get_watchlater_playlist_id(youtube)))
    #delete_playlist_by_id(youtube, "PLR21k8SuCtZcvTRh5jhkLMqFI6b_vuoF-")
    ## Work Area ##


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

if __name__ == '__main__':
    pp = pprint.PrettyPrinter()
    main()
    
