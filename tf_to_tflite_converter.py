#Converting tf.keras models
#tensorflow 1.X implementation
import tensorflow as tf
converter = tf.lite.TFLiteConverter.from_keras_model_file('/content/Fire-64x64-color-v7-soft.h5')
tfmodel = converter.convert()
#saving tflite model
open("fire_lite_model.tflite","wb").write(tfmodel)

#tensorflow 2.X implementation
import tensorflow as tf
model = tf.keras.models.load_model('C:/Users/samar/fireDet/Fire-64x64-color-v7-soft.h5')
# Convert the model.
converter = tf.lite.TFLiteConverter.from_keras_model(model)
#save tflite model
tflite_model = converter.convert()
open("model.tflite","wb").write(tflite_model)