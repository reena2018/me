{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "   WARNING: This is a development server. Do not use it in a production deployment.\n",
      "   Use a production WSGI server instead.\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Running on http://0.0.0.0:9090/ (Press CTRL+C to quit)\n",
      "127.0.0.1 - - [27/Jun/2022 15:58:30] \"\u001b[33mGET /selecftfiles HTTP/1.1\u001b[0m\" 404 -\n",
      "127.0.0.1 - - [27/Jun/2022 15:58:30] \"\u001b[33mGET /favicon.ico HTTP/1.1\u001b[0m\" 404 -\n",
      "127.0.0.1 - - [27/Jun/2022 15:58:38] \"\u001b[37mGET /selectfiles HTTP/1.1\u001b[0m\" 200 -\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Empty DataFrame\n",
      "Columns: [File name, Category]\n",
      "Index: []\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "127.0.0.1 - - [27/Jun/2022 15:58:39] \"\u001b[37mGET /static/css/main.css HTTP/1.1\u001b[0m\" 200 -\n",
      "127.0.0.1 - - [27/Jun/2022 15:58:39] \"\u001b[33mGET /static/images/script_background.png HTTP/1.1\u001b[0m\" 404 -\n"
     ]
    }
   ],
   "source": [
    "from flask import Flask, render_template, request\n",
    "from wtforms import (Form, FileField, StringField, TextAreaField, validators, SubmitField, IntegerField, MultipleFileField)\n",
    "from keras.models import load_model\n",
    "import tensorflow as tf\n",
    "import html\n",
    "import nltk\n",
    "from nltk.corpus import stopwords\n",
    "from nltk.tokenize import word_tokenize\n",
    "from keras.preprocessing.text import Tokenizer\n",
    "from keras.preprocessing.sequence import pad_sequences\n",
    "import pandas as pd\n",
    "from sklearn.preprocessing import LabelEncoder\n",
    "import pdfplumber\n",
    "from docx2pdf import convert\n",
    "import os\n",
    "import pandas as pd\n",
    "import pythoncom\n",
    "\n",
    "# Create app\n",
    "app = Flask(__name__)\n",
    "\n",
    "class ReusableForm1(Form):\n",
    "    \"\"\"Document Classifier - DCNN Model\"\"\"\n",
    "    #Document name\n",
    "    docName = StringField(u'Enter document name:', validators=[\n",
    "                     validators.InputRequired()])\n",
    "    # Document content\n",
    "    docContent = TextAreaField(u'Enter document content:', validators=[\n",
    "                     validators.InputRequired()])\n",
    "    \n",
    "    # Submit button\n",
    "    submit1 = SubmitField(\"Submit\")\n",
    "\n",
    "class ReusableForm2(Form):\n",
    "    \"\"\"Document Classifier - DCNN Model\"\"\"\n",
    "    #Document name\n",
    "    docFiles = MultipleFileField(u'', validators=[\n",
    "                     validators.InputRequired()])\n",
    "    \n",
    "    # Submit button\n",
    "    submit2 = SubmitField(\"Submit\")\n",
    "    \n",
    "def load_dcnn_model():\n",
    "    \"\"\"Load in the pre-trained model\"\"\"\n",
    "    global cnnmodel\n",
    "    cnnmodel = load_model('DCNN_Model/dcnnmodel')\n",
    "    \n",
    "\n",
    "# Home page\n",
    "@app.route(\"/index\", methods=['GET', 'POST'])\n",
    "def index():\n",
    "    \"\"\"Home page of app with form\"\"\"\n",
    "    # Create form\n",
    "    form1 = ReusableForm1(request.form)\n",
    "\n",
    "    # Send template information to index.html\n",
    "    return render_template('index.html', form=form1)\n",
    "\n",
    "@app.route('/selectfiles', methods=['GET', 'POST'])\n",
    "def selectfiles():\n",
    "    # Create form\n",
    "    form2 = ReusableForm2(request.form)\n",
    "    docCategory=''\n",
    "    data = []\n",
    "    df = pd.DataFrame(data, columns=['File name', 'Category'])\n",
    "    print(df)             \n",
    "    return render_template('selectfiles.html', form=form2)\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run(debug=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Collecting wtforms\n",
      "  Downloading WTForms-3.0.1-py3-none-any.whl (136 kB)\n",
      "Requirement already satisfied: MarkupSafe in c:\\users\\reena\\anaconda3\\lib\\site-packages (from wtforms) (1.1.1)\n",
      "Installing collected packages: wtforms\n",
      "Successfully installed wtforms-3.0.1\n"
     ]
    }
   ],
   "source": [
    "!pip install wtforms"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Collecting pdfplumber\n",
      "  Downloading pdfplumber-0.7.1-py3-none-any.whl (39 kB)\n",
      "Collecting Wand>=0.6.7\n",
      "  Downloading Wand-0.6.7-py2.py3-none-any.whl (139 kB)\n",
      "Collecting Pillow>=9.1\n",
      "  Downloading Pillow-9.1.1-cp38-cp38-win_amd64.whl (3.3 MB)\n",
      "Collecting pdfminer.six==20220524\n",
      "  Downloading pdfminer.six-20220524-py3-none-any.whl (5.6 MB)\n",
      "Collecting charset-normalizer>=2.0.0\n",
      "  Downloading charset_normalizer-2.1.0-py3-none-any.whl (39 kB)\n",
      "Collecting cryptography>=36.0.0\n",
      "  Downloading cryptography-37.0.2-cp36-abi3-win_amd64.whl (2.4 MB)\n",
      "Requirement already satisfied: cffi>=1.12 in c:\\users\\reena\\anaconda3\\lib\\site-packages (from cryptography>=36.0.0->pdfminer.six==20220524->pdfplumber) (1.14.3)\n",
      "Requirement already satisfied: pycparser in c:\\users\\reena\\anaconda3\\lib\\site-packages (from cffi>=1.12->cryptography>=36.0.0->pdfminer.six==20220524->pdfplumber) (2.20)\n",
      "Installing collected packages: Wand, Pillow, charset-normalizer, cryptography, pdfminer.six, pdfplumber\n",
      "  Attempting uninstall: Pillow\n",
      "    Found existing installation: Pillow 8.0.1\n",
      "    Uninstalling Pillow-8.0.1:\n",
      "      Successfully uninstalled Pillow-8.0.1\n",
      "  Attempting uninstall: cryptography\n",
      "    Found existing installation: cryptography 3.1.1\n",
      "    Uninstalling cryptography-3.1.1:\n",
      "      Successfully uninstalled cryptography-3.1.1\n",
      "Successfully installed Pillow-9.1.1 Wand-0.6.7 charset-normalizer-2.1.0 cryptography-37.0.2 pdfminer.six-20220524 pdfplumber-0.7.1\n"
     ]
    }
   ],
   "source": [
    "!pip install pdfplumber"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Collecting docx2pdf\n",
      "  Downloading docx2pdf-0.1.8-py3-none-any.whl (6.7 kB)\n",
      "Requirement already satisfied: tqdm>=4.41.0 in c:\\users\\reena\\anaconda3\\lib\\site-packages (from docx2pdf) (4.50.2)\n",
      "Requirement already satisfied: pywin32>=227; sys_platform == \"win32\" in c:\\users\\reena\\anaconda3\\lib\\site-packages (from docx2pdf) (227)\n",
      "Installing collected packages: docx2pdf\n",
      "Successfully installed docx2pdf-0.1.8\n"
     ]
    }
   ],
   "source": [
    "!pip install docx2pdf"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
