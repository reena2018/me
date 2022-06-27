import tensorflow as tf
import html
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pdfplumber
from docx2pdf import convert
import os
import pandas as pd
import pythoncom

# Create app
app = Flask(__name__)

class ReusableForm1(Form):
    """Document Classifier - DCNN Model"""
    #Document name
    docName = StringField(u'Enter document name:', validators=[
                     validators.InputRequired()])
    # Document content
    docContent = TextAreaField(u'Enter document content:', validators=[
                     validators.InputRequired()])
    
    # Submit button
    submit1 = SubmitField("Submit")

class ReusableForm2(Form):
    """Document Classifier - DCNN Model"""
    #Document name
    docFiles = MultipleFileField(u'', validators=[
                     validators.InputRequired()])
    
    # Submit button
    submit2 = SubmitField("Submit")
    
def load_dcnn_model():
    """Load in the pre-trained model"""
    global cnnmodel
    cnnmodel = load_model('DCNN_Model/dcnnmodel')
    

# Home page
@app.route("/index", methods=['GET', 'POST'])
def index():
    """Home page of app with form"""
    # Create form
    form1 = ReusableForm1(request.form)

    # Send template information to index.html
    return render_template('index.html', form=form1)

@app.route('/selectfiles', methods=['GET', 'POST'])
def selectfiles():
    # Create form
    form2 = ReusableForm2(request.form)
    docCategory=''
    data = []
    df = pd.DataFrame(data, columns=['File name', 'Category'])
    print(df)             
    return render_template('selectfiles.html', form=form2)

if __name__ == "__main__":
    app.run(debug=True)
