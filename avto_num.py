import matplotlib.pyplot as plt
import pytesseract
from PIL import Image
import cv2
################################# Фото фиксация ####################################
def save_image_on_car():# Функция сохранения с камеры кадра(Скрин)
    with open('camera.txt', 'r') as camera:#  Открывает файл 'camera.txt' в режиме чтения
        cam_num = camera.read()# читает содержимое файла 'camera.txt'
    cap = cv2.VideoCapture(int(cam_num))# cv2.VideoCapture предоставляет доступ к видеопотоку с указанной камеры.

    for i in range(30):# Запускаем цикл
        cap.read()# считываем кадр из видеопатока
    ret, frame = cap.read()# считываем кадр из видеопатока и присваиваем переменную frame
    a = cv2.imwrite('cars/cam.png', frame)# Сохраняем кадр в cam.png
    cap.release()#  освобождает ресурсы, связанные с объектом cap
################################ ############################
pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR\\tesseract.exe'
tessdata_dir_config = r'--tessdata-dir "Tesseract-OCR\tessdata"'

def read_text_in_photo(image_input):# Принимаем в функцию изображение
    image = Image.open(image_input)# Присваеваем переменнной открытие изображения
    text = pytesseract.image_to_string(image, lang='rus', config=tessdata_dir_config) # В переменной извлекаем текст из изображения через функцию pytesseract.image_to_string
    with open('text.txt', 'w', encoding='UTF-8') as file: # Откроем файл
        file.write(text)# Записываем в файл полученый текст из переменной text

def open_img(img_path):
    carplate_img = cv2.imread(img_path)
    carplate_img = cv2.cvtColor(carplate_img, cv2.COLOR_BGR2RGB)
    plt.axis('off')
    plt.imshow(carplate_img)
    return carplate_img


def carplate_extract(image, carplate_haar_cascade):
    carplate_rects = carplate_haar_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
    # carplate_img = None

    for x, y, w, h in carplate_rects:
        carplate_img = image[y + 15:y + h - 10, x + 15:x + w - 20]

    return carplate_img


def enlarge_img(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    plt.axis('off')
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    return resized_image


def main():
    # save_image_on_car()
    # carplate_img_rgb = open_img(img_path='cars/cam.png')
    carplate_img_rgb = open_img(img_path='cars/6.jpg')


    carplate_haar_cascade = cv2.CascadeClassifier('hear_cascades/haarcascade_russian_plate_number.xml')

    carplate_extract_img = carplate_extract(carplate_img_rgb, carplate_haar_cascade)
    carplate_extract_img = enlarge_img(carplate_extract_img, 150)
    plt.imshow(carplate_extract_img)

    carplate_extract_img_gray = cv2.cvtColor(carplate_extract_img, cv2.COLOR_RGB2GRAY)
    plt.axis('off')
    plt.imshow(carplate_extract_img_gray, cmap='gray')
    plt.show()

    num_car = pytesseract.image_to_string(
        carplate_extract_img_gray,
        config='--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789').strip()

    print('Номер авто: ', pytesseract.image_to_string(
        carplate_extract_img_gray,
        config='--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
          )
    number_cars = num_car
    return number_cars


if __name__ == '__main__':
    main()
