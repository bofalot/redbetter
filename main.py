import logging
from redbetter.args import parse_args
from redbetter.config import load_config
import uvicorn

logging.basicConfig(level=logging.INFO)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def main():
    uvicorn.run("api.main:app", host="0.0.0.0", port=9725, reload=True)


if __name__ == "__main__":
    args = parse_args()
    load_config(args.config)
    main()
