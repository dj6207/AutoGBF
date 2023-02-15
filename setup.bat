git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt
pip uninstall torch -y
pip uninstall torchvision -y
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
cd ..
PAUSE