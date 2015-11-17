#!/usr/bin/env python

import getpass
from datetime import datetime, timedelta

from taiga import TaigaAPI
import pygal


API_HOST = "https://api.taiga.io/"


if __name__ == "__main__":
    api = TaigaAPI(host=API_HOST)

    # Login
    username = input("Type your username or email:\n> ")
    password = getpass.getpass("Type your password:\n> ")

    api.auth(username=username, password=password)
    me = api.me()

    # List all my projects
    projects = api.projects.list(member=me.id)

    project_list_display = "\n".join(
        ["  {} - {}".format(i, p.name) for i, p in enumerate(projects)]
    )
    index = int(input("Select project: \n{}\n> ".format(project_list_display)))
    project = projects[index]

    # Get issues stats data
    issues_stats = project.issues_stats()

    # GRAPHS
    style = pygal.style.NeonStyle()
    style.background = "transparent"

    # Draw graph: Issues by status
    chart = pygal.Pie(show_legend=False, style=style)
    chart.title = "Issues by Status in {}".format(project.name)
    for item in issues_stats["issues_per_status"].values():
        chart.add(item["name"], [{
            "value": item["count"],
            "color": item["color"]
        }])
    chart.render_to_file("../../output/chart_issues_by_status.v2.svg")
    print("Generate graph: 'Issues by Status in {}'".format(project.name))

    # Draw graph: Issues per Assigned to
    chart = pygal.HorizontalBar(style=style)
    chart.title = "Issues by Assignation in {}".format(project.name)
    for item in issues_stats["issues_per_assigned_to"].values():
        if item["count"] > 0:
            chart.add(item["name"], item["count"])
    chart.render_to_file("../../output/chart_issues_by_assigned_to.v2.svg")
    print("Generate graph: 'Issues by Assignation in {}'".format(project.name))

    # Draw graph: Issues open/closed last month
    today = datetime.today()
    last_four_weeks = [today - timedelta(days=x) for x in range(28, 0, -1)]

    chart = pygal.Dot(x_label_rotation=30, style=style)
    chart.title = "Issues Open/Closed last 4 weeks in {}".format(project.name)
    chart.x_labels = [d.strftime("%Y %b %d") for d in last_four_weeks]
    chart.add("Open",
              issues_stats["last_four_weeks_days"]["by_open_closed"]["open"])
    chart.add("Closed",
              issues_stats["last_four_weeks_days"]["by_open_closed"]["closed"])
    chart.render_to_file("../../output/chart_issues_open_close_last_4_weeks.v2.svg")
    print("Generate graph: 'Issues Open/Closed last 4 weeks in {}'".format(project.name))
