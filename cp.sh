command rm -rf ./config
mkdir -p config
cp -R ~/.config/* config

command rm -rf ./home
mkdir -p home

cp ~/.bash_logout ./home
cp ~/.bash_profile ./home
cp ~/.bashrc ./home
cp ~/.xinitrc ./home
cp ~/.zshrc ./home
cp ~/.p10k.zsh ./home
