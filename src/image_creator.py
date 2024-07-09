from PIL import Image as PILImage, ImageDraw, ImageFont
import textwrap
from reportlab.lib.units import mm


def add_cut_marks(image, margin=5, length=10):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    
    # Top-left corner
    draw.line((margin, 0, margin, length), fill='black', width=1)
    draw.line((0, margin, length, margin), fill='black', width=1)
    
    # Top-right corner
    draw.line((width - margin, 0, width - margin, length), fill='black', width=1)
    draw.line((width - length, margin, width, margin), fill='black', width=1)
    
    # Bottom-left corner
    draw.line((margin, height - length, margin, height), fill='black', width=1)
    draw.line((0, height - margin, length, height - margin), fill='black', width=1)
    
    # Bottom-right corner
    draw.line((width - margin, height - length, width - margin, height), fill='black', width=1)
    draw.line((width - length, height - margin, width, height - margin), fill='black', width=1)
    
    return image



def create_tweet_image(full_name, username, tweet_text, timestamp, likes, retweets, replies, bookmarks, views, profile_pic, add_cuts=True):
    # Initial setup
    width, height = 600, 1000
    background = PILImage.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(background)
    
    # Load fonts
    font_regular = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)

    # Start drawing
    y_offset = 10
    text_start_x = 60 if profile_pic else 10

    # Add profile picture if provided
    if profile_pic:
        profile_pic = profile_pic.resize((40, 40))
        background.paste(profile_pic, (10, y_offset))

    # Draw user info and tweet
    draw.text((text_start_x, y_offset), full_name, font=font_bold, fill='black')
    draw.text((text_start_x, y_offset + 16), f"@{username}", font=font_regular, fill='gray')
    
    y_offset += 40
    for line in textwrap.wrap(tweet_text, width=70):
        draw.text((text_start_x, y_offset), line, font=font_regular, fill='black')
        y_offset += 16

    # Draw timestamp and stats
    draw.text((text_start_x, y_offset + 10), timestamp, font=font_small, fill='gray')
    stats = f"↺ {replies} ⇄ {retweets} ♥ {likes} ⚑ {bookmarks} ◉ {views}"
    draw.text((text_start_x, y_offset + 24), stats, font=font_small, fill='gray')

    # Crop image
    bbox = PILImage.eval(background, lambda x: 255 - x).getbbox()
    cropped = background.crop(bbox)

    # Add padding
    final_image = PILImage.new('RGB', (cropped.width + 20, cropped.height + 20), color='white')
    final_image.paste(cropped, (10, 10))

    # Add cut marks if requested
    if add_cuts:
        final_image = add_cut_marks(final_image)

    return final_image


def combine_tweet_images(tweet_images, max_width=190*mm, max_height=270*mm):
    total_width = max_width
    total_height = sum(img.size[1] for img in tweet_images)
    
    if total_height > max_height:
        scale_factor = max_height / total_height
        total_height = max_height
        total_width *= scale_factor
    
    combined_image = PILImage.new('RGB', (int(total_width), int(total_height)), color='white')
    
    y_offset = 0
    for img in tweet_images:
        if total_width < img.size[0]:
            img = img.resize((int(total_width), int(img.size[1] * total_width / img.size[0])), PILImage.LANCZOS)
        combined_image.paste(img, (0, int(y_offset)))
        y_offset += img.size[1]
    
    return combined_image
