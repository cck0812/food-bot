import tensorflow as tf
import jieba
from tensorflow.keras.preprocessing import sequence 
import sys
import os


gpu = tf.config.experimental.list_physical_devices()[1]
tf.config.experimental.set_memory_growth(gpu,True)

jieba.set_dictionary('dictionary.txt')
model = tf.keras.models.load_model('Semantic_analysis.h5')

with open('word_frequency.txt','r',encoding='utf8') as f:
    word_frequency = dict(eval(f.read()))

def evaluate(data):
    temp = []
    cut = jieba.cut(data)
    for j in cut:
        try:
            temp.append(word_frequency[j])
        except:
            temp.append(0)
    test_data = sequence.pad_sequences([temp], maxlen=150)
    if model.predict_classes(test_data)[0][0] == 1:
        print('--------------------------')
        print('|        Positive        |')
        print('--------------------------')
    else:
        print('--------------------------')
        print('|        Negative        |')
        print('--------------------------')
        
if not os.isatty(sys.stdin.fileno()):
    test = sys.stdin.readlines()
    
else:
    print("Not a legal input.")

evaluate(test[0])