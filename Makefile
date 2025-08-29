.PHONY: setup dev prod console asset-downloade distclean

setup:
	-brew install python pipx aria2
	-sudo apt install pipx aria2
	pipx install poetry
	pipx run poetry install

dev:
	pipx run poetry run poe dev

prod:
	PROD_FLAG=1 pipx run poetry run poe prod

console:
	pipx run poetry run console -i

asset-downloader:
	PROD_FLAG=1 pipx run poetry run asset-downloader

distclean:
	-pipx run poetry env remove python
	-git clean -dfx
