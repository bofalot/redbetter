# REDBetter

![REDBetter Logo](logo.png)

REDBetter is a Python script that automatically transcodes and uploads FLAC torrents to redacted.ch and orpheus.network.

## Features

*   Automatically transcodes FLAC torrents to V0 and 320kbps MP3.
*   Runs as a web server to transcode on demand via webhook notifications.
*   Supports Docker for easy setup and deployment.


## Dependencies

*   Python 3.6+
*   `mktorrent`
*   `lame`, `sox`, and `flac`

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/redbetter.git
    cd redbetter
    ```

2.  **Install the dependencies:**

    *   **mktorrent, lame, sox, flac:**

        On Debian/Ubuntu:

        ```bash
        sudo apt-get install mktorrent lame sox flac
        ```

        On macOS:

        ```bash
        brew install mktorrent lame sox flac
        ```

    *   **Python dependencies:**

        ```bash
        pip install -r requirements.txt
        ```

3.  **Configure the application:**

    Copy the example configuration file:

    ```bash
    cp config.example config.ini
    ```

    Then, edit `config.ini` with your redacted.ch API key and other settings.

## Usage

### Server Mode

To run REDBetter as a web server, simply run:

```bash
python main.py
```

The server will listen on port 9725 for webhook notifications. To trigger a transcode, send a POST request to the following endpoints:

*   `/api/getCandidates`: Gets a list of transcode candidates.
    *   **Query Parameters:**
        *   `site` (optional): The site to get candidates from. Can be `red`, `ops`, or `all`. Defaults to `all`.
        *   `limit` (optional): The maximum number of candidates to return.
        *   `offset` (optional): The offset to start from.
*   `/api/transcode`: Transcodes a single torrent.
    *   **Form Data:**
        *   `torrent_url`: The URL of the torrent to transcode.
        *   `upload` (optional): Set to `true` to upload the transcoded torrent.
        *   `single` (optional): Set to `true` to only transcode one format.
        *   `add_to_qbittorrent` (optional): Set to `true` to add the transcoded torrent to qBittorrent.
*   `/api/transcode/all`: Transcodes all eligible torrents from your seeding list.
    *   **Form Data:**
        *   `upload` (optional): Set to `true` to upload the transcoded torrents.
        *   `single` (optional): Set to `true` to only transcode one format per release.
        *   `add_to_qbittorrent` (optional): Set to `true` to add the transcoded torrents to qBittorrent.

## Docker

To run REDBetter with Docker, first build the image:

```bash
docker-compose build
```

Then, run the application using `docker-compose`:

```bash
docker-compose run --rm redbetter
```

You can also use the `docker-compose-local.yml` file for local development:

```bash
docker-compose -f docker-compose-local.yml up
```

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

## To-Do
1. UI
   1. UI / Typescript Tests
   1. Show snatch better list from both Redacted and Orpheus
   1. Allow the triggering of transcoding and uploading separately
   1. Displays any errors
   1. Cache results

1. Backend
   1. Support for adding transcoded torrents straight to QBitTorrent
   2. Transcoding to spawn in a different process, using multiple threads.

1. Weekly job for checking entire snatch list on both Redacted and Orpheus and bettering whatever is possible
1. Crawling for any album which can be downloaded and then transcoded
