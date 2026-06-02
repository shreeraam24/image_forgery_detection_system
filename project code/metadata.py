import os
import time
import binascii
from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_data(image):
    """Get EXIF metadata from the image."""
    try:
        exifdata = image.getexif()
        return exifdata if exifdata else None
    except:
        return None

def get_file_properties(image_path):
    """Get basic file properties like size, creation and modification time."""
    file_size = os.path.getsize(image_path)  # in bytes
    creation_time = os.path.getctime(image_path)
    modification_time = os.path.getmtime(image_path)
    return file_size, creation_time, modification_time

def get_image_properties(image):
    """Get image dimensions and format."""
    width, height = image.size
    fmt = image.format
    return width, height, fmt

def is_unwanted_metadata(tagname, value):
    """Filter out XML packets, large binary blobs, and image resources."""
    try:
        # Skip XML packets
        if isinstance(value, bytes):
            decoded = binascii.hexlify(value).decode()
            if decoded.lower().startswith("3c3f787061636b6574"):  # '<?xpacket'
                return True

        if isinstance(value, str) and value.strip().lower().startswith("<?xpacket"):
            return True

        # Skip known noisy or bulky tags
        unwanted_keywords = ['image resources', 'photoshop', 'xpacket', 'xmp']
        if any(k in tagname.lower() for k in unwanted_keywords):
            return True

        # Skip large binary blobs
        if isinstance(value, bytes) and len(value) > 500:
            return True

    except:
        return False

    return False

def get_metadata_report(image_path):
    """Extract and compile metadata information into a formatted string."""
    output = []
    try:
        image = Image.open(image_path)
        exifdata = get_exif_data(image)

        if exifdata:
            output.append("📸 EXIF Metadata:")
            for tagid in exifdata:
                tagname = TAGS.get(tagid, tagid)
                value = exifdata.get(tagid)

                if is_unwanted_metadata(str(tagname), value):
                    continue  # Skip junk metadata

                if isinstance(value, bytes):
                    value = binascii.hexlify(value).decode()

                output.append(f"{tagname}: {value}")

            # Check for missing or suspicious data
            camera_model = exifdata.get(272)  # Camera Model
            software_used = exifdata.get(305)  # Software
            date_time = exifdata.get(306)  # DateTime

            if not camera_model or not software_used:
                output.append("⚠️ Missing camera model or software data — possible manipulation.")
            if not date_time:
                output.append("⚠️ Missing DateTime — possible forgery.")
        else:
            output.append("⚠️ No EXIF data found — Might be REAL.")

        # File timestamps
        file_size, creation, modification = get_file_properties(image_path)
        output.append(f"\n📁 File Info:")
        output.append(f"Size: {file_size} bytes")
        output.append(f"Created: {time.ctime(creation)}")
        output.append(f"Modified: {time.ctime(modification)}")

        if abs(creation - modification) < 10:
            output.append("⚠️ Creation and modification times are suspiciously close.")

        # Image dimensions
        width, height, fmt = get_image_properties(image)
        output.append(f"\n🖼️ Image Info:")
        output.append(f"Format: {fmt}")
        output.append(f"Dimensions: {width} x {height}")

    except Exception as e:
        output.append(f"❌ Error processing metadata: {e}")

    return "\n".join(output)
