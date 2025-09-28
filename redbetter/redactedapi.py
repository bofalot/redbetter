#!/usr/bin/env python
import os
import re
import json
import time

import requests
import html

# def upload(self, group, torrent, new_torrent, format, description, dry_run):

# dryrun - (bool) Only return the derived information from the posted data without actually uploading the torrent.
# file_input - (file) .torrent file contents
# groupid - (int) torrent groupID (ie album) this belongs to

# Todo: leave below out as all from group, and see if RED will accept the upload with just the group ID
# type - (int) index of category (Music, Audiobook, ...)
# artists[] - (str)
# importance[] - (int) index of artist type (Main, Guest, Composer, ...) One-indexed!
# title - (str) Album title
# year - (int) Album "Initial Year"
# releasetype - (int) index of release type (Album, Soundtrack, EP, ...)
# unknown - (bool) Unknown Release
# vanity_house - (bool) is this a Vanity House release?

# Todo: figure out values for below - seem to be on the torrent, not the group
# remaster_year - (int) Edition year
# remaster_title - (str) Edition title
# remaster_record_label - (str) Edition record label
# remaster_catalogue_number - (str) Edition catalog number
# scene - (bool) is this a scene release?
# format - (str) MP3, FLAC, etc
# bitrate - (str) 192, Lossless, Other, etc
# other_bitrate - (str) bitrate if Other
# vbr - (bool) other_bitrate is VBR
# logfiles[] - (files) ripping log files
# extra_file_#
# extra_format[]
# extra_bitrate[]
# extra_release_desc[]
# media - (str) CD, DVD, Vinyl, etc
# tags - (str)
# image - (str) link to album art
# album_desc - (str) Album description (ignored if new torrent is merged or added to existing group)
# release_desc - (str) Release (torrent) description
# desc - (str) Description for non-music torrents
# requestid - (int) requestID being filled

        # form = {
        #     'groupid' : group["group"]["id"],
        #     #'type' : group["group"]["categoryId"],
        #     #'artists' : [a["name"] for a in group["group"]["musicInfo"]["artists"]],
        #     #'importance' : [1 for a in group["group"]["musicInfo"]["artists"]],
        #     #'title' : group["name"],
        #     #'year' : group["year"],
        #     #'releaseType' : group["group"]["releaseType"],
        #     #'unknown' : False,
        #     #'vanity_house': group['group']['vanityHouse']
        #     'remaster_year': str(torrent['remasterYear']),
        #     'remaster_title': torrent['remasterTitle'],
        #     'remaster_record_label': torrent['remasterRecordLabel'],
        #     'remaster_catalogue_number': torrent['remasterCatalogueNumber'],
        #     'format': formats[format]['format'],
        #     'bitrate': formats[format]['encoding'],
        #     'media': torrent['media'],
        #     'vbr': format == 'V0',
        #     'logfiles': []
        # }
        # release_desc = '\n'.join(description)
        # if release_desc:
        #     form['release_desc'] = release_desc
        #
        # if dry_run:
        #     form['dryrun'] = True
        #
        # # Open the torrent file and send the request
        # with open(new_torrent, "rb") as torrent_file:
        #     files = {"file_input": torrent_file}
        #     response = self.session.post(self.ajax_url, params={'action': "upload"}, data=form, files=files)
        #
        # return response

#
# These functions are only used in torrent-crawl.py, which I'm not using yet
#
#    def get_better(self, search_type=3, tags=None):
#        if tags is None:
#            tags = []
#        data = self.__request('better', method='transcode', type=search_type, search=' '.join(tags))
#        out = []
#        for row in data:
#            out.append({
#                'permalink': 'torrents.php?id={}'.format(row['torrentId']),
#                'id': row['torrentId'],
#                'torrent': row['downloadUrl'],
#            })
#        return out
#
#    def get_torrent(self, torrent_id):
#        '''Downloads the torrent at torrent_id using the authkey and passkey'''
#        while time.time() - self.last_request < self.rate_limit:
#            time.sleep(0.1)
#
#        torrentpage = 'https://redacted.sh/torrents.php'
#        params = {'action': 'download', 'id': torrent_id}
#        if self.authkey:
#            params['authkey'] = self.authkey
#            params['torrent_pass'] = self.passkey
#        r = self.session.get(torrentpage, params=params, allow_redirects=False)
#
#        self.last_request = time.time() + 2.0
#        if r.status_code == 200 and 'application/x-bittorrent' in r.headers['content-type']:
#            return r.content
#        return None
#
#    def get_torrent_info(self, id):
#        return self.__request('torrent', id=id)['torrent']
