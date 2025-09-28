# REDBetter

![REDBetter Logo](logo.png)

REDBetter is a Python script that automatically transcodes and uploads FLAC torrents to redacted.ch. It can be run as a one-time script or as a web server that listens for webhook notifications.

## Features

*   Automatically transcodes FLAC torrents to V0 and 320kbps MP3.
*   Can be run as a one-time script to process all seeding torrents or specific releases.
*   Can be run as a web server to transcode on demand via webhook notifications.
*   Supports Docker for easy setup and deployment.
*   Caches transcoded torrents to avoid duplicate work.

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

### Script Mode

To run REDBetter as a one-time script, use the `--script` flag:

```bash
python main.py --script
```

This will scan all your seeding torrents and transcode any missing formats.

To transcode a specific release, provide the release URL:

```bash
python main.py --script --release-urls <release_url_1> <release_url_2>
```

By default, the script runs in dry-run mode. To actually upload the transcoded torrents, use the `--upload` flag:

```bash
python main.py --script --upload
```

### Server Mode

To run REDBetter as a web server, simply run:

```bash
python main.py
```

The server will listen on port 9725 for webhook notifications. To trigger a transcode, send a POST request to `/api/webhook` with the following form data:

*   `torrent_url`: The URL of the torrent to transcode.
*   `upload` (optional): Set to `true` to upload the transcoded torrent.
*   `single` (optional): Set to `true` to only transcode one format.

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