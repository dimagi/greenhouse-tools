import csv
import json
import sys

import os

from greenhouse.api import GreenhouseClient

USAGE = '''
To use this tool, call it with: python cli.py <api_key> [output_filename]

Go to https://app.greenhouse.io/configure/dev_center/credentials to find your API key
(note that you must be a Greenhouse superuser to use the APIs)
'''


def run_cli(api_key, output_file=None):
    print('starting the greenhouse command line interface... welcome!')
    client = GreenhouseClient(api_key)
    jobs = client.list_jobs()
    for i, job in enumerate(jobs):
        print('{}: {}'.format(i, job_to_string(job)))

    choice = int(input('\nWhat job would you like to analyze? Enter the number below:\n'))
    chosen_job = jobs[choice]
    print('Getting applications to {}...'.format(job_to_string(chosen_job)))
    applications = client.get_applications_for_job(chosen_job)
    print('Found {} applications, retrieving scorecards (this might take a while)... '.format(len(applications)))
    # will contain application, scorecard_list tuples
    all_scorecards = []
    total_scorecards_found = 0
    for i, application in enumerate(applications):
        scorecards = client.get_scorecards_for_application(application)
        all_scorecards.append((application, scorecards))
        total_scorecards_found += len(scorecards)
        # if total_scorecards_found > 20:
        #     break
        print('processed {}/{} applications (found {} total score cards)'.format(i, len(applications), total_scorecards_found))

    output_file = output_file or 'output/{} - scorecards.csv'.format(job_to_string(chosen_job))
    serialize_scorecards_to_file(all_scorecards, output_file)


def job_to_string(job):
    return '{} in {} (created: {})'.format(job['title'], job['location']['name'], job['created_at'][:10])


def serialize_scorecards_to_file(all_scorecards, output_file):
    if os.path.dirname(output_file):
        try:
            os.makedirs(os.path.dirname(output_file))
        except FileExistsError:
            # directory already exists
            pass

    # first we have to collect all potential attributes
    all_attributes, flat_scorecards = collect_attributes_and_flatten_scorecards(all_scorecards)
    with open(output_file, 'w') as f:
        field_names = ['outcome', 'overall_recommendation'] + sorted(list(all_attributes))
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        for scorecard in flat_scorecards:
            writer.writerow(scorecard['_reformatted_attributes'])


def collect_attributes_and_flatten_scorecards(all_scorecards):
    attributes = set()
    flattened_scorecards = []
    for application, scorecard_list in all_scorecards:
        for scorecard in scorecard_list:
            scorecard['_reformatted_attributes'] = {}
            for attribute in scorecard['attributes']:
                attribute_id = '{}: {}'.format(attribute['type'], attribute['name'])
                if attribute_id not in attributes:
                    attributes.add(attribute_id)
                scorecard['_reformatted_attributes'][attribute_id] = _text_to_rating(attribute['rating'])
            # import pdb; pdb.set_trace()
            scorecard['application'] = application
            scorecard['_reformatted_attributes']['outcome'] = application['status']
            scorecard['_reformatted_attributes']['overall_recommendation'] = _text_to_rating(scorecard['overall_recommendation'])
            flattened_scorecards.append(scorecard)
    return attributes, flattened_scorecards


def _text_to_rating(text):
    return {
        'definitely_not': 1,
        'no': 2,
        'no_decision': '',
        'mixed': 3,
        'yes': 4,
        'strong_yes': 5,
    }[text]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(0)
    api_key = sys.argv[1]
    output_file_arg = sys.argv[2] if len(sys.argv) > 2 else None
    run_cli(api_key, output_file_arg)
