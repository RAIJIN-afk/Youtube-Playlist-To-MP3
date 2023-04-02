import pytube as pt
import os
import subprocess

playlist_url = input("Enter the URL of the playlist you can to download: ")
playlist = pt.Playlist(playlist_url)
links = playlist.video_urls

print("Number of videos in playlist: {0}".format(playlist.length))

out_fol = os.getcwd() + "\\output"
for link in links:
    vid_ref = pt.YouTube(link)
    vid_aud = vid_ref.streams.get_audio_only()

    bn, ext = os.path.splitext(vid_aud.default_filename)

    if not os.path.isfile("{0}\\{1}.mp3".format(out_fol, bn)):
        print("Downloading and converting {0}...".format(bn))
        dl = vid_aud.download(output_path=(
            "{0}\\output".format(os.getcwd())))

        subprocess.run(['ffmpeg', '-loglevel', 'quiet', '-i', "{0}\\{1}".format(
            out_fol, vid_aud.default_filename), "{0}\\{1}.mp3".format(out_fol, bn)])
        os.remove("{0}\\{1}".format(out_fol, vid_aud.default_filename))
        print("{0} has been successfully downloaded!\n".format(vid_ref.title))
    else:
        print("{0} already exists. Skipping...".format(bn))
