---
title: Getting Started
tags: 
 - jekyll
 - github
description: Getting started with the template
---

# Getting Started

The documentation here will get you started to use the tunel-django template, developed
with Python and Django. This is intended for developers. If you want to see
the user documentation, see [the user guide]({{ site.baseurl }}/user-guide/).

## Setup

To locally (if you are developing) you'll want to clone the project:

```bash
$ git clone https://github.com/vsoch/tunel-django
$ cd tunel-django
```

### Configuration

The application has a set of configuration variables that are discovered in the environment
or in the `settings.yaml` found in the root, which can be edited before build or bound to
the container (in the same spot) at runtime.

#### Authentication 

The interface currently assumes that the "backend" (ability to log in) is done via
invite only, and so the typical registration form is not provided. If you would like help
to add a standard registration form or other forms of authentication (social auth, SAML, etc.)
please [ask for this feature]({{ site.repo }}/issues).
This means that an administrator is responsible for adding new users. 

### SendGrid

We use SendGrid to invite users to the site. Note that the emails can sometimes
end up in spam, so you should be prepared to notify invitees of this.

#### SendGrid Sender Email

You'll need a `SENDGRID_SENDER_EMAIL` exported in your .env file in order to use
SendGrid:

```
export SENDGRID_SENDER_EMAIL=myemail@domain.com
```

If this is the same as your `HELP_CONTACT_EMAIL` you can leave it blank, and the help
contact email will be used. **Important** before using the API this email needs to be added as a known [Sender](https://app.sendgrid.com/settings/sender_auth/senders). If it is not, you will get a permission denied error. You
also likely want to go to Settings -> Tracking and disable link tracking in email.

#### SendGrid Account

To send emails from the server, we use SendGrid. This means
that you need to [sign up](https://app.sendgrid.com/) for an account (the basic account with 100 emails
per day is free) and then add the `SENDGRID_API_KEY` to your .env file:

```python
export SENDGRID_API_KEY=xxxxxxxxxxxxxxx
```

Then to create your key:

 1. Go to [SendGrid](https://app.sendgrid.com/) and click on Settings -> Api keys in the left bar
 2. Click the blue button to "Create API key"
 3. Give your key a meaningful name (e.g., freegenes_dev_test)
 4. Choose "Restricted Access" and give "Full Access" to mail send by clicking the bar on the far right circle.
 5. Copy it to a safe place, likely your settings/config.py (it is only shown once!)

If the value is found to be None, emails will not be sent.


### Rate Limits

It's hard to believe that anyone would want to maliciously issue requests to your server,
but it's unfortunately a way of life. For this reason, all views have a rate limit, along
with blocking ip addresses that exceed it (for the duration of the limit, one day). You
can customize this:

```python
VIEW_RATE_LIMIT="50/1d"  # The rate limit for each view, django-ratelimit, "50 per day per ipaddress)
VIEW_RATE_LIMIT_BLOCK=True # Given that someone goes over, are they blocked for the period?
```
And see the [django-ratelimit](https://django-ratelimit.readthedocs.io/en/v1.0.0/usage.html) documentation
for other options. 

## Development

To develop locally, you'll want to build the containr:

```bash
$ docker build -t tunel-django .
```

And then run the container, binding the $PWD to `/code` if you want to develop.
And note that since we are using Docker, will will also be binding the socket to
our local machine:

```bash
$ mkdir ./tmp
$ docker run --rm -it -v $PWD:/code -v $PWD/static:/var/www/static -p 8000:8000 --name tunel tunel-django
```

We have to bind the PWD static to where nginx can generally see them.
Open your browser to [http://localhost:8000](http://localhost:8000)
To execute a command to the container (in another terminal):

```bash
$ docker exec -it tunel python3 /code/manage.py collectstatic --noinput
25 static files copied to '/var/www/static', 156 unmodified.
```

### Database

For our database, we use sqlite to easily work on HPC. However, if you have access
to a different relational database, you can update this in your settings.py file.
Ensure that credentials are not included in any code you push to GitHub!
If you ever need to delete and refresh this local testing database, you can do:

```bash
rm db.sqlite3
```

Migrations are performed at app start.

### Models

The core of any Django application is the definition of [models](https://docs.djangoproject.com/en/3.0/topics/db/models/).
A model maps directly to a database table, so when you originally design your application, you will
want to spend some time on this design. The current application creates dummy models for users, an organization,
and then associated projects. You can also imagine having models for a biological entity, or some kind
of machine learning model.  Please reach out to [@vsoch]({{ site.repo }}/issues) if you want any help
designing your models.


### Sentry for Monitoring

We can create a few account on [sentry.io](https://sentry.io/) to set up logging
for our application, and be alerted if there are any errors. The steps there will
walk you through setup, although you primarily just need to export the id number
as `SENTRY_ID` in your local .env and app.yaml.

```bash
export SENTRY_ID=https://xxxxxxxxxxxxxxxxxxxxxxxxxxx.ingest.sentry.io/111111
```

Don't add this until you are ready to start getting error reports (e.g., when testing locally
and Debug modeis true you don't need it).



### Testing

You can write tests for your models, and an example is provided in the repository "tests" folder.
You can run tests locally after sourcing your environent, and using the `manage.py test` command.

```bash
source env/bin/activate
docker exec -it tunel python3 /code/manage.py test tests.test_project
```

You can see the [Django docs for testing](https://docs.djangoproject.com/en/3.0/topics/testing/overview/) for more details.

### Deployment

**coming soon**
