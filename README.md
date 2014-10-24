skewer
=======

The Skew ElasticSearch Repo

Skewer uses skew to enumerate AWS resources and then indexes those resources
into ElasticSearch.

Installation
------------

Install skewer using pip:

    $ pip install skewer

Once installed, configure your AWS config file as described in the
[skew README](https://github.com/scopely-devops/skew/blob/develop/README.md)
so skew can associate your AWS account IDs with the right profile in your
config file.

Finally, run skewer:

    $ skewer index --host <name of ElasticSearch host> --port 9200

This will use skew to enumerate all resources matching the ARN pattern

    arn:aws:*:*:*:*/*

and will send the JSON data associated with each resource to the specified
ElasticSearch server for indexing.  A new index will be created named
``skewer-<timestamp>`` and an index alias will also be created called
``skewer``.

Running:

    $ skewer --help

will print out help for the ``skewer`` cli tool.