import playlists_sync_params as params
import os
import xml.etree.ElementTree as ET
import logging
import shutil
import fire


def build_m3u8_file(playlist_name, files):
    playlist_file = open(f'{params.playlist_output_dir}/{playlist_name}.m3u8', 'w')
    playlist_file.writelines('#EXTM3U\n')

    for file in files:
        playlist_file.writelines("#EXT-X-RATING:0\n")
        playlist_file.writelines(f'{params.mobile_files_path}{file.lstrip(params.trim_starting_path)}\n')

    playlist_file.close()


def parse_playlist_file(playlist):
    tree = ET.parse(f'{params.playlists_dir}/{playlist}/playlist.xml')
    root = tree.getroot()

    files = root.find('PlaylistItems')

    filenames = []
    for file in files:
        music_file = file.find('Path').text
        create_links(music_file)
        filenames.append(music_file)

    return filenames


def create_links(filename):
    short_dir = filename.lstrip(params.trim_starting_path)
    dir_path = f'{params.files_output_dir}/{"/".join(short_dir.split("/")[:-1])}'

    if os.path.exists(dir_path) is False:
        os.makedirs(dir_path)

    try:
        os.symlink(f'{filename}', f'{params.files_output_dir}/{short_dir}')
    except FileNotFoundError as e:
        logging.error(f'{filename} not found')
    except FileExistsError as e:
        logging.info(f'{params.files_output_dir}/{short_dir} already exists')


def clean_files():
    if os.path.exists(params.files_output_dir):
        shutil.rmtree(params.files_output_dir)

    if os.path.exists(params.playlist_output_dir):
        shutil.rmtree(params.playlist_output_dir)

    os.makedirs(params.files_output_dir)
    os.makedirs(params.playlist_output_dir)


def list_playlists():
    playlists = os.listdir(params.playlists_dir)

    for playlist in playlists:
        if params.include_playlists is None:
            sync_playlist = params.exclude_playlists is None or (
                    params.exclude_playlists is not None and playlist not in params.exclude_playlists)
        else:
            sync_playlist = playlist in params.include_playlists

        if sync_playlist:
            files = parse_playlist_file(playlist)
            build_m3u8_file(playlist, files)


def scan():
    if params.automatic_clean:
        clean_files()

    list_playlists()


def rescan_all():
    clean_files()
    list_playlists()


if __name__ == '__main__':
    fire.Fire({
        'scan': scan,
        'rescan_all': rescan_all
    })
