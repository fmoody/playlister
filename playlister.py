#!/usr/bin/env python

import argparse
import pprint
import oauth2client.tools

from google_auth_code import *
from tooling import *


def main():

    opt_parser = argparse.ArgumentParser(description="manipulate your youtube playlists", parents=[oauth2client.tools.argparser])
    opt_parser.add_argument("--playlist", help="The name of the playlist", required=True)

    action_group = opt_parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("--list", help="List a playlist", action="store_true")
    action_group.add_argument("--add", help="Add a playlist", action="store_true")
    action_group.add_argument("--rm", help="Remove a playlist", action="store_true")
    action_group.add_argument("--cp", help="Copy PLAYLIST to CP", default=False)

    opt_parser.add_argument("--description", help="Description of the playlist")
    opt_parser.add_argument("--privacy_status", help="Privacy Status",
                            choices=['public', 'private', 'unlisted'], default='private')

    args = opt_parser.parse_args()

    youtube = get_youtube_connection(args)

    if args.list:
        playlist_ids = get_playlist_id_by_title(youtube, args.playlist)
        for playlist_id in playlist_ids:
            pp.pprint(get_playlist_contents(youtube, playlist_id['id']))
    elif args.add:
        add_playlist(youtube, args.playlist, args.description, args.privacy_status)
    elif args.rm:
        delete_playlist_by_title(youtube, args.playlist)
    elif args.cp:
        print("placeholder")


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

if __name__ == '__main__':
    pp = pprint.PrettyPrinter()
    main()
