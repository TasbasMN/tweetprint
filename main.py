import argparse
from src.tweet_fetcher import get_tweet_info_from_url
from src.pdf_generator import create_pdf_layout
from src.utils import setup_logging, TEMP_DIR

def main():
    parser = argparse.ArgumentParser(description='Create printable A4 layout of tweets.')
    parser.add_argument('urls', nargs='+', help='URLs of tweets')
    parser.add_argument('output', help='Output PDF file path')
    parser.add_argument('--no-cuts', action='store_true', help='Disable cut marks on tweets')
    args = parser.parse_args()

    setup_logging()

    tweets = []
    for url in args.urls:
        tweet_info = get_tweet_info_from_url(url)
        if tweet_info:
            tweets.append(tweet_info)
        else:
            print(f"Failed to process tweet: {url}")

    if tweets:
        create_pdf_layout(tweets, args.output, add_cuts=not args.no_cuts)
        print(f"Printable tweet layout saved to {args.output}")
        print(f"Temporary files are stored in the '{TEMP_DIR}' directory")
    else:
        print("No tweets were successfully processed.")

if __name__ == "__main__":
    main()




def main():
    parser = argparse.ArgumentParser(description='Create printable A4 layout of tweets.')
    parser.add_argument('urls', nargs='+', help='URLs of tweets')
    parser.add_argument('output', help='Output PDF file path')
    parser.add_argument('--no-cuts', action='store_true', help='Disable cut marks on tweets')
    args = parser.parse_args()


    tweets = []
    for url in args.urls:
        tweet_info = get_tweet_info_from_url(url)
        if tweet_info:
            tweets.append(tweet_info)
        else:
            print(f"Failed to process tweet: {url}")

    if tweets:
        create_pdf_layout(tweets, args.output, add_cuts=not args.no_cuts)
        print(f"Printable tweet layout saved to {args.output}")
    else:
        print("No tweets were successfully processed.")

if __name__ == "__main__":
    main()
