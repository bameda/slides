from urllib.parse import urljoin
import sys
import copy
import getpass
from datetime import datetime, timedelta

import requests
import pygal


BASE_HEADERS = {
    "content-type": "application/json; charset: utf8",
    "X-DISABLE-PAGINATION": "true",
}

API_HOST = "https://api.taiga.io/"

URLS = {
    "auth": "/api/v1/auth",
    "projects": "/api/v1/projects",
    "project":  "/api/v1/projects/{}",
    "project-issues-stats": "/api/v1/projects/{}/issues_stats",
}


if __name__ == "__main__":
    headers = copy.deepcopy(BASE_HEADERS)

    # Login
    username = input("Type your username or email:\n> ")
    password = getpass.getpass("Type your password:\n> ")

    url = urljoin(API_HOST, URLS["auth"])
    data = {
        "username": username,
        "password": password,
        "type": "normal"
    }
    response = requests.post(url, json=data, headers=headers)
    me = response.json()

    headers["Authorization"] = "Bearer {}".format(me["auth_token"])

    # List all my projects
    url = urljoin(API_HOST, URLS["projects"])
    params = {
        "member": me["id"]
    }
    response = requests.get(url, params=params, headers=headers)
    projects = response.json()

    project_list_display = "\n".join(
        ["  {} - {}".format(i, p["name"]) for i, p in enumerate(projects)]
    )
    index = int(input("Select project: \n{}\n> ".format(project_list_display)))
    project = projects[index]

    # Get issues stats data
    url = urljoin(API_HOST, URLS["project-issues-stats"].format(project["id"]))
    response = requests.get(url, headers=headers)
    issues_stats = response.json()

    # GRAPHS
    style = pygal.style.NeonStyle()
    style.background = "transparent"

    # Draw graph: Issues by status
    chart = pygal.Pie(show_legend=False, style=style)
    chart.title = 'Issues by Status in {}'.format(project["name"])
    for item in issues_stats["issues_per_status"].values():
        chart.add(item["name"], [{
            "value": item["count"],
            "color": item["color"]
        }])
    chart.render_to_file("../../output/chart_issues_by_status.svg")

    # Draw graph: Issues per Assigned to
    chart = pygal.HorizontalBar(style=style)
    chart.title = 'Issues by Assignation in {}'.format(project["name"])
    for item in issues_stats["issues_per_assigned_to"].values():
        if item["count"] > 0:
            chart.add(item["name"], item["count"])
    chart.render_to_file("../../output/chart_issues_by_assigned_to.svg")

    # Draw graph: Issues open/closed last month
    today = datetime.today()
    last_four_weeks = [today - timedelta(days=x) for x in range(28, 0, -1)]

    chart = pygal.Dot(x_label_rotation=30, style=style)
    chart.title = 'Issues Open/Closed last 4 weeks in {}'.format(project["name"])
    chart.x_labels = [d.strftime('%Y %b %d') for d in last_four_weeks]
    chart.add("Open",
              issues_stats["last_four_weeks_days"]["by_open_closed"]["open"])
    chart.add("Closed",
              issues_stats["last_four_weeks_days"]["by_open_closed"]["closed"])
    chart.render_to_file("../../output/chart_issues_open_close_last_4_weeks.svg")
