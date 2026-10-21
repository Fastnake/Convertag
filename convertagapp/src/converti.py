import os
from PIL import Image
import rawpy                         
from pillow_heif import register_heif_opener  

register_heif_opener()

def converted(file_path: str, extex: str, quality=90):

    extex = extex.lower().lstrip('.')
    
    if not file_path or not os.path.exists(file_path):
        return "Ошибка, ваш файл не найден"
    
    file_dir = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    pure_name, exten = os.path.splitext(filename)
    exten = exten.lower()
    
    output_dir = os.path.join(file_dir, "converted")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    ex_filename = f"{pure_name}.{extex}"
    ex_path = os.path.join(output_dir, ex_filename)

    try:
        if exten in (".nef", ".cr2", ".arw"):
            with rawpy.imread(file_path) as raw:
                rgb_data = raw.postprocess(use_camera_wb=True)
            img = Image.fromarray(rgb_data)
        else:
            img = Image.open(file_path)

        if extex in ("jpg", "jpeg", "jfif") and exten in (".png", ".webp", ".jfif", ".jpeg", ".heic", ".nef", ".cr2", ".arw"):
            if img.mode in ("RGBA", "LA") or (img.mode == "P" and 'transparency' in img.info):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img_to_save = background
            else:         
                img_to_save = img.convert("RGB")
                
        elif extex == "webp" and exten in (".png", ".heic", ".webp"):
            if img.mode in ("RGBA", "LA") or (img.mode == "P" and 'transparency' in img.info):
                img_to_save = img.convert("RGBA")
            else:         
                img_to_save = img.convert("RGB")
                
        elif extex == "webp" and exten in (".jpg", ".jpeg", ".jfif", ".nef", ".cr2", ".arw"):         
            img_to_save = img.convert("RGB")

        else:
            if img.mode in ("RGBA", "LA"):
                img_to_save = img.convert("RGBA")
            else:
                img_to_save = img.convert("RGB")

        if extex in ("jpg", "jpeg", "jfif"):
            img_to_save.save(ex_path, "JPEG", quality=quality)
        elif extex == "webp":
            img_to_save.save(ex_path, "WEBP", quality=quality if img_to_save.mode == "RGB" else 100)
        else:
            img_to_save.save(ex_path, "PNG")

        if img_to_save != img:
            img_to_save.close()
        img.close()

        return f"Успешно конвертировано: {filename} -> {ex_filename}"

    except Exception as e:
        return f"Произошла ошибка с {filename}: {e}"