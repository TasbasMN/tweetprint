from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Image as ReportLabImage, Spacer
from PIL import Image as PILImage
from src.image_creator import create_tweet_image
from src.utils import ensure_temp_dir, TEMP_DIR
import os

def create_pdf_layout(tweets, output_file, add_cuts=True):
    ensure_temp_dir()
    
    doc = SimpleDocTemplate(output_file, pagesize=A4, topMargin=10*mm, bottomMargin=10*mm, leftMargin=10*mm, rightMargin=10*mm)
    story = []

    for i, tweet_info in enumerate(tweets):
        full_name, username, tweet_text, timestamp, likes, retweets, replies, bookmarks, views, profile_pic = tweet_info
        img = create_tweet_image(full_name, username, tweet_text, timestamp, likes, retweets, replies, bookmarks, views, profile_pic, add_cuts=add_cuts)
        
        img_path = os.path.join(TEMP_DIR, f"temp_{username}_{timestamp}.png")
        img.save(img_path)

        # Calculate image width and height in points (1 point = 1/72 inch)
        img_width, img_height = img.size
        img_width_pt, img_height_pt = img_width * 72 / 96, img_height * 72 / 96 # Assuming 96 DPI
        max_width_pt = 190 * mm * 72 / 25.4 # Convert 190mm to points

        if img_width_pt > max_width_pt:
            ratio = max_width_pt / img_width_pt
            img_width_pt, img_height_pt = max_width_pt, img_height_pt * ratio

        story.append(ReportLabImage(img_path, width=img_width_pt, height=img_height_pt))
        story.append(Spacer(1, 5*mm))

    doc.build(story)