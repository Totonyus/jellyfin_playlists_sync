playlists_dir = "/var/lib/jellyfin/data/playlists/" # where jellyfin playlists are located
files_output_dir = "/samba_shares/playlists_sync/files/" # where the symlinks files will be written
playlist_output_dir = "/samba_shares/playlists_sync/playlists/" # where the m3u8 files will be written

mobile_files_path = "primary/playlist_sync/files/" # where the files will be located on your mobile

trim_starting_path = "" # trim a part of the path to reduce file hierarchy

automatic_clean = True # delete everything before scanning

# include_playlists is always use over exclude_playlists
exclude_playlists = None # None = all playlists will be synced, include_playlists = ['Metal', 'Justin Bieber']
include_playlists = None # None = all playlists will be synced, include_playlists = ['Jazz', 'Mike Oldfield']
