
Look at the "example_settings" file. It contains a number of settings, which
need to be passed to Django via environment variables.

These settings (from that file) are only considered for your own personal test
runs, they will be different for deployments.

If you don't mind having your own personal test settings exposed in version
control, go right ahead and edit that file. However, it might be easier to just
make a copy of it, which you can edit as needed.

Usage:

        $ source example_settings
        $ python manage.py runserver



