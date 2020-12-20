[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- ABOUT THE PROJECT -->
## About The Project

[![Sanay][product-screenshot]](https://example.com)
Sanay, is a web-based chat application that provides social cues for those that find it difficult through sentiment analysis. The LSTM Keras Model has been trained on a dataset of 1.6 M tweets, achieving a 78.95% sentiment classification accuracy.

Play around with the model [here](https://github.com/kishdubey/sanay-streamlit).
Check out the notebook for the model [here](https://github.com/kishdubey/sanay/blob/master/sanay/keras_model/sanay_sentiment_analysis.ipynb).

video-based chat application with sentiment analysis coming soon!
<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* pip3
  ```sh
  sudo apt install python3-pip
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/kishdubey/sanay
   ```
2. Install packages
   ```sh
   pip3 install -r requirements.txt
   ```
3. Enter your SQLAlchemy URI in `app.py`
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = "YOUR URI"
   ```
4. Run Sanay
   ```python
   python3 app.py
   ```




<!-- USAGE EXAMPLES -->
## Usage

Register, Login, and Chat away.

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Kish Dubey - kdube076@uottawa.ca 

Project Link: https://github.com/kishdubey/sanay

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Sentiment140 Dataset](https://www.kaggle.com/kazanova/sentiment140)
* [Frontend from Sandeep Sudhakaran](https://github.com/sandeepsudhakaran/rchat-app)
* [README template](https://github.com/othneildrew/Best-README-Template)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/kishdubey/sanay/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/kishdubey/sanay/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/kishdubey/sanay/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/kishdubey/
[product-screenshot]: sanay/static/images/demo.png
