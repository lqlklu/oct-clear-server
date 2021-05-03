import tensorflow as tf
import numpy as np

generator_g = tf.keras.models.load_model("generator_g")


def process_big(s: tf.Tensor) -> tf.Tensor:
    return tf.reshape(tf.divide(tf.add(tf.cast(s, dtype=tf.float32), -127.5), 127.5),
                      [1, s.shape[0], s.shape[1], 1])


def convert(s: tf.Tensor) -> tf.Tensor:
    return tf.reshape(tf.cast(tf.add(tf.multiply(s, 127.5), 127.5), dtype=tf.uint8),
                      [s.shape[0], s.shape[1], 1])


def generate_tensor(img: np.array, model) -> tf.Tensor:
    img = tf.convert_to_tensor(img, tf.float32)
    img = tf.reshape(img, [1, 256, 256, 1])
    img = model(img)
    return img


def concat(original_img, input_img, x, y):
    for i in range(x, x + input_img.shape[0]):
        for j in range(y, y + input_img.shape[1]):
            original_img[i][j] = input_img[i - x][j - y]


def cut_splice(img, model):
    img = process_big(img)
    img = img.numpy().squeeze()
    img_row = img.shape[0]
    img_col = img.shape[1]
    row = int(tf.math.ceil(tf.divide(img.shape[0], 256)))
    col = int(tf.math.ceil(tf.divide(img.shape[1], 256)))
    final_img = np.zeros((img.shape[0], img.shape[1]))
    for i in range(row):
        for j in range(col):
            if i < row - 1 and j < col - 1:
                result_img = generate_tensor(img[i * 256:i * 256 + 256, j * 256:j * 256 + 256], model)
                result_img = result_img.numpy().squeeze()
                concat(final_img, result_img, i * 256, j * 256)
            elif (j * 256 + 256) >= img_col and i < row - 1:
                result_img = generate_tensor(img[i * 256:i * 256 + 256, img_col - 256:img_col], model)
                result_img = result_img.numpy().squeeze()
                concat(final_img, result_img, i * 256, img_col - 256)
            elif (i * 256 + 256) >= img_row and j < col - 1:
                result_img = generate_tensor(img[img_row - 256:img_row, j * 256:j * 256 + 256], model)
                result_img = result_img.numpy().squeeze()
                concat(final_img, result_img, img_row - 256, j * 256)
            else:
                result_img = generate_tensor(img[img_row - 256:img_row, img_col - 256:img_col], model)
                result_img = result_img.numpy().squeeze()
                concat(final_img, result_img, img_row - 256, img_col - 256)
    return final_img


def denoise(uf, rf):
    img = tf.image.decode_image(tf.io.read_file(uf))

    r = cut_splice(img, generator_g)

    r = convert(r)
    tf.io.write_file(rf, tf.image.encode_png(r))
