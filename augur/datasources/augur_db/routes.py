#SPDX-License-Identifier: MIT
"""
Creates routes for the Augur database data source plugin
"""

from flask import request, Response

def create_routes(server):

    augur_db = server._augur['augur_db']()

    @server.app.route('/{}/repo-groups'.format(server.api_version))
    def get_repo_groups(): #TODO: make this name automatic - wrapper?
        drs = server.transform(augur_db.repo_groups)
        return Response(response=drs,
                        status=200,
                        mimetype="application/json")
    server.updateMetricMetadata(function=augur_db.repo_groups, endpoint='/{}/repo-groups'.format(server.api_version), metric_type='git')

    @server.app.route('/{}/repos'.format(server.api_version))
    def downloaded_repos():
        drs = server.transform(augur_db.downloaded_repos)
        return Response(response=drs,
                        status=200,
                        mimetype="application/json")

    server.updateMetricMetadata(function=augur_db.downloaded_repos, endpoint='/{}/repos'.format(server.api_version), metric_type='git')


    @server.app.route('/{}/repos/<owner>/<repo>'.format(server.api_version))
    def get_repo(owner, repo):
        a = [owner, repo]
        gre = server.transform(augur_db.get_repo, args = a)
        return Response(response=gre,
                        status=200,
                        mimetype="application/json")

    server.updateMetricMetadata(function=augur_db.get_repo, endpoint='/{}/repos/<owner>/<repo>'.format(server.api_version), metric_type='git')

    #####################################
    ###           EVOLUTION           ###
    #####################################
    server.addRepoGroupMetric(augur_db.open_issues_count, 'open-issues-count')
    server.addRepoMetric(augur_db.open_issues_count, 'open-issues-count')

    server.addRepoGroupMetric(augur_db.closed_issues_count, 'closed-issues-count')
    server.addRepoMetric(augur_db.closed_issues_count, 'closed-issues-count')

    """
    @api {get} /repo-groups/:repo_group_id/code-changes
    @apiName Code Changes
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/Code_Changes.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID
    @apiParam {string} period Periodicity specification. Possible values: 'day', 'week', 'month', 'year'. Defaults to 'day'
    @apiParam {string} begin_date Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:0'
    @apiParam {string} end_date Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "commit_date": "2018-01-01T00:00:00.000Z",
                            "repo_id": 1,
                            "commit_count": 5140
                        },
                        {
                            "commit_date": "2019-01-01T00:00:00.000Z",
                            "repo_id": 1,
                            "commit_count": 711
                        },
                        {
                            "commit_date": "2015-01-01T00:00:00.000Z",
                            "repo_id": 25001,
                            "commit_count": 1071
                        }
                    ]
    """
    server.addRepoGroupMetric(augur_db.code_changes, 'code-changes')

    """
    @api {get} /repo-groups/:repo_group_id/repos/:repo_id/code-changes
    @apiName Code Changes
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/Code_Changes.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID.
    @apiParma {String} repo_id Repository ID.
    @apiParam {string} period Periodicity specification. Possible values: 'day', 'week', 'month', 'year'. Defaults to 'day'
    @apiParam {string} begin_date Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:0'
    @apiParam {string} end_date Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "commit_date": "2018-01-01T00:00:00.000Z",
                            "commit_count": 2287
                        },
                        {
                            "commit_date": "2018-02-01T00:00:00.000Z",
                            "commit_count": 1939
                        },
                        {
                            "commit_date": "2018-03-01T00:00:00.000Z",
                            "commit_count": 1979
                        },
                        {
                            "commit_date": "2018-04-01T00:00:00.000Z",
                            "commit_count": 2159
                        }
                    ]
    """
    server.addRepoMetric(augur_db.code_changes, 'code-changes')

    """
    @api {get} /repo-groups/:repo_group_id/code-changes-lines Code Changes Lines
    @apiName code-changes-lines
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/Code_Changes_Lines.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID
    @apiParam {string} period Periodicity specification. Possible values: 'day', 'week', 'month', 'year'. Defaults to 'day'
    @apiParam {string} begin_date Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:0'
    @apiParam {string} end_date Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "commit_date": "2018-01-01T00:00:00.000Z",
                            "repo_id": 1,
                            "added": 640098,
                            "removed": 694608
                        },
                        {
                            "commit_date": "2019-01-01T00:00:00.000Z",
                            "repo_id": 1,
                            "added": 56549,
                            "removed": 48962
                        },
                        {
                            "commit_date": "2014-01-01T00:00:00.000Z",
                            "repo_id": 25001,
                            "added": 19,
                            "removed": 1
                        },
                        {
                            "commit_date": "2015-01-01T00:00:00.000Z",
                            "repo_id": 25001,
                            "added": 429535,
                            "removed": 204015
                        }
                    ]
    """
    server.addRepoGroupMetric(augur_db.code_changes_lines, 'code-changes-lines')

    """
    @api {get} /repo-groups/:repo_group_id/repos/:repo_id/code-changes-lines Code Changes Lines
    @apiName code-changes-lines
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/Code_Changes_Lines.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID.
    @apiParma {String} repo_id Repository ID.
    @apiParam {string} period Periodicity specification. Possible values: 'day', 'week', 'month', 'year'. Defaults to 'day'
    @apiParam {string} begin_date Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:0'
    @apiParam {string} end_date Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "commit_date": "2014-01-01T00:00:00.000Z",
                            "added": 19,
                            "removed": 1
                        },
                        {
                            "commit_date": "2015-01-01T00:00:00.000Z",
                            "added": 429535,
                            "removed": 204015
                        },
                        {
                            "commit_date": "2016-01-01T00:00:00.000Z",
                            "added": 2739765,
                            "removed": 944568
                        },
                        {
                            "commit_date": "2017-01-01T00:00:00.000Z",
                            "added": 3945001,
                            "removed": 1011396
                        }
                    ]
    """
    server.addRepoMetric(augur_db.code_changes_lines, 'code-changes-lines')

    """
    @api {get} /repo-groups/:repo_group_id/issues-new Issues New
    @apiName issues-new
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/Issues_New.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID
    @apiParam {string} period Periodicity specification. Possible values: 'day', 'week', 'month', 'year'. Defaults to 'day'
    @apiParam {string} begin_date Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:0'
    @apiParam {string} end_date Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "issue_date": "2019-05-01T00:00:00.000Z",
                            "repo_id": 1,
                            "issues": 3
                        },
                        {
                            "issue_date": "2019-05-01T00:00:00.000Z",
                            "repo_id": 25001,
                            "issues": 1
                        }
                    ]
    """
    server.addRepoGroupMetric(augur_db.issues_new, 'issues-new')

    """
    @api {get} /repo-groups/:repo_group_id/repos/:repo_id/issues-new Issues New
    @apiName issues-new
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/Issues_New.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID.
    @apiParma {String} repo_id Repository ID.
    @apiParam {string} period Periodicity specification. Possible values: 'day', 'week', 'month', 'year'. Defaults to 'day'
    @apiParam {string} begin_date Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:0'
    @apiParam {string} end_date Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "issue_date": "2019-05-01T00:00:00.000Z",
                            "issues": 1
                        },
                        {
                            "issue_date": "2019-06-01T00:00:00.000Z",
                            "issues": 31
                        }
                    ]
    """
    server.addRepoMetric(augur_db.issues_new, 'issues-new')

    """
    @api {get} /repo-groups/:repo_group_id/issues-active Issues Active
    @apiName issues-active
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/Issues_Active.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID
    @apiParam {string} period Periodicity specification. Possible values: 'day', 'week', 'month', 'year'. Defaults to 'day'
    @apiParam {string} begin_date Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:0'
    @apiParam {string} end_date Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "date": "2019-05-01T00:00:00.000Z",
                            "repo_id": 21326,
                            "issues": 27
                        },
                        {
                            "date": "2019-05-01T00:00:00.000Z",
                            "repo_id": 21327,
                            "issues": 54
                        }
                    ]
    """
    server.addRepoGroupMetric(augur_db.issues_active, 'issues-active')

    """
    @api {get} /repo-groups/:repo_group_id/issues-active Issues Active
    @apiName issues-active
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/Issues_Active.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID.
    @apiParma {String} repo_id Repository ID.
    @apiParam {string} period Periodicity specification. Possible values: 'day', 'week', 'month', 'year'. Defaults to 'day'
    @apiParam {string} begin_date Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:0'
    @apiParam {string} end_date Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "date": "2015-07-01T00:00:00.000Z",
                            "issues": 32
                        },
                        {
                            "date": "2015-08-01T00:00:00.000Z",
                            "issues": 62
                        }
                    ]
    """
    server.addRepoMetric(augur_db.issues_active, 'issues-active')

    """
    @api {get} /repo-groups/:repo_group_id/issues-closed Issues Closed
    @apiName issues-closed
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/Issues_Closed.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID
    @apiParam {string} period Periodicity specification. Possible values: 'day', 'week', 'month', 'year'. Defaults to 'day'
    @apiParam {string} begin_date Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:0'
    @apiParam {string} end_date Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    TODO
    """
    server.addRepoGroupMetric(augur_db.issues_closed, 'issues-closed')

    """
    @api {get} /repo-groups/:repo_group_id/repos/:repo_id/issues-closed Issues Closed
    @apiName issues-closed
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/Issues_New.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID.
    @apiParma {String} repo_id Repository ID.
    @apiParam {string} period Periodicity specification. Possible values: 'day', 'week', 'month', 'year'. Defaults to 'day'
    @apiParam {string} begin_date Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:0'
    @apiParam {string} end_date Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    TODO
    """
    server.addRepoMetric(augur_db.issues_closed, 'issues-closed')

    """
    @api {get} /repo-groups/:repo_group_id/issue-duration Issue Duration
    @apiName issue-duration
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/focus_areas/code_development.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "repo_id": 21682,
                            "issue_id": 41786,
                            "duration": "0 days 00:56:26.000000000"
                        },
                        {
                            "repo_id": 21682,
                            "issue_id": 41787,
                            "duration": "0 days 13:25:04.000000000"
                        }
                    ]
    """
    server.addRepoGroupMetric(augur_db.issue_duration, 'issue-duration')

    """
    @api {get} /repo-groups/:repo_group_id/repos/:repo_id/issue-backlog Issue Duration
    @apiName issue-duration
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/focus_areas/code_development.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID.
    @apiParma {String} repo_id Repository ID.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "repo_id": 21682,
                            "issue_id": 41792,
                            "duration": "2 days 19:13:23.000000000"
                        },
                        {
                            "repo_id": 21682,
                            "issue_id": 41793,
                            "duration": "0 days 00:11:26.000000000"
                        }
                    ]
    """
    server.addRepoMetric(augur_db.issue_duration, 'issue-duration')

    """
    @api {get} /repo-groups/:repo_group_id/issue-backlog Issue Backlog
    @apiName issue-backlog
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/focus_areas/code_development.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "repo_id": 1,
                            "issue_backlog": 3
                        },
                        {
                            "repo_id": 25001,
                            "issue_backlog": 32
                        }
                    ]
    """
    server.addRepoGroupMetric(augur_db.issue_backlog, 'issue-backlog')

    """
    @api {get} /repo-groups/:repo_group_id/repos/:repo_id/issue-backlog Issue Backlog
    @apiName issue-backlog
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/focus_areas/code_development.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID.
    @apiParma {String} repo_id Repository ID.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "issue_backlog": 3
                        }
                    ]
    """
    server.addRepoMetric(augur_db.issue_backlog, 'issue-backlog')

    # @server.app.route('/{}/repo-groups/<repo_group_id>/code-changes'.format(server.api_version))
    # def code_changes_repo_group_route(repo_group_id):
    #     period = request.args.get('period', 'day')
    #     begin_date = request.args.get('begin_date')
    #     end_date = request.args.get('end_date')

    #     kwargs = {'repo_group_id': repo_group_id, 'period': period,
    #               'begin_date': begin_date, 'end_date': end_date}

    #     data = server.transform(augur_db.code_changes,
    #                             args=[],
    #                             kwargs=kwargs)

    #     return Response(response=data, status=200, mimetype='application/json')

    # @server.app.route('/{}/repo-groups/<repo_group_id>/repo/<repo_id>/code-changes'.format(server.api_version))
    # def code_changes_repo_route(repo_group_id, repo_id):
    #     period = request.args.get('period', 'day')
    #     begin_date = request.args.get('begin_date')
    #     end_date = request.args.get('end_date')

    #     kwargs = {'repo_group_id': repo_group_id, 'repo_id': repo_id,
    #               'period': period, 'begin_date': begin_date,
    #               'end_date': end_date}

    #     data = server.transform(augur_db.code_changes,
    #                             args=[],
    #                             kwargs=kwargs)

    #     return Response(response=data, status=200, mimetype='application/json')

    """
    @api {get} /repo-groups/:repo_group_id/pull-requests-merge-contributor-new New Contributors of Commits(Repo Group)
    @apiName New Contributors of Commits(Repo Group)
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/pull-requests-merge-contributor-new.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID
    @apiParam {string} [period="day"] Periodicity specification. Possible values: 'day', 'week', 'month', 'year'. Defaults to 'day'
    @apiParam {string} [begin_date="1970-1-1 0:0:1"] Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:1'
    @apiParam {string} [end_date] Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "commit_date": "2018-01-01T00:00:00.000Z",
                            "count": 5140
                        },
                        {
                            "commit_date": "2019-01-01T00:00:00.000Z",
                            "commit_count": 711
                        }
                    ]
    """
    server.addRepoGroupMetric(
        augur_db.pull_requests_merge_contributor_new, 'pull-requests-merge-contributor-new')

    """
    @api {get} /repo-groups/:repo_group_id/repos/:repo_id/pull-requests-merge-contributor-new New Contributors of Commits(Repo)
    @apiName New Contributors of Commits(Repo)
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/pull-requests-merge-contributor-new.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID.
    @apiParma {String} repo_id Repository ID.
    @apiParam {string} [period="day"] Periodicity specification. Possible values: 'day', 'week', 'month', 'year'. Defaults to 'day'
    @apiParam {string} [begin_date="1970-1-1 0:0:1"] Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:1'
    @apiParam {string} [end_date] Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "commit_date": "2018-01-01T00:00:00.000Z",
                            "count": 2287
                        },
                        {
                            "commit_date": "2018-02-01T00:00:00.000Z",
                            "count": 1939
                        }
                    ]
    """
    server.addRepoMetric(
        augur_db.pull_requests_merge_contributor_new, 'pull-requests-merge-contributor-new')

    """
    @api {get} /repo-groups/:repo_group_id/issues-first-time-opened New Contributors of Issues(Repo Group)
    @apiName New Contributors of Issues(Repo Group)
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/issues-first-time-opened.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID
    @apiParam {string} [period="day"] Periodicity specification. Possible values: 'day', 'week', 'month', 'year'. Defaults to 'day'
    @apiParam {string} [begin_date="1970-1-1 0:0:1"] Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:1'
    @apiParam {string} [end_date] Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "issue_date": "2018-05-20T00:00:00.000Z",
                            "count": 3
                        },
                        {
                            "issue_date": "2019-06-03T00:00:00.000Z",
                            "count": 23
                        }
                    ]
    """
    server.addRepoGroupMetric(
        augur_db.issues_first_time_opened, 'issues-first-time-opened')

    """
    @api {get} /repo-groups/:repo_group_id/repos/:repo_id/issues-first-time-opened New Contributors of Issues(Repo)
    @apiName New Contributors of Issues(Repo)
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/issues-first-time-opened.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID.
    @apiParma {String} repo_id Repository ID.
    @apiParam {string} [period="day"] Periodicity specification. Possible values: 'day', 'week', 'month', 'year'. Defaults to 'day'
    @apiParam {string} [begin_date="1970-1-1 0:0:1"] Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:1'
    @apiParam {string} [end_date] Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "issue_date": "2018-05-20T00:00:00.000Z",
                            "count": 3
                        },
                        {
                            "issue_date": "2019-06-03T00:00:00.000Z",
                            "count": 23
                        }
                    ]
    """
    server.addRepoMetric(
        augur_db.issues_first_time_opened, 'issues-first-time-opened')

    """
    @api {get} /repo-groups/:repo_group_id/issues-first-time-closed Closed Issues New Contributor(Repo Group)
    @apiName Closed Issues New Contributors(Repo Group)
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/issues-first-time-closed.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID
    @apiParam {string} [period="day"] Periodicity specification. Possible values: 'day', 'week', 'month', 'year'. Defaults to 'day'
    @apiParam {string} [begin_date="1970-1-1 0:0:1"] Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:1'
    @apiParam {string} [end_date] Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "issue_date": "2018-05-20T00:00:00.000Z",
                            "count": 3
                        },
                        {
                            "issue_date": "2019-06-03T00:00:00.000Z",
                            "count": 23
                        }
                    ]
    """
    server.addRepoGroupMetric(
        augur_db.issues_first_time_closed, 'issues-first-time-closed')

    """
    @api {get} /repo-groups/:repo_group_id/repos/:repo_id/issues-first-time-closed Closed Issues New Contributors(Repo)
    @apiName Closed Issues New Contributors(Repo)
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/issues-first-time-closed.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID.
    @apiParma {String} repo_id Repository ID.
    @apiParam {string} [period="day"] Periodicity specification. Possible values: 'day', 'week', 'month', 'year'. Defaults to 'day'
    @apiParam {string} [begin_date="1970-1-1 0:0:1"] Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:1'
    @apiParam {string} [end_date] Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "issue_date": "2018-05-20T00:00:00.000Z",
                            "count": 3
                        },
                        {
                            "issue_date": "2019-06-03T00:00:00.000Z",
                            "count": 23
                        }
                    ]
    """
    server.addRepoMetric(
        augur_db.issues_first_time_closed, 'issues-first-time-closed')

    """
    @api {get} /repo-groups/:repo_group_id/sub-projects Sub-Projects(Repo Group)
    @apiName Sub-Projects(Repo Group)
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/sub-projects.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID
    @apiParam {string} [begin_date="1970-1-1 0:0:1"] Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:1'
    @apiParam {string} [end_date] Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "sub_protject_count": 2
                        }
                    ]
    """
    server.addRepoGroupMetric(
        augur_db.sub_projects, 'sub-projects')

    """
    @api {get} /repo-groups/:repo_group_id/repos/:repo_id/sub-projects Sub-Projects(Repo)
    @apiName Sub-Projects(Repo)
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/sub-projects.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID.
    @apiParma {String} repo_id Repository ID.
    @apiParam {string} [begin_date="1970-1-1 0:0:1"] Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:1'
    @apiParam {string} [end_date] Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "sub_protject_count": 2
                        }
                    ]
    """
    server.addRepoMetric(
        augur_db.sub_projects, 'sub-projects')

    """
    @api {get} /repo-groups/:repo_group_id/contributors Contributors(Repo Group)
    @apiName Contributors(Repo Group)
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/contributors.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID
    @apiParam {string} [begin_date="1970-1-1 0:0:1"] Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:1'
    @apiParam {string} [end_date] Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "user": 1,
                            "commits": 0,
                            "issues": 2,
                            "commit_comments": 0,
                            "issue_comments": 0,
                            "pull_requests": 0,
                            "pull_request_comments": 0,
                            "total": 2
                        },
                        {
                            "user": 2,
                            "commits": 0,
                            "issues": 2,
                            "commit_comments": 0,
                            "issue_comments": 0,
                            "pull_requests": 0,
                            "pull_request_comments": 0,
                            "total": 2
                        }
                    ]
    """
    server.addRepoGroupMetric(
        augur_db.contributors, 'contributors')

    """
    @api {get} /repo-groups/:repo_group_id/repos/:repo_id/contributors Contributors(Repo)
    @apiName Contributors(Repo)
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/contributors.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID.
    @apiParma {String} repo_id Repository ID.
    @apiParam {string} [begin_date="1970-1-1 0:0:1"] Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:1'
    @apiParam {string} [end_date] Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                       {
                            "user": 1,
                            "commits": 0,
                            "issues": 2,
                            "commit_comments": 0,
                            "issue_comments": 0,
                            "pull_requests": 0,
                            "pull_request_comments": 0,
                            "total": 2
                        },
                        {
                            "user": 2,
                            "commits": 0,
                            "issues": 2,
                            "commit_comments": 0,
                            "issue_comments": 0,
                            "pull_requests": 0,
                            "pull_request_comments": 0,
                            "total": 2
                        }
                    ]
    """
    server.addRepoMetric(
        augur_db.contributors, 'contributors')

    """
    @api {get} /repo-groups/:repo_group_id/contributors-new New Contributors(Repo Group)
    @apiName New Contributors(Repo Group)
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/contributors-new.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID
    @apiParam {string} [period="day"] Periodicity specification. Possible values: 'day', 'week', 'month', 'year'. Defaults to 'day'
    @apiParam {string} [begin_date="1970-1-1 0:0:1"] Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:1'
    @apiParam {string} [end_date] Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "contribute_at": "2018-05-20T00:00:00.000Z",
                            "count": 3
                        },
                        {
                            "contribute_at": "2019-06-03T00:00:00.000Z",
                            "count": 23
                        }
                    ]
    """
    server.addRepoGroupMetric(
        augur_db.contributors_new, 'contributors-new')

    """
    @api {get} /repo-groups/:repo_group_id/repos/:repo_id/contributors-new New Contributors(Repo)
    @apiName New Contributors(Repo)
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/contributors-new.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID.
    @apiParma {String} repo_id Repository ID.
    @apiParam {string} [period="day"] Periodicity specification. Possible values: 'day', 'week', 'month', 'year'. Defaults to 'day'
    @apiParam {string} [begin_date="1970-1-1 0:0:1"] Beginning date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to '1970-1-1 0:0:1'
    @apiParam {string} [end_date] Ending date specification. Possible values: '2018', '2018-05', '2019-05-01', ..., ' 2017-03-02 05:34:19'. Defaults to current date & time.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "contribute_at": "2018-05-20T00:00:00.000Z",
                            "count": 3
                        },
                        {
                            "contribute_at": "2019-06-03T00:00:00.000Z",
                            "count": 23
                        }
                    ]
    """
    server.addRepoMetric(
        augur_db.contributors_new, 'contributors-new')

    """
    @api {get} /repo-groups/:repo_group_id/issues-open-age Open Issue Age(Repo Group)
    @apiName Open Issue Age(Repo Group)
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/issues-open-age.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "gh_issue_number":1,
                            "issue_title":"Property Place holder for namespaced attributes is not working",
                            "repo_name":"jrugged",
                            "datedifference":2414.0
                        },
                        {
                            "gh_issue_number":2,
                            "issue_title":"Update custom namespace to work with annotation driven config",
                            "repo_name":"jrugged",
                            "datedifference":2414.0
                        }
                    ]
    """
    server.addRepoGroupMetric(
        augur_db.issues_open_age, 'issues-open-age')

    """
    @api {get} /repo-groups/:repo_group_id/repos/:repo_id/issues-open-age Open Issue Age(Repo)
    @apiName Open Issue Age(Repo)
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/issues-open-age.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID.
    @apiParma {String} repo_id Repository ID.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "gh_issue_number":2045,
                            "issue_title":"Add possibility to render partial from subfolder with inheritance",
                            "repo_name":"rails",
                            "datedifference":2899.0
                        },
                        {
                            "gh_issue_number":2686,
                            "issue_title":"Attachments not visible in mail clients when additional inline attachments present",
                            "repo_name":"rails",
                            "datedifference":2856.0
                        }
                    ]
    """
    server.addRepoMetric(
        augur_db.issues_open_age, 'issues-open-age')

    """
    @api {get} /repo-groups/:repo_group_id/issues-closed-resolution-duration Closed Issue Resolution Duration(Repo Group)
    @apiName Closed Issue Resolution Duration(Repo Group)
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/issues-closed-resolution-duration.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID
    @apiSuccessExample {json} Success-Response:
                   [
                        {
                            "repo_name":"incubator-dubbo",
                            "gh_issue_number":4110,
                            "issue_title":"rm incubating word",
                            "created_at":"2019-05-22T03:18:13.000Z",
                            "closed_at":"2019-05-22T05:27:29.000Z",
                            "diffdate":0.0
                        },
                        {
                            "repo_name":"incubator-dubbo",
                            "gh_issue_number":4111,
                            "issue_title":"nacos registry serviceName may conflict",
                            "created_at":"2019-05-22T03:30:23.000Z",
                            "closed_at":"2019-05-23T14:36:17.000Z",
                            "diffdate":1.0
                        }
                    ]
    """
    server.addRepoGroupMetric(
        augur_db.issues_closed_resolution_duration, 'issues-closed-resolution-duration')

    """
    @api {get} /repo-groups/:repo_group_id/repos/:repo_id/issues-closed-resolution-duration Closed Issue Resolution Duration(Repo)
    @apiName Closed Issue Resolution Duration(Repo)
    @apiGroup Evolution
    @apiDescription <a href="https://github.com/chaoss/wg-evolution/blob/master/metrics/issues-closed-resolution-duration.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID.
    @apiParma {String} repo_id Repository ID.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "gh_issue_number":4223,
                            "issue_title":"Cloud Native PR",
                            "created_at":"2019-05-31T07:55:44.000Z",
                            "closed_at":"2019-06-17T03:12:48.000Z",
                            "diffdate":16.0
                        },
                        {
                            "gh_issue_number":4131,
                            "issue_title":"Reduce context switching cost by optimizing thread model on consumer side.",
                            "created_at":"2019-05-23T06:18:21.000Z",
                            "closed_at":"2019-06-03T08:07:27.000Z",
                            "diffdate":11.0
                        }
                    ]
    """
    server.addRepoMetric(
        augur_db.issues_closed_resolution_duration, 'issues-closed-resolution-duration')


    #####################################
    ###              RISK             ###
    #####################################

    """
    @api {get} /repo-groups/:repo_group_id/cii-best-practices-badge CII Best Practices Badge
    @apiName cii-best-practices-badge
    @apiGroup Risk
    @apiDescription <a href="https://github.com/chaoss/wg-risk/blob/master/focus-areas/security.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "repo_id": 21277,
                            "badge_level": "passing"
                        },
                        {
                            "repo_id": 21252,
                            "badge_level": "in_progress"
                        }
                    ]
    """
    server.addRepoGroupMetric(augur_db.cii_best_practices_badge, 'cii-best-practices-badge')

    """
    @api {get} /repo-groups/:repo_group_id/cii-best-practices-badge CII Best Practices Badge
    @apiName cii-best-practices-badge
    @apiGroup Risk
    @apiDescription <a href="https://github.com/chaoss/wg-risk/blob/master/focus-areas/security.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID.
    @apiParma {String} repo_id Repository ID.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "badge_level": "gold"
                        }
                    ]
    """
    server.addRepoMetric(augur_db.cii_best_practices_badge, 'cii-best-practices-badge')

    """
    @api {get} /repo-groups/:repo_group_id/languages Languages
    @apiName languages
    @apiGroup Risk
    @apiDescription <a href="https://github.com/chaoss/wg-risk/blob/master/focus-areas/security.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "repo_id": 21277,
                            "primary_language": "Go"
                        },
                        {
                            "repo_id": 21252,
                            "primary_language": "PHP"
                        }
                    ]
    """
    server.addRepoGroupMetric(augur_db.languages, 'languages')

    """
    @api {get} /repo-groups/:repo_group_id/languages Languages
    @apiName languages
    @apiGroup Risk
    @apiDescription <a href="https://github.com/chaoss/wg-risk/blob/master/focus-areas/security.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID.
    @apiParma {String} repo_id Repository ID.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "primary_language":"PHP"
                        }
                    ]
    """
    server.addRepoMetric(augur_db.languages, 'languages')

    """
    @api {get} /repo-groups/:repo_group_id/license-declared License Declared
    @apiName license-declared
    @apiGroup Risk
    @apiDescription <a href="https://github.com/chaoss/wg-risk/blob/master/focus-areas/licensing.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "repo_id": 21277,
                            "license": "Apache-2.0"
                        },
                        {
                            "repo_id": 21252,
                            "license": "Apache-2.0"
                        }
                    ]
    """
    server.addRepoGroupMetric(augur_db.license_declared, 'license-declared')

    """
    @api {get} /repo-groups/:repo_group_id/license-declared License Declared
    @apiName license-declared
    @apiGroup Risk
    @apiDescription <a href="https://github.com/chaoss/wg-risk/blob/master/focus-areas/licensing.md">CHAOSS Metric Definition</a>
    @apiParam {String} repo_group_id Repository Group ID.
    @apiParma {String} repo_id Repository ID.
    @apiSuccessExample {json} Success-Response:
                    [
                        {
                            "license": "Apache-2.0"
                        }
                    ]
    """
    server.addRepoMetric(augur_db.license_declared, 'license-declared')
