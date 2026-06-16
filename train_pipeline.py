# ==============================================================================
# 🔥 YANIK TESPİT SİSTEMİ - AÇIK KAYNAK MODEL EĞİTİM HATTI (TRAINING PIPELINE)
# Geliştirici: Ekin
# Mimari: YOLOv8 Nano (Orijinal GitHub Reposundan Derlenmiştir)
# ==============================================================================

print("🔄 Aşama 1: Açık Kaynak YOLOv8 Kaynak Kodu Klonlanıyor...")
# YOLOv8'in orijinal açık kaynak GitHub reposunu Colab'e çekiyoruz
!git clone https://github.com/ultralytics/ultralytics.git

# Klonladığımız klasörün içine girip kütüphaneyi kaynak kodundan (source) kuruyoruz
%cd ultralytics
!pip install -e .

print("🔄 Aşama 2: Gerekli Kütüphaneler İçe Aktarılıyor...")
import os
import shutil
import random
from ultralytics import YOLO

print("🔄 Aşama 3: Veri Seti Hazırlığı ve Klasör Mimarisi Kuruluyor...")
# Veri seti zip dosyasından çıkartılıyor (Eğer zaten çıkarttıysanız bu satırı silebilirsiniz)
# !unzip -q /content/archive.zip -d /content/yolo_veriseti/

# Mutlak dosya yolları kullanıyoruz (Çünkü ultralytics klasörünün içindeyiz)
src_dir = '/content/yolo_veriseti/'
base_dir = '/content/dataset/'

# YOLOv8'in zorunlu kıldığı klasör yapısı
os.makedirs(base_dir + 'train/images', exist_ok=True)
os.makedirs(base_dir + 'train/labels', exist_ok=True)
os.makedirs(base_dir + 'val/images', exist_ok=True)
os.makedirs(base_dir + 'val/labels', exist_ok=True)

# Görüntüleri bul ve karıştır (%80 Eğitim, %20 Doğrulama)
images = [f for f in os.listdir(src_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
random.shuffle(images)

split_idx = int(len(images) * 0.8)
train_imgs = images[:split_idx]
val_imgs = images[split_idx:]

def copy_files(img_list, split_name):
    for img in img_list:
        # Görseli taşı
        shutil.copy(os.path.join(src_dir, img), os.path.join(base_dir, f'{split_name}/images/{img}'))
        # Etiketi (.txt) taşı
        txt_name = img.rsplit('.', 1)[0] + '.txt'
        if os.path.exists(os.path.join(src_dir, txt_name)):
            shutil.copy(os.path.join(src_dir, txt_name), os.path.join(base_dir, f'{split_name}/labels/{txt_name}'))

copy_files(train_imgs, 'train')
copy_files(val_imgs, 'val')

print("📝 Aşama 4: data.yaml Dosyası Otomatik Oluşturuluyor...")
yaml_content = f"""
train: {base_dir}train/images
val: {base_dir}val/images

nc: 3
names: ['1. Derece Yanik', '2. Derece Yanik', '3. Derece Yanik']
"""
with open(os.path.join(base_dir, 'data.yaml'), 'w') as f:
    f.write(yaml_content)

print("🚀 Aşama 5: Klonlanan YOLOv8n İle Eğitim Başlatılıyor...")
# Kaynak kodundan derlediğimiz YOLOv8 Nano modeli çağrılıyor
model = YOLO('yolov8n.pt')

# Eğitim Parametreleri: Epoch=10, Image Size=224
model.train(data='/content/dataset/data.yaml', epochs=10, imgsz=224)

print("✅ Eğitim Başarıyla Tamamlandı! 'best.pt' modeli runs/detect/train/weights/ dizininde üretildi.")
