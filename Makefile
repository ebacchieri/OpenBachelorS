.PHONY: setup dev prod console asset-downloade

setup:
	brew install python pipx aria2
	pipx install poetry
	pipx run poetry install

dev:
	pipx run poetry run poe dev

prod:
	PROD_FLAG=1 python -m pipx run poetry run poe prod

console:
	pipx run poetry run console -i

asset-downloader:
	pipx run poetry run asset-downloader
