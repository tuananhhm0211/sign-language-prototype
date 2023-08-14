## 1. The goal of the project
* Create a demo using word embedding and JASigning to translate spoken vietnamese to sign language
* Explore the possibility of using Large Language Model to generate sign language
* Build knowledge about the Vietnamese sign language

## 2. Setup step
* Install python 3.8.5
* Install poetry
* Install gcloud cli to setup Google Cloud account
* Run command `poetry install` to install dependencies
* Run command `poetry shell` to activate virtual environment
* Create .env file and OPENAI_API_KEY=your_api_key to the file
* Modify config.py to change the config: need absolute path to file
* Run command `python3 spl2videos.py` to test app
Output res.xml in output folder: copy the content to the website [JASigning](https://vhg.cmp.uea.ac.uk/tech/jas/vhg2023/CWASA-plus-gui-panel.html) to see the result


## 3. Contributors
* [Minh Hang](dangminhhang261102.dn@gmail.com) - VNU University of Engineering and Technology
* [Son Tung](hasontung1772003@gmail.com) - VNU University of Engineering and Technology
* [Tuan Anh](tuananhhhm@gmail.com) - VNU University of Engineering and Technology
* [Le Thu Phuong](lethuphuong01032004@gmail.com) - University of Massachusetts Amherst
* [Le Cong Thuong](thuonglc@vnu.edu.vn) - VNU University of Engineering and Technology