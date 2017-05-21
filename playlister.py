#!/usr/bin/env python

import argparse
import oauth2client.tools

from google_auth_code import get_youtube_connection
from tooling import display_playlist_list, get_playlist_id_by_title, add_playlist, \
                    delete_playlist_by_title, copy_videos_from_playlist1_to_playlist2, \
                    list_playlist_contents, add_video_to_playlist, remove_video_from_playlist


def main():

    args = construct_arg_parser()

    youtube = get_youtube_connection(args)

    if args.action == "list_playlists":
        display_playlist_list(youtube, args.detail, args.match)
    elif args.action == "add_playlist":
        add_playlist(youtube, args.playlist, args.description, args.privacy_status)
    elif args.action == "rm_playlist":
        delete_playlist_by_title(youtube, args.playlist)
    elif args.action == "cp_playlist":
        copy_videos_from_playlist1_to_playlist2(youtube, args.from_playlist, args.to_playlist)
    elif args.action == "list":
        list_playlist_contents(youtube, args.playlist, args.detail)
    elif args.action == "add":
        playlist_id = get_playlist_id_by_title(youtube, args.playlist, True)[0]['id']
        add_video_to_playlist(youtube, playlist_id, args.videoId)
    elif args.action == "rm":
        playlist_id = get_playlist_id_by_title(youtube, args.playlist)[0]['id']
        remove_video_from_playlist(youtube, playlist_id, args.videoId)
    else:
        print "Error, no command executed."


def construct_arg_parser():
    opt_parser = argparse.ArgumentParser(description="Manipulate your youtube playlists",
                                         parents=[oauth2client.tools.argparser])

    subparsers = opt_parser.add_subparsers(title="Playlister",
                                           dest="action")

    playlists_parser = subparsers.add_parser("list_playlists",
                                             help="List Playlists")
    playlists_parser.add_argument("--match",
                                  help="Case-sensitive text to match")
    playlists_parser.add_argument("--detail",
                                  choices=["title", "id"],
                                  action="append")

    add_playlist_parser = subparsers.add_parser("add_playlist",
                                                help="Add a playlist")
    add_playlist_parser.add_argument("playlist")
    add_playlist_parser.add_argument("--description",
                                     help="Description of the playlist")
    add_playlist_parser.add_argument("--privacy_status",
                                     help="Privacy Status",
                                     choices=['public', 'private', 'unlisted'],
                                     default='private')

    rm_playlist_parser = subparsers.add_parser("rm_playlist",
                                               help="Remove a playlist")
    rm_playlist_parser.add_argument("playlist")

    cp_playlist_parser = subparsers.add_parser("cp_playlist",
                                               help="Copy a playlist to another playlist")
    cp_playlist_parser.add_argument("from_playlist")
    cp_playlist_parser.add_argument("to_playlist")

    list_parser = subparsers.add_parser("list",
                                        help="List videos in a playlist")
    list_parser.add_argument("playlist")
    list_parser.add_argument("--detail",
                             choices=["title", "id", "debug"],
                             action="append")

    add_video_parser = subparsers.add_parser("add",
                                             help="Add a video to a playlist")
    add_video_parser.add_argument("playlist",
                                  help="Playlist to add video to")
    add_video_parser.add_argument("videoId",
                                  help="Video id to add to the playlist")

    rm_video_parser = subparsers.add_parser("rm",
                                            help="Remove a video to a playlist")
    rm_video_parser.add_argument("playlist",
                                 help="Playlist to remove video from")
    rm_video_parser.add_argument("videoId",
                                 help="Video id to remove from the playlist")

    args = opt_parser.parse_args()

    return args


if __name__ == '__main__':
    main()
