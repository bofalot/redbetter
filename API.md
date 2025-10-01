# REDBetter API Specification

## Introduction

REDBetter is a Python script that automatically transcodes and uploads FLAC torrents to Redacted and Orpheus. It can be run as a web server that listens for webhook notifications.

This document describes the API endpoints for the REDBetter web server.

## Endpoints

### `/api/getCandidates`

Gets a list of transcode candidates.

*   **URL:** `/api/getCandidates`
*   **Method:** `GET`
*   **Query Parameters:**
    *   `site` (optional): The site to get candidates from. Can be `red`, `ops`, or `all`. Defaults to `all`.
    *   `limit` (optional): The maximum number of candidates to return.
    *   `offset` (optional): The offset to start from.

*   **Example Request:**

    ```bash
    curl -X GET "http://localhost:9725/api/getCandidates?site=red&limit=10"
    ```

*   **Example Response:**

    ```json
    {
        "candidates": [
            [
                12345,
                67890
            ]
        ]
    }
    ```

### `/api/transcode`

Transcodes a single torrent.

*   **URL:** `/api/transcode`
*   **Method:** `POST`
*   **Form Data:**
    *   `torrent_url` (required): The URL of the torrent to transcode.
    *   `upload` (optional): Set to `true` to upload the transcoded torrent. Defaults to `false`.
    *   `single` (optional): Set to `true` to only transcode one format. Defaults to `false`.
    *   `add_to_qbittorrent` (optional): Set to `true` to add the transcoded torrent to qBittorrent. Defaults to `false`.

*   **Example Request:**

    ```bash
    curl -X POST -F "torrent_url=https://redacted.sh/torrents.php?torrentid=12345" http://localhost:9725/api/transcode
    ```

*   **Example Response:**

    ```json
    {
        "message": "Success",
        "torrent_files": [
            "/path/to/transcoded/torrent.torrent"
        ]
    }
    ```

### `/api/transcode/all`

Transcodes all eligible torrents from your seeding list on both Redacted and Orpheus.

*   **URL:** `/api/transcode/all`
*   **Method:** `POST`
*   **Form Data:**
    *   `upload` (optional): Set to `true` to upload the transcoded torrents. Defaults to `false`.
    *   `single` (optional): Set to `true` to only transcode one format per release. Defaults to `false`.
    *   `add_to_qbittorrent` (optional): Set to `true` to add the transcoded torrents to qBittorrent. Defaults to `false`.

*   **Example Request:**

    ```bash
    curl -X POST http://localhost:9725/api/transcode/all
    ```

*   **Example Response:**

    ```json
    {
        "message": "Success",
        "results": {
            "red": {
                "message": "Success",
                "torrent_files": [
                    "/path/to/transcoded/torrent.torrent"
                ]
            },
            "ops": {
                "message": "No available transcodes to better",
                "torrent_files": []
            }
        }
    }
    ```