from tensorflow.keras.models import load_model
import tensorflow as tf
from PIL import Image
import numpy as np
import keras

# global char_
# char_ =['u', '7', '9', 'a', 'U', 'y', 'R', 'n', 'H', 'b', '6', 's', 'm', 'C', '2', 'h', 'v', 'j', 'c', 'T', 'q', 'B', 'K', 'P', 'd', 'f', 'Q', 'g', 'r', 'X', 'G', '8', 'S', 't', 'V', '3', '4', 'x', 'z', 'F', '5', 'Z', 'p', 'e', 'k']

# decode
def decode_batch_predictions(pred, char_ = ['u', '7', '9', 'a', 'U', 'y', 'R', 'n', 'H', 'b', '6', 's', 'm', 'C', '2', 'h', 'v', 'j', 'c', 'T', 'q', 'B', 'K', 'P', 'd', 'f', 'Q', 'g', 'r', 'X', 'G', '8', 'S', 't', 'V', '3', '4', 'x', 'z', 'F', '5', 'Z', 'p', 'e', 'k']):
    max_length = 5
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    # Use greedy search. For complex tasks, you can use beam search
    results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][
        :, :max_length
    ]
    # Iterate over the results and get back the text
    output_text = ''
    #conver to text
    for res in results:
        res = np.array(res)
        for r in res:
            try:
                output_text += char_[int(r)]
            except:
                output_text += '_'
    return output_text

# predict
def predict(img):	
	# load the model from file
	model = load_model(r'.\services\Pred_Capthcha_t1v1\\Model\model_PredictCaptcha.h5', compile=False)
	img = img.convert('L').resize((145, 50))
	img = np.array(img)
	img = img.reshape(50, 145, 1)

	new_img = tf.expand_dims(img,0)
	new_img = new_img / 255
	preds = model.predict(new_img)
	pred_texts = decode_batch_predictions(preds)
    
	return pred_texts