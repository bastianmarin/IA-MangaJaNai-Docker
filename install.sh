# 0. Update apt, upgrade, and install dependencies
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y git wget unzip build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev

# 1. Install Python 3.12
if ! command -v python3.12 &> /dev/null; then
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt-get update
    sudo apt-get install -y python3.12 python3.12-venv
fi

# 2. Install pip for Python 3.12
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.12

# 3. Upgrade pip and install required Python packages globally
sudo python3.12 -m pip install --upgrade pip

# 4. Clone the IA-MangaJaNai-CLI repository
if [ ! -d "IA-MangaJaNai-CLI" ]; then
    git clone https://github.com/bastianmarin/IA-MangaJaNai-CLI.git
fi
cd IA-MangaJaNai-CLI

# 5. Download models if not present
if [ ! -d "models" ]; then
    mkdir models
    wget -O models/IllustrationJaNai_V1_ModelsOnly.zip https://github.com/the-database/MangaJaNai/releases/download/1.0.0/IllustrationJaNai_V1_ModelsOnly.zip
    wget -O models/MangaJaNai_V1_ModelsOnly.zip https://github.com/the-database/MangaJaNai/releases/download/1.0.0/MangaJaNai_V1_ModelsOnly.zip
    unzip models/IllustrationJaNai_V1_ModelsOnly.zip -d models
    unzip models/MangaJaNai_V1_ModelsOnly.zip -d models
fi

# 6. Install the required Python packages globally
sudo python3.12 -m pip install -r ../requirements.txt
sudo python3.12 -m pip install -r requirements.txt

# 7. Install torch and torchvision NVIDIA CUDA 12.1 globally
sudo python3.12 -m pip install torch==2.2.1+cu121 torchvision==0.17.1+cu121 --index-url https://download.pytorch.org/whl/cu121