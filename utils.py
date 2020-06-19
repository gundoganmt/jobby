import os

def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
        for root_path, dirs, files in os.walk(folder)
        for f in files))

ALLOWED_IMG_EXTENSIONS = {'jpeg', 'jpg', 'png'}
ALLOWED_OFFER_EXTENSIONS = {'jpeg', 'jpg', 'png', 'pdf', 'zip'}

UPLOAD_IMG_FOLDER = os.path.join(os.getcwd(), 'jobby/static/images')
UPLOAD_OFFER_FOLDER = os.path.join(os.getcwd(), 'jobby/static/files')

def allowed_img_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMG_EXTENSIONS

def allowed_offer_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_OFFER_EXTENSIONS

def get_extension(filename):
    return '.'+ filename.rsplit('.', 1)[1].lower()

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))
