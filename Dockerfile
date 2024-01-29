FROM python:3.11-bookworm

RUN useradd -m horse
RUN mkdir /srv/horse
RUN chown -R horse:horse /srv/horse

COPY --chown=horse:horse . /srv/horse
USER horse

WORKDIR /srv/horse
RUN python3 -m pip install -r requirements.txt

CMD [ "/usr/bin/env", "python3", "./main.py" ]