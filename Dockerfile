FROM python:3.8-alpine

WORKDIR /usr/src/app

ENV DJANGO_SETTINGS_MODULE=spicystores.deploy_settings

# Install Node.JS and build tools
RUN apk --no-cache add nodejs npm build-base musl-dev linux-headers

# Install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt uwsgi

# Copy app
COPY . .

# Build customer site
WORKDIR /usr/src/app/CustomerSite
RUN npm i && npm run build
WORKDIR /usr/src/app

# Collect static files
RUN python manage.py collectstatic --noinput --clear

EXPOSE 8080

ENTRYPOINT [ "uwsgi", "--ini", "uwsgi.ini" ]