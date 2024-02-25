FROM python:3.11-bookworm
RUN pip install pipenv

RUN useradd -m horse
RUN mkdir /srv/horse
RUN chown -R horse:horse /srv/horse

COPY --chown=horse:horse . /srv/horse

USER horse
WORKDIR /srv/horse
RUN pipenv install --system

CMD [ "/usr/bin/env", "python3", "./main.py" ]