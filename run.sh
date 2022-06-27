source ./pyenv/bin/activate
echo "Launching bot..."
echo "----------------------"
if [[ -s "./token.txt" ]]; then
	python main.py
else
	echo "The token.txt file is empty. Insert the bot token to token.txt file and try again."
fi