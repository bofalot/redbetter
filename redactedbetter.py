import pickle
import os
import shutil
import sys
import tempfile
import traceback
from pprint import pprint

import tagging
import transcode
import redactedapi


def create_description(flac_dir, format, permalink):
    # Create an example command to document the transcode process.
    cmds = transcode.transcode_commands(format,
                                        transcode.needs_resampling(flac_dir),
                                        transcode.resample_rate(flac_dir),
            'input.flac', 'output' + transcode.encoders[format]['ext'])

    description = [
        'Transcode of [url=%s]%s[/url]' % (permalink, permalink),
        '',
        'Transcode process:',
        '',
        '[code]%s[/code]' % ' | '.join(cmds),
        ''
        ]
    return description

def formats_needed(torrents, torrent, supported_formats):
    same_group = lambda t: t['media'] == torrent['media'] and\
                           t['remasterYear'] == torrent['remasterYear'] and\
                           t['remasterTitle'] == torrent['remasterTitle'] and\
                           t['remasterRecordLabel'] == torrent['remasterRecordLabel'] and\
                           t['remasterCatalogueNumber'] == torrent['remasterCatalogueNumber']

    others = filter(same_group, torrents)
    current_formats = set((t['format'], t['encoding']) for t in others)
    missing_formats = [format for format, details in [(f, redactedapi.formats[f]) for f in supported_formats]\
                           if (details['format'], details['encoding']) not in current_formats]
    allowed_formats = redactedapi.allowed_transcodes(torrent)
    return [format for format in missing_formats if format in allowed_formats]

def border_msg(msg):
    width = 0
    for line in msg.splitlines():
        length = len(line)
        if length > width:
            width = length

    dash = "-" * (width - 1)
    return "+{dash}+\n{msg}\n+{dash}+".format(dash=dash,msg=msg)

#
# todo: move api, seen etc... into a class for passing around
#
def find_and_upload_missing_transcodes(candidates, api, seen, data_dirs, output_dir, torrent_dir, upload_torrent, single):
    new_torrents = []
    for groupId, torrentId in candidates:
        group = api.torrent_group(groupId)
        if group is not None:
            torrent = next(filter(lambda t: t["id"] == torrentId, group["torrents"]))

            release_artist = "Release artist(s): %s" % group["artist"]
            release_name   = "Release name     : %s" % group["name"]
            release_year   = "Release year     : %s" % group["year"]
            release_url    = "Release URL      : %s" % redactedapi.release_url(groupId, torrentId)
            print("\n\n")
            print(border_msg(release_artist + "\n" + release_name + "\n" + release_year + "\n" + release_url))

            if not torrent["filePath"]:
                print("No filepath for %s (%s) - skipping" % (release_name, release_url))
                continue

            data_dir_found = False
            flac_dir = None
            for data_dir in data_dirs:
                flac_dir = os.path.join(data_dir, redactedapi.unescape(torrent["filePath"]))
                if os.path.exists(flac_dir):
                    data_dir_found = True
                    break

            if not data_dir_found:
                print("Path (%s) does not exist in data directories - skipping" % torrent["filePath"])
                continue

            if transcode.is_multichannel(flac_dir):
                print("This is a multichannel release, which is unsupported - skipping")
                continue

            needed = formats_needed(group["torrents"], torrent, ["V0", "320"])
            print("Formats needed: %s" % ', '.join(needed))

            if needed:
                # Before proceeding, do the basic tag checks on the source
                # files to ensure any uploads won't be reported, but punt
                # on the tracknumber formatting; problems with tracknumber
                # may be fixable when the tags are copied.
                broken_tags = False
                for flac_file in transcode.locate(flac_dir, transcode.ext_matcher('.flac')):
                    (ok, msg) = tagging.check_tags(flac_file, check_tracknumber_format=False)
                    if not ok:
                        print("A FLAC file in this release has unacceptable tags - skipping: %s" % msg)
                        print("You might be able to trump it.")
                        broken_tags = True
                        break
                if broken_tags:
                    continue

            for format in needed:
                print("Adding format %s..." % format)
                tmpdir = tempfile.mkdtemp()
                try:
                    if len(torrent['remasterTitle']) >= 1:
                        basename = group["artist"] + " - " + group["name"] + " (" + torrent['remasterTitle'] + ") " + "[" + group["year"] + "] (" + torrent['media'] + " - "
                    else:
                        basename = group["artist"] + " - " + group["name"] + " [" + group["year"] + "] (" + torrent['media'] + " - "

                    #todo get max_threads from args.
                    transcode_dir = transcode.transcode_release(flac_dir, output_dir, basename, format)
                    if not transcode_dir:
                        print("Some file(s) in this release were incorrectly marked as 24bit - skipping")
                        break

                    new_torrent = transcode.make_torrent(transcode_dir, tmpdir, api.tracker, api.passkey)
                    permalink = redactedapi.permalink(torrent["id"])
                    description = create_description(flac_dir, format, permalink)
                    result = api.upload(group, torrent, new_torrent, format, description, not upload_torrent)
                    pprint(result.text)

                    new_torrent_dest = shutil.copy(new_torrent, torrent_dir)
                    new_torrents.append(new_torrent_dest)
                    print("done!")
                    if single: break
                except Exception as e:
                    print("Error adding format %s: %s: %s" % (format, e, traceback.format_exc()))
                finally:
                    shutil.rmtree(tmpdir)

            #todo re-enable cache. Need to make args.cache available here
            #seen.add(str(torrentId))
            #pickle.dump(seen, open(args.cache, 'wb'))
    return new_torrents
