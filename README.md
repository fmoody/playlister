# playlister
General Youtube Playlist Munger

State: In-Progress

Problem: Youtube Watch Later playlist has grown out of control and general annoyance with the youtube playlist UI.

Solution: Command line munging of youtube playlists!  Unfortunately, before playlister was done, Youtube removed the ability to access the Watch Later playlist...  But it is still handy to be able to muck about with playlists and their videos.

```
usage: playlister.py [-h] [--auth_host_name AUTH_HOST_NAME]
                     [--noauth_local_webserver]
                     [--auth_host_port [AUTH_HOST_PORT [AUTH_HOST_PORT ...]]]
                     [--logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                     {list_playlists,add_playlist,rm_playlist,cp_playlist,list,add,rm}
                     ...

Manipulate your youtube playlists

optional arguments:
  -h, --help            show this help message and exit
  --auth_host_name AUTH_HOST_NAME
                        Hostname when running a local web server.
  --noauth_local_webserver
                        Do not run a local web server.
  --auth_host_port [AUTH_HOST_PORT [AUTH_HOST_PORT ...]]
                        Port web server should listen on.
  --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level of detail.

Playlister:
  {list_playlists,add_playlist,rm_playlist,cp_playlist,list,add,rm}
    list_playlists      List Playlists
    add_playlist        Add a playlist
    rm_playlist         Remove a playlist
    cp_playlist         Copy a playlist to another playlist
    list                List videos in a playlist
    add                 Add a video to a playlist
    rm                  Remove a video to a playlist
```
