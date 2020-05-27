from app import create_app

application = create_app()


@application.cli.command()
def routes():
    """List the routes."""
    import urllib

    output = []
    for rule in application.url_map.iter_rules():
        methods = ",".join(rule.methods)
        line = urllib.parse.unquote("{:40s} {:30s} {}".format(rule.endpoint, methods, rule))
        output.append(line)

    for line in sorted(output):
        print(line)
