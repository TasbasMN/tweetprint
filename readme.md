# Tweet Printer

This project allows you to create printable A4 layouts of tweets from their URLs.

## Usage

Run the script from the command line:

```
python main.py <tweet_url1> <tweet_url2> ... <output_file.pdf>
```

Optional arguments:
- `--no-cuts`: Disable cut marks on tweets

Example:
```
python main.py https://twitter.com/user/status/123456789 output.pdf
```

## Requirements

- Python 3.6+
- Chrome WebDriver (for Selenium)"}
